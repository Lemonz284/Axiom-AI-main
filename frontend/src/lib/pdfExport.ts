import { jsPDF } from "jspdf";
import { Roadmap, FlashcardDeck, Quiz, MindMap } from "../components/types";

// ---------------------------------------------------------------------------
// Design System Constants (A4: 210mm x 297mm)
// ---------------------------------------------------------------------------
const PAGE_WIDTH = 210;
const PAGE_HEIGHT = 297;
const MARGIN_X = 18;
const MARGIN_TOP = 20;
const MARGIN_BOTTOM = 20;
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN_X * 2; // 174mm
const FOOTER_Y = PAGE_HEIGHT - 12;

type RGB = readonly [number, number, number] | [number, number, number];

// Palette (RGB)
const COLOR_PRIMARY: RGB = [15, 23, 42];        // Slate 900
const COLOR_SECONDARY: RGB = [30, 41, 59];      // Slate 800
const COLOR_ACCENT_BLUE: RGB = [37, 99, 235];   // Blue 600
const COLOR_BG_ACCENT: RGB = [239, 246, 255];   // Blue 50
const COLOR_CARD_BG: RGB = [248, 250, 252];     // Slate 50
const COLOR_BORDER: RGB = [226, 232, 240];      // Slate 200
const COLOR_BORDER_DARK: RGB = [203, 213, 225]; // Slate 300
const COLOR_TEXT_MAIN: RGB = [30, 41, 59];      // Slate 800
const COLOR_TEXT_MUTED: RGB = [100, 116, 139];  // Slate 500
const COLOR_SUCCESS: RGB = [22, 163, 74];       // Green 600
const COLOR_SUCCESS_BG: RGB = [240, 253, 244];  // Green 50
const COLOR_MUTED_BG: RGB = [241, 245, 249];    // Slate 100
const COLOR_DANGER: RGB = [220, 38, 38];        // Red 600
const COLOR_DANGER_BG: RGB = [254, 242, 242];   // Red 50

const setFill = (doc: jsPDF, c: RGB) => doc.setFillColor(c[0], c[1], c[2]);
const setDraw = (doc: jsPDF, c: RGB) => doc.setDrawColor(c[0], c[1], c[2]);
const setText = (doc: jsPDF, c: RGB) => doc.setTextColor(c[0], c[1], c[2]);

/**
 * Renders the top brand header on a page.
 */
function renderDocumentHeader(
  doc: jsPDF,
  category: string,
  title: string,
  metadataRight?: string
): number {
  let y = MARGIN_TOP;

  // Category Pill Badge
  setFill(doc, COLOR_BG_ACCENT);
  setDraw(doc, COLOR_ACCENT_BLUE);
  doc.roundedRect(MARGIN_X, y, 54, 6.5, 1.5, 1.5, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(7.5);
  setText(doc, COLOR_ACCENT_BLUE);
  doc.text(category.toUpperCase(), MARGIN_X + 27, y + 4.5, { align: "center" });

  // Optional Metadata on the right (e.g. date)
  if (metadataRight) {
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8.5);
    setText(doc, COLOR_TEXT_MUTED);
    doc.text(metadataRight, PAGE_WIDTH - MARGIN_X, y + 4.5, { align: "right" });
  }

  y += 11;

  // Document Title
  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  setText(doc, COLOR_PRIMARY);
  const titleLines = doc.splitTextToSize(title, CONTENT_WIDTH);
  doc.text(titleLines, MARGIN_X, y);
  y += titleLines.length * 6.5 + 2;

  // Divider line
  setDraw(doc, COLOR_BORDER);
  doc.setLineWidth(0.35);
  doc.line(MARGIN_X, y, PAGE_WIDTH - MARGIN_X, y);
  y += 7;

  return y;
}

/**
 * Stamps running footers ("Page X of Y") across all pages.
 */
function stampFooters(doc: jsPDF, docType: string) {
  const totalPages = doc.getNumberOfPages();
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i);

    // Subtle footer separator
    setDraw(doc, COLOR_BORDER);
    doc.setLineWidth(0.25);
    doc.line(MARGIN_X, FOOTER_Y - 4, PAGE_WIDTH - MARGIN_X, FOOTER_Y - 4);

    // Footer text
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8);
    setText(doc, COLOR_TEXT_MUTED);
    doc.text(
      `AxiomAI Study Studio • ${docType}`,
      MARGIN_X,
      FOOTER_Y
    );
    doc.text(
      `Page ${i} of ${totalPages}`,
      PAGE_WIDTH - MARGIN_X,
      FOOTER_Y,
      { align: "right" }
    );
  }
}

