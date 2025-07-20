import { useState } from 'react';
import { parseGroceryReceipt } from './services/api/groceryReceipt';

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [parsedData, setParsedData] = useState<any>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleParseReceipt = async () => {
    if (!selectedFile) {
      alert('Please select a file first.');
      return;
    }


    try {
      const groceryData = await parseGroceryReceipt({
        user: 'test_user', // Replace with actual user ID or context
        imgFile: selectedFile,
      });
      setParsedData(groceryData);
    } 
    catch (error) {
      console.error('Error parsing receipt:', error);
      alert('An unexpected error occurred.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Grocery Receipt Parser</h1>
        <div className="mb-4">
          <input type="file" onChange={handleFileChange} className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100" />
        </div>
        <button onClick={handleParseReceipt} className="w-full bg-violet-500 text-white py-2 px-4 rounded-lg hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500">
          Parse Receipt
        </button>
        {parsedData && (
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h2 className="text-xl font-semibold mb-2">Parsed Data</h2>
            <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(parsedData, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
