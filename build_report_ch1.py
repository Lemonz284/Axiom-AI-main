from report_helper import (
    add_heading_1, add_heading_2, add_heading_3,
    add_body_p, add_bullet_p, add_figure, create_academic_table, add_callout_box
)

def build_chapter_1(doc):
    add_heading_1(doc, "CHAPTER 1: INTRODUCTION")

    # 1.1 Background
    add_heading_2(doc, "1.1 Background: Motivation and Technological Need")
    add_body_p(doc, "In the modern digital era, the landscape of higher education, scientific research, and engineering studies has undergone a monumental paradigm shift. The primary challenge confronting university students, academic scholars, and corporate researchers is no longer the scarcity of educational information, but rather its overwhelming superabundance and severe structural fragmentation. Contemporary university students routinely interact with highly heterogeneous, multimodal knowledge repositories across a wide spectrum of digital formats: academic textbooks and peer-reviewed research papers distributed as Portable Document Format (PDF) files; digital lecture notes and plain text documentations; unstructured online web publications and encyclopedia articles; and multimedia video repositories—most notably multi-hour academic lecture playlists hosted on platforms such as YouTube.")
    add_body_p(doc, "Despite the unprecedented accessibility of these learning materials, the human cognitive architecture possesses finite working memory capacity, a fundamental psychological principle formalized by John Sweller's Cognitive Load Theory. When students are forced to constantly juggle multiple browser tabs, search through multi-hundred-page research monographs for specific mathematical derivations, and scrub through lengthy video timelines to locate precise instructor explanations, their mental bandwidth is consumed by extraneous cognitive overhead rather than germane schema acquisition. The resulting cognitive fragmentation impedes deep conceptual synthesis, exacerbates academic fatigue, and leads to superficial learning patterns.")
    
    add_callout_box(doc, "The Core Problem in Plain English: Digital Information Overload",
                    "Imagine a student studying for an advanced exam in Quantum Computing. Their professor assigned a 400-page textbook PDF, 15 scientific research papers, and a YouTube playlist containing 20 hours of lectures. When the student has a specific question—such as 'How does Shor's algorithm find the period of a function?'—they must manually open five different PDF viewers, search for keywords, and scrub through hours of video timelines. Instead of spending their mental energy understanding quantum physics, 80% of their energy is wasted hunting for information across disorganized files. AxiomAI was built to solve this exact problem: it acts as an intelligent, unified digital research companion that reads all those textbooks, papers, and video lectures simultaneously, allowing the student to ask questions in plain English and receive instant, verifiable answers with exact page numbers and video timestamps.")

    add_body_p(doc, "While the recent emergence of generative Large Language Models (LLMs) such as OpenAI's GPT-4 has demonstrated remarkable linguistic fluencies and general-purpose reasoning capabilities, their off-the-shelf application to rigorous academic learning presents catastrophic vulnerabilities. Primary among these limitations is the pervasive phenomenon of artificial intelligence hallucinations—wherein models generate fabricated citations, incorrect mathematical formulas, and counter-factual statements with high rhetorical confidence. Furthermore, frontier commercial foundation models operate on closed parameter weights with rigid knowledge cutoff dates, possessing zero native awareness of specialized student coursework, localized institution syllabi, or newly uploaded laboratory research reports.")
    add_body_p(doc, "Retrieval-Augmented Generation (RAG) has surfaced as the preeminent architectural paradigm to bridge the gap between parametric LLM intelligence and non-parametric external knowledge bases. However, conventional 'naive' RAG implementations exhibit severe structural frailties when subjected to real-world educational workloads: (1) single-vector keyword searches fail to capture complex semantic intents when students phrase queries colloquially; (2) document chunking mechanisms routinely sever sentences across arbitrary token boundaries, discarding crucial context; (3) heterogeneous multi-source retrieval tends to be monopolized by large, dense documents, completely starving out shorter video transcripts or targeted web summaries; and (4) conventional RAG tools operate merely as passive question-answering engines, failing to transform retrieved knowledge into active learning artifacts such as concept maps, spaced repetition flashcards, or self-assessment quizzes.")
    add_body_p(doc, "This capstone project is motivated by the urgent necessity to engineer an autonomous, multimodal, enterprise-grade research and active learning workspace—named AxiomAI. By synergizing advanced multi-query expansion (Step-Back Abstraction Prompting and Hypothetical Document Embeddings), high-performance vector indexing via Qdrant, asynchronous distributed ingestion via BullMQ and Redis, and an integrated Corrective RAG (CRAG) factual verification judge, AxiomAI establishes an end-to-end framework that not only delivers verifiable, citation-grounded research synthesis, but actively transforms static study materials into interactive, visual learning environments.")

    # 1.2 Problem Definition and Objectives
    add_heading_2(doc, "1.2 Problem Definition and Engineering Objectives")
    add_body_p(doc, "Formal Problem Definition: Given an arbitrary collection of multimodal, uncurated academic research sources S = {s_1, s_2, ..., s_n} encompassing text files, complex scientific PDFs, web URLs, and multi-part YouTube lecture video playlists, engineer an autonomous, resilient, and containerized computational pipeline capable of asynchronously ingesting, chunking, and indexing heterogeneous media into a high-dimensional vector space, executing sub-two-second multi-query semantic retrieval with zero ungrounded hallucinations, and programmatically synthesizing hierarchical active learning structures without human intervention.")
    add_body_p(doc, "To achieve a rigorous, verifiable solution to this technical challenge, the capstone project establishes five clear, measurable engineering objectives:")
    add_bullet_p(doc, "Objective 1: Multimodal Asynchronous Ingestion Engine — Engineer a distributed background queue architecture (BullMQ + Redis) capable of ingesting and extracting text from PDFs, web articles, and YouTube video playlists with second-by-second timestamp synchronization, achieving an average ingestion and indexing throughput of under 10 seconds for standard academic papers (up to 30 pages) without blocking the client interface.", bold_prefix="1. Multimodal Ingestion Throughput: ")
    add_bullet_p(doc, "Objective 2: Advanced Multi-Query Retrieval Accuracy — Design and implement an advanced RAG retrieval pipeline incorporating semantic query rewriting, Step-Back Abstraction Prompting, and Hypothetical Document Embeddings (HyDE) that achieves a minimum Information Retrieval Recall@10 of greater than 90% across challenging domain-specific academic queries, outperforming standard naive RAG by at least 15%.", bold_prefix="2. Retrieval Recall & Precision: ")
    add_bullet_p(doc, "Objective 3: Zero-Hallucination Factual Grounding — Integrate a dual-phase Corrective RAG (CRAG) verification judge that rigorously audits synthesized LLM answers against retrieved source context, guaranteeing that 100% of factual assertions contain precise, clickable inline chunk citations ([CID:chunk_id]) mapping to exact PDF page numbers or video timestamp coordinates.", bold_prefix="3. Factual Grounding & Verification: ")
    add_bullet_p(doc, "Objective 4: Autonomous Active Learning Synthesis — Implement the Axiom Studio module to programmatically generate interactive, visual educational artifacts directly from indexed source texts: (a) hierarchical mind maps calculated using D3 layout geometry and rendered on a React Flow canvas; (b) spaced-repetition flashcards conforming to the SuperMemo SM-2 algorithmic model; (c) four-option diagnostic quizzes with complete distractor rationales; and (d) structured, step-by-step learning roadmaps.", bold_prefix="4. Active Learning Generation: ")
    add_bullet_p(doc, "Objective 5: Resource Efficiency and Zero-Cost Local Resilience — Containerize the full-stack system within a unified Docker Compose topology, ensuring seamless deployment on standard consumer hardware, providing an offline fallback mode (SQLite and mock authentication), and optimizing all cloud LLM calls to gpt-4o-mini to operate sustainably within a lifetime capstone budget of $5.00 USD across thousands of queries.", bold_prefix="5. Economic & Architectural Viability: ")

    # 1.3 Social & Environmental Relevance
    add_heading_2(doc, "1.3 Social, Educational, and Environmental Relevance")
    add_body_p(doc, "The development of AxiomAI carries profound societal, pedagogical, and environmental implications. From an educational equity perspective, personalized 1-on-1 tutoring has long been recognized by educational psychologists (such as Benjamin Bloom's Two Sigma Problem) as the gold standard of instructional efficacy. However, personalized human tutoring remains economically prohibitive for millions of students globally. By providing an autonomous AI research companion that can ingest any curriculum, explain complex concepts with mathematical rigor, and generate customized quizzes and flashcards tailored to an individual student's syllabus, AxiomAI democratizes access to elite educational tutoring, directly advancing United Nations Sustainable Development Goal 4 (Quality Education).")
    add_body_p(doc, "From an ethical and academic integrity standpoint, mainstream AI tools frequently encourage intellectual laziness and academic dishonesty by generating unverified, non-attributed text that students copy blindly. In contrast, AxiomAI enforces strict citation provenance: every generated assertion is explicitly tethered to an underlying document chunk or video timestamp. Students are not insulated from their reading material; rather, AxiomAI acts as an intelligent index that navigates students directly into the original academic literature, fostering critical thinking, literature verification, and scholarly rigor.")
    add_body_p(doc, "From an environmental sustainability perspective, the exponential expansion of massive frontier AI models (such as GPT-4, Gemini Ultra, and Claude Opus) consumes exorbitant electrical power and cooling water in hyperscale data centers, contributing significantly to global carbon emissions. A key design principle of AxiomAI is computational parsimony: by employing sophisticated algorithmic scaffolding—namely HyDE, Step-Back Prompting, and Qdrant vector filtering—AxiomAI achieves state-of-the-art retrieval accuracy while routing inference to gpt-4o-mini, a compact, highly optimized model requiring a fraction of the computational wattage of monolithic frontier architectures. This ensures that the system's operational carbon footprint remains minimal, adhering to Green Computing principles.")

    # 1.4 Project Plan
    add_heading_2(doc, "1.4 Project Plan and Execution Methodology")
    add_body_p(doc, "The AxiomAI capstone engineering lifecycle was structured across a 16-week rigorous timeline, organized into five core functional work streams: Requirements & Literature Analysis, Multimodal Ingestion Engineering, Advanced RAG Query Engine Development, Axiom Studio Active Learning Implementation, and System Evaluation & Containerized Deployment.")

    # 1.4.1 Work Breakdown Structure
    add_heading_3(doc, "1.4.1 Work Breakdown Structure (WBS)")
    add_body_p(doc, "The Work Breakdown Structure hierarchically decomposes the project into manageable engineering deliverables, illustrated in Figure 1.1 and detailed in Table 1.1.")
    
    add_figure(doc, 'report_assets/fig_1_1_wbs.png', "Figure 1.1: Work Breakdown Structure (WBS) Tree of AxiomAI System", width_inches=6.0)

    add_callout_box(doc, "Understanding Figure 1.1: The Work Breakdown Structure Explained",
                    "Figure 1.1 represents the complete engineering blueprint of AxiomAI broken down into five distinct branches:\n"
                    "• Tier 1.0 (Requirements & Research): The foundation where we evaluated vector databases (comparing Pinecone, Chroma, and Qdrant) and finalized mathematical retrieval formulas.\n"
                    "• Tier 2.0 (Multimodal Ingestion): The engine responsible for swallowing any file type (PDFs, text files, YouTube video transcripts, and web articles) and cutting them into clean 1,000-character chunks.\n"
                    "• Tier 3.0 (Advanced RAG Engine): The brain of the search system, combining Step-Back Prompting, HyDE hypothetical answers, and a Fact-Checking Judge (CRAG).\n"
                    "• Tier 4.0 (Axiom Studio Suite): The educational workshop that automatically creates visual Mind Maps, Spaced Repetition Flashcards, and Practice Quizzes.\n"
                    "• Tier 5.0 (Evaluation & Deploy): The final packaging phase where the system was benchmarked, optimized to run within a $5 budget, and wrapped inside a single Docker container.")

    wbs_data = [
        ["1.0 Requirements & Research", "1.1 Domain Analysis\n1.2 Technology Selection\n1.3 Formal System Specs", "Literature review of RAG architectures; trade-off evaluation between Pinecone, Chroma, and Qdrant; mathematical modeling of vector search."],
        ["2.0 Multimodal Ingestion", "2.1 PDF/Text Engine\n2.2 YouTube VTT Extractor\n2.3 Sliding Chunker & S3", "Building PDF parser, YouTube transcript synchronization module, regex-based sliding window chunker, and local S3 fallback storage."],
        ["3.0 Advanced RAG Engine", "3.1 Multi-Query Expansion\n3.2 Qdrant Hybrid Search\n3.3 CRAG Verification Judge", "Implementing HyDE, Step-Back Abstraction, batch embedding vectorization, multi-source re-ranking, and CRAG factual auditing judge."],
        ["4.0 Axiom Studio Suite", "4.1 D3 Mind Map Engine\n4.2 Flashcard SM-2 Module\n4.3 Diagnostic Quizzes\n4.4 Learning Roadmaps", "Developing D3 hierarchical graph layouts on React Flow canvas, SuperMemo SM-2 spaced repetition logic, 4-option quiz generator, and curricula roadmaps."],
        ["5.0 Evaluation & Deploy", "5.1 Empirical Benchmarking\n5.2 Docker Containerization\n5.3 Academic Documentation", "Conducting Recall@K tests, latency profiling, cost optimization under $5 budget, multi-stage Dockerfile construction, and final report compilation."]
    ]
    create_academic_table(doc, ["WBS Tier 1 Component", "Sub-Modules & Deliverables", "Engineering Scope & Activity Description"], wbs_data, col_widths=[1.8, 1.8, 3.2])

    # 1.4.2 Timeline
    add_heading_3(doc, "1.4.2 Project Schedule and Milestone Timeline")
    add_body_p(doc, "The project implementation followed an agile development framework across sixteen academic weeks. Figure 1.2 displays the project milestone Gantt chart, while Table 1.2 summarizes the execution schedule and milestone validation gates.")

    add_figure(doc, 'report_assets/fig_1_2_gantt.png', "Figure 1.2: Project Implementation Schedule and Milestone Gantt Chart", width_inches=6.0)

    add_callout_box(doc, "Understanding Figure 1.2: Milestone Schedule and Risk Prevention",
                    "Figure 1.2 charts our 16-week journey from initial research to working deployment. Notice how the phases overlap intentionally: while the multimodal ingestion engine was being finalized in Weeks 3–6, work on the vector database setup began in parallel in Week 7. This overlapping 'agile sprint' strategy ensured that if one component ran into a technical hurdle (such as changes to YouTube's transcript format), the rest of the project continued progressing smoothly without stalling.")

    milestone_data = [
        ["Milestone 1", "Weeks 1 - 4", "Problem Identification & Literature Review", "Completed comprehensive survey of 35+ papers; finalized system requirements specification and mathematical model."],
        ["Milestone 2", "Weeks 3 - 6", "System Architecture & Ingestion Prototyping", "Implemented multimodal extractors (PDF, Text, YouTube); configured BullMQ and Redis; verified asynchronous job lifecycle."],
        ["Milestone 3", "Weeks 7 - 10", "Vector Database Setup & Core RAG Pipeline", "Deployed Qdrant vector database; implemented Step-Back and HyDE query expansions; established baseline vector search."],
        ["Milestone 4", "Weeks 9 - 13", "CRAG Verification & Axiom Studio Modules", "Integrated Corrective RAG evaluation judge; engineered D3 Mind Map canvas, SM-2 flashcard generator, and quiz engine."],
        ["Milestone 5", "Weeks 13 - 15", "Benchmarking, Optimization & Dockerization", "Conducted latency profiling and Recall@K testing; optimized model parameters to gpt-4o-mini; constructed multi-stage Docker build."],
        ["Milestone 6", "Weeks 15 - 16", "Final Verification, Defense & Documentation", "Completed end-to-end integration tests; verified 100% citation accuracy; assembled final capstone thesis report."]
    ]
    create_academic_table(doc, ["Milestone ID", "Academic Period", "Key Deliverable / Phase", "Validation Criteria & Outcomes Achieved"], milestone_data, col_widths=[1.2, 1.3, 2.0, 2.5])

    # 1.4.3 Roles and responsibilities
    add_heading_3(doc, "1.4.3 Team Roles and Technical Responsibilities")
    add_body_p(doc, "To ensure accountability and seamless inter-module cohesion, technical responsibilities were partitioned systematically among the three capstone research team members based on specialized domain competencies:")
    add_bullet_p(doc, "Student A (Lead Systems Architect & Backend Engineer): Responsible for core Express server design, TypeScript API gateway, BullMQ asynchronous queue integration, Redis broker management, Prisma relational database modeling, and multi-stage Docker containerization orchestration.", bold_prefix="Student A: ")
    add_bullet_p(doc, "Student B (AI & Information Retrieval Specialist): Responsible for the end-to-end RAG architecture, Qdrant vector database configuration, mathematical formulation of metric space search, Step-Back and HyDE prompt engineering, Corrective RAG verification judge design, and empirical Recall@K benchmarking.", bold_prefix="Student B: ")
    add_bullet_p(doc, "Student C (Frontend & Active Learning Visualization Engineer): Responsible for the React 18 Single Page Application, shadcn/ui visual architecture, D3 hierarchy mathematical layout integration on React Flow canvas, SuperMemo SM-2 spaced repetition UI, and client-side citation interaction handlers.", bold_prefix="Student C: ")

    # 1.4.4 Challenges and risk management
    add_heading_3(doc, "1.4.4 Risk Assessment and Engineering Mitigation Management")
    add_body_p(doc, "Throughout the system engineering lifecycle, several significant technological, operational, and algorithmic risks were identified. Table 1.3 outlines the proactive risk management matrix implemented to ensure continuous system reliability.")

    risk_data = [
        ["API Rate Limits & Cost Exhaustion", "High", "High", "Implemented token-efficient prompt structures; transitioned all model calls to gpt-4o-mini; introduced in-memory deterministic fallback vectors."],
        ["YouTube Transcript Scraping Failures", "Medium", "High", "Engineered multi-layered fallback: Supadata API primary tier, youtube-transcript secondary tier, and graceful placeholder error extraction."],
        ["Redis / Queue Service Outages", "Medium", "Medium", "Programmed graceful offline error handlers; if Redis is down, server executes ingestion directly in-process via fallback async routines."],
        ["Vector Database Memory Overhead", "Low", "Medium", "Engineered an in-memory cosine similarity fallback Map; configured Qdrant collection payload indexing for isolated tenant namespaces."],
        ["Hallucinations in Complex STEM Queries", "High", "Critical", "Introduced secondary CRAG evaluation judge that validates generated text against retrieved context before returning answers to the user."]
    ]
    create_academic_table(doc, ["Identified Risk Factor", "Probability", "Severity", "Engineering Mitigation & Fallback Strategy"], risk_data, col_widths=[1.8, 1.0, 1.0, 3.0])

    # 1.5 Scope and Limitations
    add_heading_2(doc, "1.5 Scope and System Boundaries")
    add_body_p(doc, "The scope of the AxiomAI system encompasses the end-to-end processing of educational research materials. Specifically, the system is designed to support:")
    add_bullet_p(doc, "Document Ingestion: Native PDF parsing (text extraction, page mapping), UTF-8 plain text files, web page articles via DOM Readability, and YouTube video/playlist transcripts with synchronized second-based timestamps.")
    add_bullet_p(doc, "Semantic Retrieval: Advanced multi-query expansion using Step-Back Prompting, HyDE, and query rewriting, mapped to 1536-dimensional embeddings with HNSW cosine distance search.")
    add_bullet_p(doc, "Grounded Question Answering: Interactive conversational RAG with strict inline chunk ID citations, verifiable against source documents.")
    add_bullet_p(doc, "Active Learning Generation: Autonomous creation of D3-rendered mind maps, spaced repetition flashcard decks, multiple-choice quizzes, and structured learning roadmaps.")
    add_bullet_p(doc, "Deployment: Fully containerized multi-container Docker Compose deployment with local SQLite persistence and mock user authentication.")
    add_body_p(doc, "Explicit System Limitations and Boundary Conditions:")
    add_bullet_p(doc, "Optical Character Recognition (OCR): The current ingestion pipeline processes digitally rendered PDFs. Scanned image-only PDFs or low-resolution handwritten student notes require external OCR pre-processing.", bold_prefix="1. OCR Limitations: ")
    add_bullet_p(doc, "Live Audio Transcription: Videos without pre-existing closed captions or auto-generated subtitles require external speech-to-text transcription APIs (e.g., OpenAI Whisper), which were excluded to preserve the zero-cost local architecture.", bold_prefix="2. Audio Processing: ")
    add_bullet_p(doc, "Context Window Constraints: Highly dense textbooks exceeding 500 pages are subject to sliding-window truncation during whole-notebook overview synthesis, prioritizing the top 35,000 characters per source.", bold_prefix="3. Context Window Bounds: ")

    doc.add_page_break()

print("Chapter 1 builder updated successfully.")
