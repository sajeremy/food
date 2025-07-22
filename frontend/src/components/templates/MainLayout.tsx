import { Header } from '@/components/organisms/Header';
import { NavigationBar } from '@/components/molecules/NavigationBar';

interface MainLayoutProps {
  children: React.ReactNode;
  activeSection?: string;
  onSectionChange?: (section: string) => void;
  onLogout?: () => void;
  avatarSrc?: string;
  userName?: string;
}

export function MainLayout({ 
  children, 
  activeSection = 'upload', 
  onSectionChange, 
  onLogout,
  avatarSrc,
  userName = 'DemoUser'
}: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Header 
        onLogout={onLogout}
        avatarSrc={avatarSrc}
        userName={userName}
      />
      <NavigationBar 
        activeSection={activeSection} 
        onSectionChange={onSectionChange} 
      />
      <main className="flex-1 mt-6">
        {children}
      </main>
    </div>
  );
}