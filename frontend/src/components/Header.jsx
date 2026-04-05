import { useTheme } from '../context/ThemeContext';
import { Sun, Moon } from 'lucide-react';

const Header = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <h1>CURE</h1>
          </div>
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
