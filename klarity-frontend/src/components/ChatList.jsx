// klarity-frontend/src/components/ChatList.jsx
import React, { useEffect, useRef, useState } from "react";
import { renameChat, deleteChat } from "../api/chatApi";
import { createPortal } from "react-dom";


export default function ChatList({
  chats = [],
  currentChatId,
  onSelect,
  onCreate,
}) {
  const [localChats, setLocalChats] = useState(chats);
  const [openMenuId, setOpenMenuId] = useState(null);
  const [menuDirection, setMenuDirection] = useState("down"); // ⬅️ NEW
  const [renamingId, setRenamingId] = useState(null);
  const [renameValue, setRenameValue] = useState("");
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);

  const menuRef = useRef(null);
  const renameInputRef = useRef(null);

  useEffect(() => setLocalChats(chats), [chats]);

  /* ========== CLOSE MENU ON OUTSIDE CLICK ========== */
  useEffect(() => {
    const close = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setOpenMenuId(null);
      }
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  /* ========== AUTO FOCUS RENAME ========== */
  useEffect(() => {
    if (renamingId && renameInputRef.current) {
      renameInputRef.current.focus();
      renameInputRef.current.select();
    }
  }, [renamingId]);

  /* ========== RENAME ========== */
  const startRename = (chat) => {
    setRenamingId(chat.id);
    setRenameValue(chat.title || "");
    setOpenMenuId(null);
  };

  const submitRename = async (chatId) => {
    const title = renameValue.trim();
    if (!title) return cancelRename();

    setLocalChats((prev) =>
      prev.map((c) => (c.id === chatId ? { ...c, title } : c))
    );

    try {
      await renameChat(chatId, title);
    } catch (err) {
      console.error(err);
    } finally {
      setRenamingId(null);
    }
  };

  const cancelRename = () => {
    setRenamingId(null);
    setRenameValue("");
  };

  /* ========== DELETE ========== */
  const confirmDelete = async (chatId) => {
    setLocalChats((prev) => prev.filter((c) => c.id !== chatId));
    try {
      await deleteChat(chatId);
    } catch (err) {
      console.error(err);
    } finally {
      setConfirmDeleteId(null);
    }
  };

  /* ========== MENU POSITIONING (CHATGPT STYLE) ========== */
  const openMenu = (chatId, buttonEl) => {
    const rect = buttonEl.getBoundingClientRect();
    const spaceBelow = window.innerHeight - rect.bottom;
    setMenuDirection(spaceBelow < 160 ? "up" : "down");
    setOpenMenuId(chatId);
  };

  return (
    <div className="fixed inset-y-0 left-0 w-70 flex flex-col bg-[#1D1D1E] z-40">
      {/* ================= TOP ================= */}
      <div className="px-5 pt-6 pb-4">
        <div className="text-lg font-semibold mb-4">Klarity</div>

        <button
          onClick={onCreate}
          className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium hover:bg-white/10 transition cursor-pointer"
        >
          <span className="text-lg">＋</span>
          New chat
        </button>

        <p className="mt-3 text-xs text-textSecondary">
          Chats are scoped per PDF
        </p>
      </div>

      <div className="h-px bg-white/5 mx-5" />

      {/* ================= LIST ================= */}
      <div className="flex-1 overflow-y-auto py-4">
        <div className="px-5 mb-3 text-[11px] uppercase tracking-wide text-textSecondary/70">
          Your chats
        </div>

        <ul className="space-y-1">
          {localChats.map((chat) => {
            const selected = currentChatId === chat.id;
            const menuOpen = openMenuId === chat.id;
            const renaming = renamingId === chat.id;

            return (
              <li
                key={chat.id}
                onClick={() => !renaming && onSelect(chat.id)}
                className={`group relative mx-3 px-3 py-2 rounded-xl flex items-start gap-2 cursor-pointer transition ${
                  selected ? "bg-white/15" : "hover:bg-white/10"
                }`}
              >
                {/* TITLE */}
                <div className="flex-1 min-w-0">
                  {renaming ? (
                    <input
                      ref={renameInputRef}
                      value={renameValue}
                      onChange={(e) => setRenameValue(e.target.value)}
                      onBlur={cancelRename}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") submitRename(chat.id);
                        if (e.key === "Escape") cancelRename();
                      }}
                      className="w-full bg-transparent text-sm outline-none border-b border-white/20"
                    />
                  ) : (
                    <>
                      <div className="text-sm truncate">
                        {chat.title || "Untitled chat"}
                      </div>
                      <div className="text-[11px] opacity-60 mt-0.5">
                        {new Date(
                          chat.updated_at || chat.created_at
                        ).toLocaleDateString(undefined, {
                          month: "short",
                          day: "numeric",
                        })}
                      </div>
                    </>
                  )}
                </div>

                {/* 3 DOT MENU */}
                {!renaming && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      openMenu(chat.id, e.currentTarget);
                    }}
                    className="opacity-0 group-hover:opacity-100 p-2 rounded-full hover:bg-white/15 transition cursor-pointer text-lg"
                  >
                    ⋯
                  </button>
                )}

                {menuOpen && (
                  <div
                    ref={menuRef}
                    className={`absolute right-2 ${
                      menuDirection === "up" ? "bottom-12" : "top-12"
                    } w-40 rounded-xl bg-[#242425] border border-white/10 shadow-xl overflow-hidden z-50`}
                    onClick={(e) => e.stopPropagation()}
                  >
                    <button
                      onClick={() => startRename(chat)}
                      className="w-full px-4 py-2 text-left text-sm hover:bg-white/10 cursor-pointer"
                    >
                      Rename
                    </button>
                    <button
                      onClick={() => setConfirmDeleteId(chat.id)}
                      className="w-full px-4 py-2 text-left text-sm text-red-400 hover:bg-white/10 cursor-pointer"
                    >
                      Delete
                    </button>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      </div>

      {/* ================= DELETE MODAL ================= */}
      {confirmDeleteId &&
  createPortal(
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 backdrop-blur-sm">
      <div
        className="
          w-[360px]
          rounded-2xl
          bg-[#242425]
          p-6
          border border-white/10
          shadow-2xl
          animate-[fadeIn_0.15s_ease-out]
        "
      >
        <h3 className="text-base font-semibold mb-1 text-textPrimary">
          Delete chat?
        </h3>

        <p className="text-sm text-textSecondary mb-5">
          This chat and all its messages will be permanently deleted.
        </p>

        <div className="flex justify-end gap-3">
          <button
            onClick={() => setConfirmDeleteId(null)}
            className="
              px-4 py-2
              rounded-lg
              hover:bg-white/10
              transition
              cursor-pointer
            "
          >
            Cancel
          </button>

          <button
            onClick={() => confirmDelete(confirmDeleteId)}
            className="
              px-4 py-2
              rounded-lg
              bg-red-500
              hover:bg-red-600
              text-white
              transition
              cursor-pointer
            "
          >
            Delete
          </button>
        </div>
      </div>
    </div>,
    document.body
  )
}

    </div>
  );
}
