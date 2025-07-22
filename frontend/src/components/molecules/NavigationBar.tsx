import { Upload, BarChart3, TrendingUp, MapPin } from 'lucide-react';

interface NavigationItemProps {
  icon: React.ReactNode;
  label: string;
  isActive?: boolean;
  onClick?: () => void;
}

function NavigationItem({ icon, label, isActive = false, onClick }: NavigationItemProps) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-3 px-6 py-2 rounded-lg transition-all duration-200 group hover:scale-105 ${
        isActive
          ? 'bg-gradient-to-br from-violet-500 to-purple-600 text-white shadow-lg'
          : 'bg-white hover:bg-gradient-to-br hover:from-violet-50 hover:to-purple-50 text-gray-600 hover:text-violet-600 border border-gray-200 hover:border-violet-200'
      }`}
    >
      <div className={`transition-transform duration-200 group-hover:scale-110 ${
        isActive ? 'text-white' : 'text-gray-500 group-hover:text-violet-600'
      }`}>
        {icon}
      </div>
      <span className={`text-sm font-medium transition-colors duration-200 ${
        isActive ? 'text-white' : 'text-gray-600 group-hover:text-violet-600'
      }`}>
        {label}
      </span>
    </button>
  );
}

interface NavigationBarProps {
  activeSection?: string;
  onSectionChange?: (section: string) => void;
}

export function NavigationBar({ activeSection = 'dashboard', onSectionChange }: NavigationBarProps) {
  const navigationItems = [
    { id: 'upload', icon: <Upload size={20} />, label: 'Upload' },
    { id: 'dashboard', icon: <BarChart3 size={20} />, label: 'Dashboard' },
    { id: 'trends', icon: <TrendingUp size={20} />, label: 'Trends' },
    { id: 'store-finder', icon: <MapPin size={20} />, label: 'Store Finder' },
  ];

  return (
    <nav className="bg-white shadow-sm border border-gray-200 rounded-xl mx-6 mt-4">
      <div className="flex items-center justify-center gap-4 p-2">
        {navigationItems.map((item) => (
          <NavigationItem
            key={item.id}
            icon={item.icon}
            label={item.label}
            isActive={activeSection === item.id}
            onClick={() => onSectionChange?.(item.id)}
          />
        ))}
      </div>
    </nav>
  );
}