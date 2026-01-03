// src/components/ChatBox.jsx
import React, { useEffect, useRef, useState } from "react";
import MessageBubble from "./MessageBubble";

export default function ChatBox({ messages = [], loading = false }) {
  const containerRef = useRef(null);
  const bottomRef = useRef(null);

  const [autoScroll, setAutoScroll] = useState(true);

  // Detect user scroll
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const handleScroll = () => {
      const nearBottom =
        el.scrollHeight - el.scrollTop - el.clientHeight < 80;

      setAutoScroll(nearBottom);
    };

    el.addEventListener("scroll", handleScroll);
    return () => el.removeEventListener("scroll", handleScroll);
  }, []);

  // Auto-scroll while messages / typing updates
  useEffect(() => {
    if (!autoScroll) return;
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading, autoScroll]);

  return (
    <div
      ref={containerRef}
      className="
        flex-1 overflow-y-auto
        px-6 pt-8 pb-44
        text-textPrimary
      "
    >
      <div className="max-w-3xl mx-auto space-y-6">
        {messages.map((m) => (
          <MessageBubble
            key={m.id}
            role={m.role}
            content={m.content ?? ""}
            timestamp={m.timestamp}
          />
        ))}

        {loading && (
          <div className="flex animate-pulse">
            <div className="flex-1 space-y-3">
              <div className="h-4 bg-white/10 rounded w-3/4" />
              <div className="h-4 bg-white/10 rounded w-1/2" />
              <div className="h-4 bg-white/10 rounded w-5/6" />
            </div>
          </div>
        )}
      </div>

      <div ref={bottomRef} />
    </div>
  );
}
