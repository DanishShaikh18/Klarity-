import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import SingleChatPage from "./pages/SingleChatPage";

export default function App() {
  return (
    <Routes>
      {/* Landing / New chat */}
      <Route path="/" element={<SingleChatPage />} />

      {/* Specific chat */}
      <Route path="/chat/:chatId" element={<SingleChatPage />} />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
