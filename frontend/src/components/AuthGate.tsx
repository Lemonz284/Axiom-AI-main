import React from "react";
import { SignInButton } from "@clerk/react";
import { Button } from "@/components/ui/button";
import { GoogleIcon } from "./GoogleIcon";
import { ArrowRight, ShieldCheck, Sparkles } from "lucide-react";

export const AuthGate: React.FC<{ onReturnToLanding?: () => void }> = ({ onReturnToLanding }) => {
  return (
    <div className="min-h-screen w-full bg-[#09090b] text-zinc-100 flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* Background radial glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[550px] bg-emerald-500/10 rounded-full blur-[140px] pointer-events-none" />

      {/* Main Card */}
      <div className="relative z-10 w-full max-w-md bg-zinc-900/90 border border-zinc-800/90 rounded-2xl p-8 shadow-2xl backdrop-blur-xl text-center flex flex-col items-center">
        {/* Brand Icon */}
        <div className="w-14 h-14 rounded-2xl bg-zinc-800/80 border border-zinc-700/80 flex items-center justify-center mb-5 shadow-inner">
          <img src="/favicon.png" alt="AxiomAI" className="w-7 h-7 object-contain" />
        </div>

        {/* Title & Description */}
        <h2 className="text-xl font-bold tracking-tight text-white mb-2">
          Sign In to AxiomAI
        </h2>
        <p className="text-xs text-zinc-400 max-w-xs mb-7 leading-relaxed">
          Authentication is required to access research notebooks, multimodal video transcription, and AI study tools.
        </p>

        {/* Action Buttons */}
        <div className="w-full space-y-3">
          <SignInButton mode="modal">
            <Button
              size="lg"
              className="w-full h-11 bg-white hover:bg-zinc-100 text-zinc-950 font-semibold text-xs sm:text-sm gap-2.5 rounded-xl shadow-lg transition-all hover:scale-[1.01]"
            >
              <GoogleIcon className="w-4 h-4" />
              <span>Continue with Google</span>
              <ArrowRight className="w-4 h-4 text-zinc-600 ml-auto" />
            </Button>
          </SignInButton>

          <SignInButton mode="modal">
            <Button
              variant="outline"
              size="lg"
              className="w-full h-11 border-zinc-800 bg-zinc-900 hover:bg-zinc-800 text-zinc-300 text-xs sm:text-sm font-medium rounded-xl"
            >
              Sign In with Email / Other
            </Button>
          </SignInButton>
        </div>

        {/* Trust Badges */}
        <div className="mt-8 pt-6 border-t border-zinc-800/80 w-full flex items-center justify-center gap-4 text-[11px] text-zinc-500 font-mono">
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Secure Clerk Auth</span>
          </div>
          <span className="text-zinc-700">·</span>
          <div className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-zinc-400" />
            <span>Isolated Workspaces</span>
          </div>
        </div>

        {onReturnToLanding && (
          <button
            onClick={onReturnToLanding}
            className="mt-5 text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
          >
            ← Back to Home
          </button>
        )}
      </div>
    </div>
  );
};
