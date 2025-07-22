import { ShoppingCart } from 'lucide-react';

interface LogoProps {
  className?: string;
}

export function Logo({ className }: LogoProps) {
  return (
    <div className={`flex items-center gap-3 group cursor-pointer transition-all duration-200 hover:scale-105 ${className}`}>
      <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500 to-purple-600 group-hover:from-violet-400 group-hover:to-purple-500 transition-all duration-200 group-hover:shadow-lg">
        <ShoppingCart 
          size={24} 
          className="text-white group-hover:scale-110 transition-transform duration-200" 
        />
      </div>
      <h1 className="text-xl font-bold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent group-hover:from-violet-500 group-hover:to-purple-500 transition-all duration-200">
        ShopSync
      </h1>
    </div>
  );
}