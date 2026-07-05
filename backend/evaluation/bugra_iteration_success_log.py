"""Log the real iteration where /api/autonomous-repair succeeds.

This script intentionally refuses to run the experiment without OPENAI_API_KEY.
It writes CSV output only after real endpoint calls complete.
"""

from __future__ import annotations

import csv
import os
import sys
from collections import Counter
from pathlib import Path

from bugra_experiment_cases import INVALID_PLANTUML_CASES


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
AI_CORE = ROOT / "ai_core" / "src"
RESULTS = BACKEND / "evaluation" / "results"
OUTPUT_CSV = RESULTS / "bugra_iteration_success_log.csv"


def configure_paths() -> None:
    sys.path.insert(0, str(BACKEND))
    sys.path.insert(0, str(AI_CORE))


def require_openai_key() -> bool:
    if os.getenv("OPENAI_API_KEY"):
        return True
    print("OPENAI_API_KEY bulunamadi. Iterasyon basari logu calistirilmadi; CSV uretilmedi.")
    print("API anahtari olmadan bu gorev gercek anlamda tamamlanamaz.")
    return False


def successful_repair_iteration(response: dict):
    """Convert the internal agent counter to a 1-based repair iteration."""
    if not response["basarili"]:
        return None
    agent_count = response.get("agent_iteration_count")
    if agent_count is None:
        return None
    return max(int(agent_count) - 1, 0)


def main() -> int:
    if not require_openai_key():
        return 2

    configure_paths()
    from src.api.endpoints import OtonomOnarimGirdisi, otonom_onarim

    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = []

    for case in INVALID_PLANTUML_CASES:
        response = otonom_onarim(
            OtonomOnarimGirdisi(
                plantuml_kodu=case["plantuml_kodu"],
                srs_metni=case["srs_metni"],
                max_iterasyon=3,
            )
        )
        success_iteration = successful_repair_iteration(response)
        rows.append(
            {
                "case_id": case["case_id"],
                "basarili_iterasyon": success_iteration or "BASARISIZ",
                "final_basarili": response["basarili"],
            }
        )
        print(
            f"{case['case_id']} final_basarili={response['basarili']} "
            f"basarili_iterasyon={rows[-1]['basarili_iterasyon']}"
        )

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["case_id", "basarili_iterasyon", "final_basarili"],
        )
        writer.writeheader()
        writer.writerows(rows)

    distribution = Counter(row["basarili_iterasyon"] for row in rows)
    print(f"CSV yazildi: {OUTPUT_CSV}")
    print("DAGILIM")
    print(f"1. iterasyon: {distribution.get(1, 0)}")
    print(f"2. iterasyon: {distribution.get(2, 0)}")
    print(f"3. iterasyon: {distribution.get(3, 0)}")
    print(f"basarisiz: {distribution.get('BASARISIZ', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
