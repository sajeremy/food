import { X, Save } from 'lucide-react';
import { useEffect, useState } from 'react';
import heic2any from 'heic2any';

interface ReceiptReviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  receiptImage: File;
  parsedData: any;
  onSave: (data: any) => void;
  onCancel: () => void;
}

export function ReceiptReviewModal({ 
  isOpen, 
  onClose, 
  receiptImage, 
  parsedData, 
  onSave,
}: ReceiptReviewModalProps) {
  const [imageUrl, setImageUrl] = useState<string>('');
  const [isConverting, setIsConverting] = useState(false);

  const convertHeicToJpg = async (file: File): Promise<File> => {
    try {
      setIsConverting(true);
      const convertedBlob = await heic2any({
        blob: file,
        toType: 'image/jpeg',
        quality: 0.8
      }) as Blob;
      
      // Create a new File object from the converted blob
      return new File([convertedBlob], file.name.replace(/\.heic$/i, '.jpg'), {
        type: 'image/jpeg',
        lastModified: file.lastModified
      });
    } catch (error) {
      console.error('Error converting HEIC to JPG:', error);
      throw error;
    } finally {
      setIsConverting(false);
    }
  };

  const isHeicFile = (file: File): boolean => {
    return file.type === 'image/heic' || file.name.toLowerCase().endsWith('.heic');
  };

  useEffect(() => {
    const processImage = async () => {
      if (receiptImage) {
        try {
          let fileToDisplay = receiptImage;
          
          // Convert HEIC to JPG if needed
          if (isHeicFile(receiptImage)) {
            fileToDisplay = await convertHeicToJpg(receiptImage);
          }
          
          const url = URL.createObjectURL(fileToDisplay);
          setImageUrl(url);
          
          // Cleanup object URL when component unmounts or image changes
          return () => {
            URL.revokeObjectURL(url);
          };
        } catch (error) {
          console.error('Error processing image:', error);
          // Fallback to original file if conversion fails
          const url = URL.createObjectURL(receiptImage);
          setImageUrl(url);
          return () => {
            URL.revokeObjectURL(url);
          };
        }
      }
    };

    processImage();
  }, [receiptImage]);

  if (!isOpen) return null;

  const handleSave = () => {
    onSave(parsedData);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Review Receipt</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors duration-200"
          >
            <X size={20} className="text-gray-500" />
          </button>
        </div>

        {/* Content */}
        <div className="flex h-[70vh]">
          {/* Left side - Receipt Image */}
          <div className="w-1/2 p-6 border-r border-gray-200">
            <div className="h-full flex flex-col">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Receipt Image</h3>
              <div className="flex-1 bg-gray-50 rounded-lg flex items-center justify-center overflow-hidden">
                {imageUrl ? (
                  <img
                    src={imageUrl}
                    alt="Receipt"
                    className="max-w-full max-h-full object-contain"
                    onError={(e) => {
                      console.error('Error loading image:', e);
                    }}
                  />
                ) : (
                  <div className="text-gray-500 text-center">
                    {isConverting ? (
                      <div>
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-violet-600 mx-auto mb-2"></div>
                        <div>Converting HEIC to JPG...</div>
                      </div>
                    ) : (
                      'Loading image...'
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right side - Parsed Data */}
          <div className="w-1/2 p-6">
            <div className="h-full flex flex-col">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Parsed Data</h3>
              <div className="flex-1 bg-gray-50 rounded-lg p-4 overflow-auto">
                <pre className="text-sm whitespace-pre-wrap text-gray-700">
                  {JSON.stringify(parsedData, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        </div>

        {/* Footer with action buttons */}
        <div className="flex items-center justify-end gap-4 p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={handleSave}
            className="flex items-center gap-2 px-6 py-2 text-white bg-violet-600 rounded-lg hover:bg-violet-700 transition-colors duration-200"
          >
            <Save size={16} />
            Save Receipt
          </button>
        </div>
      </div>
    </div>
  );
}