// ===========================================================================
// 1. ROADMAP PDF EXPORT
// ===========================================================================
export function downloadRoadmapPDF(roadmap: Roadmap, notebookName?: string) {
  const doc = new jsPDF({ orientation: "portrait", unit: "mm", format: "a4" });
  const dateStr = new Date().toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  const totalStages = roadmap.stages?.length || 0;
  const completedStages = roadmap.stages?.filter((s) => s.completed).length || 0;
  const totalMinutes = roadmap.stages?.reduce((acc, s) => acc + (s.estimatedMinutes || 0), 0) || 0;

  let currentY = renderDocumentHeader(
    doc,
    "Learning Roadmap",
    roadmap.title || "Curriculum Roadmap",
    `Exported: ${dateStr}`
  );

  // Summary Stat Strip
  setFill(doc, COLOR_CARD_BG);
  setDraw(doc, COLOR_BORDER);
  doc.roundedRect(MARGIN_X, currentY, CONTENT_WIDTH, 14, 2, 2, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(9);
  setText(doc, COLOR_PRIMARY);
  doc.text(`Notebook: ${notebookName || "General Workspace"}`, MARGIN_X + 5, currentY + 6);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(8.5);
  setText(doc, COLOR_TEXT_MUTED);
  doc.text(
    `Total Stages: ${totalStages}   •   Completed: ${completedStages}   •   Est. Total Duration: ~${totalMinutes} mins`,
    MARGIN_X + 5,
    currentY + 10.5
  );

  currentY += 20;

  // Render Each Stage
  if (roadmap.stages && roadmap.stages.length > 0) {
    roadmap.stages.forEach((stage, idx) => {
      // Calculate height needed for this stage
      const stageTitle = `Stage ${idx + 1}: ${stage.title}`;
      const descLines = stage.description
        ? doc.splitTextToSize(stage.description, CONTENT_WIDTH - 12)
        : [];
      
      let outcomesHeight = 0;
      if (stage.outcomes && stage.outcomes.length > 0) {
        outcomesHeight += 7; // Header "Target Outcomes"
        stage.outcomes.forEach((o) => {
          const oLines = doc.splitTextToSize(`• ${o}`, CONTENT_WIDTH - 16);
          outcomesHeight += oLines.length * 4.5;
        });
      }

      const cardHeight =
        14 + // header & badge
        descLines.length * 4.5 +
        outcomesHeight +
        6; // padding

      // Check if page break is needed
      if (currentY + cardHeight > PAGE_HEIGHT - MARGIN_BOTTOM) {
        doc.addPage();
        currentY = renderDocumentHeader(
          doc,
          "Learning Roadmap",
          roadmap.title || "Curriculum Roadmap",
          `Page ${doc.getNumberOfPages()}`
        );
      }

      // Stage Card Box
      setFill(doc, COLOR_CARD_BG);
      setDraw(doc, COLOR_BORDER);
      doc.roundedRect(MARGIN_X, currentY, CONTENT_WIDTH, cardHeight, 2, 2, "FD");

      // Left Accent Indicator
      setFill(doc, stage.completed ? COLOR_SUCCESS : COLOR_ACCENT_BLUE);
      doc.rect(MARGIN_X, currentY, 2.5, cardHeight, "F");

      // Stage Header row
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10.5);
      setText(doc, COLOR_PRIMARY);
      doc.text(stageTitle, MARGIN_X + 6, currentY + 6.5);

      // Duration & Status Pill on right
      const statusPill = stage.completed ? "COMPLETED" : `${stage.estimatedMinutes || 30} MINS`;
      doc.setFont("helvetica", "bold");
      doc.setFontSize(7.5);
      setFill(doc, stage.completed ? COLOR_SUCCESS_BG : COLOR_BG_ACCENT);
      setDraw(doc, stage.completed ? COLOR_SUCCESS : COLOR_ACCENT_BLUE);
      doc.roundedRect(PAGE_WIDTH - MARGIN_X - 28, currentY + 2.5, 24, 5.5, 1, 1, "FD");
      setText(doc, stage.completed ? COLOR_SUCCESS : COLOR_ACCENT_BLUE);
      doc.text(statusPill, PAGE_WIDTH - MARGIN_X - 16, currentY + 6.2, { align: "center" });

      let cardInnerY = currentY + 12;

      // Description
      if (descLines.length > 0) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9);
        setText(doc, COLOR_TEXT_MAIN);
        doc.text(descLines, MARGIN_X + 6, cardInnerY);
        cardInnerY += descLines.length * 4.5 + 2;
      }

      // Outcomes
      if (stage.outcomes && stage.outcomes.length > 0) {
        doc.setFont("helvetica", "bold");
        doc.setFontSize(8.5);
        setText(doc, COLOR_SECONDARY);
        doc.text("Key Learning Outcomes:", MARGIN_X + 6, cardInnerY);
        cardInnerY += 4.5;

        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.5);
        setText(doc, COLOR_TEXT_MUTED);

        stage.outcomes.forEach((outcome) => {
          const outcomeLines = doc.splitTextToSize(`•  ${outcome}`, CONTENT_WIDTH - 14);
          doc.text(outcomeLines, MARGIN_X + 8, cardInnerY);
          cardInnerY += outcomeLines.length * 4.5;
        });
      }

      currentY += cardHeight + 6;
    });
  }

  stampFooters(doc, "Learning Roadmap");
  const filename = `${(roadmap.title || "Roadmap").replace(/[^a-zA-Z0-9_-]/g, "_")}_AxiomAI.pdf`;
  doc.save(filename);
}

