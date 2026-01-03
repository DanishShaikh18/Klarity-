// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0f0f10",
        panel: "rgba(255,255,255,0.06)",
        panelBorder: "rgba(255,255,255,0.12)",
        textPrimary: "#e5e7eb",
        textSecondary: "#9ca3af",
        accent: "#22c55e",
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
};
