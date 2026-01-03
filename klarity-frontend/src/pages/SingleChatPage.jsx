//klarity-frontend\src\pages\SingleChatPage.jsx

import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import ChatList from "../components/ChatList";
import ChatWindow from "../components/ChatWindow";
import { getChats, createChat } from "../api/chatApi";

export default function SingleChatPage() {
  const { chatId: chatIdParam } = useParams();
  const navigate = useNavigate();

  const chatIdFromUrl = chatIdParam ? Number(chatIdParam) : null;

  const [chats, setChats] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(chatIdFromUrl);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    const loadChats = async () => {
      try {
        setLoading(true);
        const data = await getChats();
        setChats(Array.isArray(data) ? data : []);
      } catch (err) {
        setError("Failed to load chats");
      } finally {
        setLoading(false);
      }
    };
    loadChats();
  }, []);

  useEffect(() => {
    setCurrentChatId(chatIdFromUrl);
  }, [chatIdFromUrl]);

  const handleFirstMessage = async (question) => {
    const created = await createChat(question.slice(0, 40) || "New chat");
    setChats((prev) => [created, ...prev]);
    navigate(`/chat/${created.id}`);
    return created.id;
  };

  const handleSelectChat = (chatId) => {
    navigate(`/chat/${chatId}`);
    setSidebarOpen(false);
  };

  const handleCreateChat = () => {
    navigate("/");
    setSidebarOpen(false);
  };

  const currentChat = chats.find((c) => c.id === currentChatId) || null;

  return (
    <div className="flex h-screen bg-bg text-textPrimary overflow-hidden">
      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 glass transform transition-transform duration-200 ease-in-out
        md:relative md:translate-x-0
        ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}`}
      >
        <ChatList
          chats={chats}
          currentChatId={currentChatId}
          onSelect={handleSelectChat}
          onCreate={handleCreateChat}
        />
      </aside>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-40 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main */}
      <main className="flex-1 flex flex-col h-full">
        {/* Mobile top bar */}
        <div className="md:hidden glass px-4 py-3 flex items-center justify-between border-b border-panelBorder">
          <button onClick={() => setSidebarOpen(true)}>
            ☰
          </button>
          <span className="text-sm font-medium">
            {currentChat?.title || "Klarity"}
          </span>
          <div className="w-6" />
        </div>

        {loading && (
          <div className="px-6 py-2 text-sm text-textSecondary">
            Loading…
          </div>
        )}

        {error && (
          <div className="px-6 py-2 text-sm text-red-400">
            {error}
          </div>
        )}

        <div className="flex-1 overflow-hidden">
          <ChatWindow
            chatId={currentChatId}
            chatTitle={currentChat?.title}
            onFirstMessage={handleFirstMessage}
          />
        </div>
      </main>
    </div>
  );
}
