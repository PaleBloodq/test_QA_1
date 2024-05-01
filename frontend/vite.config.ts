import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: import.meta.env.VITE_BASE_URL,
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@icons": path.resolve(__dirname, "./src/assets/icons"),
      "@services": path.resolve(__dirname, "./src/services"),
      "@components": path.resolve(__dirname, "./src/components/"),
    },
  },
});
