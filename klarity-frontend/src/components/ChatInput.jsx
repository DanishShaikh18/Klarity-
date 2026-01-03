// src/components/ChatInput.jsx
import React, { useState, useRef, useEffect } from "react";

export default function ChatInput({ onSend, disabled = false, onUpload }) {
  const [value, setValue] = useState("");
  const textareaRef = useRef(null);

  const send = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  };

  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 140) + "px";
  }, [value]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <div className="bg-bg px-3 pb-5">
      <div
        className="
          max-w-3xl mx-auto
          glass
          rounded-full
          px-4 py-2
          flex items-center gap-2
          backdrop-blur-md
        "
      >
        {onUpload && (
          <label className="flex-shrink-0 cursor-pointer">
            <input
              type="file"
              accept=".pdf"
              className="hidden"
              disabled={disabled}
              onChange={(e) => {
                if (e.target.files?.[0]) {
                  onUpload(e.target.files[0]);
                  e.target.value = "";
                }
              }}
            />
            <div className="flex place-items-start rounded-full text-textSecondary text-2xl hover:bg-white/10">
              +
            </div>
          </label>
        )}

        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask Klarity…"
          rows={1}
          disabled={disabled}
          className="
            flex-1 resize-none bg-transparent
            text-textPrimary placeholder:text-textSecondary/60
            text-sm leading-relaxed
            focus:outline-none
          "
        />

        <button
          onClick={send}
          disabled={disabled || !value.trim()}
          className="
            p-2 rounded-full
            bg-white/20 hover:bg-white/30
            disabled:bg-white/5
          "
        >
          ➤
        </button>
      </div>
    </div>
  );
}
