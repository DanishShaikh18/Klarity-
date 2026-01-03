// src/components/MessageBubble.jsx
import React, { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function MessageBubble({
  role = "assistant",
  content = "",
  timestamp,
}) {
  const isUser = role === "user";

  /* ================= ASSISTANT TYPING CONTROL ================= */
  const [displayed, setDisplayed] = useState(content);
  const initialContentRef = useRef(content);

  useEffect(() => {
    if (isUser) return;

    const shouldAnimate =
      initialContentRef.current === "" && content !== "";

    if (!shouldAnimate) {
      setDisplayed(content);
      return;
    }

    setDisplayed("");
    let i = 0;
    const speed = 8;

    const interval = setInterval(() => {
      i++;
      setDisplayed(content.slice(0, i));
      if (i >= content.length) clearInterval(interval);
    }, speed);

    return () => clearInterval(interval);
  }, [content, isUser]);

  /* ================= ASSISTANT ================= */
  if (!isUser) {
    return (
      <div className="flex">
        <div className="max-w-3xl w-full">
          {/* Markdown content */}
          <div className="prose prose-invert max-w-none text-textPrimary leading-relaxed ">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {displayed}
            </ReactMarkdown>
          </div>

          {/* Timestamp */}
          {timestamp && (
            <p className="mt-2 text-xs text-textSecondary">
              {new Date(timestamp).toLocaleTimeString(undefined, {
                hour: "numeric",
                minute: "2-digit",
              })}
            </p>
          )}
        </div>
      </div>
    );
  }

  /* ================= USER ================= */
  return (
    <div className="flex justify-end">
      <div
        className="
          max-w-[70%]
          px-4 py-3
          rounded-2xl rounded-br-md
          bg-white/15
          text-textPrimary
          backdrop-blur-sm
          whitespace-pre-wrap
          break-words
        "
      >
        <p className="text-sm leading-relaxed">{content}</p>

        {timestamp && (
          <p className="mt-2 text-xs text-textSecondary text-right">
            {new Date(timestamp).toLocaleTimeString(undefined, {
              hour: "numeric",
              minute: "2-digit",
            })}
          </p>
        )}
      </div>
    </div>
  );
}
