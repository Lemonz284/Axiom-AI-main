import React, { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Send,
  Bot,
  User,
  BookmarkCheck,
  Plus,
  Volume2,
  VolumeX,
  Copy,
  Check,
  Sparkles,
} from "lucide-react";
import { QueryMessage, Citation } from "./types";
import { NotebookOverviewCard } from "./NotebookOverviewCard";
import { cleanTextForSpeech } from "../lib/speechUtils";

interface ChatViewProps {
  notebookId: string;
  notebookName?: string;
  messages: QueryMessage[];
  onSendMessage: (question: string) => Promise<void>;
  onCitationClick: (chunkId: string) => void;
  isLoading: boolean;
  sourceCount: number;
  onOpenAddSource?: () => void;
}

const QUICK_PROMPTS = [
  "Summarize core thesis & findings",
  "Key definitions & formulas",
  "Explain for beginners (ELI5)",
  "Critical limitations & caveats",
];

export const ChatView: React.FC<ChatViewProps> = ({
  notebookId,
  notebookName,
  messages,
  onSendMessage,
  onCitationClick,
  isLoading,
  sourceCount,
  onOpenAddSource,
}) => {
  const [inputQuery, setInputQuery] = useState("");
  const [speakingMsgId, setSpeakingMsgId] = useState<string | null>(null);
  const [copiedMsgId, setCopiedMsgId] = useState<string | null>(null);

  // Clean up speech synthesis on component unmount
  useEffect(() => {
    return () => {
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputQuery.trim() || isLoading) return;
    const q = inputQuery.trim();
    setInputQuery("");
    await onSendMessage(q);
  };

  const handleQuickPromptClick = async (prompt: string) => {
    if (isLoading) return;
    await onSendMessage(prompt);
  };

  const handleToggleSpeech = (msgId: string, text: string) => {
    if (!("speechSynthesis" in window)) {
      alert("Speech synthesis is not supported in this browser.");
      return;
    }

    if (speakingMsgId === msgId) {
      window.speechSynthesis.cancel();
      setSpeakingMsgId(null);
      return;
    }

    window.speechSynthesis.cancel();
    const spokenText = cleanTextForSpeech(text);
    if (!spokenText) return;

    const utterance = new SpeechSynthesisUtterance(spokenText);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.onend = () => setSpeakingMsgId(null);
    utterance.onerror = () => setSpeakingMsgId(null);
    setSpeakingMsgId(msgId);
    window.speechSynthesis.speak(utterance);
  };

  const renderInlineFormatted = (
    text: string,
    citations: Citation[],
    keyPrefix: string
  ): React.ReactNode => {
    const regex = /(\[CID:[a-zA-Z0-9_-]+\]|\[\d+\]|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
    const parts = text.split(regex);

    return parts.map((part, idx) => {
      if (!part) return null;
      const key = `${keyPrefix}-${idx}`;

      if (part.startsWith("[CID:") && part.endsWith("]")) {
        const cid = part.slice(5, -1);
        const citIdx = citations.findIndex((c) => c.chunkId === cid);
        const displayNum = citIdx !== -1 ? citIdx + 1 : 1;
        return (
          <button
            key={key}
            onClick={() => onCitationClick(cid)}
            className="inline-flex items-center justify-center px-1.5 py-0 mx-0.5 rounded text-[10px] font-mono font-bold bg-primary/10 text-primary hover:bg-primary/20 border border-primary/30 align-baseline transition-colors"
            title={`Jump to Grounded Citation [${displayNum}]`}
          >
            [{displayNum}]
          </button>
        );
      }

      if (/^\[\d+\]$/.test(part)) {
        const num = parseInt(part.slice(1, -1), 10);
        const cit = citations[num - 1];
        return (
          <button
            key={key}
            onClick={() => cit && onCitationClick(cit.chunkId)}
            className="inline-flex items-center justify-center px-1.5 py-0 mx-0.5 rounded text-[10px] font-mono font-bold bg-primary/10 text-primary hover:bg-primary/20 border border-primary/30 align-baseline transition-colors"
            title={cit ? `Jump to Grounded Citation [${num}]` : `Citation [${num}]`}
          >
            [{num}]
          </button>
        );
      }

      if (part.startsWith("**") && part.endsWith("**") && part.length > 4) {
        return <strong key={key} className="font-semibold text-foreground">{part.slice(2, -2)}</strong>;
      }

      if (part.startsWith("*") && part.endsWith("*") && part.length > 2) {
        return <em key={key} className="italic text-foreground/90">{part.slice(1, -1)}</em>;
      }

      if (part.startsWith("`") && part.endsWith("`") && part.length > 2) {
        return (
          <code key={key} className="px-1.5 py-0.5 rounded bg-muted font-mono text-[11px] text-foreground border border-border/80">
            {part.slice(1, -1)}
          </code>
        );
      }

      return part;
    });
  };

  const renderFormattedAnswer = (rawText: string, citations: Citation[]) => {
    const lines = rawText.split("\n");
    const elements: React.ReactNode[] = [];
    let i = 0;

    while (i < lines.length) {
      const line = lines[i];

      if (!line.trim()) {
        i++;
        continue;
      }

      // Fenced Code Block
      if (line.trim().startsWith("```")) {
        const codeLines: string[] = [];
        i++;
        while (i < lines.length && !lines[i].trim().startsWith("```")) {
          codeLines.push(lines[i]);
          i++;
        }
        if (i < lines.length) i++;
        elements.push(
          <pre key={`code-${i}`} className="p-3 my-2.5 rounded-lg bg-zinc-950 border border-zinc-800 text-zinc-100 font-mono text-[11px] overflow-x-auto leading-relaxed">
            <code>{codeLines.join("\n")}</code>
          </pre>
        );
        continue;
      }

      // Markdown Table
      if (line.trim().startsWith("|") && line.trim().endsWith("|")) {
        const tableLines: string[] = [];
        while (i < lines.length && lines[i].trim().startsWith("|") && lines[i].trim().endsWith("|")) {
          tableLines.push(lines[i]);
          i++;
        }

        const parseRow = (rowStr: string) =>
          rowStr
            .split("|")
            .slice(1, -1)
            .map((c) => c.trim());

        if (tableLines.length >= 2) {
          const headerCols = parseRow(tableLines[0]);
          const hasDivider = tableLines[1].includes("---");
          const bodyRows = tableLines.slice(hasDivider ? 2 : 1).map(parseRow);

          elements.push(
            <div key={`table-${i}`} className="overflow-x-auto my-3 rounded-lg border border-border">
              <table className="w-full text-xs text-left border-collapse">
                <thead className="bg-muted/60 text-foreground font-semibold border-b border-border">
                  <tr>
                    {headerCols.map((col, cIdx) => (
                      <th key={`th-${cIdx}`} className="px-3 py-2 border-r border-border/50 last:border-r-0">
                        {renderInlineFormatted(col, citations, `th-${i}-${cIdx}`)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/60">
                  {bodyRows.map((row, rIdx) => (
                    <tr key={`tr-${rIdx}`} className="hover:bg-muted/30 transition-colors">
                      {row.map((cell, cIdx) => (
                        <td key={`td-${rIdx}-${cIdx}`} className="px-3 py-2 border-r border-border/50 last:border-r-0">
                          {renderInlineFormatted(cell, citations, `td-${i}-${rIdx}-${cIdx}`)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
          continue;
        }
      }

      // Blockquotes
      if (line.trim().startsWith(">")) {
        const quoteLines: string[] = [];
        while (i < lines.length && lines[i].trim().startsWith(">")) {
          quoteLines.push(lines[i].replace(/^>\s?/, ""));
          i++;
        }
        const fullQuote = quoteLines.join("\n");
        const isAxiomNote = fullQuote.includes("Note from AxiomAI");

        elements.push(
          <div
            key={`quote-${i}`}
            className={cn(
              "my-3 p-3.5 rounded-xl border text-xs leading-relaxed",
              isAxiomNote
                ? "border-indigo-500/30 bg-indigo-50/70 dark:bg-indigo-950/30 text-indigo-950 dark:text-indigo-200"
                : "border-border bg-muted/30 text-foreground/90 italic"
            )}
          >
            {isAxiomNote && (
              <div className="flex items-center gap-1.5 font-bold text-[11px] text-indigo-600 dark:text-indigo-300 uppercase tracking-wider mb-1.5">
                <Sparkles className="w-3.5 h-3.5" />
                <span>AxiomAI Knowledge Note</span>
              </div>
            )}
            <div className="whitespace-pre-line">
              {renderInlineFormatted(fullQuote, citations, `quote-body-${i}`)}
            </div>
          </div>
        );
        continue;
      }

      // Headers
      if (line.startsWith("### ")) {
        elements.push(
          <h4 key={`h4-${i}`} className="text-sm font-bold text-foreground mt-4 mb-1.5">
            {renderInlineFormatted(line.slice(4), citations, `h4-${i}`)}
          </h4>
        );
        i++;
        continue;
      }

      if (line.startsWith("## ")) {
        elements.push(
          <h3 key={`h3-${i}`} className="text-base font-bold text-foreground mt-5 mb-2 pb-1 border-b border-border/50">
            {renderInlineFormatted(line.slice(3), citations, `h3-${i}`)}
          </h3>
        );
        i++;
        continue;
      }

      if (line.startsWith("# ")) {
        elements.push(
          <h2 key={`h2-${i}`} className="text-lg font-bold text-foreground mt-6 mb-2">
            {renderInlineFormatted(line.slice(2), citations, `h2-${i}`)}
          </h2>
        );
        i++;
        continue;
      }

      // Horizontal divider
      if (line.trim() === "---" || line.trim() === "***") {
        elements.push(<hr key={`hr-${i}`} className="my-3 border-border/60" />);
        i++;
        continue;
      }

      // Lists
      const isBullet = /^[*-●]\s+/.test(line.trim());
      const isNumberList = /^\d+\.\s+/.test(line.trim());

      if (isBullet || isNumberList) {
        const listItems: { text: string; num?: string }[] = [];
        while (i < lines.length && (/^[*-●]\s+/.test(lines[i].trim()) || /^\d+\.\s+/.test(lines[i].trim()))) {
          const cur = lines[i].trim();
          if (/^\d+\.\s+/.test(cur)) {
            const dotIdx = cur.indexOf(".");
            listItems.push({ text: cur.slice(dotIdx + 1).trim(), num: cur.slice(0, dotIdx + 1) });
          } else {
            listItems.push({ text: cur.replace(/^[*-●]\s+/, "") });
          }
          i++;
        }

        elements.push(
          <ul key={`list-${i}`} className="space-y-1.5 my-2">
            {listItems.map((item, lIdx) => (
              <li key={`li-${lIdx}`} className="flex items-start gap-2 text-xs text-foreground leading-relaxed">
                <span className="shrink-0 text-primary font-bold text-[11px] mt-0.5">
                  {item.num || "•"}
                </span>
                <span className="flex-1">
                  {renderInlineFormatted(item.text, citations, `li-${i}-${lIdx}`)}
                </span>
              </li>
            ))}
          </ul>
        );
        continue;
      }

      // Normal paragraph
      elements.push(
        <p key={`p-${i}`} className="text-xs text-foreground leading-relaxed my-2">
          {renderInlineFormatted(line, citations, `p-${i}`)}
        </p>
      );
      i++;
    }

    return <div className="space-y-1">{elements}</div>;
  };

  const handleCopyMessage = (msgId: string, text: string, citations: Citation[]) => {
    let content = text;
    if (citations.length > 0) {
      content += "\n\n---\n**Grounded Sources:**\n";
      citations.forEach((c, idx) => {
        content += `[${idx + 1}] ${c.sourceTitle || "Source"}: "${c.snippet}"\n`;
      });
    }
    navigator.clipboard.writeText(content);
    setCopiedMsgId(msgId);
    setTimeout(() => setCopiedMsgId(null), 2000);
  };

  const parseCitations = (citationsRaw: any): Citation[] => {
    if (!citationsRaw) return [];
    if (Array.isArray(citationsRaw)) return citationsRaw;
    try {
      return JSON.parse(citationsRaw);
    } catch (err) {
      return [];
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-background relative min-h-0 overflow-hidden">
      {/* Header */}
      <div className="px-6 py-3 border-b border-border bg-card/60 backdrop-blur flex items-center justify-between shrink-0 z-10">
        <span className="text-xs font-semibold text-foreground tracking-tight">
          {notebookName || "Untitled Document"}
        </span>
        <span className="text-[11px] font-mono text-muted-foreground">
          {sourceCount} source{sourceCount === 1 ? "" : "s"} connected
        </span>
      </div>

      {/* Message List */}
      <ScrollArea className="flex-1 min-h-0">
        <div className="px-6 pt-6 pb-36 space-y-6">
          {/* Overview card (shows when sources exist) */}
          {sourceCount > 0 && (
            <NotebookOverviewCard
              notebookId={notebookId}
              sourceCount={sourceCount}
              onQuestionSelect={async (q) => {
                if (isLoading) return;
                await onSendMessage(q);
              }}
              hasMessages={messages.length > 0}
            />
          )}

          {/* Empty state — no sources */}
          {sourceCount === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-center p-8 max-w-md mx-auto pt-20 space-y-4">
              <div className="w-12 h-12 rounded-xl bg-card border border-border flex items-center justify-center text-foreground">
                <Bot className="w-6 h-6" />
              </div>
              <div className="space-y-1">
                <h3 className="text-sm font-semibold text-foreground">No Knowledge Sources Yet</h3>
                <p className="text-xs text-muted-foreground leading-relaxed max-w-xs">
                  Upload research PDFs, YouTube videos, web articles, or notes to ground your AI assistant with verifiable citations.
                </p>
              </div>
              {onOpenAddSource && (
                <Button
                  onClick={onOpenAddSource}
                  size="sm"
                  className="bg-primary text-primary-foreground hover:bg-zinc-200 text-xs gap-1.5 font-medium"
                >
                  <Plus className="w-3.5 h-3.5" />
                  Add Knowledge Source
                </Button>
              )}
            </div>
          )}

          {/* Chat messages */}
          {messages.map((msg) => {
            const citations = parseCitations(msg.answer?.citations);

            return (
              <div key={msg.id} className="space-y-3 max-w-3xl mx-auto">
                {/* User Question */}
                <div className="flex items-start gap-3 justify-end">
                  <div className="bg-secondary border border-border rounded-xl px-4 py-2.5 text-xs text-foreground max-w-lg leading-relaxed shadow-sm">
                    {msg.question}
                  </div>
                  <div className="w-6 h-6 rounded-md bg-zinc-800 border border-zinc-700 flex items-center justify-center text-zinc-300 text-xs font-semibold shrink-0 mt-0.5">
                    <User className="w-3.5 h-3.5" />
                  </div>
                </div>

                {/* AI Answer */}
                {msg.answer && (
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 rounded-md bg-zinc-800 border border-zinc-700 flex items-center justify-center text-zinc-200 shrink-0 mt-0.5">
                      <Bot className="w-3.5 h-3.5" />
                    </div>
                    <div className="flex-1 space-y-3 bg-card/60 border border-border rounded-xl p-4 shadow-sm">
                      {renderFormattedAnswer(msg.answer.text, citations)}

                      {/* Verifiable Citations */}
                      {citations.length > 0 && (
                        <div className="pt-3 border-t border-border">
                          <div className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2 flex items-center gap-1.5">
                            <BookmarkCheck className="w-3 h-3 text-zinc-400" />
                            Grounded Sources ({citations.length})
                          </div>
                          <div className="flex flex-wrap gap-1.5">
                            {citations.map((cit, idx) => (
                              <button
                                key={`${cit.chunkId}-${idx}`}
                                onClick={() => onCitationClick(cit.chunkId)}
                                className="group flex items-center gap-1.5 px-2 py-0.5 rounded bg-background hover:bg-accent border border-border text-xs text-muted-foreground hover:text-foreground transition"
                                title={cit.snippet}
                              >
                                <span className="font-mono font-semibold text-zinc-300">[{idx + 1}]</span>
                                <span className="truncate max-w-[150px]">{cit.snippet}</span>
                              </button>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Utilities Bar: Read Aloud + Copy */}
                      <div className="flex items-center justify-end gap-2 pt-2 border-t border-border/40 text-[11px] text-muted-foreground">
                        <button
                          onClick={() => handleToggleSpeech(msg.id, msg.answer!.text)}
                          className={`flex items-center gap-1 px-2 py-0.5 rounded border text-[11px] transition-colors ${
                            speakingMsgId === msg.id
                              ? "bg-zinc-800 border-zinc-600 text-white"
                              : "border-border/60 hover:bg-accent hover:text-foreground"
                          }`}
                          title={speakingMsgId === msg.id ? "Stop audio read-aloud" : "Read aloud (zero-cost browser TTS)"}
                        >
                          {speakingMsgId === msg.id ? (
                            <>
                              <VolumeX className="w-3 h-3 text-rose-400" />
                              <span className="text-rose-400">Stop</span>
                            </>
                          ) : (
                            <>
                              <Volume2 className="w-3 h-3" />
                              <span>Listen</span>
                            </>
                          )}
                        </button>

                        <button
                          onClick={() => handleCopyMessage(msg.id, msg.answer!.text, citations)}
                          className="flex items-center gap-1 px-2 py-0.5 rounded border border-border/60 hover:bg-accent hover:text-foreground transition-colors text-[11px]"
                          title="Copy answer with markdown citations"
                        >
                          {copiedMsgId === msg.id ? (
                            <>
                              <Check className="w-3 h-3 text-emerald-400" />
                              <span className="text-emerald-400 font-medium">Copied</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3 h-3" />
                              <span>Copy</span>
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}

          {isLoading && (
            <div className="flex items-center gap-3 max-w-3xl mx-auto">
              <div className="w-6 h-6 rounded-md bg-zinc-800 border border-zinc-700 flex items-center justify-center text-zinc-300 animate-pulse">
                <Bot className="w-3.5 h-3.5" />
              </div>
              <div className="text-xs text-muted-foreground animate-pulse font-mono">
                Searching vectors & synthesizing grounded response...
              </div>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Floating Query Bar + Quick Prompts */}
      <div className="absolute bottom-5 left-0 right-0 px-6 z-20 pointer-events-none">
        <div className="max-w-3xl mx-auto space-y-2 pointer-events-auto">
          {/* Quick Prompt Pills */}
          {sourceCount > 0 && (
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 justify-center scrollbar-none">
              {QUICK_PROMPTS.map((prompt, idx) => (
                <button
                  key={idx}
                  type="button"
                  disabled={isLoading}
                  onClick={() => handleQuickPromptClick(prompt)}
                  className="text-[11px] px-2.5 py-1 rounded-full border border-border/80 bg-card/90 text-muted-foreground hover:text-foreground hover:border-zinc-500 transition-colors whitespace-nowrap shadow-sm backdrop-blur-md cursor-pointer"
                >
                  {prompt}
                </button>
              ))}
            </div>
          )}

          {/* Form Input */}
          <form onSubmit={handleSubmit} className="flex items-center relative">
            <input
              type="text"
              placeholder="Ask a grounded question about your sources..."
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              disabled={isLoading}
              className="w-full text-xs px-4 py-3 bg-card border border-border rounded-xl text-foreground placeholder-muted-foreground focus:outline-none focus:border-zinc-500 transition shadow-lg"
            />
            <div className="absolute right-2.5 flex items-center gap-2">
              <Button
                type="submit"
                size="sm"
                disabled={!inputQuery.trim() || isLoading}
                className="h-7 w-7 p-0 rounded-lg bg-primary text-primary-foreground hover:bg-zinc-200"
              >
                <Send className="w-3.5 h-3.5" />
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