// ===========================================================================
// 2. FLASHCARDS PDF EXPORT
// ===========================================================================
export function downloadFlashcardsPDF(deck: FlashcardDeck, notebookName?: string) {
  const doc = new jsPDF({ orientation: "portrait", unit: "mm", format: "a4" });
  const dateStr = new Date().toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  const totalCards = deck.cards?.length || 0;

  let currentY = renderDocumentHeader(
    doc,
    "Flashcard Deck",
    deck.title || "Study Flashcards",
    `Exported: ${dateStr}`
  );

  // Deck Summary Strip
  setFill(doc, COLOR_CARD_BG);
  setDraw(doc, COLOR_BORDER);
  doc.roundedRect(MARGIN_X, currentY, CONTENT_WIDTH, 14, 2, 2, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(9);
  setText(doc, COLOR_PRIMARY);
  doc.text(`Notebook: ${notebookName || "General Workspace"}`, MARGIN_X + 5, currentY + 6);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(8.5);
  setText(doc, COLOR_TEXT_MUTED);
  doc.text(
    `Total Cards: ${totalCards}   •   Format: Active Recall (Question & Answer Pairs)`,
    MARGIN_X + 5,
    currentY + 10.5
  );

  currentY += 20;

  // Render Each Flashcard
  if (deck.cards && deck.cards.length > 0) {
    deck.cards.forEach((card, idx) => {
      const qLines = doc.splitTextToSize(card.question, CONTENT_WIDTH - 14);
      const aLines = doc.splitTextToSize(card.answer, CONTENT_WIDTH - 14);

      // Card height calculation
      const cardHeight =
        8 + // Card number badge header
        qLines.length * 4.5 +
        6 + // Divider spacing
        aLines.length * 4.5 +
        8; // Bottom padding

      // Check if page break is needed
      if (currentY + cardHeight > PAGE_HEIGHT - MARGIN_BOTTOM) {
        doc.addPage();
        currentY = renderDocumentHeader(
          doc,
          "Flashcard Deck",
          deck.title || "Study Flashcards",
          `Page ${doc.getNumberOfPages()}`
        );
      }

      // Outer Card Box
      setFill(doc, COLOR_CARD_BG);
      setDraw(doc, COLOR_BORDER);
      doc.roundedRect(MARGIN_X, currentY, CONTENT_WIDTH, cardHeight, 2, 2, "FD");

      // Left Accent Strip
      setFill(doc, COLOR_ACCENT_BLUE);
      doc.rect(MARGIN_X, currentY, 2.5, cardHeight, "F");

      // Card Number Tag
      doc.setFont("helvetica", "bold");
      doc.setFontSize(7.5);
      setText(doc, COLOR_ACCENT_BLUE);
      doc.text(`CARD ${idx + 1} OF ${totalCards}`, MARGIN_X + 6, currentY + 6.5);

      let innerY = currentY + 11.5;

      // Question Section
      doc.setFont("helvetica", "bold");
      doc.setFontSize(9.5);
      setText(doc, COLOR_PRIMARY);
      doc.text(qLines, MARGIN_X + 6, innerY);
      innerY += qLines.length * 4.5 + 2;

      // Subtle Divider inside card
      setDraw(doc, COLOR_BORDER);
      doc.setLineWidth(0.2);
      doc.line(MARGIN_X + 6, innerY, PAGE_WIDTH - MARGIN_X - 6, innerY);
      innerY += 4.5;

      // Answer Header
      doc.setFont("helvetica", "bold");
      doc.setFontSize(7.5);
      setText(doc, COLOR_SUCCESS);
      doc.text("ANSWER:", MARGIN_X + 6, innerY);
      innerY += 4;

      // Answer Text
      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      setText(doc, COLOR_TEXT_MAIN);
      doc.text(aLines, MARGIN_X + 6, innerY);

      currentY += cardHeight + 6;
    });
  }

  stampFooters(doc, "Flashcard Study Deck");
  const filename = `${(deck.title || "Flashcards").replace(/[^a-zA-Z0-9_-]/g, "_")}_AxiomAI.pdf`;
  doc.save(filename);
}

// ===========================================================================
// 3. QUIZ PDF EXPORT
// ===========================================================================
export function downloadQuizPDF(
  quiz: Quiz,
  notebookName?: string,
  userAnswers?: Record<string, { selectedOptionId: string; correct: boolean }>
) {
  const doc = new jsPDF({ orientation: "portrait", unit: "mm", format: "a4" });
  const dateStr = new Date().toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  const totalQuestions = quiz.questions?.length || 0;
  
  // Calculate score if answers provided
  let correctCount = 0;
  let hasAnswers = false;
  if (userAnswers && Object.keys(userAnswers).length > 0) {
    hasAnswers = true;
    Object.values(userAnswers).forEach((a) => {
      if (a.correct) correctCount++;
    });
  }

  let currentY = renderDocumentHeader(
    doc,
    "Diagnostic Assessment",
    quiz.title || "Diagnostic Quiz & Review",
    `Exported: ${dateStr}`
  );

  // Summary Stat Strip
  setFill(doc, COLOR_CARD_BG);
  setDraw(doc, COLOR_BORDER);
  doc.roundedRect(MARGIN_X, currentY, CONTENT_WIDTH, 14, 2, 2, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(9);
  setText(doc, COLOR_PRIMARY);
  doc.text(`Notebook: ${notebookName || "General Workspace"}`, MARGIN_X + 5, currentY + 6);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(8.5);
  setText(doc, COLOR_TEXT_MUTED);

  const scoreText = hasAnswers
    ? `Score: ${correctCount} / ${totalQuestions} (${Math.round((correctCount / (totalQuestions || 1)) * 100)}%)   •   Format: Multiple Choice with Explanations`
    : `Total Questions: ${totalQuestions}   •   Format: Multiple Choice with Complete Rationale Key`;
  
  doc.text(scoreText, MARGIN_X + 5, currentY + 10.5);

  currentY += 20;

  // Render Each Question
  if (quiz.questions && quiz.questions.length > 0) {
    quiz.questions.forEach((q, idx) => {
      const qHeader = `Question ${idx + 1} of ${totalQuestions}`;
      const promptLines = doc.splitTextToSize(q.prompt, CONTENT_WIDTH - 14);

      // Estimate options height
      let optionsHeight = 0;
      const optionDetails: { label: string; lines: string[]; isCorrect: boolean; isUserChoice: boolean }[] = [];

      const userAns = userAnswers ? userAnswers[q.id] : null;

      q.options.forEach((opt, optIdx) => {
        const letter = String.fromCharCode(65 + optIdx); // A, B, C, D
        const optText = `${letter}.  ${opt.label}`;
        const optLines = doc.splitTextToSize(optText, CONTENT_WIDTH - 20);
        const isCorrect = opt.id === q.correctOptionId;
        const isUserChoice = userAns?.selectedOptionId === opt.id;
        optionDetails.push({ label: optText, lines: optLines, isCorrect, isUserChoice });
        optionsHeight += optLines.length * 4.5 + 3.5;
      });

      // Explanation height
      const correctOpt = q.options.find((o) => o.id === q.correctOptionId);
      const explanationText = correctOpt?.rationale || "Verified academic rationale from study source.";
      const expLines = doc.splitTextToSize(explanationText, CONTENT_WIDTH - 18);
      const expHeight = 6 + expLines.length * 4.2 + 4;

      const totalCardHeight =
        8 + // Header
        promptLines.length * 4.8 +
        5 + // Gap
        optionsHeight +
        expHeight +
        8; // Padding

      // Check if page break needed
      if (currentY + totalCardHeight > PAGE_HEIGHT - MARGIN_BOTTOM) {
        doc.addPage();
        currentY = renderDocumentHeader(
          doc,
          "Diagnostic Assessment",
          quiz.title || "Diagnostic Quiz & Review",
          `Page ${doc.getNumberOfPages()}`
        );
      }

      // Outer Card Box
      setFill(doc, COLOR_CARD_BG);
      setDraw(doc, COLOR_BORDER);
      doc.roundedRect(MARGIN_X, currentY, CONTENT_WIDTH, totalCardHeight, 2, 2, "FD");

      // Left Accent Strip (green if answered correct, red if wrong, blue if unattempted)
      const accentColor: RGB = userAns ? (userAns.correct ? COLOR_SUCCESS : COLOR_DANGER) : COLOR_ACCENT_BLUE;
      setFill(doc, accentColor);
      doc.rect(MARGIN_X, currentY, 2.5, totalCardHeight, "F");

      // Question Number Header
      doc.setFont("helvetica", "bold");
      doc.setFontSize(8);
      setText(doc, COLOR_ACCENT_BLUE);
      doc.text(qHeader.toUpperCase(), MARGIN_X + 6, currentY + 6.5);

      let innerY = currentY + 11.5;

      // Question Prompt
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      setText(doc, COLOR_PRIMARY);
      doc.text(promptLines, MARGIN_X + 6, innerY);
      innerY += promptLines.length * 4.8 + 4;

      // Render Options
      optionDetails.forEach((opt) => {
        const rowHeight = opt.lines.length * 4.5 + 2.5;

        // Background for correct answer or selected option
        if (opt.isCorrect) {
          setFill(doc, COLOR_SUCCESS_BG);
          setDraw(doc, COLOR_SUCCESS);
          doc.roundedRect(MARGIN_X + 6, innerY - 3, CONTENT_WIDTH - 12, rowHeight, 1, 1, "FD");
        } else if (opt.isUserChoice && !opt.isCorrect) {
          setFill(doc, COLOR_DANGER_BG);
          setDraw(doc, COLOR_DANGER);
          doc.roundedRect(MARGIN_X + 6, innerY - 3, CONTENT_WIDTH - 12, rowHeight, 1, 1, "FD");
        }

        // Option Text
        doc.setFont("helvetica", opt.isCorrect ? "bold" : "normal");
        doc.setFontSize(8.5);
        if (opt.isCorrect) {
          setText(doc, COLOR_SUCCESS);
        } else if (opt.isUserChoice && !opt.isCorrect) {
          setText(doc, COLOR_DANGER);
        } else {
          setText(doc, COLOR_TEXT_MAIN);
        }

        doc.text(opt.lines, MARGIN_X + 9, innerY + 0.5);

        // Badge indicator on right for correct answer
        if (opt.isCorrect) {
          doc.setFont("helvetica", "bold");
          doc.setFontSize(7);
          doc.text("[CORRECT ANSWER]", PAGE_WIDTH - MARGIN_X - 10, innerY + 0.5, { align: "right" });
        } else if (opt.isUserChoice) {
          doc.setFont("helvetica", "bold");
          doc.setFontSize(7);
          doc.text("[YOUR SELECTION]", PAGE_WIDTH - MARGIN_X - 10, innerY + 0.5, { align: "right" });
        }

        innerY += rowHeight + 1.5;
      });

      innerY += 2;

      // Explanation Box
      setFill(doc, COLOR_MUTED_BG);
      setDraw(doc, COLOR_BORDER_DARK);
      doc.roundedRect(MARGIN_X + 6, innerY, CONTENT_WIDTH - 12, expHeight - 2, 1.5, 1.5, "FD");

      doc.setFont("helvetica", "bold");
      doc.setFontSize(7.5);
      setText(doc, COLOR_SECONDARY);
      doc.text("EXPLANATION & DISTRACTOR RATIONALE:", MARGIN_X + 9, innerY + 4.5);

      doc.setFont("helvetica", "normal");
      doc.setFontSize(8);
      setText(doc, COLOR_TEXT_MAIN);
      doc.text(expLines, MARGIN_X + 9, innerY + 8.5);

      currentY += totalCardHeight + 6;
    });
  }

  stampFooters(doc, "Diagnostic Quiz & Assessment");
  const filename = `${(quiz.title || "Quiz").replace(/[^a-zA-Z0-9_-]/g, "_")}_AxiomAI.pdf`;
  doc.save(filename);
}

// ---------------------------------------------------------------------------
// 4. Mind Map & Concept Hierarchy PDF Exporter
// ---------------------------------------------------------------------------

const BRANCH_COLORS: RGB[] = [
  [79, 70, 229],   // Indigo
  [16, 185, 129],  // Emerald
  [217, 119, 6],   // Amber
  [147, 51, 234],  // Purple
  [225, 29, 72],   // Rose
  [8, 145, 178],   // Cyan
];

export function downloadMindMapPDF(
  mindMap: MindMap,
  notebookName?: string
): void {
  const doc = new jsPDF({
    unit: "mm",
    format: "a4",
    orientation: "portrait",
  });

  const root = mindMap.root;
  if (!root) return;

  const countNodes = (n: typeof root): number => {
    let count = 1;
    for (const child of n.children || []) {
      count += countNodes(child);
    }
    return count;
  };

  const totalNodes = countNodes(root);
  const topBranches = root.children || [];

  let currentY = renderDocumentHeader(
    doc,
    "KNOWLEDGE HIERARCHY & MIND MAP",
    notebookName || mindMap.title || "Conceptual Mind Map",
    `${topBranches.length} Major Themes | ${totalNodes} Concepts`
  );

  // Central Root Concept Card
  setFill(doc, COLOR_PRIMARY);
  setDraw(doc, COLOR_ACCENT_BLUE);
  doc.roundedRect(MARGIN_X, currentY, CONTENT_WIDTH, 22, 2.5, 2.5, "FD");

  // Accent indicator line inside root card
  setFill(doc, COLOR_ACCENT_BLUE);
  doc.rect(MARGIN_X + 2, currentY + 3, 2, 16, "F");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(8);
  setText(doc, [147, 197, 253]); // Light blue
  doc.text("CENTRAL KNOWLEDGE CORE", MARGIN_X + 8, currentY + 7);

  doc.setFont("helvetica", "bold");
  doc.setFontSize(13);
  setText(doc, [255, 255, 255]);
  const rootLabelLines = doc.splitTextToSize(root.label || "Core Topic", CONTENT_WIDTH - 20);
  doc.text(rootLabelLines[0] || root.label, MARGIN_X + 8, currentY + 14);

  if (root.summary) {
    doc.setFont("helvetica", "normal");
    doc.setFontSize(7.5);
    setText(doc, [203, 213, 225]);
    const rootSummary = doc.splitTextToSize(root.summary, CONTENT_WIDTH - 20);
    doc.text(rootSummary[0] || "", MARGIN_X + 8, currentY + 19);
  }

  currentY += 28;

  // Render each Level 1 Branch
  topBranches.forEach((branch, bIdx) => {
    const branchColor = BRANCH_COLORS[bIdx % BRANCH_COLORS.length];

    // Check space for branch header
    if (currentY + 25 > PAGE_HEIGHT - MARGIN_BOTTOM) {
      doc.addPage();
      currentY = MARGIN_TOP;
    }

    // Branch Header Banner
    setFill(doc, COLOR_CARD_BG);
    setDraw(doc, branchColor);
    doc.roundedRect(MARGIN_X, currentY, CONTENT_WIDTH, 14, 2, 2, "FD");

    // Left accent pill
    setFill(doc, branchColor);
    doc.rect(MARGIN_X, currentY, 4, 14, "F");

    // Branch tag
    doc.setFont("helvetica", "bold");
    doc.setFontSize(7.5);
    setText(doc, branchColor);
    doc.text(`THEME ${bIdx + 1} (${(branch.children || []).length} SUBTOPICS)`, MARGIN_X + 8, currentY + 5.5);

    // Branch label
    doc.setFont("helvetica", "bold");
    doc.setFontSize(10.5);
    setText(doc, COLOR_PRIMARY);
    doc.text(branch.label, MARGIN_X + 8, currentY + 11);

    currentY += 17;

    // Optional branch summary
    if (branch.summary) {
      doc.setFont("helvetica", "italic");
      doc.setFontSize(8);
      setText(doc, COLOR_TEXT_MUTED);
      const bSummLines = doc.splitTextToSize(branch.summary, CONTENT_WIDTH - 12);
      doc.text(bSummLines, MARGIN_X + 6, currentY);
      currentY += bSummLines.length * 3.8 + 3;
    }

    // Level 2 Children (Subtopics)
    (branch.children || []).forEach((subtopic, sIdx) => {
      const subChildren = subtopic.children || [];
      const subSummLines = subtopic.summary
        ? doc.splitTextToSize(subtopic.summary, CONTENT_WIDTH - 28)
        : [];
      
      const leafLinesCount = subChildren.reduce((acc, leaf) => {
        const leafDesc = leaf.summary ? doc.splitTextToSize(leaf.summary, CONTENT_WIDTH - 38) : [];
        return acc + 1 + leafDesc.length;
      }, 0);

      const estimatedHeight = 12 + subSummLines.length * 3.6 + (subChildren.length > 0 ? 8 + leafLinesCount * 3.6 : 0);

      if (currentY + estimatedHeight > PAGE_HEIGHT - MARGIN_BOTTOM) {
        doc.addPage();
        currentY = MARGIN_TOP;
      }

      // Subtopic Card
      setFill(doc, [255, 255, 255]);
      setDraw(doc, COLOR_BORDER);
      doc.roundedRect(MARGIN_X + 6, currentY, CONTENT_WIDTH - 6, estimatedHeight, 1.5, 1.5, "FD");

      // Left branch indicator line
      setFill(doc, branchColor);
      doc.rect(MARGIN_X + 6, currentY, 2, estimatedHeight, "F");

      // Subtopic title
      doc.setFont("helvetica", "bold");
      doc.setFontSize(9);
      setText(doc, COLOR_SECONDARY);
      doc.text(`${bIdx + 1}.${sIdx + 1}  ${subtopic.label}`, MARGIN_X + 12, currentY + 6);

      let innerY = currentY + 10;

      // Subtopic summary
      if (subSummLines.length > 0) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8);
        setText(doc, COLOR_TEXT_MAIN);
        doc.text(subSummLines, MARGIN_X + 12, innerY);
        innerY += subSummLines.length * 3.6 + 2;
      }

      // Level 3 Children (Leaves / Detailed Concepts)
      if (subChildren.length > 0) {
        subChildren.forEach((leaf, lIdx) => {
          doc.setFont("helvetica", "bold");
          doc.setFontSize(7.5);
          setText(doc, branchColor);
          doc.text(`*`, MARGIN_X + 14, innerY);

          doc.setFont("helvetica", "bold");
          doc.setFontSize(8);
          setText(doc, COLOR_PRIMARY);
          doc.text(leaf.label, MARGIN_X + 18, innerY);
          innerY += 3.8;

          if (leaf.summary) {
            doc.setFont("helvetica", "normal");
            doc.setFontSize(7.5);
            setText(doc, COLOR_TEXT_MUTED);
            const leafSumm = doc.splitTextToSize(leaf.summary, CONTENT_WIDTH - 36);
            doc.text(leafSumm, MARGIN_X + 18, innerY);
            innerY += leafSumm.length * 3.4 + 1.5;
          }
        });
      }

      currentY += estimatedHeight + 4;
    });

    currentY += 4;
  });

  stampFooters(doc, "Knowledge Mind Map & Conceptual Hierarchy");
  const filename = `${(mindMap.title || "MindMap").replace(/[^a-zA-Z0-9_-]/g, "_")}_AxiomAI.pdf`;
  doc.save(filename);
}
