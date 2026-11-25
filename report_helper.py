import os
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_element(name):
    return OxmlElement(name)

def set_cell_border(cell, **kwargs):
    """
    Set cell borders
    kwargs: top, bottom, left, right
    values: dict(sz=12, val='single', color='000000')
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, attr in [("val", "w:val"), ("color", "w:color"), ("sz", "w:sz"), ("space", "w:space")]:
                if key in edge_data:
                    element.set(qn(attr), str(edge_data[key]))

def set_cell_shading(cell, color_hex):
    """Set background color of a table cell (e.g., 'E0E0E0' or 'F5F5F5')"""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def format_paragraph(p, space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align

def add_heading_1(doc, text):
    """Chapter heading (16pt, Bold, Times New Roman, Black)"""
    p = doc.add_paragraph()
    format_paragraph(p, space_before=12, space_after=12, line_spacing=1.5)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text):
    """Section heading (14pt, Bold, Times New Roman, Black)"""
    p = doc.add_paragraph()
    format_paragraph(p, space_before=10, space_after=6, line_spacing=1.5)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_3(doc, text):
    """Sub-section heading (12pt, Bold, Times New Roman, Black)"""
    p = doc.add_paragraph()
    format_paragraph(p, space_before=6, space_after=4, line_spacing=1.5)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_body_p(doc, text, bold_prefix=None, italic=False, justify=True):
    """Standard body paragraph (12pt, Times New Roman, 1.5 line spacing, 6pt space after)"""
    p = doc.add_paragraph()
    align = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    format_paragraph(p, space_before=0, space_after=6, line_spacing=1.5, align=align)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet_p(doc, text, bold_prefix=None):
    """Bullet item with academic formatting"""
    p = doc.add_paragraph(style='List Bullet')
    format_paragraph(p, space_before=0, space_after=3, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_figure(doc, img_path, caption_text, width_inches=6.0):
    """Add a centered black & white figure with formal academic caption"""
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_paragraph(p_img, space_before=8, space_after=4, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
        p_img.add_run().add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        format_paragraph(p_cap, space_before=2, space_after=10, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10)
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGBColor(0, 0, 0)
    else:
        print(f"Warning: Image file not found: {img_path}")

def create_academic_table(doc, headers, data, col_widths=None):
    """Creates a standardized academic black-and-white table with borders and alternating fills"""
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = header_text
        set_cell_shading(hdr_cells[i], 'D0D0D0')
        p = hdr_cells[i].paragraphs[0]
        format_paragraph(p, space_before=2, space_after=2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        set_cell_border(hdr_cells[i], top=dict(sz=12, val='single', color='000000'),
                                     bottom=dict(sz=12, val='single', color='000000'),
                                     left=dict(sz=6, val='single', color='000000'),
                                     right=dict(sz=6, val='single', color='000000'))

    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        bg_color = 'F9F9F9' if row_idx % 2 == 1 else 'FFFFFF'
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            set_cell_shading(row_cells[col_idx], bg_color)
            p = row_cells[col_idx].paragraphs[0]
            format_paragraph(p, space_before=2, space_after=2, line_spacing=1.1, align=WD_ALIGN_PARAGRAPH.LEFT)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(0, 0, 0)
            set_cell_border(row_cells[col_idx], top=dict(sz=4, val='single', color='888888'),
                                               bottom=dict(sz=6 if row_idx == len(data)-1 else 4, val='single', color='000000' if row_idx == len(data)-1 else '888888'),
                                               left=dict(sz=6, val='single', color='000000'),
                                               right=dict(sz=6, val='single', color='000000'))

    # Apply col widths if specified
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    # Empty space after table
    p_sp = doc.add_paragraph()
    format_paragraph(p_sp, space_before=0, space_after=6, line_spacing=1.0)
    return table

def add_callout_box(doc, title, text):
    """Creates a spacious callout box with a thick left border for intuitive/simple explanations"""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_shading(cell, 'F4F4F6')
    set_cell_border(cell, 
                    left=dict(sz=24, val='single', color='000000'),
                    top=dict(val='none'),
                    bottom=dict(val='none'),
                    right=dict(val='none'))
    
    # Internal text
    p = cell.paragraphs[0]
    format_paragraph(p, space_before=4, space_after=4, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    r_title = p.add_run(f"💡 {title}\n")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(11)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0, 0, 0)
    
    r_text = p.add_run(text)
    r_text.font.name = 'Times New Roman'
    r_text.font.size = Pt(10.5)
    r_text.font.italic = True
    r_text.font.color.rgb = RGBColor(30, 30, 30)

    # Empty space after callout
    p_sp = doc.add_paragraph()
    format_paragraph(p_sp, space_before=0, space_after=6, line_spacing=1.0)
    return table

print("Word document helper module loaded successfully.")
