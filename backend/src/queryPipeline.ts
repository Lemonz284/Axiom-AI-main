import { db } from "./db";
import { generateText, generateJSON } from "./llm";
import { searchNotebookChunks } from "./qdrant";

export interface Citation {
  chunkId: string;
  sourceId: string;
  sourceTitle?: string;
  snippet: string;
}

export interface QueryResult {
  queryId: string;
  text: string;
  citations: Citation[];
}

interface ChunkCandidate {
  id: string;
  sourceId: string;
  notebookId: string;
  text: string;
  chunkIndex: number;
  location: any;
  score: number;
  sourceTitle?: string;
}

interface QueryExpansion {
  synonyms: string[];
  keyphrases: string[];
  keywords: string[];
  domainStopwords?: string[];
}

export async function runQueryPipeline(notebookId: string, question: string): Promise<QueryResult> {
  const queryRecord = await db.query.create({
    data: {
      notebookId,
      question,
    },
  });

  let currentQuestion = question;
  let attempts = 0;
  const maxAttempts = 2;

  let finalAnswerText = "";
  let finalCitations: Citation[] = [];

  while (attempts <= maxAttempts) {
    attempts++;

    // -------------------------------------------------------------------------
    // 1. Semantic Query Expansion (Synonym & Multi-Word Phrase Discovery)
    // -------------------------------------------------------------------------
    const expansionPrompt = `Analyze this user research query for multimodal retrieval across video transcripts, audio lectures, textbooks, and documentation: "${currentQuestion}".

Identify:
1. "synonyms": 3-6 canonical synonyms, alternative phrasing, or related technical terms that different lecturers/authors use for this topic (e.g., for "subqueries": ["nested queries", "nested query", "inner query", "sub-select", "query within a query"]; for "joins": ["table join", "inner join", "combining tables", "cross join"]).
2. "keyphrases": 2-4 word distinctive technical phrases that are literally spoken or written when teaching this concept.
3. "keywords": 3-6 specific discriminating single words (exclude broad domain stopwords like "data", "database", "sql", "system", "table").
4. "domainStopwords": 3-6 ultra-broad words in this subject area that appear in almost every section and should not dominate search ranking.

Output strictly valid JSON:
{
  "synonyms": ["..."],
  "keyphrases": ["..."],
  "keywords": ["..."],
  "domainStopwords": ["..."]
}`;

    let expansion: QueryExpansion = { synonyms: [], keyphrases: [], keywords: [], domainStopwords: [] };
    let hydeHypotheticalDoc = "";

    try {
      const [expResult, hydeResult] = await Promise.all([
        generateJSON<QueryExpansion>(
          expansionPrompt,
          "You are an expert search retrieval expansion engine. Output strictly valid JSON."
        ),
        generateText(
          `Write a short, authoritative 2-sentence synthesis directly answering: "${currentQuestion}"`,
          "You are an expert academic research synthesizer.",
          "gpt-4o-mini"
        ),
      ]);
      if (expResult && (expResult.synonyms || expResult.keywords)) {
        expansion = expResult;
      }
      hydeHypotheticalDoc = hydeResult || "";
    } catch (expErr) {
      console.warn("[QueryPipeline] Query expansion failed, using rule-based fallback:", (expErr as Error).message);
    }

    // -------------------------------------------------------------------------
    // 2. Fetch Notebook Chunks
    // -------------------------------------------------------------------------
    const allNotebookChunks = await db.chunk.findMany({
      where: { notebookId },
      include: { source: true },
    });

    if (allNotebookChunks.length === 0) {
      finalAnswerText = "No sources found in this notebook. Please add notes, documents, or video links first.";
      finalCitations = [];
      break;
    }

    const candidateScores = new Map<string, number>();

    // -------------------------------------------------------------------------
    // 3. Dense Semantic Vector Retrieval (if embeddings available)
    // -------------------------------------------------------------------------
    try {
      const { getEmbeddings } = await import("./llm");
      const searchTexts = [currentQuestion];
      if (expansion.synonyms?.[0]) searchTexts.push(expansion.synonyms[0]);
      if (hydeHypotheticalDoc) searchTexts.push(hydeHypotheticalDoc);

      const queryVectors = await getEmbeddings(searchTexts);
      await Promise.all(
        queryVectors.map(async (qVec) => {
          const searchRes = await searchNotebookChunks(notebookId, qVec, 8);
          for (const res of searchRes) {
            const existing = candidateScores.get(res.id) || 0;
            candidateScores.set(res.id, Math.max(existing, res.score * 50));
          }
        })
      );
    } catch (embErr) {
      // Vector search is optional; proceed with hybrid phrase/lexical search
    }

    // -------------------------------------------------------------------------
    // 4. Multi-Word Phrase Matching & BM25 Inverse Document Frequency Scoring
    // -------------------------------------------------------------------------
    const phrases = [...(expansion.synonyms || []), ...(expansion.keyphrases || [])]
      .map((p) => p.toLowerCase().trim())
      .filter((p) => p.length >= 3);

    const keywords = (expansion.keywords || [])
      .map((k) => k.toLowerCase().trim())
      .filter((k) => k.length >= 3);

    const commonEnglishStopwords = new Set([
      "a", "an", "the", "and", "or", "but", "if", "in", "on", "at", "to", "for", "with",
      "about", "against", "between", "into", "through", "during", "before", "after",
      "above", "below", "from", "up", "down", "is", "are", "was", "were", "be", "been",
      "being", "have", "has", "had", "do", "does", "did", "can", "could", "shall",
      "should", "will", "would", "may", "might", "must", "it", "its", "this", "that",
      "these", "those", "what", "which", "who", "whom", "how", "why", "where", "when",
      "tell", "give", "explain", "describe", "show", "me", "you", "your", "please", "we"
    ]);

    const directUserTerms = currentQuestion
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, " ")
      .split(/\s+/)
      .filter((w) => w.length >= 3 && !commonEnglishStopwords.has(w));

    // Stems for direct terms
    const directUserStems: string[] = [];
    for (const w of directUserTerms) {
      directUserStems.push(w);
      const s = w.replace(/(?:ing|ies|es|ed|s)$/, "");
      if (s.length >= 3 && s !== w) directUserStems.push(s);
    }

    const domainStopwords = new Set([
      ...(expansion.domainStopwords || []).map((s) => s.toLowerCase().trim()),
      "data", "database", "system"
    ]);

    // Calculate Document Frequency (DF) across the notebook
    const N = allNotebookChunks.length;
    const dfMap = new Map<string, number>();
    for (const chunk of allNotebookChunks) {
      const textLower = chunk.text.toLowerCase();
      for (const phrase of phrases) {
        if (textLower.includes(phrase)) {
          dfMap.set(phrase, (dfMap.get(phrase) || 0) + 1);
        }
      }
      for (const term of [...directUserStems, ...keywords]) {
        if (textLower.includes(term)) {
          dfMap.set(term, (dfMap.get(term) || 0) + 1);
        }
      }
    }

    for (const chunk of allNotebookChunks) {
      const textLower = chunk.text.toLowerCase();
      let chunkScore = candidateScores.get(chunk.id) || 0;

      // 4a. Multi-Word Phrase Matches (Highest Signal, e.g. "nested queries", "inner join")
      for (const phrase of phrases) {
        if (textLower.includes(phrase)) {
          const occurrences = textLower.split(phrase).length - 1;
          const df = dfMap.get(phrase) || 1;
          const idf = Math.log((N - df + 0.5) / (df + 0.5) + 1);
          chunkScore += 65 * Math.max(0.6, idf) * Math.min(occurrences, 3);
        }
      }

      // 4b. Direct User Question Terms (excluding domain stopwords)
      for (const term of directUserStems) {
        if (domainStopwords.has(term)) continue;
        if (textLower.includes(term)) {
          const occurrences = textLower.split(term).length - 1;
          const df = dfMap.get(term) || 1;
          const idf = Math.log((N - df + 0.5) / (df + 0.5) + 1);
          chunkScore += 30 * Math.max(0.2, idf) * Math.min(occurrences, 3);
        }
      }

      // 4c. Concept Keywords
      for (const kw of keywords) {
        if (domainStopwords.has(kw)) continue;
        if (textLower.includes(kw)) {
          const occurrences = textLower.split(kw).length - 1;
          const df = dfMap.get(kw) || 1;
          const idf = Math.log((N - df + 0.5) / (df + 0.5) + 1);
          chunkScore += 12 * Math.max(0.2, idf) * Math.min(occurrences, 2);
        }
      }

      // 4d. HyDE Semantic Support
      if (hydeHypotheticalDoc && hydeHypotheticalDoc.length > 20) {
        const hydeTokens = hydeHypotheticalDoc
          .toLowerCase()
          .replace(/[^a-z0-9\s]/g, " ")
          .split(/\s+/)
          .filter((t) => t.length > 5 && !commonEnglishStopwords.has(t) && !domainStopwords.has(t));
        let hydeOverlap = 0;
        for (const ht of hydeTokens.slice(0, 10)) {
          if (textLower.includes(ht)) hydeOverlap++;
        }
        if (hydeOverlap > 1) {
          chunkScore += hydeOverlap * 3;
        }
      }

      if (chunkScore > 0) {
        candidateScores.set(chunk.id, chunkScore);
      }
    }

    // Sort candidate chunks by stage 1 score
    const scoredCandidates: ChunkCandidate[] = allNotebookChunks
      .filter((c) => candidateScores.has(c.id) && (candidateScores.get(c.id) || 0) > 0)
      .map((c) => ({
        id: c.id,
        sourceId: c.sourceId,
        notebookId: c.notebookId,
        text: c.text,
        chunkIndex: c.chunkIndex,
        location: JSON.parse(c.location || "{}"),
        score: candidateScores.get(c.id) || 0,
        sourceTitle: (c as any).source?.title || "Source Document",
      }))
      .sort((a, b) => b.score - a.score);

    // Fallback if no specific matches found
    let candidatePool = scoredCandidates.slice(0, 14);
    if (candidatePool.length === 0) {
      const step = Math.max(1, Math.floor(allNotebookChunks.length / 8));
      candidatePool = allNotebookChunks
        .filter((_, idx) => idx % step === 0)
        .slice(0, 8)
        .map((c) => ({
          id: c.id,
          sourceId: c.sourceId,
          notebookId: c.notebookId,
          text: c.text,
          chunkIndex: c.chunkIndex,
          location: JSON.parse(c.location || "{}"),
          score: 1,
          sourceTitle: (c as any).source?.title || "Source Document",
        }));
    }

    // -------------------------------------------------------------------------
    // 5. Stage 2: Cross-Encoder LLM Reranking
    // -------------------------------------------------------------------------
    let topK: ChunkCandidate[] = candidatePool;

    if (candidatePool.length > 1) {
      try {
        const rerankPrompt = `User Question: "${question}"

Candidate Excerpts from Study Materials:
${candidatePool.slice(0, 10).map((tc, idx) => {
  const loc = tc.location;
  const timeInfo = loc?.startSeconds !== undefined
    ? `Timestamp: ${Math.floor(loc.startSeconds / 3600)}h ${Math.floor((loc.startSeconds % 3600) / 60)}m ${loc.startSeconds % 60}s`
    : `Index: ${tc.chunkIndex}`;
  return `[Candidate ${idx + 1} | ID: ${tc.id} | ${timeInfo}]
Source: "${tc.sourceTitle}"
Snippet: ${tc.text.slice(0, 240).replace(/\s+/g, " ")}`;
}).join("\n\n")}

Task: Select and rank the top 4 excerpts that directly explain, define, or demonstrate the answer to the user question.
Crucial rule: If the author or instructor teaches the concept using canonical synonyms (such as "nested queries" for "subqueries", or "relational vs document store" for "non-relational"), rank those instructional chunks at the top!

Output strictly a JSON object:
{
  "rankedIds": ["<id1>", "<id2>", "<id3>", "<id4>"]
}`;

        const rerankResult = await generateJSON<{ rankedIds: string[] }>(
          rerankPrompt,
          "You are an expert search reranker. Output strictly valid JSON."
        );

        if (rerankResult && Array.isArray(rerankResult.rankedIds) && rerankResult.rankedIds.length > 0) {
          const candidateMap = new Map(candidatePool.map((c) => [c.id, c]));
          const rerankedList: ChunkCandidate[] = [];
          for (const id of rerankResult.rankedIds) {
            const found = candidateMap.get(id);
            if (found) rerankedList.push(found);
          }
          // Append remaining candidates from pool
          for (const c of candidatePool) {
            if (!rerankedList.some((r) => r.id === c.id)) {
              rerankedList.push(c);
            }
          }
          topK = rerankedList.slice(0, 7);
        } else {
          topK = candidatePool.slice(0, 7);
        }
      } catch (rerankErr) {
        console.warn("[QueryPipeline] LLM Rerank failed, proceeding with BM25 top chunks:", (rerankErr as Error).message);
        topK = candidatePool.slice(0, 7);
      }
    }

    // -------------------------------------------------------------------------
    // 6. Grounded Answer Synthesis
    // -------------------------------------------------------------------------
    const contextPrompt = topK
      .map((c) => `--- CHUNK [ID: ${c.id} | Source: "${c.sourceTitle}"] ---\n${c.text}`)
      .join("\n\n");

    const answerPrompt = `You are AxiomAI, an advanced multimodal AI learning assistant.
Examine the following Context Sources to answer the User Question thoroughly, professionally, and in depth.

CONTEXT SOURCES:
${contextPrompt}

USER QUESTION:
${question}

GUIDELINES & INSTRUCTIONS:
1. Grounded Citations:
   - Synthesize a detailed, comprehensive, high-value study guide directly grounded in these sources.
   - For every substantive claim, definition, code example, or key mechanism, cite the source chunk using [CID:chunk_id] directly after the statement (e.g., "...uses nested SELECT statements [CID:${topK[0]?.id || "id"}].").
2. Synonym & Terminology Awareness:
   - If the instructor or author uses alternative terminology in the lesson (e.g. "nested queries" for "subqueries", or "relational vs document store"), explicitly clarify this connection for the student (e.g., "In this course, subqueries are taught under the term **nested queries**...").
3. Missing or External Topics (Fallback Rule):
   - ONLY IF the uploaded sources genuinely do NOT contain enough information to answer the question:
     FIRST output a clear callout note:
     "> **Note from AxiomAI**: This specific detail is not directly covered in your uploaded sources. Below is an authoritative explanation based on broader AI and computer science domain knowledge:"
     THEN provide a complete, expert answer.
4. Formatting & Completeness:
   - Provide complete, well-aligned, structured study notes.
   - Organize with clear markdown headings (###), bold key terms, bullet points, and code syntax blocks.
   - Explain how mechanisms work step-by-step and include clear query examples.
`;

    const draftedAnswer = await generateText(
      answerPrompt,
      "You are a precise grounded AI research assistant. Synthesize thorough answers with markdown formatting and include correct [CID:chunk_id] citations where appropriate.",
      "gpt-4o-mini"
    );

    // -------------------------------------------------------------------------
    // 7. CRAG Verification & Citation Extraction
    // -------------------------------------------------------------------------
    const cRagPrompt = `Source Context:\n${contextPrompt}\n\nDrafted Answer:\n${draftedAnswer}\n\nIs the drafted answer helpful, factually consistent, and properly addresses the user question (either grounded in context or appropriately noting external knowledge)? Reply with YES or NO followed by a brief reason.`;

    let isGrounded = true;
    try {
      const cRagVerification = await generateText(
        cRagPrompt,
        "You are a factual verification judge.",
        "gpt-4o-mini"
      );
      isGrounded = cRagVerification.toUpperCase().includes("YES") || draftedAnswer.includes("Note from AxiomAI");
    } catch (verErr) {
      isGrounded = true;
    }

    if (isGrounded || attempts > maxAttempts) {
      // Extract cited chunk IDs in the order they appear in draftedAnswer
      const citedMatches: string[] = [];
      const regex = /[\[【]CID:([a-zA-Z0-9_-]+)[\]】]/g;
      let match;
      while ((match = regex.exec(draftedAnswer)) !== null) {
        if (!citedMatches.includes(match[1])) {
          citedMatches.push(match[1]);
        }
      }

      const candidateMap = new Map(topK.map((c) => [c.id, c]));
      const chunksToCite: ChunkCandidate[] = [];

      for (const cid of citedMatches) {
        const found = candidateMap.get(cid);
        if (found && !chunksToCite.some((c) => c.id === found.id)) {
          chunksToCite.push(found);
        }
      }

      // If no chunks were cited in text, take top 1-2 chunks unless it was purely external note
      if (chunksToCite.length === 0 && !draftedAnswer.includes("Note from AxiomAI")) {
        chunksToCite.push(...topK.slice(0, 2));
      }

      finalCitations = chunksToCite.map((c) => ({
        chunkId: c.id,
        sourceId: c.sourceId,
        sourceTitle: c.sourceTitle,
        snippet: c.text.slice(0, 220) + (c.text.length > 220 ? "..." : ""),
      }));

      // Map cited chunk IDs to 1-based sequential badges [1], [2], etc.
      const chunkIdToIndex = new Map<string, number>();
      chunksToCite.forEach((c, i) => chunkIdToIndex.set(c.id, i + 1));

      finalAnswerText = draftedAnswer.replace(/[\[【]CID:([a-zA-Z0-9_-]+)[\]】]/g, (m, cid) => {
        const idx = chunkIdToIndex.get(cid);
        return idx !== undefined ? `[${idx}]` : "";
      });

      break;
    } else {
      currentQuestion = `Detailed clarification regarding ${question}`;
    }
  }

  await db.answer.create({
    data: {
      queryId: queryRecord.id,
      text: finalAnswerText,
      citations: JSON.stringify(finalCitations),
    },
  });

  return {
    queryId: queryRecord.id,
    text: finalAnswerText,
    citations: finalCitations,
  };
}
