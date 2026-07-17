"""Shared invalid PlantUML cases for the AI-core experiments."""

INVALID_PLANTUML_CASES = [
    {
        "case_id": "CASE-001",
        "girdi_turu": "missing_startuml",
        "srs_metni": "The UserManager uses the AuthService to authenticate users.",
        "plantuml_kodu": "class UserManager {}\nclass AuthService {}\nUserManager --> AuthService\n@enduml",
    },
    {
        "case_id": "CASE-002",
        "girdi_turu": "missing_enduml",
        "srs_metni": "The OrderService creates Order records and uses PaymentGateway.",
        "plantuml_kodu": "@startuml\nclass OrderService {}\nclass PaymentGateway {}\nOrderService --> PaymentGateway",
    },
    {
        "case_id": "CASE-003",
        "girdi_turu": "no_class",
        "srs_metni": "The ReportService generates reports from AnalyticsEngine data.",
        "plantuml_kodu": "@startuml\nReportService --> AnalyticsEngine\n@enduml",
    },
    {
        "case_id": "CASE-004",
        "girdi_turu": "duplicate_class",
        "srs_metni": "The InventoryService updates StockRepository records.",
        "plantuml_kodu": "@startuml\nclass InventoryService {}\nclass InventoryService {}\n@enduml",
    },
    {
        "case_id": "CASE-005",
        "girdi_turu": "empty_diagram",
        "srs_metni": "The NotificationService sends messages through EmailGateway.",
        "plantuml_kodu": "@startuml\n@enduml",
    },
    {
        "case_id": "CASE-006",
        "girdi_turu": "missing_both_tags",
        "srs_metni": "The BillingService calls InvoiceGenerator for monthly invoices.",
        "plantuml_kodu": "class BillingService {}\nclass InvoiceGenerator {}\nBillingService --> InvoiceGenerator",
    },
    {
        "case_id": "CASE-007",
        "girdi_turu": "duplicate_and_missing_end",
        "srs_metni": "The ProfileController uses ProfileService and AuditLogger.",
        "plantuml_kodu": "@startuml\nclass ProfileController {}\nclass ProfileController {}\nclass AuditLogger {}",
    },
    {
        "case_id": "CASE-008",
        "girdi_turu": "lowercase_duplicate",
        "srs_metni": "The SearchService queries SearchRepository for catalog results.",
        "plantuml_kodu": "@startuml\nclass searchService {}\nclass searchService {}\n@enduml",
    },
    {
        "case_id": "CASE-009",
        "girdi_turu": "only_relation",
        "srs_metni": "The CartService uses PricingEngine before checkout.",
        "plantuml_kodu": "CartService --> PricingEngine",
    },
    {
        "case_id": "CASE-010",
        "girdi_turu": "comment_only",
        "srs_metni": "The TicketService assigns tickets to SupportAgent.",
        "plantuml_kodu": "@startuml\n' no classes are declared here\n@enduml",
    },
    {
        "case_id": "CASE-011",
        "girdi_turu": "duplicate_repository",
        "srs_metni": "The CustomerService stores customer records in CustomerRepository.",
        "plantuml_kodu": "@startuml\nclass CustomerRepository {}\nclass CustomerRepository {}\n@enduml",
    },
    {
        "case_id": "CASE-012",
        "girdi_turu": "missing_start_duplicate",
        "srs_metni": "The ShipmentService notifies TrackingService about status changes.",
        "plantuml_kodu": "class ShipmentService {}\nclass ShipmentService {}\nclass TrackingService {}\n@enduml",
    },
    {
        "case_id": "CASE-013",
        "girdi_turu": "no_class_with_tags",
        "srs_metni": "The PolicyEngine validates PolicyRule objects.",
        "plantuml_kodu": "@startuml\nPolicyEngine : validate()\n@enduml",
    },
    {
        "case_id": "CASE-014",
        "girdi_turu": "missing_end_duplicate",
        "srs_metni": "The DocumentParser sends parsed documents to IndexService.",
        "plantuml_kodu": "@startuml\nclass DocumentParser {}\nclass DocumentParser {}\nclass IndexService {}",
    },
    {
        "case_id": "CASE-015",
        "girdi_turu": "minimal_invalid",
        "srs_metni": "The LoginController delegates authentication to AuthService.",
        "plantuml_kodu": "class LoginController {}",
    },
    {
        "case_id": "CASE-016",
        "girdi_turu": "duplicate_with_relation",
        "srs_metni": "The AuditService stores events in EventStore.",
        "plantuml_kodu": "@startuml\nclass AuditService {}\nclass EventStore {}\nclass EventStore {}\nAuditService --> EventStore\n@enduml",
    },
    {
        "case_id": "CASE-017",
        "girdi_turu": "no_class_relation_with_tags",
        "srs_metni": "The SchedulerService triggers JobExecutor jobs.",
        "plantuml_kodu": "@startuml\nSchedulerService --> JobExecutor\n@enduml",
    },
    {
        "case_id": "CASE-018",
        "girdi_turu": "missing_start_no_class",
        "srs_metni": "The MetricsCollector sends metrics to MonitoringGateway.",
        "plantuml_kodu": "MetricsCollector --> MonitoringGateway\n@enduml",
    },
    {
        "case_id": "CASE-019",
        "girdi_turu": "missing_end_no_class",
        "srs_metni": "The RuleEngine evaluates FraudDetector rules.",
        "plantuml_kodu": "@startuml\nRuleEngine --> FraudDetector",
    },
    {
        "case_id": "CASE-020",
        "girdi_turu": "empty_string",
        "srs_metni": "The UploadService stores files through StorageGateway.",
        "plantuml_kodu": "",
    },
]
