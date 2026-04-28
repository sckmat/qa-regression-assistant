import json
from typing import Any

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.clients.data_service_client import DataServiceClient
from services.user_service.app.core.config import settings
from services.user_service.app.repositories.project_repository import (
    ProjectRepository,
)
from services.user_service.app.repositories.user_preference_repository import (
    UserPreferenceRepository,
)


class TestCaseGatewayService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.project_repository = ProjectRepository(session)
        self.data_service_client = DataServiceClient(
            base_url=settings.data_service_base_url,
        )

    async def list_test_cases(self, project_id: int) -> list[dict[str, Any]]:
        await self._ensure_project_exists(project_id)
        return await self.data_service_client.list_test_cases(project_id)

    async def get_test_case(self, test_case_id: int) -> dict[str, Any]:
        return await self.data_service_client.get_test_case(test_case_id)

    async def import_test_cases_file(
        self,
        project_id: int,
        file: UploadFile,
    ) -> dict[str, Any]:
        await self._ensure_project_exists(project_id)

        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required.",
            )

        if not file.filename.lower().endswith(".json"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only .json files are supported.",
            )

        raw_bytes = await file.read()
        if not raw_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        try:
            raw_text = raw_bytes.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to decode file as UTF-8 JSON.",
            ) from exc

        try:
            parsed_payload = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid JSON file: {exc}",
            ) from exc

        if not isinstance(parsed_payload, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="JSON root must be an object.",
            )

        items = parsed_payload.get("items")
        if not isinstance(items, list):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="JSON must contain field 'items' as array.",
            )

        import_result = await self.data_service_client.import_test_cases(
            project_id=project_id,
            payload=parsed_payload,
        )

        pref_repo = UserPreferenceRepository(self.session)
        project = await self.project_repository.get_by_id(project_id)
        pref = await pref_repo.get_or_create(project.owner_user_id)

        provider = pref.preferred_llm_provider

        print(f"[IMPORT+REINDEX] provider={provider}")

        try:
            reindex_result = await self.data_service_client.reindex_test_cases(
                project_id,
                embedding_provider=provider,
            )

            return {
                "status": "completed",
                "message": "Тест-кейсы успешно загружены и переиндексированы.",
                "import_result": import_result,
                "reindex_result": reindex_result,
            }

        except HTTPException as exc:
            return {
                "status": "partial_success",
                "message": "Тест-кейсы загружены, но переиндексация не завершилась.",
                "import_result": import_result,
                "reindex_error": exc.detail,
            }

    async def reindex_test_cases(self, project_id: int) -> dict[str, Any]:
        await self._ensure_project_exists(project_id)

        pref_repo = UserPreferenceRepository(self.session)
        project = await self.project_repository.get_by_id(project_id)
        pref = await pref_repo.get_or_create(project.owner_user_id)

        provider = pref.preferred_llm_provider

        print(f"[REINDEX] provider={provider}")

        return await self.data_service_client.reindex_test_cases(
            project_id,
            embedding_provider=provider,  # 🔥
        )

    async def _ensure_project_exists(self, project_id: int) -> None:
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id={project_id} not found.",
            )