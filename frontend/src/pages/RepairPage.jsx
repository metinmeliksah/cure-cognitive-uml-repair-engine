import { useState, useEffect, useRef } from 'react';
import {
  Play,
  CheckCircle,
  XCircle,
  Download,
  RotateCcw,
  FlaskConical,
  ChevronDown,
} from 'lucide-react';
import RepairProgressBar from '../components/RepairProgressBar';
import RepairTimeline from '../components/RepairTimeline';
import {
  mockRepairSession,
  mockRepairSessionSuccess1,
  mockRepairSessionFailed,
  REPAIR_STATUS,
  REPAIR_PHASES_ORDERED,
} from '../data/mockData';

const SCENARIOS = [
  { key: 'two', label: '2. Denemede Başarı', data: mockRepairSession },
  { key: 'one', label: '1. Denemede Başarı', data: mockRepairSessionSuccess1 },
  { key: 'fail', label: '3 Denemede Başarısızlık', data: mockRepairSessionFailed },
];

const PHASE_DELAY_MS = 900;

const useRepairSimulation = (session) => {
  const [visibleIterations, setVisibleIterations] = useState([]);
  const [currentPhase, setCurrentPhase] = useState(REPAIR_PHASES_ORDERED[0].key);
  const [currentIterationNo, setCurrentIterationNo] = useState(0);
  const [overallStatus, setOverallStatus] = useState(REPAIR_STATUS.IN_PROGRESS);
  const [running, setRunning] = useState(false);
  const timerRef = useRef(null);

  const reset = () => {
    clearTimeout(timerRef.current);
    setVisibleIterations([]);
    setCurrentPhase(REPAIR_PHASES_ORDERED[0].key);
    setCurrentIterationNo(0);
    setOverallStatus(REPAIR_STATUS.IN_PROGRESS);
    setRunning(false);
  };

  const start = () => {
    reset();
    setRunning(true);
  };

  useEffect(() => {
    if (!running) return;

    let iterIdx = 0;
    let phaseIdx = 0;

    const tick = () => {
      if (iterIdx >= session.iterations.length) {
        setOverallStatus(session.status);
        setRunning(false);
        return;
      }

      const iter = session.iterations[iterIdx];

      if (phaseIdx < REPAIR_PHASES_ORDERED.length) {
        setCurrentPhase(REPAIR_PHASES_ORDERED[phaseIdx].key);
        setCurrentIterationNo(iterIdx + 1);
        phaseIdx++;
        timerRef.current = setTimeout(tick, PHASE_DELAY_MS);
      } else {
        // Bir iterasyon bitti
        setVisibleIterations((prev) => [...prev, iter]);
        phaseIdx = 0;
        iterIdx++;
        timerRef.current = setTimeout(tick, PHASE_DELAY_MS);
      }
    };

    timerRef.current = setTimeout(tick, 300);
    return () => clearTimeout(timerRef.current);
  }, [running, session]);

  return {
    visibleIterations,
    currentPhase,
    currentIterationNo: Math.max(currentIterationNo, 1),
    overallStatus,
    running,
    start,
    reset,
  };
};

