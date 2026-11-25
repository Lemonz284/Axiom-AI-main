import { db } from "./db";
import { generateJSON, generateText } from "./llm";
import crypto from "crypto";

export interface QuizOption {
  id: string;
  label: string;
  rationale: string;
}

export interface QuizQuestion {
  id: string;
  prompt: string;
  options: QuizOption[];
  correctOptionId: string;
}

export interface QuizResult {
  id: string;
  notebookId: string;
  sourceIds: string[];
  title: string;
  questions: QuizQuestion[];
  createdAt: string;
}

export async function generateQuiz(
  notebookId: string,
  sourceIds: string[],
  questionCount: number = 10,
  regenerate: boolean = false
): Promise<QuizResult> {
  const sortedSourceIds = [...sourceIds].sort();
  const sourceIdsJson = JSON.stringify(sortedSourceIds);

  if (!regenerate) {
    const existing = await db.quiz.findFirst({
      where: {
        notebookId,
        sourceIds: sourceIdsJson,
      },
      orderBy: { createdAt: "desc" },
    });

    if (existing) {
      const parsedQuestions: QuizQuestion[] = JSON.parse(existing.questions || "[]");
      // Check if questions are valid and not the old truncated fallback with "Based on the text: ... ..."
      const isTruncatedFallback = parsedQuestions.some(
        (q) => q.prompt.startsWith("Based on the text: ") && q.prompt.endsWith("...")
      );
      if (parsedQuestions.length >= 5 && !isTruncatedFallback) {
        return {
          id: existing.id,
          notebookId: existing.notebookId,
          sourceIds: JSON.parse(existing.sourceIds),
          title: existing.title,
          questions: parsedQuestions,
          createdAt: existing.createdAt.toISOString(),
        };
      }
    }
  }

  const chunks = await db.chunk.findMany({
    where: {
      sourceId: { in: sortedSourceIds },
      notebookId,
    },
    orderBy: { chunkIndex: "asc" },
  });

  if (chunks.length === 0) {
    throw new Error("No indexed content found for the selected sources. Please wait for indexing to complete.");
  }

  let sourceText = chunks.map((c) => c.text).join("\n\n");
  if (sourceText.length > 18000) {
    sourceText = sourceText.slice(0, 18000) + "... (truncated)";
  }

  const effectiveCount = Math.max(5, Math.min(questionCount, 25));

  const prompt = `
Generate a comprehensive ${effectiveCount}-question multiple-choice diagnostic quiz from the following source material.

SOURCE TEXT:
"""
${sourceText}
"""

Rules:
- Generate EXACTLY ${effectiveCount} distinct multiple-choice questions testing key concepts, definitions, mechanisms, and findings in the text.
- Every question prompt MUST be a full, complete, and articulate question or statement. NEVER truncate questions or append trailing ellipses "...".
- Each question must have exactly 4 options with full sentences/phrases, only one correct.
- Distractors must be plausible (based on real details/numbers/near-misses from the source), not obviously wrong.
- For EVERY option (correct and incorrect), write an informative rationale explaining why it is right or wrong, grounded in the source text.
- Vary question types across all core chapters: architecture, algorithms, CRAG verification, vector search, active learning tools, and results.

Return ONLY JSON matching schema:
{
  "questions": [
    {
      "prompt": "string",
      "options": [
        { "label": "string", "rationale": "string", "isCorrect": boolean }
      ]
    }
  ]
}
`;

  let questions: QuizQuestion[] = [];
  const maxAttempts = 2;

  for (let attempts = 1; attempts <= maxAttempts; attempts++) {
    try {
      const parsed = await generateJSON<{ questions: any[] }>(
        prompt,
        "You are a precise study material generator. Always return valid JSON matching schema.",
        "gpt-4o-mini"
      );

      if (!parsed.questions || !Array.isArray(parsed.questions)) {
        throw new Error("Response missing 'questions' array");
      }

      questions = [];
      for (const q of parsed.questions) {
        if (!q.prompt || !Array.isArray(q.options) || q.options.length !== 4) continue;
        
        const rawOptions = q.options.map((opt: any) => ({
          label: String(opt.label).trim(),
          rationale: String(opt.rationale).trim(),
          isCorrect: !!opt.isCorrect,
        }));

        // Shuffle options server-side
        for (let i = rawOptions.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [rawOptions[i], rawOptions[j]] = [rawOptions[j], rawOptions[i]];
        }

        const optionLetters = ['A', 'B', 'C', 'D'];
        let correctOptionId = 'A';

        const finalOptions: QuizOption[] = rawOptions.map((opt: { label: string; rationale: string; isCorrect: boolean }, idx: number) => {
          const letter = optionLetters[idx] || 'A';
          if (opt.isCorrect) {
            correctOptionId = letter;
          }
          return {
            id: letter,
            label: opt.label,
            rationale: opt.rationale,
          };
        });

        questions.push({
          id: crypto.randomUUID(),
          prompt: String(q.prompt).trim(),
          options: finalOptions,
          correctOptionId,
        });
      }

      if (questions.length >= Math.ceil(effectiveCount * 0.5)) {
        break;
      }
    } catch (err) {
      console.warn(`Quiz generation attempt ${attempts} failed:`, (err as Error).message);
      if (attempts >= maxAttempts) {
        if (questions.length > 0) {
          break; // Use whatever we got
        }
        questions = generateFallbackQuiz(sourceText, effectiveCount);
        break;
      }
    }
  }

  if (regenerate) {
    await db.quiz.deleteMany({
      where: { notebookId, sourceIds: sourceIdsJson },
    });
  }

  const savedQuiz = await db.quiz.create({
    data: {
      notebookId,
      sourceIds: sourceIdsJson,
      title: `${questions.length}-Question Quiz`,
      questions: JSON.stringify(questions),
    },
  });

  return {
    id: savedQuiz.id,
    notebookId: savedQuiz.notebookId,
    sourceIds: sortedSourceIds,
    title: savedQuiz.title,
    questions: questions,
    createdAt: savedQuiz.createdAt.toISOString(),
  };
}

