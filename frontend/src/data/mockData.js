/**
 * API bağlanana kadar tüm ekranları test etmek için kullanılacak sahte veri.
 * Backend /results/:jobId endpoint'inden döneceği düşünülen JSON yapısını yansıtır.
 */

export const ERROR_TYPES = {
  HALLUCINATION: 'HALLUCINATION',
  DESIGN_SMELL: 'DESIGN_SMELL',
  SYNTAX_ERROR: 'SYNTAX_ERROR',
  MISSING_ELEMENT: 'MISSING_ELEMENT',
  INCONSISTENCY: 'INCONSISTENCY',
};

export const SEVERITY = {
  HIGH: 'HIGH',
  MEDIUM: 'MEDIUM',
  LOW: 'LOW',
};

export const ERROR_STATUS = {
  OPEN: 'OPEN',
  ACKNOWLEDGED: 'ACKNOWLEDGED',
  FIXED: 'FIXED',
};

export const mockErrorReport = {
  job_id: 'job_2026041801',
  status: 'COMPLETED',
  timestamp: '2026-04-18T10:30:00Z',
  document: 'requirements-v2.txt',
  uml_file: 'system-diagram.puml',
  processing_time_ms: 4320,
  summary: {
    total: 9,
    high: 3,
    medium: 4,
    low: 2,
    open: 7,
    acknowledged: 1,
    fixed: 1,
  },
  errors: [
    {
      id: 'err_001',
      type: ERROR_TYPES.HALLUCINATION,
      severity: SEVERITY.HIGH,
      element: 'PaymentGateway',
      element_type: 'Class',
      description:
        'PaymentGateway sınıfı SRS belgesinde tanımlanmamış; diyagramda hatalı olarak yer almaktadır.',
      line: 12,
      suggestion:
        'PaymentGateway sınıfını SRS kapsamı dışında olduğu için diyagramdan kaldırın ya da ilgili gereksinimi belgeye ekleyin.',
      status: ERROR_STATUS.OPEN,
      detected_at: '2026-04-18T10:30:12Z',
    },
    {
      id: 'err_002',
      type: ERROR_TYPES.DESIGN_SMELL,
      severity: SEVERITY.HIGH,
      element: 'UserController',
      element_type: 'Class',
      description:
        'God Class anti-pattern tespit edildi. UserController 23 metot içeriyor; tek sorumluluk ilkesini ihlal ediyor.',
      line: 45,
      suggestion:
        'Sorumlulukları AuthController, ProfileController ve OrderController gibi daha küçük sınıflara ayırın.',
      status: ERROR_STATUS.OPEN,
      detected_at: '2026-04-18T10:30:14Z',
    },
    {
      id: 'err_003',
      type: ERROR_TYPES.MISSING_ELEMENT,
      severity: SEVERITY.HIGH,
      element: 'NotificationService',
      element_type: 'Class',
      description:
        'SRS belgesinde bahsedilen NotificationService sınıfı diyagramda eksik.',
      line: null,
      suggestion:
        'NotificationService sınıfını ve ilgili bağımlılıklarını diyagrama ekleyin.',
      status: ERROR_STATUS.OPEN,
      detected_at: '2026-04-18T10:30:16Z',
    },
    {
      id: 'err_004',
      type: ERROR_TYPES.INCONSISTENCY,
      severity: SEVERITY.MEDIUM,
      element: 'Order → Product',
      element_type: 'Association',
      description:
        'Order ile Product arasındaki çokluk ilişkisi SRS\'de "bir-çok" olarak belirtilmiş; diyagramda "çok-çok" gösteriliyor.',
      line: 78,
      suggestion:
        'Order → Product ilişkisinin kardinalitesini diyagramda 1..* olarak düzeltin.',
      status: ERROR_STATUS.ACKNOWLEDGED,
      detected_at: '2026-04-18T10:30:18Z',
    },
    {
      id: 'err_005',
      type: ERROR_TYPES.HALLUCINATION,
      severity: SEVERITY.MEDIUM,
      element: 'ReportEngine',
      element_type: 'Component',
      description:
        'ReportEngine bileşeni SRS\'de belirtilmemiş; AI tarafından yanlışlıkla eklenmiş olabilir.',
      line: 91,
      suggestion:
        'Gereksinim analizi yaparak ReportEngine\'in kapsama girip girmediğini doğrulayın.',
      status: ERROR_STATUS.OPEN,
      detected_at: '2026-04-18T10:30:20Z',
    },
    {
      id: 'err_006',
      type: ERROR_TYPES.SYNTAX_ERROR,
      severity: SEVERITY.MEDIUM,
      element: 'CustomerRepository',
      element_type: 'Class',
      description:
        'CustomerRepository\'deki findByEmail() metodu PlantUML sözdizimi kurallarını ihlal ediyor; parametre türü eksik.',
      line: 103,
      suggestion:
        'findByEmail(email: String): Customer şeklinde tür bilgisini ekleyin.',
      status: ERROR_STATUS.OPEN,
      detected_at: '2026-04-18T10:30:22Z',
    },
    {
      id: 'err_007',
      type: ERROR_TYPES.DESIGN_SMELL,
      severity: SEVERITY.MEDIUM,
      element: 'DatabaseManager',
      element_type: 'Class',
      description:
        'Singleton anti-pattern tespit edildi. DatabaseManager statik instance kullanıyor; test edilebilirliği düşürüyor.',
      line: 130,
      suggestion:
        'Dependency Injection kullanarak DatabaseManager\'ı test edilebilir hale getirin.',
      status: ERROR_STATUS.OPEN,
      detected_at: '2026-04-18T10:30:24Z',
    },
    {
      id: 'err_008',
      type: ERROR_TYPES.INCONSISTENCY,
      severity: SEVERITY.LOW,
      element: 'User',
      element_type: 'Class',
      description:
        'User sınıfının "email" özniteliği SRS\'de zorunlu olarak tanımlanmış; diyagramda opsiyonel (0..1) gösterilmiş.',
      line: 22,
      suggestion:
        'User.email özniteliğini [1] çokluk ile zorunlu alan olarak işaretleyin.',
      status: ERROR_STATUS.FIXED,
      detected_at: '2026-04-18T10:30:26Z',
    },
    {
      id: 'err_009',
      type: ERROR_TYPES.SYNTAX_ERROR,
      severity: SEVERITY.LOW,
      element: 'ProductCatalog',
      element_type: 'Class',
      description:
        'ProductCatalog sınıfında kullanılan "<<Interface>>" stereotipi büyük/küçük harf uyumsuzluğu içeriyor.',
      line: 57,
      suggestion:
        '"<<interface>>" yerine PlantUML\'in kabul ettiği "<<Interface>>" ya da "interface" anahtar kelimesini kullanın.',
      status: ERROR_STATUS.OPEN,
      detected_at: '2026-04-18T10:30:28Z',
    },
  ],
};

