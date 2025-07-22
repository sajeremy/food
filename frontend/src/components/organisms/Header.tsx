import { UserMenu } from '@/components/molecules/UserMenu';
import { Logo } from '@/components/atoms/Logo';

interface HeaderProps {
  avatarSrc?: string;
  userName?: string;
  onLogout?: () => void;
}

export function Header({ 
  avatarSrc, 
  userName = 'DemoUser', 
  onLogout 
}: HeaderProps) {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <Logo />
        <UserMenu 
          avatarSrc={avatarSrc}
          userName={userName}
          onLogout={onLogout}
        />
      </div>
    </header>
  );
}