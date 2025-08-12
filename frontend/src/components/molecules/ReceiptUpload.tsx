import { useState, useRef, type DragEvent } from 'react';
import { Upload } from 'lucide-react';

interface ReceiptUploadProps {
  onFileSelect: (file: File) => void;
  onUpload: () => void;
  onViewResults?: () => void;
  isUploading?: boolean;
  selectedFile?: File | null;
  hasParsedData?: boolean;
}

export function ReceiptUpload({ onFileSelect, onUpload, onViewResults, isUploading = false, selectedFile, hasParsedData = false }: ReceiptUploadProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (isValidFileType(file)) {
        onFileSelect(file);
      } else {
        alert('Please upload a valid image file (JPG, PNG, HEIC)');
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (isValidFileType(file)) {
        onFileSelect(file);
      } else {
        alert('Please upload a valid image file (JPG, PNG, HEIC)');
      }
    }
  };

  const isValidFileType = (file: File) => {
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/heic'];
    return validTypes.includes(file.type);
  };

  const handleSelectFiles = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Upload Receipt</h2>
        <p className="text-sm text-gray-600">
          Upload your grocery receipts to analyze your spending patterns and get personalized recommendations
        </p>
      </div>
      
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ${
          isDragOver
            ? 'border-violet-400 bg-violet-50'
            : 'border-gray-300 hover:border-violet-300 hover:bg-gray-50'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileChange}
          accept=".jpg,.jpeg,.png,.heic"
          className="hidden"
        />
        
        <div className="flex flex-col items-center gap-4">
          <div className={`p-3 rounded-full transition-colors duration-200 ${
            isDragOver ? 'bg-violet-100' : 'bg-gray-100'
          }`}>
            <Upload 
              size={32} 
              className={`transition-colors duration-200 ${
                isDragOver ? 'text-violet-600' : 'text-gray-500'
              }`} 
            />
          </div>
          
          <div>
            <h3 className="text-base font-medium text-gray-900 mb-1">
              Drop receipt here
            </h3>
            <p className="text-sm text-gray-500 mb-3">
              or click to browse your files
            </p>
            <p className="text-xs text-gray-400">
              Supports JPG, PNG, HEIC files up to 10MB
            </p>
          </div>
          
          <button
            onClick={handleSelectFiles}
            className="bg-gray-900 text-white px-6 py-2 rounded-lg font-medium hover:bg-gray-800 transition-colors duration-200"
          >
            Select Files
          </button>
        </div>
      </div>

      {selectedFile && (
        <div className="mt-4 p-4 bg-violet-50 rounded-lg border border-violet-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-violet-900">
                Selected: {selectedFile.name}
              </p>
              <p className="text-xs text-violet-600">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
            <div className="flex gap-2">
              {hasParsedData && onViewResults && (
                <button
                  onClick={onViewResults}
                  className="bg-gray-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-700 transition-colors duration-200"
                >
                  View Results
                </button>
              )}
              <button
                onClick={onUpload}
                disabled={isUploading}
                className="bg-violet-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-violet-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
              >
                {isUploading ? 'Processing...' : hasParsedData ? 'Re-parse' : 'Parse Receipt'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}