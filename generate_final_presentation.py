import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# Color Palette (Modern Executive / Tech Clean)
# -------------------------------------------------------------
COLOR_PRIMARY_DARK = RGBColor(15, 23, 42)      # Slate 900
COLOR_NAVY = RGBColor(30, 41, 59)              # Slate 800
COLOR_ACCENT = RGBColor(37, 99, 235)           # Blue 600
COLOR_ACCENT_LIGHT = RGBColor(239, 246, 255)   # Blue 50
COLOR_ACCENT_CYAN = RGBColor(14, 165, 233)     # Sky 500
COLOR_TEXT_MAIN = RGBColor(30, 41, 59)         # Slate 800
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)     # Slate 500
COLOR_BG_LIGHT = RGBColor(248, 250, 252)       # Slate 50
COLOR_CARD_BG = RGBColor(255, 255, 255)        # Pure White
COLOR_CARD_BORDER = RGBColor(226, 232, 240)    # Slate 200
COLOR_HIGHLIGHT_GREEN = RGBColor(22, 163, 74)  # Green 600
COLOR_WHITE = RGBColor(255, 255, 255)

def create_base_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def add_header(slide, title_text, category_text="AXIOMAI CAPSTONE PROJECT"):
    """Adds a standardized clean header banner and footer to a content slide"""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG_LIGHT
    bg.line.fill.background()

    if category_text:
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.32))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Segoe UI"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT

    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.6))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_PRIMARY_DARK

    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_CARD_BORDER
    div.line.fill.background()

    f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.733), Inches(0.3))
    tf_f = f_box.text_frame
    tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = "AxiomAI: AI-Powered Multimodal Learning Workspace | JIIT Noida Capstone Defense 2026-2027"
    p_f.font.name = "Segoe UI"
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = COLOR_TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_content_card(slide, left, top, width, height, title, items, icon="🔹", bg_color=COLOR_CARD_BG):
    """Draws a card containing a title and bullet items with bold prefix support"""
    add_card(slide, left, top, width, height, bg_color)
    tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.22), Inches(width - 0.5), Inches(height - 0.44))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    if title:
        p_t = tf.paragraphs[0]
        p_t.text = f"{icon}  {title}" if icon else title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY_DARK
        p_t.space_after = Pt(8)
    
    for idx, item in enumerate(items):
        p = tf.add_paragraph() if (title or idx > 0) else tf.paragraphs[0]
        p.space_after = Pt(6)
        if ":" in item:
            prefix, body = item.split(":", 1)
            r_pre = p.add_run()
            r_pre.text = f"• {prefix.strip()}: "
            r_pre.font.name = "Segoe UI"
            r_pre.font.size = Pt(10.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_PRIMARY_DARK

            r_bod = p.add_run()
            r_bod.text = body.strip()
            r_bod.font.name = "Segoe UI"
            r_bod.font.size = Pt(10.5)
            r_bod.font.color.rgb = COLOR_TEXT_MAIN
        else:
            r = p.add_run()
            r.text = f"• {item}"
            r.font.name = "Segoe UI"
            r.font.size = Pt(10.5)
            r.font.color.rgb = COLOR_TEXT_MAIN

def generate_presentation():
    print("Generating refined 17-slide AxiomAI presentation...")
    prs = create_base_presentation()
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Executive Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_PRIMARY_DARK
    bg1.line.fill.background()

    # Pill badge
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.85), Inches(5.6), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 41, 59)
    pill.line.color.rgb = COLOR_ACCENT_CYAN
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = "MAJOR PROJECT DEFENSE | B.TECH CSE (2026–2027)"
    p_pill.font.name = "Segoe UI"
    p_pill.font.size = Pt(10.5)
    p_pill.font.bold = True
    p_pill.font.color.rgb = COLOR_ACCENT_CYAN
    p_pill.alignment = PP_ALIGN.CENTER

    # Main Title
    t_box1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(2.2))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "AxiomAI: AI-Powered Multimodal\nLearning Workspace"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Transforming Complex Course Documents & Lecture Videos into an Interactive, Grounded Study Hub"
    p1_sub.font.name = "Segoe UI"
    p1_sub.font.size = Pt(16)
    p1_sub.font.color.rgb = RGBColor(148, 163, 184)
    p1_sub.space_before = Pt(10)

    # Student Team Card
    c_team = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.5), Inches(5.4), Inches(2.2))
    c_team.fill.solid()
    c_team.fill.fore_color.rgb = RGBColor(30, 41, 59)
    c_team.line.color.rgb = RGBColor(51, 65, 85)
    tf_team = c_team.text_frame
    p_th = tf_team.paragraphs[0]
    p_th.text = "STUDENT PROJECT TEAM"
    p_th.font.name = "Segoe UI"
    p_th.font.size = Pt(11)
    p_th.font.bold = True
    p_th.font.color.rgb = COLOR_ACCENT_CYAN
    p_th.space_after = Pt(8)

    students = [
        "Uttkarsh Thakur (Enrollment: 9923103196)",
        "Ayush Singh (Enrollment: 9923103193)",
        "B.Tech Computer Science & Engineering (4th Year, 7th Sem)"
    ]
    for s in students:
        p = tf_team.add_paragraph()
        p.text = f"• {s}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    # Supervisor & Institute Card
    c_guide = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(4.5), Inches(5.4), Inches(2.2))
    c_guide.fill.solid()
    c_guide.fill.fore_color.rgb = RGBColor(30, 41, 59)
    c_guide.line.color.rgb = RGBColor(51, 65, 85)
    tf_guide = c_guide.text_frame
    p_gh = tf_guide.paragraphs[0]
    p_gh.text = "ACADEMIC SUPERVISION & INSTITUTION"
    p_gh.font.name = "Segoe UI"
    p_gh.font.size = Pt(11)
    p_gh.font.bold = True
    p_gh.font.color.rgb = COLOR_ACCENT_CYAN
    p_gh.space_after = Pt(8)

    guide_info = [
        "Project Supervisor: Mr. Twinkle Tyagi, Assistant Professor",
        "Department of Computer Science & Engineering and IT",
        "Jaypee Institute of Information Technology (JIIT), Noida"
    ]
    for g in guide_info:
        p = tf_guide.add_paragraph()
        p.text = f"• {g}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 2: PROJECT OVERVIEW & VISION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Project Overview: What is AxiomAI?", "PROJECT INTRODUCTION")

    # Banner
    add_card(s2, 0.8, 1.6, 11.733, 1.1, bg_color=COLOR_ACCENT_LIGHT, border_color=COLOR_ACCENT)
    tb_b = s2.shapes.add_textbox(Inches(1.05), Inches(1.72), Inches(11.2), Inches(0.85))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p_bv = tf_b.paragraphs[0]
    p_bv.text = "AxiomAI is an autonomous, full-stack learning platform engineered to help university students conquer complex study materials by synthesizing Retrieval-Augmented Generation (RAG) with cognitive active study tools."
    p_bv.font.name = "Segoe UI"
    p_bv.font.size = Pt(12.5)
    p_bv.font.color.rgb = COLOR_NAVY

    # 3 Pillar Cards
    pillars = [
        ("Multimodal Ingestion", [
            "Universal Content Support: Ingests academic PDFs, research papers, lecture slides, and complete YouTube playlists.",
            "Timestamp Synchronization: Transcribes YouTube video lectures with second-by-second clickable timestamps.",
            "Asynchronous Processing: Background queue handles large files smoothly without UI freezing."
        ], "📁"),
        ("Grounded Factual Q&A", [
            "Zero Hallucination: Restricts AI responses strictly to content present in the uploaded materials.",
            "Inline Citations: Every single answer includes clickable reference tags [CID:chunk_id].",
            "Instant Provenance: Clicking any citation displays the original source paragraph or jumps to the video frame."
        ], "🔍"),
        ("Axiom Study Studio", [
            "Visual Mind Maps: Generates interactive hierarchical concept trees for visual learning.",
            "Active Recall Quizzes: Creates diagnostic multiple-choice questions with full explanations.",
            "Spaced Repetition: Generates flashcards with memory retention algorithms (SuperMemo SM-2)."
        ], "🧠")
    ]
    card_w = 3.7
    for idx, (title, items, icon) in enumerate(pillars):
        add_content_card(s2, 0.8 + idx * 4.02, 2.9, card_w, 3.85, title, items, icon=icon)

    # =========================================================================
    # SLIDE 3: THE PROBLEM STATEMENT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Problem: Challenges in Modern University Learning", "PROBLEM DEFINITION")

    problems = [
        ("Information Overload & Fragmentation", [
            "Multi-Platform Chaos: Students juggle textbooks, lecture PDFs, slides, and multi-hour YouTube playlists across disconnected browser tabs.",
            "High Search Friction: Finding a specific definition or equation across 500-page textbooks wastes hours of valuable study time.",
            "Unindexed Video Content: Video lectures lack keyword searchability, forcing students to manually scrub through hours of footage."
        ], "⚠️"),
        ("The AI Chatbot Hallucination Trap", [
            "Plausible but False Facts: Generic LLMs (like standard ChatGPT) frequently hallucinate formulas, historical dates, and code syntaxes.",
            "No Source Verification: Commercial chatbots do not cite exact textbook pages, making fact-checking risky before exams.",
            "Academic Integrity Risk: Unreferenced AI responses promote passive copying rather than genuine scholarly comprehension."
        ], "❌"),
        ("Ineffective Passive Learning Habits", [
            "The Illusion of Competence: Simply highlighting textbooks and re-reading notes creates a false feeling of mastery without true retention.",
            "Lack of Active Retrieval: Without self-testing and spaced recall, students forget over 70% of study material within 48 hours (Ebbinghaus Curve).",
            "Missing Visual Structures: Complex interconnected engineering concepts are hard to understand without visual hierarchy graphs."
        ], "📉")
    ]
    for idx, (title, items, icon) in enumerate(problems):
        add_content_card(s3, 0.8 + idx * 4.02, 1.6, card_w, 5.15, title, items, icon=icon)

    # =========================================================================
    # SLIDE 4: CORE CAPABILITIES & HIGHLIGHTS
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Core Capabilities: How AxiomAI Solves These Challenges", "KEY SYSTEM FEATURES")

    features = [
        ("Multimodal Knowledge Hub", [
            "Upload multiple PDFs, notes, and web articles into dedicated course notebooks.",
            "Paste entire multi-video YouTube playlists; the system extracts transcripts and indexes timestamps.",
            "Unified searchable memory pool for all learning materials in a single workspace."
        ], "📚"),
        ("Verifiable Conversational Tutor", [
            "Conversational chat powered by state-of-the-art Retrieval-Augmented Generation.",
            "Every statement is backed by verifiable in-line citations pointing to the exact page.",
            "Clicking any citation instantly highlights the underlying source chunk in the side viewer."
        ], "💬"),
        ("Axiom Studio Concept Visualizer", [
            "Transforms dense chapters into interactive, expandable horizontal mind maps.",
            "Powered by React Flow and D3.js for silky smooth pan, zoom, and node navigation.",
            "Enables students to visualize relationships between core concepts at a single glance."
        ], "🗺️"),
        ("Active Recall & Self-Testing", [
            "Diagnostic Quizzes: Generates 4-option multiple-choice tests with distractor explanations.",
            "Smart Flashcards: Spaced-repetition cards powered by SuperMemo SM-2 for optimal memory retention.",
            "Curriculum Roadmaps: Auto-generates sequenced milestone study paths from ingested materials."
        ], "🎯")
    ]
    f_w = 5.7
    f_h = 2.45
    coords = [
        (0.8, 1.6), (6.833, 1.6),
        (0.8, 4.3), (6.833, 4.3)
    ]
    for idx, (title, items, icon) in enumerate(features):
        x, y = coords[idx]
        add_content_card(s4, x, y, f_w, f_h, title, items, icon=icon)

    # =========================================================================
    # SLIDE 5: SYSTEM ARCHITECTURE (NON-OVERLY TECHNICAL)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "System Architecture: Clean High-Level Pipeline", "SYSTEM DESIGN")

    # 4 Architecture Stages
    stages = [
        ("1. Input Layer", [
            "Frontend Web App: Modern Next.js interface.",
            "Input Formats: PDF documents, plain text, web URLs, and YouTube playlists.",
            "Notebook Organization: Group materials by subject or course unit."
        ], "1"),
        ("2. Processing Layer", [
            "API Gateway: Express & TypeScript routing.",
            "Worker Queues: BullMQ & Redis manage asynchronous ingestion jobs.",
            "Smart Chunking: Content is sliced into overlapping semantic passages."
        ], "2"),
        ("3. Intelligence Layer", [
            "Vector Database: Qdrant indexes dense semantic embeddings.",
            "Semantic Search: Finds the exact relevant paragraphs for any student question.",
            "Context Verification: Audits retrieved chunks to prevent irrelevant data."
        ], "3"),
        ("4. Output & Study Suite", [
            "Grounded Answers: Synthesized response with clickable citations.",
            "Interactive Mind Maps: D3 hierarchical visual graph.",
            "Diagnostic Quizzes: Multiple-choice active recall assessments."
        ], "4")
    ]
    step_w = 2.75
    for idx, (title, items, step_num) in enumerate(stages):
        add_content_card(s5, 0.8 + idx * 2.99, 1.6, step_w, 3.85, title, items, icon=f"Step {step_num}:")

    # Bottom Callout Card
    add_card(s5, 0.8, 5.65, 11.733, 1.1, bg_color=COLOR_ACCENT_LIGHT, border_color=COLOR_ACCENT)
    tb_arch = s5.shapes.add_textbox(Inches(1.05), Inches(5.75), Inches(11.2), Inches(0.85))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True
    p_at = tf_arch.paragraphs[0]
    p_at.text = "Key Architectural Principle: Complete Separation of Concerns"
    p_at.font.name = "Segoe UI"
    p_at.font.size = Pt(12)
    p_at.font.bold = True
    p_at.font.color.rgb = COLOR_NAVY

    p_ab = tf_arch.add_paragraph()
    p_ab.text = "The frontend focuses on responsive user experience and visual graphs, while background worker microservices handle heavy file parsing, transcription, and vector retrieval independently to guarantee zero lag."
    p_ab.font.name = "Segoe UI"
    p_ab.font.size = Pt(11)
    p_ab.font.color.rgb = COLOR_TEXT_MAIN
    p_ab.space_before = Pt(3)

    # =========================================================================
    # SLIDE 6: TECHNOLOGIES & TOOLS USED
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Technologies & Tools: The Full-Stack Ecosystem", "TECHNOLOGY STACK")

    tech_categories = [
        ("Frontend & UI Framework", [
            "Next.js & React 19: High-performance component architecture.",
            "TypeScript: Type-safe client-side application state.",
            "Tailwind CSS: Clean, responsive modern styling system.",
            "React Flow & D3.js: Smooth interactive canvas for concept mind mapping.",
            "Lucide React: Cohesive, accessible interface iconography."
        ], "💻"),
        ("Backend & Ingestion Engine", [
            "Node.js & Express: Lightweight RESTful API gateway.",
            "Prisma ORM: Strongly-typed schema modeling for workspaces and study tools.",
            "SQLite & PostgreSQL: Resilient transactional data storage.",
            "BullMQ & Redis: High-throughput background task queue for parsing heavy PDFs.",
            "YouTube Transcript API: Synchronized caption extraction with second-level timestamps."
        ], "⚙️"),
        ("AI, Vector DB & Search", [
            "Qdrant Vector Database: High-speed approximate nearest neighbor vector indexing.",
            "OpenAI text-embedding-3-small: 1536-dimensional dense semantic vectors.",
            "OpenAI GPT-4o-mini: Fast, accurate, and cost-efficient factual generation.",
            "Sliding-Window Chunker: 600-token chunks with 100-token overlap preserving context."
        ], "🤖"),
        ("DevOps & Deployment", [
            "Docker & Docker Compose: Containerized single-command local deployment.",
            "In-Memory Vector Fallback: Runs locally without mandatory cloud services.",
            "Mock Authentication: Instant developer onboarding for evaluation.",
            "Environment Security: Strict environment variable isolation and API key hygiene."
        ], "🚀")
    ]
    for idx, (title, items, icon) in enumerate(tech_categories):
        x, y = coords[idx]
        add_content_card(s6, x, y, f_w, f_h, title, items, icon=icon)

    # =========================================================================
    # SLIDE 7: USER JOURNEY & WORKFLOW
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "User Experience: The 4-Stage Student Learning Journey", "WORKFLOW")

    journey = [
        ("Stage 1: Create Notebook", [
            "Organize studies by course (e.g., 'Operating Systems', 'Machine Learning').",
            "Maintain distinct, isolated knowledge boundaries for each academic subject.",
            "Fast 1-click workspace setup."
        ], "1️⃣"),
        ("Stage 2: Add Sources", [
            "Upload course textbook chapters, lab manuals, or research PDFs.",
            "Paste URLs for YouTube lectures or entire course playlists.",
            "System parses and indexes all materials in the background."
        ], "2️⃣"),
        ("Stage 3: Grounded Chat", [
            "Ask questions in natural language like talking to a professor.",
            "Receive factual answers with clickable citations.",
            "Inspect exact source paragraphs and video timestamps."
        ], "3️⃣"),
        ("Stage 4: Active Mastery", [
            "Explore auto-generated concept mind maps on React Flow.",
            "Test retention with diagnostic 4-option quizzes.",
            "Practice spaced-repetition flashcards to lock in memory."
        ], "4️⃣")
    ]
    for idx, (title, items, icon) in enumerate(journey):
        add_content_card(s7, 0.8 + idx * 2.99, 1.6, step_w, 5.15, title, items, icon=icon)

    # =========================================================================
    # SLIDE 8: SCREENSHOT 1 — WELCOME & LANDING PAGE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Interface Walkthrough: Welcome & Workspace Hub", "SYSTEM DEMONSTRATION")

    # Screenshot on the left
    img1_path = os.path.abspath('temp/landing_page.jpeg')
    if os.path.exists(img1_path):
        add_card(s8, 0.8, 1.6, 6.7, 5.15)
        s8.shapes.add_picture(img1_path, Inches(0.9), Inches(2.2), width=Inches(6.5))
        # Image label caption
        tb_c1 = s8.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(6.5), Inches(0.4))
        p_c1 = tb_c1.text_frame.paragraphs[0]
        p_c1.text = "Figure 1: AxiomAI System Welcome & Dashboard Interface"
        p_c1.font.name = "Segoe UI"
        p_c1.font.size = Pt(11)
        p_c1.font.bold = True
        p_c1.font.color.rgb = COLOR_ACCENT

    # Explanation Card on the right
    exp1_items = [
        "Modern Academic Hub: Welcoming student landing dashboard designed for immediate clarity and zero cognitive clutter.",
        "Notebook Management: Allows students to create, pin, and manage isolated research notebooks for different academic courses.",
        "Quick Access & Navigation: Seamless shortcuts to jump directly into conversational Q&A, source uploads, or active study tools.",
        "Recent Activity Overview: Displays indexed document counts, source statuses, and study progress at a glance.",
        "Intuitive User Onboarding: Clear call-to-action buttons to help students start researching within seconds."
    ]
    add_content_card(s8, 7.7, 1.6, 4.833, 5.15, "Dashboard Features & How It Works", exp1_items, icon="🖥️")

    # =========================================================================
    # SLIDE 9: SCREENSHOT 2 — ADD KNOWLEDGE SOURCES
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Interface Walkthrough: Adding Knowledge Sources", "SYSTEM DEMONSTRATION")

    img2_path = os.path.abspath('temp/add_knowledge_source.jpeg')
    if os.path.exists(img2_path):
        add_card(s9, 0.8, 1.6, 6.7, 5.15)
        s9.shapes.add_picture(img2_path, Inches(0.9), Inches(2.2), width=Inches(6.5))
        tb_c2 = s9.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(6.5), Inches(0.4))
        p_c2 = tb_c2.text_frame.paragraphs[0]
        p_c2.text = "Figure 2: Multimodal Source Ingestion Modal (PDF, YouTube, Web)"
        p_c2.font.name = "Segoe UI"
        p_c2.font.size = Pt(11)
        p_c2.font.bold = True
        p_c2.font.color.rgb = COLOR_ACCENT

    exp2_items = [
        "Unified Ingestion Modal: Single dialog to feed diverse learning formats into the notebook repository.",
        "Drag-and-Drop PDFs: Upload textbook chapters, academic papers, and lecture slides with instant file validation.",
        "YouTube Playlist Integration: Paste any YouTube video or multi-video playlist URL for automated transcript ingestion.",
        "Web & Plain Text Support: Ingest online documentation, research articles, or custom lecture notes directly.",
        "Asynchronous Ingestion Pipeline: Ingestion runs in the background via BullMQ queues, keeping the user interface smooth and responsive.",
        "Semantic Text Chunking: Extracted text is automatically partitioned into overlapping 600-token passages with source provenance."
    ]
    add_content_card(s9, 7.7, 1.6, 4.833, 5.15, "Ingestion Pipeline & Capabilities", exp2_items, icon="📥")

    # =========================================================================
    # SLIDE 10: SCREENSHOT 3 — CORE RESEARCH WORKSPACE & CHAT
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Interface Walkthrough: Grounded Q&A Workspace", "SYSTEM DEMONSTRATION")

    img3_path = os.path.abspath('temp/workspace.jpeg')
    if os.path.exists(img3_path):
        add_card(s10, 0.8, 1.6, 6.7, 5.15)
        s10.shapes.add_picture(img3_path, Inches(0.9), Inches(2.2), width=Inches(6.5))
        tb_c3 = s10.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(6.5), Inches(0.4))
        p_c3 = tb_c3.text_frame.paragraphs[0]
        p_c3.text = "Figure 3: Interactive Research Workspace with In-Line Verified Citations"
        p_c3.font.name = "Segoe UI"
        p_c3.font.size = Pt(11)
        p_c3.font.bold = True
        p_c3.font.color.rgb = COLOR_ACCENT

    exp3_items = [
        "Multi-Panel Study Environment: Clean 3-pane layout showing sources on the left, interactive AI chat in the center, and study tools on top.",
        "Conversational AI Tutoring: Ask natural-language questions about complex concepts, algorithms, or course notes.",
        "Verifiable In-Line Citations: Every generated assertion includes clickable tags [CID:chunk_id] identifying the exact source passage.",
        "Instant Citation Inspector: Clicking any citation immediately displays the exact textbook paragraph and page number.",
        "Strict Grounding Guardrails: The AI model is strictly constrained to source materials, eliminating hallucinated answers.",
        "Interactive Notebook Overview: Automatically summarizes notebook contents and highlights key study topics upon opening."
    ]
    add_content_card(s10, 7.7, 1.6, 4.833, 5.15, "Workspace Architecture & Features", exp3_items, icon="💬")

    # =========================================================================
    # SLIDE 11: SCREENSHOT 4 — INTERACTIVE CONCEPT MIND MAP
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Axiom Studio: Interactive Concept Mind Mapping", "ACTIVE LEARNING SUITE")

    img4_path = os.path.abspath('temp/mind_map.jpeg')
    if os.path.exists(img4_path):
        # Portrait image
        add_card(s11, 0.8, 1.6, 4.0, 5.15)
        s11.shapes.add_picture(img4_path, Inches(1.15), Inches(2.1), height=Inches(4.5))
        tb_c4 = s11.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(3.8), Inches(0.4))
        p_c4 = tb_c4.text_frame.paragraphs[0]
        p_c4.text = "Figure 4: D3 Interactive Mind Map"
        p_c4.font.name = "Segoe UI"
        p_c4.font.size = Pt(11)
        p_c4.font.bold = True
        p_c4.font.color.rgb = COLOR_ACCENT

    exp4_items = [
        "Automatic Concept Extraction: Synthesizes complex multi-page textbook chapters into a structured, hierarchical knowledge graph.",
        "Interactive React Flow Canvas: Students can smoothly pan, zoom, drag, and expand topic branches on an infinite canvas.",
        "Color-Coded Semantic Hierarchy: Distinct visual tiers differentiate central subject themes, intermediate subtopics, and granular details.",
        "Cognitive Load Reduction: Breaks down overwhelming 50-page reading assignments into digestible visual chunks (Sweller's Cognitive Load Theory).",
        "Regeneration & Customization: Students can regenerate the map with different focal depths to explore specific chapters.",
        "Visual Exam Review: Enables lightning-fast visual revision of interconnected topics right before exams."
    ]
    add_content_card(s11, 5.05, 1.6, 7.48, 5.15, "Mind Map Capabilities & Visual Learning Impact", exp4_items, icon="🗺️")

    # =========================================================================
    # SLIDE 12: SCREENSHOT 5 — ACTIVE RECALL DIAGNOSTIC QUIZ
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Axiom Studio: Active Recall Testing & Quizzes", "ACTIVE LEARNING SUITE")

    img5_path = os.path.abspath('temp/quiz.jpeg')
    if os.path.exists(img5_path):
        add_card(s12, 0.8, 1.6, 4.0, 5.15)
        s12.shapes.add_picture(img5_path, Inches(1.15), Inches(2.1), height=Inches(4.5))
        tb_c5 = s12.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(3.8), Inches(0.4))
        p_c5 = tb_c5.text_frame.paragraphs[0]
        p_c5.text = "Figure 5: Active Recall Diagnostic Quiz"
        p_c5.font.name = "Segoe UI"
        p_c5.font.size = Pt(11)
        p_c5.font.bold = True
        p_c5.font.color.rgb = COLOR_ACCENT

    exp5_items = [
        "Dynamically Generated Quizzes: Automatically synthesizes 4-option multiple-choice questions directly from notebook documents.",
        "Instant Feedback & Validation: Real-time visual feedback highlights correct choices in green and incorrect selections in red.",
        "Detailed Distractor Explanations: Unlike basic quizzes, AxiomAI provides thorough rationales explaining why incorrect options are wrong.",
        "Exam-Oriented Question Framing: Focuses on core definitions, algorithmic principles, and comparative trade-offs students face in university exams.",
        "Testing Effect in Action: Grounded in Roediger & Karpicke's research proving that self-testing produces superior retention compared to passive reading.",
        "Configurable Question Volume: Students can generate quick 5-question spot checks or comprehensive 20-question practice exams."
    ]
    add_content_card(s12, 5.05, 1.6, 7.48, 5.15, "Quiz Engine Features & Learning Methodology", exp5_items, icon="📝")

    # =========================================================================
    # SLIDE 13: FLASHCARDS & ROADMAPS
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Axiom Studio: Spaced-Repetition Flashcards & Roadmaps", "ACTIVE LEARNING SUITE")

    # 2 Large Cards
    flash_items = [
        "SuperMemo SM-2 Algorithm: Leverages the scientifically validated spaced-repetition algorithm to combat memory decay.",
        "Dynamic Interval Calculation: Computes future review intervals based on student recall ratings (Again, Hard, Good, Easy).",
        "Front-and-Back Active Recall: Tests definitions, theorem proofs, and architectural concepts through active mental retrieval.",
        "Cramming Prevention: Intelligently surfaces cards right at the threshold of forgetting to lock knowledge into long-term memory."
    ]
    add_content_card(s13, 0.8, 1.6, 5.7, 5.15, "Spaced-Repetition Flashcard Deck", flash_items, icon="📇")

    roadmap_items = [
        "Automated Curriculum Sequencing: Structures disorganized lecture notes into a progressive, milestone-based learning roadmap.",
        "Prerequisite Dependency Mapping: Ensures students master foundational concepts before tackling advanced topics.",
        "Stage-by-Stage Tracking: Visual progress checkpoints keep students motivated as they advance through syllabus milestones.",
        "Custom Study Pacing: Adaptable to both short-term exam cramming and semester-long self-paced learning."
    ]
    add_content_card(s13, 6.833, 1.6, 5.7, 5.15, "Progressive Learning Roadmap", roadmap_items, icon="🚀")

    # =========================================================================
    # SLIDE 14: SYSTEM ADVANTAGES & PRACTICAL BENEFITS
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "System Advantages: Why AxiomAI Stands Out", "PROJECT IMPACT")

    advantages = [
        ("Zero Factual Hallucinations", [
            "Strict RAG Grounding: All answers are tethered to uploaded documents.",
            "Inline Citation Provenance: Complete traceability down to the paragraph.",
            "Professor & Student Trust: Reliable for rigorous university preparation."
        ], "🛡️"),
        ("Unified Multimodal Synthesis", [
            "PDFs + Video Lectures: Seamlessly merges written texts and YouTube video lectures.",
            "Clickable Video Timestamps: Jump directly to the exact lecture explanation.",
            "No Tab Switching: Everything lives in one centralized research hub."
        ], "🔗"),
        ("Active Learning over Passive Chat", [
            "Goes Beyond Generic Chatbots: Provides visual mind maps, quizzes, and flashcards.",
            "Pedagogically Proven: Built on active recall and cognitive load theory.",
            "Demonstrable Grade Improvement: Fosters genuine concept retention."
        ], "📈"),
        ("Economical & Locally Deployable", [
            "Runs on Standard Laptops: In-memory fallback and SQLite require zero cloud fees.",
            "Containerized Deployment: Docker Compose runs full stack in one command.",
            "Lightweight AI Model: Uses gpt-4o-mini to operate sustainably under a $5 budget."
        ], "💡")
    ]
    for idx, (title, items, icon) in enumerate(advantages):
        x, y = coords[idx]
        add_content_card(s14, x, y, f_w, f_h, title, items, icon=icon)

    # =========================================================================
    # SLIDE 15: RESEARCH FOUNDATIONS (NOT IN HEAVY DETAIL)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Research Foundations: Key Literature Referenced", "THEORETICAL FOUNDATIONS")

    # Subtitle banner
    add_card(s15, 0.8, 1.55, 11.733, 0.65, bg_color=COLOR_ACCENT_LIGHT, border_color=COLOR_ACCENT)
    tb_ref = s15.shapes.add_textbox(Inches(0.95), Inches(1.62), Inches(11.4), Inches(0.5))
    tf_ref = tb_ref.text_frame
    p_rf = tf_ref.paragraphs[0]
    p_rf.text = "Key research papers that inspired our system architecture and learning algorithms (summarized conceptually):"
    p_rf.font.name = "Segoe UI"
    p_rf.font.size = Pt(11.5)
    p_rf.font.color.rgb = COLOR_NAVY

    papers = [
        ("1. Retrieval-Augmented Generation (RAG)", [
            "Paper: P. Lewis et al., NeurIPS 2020",
            "Core Concept Borrowed: Combines pre-trained language models with external vector retrieval to ground answers in factual documents rather than model memory."
        ], "📄"),
        ("2. Dense Passage Retrieval (DPR)", [
            "Paper: V. Karpukhin et al., EMNLP 2020",
            "Core Concept Borrowed: Employs dense vector embeddings instead of naive keyword matching, allowing students to retrieve relevant concepts even with different phrasing."
        ], "📄"),
        ("3. Hypothetical Document Embeddings (HyDE)", [
            "Paper: L. Gao et al., ACL 2023",
            "Core Concept Borrowed: Bridges the vocabulary gap between short student questions and detailed textbook passages by generating an intermediate semantic query representation."
        ], "📄"),
        ("4. Corrective RAG (CRAG) & Verification", [
            "Paper: S.-Q. Yan et al., 2024",
            "Core Concept Borrowed: Evaluates the relevance of retrieved document chunks before generating the final answer to filter out noisy or irrelevant text."
        ], "📄"),
        ("5. Spaced Repetition & Testing Effect", [
            "Papers: J. Karpicke & H. Roediger (Science 2008) | P. Wozniak (1990)",
            "Core Concept Borrowed: Memory retention improves dramatically when students practice active testing and spaced repetition (SuperMemo SM-2) compared to passive reading."
        ], "🧠")
    ]
    # 5 cards nicely laid out (top 3, bottom 2)
    top_y = 2.35
    bot_y = 4.8
    top_w = 3.7
    top_h = 2.3
    bot_w = 5.7
    bot_h = 2.1

    # Top 3
    for idx in range(3):
        title, items, icon = papers[idx]
        add_content_card(s15, 0.8 + idx * 4.02, top_y, top_w, top_h, title, items, icon=icon)

    # Bottom 2
    for idx in range(2):
        title, items, icon = papers[3 + idx]
        add_content_card(s15, 0.8 + idx * 6.033, bot_y, bot_w, bot_h, title, items, icon=icon)

    # =========================================================================
    # SLIDE 16: FUTURE SCOPE & CONCLUSION
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Future Scope & Project Conclusion", "SUMMARY")

    future_items = [
        "Offline Local Small Language Models (SLMs): Running quantized models (e.g., Llama-3-8B or Phi-3) directly in the browser via WebGPU for 100% private, zero-cost offline tutoring.",
        "Real-Time Multi-User Collaborative Rooms: Enabling study groups to share real-time interactive mind maps and take synchronized quiz challenges together.",
        "Native Mobile Application: Developing a cross-platform mobile companion app for reviewing spaced-repetition flashcards on the go.",
        "On-Device Audio Recording: Integrating automated local Whisper transcription for real-time classroom lecture recording and indexing."
    ]
    add_content_card(s16, 0.8, 1.6, 5.7, 5.15, "Future Roadmap & Planned Enhancements", future_items, icon="🔮")

    conclusion_items = [
        "Autonomous Multimodal Solution: Successfully built and validated an end-to-end learning workspace that unifies academic PDFs, YouTube lectures, and web articles.",
        "Elimination of Factual Hallucinations: Proved that strict retrieval-augmented generation and inline citations provide the factual reliability required for university coursework.",
        "Active Study Over Passive Consumption: Replaced unproductive passive reading with interactive concept mind mapping and spaced-repetition diagnostic self-testing.",
        "Production-Ready Engineering: Fully containerized in Docker Compose with local fallbacks, delivering an accessible, zero-cost study tool for students."
    ]
    add_content_card(s16, 6.833, 1.6, 5.7, 5.15, "Project Conclusion & Key Takeaways", conclusion_items, icon="✅")

    # =========================================================================
    # SLIDE 17: THANK YOU & Q&A (Dark Executive Theme)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    bg17 = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg17.fill.solid()
    bg17.fill.fore_color.rgb = COLOR_PRIMARY_DARK
    bg17.line.fill.background()

    tb_ty = s17.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(2.2))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True

    p_ty1 = tf_ty.paragraphs[0]
    p_ty1.text = "Thank You!"
    p_ty1.font.name = "Segoe UI"
    p_ty1.font.size = Pt(44)
    p_ty1.font.bold = True
    p_ty1.font.color.rgb = COLOR_WHITE
    p_ty1.alignment = PP_ALIGN.CENTER

    p_ty2 = tf_ty.add_paragraph()
    p_ty2.text = "Questions & Discussion"
    p_ty2.font.name = "Segoe UI"
    p_ty2.font.size = Pt(22)
    p_ty2.font.color.rgb = COLOR_ACCENT_CYAN
    p_ty2.alignment = PP_ALIGN.CENTER
    p_ty2.space_before = Pt(8)

    # Info footer card on slide 17
    c_info = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(4.5), Inches(8.933), Inches(1.8))
    c_info.fill.solid()
    c_info.fill.fore_color.rgb = RGBColor(30, 41, 59)
    c_info.line.color.rgb = RGBColor(51, 65, 85)
    tf_info = c_info.text_frame
    p_ih = tf_info.paragraphs[0]
    p_ih.text = "AxiomAI: AI-Powered Multimodal Learning Workspace"
    p_ih.font.name = "Segoe UI"
    p_ih.font.size = Pt(13)
    p_ih.font.bold = True
    p_ih.font.color.rgb = COLOR_WHITE
    p_ih.alignment = PP_ALIGN.CENTER
    p_ih.space_after = Pt(6)

    p_im = tf_info.add_paragraph()
    p_im.text = "Students: Uttkarsh Thakur (9923103196) & Ayush Singh (9923103193)"
    p_im.font.name = "Segoe UI"
    p_im.font.size = Pt(11)
    p_im.font.color.rgb = COLOR_ACCENT_CYAN
    p_im.alignment = PP_ALIGN.CENTER

    p_is = tf_info.add_paragraph()
    p_is.text = "Supervisor: Mr. Twinkle Tyagi, Assistant Professor | Dept. of CSE & IT, JIIT Noida"
    p_is.font.name = "Segoe UI"
    p_is.font.size = Pt(11)
    p_is.font.color.rgb = RGBColor(148, 163, 184)
    p_is.alignment = PP_ALIGN.CENTER
    p_is.space_before = Pt(4)

    output_file = "AxiomAI_Final_Presentation_17_Slides.pptx"
    prs.save(output_file)
    print(f"Presentation saved successfully to: {os.path.abspath(output_file)}")
    print(f"Total Slides: {len(prs.slides)}")

if __name__ == '__main__':
    generate_presentation()