const StatusBanner = ({ status, resolvedAt, maxIterations, document: doc }) => {
  if (status === REPAIR_STATUS.IN_PROGRESS) {
    return (
      <div className="repair-banner repair-banner--waiting">
        <div className="repair-banner__icon">
          <div className="pulse-dot" />
        </div>
        <div className="repair-banner__text">
          <strong>Bekleyin — Otonom onarım devam ediyor.</strong>
          <span>Sistem {doc} dosyasını analiz edip düzeltiyor. Bu işlem birkaç saniye sürebilir.</span>
        </div>
      </div>
    );
  }

  if (status === REPAIR_STATUS.SUCCESS) {
    return (
      <div className="repair-banner repair-banner--success">
        <CheckCircle size={24} />
        <div className="repair-banner__text">
          <strong>Tamamlandı — Diyagram başarıyla onarıldı.</strong>
          <span>
            {resolvedAt === 1
              ? 'İlk denemede derleme testi geçti.'
              : `${resolvedAt}. denemede derleme testi geçti.`}{' '}
            Final diyagram aşağıdan indirilebilir.
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="repair-banner repair-banner--failed">
      <XCircle size={24} />
      <div className="repair-banner__text">
        <strong>Onarım Tamamlanamadı — {maxIterations} deneme sonrası durduruldu.</strong>
        <span>
          Sistem maksimum iterasyon limitine ({maxIterations}) ulaştı. Lütfen diyagramı manuel olarak
          inceleyin veya SRS belgenizi güncelleyin.
        </span>
      </div>
    </div>
  );
};

const RepairPage = () => {
  const [scenarioKey, setScenarioKey] = useState('two');
  const [showScenarios, setShowScenarios] = useState(false);
  const activeScenario = SCENARIOS.find((s) => s.key === scenarioKey);

  const {
    visibleIterations,
    currentPhase,
    currentIterationNo,
    overallStatus,
    running,
    start,
    reset,
  } = useRepairSimulation(activeScenario.data);

  const isIdle = !running && overallStatus === REPAIR_STATUS.IN_PROGRESS && visibleIterations.length === 0;
  const isFinished = !running && overallStatus !== REPAIR_STATUS.IN_PROGRESS;

  const handleScenario = (key) => {
    setScenarioKey(key);
    setShowScenarios(false);
    reset();
  };

  return (
    <div className="page repair-page">
      <div className="container">
        <div className="content-card">
          <div className="card-header">
            <h2>Otonom Onarım İzleme</h2>
            <p>
              Sistem, UML diyagramınızdaki hataları OCL kuralları ile tespit edip otonom olarak
              onarır. Her denemenin sonucu anlık olarak aşağıda izlenebilir.
            </p>
          </div>

          {/* Mock uyarısı + senaryo seçici */}
          <div className="repair-controls">
            <div className="mock-notice">
              <FlaskConical size={15} />
              <span>
                <strong>Test modu</strong> — API bağlantısı kurulana kadar simülasyon verisi
                kullanılıyor.
              </span>
            </div>

            <div className="scenario-picker">
              <button
                className="scenario-picker__btn"
                onClick={() => setShowScenarios((v) => !v)}
              >
                <span>Senaryo: {activeScenario.label}</span>
                <ChevronDown size={14} />
              </button>
              {showScenarios && (
                <div className="scenario-picker__menu">
                  {SCENARIOS.map((s) => (
                    <button
                      key={s.key}
                      className={`scenario-picker__item ${s.key === scenarioKey ? 'scenario-picker__item--active' : ''}`}
                      onClick={() => handleScenario(s.key)}
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* İş meta */}
          <div className="job-meta">
            <span className="job-meta__item">Belge: {activeScenario.data.document}</span>
            <span className="job-meta__item">UML: {activeScenario.data.uml_file}</span>
            <span className="job-meta__item job-meta__id">#{activeScenario.data.run_id}</span>
          </div>

          {/* Kullanıcı bilgilendirme banner */}
          {!isIdle && (
            <StatusBanner
              status={overallStatus}
              resolvedAt={activeScenario.data.resolved_at_iteration}
              maxIterations={activeScenario.data.max_iterations}
              document={activeScenario.data.document}
            />
          )}

          {/* Progress bar */}
          {!isIdle && (
            <RepairProgressBar
              currentPhase={currentPhase}
              iterationNo={currentIterationNo}
              maxIterations={activeScenario.data.max_iterations}
              overallStatus={overallStatus}
            />
          )}

          {/* Başlat / Sıfırla butonları */}
          <div className="repair-actions">
            {isIdle && (
              <button className="btn btn-primary" onClick={start}>
                <Play size={18} />
                <span>Simülasyonu Başlat</span>
              </button>
            )}
            {running && (
              <button className="btn btn-secondary" disabled>
                <div className="spinner spinner--sm" />
                <span>Onarım devam ediyor…</span>
              </button>
            )}
            {isFinished && (
              <div className="repair-done-actions">
                <button className="btn btn-outline" onClick={reset}>
                  <RotateCcw size={16} />
                  <span>Yeniden Başlat</span>
                </button>
                {overallStatus === REPAIR_STATUS.SUCCESS && (
                  <button className="btn btn-primary">
                    <Download size={16} />
                    <span>Final Diyagramı İndir</span>
                  </button>
                )}
              </div>
            )}
          </div>

          {/* İterasyon timeline */}
          {visibleIterations.length > 0 && (
            <RepairTimeline iterations={visibleIterations} />
          )}

          {/* Boş durum */}
          {isIdle && (
            <div className="repair-idle">
              <div className="repair-idle__icon">
                <Play size={32} />
              </div>
              <p>
                Simülasyonu başlatmak için <strong>Simülasyonu Başlat</strong> düğmesine tıklayın.
                Farklı senaryoları üstteki menüden seçebilirsiniz.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RepairPage;
