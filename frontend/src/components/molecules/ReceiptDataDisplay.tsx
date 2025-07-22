import { Calendar, MapPin, Phone, User, ShoppingBag, Tag, Package } from 'lucide-react';

// Type definitions based on the API schema
interface UserBase {
  username: string;
}

interface StoreBase {
  name: string;
  address?: string | null;
  phone?: string | null;
}

interface Purchase {
  name: string;
  category: "produce" | "dairy" | "meat" | "dessert" | "beverage" | "snacks" | "frozen" | "canned" | "grains" | "condiments" | "household" | "personal_care" | "other";
  brand?: string | null;
  quantity: number;
  unit_price: number;
  unit_type: "oz" | "lb" | "ea";
}

interface GroceryReceiptData {
  date_time?: string | null;
  is_valid: boolean;
  user: UserBase;
  store: StoreBase;
  purchases: Purchase[];
}

interface ReceiptDataDisplayProps {
  data: GroceryReceiptData;
}

export function ReceiptDataDisplay({ data }: ReceiptDataDisplayProps) {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Unknown date';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const categoryColors: Record<string, string> = {
    produce: 'bg-green-100 text-green-800',
    dairy: 'bg-blue-100 text-blue-800',
    meat: 'bg-red-100 text-red-800',
    dessert: 'bg-pink-100 text-pink-800',
    beverage: 'bg-purple-100 text-purple-800',
    snacks: 'bg-yellow-100 text-yellow-800',
    frozen: 'bg-cyan-100 text-cyan-800',
    canned: 'bg-orange-100 text-orange-800',
    grains: 'bg-amber-100 text-amber-800',
    condiments: 'bg-lime-100 text-lime-800',
    household: 'bg-gray-100 text-gray-800',
    personal_care: 'bg-indigo-100 text-indigo-800',
    other: 'bg-slate-100 text-slate-800'
  };

  const totalAmount = data.purchases.reduce((sum, purchase) => {
    return sum + (purchase.quantity * purchase.unit_price);
  }, 0);

  if (!data.is_valid) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 text-lg font-medium mb-2">Invalid Receipt</div>
        <p className="text-gray-600">This doesn't appear to be a valid grocery receipt.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Receipt Header */}
      <div className="bg-gradient-to-br from-violet-50 to-purple-50 rounded-lg p-4 border border-violet-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Receipt Information</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Date */}
          <div className="flex items-center gap-2">
            <Calendar size={16} className="text-violet-600" />
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wide">Date</p>
              <p className="text-sm font-medium text-gray-900">{formatDate(data.date_time)}</p>
            </div>
          </div>

          {/* User */}
          <div className="flex items-center gap-2">
            <User size={16} className="text-violet-600" />
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wide">User</p>
              <p className="text-sm font-medium text-gray-900">{data.user.username}</p>
            </div>
          </div>

          {/* Store Name */}
          <div className="flex items-center gap-2">
            <ShoppingBag size={16} className="text-violet-600" />
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wide">Store</p>
              <p className="text-sm font-medium text-gray-900">{data.store.name}</p>
            </div>
          </div>

          {/* Store Address */}
          {data.store.address && (
            <div className="flex items-center gap-2">
              <MapPin size={16} className="text-violet-600" />
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide">Address</p>
                <p className="text-sm font-medium text-gray-900">{data.store.address}</p>
              </div>
            </div>
          )}

          {/* Store Phone */}
          {data.store.phone && (
            <div className="flex items-center gap-2">
              <Phone size={16} className="text-violet-600" />
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide">Phone</p>
                <p className="text-sm font-medium text-gray-900">{data.store.phone}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Items List */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Items Purchased</h3>
          <div className="text-sm text-gray-500">
            {data.purchases.length} {data.purchases.length === 1 ? 'item' : 'items'}
          </div>
        </div>

        <div className="space-y-3">
          {data.purchases.map((purchase, index) => (
            <div key={index} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="font-medium text-gray-900">{purchase.name}</h4>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${categoryColors[purchase.category] || categoryColors.other}`}>
                      {purchase.category.replace('_', ' ')}
                    </span>
                  </div>
                  
                  <div className="flex items-center gap-4 text-sm text-gray-600">
                    {purchase.brand && (
                      <div className="flex items-center gap-1">
                        <Tag size={14} />
                        <span>{purchase.brand}</span>
                      </div>
                    )}
                    <div className="flex items-center gap-1">
                      <Package size={14} />
                      <span>{purchase.quantity} {purchase.unit_type}</span>
                    </div>
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="text-lg font-semibold text-gray-900">
                    {formatPrice(purchase.quantity * purchase.unit_price)}
                  </div>
                  <div className="text-xs text-gray-500">
                    {formatPrice(purchase.unit_price)} per {purchase.unit_type}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Total */}
      <div className="bg-gradient-to-br from-violet-50 to-purple-50 rounded-lg p-4 border border-violet-200">
        <div className="flex items-center justify-between">
          <span className="text-lg font-semibold text-gray-900">Total Amount</span>
          <span className="text-2xl font-bold text-violet-600">{formatPrice(totalAmount)}</span>
        </div>
      </div>
    </div>
  );
}