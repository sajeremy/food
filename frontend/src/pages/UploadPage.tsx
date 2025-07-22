import { useState } from 'react';
import { parseGroceryReceipt } from '../services/api/groceryReceipt';
import { ReceiptUpload } from '@/components/molecules/ReceiptUpload';

export function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [parsedData, setParsedData] = useState<any>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setParsedData(null); // Clear previous results when new file is selected
  };

  const handleParseReceipt = async () => {
    if (!selectedFile) {
      alert('Please select a file first.');
      return;
    }

    setIsUploading(true);
    try {
      const groceryData = await parseGroceryReceipt({
        user: 'DemoUser',
        imgFile: selectedFile,
      });
      setParsedData(groceryData);
    } 
    catch (error) {
      console.error('Error parsing receipt:', error);
      alert('An unexpected error occurred.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center px-6 max-w-2xl mx-auto">
      <ReceiptUpload
        onFileSelect={handleFileSelect}
        onUpload={handleParseReceipt}
        selectedFile={selectedFile}
        isUploading={isUploading}
      />
      
      {parsedData && (
        <div className="mt-6 p-6 bg-white rounded-xl shadow-md border border-gray-200 w-full">
          <h2 className="text-xl font-semibold mb-4 text-gray-900">Parsed Data</h2>
          <div className="bg-gray-50 rounded-lg p-4 overflow-auto max-h-96">
            <pre className="text-sm whitespace-pre-wrap text-gray-700">
              {JSON.stringify(parsedData, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}