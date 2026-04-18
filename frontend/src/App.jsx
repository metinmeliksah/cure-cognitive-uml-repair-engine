import { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import ErrorLogPage from './pages/ErrorLogPage';
import './App.css';

const PAGES = {
  home: HomePage,
  errors: ErrorLogPage,
};

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const PageComponent = PAGES[currentPage] ?? HomePage;

  return (
    <ThemeProvider>
      <div className="app">
        <Header currentPage={currentPage} onNavigate={setCurrentPage} />
        <main className="main-content">
          <PageComponent />
        </main>
        <footer className="footer">
          <div className="container">
            <p>© 2026 CURE - Cognitive UML Repair Engine. Tüm hakları saklıdır.</p>
          </div>
        </footer>
      </div>
    </ThemeProvider>
  );
}

export default App;
