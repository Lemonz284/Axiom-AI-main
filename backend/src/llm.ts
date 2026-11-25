import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";
import OpenAI from "openai";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Ensure .env is always loaded whether run from root, backend, or subdirs
dotenv.config();
dotenv.config({ path: path.resolve(__dirname, "../.env") });

// ---------------------------------------------------------------------------
// Configuration & Multi-Provider Clients
// ---------------------------------------------------------------------------

// 1. Primary: OpenAI
const OPENAI_API_KEY = process.env.OPENAI_API_KEY?.trim();
const OPENAI_MODEL = process.env.OPENAI_MODEL?.trim() || "gpt-4o-mini";
const OPENAI_BASE_URL = process.env.OPENAI_BASE_URL?.trim();

let openaiClient: OpenAI | null = null;
if (OPENAI_API_KEY && !OPENAI_API_KEY.includes("your-api-key")) {
  openaiClient = new OpenAI({
    apiKey: OPENAI_API_KEY,
    ...(OPENAI_BASE_URL ? { baseURL: OPENAI_BASE_URL } : {}),
    timeout: 30000,
  });
}

// 2. Fallback / Alternative: Groq
const GROQ_API_KEY = process.env.GROQ_API_KEY?.trim();
const GROQ_MODEL = process.env.GROQ_MODEL?.trim() || process.env.LLM_MODEL?.trim() || "openai/gpt-oss-120b";
const GROQ_BASE_URL = process.env.GROQ_BASE_URL?.trim() || "https://api.groq.com/openai/v1";

let groqClient: OpenAI | null = null;
if (GROQ_API_KEY && !GROQ_API_KEY.includes("your-api-key")) {
  groqClient = new OpenAI({
    apiKey: GROQ_API_KEY,
    baseURL: GROQ_BASE_URL,
    timeout: 30000,
  });
}

// 3. AICredits (Optional Third Provider)
const AICREDITS_API_KEY = process.env.AICREDITS_API_KEY?.trim();
const AICREDITS_BASE_URL = process.env.AICREDITS_BASE_URL?.trim() || "https://api.aicredits.in/v1";

let aicreditsClient: OpenAI | null = null;
if (AICREDITS_API_KEY && !AICREDITS_API_KEY.includes("your-api-key")) {
  aicreditsClient = new OpenAI({
    apiKey: AICREDITS_API_KEY,
    baseURL: AICREDITS_BASE_URL,
    timeout: 30000,
  });
}

// Log status on startup
if (openaiClient) {
  console.log(`[LLM Service] Primary provider initialized: OpenAI (${OPENAI_MODEL})`);
}
if (groqClient) {
  console.log(`[LLM Service] Fallback/Active provider initialized: Groq (${GROQ_MODEL})`);
}
if (!openaiClient && !groqClient && !aicreditsClient) {
  console.warn(`[LLM Service] No external LLM keys detected. Running in offline fallback mode.`);
}

// ---------------------------------------------------------------------------
// Embeddings (1536-Dimensional Vectors)
// ---------------------------------------------------------------------------
function createDeterministicEmbedding(text: string, dim: number = 1536): number[] {
  const vec = new Array(dim).fill(0);
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    hash = (hash << 5) - hash + text.charCodeAt(i);
    hash |= 0;
  }
  for (let i = 0; i < dim; i++) {
    const val = Math.sin(hash + i) * 10000;
    vec[i] = val - Math.floor(val);
  }
  let sumSq = 0;
  for (let i = 0; i < dim; i++) sumSq += vec[i] * vec[i];
  const norm = Math.sqrt(sumSq) || 1;
  return vec.map((v) => v / norm);
}

export async function getEmbedding(text: string): Promise<number[]> {
  // Try OpenAI embeddings first
  if (openaiClient) {
    try {
      const response = await openaiClient.embeddings.create({
        model: "text-embedding-3-small",
        input: text,
      });
      const emb = response.data[0]?.embedding;
      if (emb) return emb;
    } catch (err) {
      console.warn("[LLM Service] OpenAI embedding call failed, using deterministic fallback:", (err as Error).message);
    }
  }

  // Fallback deterministic embeddings for local dev/test or when key is not set
  return createDeterministicEmbedding(text);
}

export async function getEmbeddings(texts: string[]): Promise<number[][]> {
  if (texts.length === 0) return [];
  if (openaiClient) {
    try {
      const response = await openaiClient.embeddings.create({
        model: "text-embedding-3-small",
        input: texts,
      });
      const sortedData = response.data.sort((a, b) => a.index - b.index);
      return sortedData.map((d) => d.embedding);
    } catch (err) {
      console.warn("[LLM Service] OpenAI batch embedding call failed, using deterministic fallback:", (err as Error).message);
    }
  }

  return texts.map((t) => createDeterministicEmbedding(t));
}

