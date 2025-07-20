import { createSnakeCaseFormData } from "./utils";

type receiptInput = {
  user: string;
  imgFile: File;
};

const foodApiBaseUrl = import.meta.env.VITE_FOOD_API_BASE_URL;

const parseGroceryReceipt = async (inputs: receiptInput) => {
  const formData = createSnakeCaseFormData(inputs);
  const response = await fetch(`${foodApiBaseUrl}/grocery_receipt`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to parse grocery receipt");
  }

  return response.json();
};

export { parseGroceryReceipt };
