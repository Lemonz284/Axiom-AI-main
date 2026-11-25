import React, { createContext, useContext } from "react";

interface AuthContextType {
  isSignedIn: boolean;
  isLoaded: boolean;
  user: any;
  getToken: () => Promise<string | null>;
}

const defaultUser = {
  id: "default-user",
  fullName: "Axiom Researcher",
  firstName: "Researcher",
  primaryEmailAddress: { emailAddress: "researcher@axiom.local" },
};

const AuthContext = createContext<AuthContextType>({
  isSignedIn: true,
  isLoaded: true,
  user: defaultUser,
  getToken: async () => "dev-local-token",
});

export const ClerkProvider = ({ children }: { children: React.ReactNode; [key: string]: any }) => {
  return (
    <AuthContext.Provider
      value={{
        isSignedIn: true,
        isLoaded: true,
        user: defaultUser,
        getToken: async () => "dev-local-token",
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  return {
    isSignedIn: ctx.isSignedIn,
    isLoaded: ctx.isLoaded,
    userId: "default-user",
    sessionId: "dev-session",
    getToken: ctx.getToken,
    signOut: async () => {},
  };
};

export const useUser = () => {
  const ctx = useContext(AuthContext);
  return {
    isSignedIn: ctx.isSignedIn,
    isLoaded: ctx.isLoaded,
    user: ctx.user,
  };
};

export const Show = ({
  when,
  children,
}: {
  when: "signed-in" | "signed-out";
  children: React.ReactNode;
}) => {
  const { isSignedIn } = useAuth();
  if (when === "signed-in" && isSignedIn) return <>{children}</>;
  if (when === "signed-out" && !isSignedIn) return <>{children}</>;
  return null;
};

export const SignInButton = ({
  children,
}: {
  children: React.ReactNode;
  mode?: string;
}) => {
  return (
    <span
      onClick={() =>
        alert(
          "Clerk authentication is currently unconfigured in .env.\n\nTo enable sign-in:\n1. Get your keys from https://dashboard.clerk.com\n2. Put VITE_CLERK_PUBLISHABLE_KEY in frontend/.env.local\n3. Put CLERK_SECRET_KEY in backend/.env\n\nYou can click 'Open Workspace' or 'Launch Research Workspace' to explore the demo workspace now!"
        )
      }
    >
      {children}
    </span>
  );
};

export const SignUpButton = ({
  children,
}: {
  children: React.ReactNode;
  mode?: string;
}) => {
  return (
    <span
      onClick={() =>
        alert(
          "Clerk authentication is currently unconfigured in .env.\n\nTo enable sign-up:\n1. Get your keys from https://dashboard.clerk.com\n2. Put VITE_CLERK_PUBLISHABLE_KEY in frontend/.env.local\n3. Put CLERK_SECRET_KEY in backend/.env\n\nYou can click 'Open Workspace' or 'Launch Research Workspace' to explore the demo workspace now!"
        )
      }
    >
      {children}
    </span>
  );
};

export const UserButton = () => (
  <div className="flex items-center gap-2 px-2.5 py-1 rounded-full bg-zinc-900 border border-zinc-700/80 text-xs text-zinc-300">
    <div className="w-2 h-2 rounded-full bg-emerald-400" />
    <span className="font-medium text-xs">Researcher</span>
  </div>
);