export async function getQuizzes(notebookId: string): Promise<QuizResult[]> {
  const records = await db.quiz.findMany({
    where: { notebookId },
    orderBy: { createdAt: "desc" },
  });
  return records.map(record => ({
    id: record.id,
    notebookId: record.notebookId,
    sourceIds: JSON.parse(record.sourceIds),
    title: record.title,
    questions: JSON.parse(record.questions),
    createdAt: record.createdAt.toISOString(),
  }));
}

export async function deleteQuiz(quizId: string, notebookId: string): Promise<void> {
  await db.quiz.deleteMany({
    where: { id: quizId, notebookId },
  });
}

function generateFallbackQuiz(text: string, count: number): QuizQuestion[] {
  const sentences = text
    .split(/(?<=[.!?])\s+/)
    .map((s) => s.trim())
    .filter((s) => s.length > 50 && s.length < 250);

  const questions: QuizQuestion[] = [];
  const targetCount = Math.max(8, count);
  const step = Math.max(1, Math.floor(sentences.length / targetCount));

  for (let i = 0; i < sentences.length && questions.length < targetCount; i += step) {
    const sentence = sentences[i];
    if (!sentence) continue;
    
    questions.push({
      id: crypto.randomUUID(),
      prompt: `Which of the following statements accurately reflects the source documentation regarding: "${sentence.slice(0, 80)}"?`,
      correctOptionId: 'A',
      options: [
        { id: 'A', label: sentence, rationale: "This statement directly reflects the verified findings documented in the source text." },
        { id: 'B', label: "The system bypasses verification and assumes all output is automatically grounded.", rationale: "Incorrect. The architecture strictly enforces verification and citation bounds." },
        { id: 'C', label: "This architectural component operates entirely offline without data persistence.", rationale: "Incorrect. Persistent vector and relational stores maintain system state." },
        { id: 'D', label: "The findings were invalidated during benchmark testing.", rationale: "Incorrect. Empirical benchmarks confirm system validity." }
      ]
    });
  }

  if (questions.length === 0) {
    questions.push({
      id: crypto.randomUUID(),
      prompt: "What is the primary architecture and objective of the AxiomAI system?",
      correctOptionId: 'A',
      options: [
        { id: 'A', label: "A multimodal AI workspace featuring grounded RAG, CRAG verification, and active learning tools.", rationale: "Accurately summarizes the core platform specification." },
        { id: 'B', label: "A single-tier legacy keyword search database.", rationale: "Incorrect. AxiomAI uses a modern 4-tier topology." },
        { id: 'C', label: "An ungrounded text generation script without citation checks.", rationale: "Incorrect. Citation checks and CRAG auditing are foundational." },
        { id: 'D', label: "None of the above.", rationale: "Incorrect." }
      ]
    });
  }

  return questions;
}
