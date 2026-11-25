import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const publishableKey = env.VITE_CLERK_PUBLISHABLE_KEY || "";
  const hasValidClerk = Boolean(
    publishableKey &&
    !publishableKey.includes("...") &&
    publishableKey.startsWith("pk_") &&
    publishableKey.length > 20
  );

  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
        ...(!hasValidClerk ? { "@clerk/react": path.resolve(__dirname, "./src/lib/mockClerk.tsx") } : {}),
      },
    },
    server: {
      port: 5173,
      proxy: {
        "/api": {
          target: "http://localhost:3001",
          changeOrigin: true,
        },
      },
    },
  };
});
