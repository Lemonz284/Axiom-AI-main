import React, { useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { StudioFeatureCard } from "./StudioFeatureCard";
import { FlashcardStudioView } from "./FlashcardStudioView";
import { QuizStudioView } from "./QuizStudioView";
import { MindMapStudioView } from "./MindMapStudioView";
import { RoadmapStudioView } from "./RoadmapStudioView";
import {
  Layers,
  BrainCircuit,
  FileQuestion,
  Network,
  Route,
  Download,
  Sparkles,
} from "lucide-react";
import type { Source } from "../types";

interface StudioPanelProps {
  notebookId: string;
  notebookName: string;
  sources: Source[];
}

type StudioView = "grid" | "flashcards" | "quiz" | "mindmap" | "roadmap";

export const StudioPanel: React.FC<StudioPanelProps> = ({
  notebookId,
  notebookName,
  sources,
}) => {
  const [activeView, setActiveView] = useState<StudioView>("grid");

  const readySources = sources.filter((s) => s.status === "READY");
  const hasReadySources = readySources.length > 0;
  const readySourceIds = readySources.map((s) => s.id);
  const playlistSource = readySources.find(
    (s) => s.type === "youtube_playlist" || s.type === "YOUTUBE_PLAYLIST"
  );

  if (activeView === "flashcards") {
    return (
      <FlashcardStudioView
        notebookId={notebookId}
        sourceIds={readySourceIds}
        notebookName={notebookName}
        onBackToStudio={() => setActiveView("grid")}
      />
    );
  }

  if (activeView === "quiz") {
    return (
      <QuizStudioView
        notebookId={notebookId}
        sourceIds={readySourceIds}
        notebookName={notebookName}
        onBackToStudio={() => setActiveView("grid")}
      />
    );
  }

  if (activeView === "mindmap") {
    return (
      <MindMapStudioView
        notebookId={notebookId}
        sourceIds={readySourceIds}
        notebookName={notebookName}
        onBackToStudio={() => setActiveView("grid")}
      />
    );
  }

  if (activeView === "roadmap" && playlistSource) {
    return (
      <RoadmapStudioView
        notebookId={notebookId}
        playlistSource={playlistSource}
        onBackToStudio={() => setActiveView("grid")}
      />
    );
  }

  return (
    <div className="flex flex-col h-full bg-card">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-primary" />
          <h2 className="text-sm font-semibold text-foreground">Studio</h2>
        </div>
        <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground bg-muted/60 px-2 py-0.5 rounded-full">
          <Download className="w-3 h-3 text-primary" />
          <span>PDF Export Enabled</span>
        </div>
      </div>

      {/* Feature Grid */}
      <ScrollArea className="flex-1">
        <div className="p-4">
          <div className="mb-3.5">
            <p className="text-xs font-medium text-foreground">
              Generate study tools from your sources
            </p>
            <p className="text-[11px] text-muted-foreground mt-0.5">
              Click any tool to open its dedicated view, review contents, and download high-quality PDFs.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-2.5">
            {/* Flashcards */}
            <StudioFeatureCard
              icon={<BrainCircuit className="w-4 h-4 text-primary" />}
              label="Flashcards"
              badge="PDF"
              onClick={() => setActiveView("flashcards")}
              disabled={!hasReadySources}
              disabledReason="Select at least one source"
              colorClass="hover:bg-accent/60 border-border"
            />

            {/* Quiz */}
            <StudioFeatureCard
              icon={<FileQuestion className="w-4 h-4 text-primary" />}
              label="Quiz"
              badge="PDF"
              onClick={() => setActiveView("quiz")}
              disabled={!hasReadySources}
              disabledReason="Select at least one source"
              colorClass="hover:bg-accent/60 border-border"
            />

            {/* Mind Map */}
            <StudioFeatureCard
              icon={<Network className="w-4 h-4 text-primary" />}
              label="Mind Map"
              badge="PDF"
              onClick={() => setActiveView("mindmap")}
              disabled={!hasReadySources}
              disabledReason="Select at least one source"
              colorClass="hover:bg-accent/60 border-border"
            />

            {/* Roadmap */}
            <StudioFeatureCard
              icon={<Route className="w-4 h-4 text-primary" />}
              label="Roadmap"
              badge="PDF"
              onClick={() => setActiveView("roadmap")}
              disabled={!playlistSource}
              disabledReason="Add a YouTube playlist source"
              colorClass="hover:bg-accent/60 border-border"
            />
          </div>

          <div className="mt-4 p-3 rounded-lg border border-border/80 bg-muted/30">
            <div className="flex items-center gap-2 text-xs font-semibold text-foreground">
              <Sparkles className="w-3.5 h-3.5 text-primary" />
              <span>Independent Downloads</span>
            </div>
            <p className="text-[11px] text-muted-foreground mt-1 leading-relaxed">
              Each studio tool generates its own standalone, professionally formatted study PDF. Open any feature above to access its <strong>Download PDF</strong> button.
            </p>
          </div>

          {!hasReadySources && sources.length > 0 && (
            <>
              <Separator className="my-4" />
              <p className="text-xs text-muted-foreground text-center">
                Waiting for sources to finish indexing…
              </p>
            </>
          )}

          {sources.length === 0 && (
            <>
              <Separator className="my-4" />
              <p className="text-xs text-muted-foreground text-center">
                Add a source to get started
              </p>
            </>
          )}
        </div>
      </ScrollArea>
    </div>
  );
};
