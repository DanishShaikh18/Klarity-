import React, { useEffect, useState } from "react";
import {
  getMessages,
  askInChat,
  uploadToChat,
  getChatDocuments,
} from "../api/chatApi";

import ChatBox from "./ChatBox";
import ChatInput from "./ChatInput";
import FileUploader from "./FileUploader";

export default function ChatWindow({ chatId, onFirstMessage }) {
  const [messages, setMessages] = useState([]);
  const [files, setFiles] = useState([]);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [asking, setAsking] = useState(false);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    if (!chatId) {
      setMessages([]);
      setFiles([]);
      return;
    }

    const load = async () => {
      setLoadingMessages(true);
      const msgs = await getMessages(chatId);
      const docs = await getChatDocuments(chatId);

      setMessages(msgs || []);
      setFiles(docs?.map(d => ({ id: d.id, name: d.file_name })) || []);
      setLoadingMessages(false);
    };

    load();
  }, [chatId]);

  /* ================= SEND MESSAGE ================= */
  const handleSend = async (question) => {
    if (!question.trim()) return;

    let activeChatId = chatId;
    if (!activeChatId) {
      activeChatId = await onFirstMessage(question);
    }

    // 1️⃣ Show user message immediately
    setMessages(prev => [
      ...prev,
      { role: "user", content: question },
    ]);

    // 2️⃣ Show assistant placeholder
    const tempId = Date.now();
    setMessages(prev => [
      ...prev,
      { id: tempId, role: "assistant", content: "" },
    ]);

    setAsking(true);

    // 3️⃣ Fetch answer
    const resp = await askInChat(activeChatId, question);

    // 4️⃣ Replace placeholder with real answer
    setMessages(prev =>
      prev.map(m =>
        m.id === tempId
          ? { ...m, content: resp.answer }
          : m
      )
    );

    setAsking(false);
  };

  /* ================= UPLOAD FILE ================= */
  const handleUpload = async (file) => {
    let activeChatId = chatId;
    if (!activeChatId) {
      activeChatId = await onFirstMessage(file.name);
    }

    setUploading(true);

    const resp = await uploadToChat(activeChatId, file);

    // Show file strip immediately after upload
    setFiles(prev => [
      ...prev,
      { id: resp.doc_db_id, name: resp.file },
    ]);

    setUploading(false);
  };

  const showWelcome = messages.length === 0 && files.length === 0;

  return (
    <div className=" flex flex-col h-full bg-bg text-textPrimary md:ml-7">
      {/* ===== FILE STRIP ===== */}
      {(files.length > 0 || uploading) && (
        <div className="px-6 py-2 flex items-center gap-2 overflow-x-auto border-b border-white/5">
          {files.map(file => (
            <div
              key={file.id}
              className="px-3 py-1.5 rounded-full bg-white/10 text-sm whitespace-nowrap"
            >
              {file.name}
            </div>
          ))}

          {uploading && (
            <div className="px-3 py-1.5 rounded-full bg-white/10 text-sm text-textSecondary flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-white/40 animate-pulse" />
              Uploading…
            </div>
          )}

          <div className="flex-1" />
          <FileUploader small onUpload={handleUpload} />
        </div>
      )}

      {/* ===== WELCOME ===== */}
      {showWelcome && (
        <div className="flex-1 flex flex-col items-center justify-center px-6 text-center">
          <h1 className="text-4xl font-semibold mb-3">Klarity</h1>
          <p className="text-textSecondary mb-10">
            Upload PDFs and ask questions instantly
          </p>
          <FileUploader onUpload={handleUpload} />
        </div>
      )}

      {/* ===== CHAT ===== */}
      <ChatBox
        messages={messages}
        loading={loadingMessages || asking}
      />

      {/* ===== INPUT ===== */}
      <ChatInput
        onSend={handleSend}
        disabled={asking || uploading}
        onUpload={handleUpload}
      />
    </div>
  );
}
