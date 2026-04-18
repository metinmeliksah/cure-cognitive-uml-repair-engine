import { useState } from 'react';
import {
  AlertTriangle,
  AlertCircle,
  CheckCircle,
  Clock,
  FileText,
  FlaskConical,
} from 'lucide-react';
import ErrorList from '../components/ErrorList';
import LogPanel from '../components/LogPanel';
import { mockErrorReport, mockLogHistory } from '../data/mockData';

const TAB = { ERRORS: 'ERRORS', HISTORY: 'HISTORY' };

const SummaryCard = ({ label, value, icon: Icon, colorClass }) => (
  <div className={`summary-card ${colorClass}`}>
    <div className="summary-card__icon">
      <Icon size={20} />
    </div>
    <div className="summary-card__body">
      <span className="summary-card__value">{value}</span>
      <span className="summary-card__label">{label}</span>
    </div>
  </div>
);

const ErrorLogPage = () => {
  const [activeTab, setActiveTab] = useState(TAB.ERRORS);
  const [currentReport, setCurrentReport] = useState(mockErrorReport);

  const { summary } = currentReport;

  const handleSelectJob = (log) => {
    if (log.status === 'FAILED') return;
    setCurrentReport({
      ...mockErrorReport,
      job_id: log.job_id,
      document: log.document,
      timestamp: log.timestamp,
    });
    setActiveTab(TAB.ERRORS);
  };

  return (
    <div className="page error-log-page">
      <div className="container">
        <div className="content-card">
          <div className="card-header">
            <h2>Hata Günlüğü</h2>
            <p>
              Analiz edilen UML diyagramlarındaki halüsinasyon, tasarım kokusu
              ve sözdizimi hatalarının görsel listesi.
            </p>
          </div>

          <div className="mock-notice">
            <FlaskConical size={15} />
            <span>
              Şu an <strong>test verisi</strong> gösteriliyor — API bağlantısı
              kurulduğunda gerçek sonuçlar burada görünecek.
            </span>
          </div>

          <div className="job-meta">
            <span className="job-meta__item">
              <FileText size={14} />
              {currentReport.document}
            </span>
            <span className="job-meta__item">
              <Clock size={14} />
              {new Date(currentReport.timestamp).toLocaleString('tr-TR')}
            </span>
            <span className="job-meta__item job-meta__id">
              #{currentReport.job_id}
            </span>
          </div>

          <div className="summary-grid">
            <SummaryCard
              label="Toplam Hata"
              value={summary.total}
              icon={AlertCircle}
              colorClass="summary-card--neutral"
            />
            <SummaryCard
              label="Yüksek Şiddet"
              value={summary.high}
              icon={AlertTriangle}
              colorClass="summary-card--high"
            />
            <SummaryCard
              label="Orta Şiddet"
              value={summary.medium}
              icon={AlertCircle}
              colorClass="summary-card--medium"
            />
            <SummaryCard
              label="Düzeltildi"
              value={summary.fixed}
              icon={CheckCircle}
              colorClass="summary-card--fixed"
            />
          </div>

          <div className="tab-bar">
            <button
              className={`tab-btn ${activeTab === TAB.ERRORS ? 'tab-btn--active' : ''}`}
              onClick={() => setActiveTab(TAB.ERRORS)}
            >
              <AlertCircle size={16} />
              Aktif Hatalar
              <span className="tab-badge">{summary.total}</span>
            </button>
            <button
              className={`tab-btn ${activeTab === TAB.HISTORY ? 'tab-btn--active' : ''}`}
              onClick={() => setActiveTab(TAB.HISTORY)}
            >
              <Clock size={16} />
              Analiz Geçmişi
              <span className="tab-badge">{mockLogHistory.length}</span>
            </button>
          </div>

          {activeTab === TAB.ERRORS && (
            <ErrorList errors={currentReport.errors} />
          )}

          {activeTab === TAB.HISTORY && (
            <LogPanel logs={mockLogHistory} onSelectJob={handleSelectJob} />
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorLogPage;
