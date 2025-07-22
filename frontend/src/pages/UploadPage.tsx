import { useState } from 'react';
import { parseGroceryReceipt } from '../services/api/groceryReceipt';
import { ReceiptUpload, ReceiptReviewModal } from '@/components/molecules';

export function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [parsedData, setParsedData] = useState<any>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);

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
      setShowReviewModal(true);
    } 
    catch (error) {
      console.error('Error parsing receipt:', error);
      alert('An unexpected error occurred.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleSaveReceipt = (data: any) => {
    // Here you would typically save the data to your backend/database
    console.log('Saving receipt data:', data);
    alert('Receipt saved successfully!');
    // Reset the form
    setSelectedFile(null);
    setParsedData(null);
  };

  const handleCancelReview = () => {
    // Keep the parsed data but close modal - user can review again
    console.log('Review cancelled');
  };

  return (
    <div className="flex flex-col items-center justify-center px-6 max-w-2xl mx-auto">
      <ReceiptUpload
        onFileSelect={handleFileSelect}
        onUpload={handleParseReceipt}
        selectedFile={selectedFile}
        isUploading={isUploading}
      />
      
      {selectedFile && parsedData && (
        <ReceiptReviewModal
          isOpen={showReviewModal}
          onClose={() => setShowReviewModal(false)}
          receiptImage={selectedFile}
          parsedData={parsedData}
          onSave={handleSaveReceipt}
          onCancel={handleCancelReview}
        />
      )}
    </div>
  );
}