# Zeynep Backend Repair Experiment Log

This is a fresh reproducible experiment log generated from the current repository state.
It should not be described as an original historical run.

## Summary

- Run id: `aa37598e-a614-4ad3-a0ae-858ce90344eb`
- Generated at: `2026-07-06T23:32:07.203374+00:00`
- Scope: backend/src/ocl_engine structural validation and deterministic local repair
- Repair engine: deterministic_backend_repair; no LLM or external API calls
- Total cases: 20
- Successful repairs: 15
- Success rate: 75.0%
- Wilson 95% CI: 53.1% - 88.8%
- Expectation checks passed: 20/20

## Case Results

| Case | Category | Final success | Iterations | Final errors |
|---|---|---:|---:|---|
| R01 | missing_startuml | True | 1 | - |
| R02 | missing_enduml | True | 1 | - |
| R03 | missing_both_boundaries | True | 1 | - |
| R04 | empty_diagram | True | 1 | - |
| R05 | plain_empty_input | True | 1 | - |
| R06 | missing_startuml_with_relation | True | 1 | - |
| R07 | missing_enduml_with_relation | True | 1 | - |
| R08 | missing_both_with_relation | True | 1 | - |
| R09 | only_start_token | True | 1 | - |
| R10 | only_end_token | True | 1 | - |
| R11 | comment_only | True | 1 | - |
| R12 | missing_startuml_pascal_warning | True | 1 | - |
| R13 | missing_enduml_isolated_warning | True | 1 | - |
| R14 | missing_both_god_class_warning | True | 1 | - |
| R15 | whitespace_empty | True | 1 | - |
| R16 | duplicate_class | False | 1 | Tekrar eden sinif ismi: ['UserManager'] |
| R17 | duplicate_class_missing_start | False | 2 | Tekrar eden sinif ismi: ['UserManager'] |
| R18 | duplicate_class_missing_end | False | 2 | Tekrar eden sinif ismi: ['DiagramService'] |
| R19 | duplicate_lowercase | False | 1 | Tekrar eden sinif ismi: ['userManager'] |
| R20 | duplicate_with_relation | False | 1 | Tekrar eden sinif ismi: ['AuthService'] |

## Interpretation

The 15/20 result belongs to this newly generated deterministic backend repair experiment.
It is suitable as repository-backed evidence for the backend repair layer, but it does not
measure the full LLM-based Critic-Healer workflow.
