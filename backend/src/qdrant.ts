import { QdrantClient } from "@qdrant/js-client-rest";

const QDRANT_URL = process.env.QDRANT_URL || "http://localhost:6333";
const QDRANT_API_KEY = process.env.QDRANT_API_KEY?.trim();
const COLLECTION_NAME = "chunks";

interface VectorPoint {
  id: string;
  vector: number[];
  payload: {
    notebook_id: string;
    source_id: string;
    [key: string]: any;
  };
}

export const qdrantClient = new QdrantClient({
  url: QDRANT_URL,
  ...(QDRANT_API_KEY ? { apiKey: QDRANT_API_KEY } : {}),
  checkCompatibility: false,
});

// In-memory fallback for local development when Qdrant is not running
const localVectorStore = new Map<string, VectorPoint>();
let qdrantAvailable = true;

function cosineSimilarity(a: number[], b: number[]): number {
  let dot = 0;
  let normA = 0;
  let normB = 0;
  const len = Math.min(a.length, b.length);
  for (let i = 0; i < len; i++) {
    const valA = a[i] ?? 0;
    const valB = b[i] ?? 0;
    dot += valA * valB;
    normA += valA * valA;
    normB += valB * valB;
  }
  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
}

export async function ensureCollection(): Promise<boolean> {
  if (!qdrantAvailable) return false;
  try {
    const collections = await qdrantClient.getCollections();
    const exists = collections.collections.some((c) => c.name === COLLECTION_NAME);
    if (!exists) {
      await qdrantClient.createCollection(COLLECTION_NAME, {
        vectors: {
          size: 1536,
          distance: "Cosine",
        },
      });
      await qdrantClient.createPayloadIndex(COLLECTION_NAME, {
        field_name: "source_id",
        field_schema: "keyword",
      });
      await qdrantClient.createPayloadIndex(COLLECTION_NAME, {
        field_name: "notebook_id",
        field_schema: "keyword",
      });
    }
    return true;
  } catch (err) {
    if (qdrantAvailable) {
      console.warn(`Qdrant unavailable at ${QDRANT_URL}, using local in-memory vector store`);
      qdrantAvailable = false;
    }
    return false;
  }
}

export async function upsertChunkVectors(points: VectorPoint[]): Promise<void> {
  const isAvailable = await ensureCollection();
  if (isAvailable) {
    try {
      await qdrantClient.upsert(COLLECTION_NAME, {
        wait: true,
        points: points.map((p) => ({
          id: p.id,
          vector: p.vector,
          payload: p.payload,
        })),
      });
      return;
    } catch (err) {
      console.warn("Qdrant upsert failed, saving to local store:", (err as Error).message);
    }
  }

  for (const p of points) {
    localVectorStore.set(p.id, p);
  }
}

export async function searchNotebookChunks(
  notebookId: string,
  queryVector: number[],
  limit: number = 5
): Promise<Array<{ id: string; score: number }>> {
  const isAvailable = await ensureCollection();
  if (isAvailable) {
    try {
      const res = await qdrantClient.search(COLLECTION_NAME, {
        vector: queryVector,
        filter: {
          must: [
            {
              key: "notebook_id",
              match: { value: notebookId },
            },
          ],
        },
        limit,
      });
      return res.map((r) => ({ id: String(r.id), score: r.score }));
    } catch (err) {
      console.warn("Qdrant search failed, searching local store:", (err as Error).message);
    }
  }

  const results: Array<{ id: string; score: number }> = [];
  for (const point of localVectorStore.values()) {
    if (point.payload?.notebook_id === notebookId) {
      const score = cosineSimilarity(queryVector, point.vector);
      results.push({ id: point.id, score });
    }
  }
  return results.sort((a, b) => b.score - a.score).slice(0, limit);
}

export async function deleteChunksBySourceId(sourceId: string): Promise<void> {
  const isAvailable = await ensureCollection();
  if (isAvailable) {
    try {
      await qdrantClient.delete(COLLECTION_NAME, {
        filter: {
          must: [
            {
              key: "source_id",
              match: { value: sourceId },
            },
          ],
        },
      });
    } catch (err) {
      // Ignore qdrant cleanup errors in dev
    }
  }

  for (const [id, point] of localVectorStore.entries()) {
    if (point.payload?.source_id === sourceId) {
      localVectorStore.delete(id);
    }
  }
}