// ---------------------------------------------------------------------------
// Text Generation with Multi-Tier Fallback (OpenAI -> Groq gpt-oss-120b)
// ---------------------------------------------------------------------------
export async function generateText(
  prompt: string,
  systemInstruction?: string,
  explicitModel?: string
): Promise<string> {
  const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [
    ...(systemInstruction ? [{ role: "system" as const, content: systemInstruction }] : []),
    { role: "user" as const, content: prompt },
  ];

  // 1. Attempt Primary: OpenAI
  if (openaiClient) {
    const modelToUse = explicitModel || OPENAI_MODEL;
    try {
      const response = await openaiClient.chat.completions.create({
        model: modelToUse,
        messages,
      });
      const content = response.choices[0]?.message?.content;
      if (content) return content;
    } catch (err) {
      console.warn(
        `[LLM Service] Primary OpenAI (${modelToUse}) failed: ${(err as Error).message}. Attempting Groq fallback...`
      );
    }
  }

  // 2. Attempt Fallback: Groq (gpt-oss-120b with llama-3.3-70b-versatile backup)
  if (groqClient) {
    const candidateModels = [
      explicitModel && !explicitModel.includes("gpt-4o") ? explicitModel : GROQ_MODEL,
      "openai/gpt-oss-20b",
      "qwen/qwen3.8-27b",
    ].filter((m, idx, arr) => arr.indexOf(m) === idx);

    for (const modelToUse of candidateModels) {
      try {
        const response = await groqClient.chat.completions.create({
          model: modelToUse,
          messages,
        });
        const content = response.choices[0]?.message?.content;
        if (content) return content;
      } catch (err) {
        console.warn(`[LLM Service] Groq (${modelToUse}) failed: ${(err as Error).message}`);
      }
    }
  }

  // 3. Attempt AICredits (if configured)
  if (aicreditsClient) {
    try {
      const response = await aicreditsClient.chat.completions.create({
        model: explicitModel || "gpt-4o-mini",
        messages,
      });
      const content = response.choices[0]?.message?.content;
      if (content) return content;
    } catch (err) {
      console.warn(`[LLM Service] AICredits fallback failed: ${(err as Error).message}`);
    }
  }

  throw new Error(
    "All LLM generation providers failed or no API keys provided. Please set OPENAI_API_KEY or GROQ_API_KEY in backend/.env"
  );
}

// ---------------------------------------------------------------------------
// JSON Generation with Multi-Tier Fallback (OpenAI -> Groq gpt-oss-120b)
// ---------------------------------------------------------------------------
export async function generateJSON<T = any>(
  prompt: string,
  systemInstruction?: string,
  explicitModel?: string
): Promise<T> {
  const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [
    ...(systemInstruction ? [{ role: "system" as const, content: systemInstruction }] : []),
    { role: "user" as const, content: prompt },
  ];

  function extractJSON(rawText: string): T {
    let jsonStr = rawText.trim();
    const jsonMatch = jsonStr.match(/```(?:json)?\s*([\s\S]*?)```/);
    if (jsonMatch && jsonMatch[1]) {
      jsonStr = jsonMatch[1].trim();
    }
    const objMatch = jsonStr.match(/\{[\s\S]*\}/) || jsonStr.match(/\[[\s\S]*\]/);
    if (objMatch) {
      jsonStr = objMatch[0];
    }
    return JSON.parse(jsonStr) as T;
  }

  // 1. Attempt Primary: OpenAI
  if (openaiClient) {
    const modelToUse = explicitModel || OPENAI_MODEL;
    try {
      const response = await openaiClient.chat.completions.create({
        model: modelToUse,
        messages,
        response_format: { type: "json_object" },
      });
      const content = response.choices[0]?.message?.content;
      if (content) {
        return extractJSON(content);
      }
    } catch (err) {
      console.warn(
        `[LLM Service] Primary OpenAI JSON generation (${modelToUse}) failed: ${(err as Error).message}. Attempting Groq fallback...`
      );
    }
  }

  // 2. Attempt Fallback: Groq (gpt-oss-120b with llama-3.3-70b-versatile backup)
  if (groqClient) {
    const candidateModels = [
      explicitModel && !explicitModel.includes("gpt-4o") ? explicitModel : GROQ_MODEL,
      "openai/gpt-oss-20b",
      "qwen/qwen3.8-27b",
    ].filter((m, idx, arr) => arr.indexOf(m) === idx);

    for (const modelToUse of candidateModels) {
      try {
        const response = await groqClient.chat.completions.create({
          model: modelToUse,
          messages,
          response_format: { type: "json_object" },
        });
        const content = response.choices[0]?.message?.content;
        if (content) {
          return extractJSON(content);
        }
      } catch (err) {
        console.warn(`[LLM Service] Groq JSON generation (${modelToUse}) failed: ${(err as Error).message}`);
      }
    }
  }

  // 3. Fallback: Generate via plain text and parse JSON
  try {
    const rawText = await generateText(
      prompt + "\n\nIMPORTANT: Return ONLY a valid JSON object or array. Do NOT include markdown text outside of the JSON.",
      systemInstruction,
      explicitModel
    );
    return extractJSON(rawText);
  } catch (err) {
    throw new Error(
      `Failed to generate structured JSON: ${(err as Error).message}`
    );
  }
}
