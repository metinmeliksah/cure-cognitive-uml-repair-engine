"""Run real latency measurements for /api/autonomous-repair.

This script intentionally refuses to run the experiment without OPENAI_API_KEY.
It writes CSV output only after real endpoint calls complete.
"""

from __future__ import annotations

import csv
import os
import sys
import time
from pathlib import Path

from autonomous_repair_cases import INVALID_PLANTUML_CASES


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
AI_CORE = ROOT / "ai_core" / "src"
RESULTS = BACKEND / "evaluation" / "results"
OUTPUT_CSV = RESULTS / "autonomous_repair_latency_experiment.csv"


def configure_paths() -> None:
    sys.path.insert(0, str(BACKEND))
    sys.path.insert(0, str(AI_CORE))


def require_openai_key() -> bool:
    if os.getenv("OPENAI_API_KEY"):
        return True
    print("OPENAI_API_KEY bulunamadi. Deney calistirilmadi; CSV uretilmedi.")
    print("Bu script gercek /api/autonomous-repair LLM cagrilari icin API anahtari gerektirir.")
    return False


def repair_attempt_count(response: dict) -> int:
    """Convert the internal agent counter to actual repair attempts."""
    agent_count = response.get("agent_iteration_count")
    if agent_count is not None:
        return max(int(agent_count) - 1, 0)
    return max(len(response["iterasyonlar"]) - 1, 0)


def main() -> int:
    if not require_openai_key():
        return 2

    configure_paths()
    from src.api.endpoints import AutonomousRepairRequest, autonomous_repair

    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = []
    started = time.time()

    for case in INVALID_PLANTUML_CASES:
        response = autonomous_repair(
            AutonomousRepairRequest(
                plantuml_kodu=case["plantuml_kodu"],
                srs_metni=case["srs_metni"],
                max_iterations=3,
            )
        )
        rows.append(
            {
                "case_id": case["case_id"],
                "girdi_turu": case["girdi_turu"],
                "basarili": response["basarili"],
                "sure_saniye": response["sure_saniye"],
                "iterasyon_sayisi": repair_attempt_count(response),
            }
        )
        print(
            f"{case['case_id']} basarili={response['basarili']} "
            f"sure_saniye={response['sure_saniye']} "
            f"iterasyon_sayisi={rows[-1]['iterasyon_sayisi']}"
        )

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["case_id", "girdi_turu", "basarili", "sure_saniye", "iterasyon_sayisi"],
        )
        writer.writeheader()
        writer.writerows(rows)

    elapsed = round(time.time() - started, 3)
    successful = sum(1 for row in rows if row["basarili"])
    print(f"CSV yazildi: {OUTPUT_CSV}")
    print(f"Toplam sure_saniye={elapsed}; basarili={successful}/{len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
