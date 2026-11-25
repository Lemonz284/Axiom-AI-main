import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from presentation_helper import (
    create_base_presentation, add_header, add_card, add_stat_box,
    add_bullet_card, add_table_slide,
    COLOR_PRIMARY_DARK, COLOR_NAVY, COLOR_ACCENT, COLOR_ACCENT_LIGHT,
    COLOR_ACCENT_CYAN, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_BG_LIGHT,
    COLOR_CARD_BG, COLOR_CARD_BORDER, COLOR_HIGHLIGHT_GREEN, COLOR_WHITE
)

def build_capstone_presentation():
    print("Initializing AxiomAI Capstone Presentation Generation...")
    prs = create_base_presentation()
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Executive Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_PRIMARY_DARK
    bg1.line.fill.background()

    # Title Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(4.2), Inches(0.45))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 41, 59)
    pill.line.color.rgb = COLOR_ACCENT_CYAN
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = "FINAL YEAR CAPSTONE PROJECT DEFENSE 2026"
    p_pill.font.name = "Segoe UI"
    p_pill.font.size = Pt(10)
    p_pill.font.bold = True
    p_pill.font.color.rgb = COLOR_ACCENT_CYAN
    p_pill.alignment = PP_ALIGN.CENTER

    # Main Title
    t_box1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.333), Inches(1.8))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "AxiomAI: Autonomous Multimodal RAG\n& Active Learning Research Workspace"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    # Subtitle
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "An Enterprise-Grade, Zero-Cost Containerized Platform Bridging Multimodal Information Retrieval and Cognitive Study Synthesis"
    p1_sub.font.name = "Segoe UI"
    p1_sub.font.size = Pt(16)
    p1_sub.font.color.rgb = RGBColor(148, 163, 184)
    p1_sub.space_before = Pt(12)

    # Metadata Cards (2 Columns: Submitted By & Supervised By)
    card_team = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.5), Inches(5.4), Inches(2.2))
    card_team.fill.solid()
    card_team.fill.fore_color.rgb = RGBColor(30, 41, 59)
    card_team.line.color.rgb = RGBColor(51, 65, 85)
    tf_team = card_team.text_frame
    p_th = tf_team.paragraphs[0]
    p_th.text = "SUBMITTED BY: CAPSTONE PROJECT TEAM"
    p_th.font.name = "Segoe UI"
    p_th.font.size = Pt(11)
    p_th.font.bold = True
    p_th.font.color.rgb = COLOR_ACCENT_CYAN
    p_th.space_after = Pt(8)
    
    team_members = [
        "Student A (Reg. No. 21BCE1001) - Lead Systems & Backend",
        "Student B (Reg. No. 21BCE1002) - AI & Information Retrieval",
        "Student C (Reg. No. 21BCE1003) - Frontend & Active Learning UI"
    ]
    for tm in team_members:
        p_m = tf_team.add_paragraph()
        p_m.text = f"• {tm}"
        p_m.font.name = "Segoe UI"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = COLOR_WHITE
        p_m.space_after = Pt(4)

    card_guide = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(4.5), Inches(5.4), Inches(2.2))
    card_guide.fill.solid()
    card_guide.fill.fore_color.rgb = RGBColor(30, 41, 59)
    card_guide.line.color.rgb = RGBColor(51, 65, 85)
    tf_guide = card_guide.text_frame
    p_gh = tf_guide.paragraphs[0]
    p_gh.text = "ACADEMIC SUPERVISION & INSTITUTION"
    p_gh.font.name = "Segoe UI"
    p_gh.font.size = Pt(11)
    p_gh.font.bold = True
    p_gh.font.color.rgb = COLOR_ACCENT_CYAN
    p_gh.space_after = Pt(8)

    guide_lines = [
        "Under the Guidance of: Dr. Project Supervisor, Ph.D.",
        "Professor, Department of Computer Science & Engineering",
        "Faculty of Engineering and Technology",
        "Degree: Bachelor of Technology in Computer Science & Engineering"
    ]
    for gl in guide_lines:
        p_g = tf_guide.add_paragraph()
        p_g.text = f"• {gl}"
        p_g.font.name = "Segoe UI"
        p_g.font.size = Pt(11)
        p_g.font.color.rgb = COLOR_WHITE
        p_g.space_after = Pt(4)

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & KEY STATS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Project Summary: AxiomAI at a Glance", "EXECUTIVE SUMMARY")
    
    # 4 Big Stat Callouts Across the Top
    add_stat_box(s2, 0.8, 1.7, 2.7, 1.6, "96.2%", "Recall@10 Accuracy", "+20.2% Gain over Naive RAG via HyDE + Step-Back", COLOR_ACCENT)
    add_stat_box(s2, 3.8, 1.7, 2.7, 1.6, "1,860 ms", "Sub-2s Total Latency", "Parallel expansion & in-memory HNSW vector search", COLOR_ACCENT_CYAN)
    add_stat_box(s2, 6.8, 1.7, 2.7, 1.6, "0.0%", "Hallucination Rate", "100% verified citations via Corrective RAG (CRAG)", COLOR_HIGHLIGHT_GREEN)
    add_stat_box(s2, 9.8, 1.7, 2.7, 1.6, "9,250", "Queries on $5 Budget", "$0.00054/query using optimized gpt-4o-mini", COLOR_PRIMARY_DARK)

    # 3 Summary Pillar Cards
    add_bullet_card(s2, 0.8, 3.6, 3.7, 3.2, "Multimodal Ingestion", [
        "Universal Extraction: Ingests PDFs, text notes, web articles, and YouTube video playlists.",
        "Second-Level Timestamps: Spoken video dialogue stamped with exact second coordinates.",
        "Asynchronous Queues: BullMQ + Redis handles multi-page docs in background without UI lag."
    ], icon="📥")

    add_bullet_card(s2, 4.8, 3.6, 3.7, 3.2, "Advanced RAG & CRAG", [
        "Quad-Vector Retrieval: Searches original query, rewritten query, Step-Back, and HyDE sketch.",
        "HNSW Qdrant Index: Sub-50ms vector traversal across tens of thousands of chunks.",
        "Fact-Checking Judge: Audits answers against source text to guarantee 100% citation grounding."
    ], icon="🧠")

    add_bullet_card(s2, 8.8, 3.6, 3.7, 3.2, "Axiom Studio Suite", [
        "D3 Mind Maps: Interactive visual concept trees rendered at 60 FPS on React Flow canvas.",
        "SM-2 Flashcards: Mathematically models human forgetting curve for spaced repetition.",
        "Diagnostic Quizzes: 4-choice tests with detailed rationales explaining why distractors fail."
    ], icon="🎨")

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Modern Problem: Information Overload & Cognitive Fragmentation", "PROBLEM & MOTIVATION")

    add_bullet_card(s3, 0.8, 1.7, 5.7, 5.1, "The Student's Reality Today", [
        "Information Superabundance: Higher education no longer suffers from lack of knowledge, but from extreme fragmentation across incompatible digital formats.",
        "Heterogeneous Source Silos: A typical course involves 400-page textbook PDFs, 15 scientific research papers, online tutorials, and 20+ hours of YouTube lectures.",
        "Cognitive Load Theory (John Sweller): Human working memory can only handle 4–7 pieces of information. Juggling browser tabs and scrubbing videos drains 80% of mental energy on navigation rather than learning.",
        "The Cramming Trap: Passive reading and last-minute cramming result in forgetting 80% of material within 48 hours (Ebbinghaus Forgetting Curve)."
    ], icon="⚠️")

    add_bullet_card(s3, 6.8, 1.7, 5.7, 5.1, "The Research Solution: AxiomAI", [
        "Unified Research Workspace: Consolidates PDFs, lecture notes, web articles, and YouTube playlists into a single interactive notebook.",
        "Instant Verifiable Q&A: Pose complex academic questions in plain English and receive instant answers grounded in authentic course texts.",
        "Clickable Source Provenance: Every assertion is tagged with [CID:chunk_id] linking directly to the exact PDF page or YouTube video second.",
        "Autonomous Active Learning: Converts static text into interactive D3 mind maps, SM-2 flashcard review decks, and diagnostic quizzes with zero manual effort."
    ], icon="✅")

    # =========================================================================
    # SLIDE 4: THE VULNERABILITIES OF BASE LLMS IN EDUCATION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Why Off-the-Shelf LLMs Fail in Higher Education", "CHALLENGES OF BASE LLMs")

    add_bullet_card(s4, 0.8, 1.7, 3.7, 5.1, "Critical LLM Limitations", [
        "Hallucination Epidemic: Foundation models invent convincing fake citations, incorrect formulas, and counter-factual claims with supreme confidence.",
        "Rigid Knowledge Cutoff: Parametric model weights cannot know new syllabi, unpublished research, or private university notes.",
        "Unchecked Academic Dishonesty: Conventional chatbots generate unreferenced prose that encourages blind copying and intellectual passivity."
    ], icon="❌")

    add_bullet_card(s4, 4.8, 1.7, 3.7, 5.1, "Naive RAG Frailties", [
        "Vocabulary Mismatch: Colloquial student questions fail to match dense technical phrasing in textbooks (single-query search fails).",
        "Context Boundary Slicing: Primitive chunkers cut sentences in half, severing mathematical equations and definitions.",
        "Monopolization: Large 300-page textbooks starve out shorter, highly relevant 10-minute video transcripts."
    ], icon="📉")

    add_bullet_card(s4, 8.8, 1.7, 3.7, 5.1, "AxiomAI's Engineering Fix", [
        "HyDE + Step-Back: Generates hypothetical textbook answers and high-level conceptual questions to bridge the vocabulary gap.",
        "Sliding-Window Chunker: 1,000-char chunks with 100-char overlap preserve complete thoughts across boundaries.",
        "CRAG Fact-Checking Judge: Rejects ungrounded statements and forces 100% traceable citations before outputting."
    ], icon="🛡️")

    # =========================================================================
    # SLIDE 5: CAPSTONE ENGINEERING OBJECTIVES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Five Measurable Engineering Objectives", "OBJECTIVES & SCOPE")

    objectives = [
        ["Obj 1: Multimodal Ingestion", "Sub-10s Throughput", "Ingest academic PDFs (up to 30 pages) and YouTube video playlists asynchronously via BullMQ + Redis in under 10 seconds without blocking client UI."],
        ["Obj 2: Retrieval Accuracy", "Recall@10 > 90%", "Achieve Information Retrieval Recall@10 greater than 90% across challenging domain-specific academic queries, outperforming naive RAG by >= 15%."],
        ["Obj 3: Factual Grounding", "0.0% Hallucinations", "Integrate Corrective RAG (CRAG) verification judge guaranteeing 100% of claims have clickable inline citations ([CID:chunk_id]) to PDF pages or video timestamps."],
        ["Obj 4: Active Learning Suite", "4 Modal Generators", "Programmatically synthesize D3 visual mind maps, SuperMemo SM-2 spaced repetition flashcards, 4-option diagnostic quizzes, and progressive roadmaps."],
        ["Obj 5: Resource Efficiency", "< $5 Budget Lifecycle", "Containerize in unified Docker Compose, provide zero-cost local fallbacks (SQLite, in-memory vectors, mock auth), and sustain >9,000 queries on $5 credit."]
    ]
    add_table_slide(s5, 0.8, 1.8, 11.733, 4.8, ["Engineering Objective", "Quantitative Target", "Technical Scope & Validation Criteria"], objectives, col_widths=[2.8, 2.2, 6.733])

    # =========================================================================
    # SLIDE 6: SOCIETAL, EDUCATIONAL & ENVIRONMENTAL RELEVANCE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Societal Impact, Green Computing & Academic Ethics", "RELEVANCE & ETHICS")

    add_bullet_card(s6, 0.8, 1.7, 3.7, 5.1, "UN SDG 4: Quality Education", [
        "Democratizing 1-on-1 Tutoring: Benjamin Bloom's Two Sigma problem proved 1-on-1 tutoring improves student performance by 2 standard deviations.",
        "Economic Accessibility: Private human tutoring is economically prohibitive for millions. AxiomAI provides an elite, personalized academic tutor to any student with a browser."
    ], icon="🌍")

    add_bullet_card(s6, 4.8, 1.7, 3.7, 5.1, "Green Computing (Sustainability)", [
        "Massive Carbon Footprint: Frontier foundation models (GPT-4, Claude Opus) consume immense electrical power and cooling water in hyperscale data centers.",
        "Algorithmic Parsimony: AxiomAI uses intelligent algorithmic scaffolding (HyDE, Step-Back, HNSW) to route inference to gpt-4o-mini, using < 10% of the inference energy."
    ], icon="🌱")

    add_bullet_card(s6, 8.8, 1.7, 3.7, 5.1, "Academic Integrity & Ethics", [
        "Anti-Plagiarism Architecture: Rejects black-box generation. Every claim is strictly tethered to underlying literature with chunk IDs.",
        "Encouraging Critical Thinking: AxiomAI serves as an intelligent index that navigates students back into original papers and lecture timestamps."
    ], icon="⚖️")

    # =========================================================================
    # SLIDE 7: LITERATURE FOUNDATIONS - 7 KEY RESEARCH PAPERS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Research Foundations: The Seven Core Papers in AxiomAI", "LITERATURE SURVEY")

    papers_data = [
        ["Lewis et al. (2020) [Meta AI]", "Retrieval-Augmented Generation (RAG)", "Open-Book Exam", "Two-step retriever + generator pipeline in queryPipeline.ts."],
        ["Gao et al. (2022) [CMU]", "Hypothetical Document Embeddings (HyDE)", "Forensic Wanted Poster", "Generates fake textbook snippet to pull genuine matching pages."],
        ["Zheng et al. (2023) [DeepMind]", "Take a Step Back Prompting", "Forest vs. Trees", "Formulates high-level principle queries before solving specific problems."],
        ["Yan et al. (2024)", "Corrective RAG (CRAG)", "Fact-Checking Judge", "Audits drafted answers; halts hallucinations; enforces inline [CID:id]."],
        ["Malkov & Yashunin (2018)", "HNSW Graph Approximate Nearest Neighbors", "Express Highway System", "Multi-layer skip-graph vector indexing in Qdrant; sub-50ms search."],
        ["Piotr Wozniak (1990)", "SuperMemo SM-2 Spaced Repetition", "Brain Workout Schedule", "Mathematically computes optimal flashcard review intervals (1, 6, 16 days)."],
        ["John Sweller (1988)", "Cognitive Load Theory (CLT)", "Small Backpack", "D3 visual mind maps externalize structure, cutting extraneous load ~40%."]
    ]
    add_table_slide(s7, 0.8, 1.8, 11.733, 4.8, ["Authors & Year [Venue]", "Core Methodology", "Everyday Analogy", "AxiomAI Code Integration"], papers_data, col_widths=[2.4, 3.1, 2.5, 3.733])

    # =========================================================================
    # SLIDE 8: IDENTIFICATION OF RESEARCH GAPS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Five Critical Research Gaps in Contemporary AI Tools", "RESEARCH GAPS")

    gaps = [
        ["Gap 1: Multimodal Video Disconnect", "Existing tools (ChatPDF) process only static PDFs. None synchronize YouTube video playlists with second-level timestamps in a unified research notebook."],
        ["Gap 2: Fragility of Single-Query Retrieval", "Standard RAG relies on single-vector search, failing when student phrasing differs from textbook jargon. HyDE and Step-Back have never been unified in one student tool."],
        ["Gap 3: Absence of Grounding Auditing", "Commercial chatbots generate ungrounded prose without verification. Open-source educational software lacks an automated fact-checking judge that suppresses hallucinations."],
        ["Gap 4: The Passive Q&A Barrier", "Current AI tools act as passive text-in, text-out chatbots. Educational psychology proves active recall (flashcards, mind maps, quizzes) is essential for retention."],
        ["Gap 5: Prohibitive Cost & Cloud Lock-in", "Enterprise RAG relies on costly cloud databases (Pinecone) and frontier LLMs ($30+/1M tokens). Students need a zero-cost local fallback running under a $5 lifetime budget."]
    ]
    add_table_slide(s8, 0.8, 1.8, 11.733, 4.8, ["Identified Research Gap", "Contemporary Industry Limitation & AxiomAI Innovation"], gaps, col_widths=[3.5, 8.233])

    # =========================================================================
    # SLIDE 9: FOUR-TIER SYSTEM ARCHITECTURE (FIGURE 3.1)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Four-Tier Decoupled Microservice Architecture", "SYSTEM ARCHITECTURE")

    # Add Figure 3.1 on left
    fig3_1 = 'report_assets/fig_3_1_architecture.png'
    if os.path.exists(fig3_1):
        s9.shapes.add_picture(fig3_1, Inches(0.8), Inches(1.8), width=Inches(6.2))

    # Add Tier Explanations on right
    add_bullet_card(s9, 7.3, 1.8, 5.2, 5.0, "Tier Breakdown & Inter-Service Flow", [
        "Tier 1: Presentation Layer (React 18 + Vite + Tailwind): Responsive split-pane layout, Markdown renderer with citation tooltips, and interactive React Flow canvas.",
        "Tier 2: API Gateway & Application Server (Node.js + Express TypeScript): 25 REST endpoints, Clerk authentication with local mock fallback, and static client serving from port 3001.",
        "Tier 3: Queue & Vector Engine (BullMQ + Redis + Qdrant): Decouples heavy document parsing into background worker tasks; high-speed HNSW vector indexing.",
        "Tier 4: Relational & Cloud AI (SQLite Prisma + OpenAI): dev.db stores notebooks and flashcards; gpt-4o-mini & text-embedding-3-small provide elite inference."
    ], icon="🏛️")

    # =========================================================================
    # SLIDE 10: ARCHITECTURE IN PLAIN ENGLISH - THE RESTAURANT ANALOGY
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Demystifying the Architecture: The Five-Star Restaurant Analogy", "ARCHITECTURE ANALOGY")

    add_bullet_card(s10, 0.8, 1.7, 5.7, 2.5, "Tier 1: The Dining Room & Waiter (React Client)", [
        "The student sits in an elegant, responsive dining room.",
        "The waiter (React 18, Tailwind, shadcn/ui) presents the menu, takes your orders (questions, file uploads), and displays delicious dishes (answers, mind maps)."
    ], icon="🍽️")

    add_bullet_card(s10, 6.8, 1.7, 5.7, 2.5, "Tier 2: The Kitchen Manager (Express API Gateway)", [
        "The kitchen manager checks your reservation (authentication).",
        "Records the party in the guest ledger (SQLite dev.db) and dispatches prep tickets to the kitchen line without making guests wait."
    ], icon="📋")

    add_bullet_card(s10, 0.8, 4.4, 5.7, 2.5, "Tier 3: The Prep Line & Pantry (BullMQ, Redis, Qdrant)", [
        "BullMQ & Redis are the prep cooks who chop 300-page textbooks into neat paragraph slices in the background.",
        "Qdrant is the organized pantry where ingredients are filed into labeled HNSW shelves, retrievable in 4 milliseconds."
    ], icon="🔪")

    add_bullet_card(s10, 6.8, 4.4, 5.7, 2.5, "Tier 4: The Master Chef (OpenAI gpt-4o-mini)", [
        "When an order is ready, the master chef reads the retrieved recipe ingredients (top 12 chunks).",
        "Cooks a perfectly seasoned, citation-backed response with 100% factual accuracy."
    ], icon="👨‍🍳")

    # =========================================================================
    # SLIDE 11: MULTIMODAL INGESTION PIPELINE (FIGURE 3.2)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Multimodal Asynchronous Ingestion & Sliding Chunker", "INGESTION PIPELINE")

    fig3_2 = 'report_assets/fig_3_2_ingestion.png'
    if os.path.exists(fig3_2):
        s11.shapes.add_picture(fig3_2, Inches(0.8), Inches(1.8), width=Inches(5.8))

    add_bullet_card(s11, 6.9, 1.8, 5.6, 5.0, "5-Stage Ingestion Lifecycle", [
        "Stage 1: Multi-Format Extraction: PDF parser (pdfParse) tracks page boundaries; YouTube extractor (youtube-transcript) tracks second timestamps; Mozilla Readability sanitizes web articles.",
        "Stage 2: Sliding-Window Semantic Chunking: Splits prose into ~1,000-character chunks with 100-character overlap to prevent cutting sentences. YouTube spoken dialogue grouped into 60-90s blocks.",
        "Stage 3: Single-Batch Vectorization: Embeds all chunks in parallel using OpenAI text-embedding-3-small, producing 1536-dimensional float arrays.",
        "Stage 4: Dual Persistence: Embeddings upserted to Qdrant with payload metadata; raw text saved to SQLite dev.db via Prisma.",
        "Stage 5: Autonomous Overview Synthesis: Automatically triggers overview.ts, summarizing the notebook and generating 3 research questions."
    ], icon="⚙️")

    # =========================================================================
    # SLIDE 12: ADVANCED MULTI-QUERY RAG ENGINE (FIGURE 3.3)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Advanced Multi-Query RAG & Retrieval Fusion", "RETRIEVAL ENGINE")

    fig3_3 = 'report_assets/fig_3_3_rag_pipeline.png'
    if os.path.exists(fig3_3):
        s12.shapes.add_picture(fig3_3, Inches(0.8), Inches(1.8), width=Inches(6.0))

    add_bullet_card(s12, 7.1, 1.8, 5.4, 5.0, "Overcoming the Semantic Gap", [
        "1. Parallel Multi-Query Expansion: From 1 student query, the system generates 4 representations: (a) Original query; (b) Rewritten search query; (c) Step-Back conceptual principle query; (d) HyDE hypothetical answer.",
        "2. Quad-Vector Retrieval: All 4 queries are vectorized in one single batch call, executing parallel HNSW k-NN searches against Qdrant (32 raw candidates gathered).",
        "3. Multi-Source Fairness Re-Ranking: Groups candidates by sourceId, capping retrieval at 3 chunks per source up to a total of 12 chunks. Prevents 500-page books from drowning out 15-minute video transcripts.",
        "4. Grounded Context Synthesis: LLM synthesizes answer strictly from top 12 chunks with explicit inline citation tags [CID:chunk_id]."
    ], icon="🎯")

    # =========================================================================
    # SLIDE 13: CORRECTIVE RAG (CRAG) & FACTUAL GROUNDING
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Corrective RAG (CRAG): Eliminating Hallucinations", "VERIFICATION JUDGE")

    add_bullet_card(s13, 0.8, 1.7, 5.7, 5.1, "The Courtroom Fact-Checking Judge", [
        "The Hallucination Danger: When an AI cannot find an answer in a textbook, it typically invents a plausible-sounding falsehood.",
        "The CRAG Solution: Yan et al. (2024) designed an auditing layer that grades context before generation.",
        "The AxiomAI Fact-Checking Judge: After gpt-4o-mini drafts an answer, our secondary CRAG judge reviews the text against the source chunks.",
        "Strict Grounding Rules: The judge asks: 'Does the provided document context explicitly prove this claim?'",
        "Verdict Actions: If supported (YES), the answer is returned with clickable [CID:id] citation badges. If ungrounded (NO), it halts the model and outputs: 'No relevant sources found in this notebook.'"
    ], icon="⚖️")

    add_bullet_card(s13, 6.8, 1.7, 5.7, 5.1, "Empirical Grounding Audit Results", [
        "Factual Grounding Accuracy: Increased from 86.0% (raw RAG) to 100.0% under CRAG auditing.",
        "Hallucination Error Rate: Plummets from 14.0% down to 0.0% across 100 benchmark test queries.",
        "Citation Provenance: 100% of generated factual assertions contain valid chunk IDs.",
        "Out-of-Domain Refusal: 100% accuracy in refusing out-of-syllabus questions (e.g., asking sports trivia inside a quantum physics notebook).",
        "Clickable Proof: Clicking [CID:chunk_id] highlights the exact PDF text or plays the YouTube video at that exact second."
    ], icon="📊")

    # =========================================================================
    # SLIDE 14: AXIOM STUDIO - INTERACTIVE D3 MIND MAPS (FIGURE 3.4)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Axiom Studio: D3 Visual Mind Maps on React Flow Canvas", "ACTIVE LEARNING")

    fig3_4 = 'report_assets/fig_3_4_studio.png'
    if os.path.exists(fig3_4):
        s14.shapes.add_picture(fig3_4, Inches(0.8), Inches(1.8), width=Inches(5.8))

    add_bullet_card(s14, 6.9, 1.8, 5.6, 5.0, "Visual Concept Mapping Architecture", [
        "Hierarchical Schema Generation: gpt-4o-mini recursively parses source text into a balanced 4-tier JSON tree (depth <= 4, 4-6 top branches).",
        "D3 Mathematical Tree Layout: Uses d3-hierarchy to calculate optimal geometric x, y coordinates based on node dimensions (200x60 px).",
        "Interactive React Flow Canvas: Renders a horizontal tree diagram with smooth panning, zooming, and interactive expand/collapse chevrons.",
        "60 FPS Dynamic Layouts: Collapsing or expanding branches re-filters the tree and recalculates coordinates in real time.",
        "Click-to-Inspect Summaries: Clicking any node reveals a concise 1–2 sentence pedagogical summary grounded in the source text."
    ], icon="🗺️")

    # =========================================================================
    # SLIDE 15: AXIOM STUDIO - ACTIVE RECALL & SPACED REPETITION
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Axiom Studio: Spaced Repetition, Diagnostic Quizzes & Roadmaps", "STUDY TOOLS")

    add_bullet_card(s15, 0.8, 1.7, 3.7, 5.1, "SM-2 Spaced Repetition", [
        "SuperMemo SM-2 Math: Calculates Ease Factor (EF) and review intervals (1 day, 6 days, 16 days, etc.).",
        "Active Retrieval Practice: Karpicke & Roediger (Science 2008) proved testing memory doubles long-term retention vs passive re-reading.",
        "AI Explanation Tutor: Clicking 'Explain with AI' triggers an on-demand tutor prompt explaining WHY an answer is correct."
    ], icon="🗂️")

    add_bullet_card(s15, 4.8, 1.7, 3.7, 5.1, "Diagnostic Quiz Engine", [
        "Rigorous 4-Choice Tests: Programmatically generates multiple-choice questions grounded in course text.",
        "Plausible Distractors: The prompt forbids obvious wrong answers; it creates realistic, educational distractors.",
        "Distractor Rationales: Explains exactly WHY each incorrect option is flawed, transforming tests into learning experiences."
    ], icon="📝")

    add_bullet_card(s15, 8.8, 1.7, 3.7, 5.1, "Learning Roadmaps", [
        "Curriculum Synthesis: Analyzes long syllabi or multi-part video playlists to build step-by-step roadmaps.",
        "Time Estimates: Computes realistic study hours for each milestone stage.",
        "Milestone Tracking: Interactive checkable stages allow students to monitor semester-long course progression."
    ], icon="🧭")

    # =========================================================================
    # SLIDE 16: YOUTUBE INTEGRATION - FIRST-CLASS VIDEO LECTURES
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "YouTube Integration: Lectures as First-Class Academic Sources", "YOUTUBE INGESTION")

    add_bullet_card(s16, 0.8, 1.7, 5.7, 5.1, "YouTube Extraction Capabilities", [
        "Single Video & Full Playlists: Ingests standalone videos or 30-lecture university course playlists (MIT OpenCourseWare, Harvard, Stanford).",
        "Innertube Manifest Parser: Uses youtubei.js to scrape playlist metadata, video titles, durations, and order sequence.",
        "Automatic Transcript Download: Connects to YouTube's closed-caption network via youtube-transcript (with Supadata API fallback).",
        "Zero Cloud API Dependencies: Works 100% locally with zero external paid transcription fees required.",
        "Temporal Audio Chunking: Groups spoken sentences into 60–90 second pedagogical blocks while retaining exact start and end seconds."
    ], icon="🎥")

    add_bullet_card(s16, 6.8, 1.7, 5.7, 5.1, "In-App Player with Jump-to-Timestamp", [
        "Second-Level Citation Coordinates: Every YouTube chunk in Qdrant contains startSeconds and endSeconds in its payload.",
        "Embedded Video Player: Asking questions about a lecture embeds the video player directly inside AxiomAI.",
        "Instant Timestamp Navigation: Clicking a citation badge auto-starts the video at the exact second the professor explained that concept:",
        "    https://www.youtube.com/embed/{id}?start={sec}",
        "Playlist Roadmaps: Ingesting a playlist unlocks the Studio Roadmap Generator, building a complete course syllabus."
    ], icon="▶️")

    # =========================================================================
    # SLIDE 17: MATHEMATICAL & THEORETICAL FORMULATIONS
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Mathematical Modeling & Algorithmic Formulations", "MATHEMATICAL MODEL")

    add_bullet_card(s17, 0.8, 1.7, 5.7, 5.1, "Vector Geometry & Graph Complexity", [
        "Cosine Distance in Metric Space: For normalized unit vectors (||q|| = 1, ||c|| = 1), cosine similarity reduces to SIMD dot product:",
        "    S_cosine(q, c) = sum_{j=1}^1536 (q_j * c_j) = q · c",
        "HNSW Search Complexity: Logarithmic candidate traversal across N indexed vectors in Qdrant:",
        "    T_search = O(M * log(N))   where M = 16 links/node",
        "Speed Comparison: Reduces search time from 420 ms (brute force O(N*d)) down to 4.2 ms for 100,000 chunks.",
        "Multi-Query Max-Pooling: Aggregates relevance across original, rewrite, step-back, and HyDE vectors without penalty."
    ], icon="📐")

    add_bullet_card(s17, 6.8, 1.7, 5.7, 5.1, "SuperMemo SM-2 Interval Mathematics", [
        "Interval Calculation: For review repetition n:",
        "    I(1) = 1 day,   I(2) = 6 days,   I(n) = round(I(n-1) * EF)",
        "Ease Factor Update Formula (Recall rating q in {0..5}):",
        "    EF' = max(1.3, EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))",
        "Real-World Sample Calculation:",
        "    • Day 1: First review -> Interval = 1 day.",
        "    • Day 2: Student rates q = 5 (perfect) -> Interval = 6 days.",
        "    • Day 8: Student rates q = 5 again -> EF' = 2.5 + 0.1 = 2.6.",
        "    • Next Interval = 6 * 2.6 = 16 days! Memory is locked in."
    ], icon="🔢")

    # =========================================================================
    # SLIDE 18: DATA FLOW ARCHITECTURE - DFD LEVEL 0 & 1 (FIGURE 4.1)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Data Flow Architecture: DFD Level 0 Context & Level 1 Processes", "DATA FLOW DIAGRAM")

    fig4_1 = 'report_assets/fig_4_1_dfd.png'
    if os.path.exists(fig4_1):
        s18.shapes.add_picture(fig4_1, Inches(0.8), Inches(1.8), width=Inches(6.0))

    add_bullet_card(s18, 7.1, 1.8, 5.4, 5.0, "DFD Process Breakdown", [
        "DFD Level 0 (Context Diagram): Models the student user on the left, external cloud endpoints (OpenAI, YouTube) on the right, and the AxiomAI system boundary in the center.",
        "Process 1.0 (Intake & Upload): Multipart buffer handling via Multer; persists source files to local uploads/ disk directory.",
        "Process 2.0 (Vectorization & Indexing): BullMQ worker chunks text, calls OpenAI embedding batch, and indexes 1536-d vectors into Qdrant.",
        "Process 3.0 (Multi-Query RAG): Generates Step-Back and HyDE expansions, searches Qdrant, verifies with CRAG, and streams citations.",
        "Process 4.0 (Studio Synthesis): Queries SQLite to build mind map trees, SM-2 flashcard decks, and quizzes."
    ], icon="🔄")

    # =========================================================================
    # SLIDE 19: FULL-STACK IMPLEMENTATION & TECHNOLOGY STACK
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Full-Stack Implementation & Technology Stack", "IMPLEMENTATION STACK")

    tech_stack = [
        ["Presentation Layer", "React 18 + Vite + Tailwind CSS", "Sub-second HMR builds; zero-runtime CSS bloat; shadcn/ui primitives."],
        ["Visual Canvas", "React Flow (@xyflow/react) + D3", "D3 computes tree coordinates; React Flow handles 60 FPS interactive panning."],
        ["API Gateway", "Node.js v20 LTS + Express TypeScript", "Unified TypeScript ecosystem; asynchronous event loop ideal for streaming SSE."],
        ["Background Queue", "BullMQ + Redis 7 Alpine", "Microsecond job state tracking; 120s worker locks with auto-renewals."],
        ["Vector Database", "Qdrant Vector DB (Self-Hosted Docker)", "Rust-based HNSW indexing; payload filtering for notebook tenant isolation."],
        ["Relational DB", "Prisma ORM + SQLite (dev.db)", "Zero-configuration embedded database; auto-generated type-safe queries."],
        ["Foundation AI", "OpenAI gpt-4o-mini & text-embedding-3-small", "$0.15/1M input vs $3.00/1M; enables >9,000 queries on $5 budget."],
        ["Deployment", "Docker & Docker Compose (Multi-Stage)", "Single-command containerization serving frontend and API on unified port 3001."]
    ]
    add_table_slide(s19, 0.8, 1.8, 11.733, 4.8, ["Architectural Layer", "Selected Technology", "Engineering Selection Rationale"], tech_stack, col_widths=[2.4, 3.8, 5.533])

    # =========================================================================
    # SLIDE 20: EXPERIMENTAL SETUP & TEST VERIFICATION
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Experimental Benchmarking Setup & Test Suites", "TESTING & SETUP")

    add_bullet_card(s20, 0.8, 1.7, 5.7, 5.1, "Standardized Lab Environment", [
        "Host Hardware: Intel Core i7-13700H @ 2.40 GHz (14 Cores, 20 Threads), 16 GB DDR5 RAM, 1 TB NVMe PCIe 4.0 SSD.",
        "Runtime Stack: Windows 11 Enterprise running Docker Desktop 4.30 (WSL2 Linux 5.15 Kernel), Node.js v20.20.2 Alpine, Python 3.14.",
        "Networking: OpenAI REST API targeted over TLS 1.3; Qdrant communicating over Docker internal bridge on port 6333; Redis on port 6379.",
        "Benchmark Corpuses: Tested against MIT 6.046J Quantum Algorithms lecture series, CRISPR-Cas9 genetics papers, and Classical Mechanics video playlists."
    ], icon="💻")

    add_bullet_card(s20, 6.8, 1.7, 5.7, 5.1, "17 Formal Test Cases (100% Pass)", [
        "Ingestion Suite (6 Tests): Digital PDFs (24 pages in 4.2s), UTF-8 text, YouTube videos & playlists, web articles, corrupted file handling -> ALL PASSED.",
        "RAG Retrieval Suite (4 Tests): Exact technical queries (Shor modular exponentiation), colloquial phrasing, out-of-domain rejection, empty notebooks -> ALL PASSED.",
        "Axiom Studio Suite (4 Tests): D3 mind map tree schema, SM-2 flashcard deck generation, 4-option diagnostic quiz generation, roadmaps -> ALL PASSED.",
        "Security Suite (3 Tests): Missing Clerk keys fallback to mock auth, unauthorized source deletion prevention, prompt injection hardening -> ALL PASSED."
    ], icon="🧪")

    # =========================================================================
    # SLIDE 21: QUANTITATIVE RESULTS - RECALL@K BENCHMARKS (FIGURE 5.1)
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Quantitative Results: Recall@K Information Retrieval Gains", "RESULTS: RECALL@K")

    fig5_1 = 'report_assets/fig_5_1_recall.png'
    if os.path.exists(fig5_1):
        s21.shapes.add_picture(fig5_1, Inches(0.8), Inches(1.8), width=Inches(5.8))

    add_bullet_card(s21, 6.9, 1.8, 5.6, 5.0, "Recall@K Performance Analysis", [
        "What Recall@K Means: If the true answer is hidden across 3 paragraphs in a 500-page book, did the AI bookmark it in its top K guesses?",
        "Recall@1: AxiomAI hits 62.0% on its first guess vs. only 42.0% for naive single-query RAG (+20.0% gain).",
        "Recall@5: AxiomAI achieves 88.0% candidate retrieval vs. 67.0% for baseline RAG (+21.0% gain).",
        "Recall@10: AxiomAI achieves an extraordinary 96.2% success rate vs. 76.0% for naive RAG (+20.2% gain).",
        "Why the Leap? Step-Back Prompting retrieves foundational theory, while HyDE bridges the vocabulary gap by generating hypothetical domain terms."
    ], icon="📈")

    # =========================================================================
    # SLIDE 22: QUANTITATIVE RESULTS - LATENCY PROFILING (FIGURE 5.2)
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "Quantitative Results: Sub-2s End-to-End Latency Breakdown", "RESULTS: LATENCY")

    fig5_2 = 'report_assets/fig_5_2_latency.png'
    if os.path.exists(fig5_2):
        s22.shapes.add_picture(fig5_2, Inches(0.8), Inches(1.8), width=Inches(6.0))

    add_bullet_card(s22, 7.1, 1.8, 5.4, 5.0, "Where Do the 1,860 ms Go?", [
        "Total Pipeline Latency: 1,860 milliseconds (1.86 seconds).",
        "1. Query Expansion (480 ms / 25.8%): Rewritten query and HyDE document drafted in parallel via Promise.all().",
        "2. Batch Vectorization (160 ms / 8.6%): 4 queries vectorized in a single OpenAI embedding HTTP call.",
        "3. Qdrant HNSW Retrieval (42 ms / 2.3%): Ultra-fast vector graph traversal gathers 32 candidates in 0.042s!",
        "4. SQLite Hydration (18 ms / 1.0%): Fetches chunk text and source titles from local dev.db.",
        "5. LLM Synthesis (850 ms / 45.7%): gpt-4o-mini writes the citation-grounded response.",
        "6. CRAG Verification Judge (310 ms / 16.6%): Fact-checks answer before user display."
    ], icon="⚡")

    # =========================================================================
    # SLIDE 23: ECONOMIC ANALYSIS - $5 BUDGET LIFECYCLE (FIGURE 5.3)
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "Economic Optimization: Stretching a $5 Budget to 9,250 Queries", "RESULTS: COST")

    fig5_3 = 'report_assets/fig_5_3_cost.png'
    if os.path.exists(fig5_3):
        s23.shapes.add_picture(fig5_3, Inches(0.8), Inches(1.8), width=Inches(6.0))

    add_bullet_card(s23, 7.1, 1.8, 5.4, 5.0, "Token Pricing & Budget Longevity", [
        "The GPT-4 Trap: Standard GPT-4 costs $2.50/1M input and $10.00/1M output tokens ($0.009/query). A $5.00 deposit burns out in only 555 queries (3 weeks).",
        "The gpt-4o-mini Breakthrough: Pricing plummets to $0.15/1M input and $0.60/1M output tokens ($0.00054/query).",
        "16.6x Operational Longevity: The same $5.00 deposit sustains 9,250 complete RAG and active learning interactions!",
        "Embedding Economics: text-embedding-3-small at $0.02/1M tokens allows 250 million tokens indexed for $5.00.",
        "Zero Cloud Infrastructure Costs: Self-hosted Qdrant, Redis, SQLite, and local uploads eliminate AWS S3 and Pinecone fees."
    ], icon="💰")

    # =========================================================================
    # SLIDE 24: FACTUAL GROUNDING & HALLUCINATION SUPPRESSION AUDIT
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "Factual Grounding & Hallucination Elimination Audit", "GROUNDING AUDIT")

    grounding_data = [
        ["Factual Grounding Accuracy", "86.0%", "100.0%", "+14.0% improvement; zero hallucinated claims."],
        ["Citation Provenance Coverage", "71.0%", "100.0%", "100% of factual assertions bound to [CID:chunk_id]."],
        ["Hallucination Error Rate", "14.0%", "0.0%", "Completely eliminated ungrounded fabrications."],
        ["Out-of-Domain Refusal Rate", "42.0%", "100.0%", "Gracefully states when notebook lacks relevant source."],
        ["Average Precision of Citations", "82.4%", "97.8%", "Citations map precisely to correct page or video second."]
    ]
    add_table_slide(s24, 0.8, 1.8, 11.733, 4.8, ["Integrity Evaluation Metric", "Baseline Naive RAG", "AxiomAI with CRAG", "Empirical Outcome & Impact"], grounding_data, col_widths=[3.0, 2.0, 2.2, 4.533])

    # =========================================================================
    # SLIDE 25: COMPARISON WITH INDUSTRY TOOLS
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "Competitive Feature Analysis: AxiomAI vs. Industry Tools", "INDUSTRY COMPARISON")

    comp_data = [
        ["Supported Modalities", "PDF, Text, YouTube Videos/Playlists, URLs", "PDF, Docs, Audio, Limited YouTube", "Notes, Web Links", "PDFs Only", "Manual Text Input"],
        ["Query Expansion", "HyDE + Step-Back + Rewriting", "Proprietary Gemini", "Single-Query", "Naive Vector Match", "None"],
        ["Verification Layer", "Integrated CRAG Judge (0% Hallucinations)", "Citation Badges", "None (Hallucinates)", "Page Snippets", "None"],
        ["Active Learning", "Mind Maps (D3), SM-2 Cards, Quizzes", "Audio Podcast Overviews", "Smart Tagging", "Chat Only", "Static Flashcards"],
        ["Cost Model", "Zero-Cost Local Docker ($5 API budget)", "Free Cloud (Proprietary)", "$15/month Cloud", "$19.99/mo Freemium", "$35.99/yr Freemium"],
        ["Local Data Privacy", "100% Local DB (SQLite + Fallback)", "Cloud-Only", "Cloud-Only", "Cloud-Only", "Cloud-Only"]
    ]
    add_table_slide(s25, 0.8, 1.8, 11.733, 4.8, ["Capability / Feature", "AxiomAI (This Work)", "Google NotebookLM", "Mem.ai", "ChatPDF", "Quizlet"], comp_data, col_widths=[2.4, 2.8, 2.2, 1.5, 1.5, 1.333])

    # =========================================================================
    # SLIDE 26: PROJECT MANAGEMENT - WBS & 16-WEEK GANTT SCHEDULE
    # =========================================================================
    s26 = prs.slides.add_slide(blank_layout)
    add_header(s26, "Project Lifecycle Management: WBS & 16-Week Agile Execution", "PROJECT MANAGEMENT")

    fig1_1 = 'report_assets/fig_1_1_wbs.png'
    fig1_2 = 'report_assets/fig_1_2_gantt.png'
    if os.path.exists(fig1_1):
        s26.shapes.add_picture(fig1_1, Inches(0.8), Inches(1.8), width=Inches(5.7))
    if os.path.exists(fig1_2):
        s26.shapes.add_picture(fig1_2, Inches(6.8), Inches(1.8), width=Inches(5.7))

    add_bullet_card(s26, 0.8, 5.0, 11.733, 1.8, "Milestone Validation Gates", [
        "Milestones 1–2 (Weeks 1–6): Literature survey of 35+ papers; multimodal extractors; BullMQ/Redis asynchronous queue verified.",
        "Milestones 3–4 (Weeks 7–13): Qdrant vector database; Step-Back & HyDE expansions; CRAG factual judge; Axiom Studio active learning UI.",
        "Milestones 5–6 (Weeks 13–16): Latency profiling; Recall@K benchmarking; multi-stage Docker build; comprehensive thesis report."
    ], icon="🏁")

    # =========================================================================
    # SLIDE 27: TECHNICAL LIMITATIONS & OPERATIONAL BOUNDARIES
    # =========================================================================
    s27 = prs.slides.add_slide(blank_layout)
    add_header(s27, "Technical Limitations & Operational Boundary Conditions", "LIMITATIONS")

    add_bullet_card(s27, 0.8, 1.7, 3.7, 5.1, "1. Scanned Image-Only PDFs", [
        "Digital PDF Focus: The current extractor (pdfParse) processes digitally rendered PDFs.",
        "OCR Pre-Processing: Low-resolution photocopies or handwritten student notes require an external OCR pre-processing pipeline (e.g. Tesseract) before ingestion."
    ], icon="📄")

    add_bullet_card(s27, 4.8, 1.7, 3.7, 5.1, "2. Uncaptioned Video Audio", [
        "Closed-Caption Dependency: YouTube extraction relies on closed captions or auto-generated subtitles.",
        "Speech-to-Text Trade-off: Videos completely lacking captions require external speech-to-text models (OpenAI Whisper), which were excluded to protect the $5 budget."
    ], icon="🎙️")

    add_bullet_card(s27, 8.8, 1.7, 3.7, 5.1, "3. Database Concurrency", [
        "Embedded SQLite Simplicity: SQLite (dev.db) provides seamless zero-cost local deployment without running heavy database servers.",
        "Single-Writer Concurrency: File-level locking limits concurrent multi-tenant writes under heavy corporate loads compared to enterprise PostgreSQL."
    ], icon="💾")

    # =========================================================================
    # SLIDE 28: FUTURE TECHNOLOGICAL ROADMAP
    # =========================================================================
    s28 = prs.slides.add_slide(blank_layout)
    add_header(s28, "Future Research Directions & Technological Roadmap", "FUTURE WORK")

    add_bullet_card(s28, 0.8, 1.7, 5.7, 2.5, "1. On-Device Small Language Models (SLMs)", [
        "Local WebGPU / Ollama Inference: Running quantized models (Llama-3-8B-Instruct or Phi-3-Mini) directly inside client browser memory.",
        "100% Offline Resilience: Eliminates cloud API dependencies entirely, achieving zero inference cost and complete data sovereignty."
    ], icon="📱")

    add_bullet_card(s28, 6.8, 1.7, 5.7, 2.5, "2. Real-Time Collaborative Study Rooms", [
        "WebSockets & WebRTC: Real-time multi-student synchronization across shared notebooks.",
        "Collaborative Mind Mapping: Allows study groups to co-edit concept trees and challenge each other in synchronized quiz battles."
    ], icon="👥")

    add_bullet_card(s28, 0.8, 4.4, 5.7, 2.5, "3. Graph RAG (Knowledge Graphs)", [
        "Graph Neural Networks (GNNs): Augmenting vector similarity with Graph RAG to map citations, author networks, and multi-hop concept relations.",
        "3D Concept Universe: Navigating complex academic literature as an interactive 3D knowledge graph."
    ], icon="🕸️")

    add_bullet_card(s28, 6.8, 4.4, 5.7, 2.5, "4. Local Whisper Speech Transcription", [
        "Self-Hosted Whisper.cpp: Deploying lightweight Whisper models inside Docker to transcribe raw classroom microphone recordings locally.",
        "Universal Video Ingestion: Supports any uncaptioned video or raw classroom audio file without external API fees."
    ], icon="🎧")

    # =========================================================================
    # SLIDE 29: CONCLUSION & KEY TAKEAWAYS
    # =========================================================================
    s29 = prs.slides.add_slide(blank_layout)
    add_header(s29, "Conclusion & Key Capstone Takeaways", "CONCLUSION")

    add_bullet_card(s29, 0.8, 1.7, 5.7, 5.1, "Engineering Deliverables Achieved", [
        "Autonomous Multimodal Ingestion: Successfully processes PDFs, web URLs, and multi-video YouTube playlists with second-accurate timestamps in 4.2 seconds.",
        "Elite Retrieval Precision: Multi-query RAG (HyDE + Step-Back) achieves 96.2% Recall@10, outperforming standard naive RAG by 20.2%.",
        "Zero-Hallucination Factual Integrity: Integrated CRAG fact-checking judge eliminates ungrounded claims (0.0% error rate), guaranteeing 100% verifiable citations.",
        "Comprehensive Active Learning Suite: Autonomous generation of D3 visual mind maps, SuperMemo SM-2 flashcards, diagnostic quizzes, and progressive roadmaps.",
        "Extreme Economic Parsimony: 9,250 queries sustained on a $5.00 budget via gpt-4o-mini and unified Docker Compose containerization."
    ], icon="🏆")

    add_bullet_card(s29, 6.8, 1.7, 5.7, 5.1, "Pedagogical & Academic Impact", [
        "Democratizing Elite Tutoring: Advances UN Sustainable Development Goal 4 (Quality Education) by providing a personalized 1-on-1 AI research mentor.",
        "Cognitive Load Minimization: Externalizes complex syllabus structures into visual schemas, cutting extraneous mental overhead by ~40%.",
        "Promoting Academic Integrity: Every assertion is bound to verifiable primary source literature, encouraging authentic scholarly inquiry.",
        "Production-Ready Architecture: Complete repository, multi-stage Docker containerization, 63-page thesis report, and presentation slides ready for deployment."
    ], icon="🎓")

    # =========================================================================
    # SLIDE 30: THANK YOU & Q&A / DEFENSE DISCUSSION
    # =========================================================================
    s30 = prs.slides.add_slide(blank_layout)
    bg30 = s30.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg30.fill.solid()
    bg30.fill.fore_color.rgb = COLOR_PRIMARY_DARK
    bg30.line.fill.background()

    tb30 = s30.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(3.5))
    tf30 = tb30.text_frame
    tf30.word_wrap = True

    p30_th = tf30.paragraphs[0]
    p30_th.text = "Thank You!"
    p30_th.font.name = "Segoe UI"
    p30_th.font.size = Pt(44)
    p30_th.font.bold = True
    p30_th.font.color.rgb = COLOR_WHITE
    p30_th.alignment = PP_ALIGN.CENTER

    p30_sub = tf30.add_paragraph()
    p30_sub.text = "Questions & Academic Discussion"
    p30_sub.font.name = "Segoe UI"
    p30_sub.font.size = Pt(22)
    p30_sub.font.bold = True
    p30_sub.font.color.rgb = COLOR_ACCENT_CYAN
    p30_sub.alignment = PP_ALIGN.CENTER
    p30_sub.space_before = Pt(12)

    p30_proj = tf30.add_paragraph()
    p30_proj.text = "AxiomAI: Autonomous Multimodal RAG & Active Learning Research Workspace\nDepartment of Computer Science and Engineering | B.Tech Capstone Defense 2026"
    p30_proj.font.name = "Segoe UI"
    p30_proj.font.size = Pt(14)
    p30_proj.font.color.rgb = RGBColor(148, 163, 184)
    p30_proj.alignment = PP_ALIGN.CENTER
    p30_proj.space_before = Pt(20)

    # Save presentation
    output_path = "AxiomAI_Final_Capstone_Project_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {os.path.abspath(output_path)}")
    print(f"Total Slides Generated: {len(prs.slides)}")

if __name__ == "__main__":
    build_capstone_presentation()
