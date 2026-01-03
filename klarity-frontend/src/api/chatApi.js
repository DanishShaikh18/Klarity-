// src/api/chatApi.js
// Chat-aware API helpers for Klarity (Phase-3)
//
// Uses the same base URL pattern as apiClient.js.
// Keeps legacy helpers (uploadPdf / askQuestion) for dev/testing.

import { postForm, postJson } from "./apiClient";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function handleGet(path) {
  const res = await fetch(BASE_URL + path);
  const contentType = res.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await res.json() : await res.text();

  if (!res.ok) {
    const errMsg = data?.detail || data?.error || res.statusText || "Request failed";
    throw new Error(errMsg);
  }
  return data;
}

/* -------------------------
   Chat-aware endpoints
   -------------------------*/

/**
 * GET /chats
 * Returns: Array of ChatOut
 */
export function getChats() {
  return handleGet("/chats");
}

/**
 * POST /chats
 * Body: { title: string }
 * Returns: ChatOut
 */
export function createChat(title) {
  if (!title || typeof title !== "string") {
    return Promise.reject(new Error("createChat: title string required"));
  }
  return postJson("/chats", { title });
}

/**
 * POST /chats/{chat_id}/upload (multipart/form-data)
 * Returns: upload response object (as returned by backend)
 */
export function uploadToChat(chatId, file) {
  if (!chatId) return Promise.reject(new Error("uploadToChat: chatId required"));
  if (!file) return Promise.reject(new Error("uploadToChat: file required"));

  const form = new FormData();
  form.append("file", file);

  // Use postForm but need to call the chat-specific path
  return postForm(`/chats/${chatId}/upload`, form);
}

/**
 * POST /chats/{chat_id}/ask
 * Body: { question: "..." }
 * Returns: { chat_id, user_message_id, assistant_message_id, answer }
 */
export function askInChat(chatId, question) {
  if (!chatId) return Promise.reject(new Error("askInChat: chatId required"));
  if (!question || typeof question !== "string")
    return Promise.reject(new Error("askInChat: question string required"));

  return postJson(`/chats/${chatId}/ask`, { question });
}

/**
 * GET /chats/{chat_id}/messages?limit=100&offset=0
 * Returns: Array of MessageOut
 */
export function getMessages(chatId, { limit = 100, offset = 0 } = {}) {
  if (!chatId) return Promise.reject(new Error("getMessages: chatId required"));

  const q = `?limit=${encodeURIComponent(limit)}&offset=${encodeURIComponent(offset)}`;
  return handleGet(`/chats/${chatId}/messages${q}`);
}

/* -------------------------
   Legacy / dev helpers (keep for tests)
   -------------------------*/

/**
 * Legacy global upload (kept for dev/testing)
 * POST /upload (multipart)
 */
export function uploadPdf(file) {
  const form = new FormData();
  form.append("file", file);
  return postForm("/upload", form);
}

/**
 * Legacy global ask (kept for dev/testing)
 * POST /ask { question }
 */
export function askQuestion(question) {
  return postJson("/ask", { question });
}


/**
 * GET /chats/{chat_id}/documents
 * Returns: Array of DocumentOut
 */
export function getChatDocuments(chatId) {
  if (!chatId) return Promise.reject(new Error("getChatDocuments: chatId required"));
  return handleGet(`/chats/${chatId}/documents`);
}


/**
 * PATCH /chats/{chat_id}
 * Body: { title: string }
 * Returns: ChatOut
 */
import { patchJson } from "./apiClient";

export function renameChat(chatId, title) {
  return patchJson(`/chats/${chatId}`, { title });
}




/**
 * DELETE /chats/{chat_id}
 * Returns: { status, deleted_chat_id }
 */
export async function deleteChat(chatId) {
  if (!chatId) {
    return Promise.reject(new Error("deleteChat: chatId required"));
  }

  const res = await fetch(`${BASE_URL}/chats/${chatId}`, {
    method: "DELETE",
  });

  const data = await res.json();

  if (!res.ok) {
    const errMsg = data?.detail || "Delete failed";
    throw new Error(errMsg);
  }

  return data;
}


/**
 * POST /chats/{chat_id}/summary
 * Returns: { chat_id, summary }
 */
export function generateChatSummary(chatId) {
  if (!chatId) {
    return Promise.reject(
      new Error("generateChatSummary: chatId required")
    );
  }

  // No body needed
  return postJson(`/chats/${chatId}/summary`, {});
}
