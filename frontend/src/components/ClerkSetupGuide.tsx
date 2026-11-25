import React, { useState } from "react";
import { GoogleIcon } from "./GoogleIcon";
import { Button } from "@/components/ui/button";
import { ExternalLink, Copy, Check, ShieldCheck, Key, Sparkles, ArrowRight } from "lucide-react";

export const ClerkSetupGuide: React.FC<{ onTemporaryBypass?: () => void }> = ({ onTemporaryBypass }) => {
  const [copied, setCopied] = useState<string | null>(null);

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="min-h-screen w-full bg-[#09090b] text-zinc-100 flex flex-col items-center justify-center p-4 sm:p-6 relative overflow-hidden font-sans">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-emerald-500/10 rounded-full blur-[150px] pointer-events-none" />

      <div className="relative z-10 w-full max-w-xl bg-zinc-900/90 border border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-2xl backdrop-blur-xl">
        {/* Header */}
        <div className="flex items-center gap-3.5 mb-6">
          <div className="w-10 h-10 rounded-xl bg-zinc-800 border border-zinc-700 flex items-center justify-center overflow-hidden shrink-0 shadow-sm">
            <GoogleIcon className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
              <span>Google Authentication Setup</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Clerk
              </span>
            </h2>
            <p className="text-xs text-zinc-400">
              One quick step to activate Google Sign-In and lock your workspaces.
            </p>
          </div>
        </div>

        {/* 3 Simple Steps */}
        <div className="space-y-3.5 mb-6 text-xs">
          {/* Step 1 */}
          <div className="p-3.5 rounded-xl border border-zinc-800/80 bg-zinc-950/60 flex items-start gap-3">
            <div className="w-5 h-5 rounded-full bg-zinc-800 border border-zinc-700 text-zinc-300 font-mono text-[11px] flex items-center justify-center shrink-0 mt-0.5">
              1
            </div>
            <div className="flex-1">
              <div className="font-semibold text-zinc-200 mb-0.5 flex items-center justify-between">
                <span>Enable Google in Clerk Dashboard</span>
                <a
                  href="https://dashboard.clerk.com"
                  target="_blank"
                  rel="noreferrer"
                  className="text-emerald-400 hover:text-emerald-300 flex items-center gap-1 font-mono text-[11px]"
                >
                  dashboard.clerk.com
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
              <p className="text-zinc-400 leading-relaxed text-[11px]">
                Create a free account $\to$ Go to <strong>Configure &gt; Social Connections</strong> $\to$ Toggle on <strong>Google</strong>.
              </p>
            </div>
          </div>

          {/* Step 2 */}
          <div className="p-3.5 rounded-xl border border-zinc-800/80 bg-zinc-950/60 flex items-start gap-3">
            <div className="w-5 h-5 rounded-full bg-zinc-800 border border-zinc-700 text-zinc-300 font-mono text-[11px] flex items-center justify-center shrink-0 mt-0.5">
              2
            </div>
            <div className="flex-1">
              <div className="font-semibold text-zinc-200 mb-1 flex items-center justify-between">
                <span>Paste Publishable Key in frontend/.env.local</span>
                <button
                  onClick={() => copyToClipboard('VITE_CLERK_PUBLISHABLE_KEY="pk_test_..."', 'f-env')}
                  className="text-zinc-400 hover:text-zinc-200 flex items-center gap-1 text-[11px]"
                >
                  {copied === 'f-env' ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>Copy variable</span>
                </button>
              </div>
              <code className="block p-2 rounded bg-zinc-900 border border-zinc-800 text-[11px] font-mono text-zinc-300 select-all">
                VITE_CLERK_PUBLISHABLE_KEY=&quot;pk_test_your_actual_key&quot;
              </code>
            </div>
          </div>

          {/* Step 3 */}
          <div className="p-3.5 rounded-xl border border-zinc-800/80 bg-zinc-950/60 flex items-start gap-3">
            <div className="w-5 h-5 rounded-full bg-zinc-800 border border-zinc-700 text-zinc-300 font-mono text-[11px] flex items-center justify-center shrink-0 mt-0.5">
              3
            </div>
            <div className="flex-1">
              <div className="font-semibold text-zinc-200 mb-1 flex items-center justify-between">
                <span>Paste Secret Key in backend/.env</span>
                <button
                  onClick={() => copyToClipboard('CLERK_SECRET_KEY="sk_test_..."', 'b-env')}
                  className="text-zinc-400 hover:text-zinc-200 flex items-center gap-1 text-[11px]"
                >
                  {copied === 'b-env' ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>Copy variable</span>
                </button>
              </div>
              <code className="block p-2 rounded bg-zinc-900 border border-zinc-800 text-[11px] font-mono text-zinc-300 select-all">
                CLERK_SECRET_KEY=&quot;sk_test_your_secret_key&quot;
              </code>
            </div>
          </div>
        </div>

        {/* Footer info & Dev Preview Bypass */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-4 border-t border-zinc-800/80 text-[11px] text-zinc-500 font-mono">
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Strict Auth Gate Enabled</span>
          </div>

          {onTemporaryBypass && (
            <button
              onClick={onTemporaryBypass}
              className="text-zinc-400 hover:text-white transition-colors underline flex items-center gap-1"
            >
              <span>Preview Landing Page without keys</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
