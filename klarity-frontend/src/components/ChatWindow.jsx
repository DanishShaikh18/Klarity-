import React, { useEffect, useState } from "react";
import {
  getMessages,
  askInChat,
  uploadToChat,
  getChatDocuments,
  generateChatSummary,
} from "../api/chatApi";

import ChatBox from "./ChatBox";
import ChatInput from "./ChatInput";
import FileUploader from "./FileUploader";
import ChatSummaryPanel from "./ChatSummaryPanel";

export default function ChatWindow({ chatId, onFirstMessage }) {
  const [messages, setMessages] = useState([]);
  const [files, setFiles] = useState([]);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [asking, setAsking] = useState(false);
  const [uploading, setUploading] = useState(false);

  /* ===== SUMMARY STATE ===== */
  const [showSummary, setShowSummary] = useState(false);
  const [summarizing, setSummarizing] = useState(false);

  // summaryCache = { chatId: summaryText }
  const [summaryCache, setSummaryCache] = useState({});

  // summaryMeta = { chatId: messageCountWhenSummarized }
  const [summaryMeta, setSummaryMeta] = useState({});

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

    // Invalidate summary for this chat (chat changed)
    setSummaryMeta(prev => ({
      ...prev,
      [activeChatId]: null,
    }));

    // Show user message immediately
    setMessages(prev => [...prev, { role: "user", content: question }]);

    const tempId = Date.now();
    setMessages(prev => [...prev, { id: tempId, role: "assistant", content: "" }]);

    setAsking(true);

    const resp = await askInChat(activeChatId, question);

    setMessages(prev =>
      prev.map(m =>
        m.id === tempId ? { ...m, content: resp.answer } : m
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

    setFiles(prev => [
      ...prev,
      { id: resp.doc_db_id, name: resp.file },
    ]);

    setUploading(false);
  };

  /* ================= SUMMARIZE ================= */
  const handleSummarize = async (force = false) => {
    if (!chatId) return;

    setShowSummary(true);

    const currentMsgCount = messages.length;
    const cached = summaryCache[chatId];
    const lastCount = summaryMeta[chatId];

    // Use cache if chat unchanged and not forced
    if (!force && cached && lastCount === currentMsgCount) {
      return;
    }

    setSummarizing(true);

    try {
      const res = await generateChatSummary(chatId);

      setSummaryCache(prev => ({
        ...prev,
        [chatId]: res.summary,
      }));

      setSummaryMeta(prev => ({
        ...prev,
        [chatId]: currentMsgCount,
      }));
    } catch (err) {
      console.error(err);
    } finally {
      setSummarizing(false);
    }
  };

  const showWelcome = messages.length === 0 && files.length === 0;

  return (
    <div className="flex flex-col h-full bg-bg text-textPrimary md:ml-7">
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

          {/* ===== SUMMARIZE BUTTON ===== */}
          <button
            onClick={() => handleSummarize(false)}
            disabled={!chatId || summarizing}
            className="
              px-3 py-1.5 rounded-full
              text-sm font-medium
              bg-white/10 hover:bg-white/20
              disabled:opacity-40
              transition
            "
          >
            {summarizing ? "Summarizing…" : "Summarize"}
          </button>

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
      <ChatBox messages={messages} loading={loadingMessages || asking} />

      {/* ===== INPUT ===== */}
      <ChatInput
        onSend={handleSend}
        disabled={asking || uploading}
        onUpload={handleUpload}
      />

      {/* ===== SUMMARY PANEL ===== */}
      <ChatSummaryPanel
        open={showSummary}
        loading={summarizing}
        summary={summaryCache[chatId]}
        onClose={() => setShowSummary(false)}
        onRegenerate={() => handleSummarize(true)}
      />
    </div>
  );
}