export const mockLogHistory = [
  {
    id: 'log_001',
    job_id: 'job_2026041801',
    document: 'requirements-v2.txt',
    timestamp: '2026-04-18T10:30:00Z',
    status: 'COMPLETED',
    error_count: 9,
    high_count: 3,
    processing_time_ms: 4320,
  },
  {
    id: 'log_002',
    job_id: 'job_2026041702',
    document: 'requirements-v1.txt',
    timestamp: '2026-04-17T15:20:00Z',
    status: 'COMPLETED',
    error_count: 14,
    high_count: 5,
    processing_time_ms: 5810,
  },
  {
    id: 'log_003',
    job_id: 'job_2026041701',
    document: 'srs-draft.pdf',
    timestamp: '2026-04-17T09:45:00Z',
    status: 'FAILED',
    error_count: 0,
    high_count: 0,
    processing_time_ms: 1200,
  },
  {
    id: 'log_004',
    job_id: 'job_2026041601',
    document: 'system-spec-final.pdf',
    timestamp: '2026-04-16T14:10:00Z',
    status: 'COMPLETED',
    error_count: 6,
    high_count: 1,
    processing_time_ms: 3950,
  },
  {
    id: 'log_005',
    job_id: 'job_2026041501',
    document: 'requirements-initial.txt',
    timestamp: '2026-04-15T11:05:00Z',
    status: 'COMPLETED',
    error_count: 21,
    high_count: 8,
    processing_time_ms: 6100,
  },
];

export const formatTimestamp = (isoString) => {
  const date = new Date(isoString);
  return date.toLocaleString('tr-TR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};
