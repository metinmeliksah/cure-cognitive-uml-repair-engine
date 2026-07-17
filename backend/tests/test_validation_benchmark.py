import os
import sys


BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(BACKEND_ROOT)
sys.path.insert(0, BACKEND_ROOT)
sys.path.insert(0, REPO_ROOT)

from backend.evaluation.validation_benchmark import (
    OCL_CASES,
    SEMANTIC_CASES,
    run_ocl_cases,
    run_semantic_cases,
    wilson_interval,
)
from backend.evaluation.deterministic_repair_experiment import build_report


def test_ocl_validation_sample_matches_expected_flags():
    rows = run_ocl_cases()
    assert len(rows) == len(OCL_CASES)
    failed = [row["id"] for row in rows if not row["passed"]]
    assert failed == []


def test_semantic_validation_sample_matches_expected_flags():
    rows = run_semantic_cases()
    assert len(rows) == len(SEMANTIC_CASES)
    failed = [row["id"] for row in rows if not row["passed"]]
    assert failed == []


def test_wilson_interval_for_paper_figure4_inference():
    interval = wilson_interval(15, 20)
    assert interval["successes"] == 15
    assert interval["total"] == 20
    assert interval["rate"] == 0.75
    assert interval["lower_percent"] == 53.1
    assert interval["upper_percent"] == 88.8


def test_repair_experiment_log_reproduces_15_of_20_success_rate():
    report = build_report()
    assert report["summary"]["total_cases"] == 20
    assert report["summary"]["successful_repairs"] == 15
    assert report["summary"]["failed_repairs"] == 5
    assert report["summary"]["success_rate_percent"] == 75.0
    assert report["summary"]["expectation_matches"] == 20
    assert report["metadata"]["repair_engine"] == "deterministic_backend_repair; no LLM or external API calls"


if __name__ == "__main__":
    tests = [
        test_ocl_validation_sample_matches_expected_flags,
        test_semantic_validation_sample_matches_expected_flags,
        test_wilson_interval_for_paper_figure4_inference,
        test_repair_experiment_log_reproduces_15_of_20_success_rate,
    ]
    passed = 0
    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")
    print(f"Sonuc: {passed}/{len(tests)} test gecti")
