import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import EntityTypeView from './pages/EntityTypeView';
import EntityView from './pages/EntityView';
import { AdminModeProvider, useAdminMode } from './context/AdminModeContext';
import './App.css';

function AppContent() {
  const { isAdminMode, toggleAdminMode } = useAdminMode();

  return (
    <div className={`app ${isAdminMode ? 'admin-mode' : ''}`}>
      <header className={isAdminMode ? 'admin-header' : ''}>
        <Link to="/">
          <h1>EAV CMS</h1>
        </Link>
        <div className="header-actions">
          <label className="toggle-switch">
            <span className="toggle-label">Admin Mode</span>
            <input
              type="checkbox"
              checked={isAdminMode}
              onChange={toggleAdminMode}
            />
            <span className="toggle-slider" />
          </label>
        </div>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/types/:typeId" element={<EntityTypeView />} />
          <Route path="/entities/:entityId" element={<EntityView />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AdminModeProvider>
        <AppContent />
      </AdminModeProvider>
    </BrowserRouter>
  );
}

export default App;
