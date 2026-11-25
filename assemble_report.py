import os
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

from report_helper import format_paragraph
from build_report_prelims import build_preliminary_pages
from build_report_ch1 import build_chapter_1
from build_report_ch2 import build_chapter_2
from build_report_ch3 import build_chapter_3
from build_report_ch4 import build_chapter_4
from build_report_ch5 import build_chapter_5
from build_report_ch6 import build_chapter_6
from build_report_backmatter import build_backmatter

def generate_full_report():
    print("Initializing Capstone Project Report generation...")
    doc = docx.Document()

    # -------------------------------------------------------------
    # Page Setup conforming strictly to Template Specifications:
    # Paper Size: A4, White
    # Margins: 2.0 cm on all sides
    # Font Style: Times New Roman, 12pt body
    # Line Spacing: 1.5
    # -------------------------------------------------------------
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)

    # Configure Default Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # Build Document Sections
    # -------------------------------------------------------------
    print("Building Preliminary Pages (Cover, Certificate, Declaration, Abstract, TOC, Lists)...")
    build_preliminary_pages(doc)

    print("Building Chapter 1: Introduction (Background, Objectives, Relevance, WBS, Gantt, Risks)...")
    build_chapter_1(doc)

    print("Building Chapter 2: Literature Survey (Critical Review, Summary Table, Research Gaps)...")
    build_chapter_2(doc)

    print("Building Chapter 3: System Design & Methodology (Architecture, Flowcharts, Math Modeling, Tools)...")
    build_chapter_3(doc)

    print("Building Chapter 4: Implementation & Testing (Development, DFD, Test Cases, Safety Protocols)...")
    build_chapter_4(doc)

    print("Building Chapter 5: Results & Discussion (Recall@K Benchmarks, Latency, Grounding, BOM, Comparisons)...")
    build_chapter_5(doc)

    print("Building Chapter 6: Conclusion & Future Scope (Achievements, Impact, Limitations, Roadmap)...")
    build_chapter_6(doc)

    print("Building References, Appendices & Annexure (35 IEEE Refs, Prisma DDL, API Specs, Turnitin, PO Mapping)...")
    build_backmatter(doc)

    output_path = "AxiomAI_Final_Capstone_Project_Report.docx"
    doc.save(output_path)
    print(f"Report saved successfully to: {os.path.abspath(output_path)}")

    # Calculate statistics
    total_paras = len(doc.paragraphs)
    total_tables = len(doc.tables)
    total_words = sum(len(p.text.split()) for p in doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                total_words += sum(len(p.text.split()) for p in cell.paragraphs)

    print("--- DOCUMENT GENERATION SUMMARY ---")
    print(f"File Name: {output_path}")
    print(f"Total Paragraphs: {total_paras}")
    print(f"Total Academic Tables: {total_tables}")
    print(f"Total Word Count: ~{total_words:,} words")
    print(f"Estimated Page Count (at ~350-400 words/page + 10 full figures + 16 tables + page breaks): 60 - 75 pages")

if __name__ == "__main__":
    generate_full_report()
