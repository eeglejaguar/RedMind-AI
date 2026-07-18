import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        void: "#0a0505",
        panel: "#150a0a",
        "panel-raised": "#1f0e0e",
        "panel-hover": "#2a1414",
        red: {
          primary: "#ff1a1a",
          glow: "#ff3333",
          dim: "#6b0f0f",
        },
        critical: "#ff0033",
        high: "#ff6600",
        medium: "#ffb700",
        low: "#3ea6ff",
        info: "#8a6a6a",
        hairline: "rgba(255,26,26,0.15)",
        "text-primary": "#f5e6e6",
        "text-muted": "#8a6a6a",
      },
      fontFamily: {
        display: ["Chakra Petch", "Rajdhani", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      keyframes: {
        scanline: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
        pulseglow: {
          "0%, 100%": { boxShadow: "0 0 6px rgba(255,26,26,0.4)" },
          "50%": { boxShadow: "0 0 18px rgba(255,51,51,0.9)" },
        },
        flashborder: {
          "0%": { borderColor: "rgba(255,0,51,1)" },
          "100%": { borderColor: "rgba(255,0,51,0)" },
        },
      },
      animation: {
        scanline: "scanline 2.4s linear infinite",
        pulseglow: "pulseglow 1.6s ease-in-out infinite",
        flashborder: "flashborder 0.8s ease-out",
      },
    },
  },
  plugins: [],
};
export default config;
