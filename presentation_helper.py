import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# Color Palette (Academic Executive / Tech Widescreen)
# -------------------------------------------------------------
COLOR_PRIMARY_DARK = RGBColor(15, 23, 42)      # Slate 900 #0F172A
COLOR_NAVY = RGBColor(30, 41, 59)              # Slate 800 #1E293B
COLOR_ACCENT = RGBColor(37, 99, 235)           # Blue 600 #2563EB
COLOR_ACCENT_LIGHT = RGBColor(239, 246, 255)   # Blue 50 #EFF6FF
COLOR_ACCENT_CYAN = RGBColor(14, 165, 233)     # Sky 500 #0EA5E9
COLOR_TEXT_MAIN = RGBColor(30, 41, 59)         # Slate 800
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)     # Slate 500 #64748B
COLOR_BG_LIGHT = RGBColor(248, 250, 252)       # Slate 50 #F8FAFC
COLOR_CARD_BG = RGBColor(255, 255, 255)        # Pure White
COLOR_CARD_BORDER = RGBColor(226, 232, 240)    # Slate 200 #E2E8F0
COLOR_HIGHLIGHT_GREEN = RGBColor(22, 163, 74)  # Green 600 #16A34A
COLOR_WHITE = RGBColor(255, 255, 255)

def create_base_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def add_header(slide, title_text, category_text="AXIOMAI CAPSTONE DEFENSE"):
    """Adds a standardized header banner and footer to a content slide"""
    # Background fill
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG_LIGHT
    bg.line.fill.background()

    # Category Pill / Tag
    if category_text:
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Segoe UI"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(0.65))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_PRIMARY_DARK

    # Subtle divider
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_CARD_BORDER
    div.line.fill.background()

    # Footer
    f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
    tf_f = f_box.text_frame
    tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = "AxiomAI: Autonomous Multimodal RAG & Active Learning Workspace | B.Tech Capstone 2026"
    p_f.font.name = "Segoe UI"
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = COLOR_TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Draws a clean white card shape with border"""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_stat_box(slide, left, top, width, height, number_str, label_str, desc_str, color=COLOR_ACCENT):
    """Draws a metric stat box with big numbers"""
    add_card(slide, left, top, width, height)
    tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.2), Inches(width - 0.4), Inches(height - 0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p_num = tf.paragraphs[0]
    p_num.text = number_str
    p_num.font.name = "Segoe UI"
    p_num.font.size = Pt(32)
    p_num.font.bold = True
    p_num.font.color.rgb = color

    p_lbl = tf.add_paragraph()
    p_lbl.text = label_str
    p_lbl.font.name = "Segoe UI"
    p_lbl.font.size = Pt(12)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_PRIMARY_DARK
    p_lbl.space_before = Pt(4)

    p_desc = tf.add_paragraph()
    p_desc.text = desc_str
    p_desc.font.name = "Segoe UI"
    p_desc.font.size = Pt(10)
    p_desc.font.color.rgb = COLOR_TEXT_MUTED
    p_desc.space_before = Pt(2)

def add_bullet_card(slide, left, top, width, height, title, bullets, icon="🔹", bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Draws a card containing a title and formatted bullet items"""
    add_card(slide, left, top, width, height, bg_color, border_color)
    tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    if title:
        p_t = tf.paragraphs[0]
        p_t.text = f"{icon}  {title}" if icon else title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY_DARK
        p_t.space_after = Pt(8)
        start_idx = 1
    else:
        start_idx = 0

    for idx, b in enumerate(bullets):
        p = tf.add_paragraph() if (title or idx > 0) else tf.paragraphs[0]
        p.space_after = Pt(6)
        
        # Check if bullet has bold prefix (e.g. "Prefix: Body")
        if ":" in b and not b.startswith("http"):
            prefix, body = b.split(":", 1)
            r_pre = p.add_run()
            r_pre.text = f"• {prefix.strip()}: "
            r_pre.font.name = "Segoe UI"
            r_pre.font.size = Pt(11)
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_PRIMARY_DARK

            r_bod = p.add_run()
            r_bod.text = body.strip()
            r_bod.font.name = "Segoe UI"
            r_bod.font.size = Pt(11)
            r_bod.font.color.rgb = COLOR_TEXT_MAIN
        else:
            r = p.add_run()
            r.text = f"• {b}"
            r.font.name = "Segoe UI"
            r.font.size = Pt(11)
            r.font.color.rgb = COLOR_TEXT_MAIN

def add_table_slide(slide, left, top, width, height, headers, data, col_widths=None):
    """Draws a clean academic table on a slide"""
    rows = len(data) + 1
    cols = len(headers)
    table_shape = slide.shapes.add_table(rows, cols, Inches(left), Inches(top), Inches(width), Inches(height))
    table = table_shape.table

    if col_widths:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = Inches(w)

    # Headers
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    # Data
    for r_idx, row in enumerate(data):
        bg_col = COLOR_CARD_BG if r_idx % 2 == 0 else RGBColor(241, 245, 249)
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = "Segoe UI"
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_PRIMARY_DARK

print("Presentation helper loaded successfully.")
