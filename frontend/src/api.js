const API_BASE = import.meta.env.VITE_API_BASE_URL.replace(/\/$/, "");


export const uploadDataset = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(error.detail || "Upload failed");
  }

  return response.json();
};

export const getDashboard = async () => {
  const response = await fetch(`${API_BASE}/dashboard`);

  if (!response.ok) {
    throw new Error("Failed to fetch dashboard");
  }

  return response.json();
};

export const askQuestion = async (question, datasetId = null) => {
  const body = { question };
  if (datasetId) {
    body.dataset_id = datasetId;
  }

  const response = await fetch(`${API_BASE}/qa`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "QA request failed" }));
    throw new Error(error.detail || "QA request failed");
  }

  return response.json();
};
