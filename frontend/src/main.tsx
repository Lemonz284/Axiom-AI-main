/// <reference types="vite/client" />
import { ClerkProvider } from "@clerk/react";
import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { ClerkSetupGuide } from "./components/ClerkSetupGuide";
import "./index.css";

const RAW_PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY || "";
const isKeyConfigured =
  typeof RAW_PUBLISHABLE_KEY === "string" &&
  RAW_PUBLISHABLE_KEY.startsWith("pk_") &&
  !RAW_PUBLISHABLE_KEY.includes("...") &&
  RAW_PUBLISHABLE_KEY.length > 20;

function Root() {
  const [bypassed, setBypassed] = useState(false);

  if (!isKeyConfigured && !bypassed) {
    return <ClerkSetupGuide onTemporaryBypass={() => setBypassed(true)} />;
  }

  return (
    <ClerkProvider
      publishableKey={isKeyConfigured ? RAW_PUBLISHABLE_KEY : "pk_test_placeholder"}
      afterSignOutUrl="/"
    >
      <App />
    </ClerkProvider>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>
);
