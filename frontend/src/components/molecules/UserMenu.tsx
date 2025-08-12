import { User } from 'lucide-react';
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/shadcn/Avatar';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/shadcn/dropdown-menu';

export function UserMenu() {
  const displayName = "Default User";
  const initials = "DU";

  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="focus:outline-none">
        <Avatar className="hover:ring-2 hover:ring-violet-200 transition-all cursor-pointer">
          <AvatarImage src="" alt={displayName} />
          <AvatarFallback>{initials}</AvatarFallback>
        </Avatar>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem>
          <User size={16} />
          <div className="ml-2">
            <div className="font-medium">{displayName}</div>
            <div className="text-sm text-gray-500">user@example.com</div>
          </div>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}