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

    async def list_test_cases(self, project_id: int, user_id: int) -> list[dict[str, Any]]:
        await self._ensure_project_access(project_id, user_id)
        return await self.data_service_client.list_test_cases(project_id)

    async def get_test_case(self, test_case_id: int, user_id: int) -> dict[str, Any]:
        test_case = await self.data_service_client.get_test_case(test_case_id)

        project_id = test_case["project_id"]
        await self._ensure_project_access(project_id, user_id)

        return test_case

    async def import_test_cases_file(
        self,
        project_id: int,
        file: UploadFile,
        user_id: int,
    ) -> dict[str, Any]:
        project = await self._ensure_project_access(project_id, user_id)

        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required.")

        if not file.filename.lower().endswith(".json"):
            raise HTTPException(status_code=415, detail="Only .json files are supported.")

        raw_bytes = await file.read()
        if not raw_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        try:
            raw_text = raw_bytes.decode("utf-8-sig")
            parsed_payload = json.loads(raw_text)
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Invalid JSON file.") from exc

        import_result = await self.data_service_client.import_test_cases(
            project_id=project_id,
            payload=parsed_payload,
        )

        pref_repo = UserPreferenceRepository(self.session)
        pref = await pref_repo.get_or_create(project.owner_user_id)

        provider = pref.preferred_llm_provider

        print(f"[IMPORT+REINDEX] provider={provider}")

        reindex_result = await self.data_service_client.reindex_test_cases(
            project_id,
            embedding_provider=provider,
        )

        return {
            "status": "completed",
            "import_result": import_result,
            "reindex_result": reindex_result,
        }

    async def reindex_test_cases(self, project_id: int, user_id: int) -> dict[str, Any]:
        project = await self._ensure_project_access(project_id, user_id)

        pref_repo = UserPreferenceRepository(self.session)
        pref = await pref_repo.get_or_create(project.owner_user_id)

        provider = pref.preferred_llm_provider

        print(f"[REINDEX] provider={provider}")

        return await self.data_service_client.reindex_test_cases(
            project_id,
            embedding_provider=provider,
        )

    async def _ensure_project_access(self, project_id: int, user_id: int):
        project = await self.project_repository.get_by_id(project_id)

        if project is None:
            raise HTTPException(404, "Project not found")

        if project.owner_user_id != user_id:
            raise HTTPException(403, "Access denied")

        return project