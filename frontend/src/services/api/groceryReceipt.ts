import { api } from "../../lib/api";

type receiptInput = {
  imgFile: File;
};

const parseGroceryReceipt = async (inputs: receiptInput) => {
  const formData = new FormData();
  formData.append('img_file', inputs.imgFile);

  const response = await api.post('/grocery_receipt', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export { parseGroceryReceipt };
