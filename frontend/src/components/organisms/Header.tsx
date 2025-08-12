import { UserMenu } from '@/components/molecules/UserMenu';
import { Logo } from '@/components/atoms/Logo';

export function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <Logo />
        <UserMenu />
      </div>
    </header>
  );
}