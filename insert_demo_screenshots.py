import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER

def insert_screenshots_into_report(doc_path):
    print(f"Loading document: {doc_path}")
    doc = docx.Document(doc_path)

    # Find styles
    p_h2_style = None
    p_h3_style = None
    p_body_style = None
    for p in doc.paragraphs:
        if p.style.name == 'Heading 2' and p_h2_style is None:
            p_h2_style = p.style
        elif p.style.name == 'Heading 3' and p_h3_style is None:
            p_h3_style = p.style
        elif p.style.name == 'Body Text' and p_body_style is None:
            p_body_style = p.style

    # 1. Locate REFERENCES heading
    ref_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().upper() == 'REFERENCES':
            ref_idx = i
            break

    if ref_idx is None:
        raise ValueError("Could not locate REFERENCES heading in document.")

    print(f"Located REFERENCES heading at paragraph index {ref_idx}")

    # The paragraph immediately preceding REFERENCES contains the section break (sectPr)
    # We insert right before this section break paragraph so all new content belongs to Chapter 6
    sect_break_p = doc.paragraphs[ref_idx - 1]
    print(f"Target insertion point is immediately before paragraph {ref_idx - 1}")

    # Define figure sequence matching the user workflow
    figures = [
        {
            'file': os.path.abspath('temp/landing_page.jpeg'),
            'width': Inches(6.0),
            'caption': 'Figure 6.5.1: AxiomAI Welcome and Landing Page Interface',
            'page_break_before': False
        },
        {
            'file': os.path.abspath('temp/add_knowledge_source.jpeg'),
            'width': Inches(6.0),
            'caption': 'Figure 6.5.2: Multimodal Knowledge Source Ingestion Dialog (PDF, Web, YouTube)',
            'page_break_before': True
        },
        {
            'file': os.path.abspath('temp/workspace.jpeg'),
            'width': Inches(6.0),
            'caption': 'Figure 6.5.3: Core Research Workspace with Grounded Chat and In-line Citations',
            'page_break_before': True
        },
        {
            'file': os.path.abspath('temp/mind_map.jpeg'),
            'width': Inches(4.3),
            'caption': 'Figure 6.5.4: Axiom Studio Interactive D3 Concept Mind Map Visualization',
            'page_break_before': True
        },
        {
            'file': os.path.abspath('temp/quiz.jpeg'),
            'width': Inches(4.3),
            'caption': 'Figure 6.5.5: Axiom Studio Active Recall Diagnostic Quiz and Evaluation Interface',
            'page_break_before': True
        }
    ]

    # Verify all image files exist
    for fig in figures:
        if not os.path.exists(fig['file']):
            raise FileNotFoundError(f"Image file not found: {fig['file']}")

    # 1. Insert Section Heading 6.5
    h2 = sect_break_p.insert_paragraph_before('6.5 System Demonstration & User Interface Walkthrough')
    h2.style = p_h2_style
    h2.paragraph_format.space_before = Pt(18)
    h2.paragraph_format.space_after = Pt(10)
    for r in h2.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.bold = True

    # 2. Insert Intro Body Paragraph
    intro = sect_break_p.insert_paragraph_before(
        "The operational workflows, responsive user interfaces, and pedagogical active learning tools engineered for AxiomAI "
        "are demonstrated through the following high-resolution production interface captures:"
    )
    intro.style = p_body_style
    intro.paragraph_format.space_after = Pt(14)
    intro.paragraph_format.line_spacing = 1.5
    for r in intro.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)

    # 3. Insert each figure and caption
    for fig in figures:
        p_img = sect_break_p.insert_paragraph_before()
        p_img.style = p_body_style
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(4)
        if fig['page_break_before']:
            p_img.paragraph_format.page_break_before = True

        r_img = p_img.add_run()
        r_img.add_picture(fig['file'], width=fig['width'])

        p_cap = sect_break_p.insert_paragraph_before(fig['caption'])
        p_cap.style = p_h3_style
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(18)
        p_cap.paragraph_format.line_spacing = 1.15
        for r in p_cap.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            r.font.bold = True

    # 4. Update List of Figures
    # Locate Figure 5.1.3.1 in List of Figures
    lof_idx = None
    for i, p in enumerate(doc.paragraphs):
        if 'Figure 5.1.3.1' in p.text:
            lof_idx = i
            break

    if lof_idx is not None:
        print(f"Found Figure 5.1.3.1 in List of Figures at paragraph {lof_idx}. Inserting new figure entries...")
        next_lof = doc.paragraphs[lof_idx + 1]
        for fig in figures:
            p_entry = next_lof.insert_paragraph_before(f"{fig['caption']}\t50")
            p_entry.style = p_body_style
            p_entry.paragraph_format.line_spacing = 1.15
            p_entry.paragraph_format.space_after = Pt(4)
            p_entry.paragraph_format.tab_stops.add_tab_stop(Inches(6.6), WD_TAB_ALIGNMENT.LEFT, WD_TAB_LEADER.SPACES)
            for r in p_entry.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11)

    doc.save(doc_path)
    print(f"Successfully modified and saved report to: {doc_path}")

if __name__ == '__main__':
    target_report = 'temp/AxiomAI_Final_Capstone_Project_Report-1.docx'
    insert_screenshots_into_report(target_report)
