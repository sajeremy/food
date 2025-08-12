import { Header } from '@/components/organisms/Header';
import { NavigationBar } from '@/components/molecules/NavigationBar';

interface MainLayoutProps {
  children: React.ReactNode;
}

export function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Header />
      <NavigationBar />
      <main className="flex-1 mt-6">
        {children}
      </main>
    </div>
  );
}