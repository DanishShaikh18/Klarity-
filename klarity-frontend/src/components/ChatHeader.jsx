// // src/components/ChatHeader.jsx
// import React from "react";
// import FileUploader from "./FileUploader";
// import { motion, AnimatePresence } from "framer-motion";

// export default function ChatHeader({
//   showWelcome,
//   uploading,
//   files,
//   onUpload,
// }) {
//   const hasFiles = files.length > 0;

//   return (
//     <>
//       {/* ===== WELCOME STATE ===== */}
//       <AnimatePresence>
//         {showWelcome && !hasFiles && (
//           <motion.div
//             key="welcome" // 🔴 important: stable key
//             initial={{ opacity: 0, y: 12 }}
//             animate={{ opacity: 1, y: 0 }}
//             exit={{ opacity: 0, y: -12 }}
//             transition={{ duration: 0.25, ease: "easeOut" }}
//             className="glass border-b border-panelBorder"
//           >
//             <div className="max-w-4xl mx-auto px-6 py-20 text-center">
//               <h1 className="text-4xl font-semibold mb-3">
//                 Klarity
//               </h1>

//               <p className="text-textSecondary">
//                 Upload PDFs and ask questions instantly
//               </p>

//               <div className="mt-10 flex justify-center">
//                 {/* ❗ uploader here NEVER reacts to uploading state */}
//                 <FileUploader onUpload={onUpload} />
//               </div>
//             </div>
//           </motion.div>
//         )}
//       </AnimatePresence>

//       {/* ===== COMPACT CHAT HEADER ===== */}
//       {!showWelcome && (
//         <div className="glass border-b border-panelBorder">
//           <div className="max-w-4xl mx-auto px-6 py-2 flex items-center gap-3 overflow-x-auto">
//             {/* Uploaded files */}
//             {files.map((file) => (
//               <div
//                 key={file.id}
//                 className="px-3 py-1.5 rounded-full bg-white/10 text-sm whitespace-nowrap"
//               >
//                 {file.name}
//               </div>
//             ))}

//             {/* ✅ SMALL, INLINE uploading indicator */}
//             {uploading && (
//               <div className="px-3 py-1.5 rounded-full bg-white/10 text-sm text-textSecondary flex items-center gap-2">
//                 <span className="w-2 h-2 rounded-full bg-white/40 animate-pulse" />
//                 Uploading…
//               </div>
//             )}

//             <div className="flex-1" />

//             <FileUploader small onUpload={onUpload} />
//           </div>
//         </div>
//       )}
//     </>
//   );
// }
