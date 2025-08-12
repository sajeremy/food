import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { MainLayout } from '@/components/templates/MainLayout';
import { UploadPage } from './pages/UploadPage';

function DashboardPage() {
  return <div className="flex items-center justify-center"><p className="text-gray-500">Dashboard page coming soon...</p></div>;
}

function TrendsPage() {
  return <div className="flex items-center justify-center"><p className="text-gray-500">Trends page coming soon...</p></div>;
}

function StoreFinderPage() {
  return <div className="flex items-center justify-center"><p className="text-gray-500">Store Finder page coming soon...</p></div>;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <MainLayout>
            <UploadPage />
          </MainLayout>
        } />
        
        <Route path="/dashboard" element={
          <MainLayout>
            <DashboardPage />
          </MainLayout>
        } />
        
        <Route path="/trends" element={
          <MainLayout>
            <TrendsPage />
          </MainLayout>
        } />
        
        <Route path="/store-finder" element={
          <MainLayout>
            <StoreFinderPage />
          </MainLayout>
        } />
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
