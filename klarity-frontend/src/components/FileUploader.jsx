import React, { useRef, useState } from "react";

export default function FileUploader({
  onUpload,
  disabled = false,
  small = false,
}) {
  const inputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);

  const handleFile = async (e) => {
    const file = e.target.files?.[0];
    if (!file || disabled) return;

    if (
      file.type !== "application/pdf" &&
      !file.name.toLowerCase().endsWith(".pdf")
    ) {
      alert("Please select a valid PDF file.");
      e.target.value = "";
      return;
    }

    setUploading(true);
    setUploaded(false);

    try {
      if (!onUpload) throw new Error("No upload handler");
      await onUpload(file);
      setUploaded(true);
      setTimeout(() => setUploaded(false), 1800);
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  return (
    <>
      {/* hidden input */}
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,application/pdf"
        className="hidden"
        onChange={handleFile}
        disabled={disabled || uploading}
      />

      {/* button */}
      <button
        onClick={() => inputRef.current?.click()}
        disabled={disabled || uploading}
        title="Upload PDF"
        className={`
          group relative
          flex items-center gap-2
          px-5 py-2.5
          rounded-full
          text-sm font-medium
          border
          transition-all duration-200
          ${
            uploading
              ? "bg-white/10 border-white/20 text-textSecondary cursor-wait"
              : uploaded
              ? "bg-green-500/10 border-green-500/30 text-green-400"
              : `
                bg-white/5 border-white/10 text-textSecondary
                hover:bg-white/10 hover:border-white/20
                hover:shadow-[0_0_0_4px_rgba(255,255,255,0.03)]
              `
          }
          active:scale-[0.97]
          disabled:opacity-50
        `}
      >
        {/* icon / spinner */}
        {uploading ? (
          <svg
            className="w-4 h-4 animate-spin"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="3"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v8z"
            />
          </svg>
        ) : uploaded ? (
          <span className="text-green-400">✓</span>
        ) : (
          <svg
            className="
              w-4 h-4
              transition-transform
              group-hover:scale-110
            "
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
        )}

        {/* text */}
        <span>
          {uploading
            ? "Uploading…"
            : uploaded
            ? "Uploaded"
            : "Upload PDF"}
        </span>
      </button>
    </>
  );
}
