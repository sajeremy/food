import snakecaseKeys from "snakecase-keys";

const createSnakeCaseFormData = (inputs: Record<string, any>): FormData => {
  const formData = new FormData();

  for (const [key, val] of Object.entries(snakecaseKeys(inputs))) {
    if (val != null) {
      formData.append(key, val);
    }
  }

  return formData;
};

export { createSnakeCaseFormData };
