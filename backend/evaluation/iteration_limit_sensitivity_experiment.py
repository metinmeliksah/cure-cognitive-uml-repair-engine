"""Run real max-iteration sensitivity analysis for the LangGraph agent.

This script intentionally refuses to run the experiment without OPENAI_API_KEY.
It writes CSV output only after real LLM calls complete.
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
OUTPUT_CSV = RESULTS / "iteration_limit_sensitivity_experiment.csv"
LIMITS = [2, 4, 5]


def configure_paths() -> None:
    sys.path.insert(0, str(BACKEND))
    sys.path.insert(0, str(AI_CORE))


def require_openai_key() -> bool:
    if os.getenv("OPENAI_API_KEY"):
        return True
    print("OPENAI_API_KEY bulunamadi. Duyarlilik deneyi calistirilmadi; CSV uretilmedi.")
    print("Limit=2/4/5 kosulari gercek OpenAI API anahtari gerektirir.")
    return False


def main() -> int:
    if not require_openai_key():
        return 2

    configure_paths()
    from ai.agent_workflow import UMLMultiAgentSystem
    from src.api.endpoints import _compile_test

    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = []

    for limit in LIMITS:
        started = time.time()
        successful = 0
        total_llm_calls = 0

        for case in INVALID_PLANTUML_CASES:
            agent = UMLMultiAgentSystem(max_iterations=limit)
            before_calls = agent.llm_call_count
            final_state = agent.run(
                original_text=case["srs_metni"],
                initial_uml=case["plantuml_kodu"],
                return_state=True,
            )
            total_llm_calls += agent.llm_call_count - before_calls
            compile_result = _compile_test(final_state["current_uml"])
            if compile_result["basarili"]:
                successful += 1
            print(
                f"limit={limit} {case['case_id']} "
                f"basarili={compile_result['basarili']} "
                f"iteration_count={final_state['iteration_count']} "
                f"llm_calls={agent.llm_call_count - before_calls}"
            )

        elapsed = round(time.time() - started, 3)
        rows.append(
            {
                "limit_degeri": limit,
                "basari_orani": round(successful / len(INVALID_PLANTUML_CASES), 3),
                "toplam_api_cagrisi": total_llm_calls,
                "toplam_sure_saniye": elapsed,
            }
        )
        print(
            f"OZET limit={limit} basari_orani={rows[-1]['basari_orani']} "
            f"toplam_api_cagrisi={total_llm_calls} toplam_sure_saniye={elapsed}"
        )

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["limit_degeri", "basari_orani", "toplam_api_cagrisi", "toplam_sure_saniye"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV yazildi: {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
