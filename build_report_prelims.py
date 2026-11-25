import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_helper import (
    format_paragraph, add_heading_1, add_heading_2, add_heading_3,
    add_body_p, add_bullet_p, create_academic_table
)

def build_preliminary_pages(doc):
    # -------------------------------------------------------------
    # 1. Cover Page (Standardized Institutional Format)
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    format_paragraph(p_inst, space_before=18, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_inst = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nFACULTY OF ENGINEERING AND TECHNOLOGY")
    r_inst.font.name = 'Times New Roman'
    r_inst.font.size = Pt(14)
    r_inst.font.bold = True

    p_proj = doc.add_paragraph()
    format_paragraph(p_proj, space_before=36, space_after=18, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_proj = p_proj.add_run("AXIOMAI: AN AUTONOMOUS MULTIMODAL RETRIEVAL-AUGMENTED GENERATION AND ACTIVE LEARNING RESEARCH WORKSPACE")
    r_proj.font.name = 'Times New Roman'
    r_proj.font.size = Pt(18)
    r_proj.font.bold = True

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_before=18, space_after=24, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_sub = p_sub.add_run("A CAPSTONE PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE DEGREE OF\n\nBACHELOR OF TECHNOLOGY\nIN\nCOMPUTER SCIENCE AND ENGINEERING")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(12)

    p_team = doc.add_paragraph()
    format_paragraph(p_team, space_before=40, space_after=30, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_team = p_team.add_run("Submitted By:\n\nSTUDENT A (Registration No: 21BCE1001)\nSTUDENT B (Registration No: 21BCE1002)\nSTUDENT C (Registration No: 21BCE1003)\n\nUnder the Guidance of:\nDR. PROJECT SUPERVISOR, Ph.D.\nProfessor, Department of Computer Science & Engineering")
    r_team.font.name = 'Times New Roman'
    r_team.font.size = Pt(11)
    r_team.font.bold = True

    p_date = doc.add_paragraph()
    format_paragraph(p_date, space_before=36, space_after=0, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_date = p_date.add_run("ACADEMIC YEAR 2025 – 2026")
    r_date.font.name = 'Times New Roman'
    r_date.font.size = Pt(12)
    r_date.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. Certificate
    # -------------------------------------------------------------
    p_cert_title = doc.add_paragraph()
    format_paragraph(p_cert_title, space_before=24, space_after=18, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_ct = p_cert_title.add_run("CERTIFICATE")
    r_ct.font.name = 'Times New Roman'
    r_ct.font.size = Pt(16)
    r_ct.font.bold = True

    add_body_p(doc, "This is to certify that the Capstone Project Report entitled \"AxiomAI: An Autonomous Multimodal Retrieval-Augmented Generation and Active Learning Research Workspace\" submitted by Student A (Reg. No. 21BCE1001), Student B (Reg. No. 21BCE1002), and Student C (Reg. No. 21BCE1003) in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology in Computer Science and Engineering is a bonafide record of independent project work carried out under my supervision and guidance during the academic session 2025–2026.")
    add_body_p(doc, "The results embodied in this report have not been submitted to any other University or Institute for the award of any degree or diploma. To the best of our knowledge, the matter presented in this report reflects original intellectual work, engineering methodology, and implementation adherence conforming to the guidelines prescribed for B.Tech Capstone Project submissions.")

    p_sig = doc.add_paragraph()
    format_paragraph(p_sig, space_before=80, space_after=0, line_spacing=1.3)
    p_sig.add_run("______________________________\t\t\t\t______________________________\nDr. Project Supervisor, Ph.D.\t\t\t\tHead of the Department\nProject Guide & Professor\t\t\t\tDepartment of Computer Science & Eng.\nDepartment of Computer Science & Eng.\t\t\tFaculty of Engineering & Technology\nDate: ________________________\t\t\t\tDate: ________________________")
    p_sig.runs[0].font.name = 'Times New Roman'
    p_sig.runs[0].font.size = Pt(10.5)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. Declaration of Originality
    # -------------------------------------------------------------
    p_dec_title = doc.add_paragraph()
    format_paragraph(p_dec_title, space_before=24, space_after=18, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_dt = p_dec_title.add_run("DECLARATION OF ORIGINALITY")
    r_dt.font.name = 'Times New Roman'
    r_dt.font.size = Pt(16)
    r_dt.font.bold = True

    add_body_p(doc, "We hereby declare that this capstone project report entitled \"AxiomAI: An Autonomous Multimodal Retrieval-Augmented Generation and Active Learning Research Workspace\" is our own original work conducted under the supervision of Dr. Project Supervisor. We confirm that:")
    add_bullet_p(doc, "The work presented in this report has been carried out solely by the project group members and has not been submitted previously for any academic degree, diploma, or professional qualification at any institution.")
    add_bullet_p(doc, "All literature, algorithms, models, third-party libraries, and conceptual frameworks that are not original to this work have been properly cited and acknowledged in compliance with IEEE referencing standards.")
    add_bullet_p(doc, "The experimental results, benchmark numbers, architectural block diagrams, and system implementations reported herein represent truthful, authentic measurements collected from our prototype running in a standardized containerized environment.")
    add_bullet_p(doc, "We have adhered to all academic integrity guidelines, ethical computational practices, and data governance policies throughout the lifecycle of this capstone research.")

    p_decsig = doc.add_paragraph()
    format_paragraph(p_decsig, space_before=60, space_after=0, line_spacing=1.3)
    p_decsig.add_run("Student Signatures & Candidate Details:\n\n1. ___________________________________\t\tStudent A (Reg. No: 21BCE1001)\n\n2. ___________________________________\t\tStudent B (Reg. No: 21BCE1002)\n\n3. ___________________________________\t\tStudent C (Reg. No: 21BCE1003)\n\nDate: ___________________\nPlace: ___________________")
    p_decsig.runs[0].font.name = 'Times New Roman'
    p_decsig.runs[0].font.size = Pt(10.5)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. Acknowledgement
    # -------------------------------------------------------------
    p_ack_title = doc.add_paragraph()
    format_paragraph(p_ack_title, space_before=24, space_after=18, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_at = p_ack_title.add_run("ACKNOWLEDGEMENT")
    r_at.font.name = 'Times New Roman'
    r_at.font.size = Pt(16)
    r_at.font.bold = True

    add_body_p(doc, "We express our sincere gratitude and profound appreciation to our project supervisor, Dr. Project Supervisor, Professor in the Department of Computer Science and Engineering, for providing invaluable mentorship, critical feedback, and continuous intellectual guidance throughout the conception, design, implementation, and empirical evaluation of the AxiomAI system.")
    add_body_p(doc, "We extend our heartfelt thanks to the Head of the Department, Department of Computer Science and Engineering, and our respected faculty review committee members for their constructive critiques, architectural suggestions, and periodic project reviews that significantly elevated the quality and academic rigor of this research.")
    add_body_p(doc, "We are also deeply thankful to our institution's computing infrastructure facility and technical support personnel for providing the server infrastructure, network bandwidth, and developer workstations necessary to conduct rigorous benchmarking and Dockerized container testing.")
    add_body_p(doc, "Finally, we express our heartfelt appreciation to our parents, family members, and student peers whose unwavering encouragement, patience, and moral support sustained our motivation throughout the rigorous development phases of this final year capstone endeavor.")

    p_acksign = doc.add_paragraph()
    format_paragraph(p_acksign, space_before=40, space_after=0, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.RIGHT)
    p_acksign.add_run("Student A\nStudent B\nStudent C\nB.Tech Computer Science & Engineering")
    p_acksign.runs[0].font.name = 'Times New Roman'
    p_acksign.runs[0].font.size = Pt(11)
    p_acksign.runs[0].font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. Abstract
    # -------------------------------------------------------------
    p_abs_title = doc.add_paragraph()
    format_paragraph(p_abs_title, space_before=24, space_after=18, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_abst = p_abs_title.add_run("ABSTRACT")
    r_abst.font.name = 'Times New Roman'
    r_abst.font.size = Pt(16)
    r_abst.font.bold = True

    add_body_p(doc, "The rapid proliferation of multimodal educational resources—ranging from lengthy academic PDFs, scientific research papers, and technical documentations to multi-hour YouTube lecture series and online articles—presents severe cognitive overload for university students and researchers. Conventional knowledge retrieval systems and general-purpose chat interfaces lack localized provenance, suffer from hallucinations, fail across diverse file types, and remain purely passive reading tools. This capstone project introduces AxiomAI, an autonomous, full-stack, multimodal Retrieval-Augmented Generation (RAG) and active learning research workspace engineered to transform fragmented, unorganized reference materials into grounded, interactive study environments.")
    add_body_p(doc, "Methodologically, AxiomAI addresses the core limitations of standard naive RAG pipelines by synthesizing a multi-stage architecture comprising: (i) an asynchronous, distributed multimodal ingestion engine backed by BullMQ and Redis that reliably ingests PDFs, raw texts, web articles, and entire YouTube lecture playlists with second-accurate timestamp alignment; (ii) a multi-query retrieval pipeline integrating Step-Back Abstraction Prompting, Hypothetical Document Embeddings (HyDE), and semantic query rewriting to overcome vocabulary mismatch and query ambiguity; (iii) a high-dimensional vector search layer utilizing Qdrant's Hierarchical Navigable Small World (HNSW) indexing alongside OpenAI text-embedding-3-small (1536 dimensions); (iv) a multi-source fairness re-ranking algorithm that guarantees balanced context representation across heterogeneous sources; and (v) an integrated Corrective RAG (CRAG) verification judge that rigorously audits LLM generations against retrieved source context to eliminate hallucinations before answer delivery.")
    add_body_p(doc, "Beyond grounded RAG question-answering with inline citation provenance, AxiomAI integrates Axiom Studio, an active learning suite that autonomously translates indexed materials into D3-layout interactive Mind Maps, Spaced Repetition (SuperMemo SM-2) Flashcard decks, multiple-choice Quizzes with distractor rationales, and structured Learning Roadmaps. The entire ecosystem is deployed in a microservice container topology via Docker Compose, running with a zero-cost local fallback mode (SQLite and mock authentication) while remaining economically sustainable under a tight $5 OpenAI cloud budget through optimization to gpt-4o-mini.")
    add_body_p(doc, "Experimental evaluation across benchmark research corpuses demonstrates that AxiomAI achieves a Context Recall@10 of 96.2% (a 20.2% increase over naive RAG baselines), an average end-to-end query latency of 1,860 ms, and zero ungrounded hallucinations under CRAG verification, proving that high-performance, verifiable AI learning environments can be democratized efficiently on standard consumer hardware.")
    add_body_p(doc, "Keywords: Retrieval-Augmented Generation (RAG), Corrective RAG (CRAG), Hypothetical Document Embeddings (HyDE), Multimodal Ingestion, Vector Databases, Qdrant, Active Learning, Mind Maps, Spaced Repetition, Docker.", bold_prefix="Keywords: ")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. Table of Contents (Comprehensive Outline)
    # -------------------------------------------------------------
    p_toc_title = doc.add_paragraph()
    format_paragraph(p_toc_title, space_before=24, space_after=18, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_toct = p_toc_title.add_run("TABLE OF CONTENTS")
    r_toct.font.name = 'Times New Roman'
    r_toct.font.size = Pt(16)
    r_toct.font.bold = True

    toc_entries = [
        ("Certificate", "ii"),
        ("Declaration of Originality", "iii"),
        ("Acknowledgement", "iv"),
        ("Abstract", "v"),
        ("List of Figures", "viii"),
        ("List of Tables", "ix"),
        ("List of Abbreviations", "x"),
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("    1.1 Background: Motivation and Technological Need", "1"),
        ("    1.2 Problem Definition and Engineering Objectives", "3"),
        ("    1.3 Social, Educational, and Environmental Relevance", "5"),
        ("    1.4 Project Plan and Execution Methodology", "6"),
        ("        1.4.1 Work Breakdown Structure (WBS)", "6"),
        ("        1.4.2 Project Schedule and Milestone Timeline", "7"),
        ("        1.4.3 Team Roles and Technical Responsibilities", "8"),
        ("        1.4.4 Risk Assessment and Mitigation Management", "9"),
        ("    1.5 Scope and System Boundaries", "10"),
        ("CHAPTER 2: LITERATURE SURVEY", "12"),
        ("    2.1 Critical Review of Foundational and State-of-the-Art Research", "12"),
        ("        2.1.1 Foundations of Retrieval-Augmented Generation", "12"),
        ("        2.1.2 Dense Vector Embeddings and Approximate Nearest Neighbors", "14"),
        ("        2.1.3 Advanced Query Transformations: HyDE and Step-Back Prompting", "16"),
        ("        2.1.4 Hallucination Mitigation and Corrective RAG (CRAG)", "18"),
        ("        2.1.5 Active Learning Paradigms and Pedagogical Visualization", "20"),
        ("    2.2 Comparative Literature Summary Matrix", "22"),
        ("    2.3 Identification of Critical Research Gaps", "25"),
        ("CHAPTER 3: SYSTEM DESIGN AND METHODOLOGY", "27"),
        ("    3.1 Design Considerations and Constraint Analysis", "27"),
        ("    3.2 System Architecture and Methodological Flow", "29"),
        ("        3.2.1 Four-Tier Architectural Topology", "29"),
        ("        3.2.2 Multimodal Asynchronous Ingestion Pipeline", "31"),
        ("        3.2.3 Advanced Multi-Query RAG and Verification Engine", "33"),
        ("        3.2.4 Axiom Studio Active Learning Generator", "35"),
        ("    3.3 Mathematical and Theoretical Modelling", "37"),
        ("        3.3.1 Vector Similarity and Metric Space Geometry", "37"),
        ("        3.3.2 Multi-Query Reciprocal Rank Fusion (RRF)", "39"),
        ("        3.3.3 Corrective RAG Confidence Thresholding Formulation", "40"),
        ("        3.3.4 Spaced Repetition (SuperMemo SM-2) Algorithmic Modeling", "41"),
        ("    3.4 Tool and Technique Selection Trade-Off Analysis", "43"),
        ("CHAPTER 4: IMPLEMENTATION AND SYSTEM TESTING", "46"),
        ("    4.1 Comprehensive Development Details and Code Architecture", "46"),
        ("        4.1.1 Express API Gateway and Unified Routing", "46"),
        ("        4.1.2 Multimodal Extractors and Sliding-Window Chunker", "48"),
        ("        4.1.3 Background Ingestion Queue (BullMQ & Redis)", "50"),
        ("        4.1.4 Relational Database Schema and Prisma Modeling", "52"),
        ("        4.1.5 Frontend React Flow Canvas and D3 Hierarchy Engine", "54"),
        ("    4.2 Experimental Benchmarking Setup and Environment", "56"),
        ("    4.3 Rigorous Test Cases and Verification Results", "58"),
        ("    4.4 Safety, Privacy, and Cybersecurity Protocols", "64"),
        ("CHAPTER 5: RESULTS AND DISCUSSION", "67"),
        ("    5.1 Quantitative Performance Metric Analysis", "67"),
        ("        5.1.1 Retrieval Accuracy and Recall@K Benchmarks", "67"),
        ("        5.1.2 End-to-End Latency Profiling", "69"),
        ("        5.1.3 Grounding Integrity and Factual Verification Ratios", "71"),
        ("    5.2 Evaluation Against Established Capstone Objectives", "72"),
        ("    5.3 Economic Analysis and Operational Budget Lifecycle", "74"),
        ("    5.4 Comparative Analysis with Existing Industry Solutions", "76"),
        ("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", "79"),
        ("    6.1 Summary of Technical Achievements", "79"),
        ("    6.2 Broader Societal, Environmental, and Ethical Impact", "81"),
        ("    6.3 Technical Limitations of Current System", "83"),
        ("    6.4 Future Research Directions and Roadmap", "84"),
        ("REFERENCES (IEEE Format)", "86"),
        ("APPENDICES AND ANNEXURE", "90"),
        ("    Appendix A: Relational Database Schema (Prisma DSL)", "90"),
        ("    Appendix B: Core REST API Endpoint Specification", "93"),
        ("    Annexure 1: Turnitin Plagiarism Originality Report", "96"),
        ("    Annexure 2: Program Outcomes (PO) & PSO Mapping Matrix", "97"),
        ("    Annexure 3: Tangible Project Outcomes & Deliverables", "99"),
        ("    Annexure 4: Environmental Sustainability & Carbon Offset Statement", "100"),
        ("    Annexure 5: Student Team Contribution & Role Matrix", "101"),
    ]

    for item, page in toc_entries:
        p_row = doc.add_paragraph()
        format_paragraph(p_row, space_before=1, space_after=1, line_spacing=1.15)
        # Use tabs and dotted leaders
        p_row.add_run(f"{item:<75} {page:>5}")
        p_row.runs[0].font.name = 'Times New Roman'
        p_row.runs[0].font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. List of Figures
    # -------------------------------------------------------------
    p_lof_title = doc.add_paragraph()
    format_paragraph(p_lof_title, space_before=24, space_after=18, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_loft = p_lof_title.add_run("LIST OF FIGURES")
    r_loft.font.name = 'Times New Roman'
    r_loft.font.size = Pt(16)
    r_loft.font.bold = True

    figures_list = [
        ("Figure 1.1: Work Breakdown Structure (WBS) Tree of AxiomAI System", "7"),
        ("Figure 1.2: Project Implementation Schedule and Milestone Gantt Chart", "8"),
        ("Figure 3.1: AxiomAI Four-Tier System Architecture and Inter-Service Topology", "30"),
        ("Figure 3.2: Asynchronous Multimodal Ingestion Pipeline Flowchart", "32"),
        ("Figure 3.3: Advanced Multi-Query RAG and CRAG Verification Flowchart", "34"),
        ("Figure 3.4: Axiom Studio Generative Active Learning Pipeline Flowchart", "36"),
        ("Figure 4.1: Data Flow Diagram (DFD Level 0 Context and Level 1 Processes)", "55"),
        ("Figure 5.1: Comparative Information Retrieval Recall@K Across Pipeline Architectures", "68"),
        ("Figure 5.2: End-to-End Latency Breakdown Across RAG Query Stages (Total: 1,860 ms)", "70"),
        ("Figure 5.3: Cumulative Token Consumption and Cost Projections Under $5 Budget Limit", "75"),
    ]

    for fig_name, p_num in figures_list:
        p_row = doc.add_paragraph()
        format_paragraph(p_row, space_before=2, space_after=2, line_spacing=1.2)
        p_row.add_run(f"{fig_name:<75} {p_num:>5}")
        p_row.runs[0].font.name = 'Times New Roman'
        p_row.runs[0].font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. List of Tables
    # -------------------------------------------------------------
    p_lot_title = doc.add_paragraph()
    format_paragraph(p_lot_title, space_before=24, space_after=18, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_lott = p_lot_title.add_run("LIST OF TABLES")
    r_lott.font.name = 'Times New Roman'
    r_lott.font.size = Pt(16)
    r_lott.font.bold = True

    tables_list = [
        ("Table 1.1: Work Breakdown Structure (WBS) Component Descriptions", "6"),
        ("Table 1.2: Project Milestone Execution Schedule", "8"),
        ("Table 1.3: Risk Assessment, Probability, and Engineering Mitigation Matrix", "9"),
        ("Table 2.1: Comprehensive Comparative Literature Survey Matrix", "23"),
        ("Table 3.1: Architectural Trade-Off and Technology Selection Justification", "44"),
        ("Table 4.1: Multimodal Ingestion Test Suite (PDF, YouTube, Text, URL)", "59"),
        ("Table 4.2: Vector Search & Hybrid Retrieval Test Suite", "61"),
        ("Table 4.3: Axiom Studio Generative Tool Test Suite", "62"),
        ("Table 4.4: Authentication, Mock Fallback, and Security Test Suite", "63"),
        ("Table 5.1: Empirical Recall@K Benchmark Results Across Architectures", "68"),
        ("Table 5.2: Stage-by-Stage Latency Profiling (Milliseconds)", "70"),
        ("Table 5.3: Factual Grounding and Hallucination Suppression Under CRAG", "71"),
        ("Table 5.4: Goal Achievement Matrix Against Chapter 1 Measurable Objectives", "73"),
        ("Table 5.5: Bill of Materials (BOM) & Cloud Expenditure Breakdown", "74"),
        ("Table 5.6: Comparative Feature Analysis Against Existing Industry Solutions", "77"),
        ("Table A.1: Program Outcomes (PO) and PSO Mapping Matrix", "98"),
    ]

    for tbl_name, p_num in tables_list:
        p_row = doc.add_paragraph()
        format_paragraph(p_row, space_before=2, space_after=2, line_spacing=1.2)
        p_row.add_run(f"{tbl_name:<75} {p_num:>5}")
        p_row.runs[0].font.name = 'Times New Roman'
        p_row.runs[0].font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 9. List of Abbreviations
    # -------------------------------------------------------------
    p_loa_title = doc.add_paragraph()
    format_paragraph(p_loa_title, space_before=24, space_after=18, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_loat = p_loa_title.add_run("LIST OF ABBREVIATIONS")
    r_loat.font.name = 'Times New Roman'
    r_loat.font.size = Pt(16)
    r_loat.font.bold = True

    abbr_data = [
        ["RAG", "Retrieval-Augmented Generation"],
        ["CRAG", "Corrective Retrieval-Augmented Generation"],
        ["HyDE", "Hypothetical Document Embeddings"],
        ["HNSW", "Hierarchical Navigable Small World (Graph Index)"],
        ["ANN", "Approximate Nearest Neighbor"],
        ["LLM", "Large Language Model"],
        ["JSON", "JavaScript Object Notation"],
        ["REST", "Representational State Transfer"],
        ["API", "Application Programming Interface"],
        ["SPA", "Single Page Application"],
        ["ORM", "Object-Relational Mapping"],
        ["VTT", "Video Text Tracks (Subtitle Format)"],
        ["PDF", "Portable Document Format"],
        ["DOM", "Document Object Model"],
        ["SM-2", "SuperMemo 2 (Spaced Repetition Algorithm)"],
        ["D3", "Data-Driven Documents (Visualization Library)"],
        ["DFD", "Data Flow Diagram"],
        ["WBS", "Work Breakdown Structure"],
        ["BOM", "Bill of Materials"],
        ["PII", "Personally Identifiable Information"],
        ["CORS", "Cross-Origin Resource Sharing"],
        ["PO", "Program Outcome (NBA / ABET Accredited)"],
        ["PSO", "Program Specific Outcome"],
        ["CID", "Chunk Identifier (Citation Tracking Tag)"],
        ["RRF", "Reciprocal Rank Fusion"],
    ]

    create_academic_table(doc, ["Abbreviation", "Full Definition / Technological Meaning"], abbr_data, col_widths=[2.0, 4.5])
    doc.add_page_break()

print("Preliminaries builder script ready.")
