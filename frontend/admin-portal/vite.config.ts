import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Super Admin Portal — talks ONLY to its own BFF under /api/admin/.
// CLAUDE.md Part 4.3: cross-portal API access is forbidden at
// the BFF layer; the dev proxy reflects that boundary.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3004,
    proxy: {
      "/api/admin": "http://localhost:8000",
    },
  },
});
