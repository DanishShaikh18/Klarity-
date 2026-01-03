// src/api/apiClient.js

// 🔧 Base URL for your FastAPI backend
// Later you can move this to .env: VITE_API_BASE_URL
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function handleResponse(res) {
  const contentType = res.headers.get("content-type") || "";

  let data = null;
  if (contentType.includes("application/json")) {
    data = await res.json();
  } else {
    // fallback (not really needed now, but safe)
    const text = await res.text();
    data = { raw: text };
  }

  if (!res.ok) {
    // Simple error wrapper – can improve later
    const message = data?.detail || data?.error || res.statusText;
    throw new Error(message || "API request failed");
  }

  return data;
}

// ✅ For JSON POST requests (e.g. /ask)
export async function postJson(path, bodyObj) {
  const res = await fetch(BASE_URL + path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(bodyObj),
  });

  return handleResponse(res);
}

// ✅ For FormData POST requests (e.g. /upload)
export async function postForm(path, formData) {
  const res = await fetch(BASE_URL + path, {
    method: "POST",
    body: formData, // browser sets correct multipart headers
  });

  return handleResponse(res);
}

export async function patchJson(url, body) {
  const res = await fetch(`${BASE_URL}${url}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data?.detail || "Request failed");
  }
  return data;
}

