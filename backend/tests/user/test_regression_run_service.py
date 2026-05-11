from services.user_service.app.services.regression_run_service import (
    RegressionRunService,
)


def test_build_result_summary():
    service = RegressionRunService(session=None)

    class Candidate:
        title = "Login test"
        normalized_score = 95

    summary = service._build_result_summary(
        candidates=[Candidate()],
        search_mode="semantic",
    )

    assert "Найдено 1" in summary


def test_build_result_summary_empty():
    service = RegressionRunService(session=None)

    summary = service._build_result_summary(
        candidates=[],
        search_mode="semantic",
    )

    assert "не найдены" in summary.lower()