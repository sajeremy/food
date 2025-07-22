import { UserMenu } from '@/components/molecules/UserMenu';

interface HeaderProps {
  title?: string;
  avatarSrc?: string;
  userName?: string;
  onLogout?: () => void;
}

export function Header({ 
  title = 'Grocery Receipt Parser', 
  avatarSrc, 
  userName = 'DemoUser', 
  onLogout 
}: HeaderProps) {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-900">{title}</h1>
        <UserMenu 
          avatarSrc={avatarSrc}
          userName={userName}
          onLogout={onLogout}
        />
      </div>
    </header>
  );
}