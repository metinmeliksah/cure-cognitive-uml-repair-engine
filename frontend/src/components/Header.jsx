import { useTheme } from '../context/ThemeContext';
import { Sun, Moon, Home, AlertCircle, Activity } from 'lucide-react';

const NAV_ITEMS = [
  { id: 'home', label: 'Ana Sayfa', icon: Home },
  { id: 'errors', label: 'Hata Günlüğü', icon: AlertCircle },
  { id: 'repair', label: 'Onarım İzleme', icon: Activity },
];

const Header = ({ currentPage, onNavigate }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <h1>CURE</h1>
          </div>

          <nav className="main-nav" aria-label="Ana navigasyon">
            {NAV_ITEMS.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                className={`nav-btn ${currentPage === id ? 'nav-btn--active' : ''}`}
                onClick={() => onNavigate?.(id)}
                aria-current={currentPage === id ? 'page' : undefined}
              >
                <Icon size={16} />
                <span>{label}</span>
              </button>
            ))}
          </nav>

          <button
            onClick={toggleTheme}
            className="theme-toggle"
            aria-label="Tema değiştir"
          >
            {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
