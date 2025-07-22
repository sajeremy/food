import { useState } from 'react';
import { MainLayout } from '@/components/templates/MainLayout';
import { UploadPage } from './pages/UploadPage';

function App() {
  const [activeSection, setActiveSection] = useState('upload');

  const handleLogout = () => {
    console.log('User logged out');
  };

  const renderPage = () => {
    switch (activeSection) {
      case 'upload':
        return <UploadPage />;
      case 'dashboard':
        return <div className="flex items-center justify-center"><p className="text-gray-500">Dashboard page coming soon...</p></div>;
      case 'trends':
        return <div className="flex items-center justify-center"><p className="text-gray-500">Trends page coming soon...</p></div>;
      case 'store-finder':
        return <div className="flex items-center justify-center"><p className="text-gray-500">Store Finder page coming soon...</p></div>;
      default:
        return <UploadPage />;
    }
  };

  return (
    <MainLayout
      activeSection={activeSection}
      onSectionChange={setActiveSection}
      onLogout={handleLogout}
    >
      {renderPage()}
    </MainLayout>
  );
}

export default App;
