import React, { useRef, useState } from "react";
import ReactMarkdown from "react-markdown";

export default function ChatSummaryPanel({
  open,
  loading,
  summary,
  onClose,
  onRegenerate,
}) {
  const [copied, setCopied] = useState(false);
  const contentRef = useRef(null);

  if (!open) return null;

  const handleCopy = async () => {
    if (!contentRef.current) return;
    await navigator.clipboard.writeText(contentRef.current.innerText);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/60">
      <div className="
        h-full w-full md:w-[75%] lg:w-[60%]
        bg-[#1D1D1E]
        border-l border-white/10
        flex flex-col
        animate-slide-in
      ">
        {/* HEADER */}
        <div className="px-6 py-4 flex justify-between border-b border-white/10">
          <h2 className="text-lg font-semibold">Chat Summary</h2>

          <div className="flex gap-2">
            <button
              onClick={onRegenerate}
              className="px-3 py-1.5 text-sm rounded-md bg-white/10 hover:bg-white/20 transition"
            >
              Regenerate
            </button>

            <button
              onClick={handleCopy}
              className={`px-3 py-1.5 text-sm rounded-md transition ${
                copied
                  ? "bg-green-500/20 text-green-400"
                  : "bg-white/10 hover:bg-white/20"
              }`}
            >
              {copied ? "Copied ✓" : "Copy"}
            </button>

            <button
              onClick={onClose}
              className="text-lg text-textSecondary hover:text-textPrimary"
            >
              ✕
            </button>
          </div>
        </div>

        {/* CONTENT */}
        <div className="flex-1 overflow-y-auto px-6 py-6">
          {loading ? (
            <div className="animate-pulse text-textSecondary">
              Generating summary…
            </div>
          ) : summary ? (
            <div
              ref={contentRef}
              className="prose prose-invert max-w-none text-sm"
            >
              <ReactMarkdown>{summary}</ReactMarkdown>
            </div>
          ) : (
            <div className="text-textSecondary text-sm">
              No summary available.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
