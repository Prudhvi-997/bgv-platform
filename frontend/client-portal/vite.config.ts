import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Client Portal — talks ONLY to its own BFF under /api/client/.
// CLAUDE.md Part 4.3: cross-portal API access is forbidden at
// the BFF layer; the dev proxy reflects that boundary.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3001,
    proxy: {
      "/api/client": "http://localhost:8000",
    },
  },
});
