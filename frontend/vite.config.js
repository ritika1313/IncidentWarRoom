import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The backend has no CORS middleware, so the dev/preview server proxies
// /api/* to FastAPI (prefix stripped). The backend itself is untouched.
const proxy = {
  "/api": {
    target: process.env.VITE_BACKEND_URL || "http://127.0.0.1:8000",
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, ""),
  },
};

export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy },
  preview: { port: 4173, proxy },
});
