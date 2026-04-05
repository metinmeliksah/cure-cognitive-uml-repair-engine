import { useState } from 'react';
import FileUpload from '../components/FileUpload';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';
import { uploadFile, processDocument } from '../services/api';
import { ArrowRight } from 'lucide-react';

const SRS_ACCEPT = {
  'text/plain': ['.txt'],
  'application/pdf': ['.pdf'],
};

const UML_ACCEPT = {
  'application/xml': ['.xmi', '.uml'],
  'text/xml': ['.xmi', '.uml'],
  'text/plain': ['.puml', '.plantuml'],
};

const HomePage = () => {
  const [srsFile, setSrsFile] = useState(null);
  const [umlFile, setUmlFile] = useState(null);
  const [uploadResetKey, setUploadResetKey] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [srsUploadError, setSrsUploadError] = useState('');
  const [umlUploadError, setUmlUploadError] = useState('');

  const handleSrsSelect = (selectedFile, err = '') => {
    setSrsFile(selectedFile);
    setSrsUploadError(err);
    setError('');
    setSuccess('');
  };

  const handleUmlSelect = (selectedFile, err = '') => {
    setUmlFile(selectedFile);
    setUmlUploadError(err);
    setError('');
    setSuccess('');
  };

  const handleSubmit = async () => {
    if (!srsFile) {
      setError('Lütfen SRS belgesi (.txt veya .pdf) yükleyin');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');
    setSrsUploadError('');
    setUmlUploadError('');

    try {
      const uploadResult = await uploadFile(srsFile, umlFile);

      await processDocument(uploadResult.fileId);

      setSuccess('Dosyalar başarıyla yüklendi ve işleme alındı!');
      setSrsFile(null);
      setUmlFile(null);
      setUploadResetKey((k) => k + 1);
    } catch (err) {
      setError(err || 'Bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page home-page">
      <div className="container">
        <div className="content-card">
          <div className="card-header">
            <h2>Akıllı UML Onarım Platformu</h2>
            <p>
              Yazılım Gereksinim Spesifikasyonu (SRS) belgenizi yükleyin. İsterseniz elinizdeki mevcut UML
              çıktısını (XMI veya PlantUML) ekleyerek onarımı bu modele göre yönlendirebilirsiniz. Sistem,
              belgeyi ve varsa mevcut diyagramı birlikte analiz ederek hataları tespit edip düzeltir.
            </p>
          </div>

          <div className="upload-stack">
            <FileUpload
              key={`srs-${uploadResetKey}`}
              onFileSelect={handleSrsSelect}
              error={srsUploadError}
              loading={loading}
              accept={SRS_ACCEPT}
              title="SRS belgesi"
              emptyDescription="SRS dosyanızı (.txt veya .pdf) sürükleyip bırakın veya seçmek için tıklayın"
              fileHint="Zorunlu · En fazla 10 MB"
              invalidTypeMessage="SRS için yalnızca .txt ve .pdf kabul edilir"
            />
            <FileUpload
              key={`uml-${uploadResetKey}`}
              onFileSelect={handleUmlSelect}
              error={umlUploadError}
              loading={loading}
              accept={UML_ACCEPT}
              title="Mevcut UML (isteğe bağlı)"
              emptyDescription="XMI (.xmi) veya PlantUML (.puml, .plantuml) dosyanızı ekleyin"
              fileHint="İsteğe bağlı · En fazla 10 MB"
              variant="compact"
              invalidTypeMessage="UML için .xmi, .uml, .puml veya .plantuml kullanın"
            />
          </div>

          {error && (
            <Alert 
              type="error" 
              message={error} 
              onClose={() => setError('')}
            />
          )}

          {success && (
            <Alert 
              type="success" 
              message={success} 
              onClose={() => setSuccess('')}
            />
          )}

          {loading ? (
            <LoadingSpinner message="Dosyalar yükleniyor ve işleniyor..." />
          ) : (
            <button 
              onClick={handleSubmit} 
              className="btn btn-primary"
              disabled={!srsFile}
            >
              <span>İşleme Başla</span>
              <ArrowRight size={20} />
            </button>
          )}
        </div>

        <div className="info-section">
          <h3>Sistem Nasıl Çalışır?</h3>
          <div className="info-grid info-grid--four">
            <div className="info-card">
              <div className="info-number">1</div>
              <h4>Girdi</h4>
              <p>SRS belgenizi yükleyin; varsa mevcut UML’inizi (XMI veya PlantUML) ekleyin</p>
            </div>
            <div className="info-card">
              <div className="info-number">2</div>
              <h4>Analiz</h4>
              <p>Belge ve isteğe bağlı UML birlikte değerlendirilir; model çıkarımı ve karşılaştırma yapılır</p>
            </div>
            <div className="info-card">
              <div className="info-number">3</div>
              <h4>Onarım</h4>
              <p>Çoklu-etmen yapı halüsinasyon ve tutarsızlıkları tespit edip düzeltir</p>
            </div>
            <div className="info-card">
              <div className="info-number">4</div>
              <h4>Sonuç</h4>
              <p>OCL ile doğrulanmış, güncellenmiş UML çıktılarına erişin</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
