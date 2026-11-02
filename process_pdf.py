import fitz

input_pdf = r"Report format pg-1-2(23-24) (1)-merged.pdf"
doc = fitz.open(input_pdf)

# 1. Remove the 5 blank pages (pages 3, 4, 5, 6, 7 -> indices 2, 3, 4, 5, 6)
doc.delete_pages([2, 3, 4, 5, 6])
print(f"Total remaining pages: {len(doc)}")

# 2. Remove '~ 1 ~' on Page 1 (Cover Page)
p1 = doc[0]
p1.add_redact_annot(fitz.Rect(280, 780, 320, 800), fill=(1, 1, 1))
p1.apply_redactions()

# 3. Update TOC Table on Page 3 (Index 2)
p_toc = doc[2]

# Redact old numbers
p_toc.add_redact_annot(fitz.Rect(520, 135, 550, 645), fill=(1, 1, 1))
p_toc.apply_redactions()

# Draw normal black table border on TOC table
x0, x1, x2, x3 = 80.8, 153.0, 469.2, 546.3
y_top = 107.8
y_bot = 646.0

p_toc.draw_rect(fitz.Rect(x0, y_top, x3, y_bot), color=(0, 0, 0), width=0.8)
p_toc.draw_line(fitz.Point(x1, y_top), fitz.Point(x1, y_bot), color=(0, 0, 0), width=0.5)
p_toc.draw_line(fitz.Point(x2, y_top), fitz.Point(x2, y_bot), color=(0, 0, 0), width=0.5)
p_toc.draw_line(fitz.Point(x0, 128.0), fitz.Point(x3, 128.0), color=(0, 0, 0), width=0.8)

toc_entries = [
    (142.9, "v", True),
    (171.5, "1", True),
    (199.9, "1", False),
    (228.7, "2", False),
    (257.6, "3", True),
    (286.1, "3", False),
    (314.9, "5", False),
    (343.7, "5", False),
    (372.5, "5", False),
    (401.3, "5", False),
    (430.2, "6", False),
    (459.0, "6", False),
    (487.8, "6", False),
    (516.6, "7", False),
    (545.4, "8", True),
    (573.8, "8", False),
    (602.6, "9", False),
    (630.6, "14", True),
]

for i in range(len(toc_entries) - 1):
    ymid = (toc_entries[i][0] + toc_entries[i+1][0]) / 2 + 1.5
    p_toc.draw_line(fitz.Point(x0, ymid), fitz.Point(x3, ymid), color=(0, 0, 0), width=0.4)

for y, val, is_b in toc_entries:
    fn = "times-bold" if is_b else "times-roman"
    px = 533 if len(val) == 1 else 528
    p_toc.insert_text(fitz.Point(px, y + 10), val, fontname=fn, fontsize=11, color=(0, 0, 0))

# 4. Update List of Figures Table on Page 4 (Index 3)
p_fig = doc[3]

# Redact old numbers
p_fig.add_redact_annot(fitz.Rect(520, 130, 550, 345), fill=(1, 1, 1))
p_fig.apply_redactions()

# Draw normal black table border on Fig table
fx0, fx1, fx2, fx3 = 81.7, 156.1, 462.5, 545.5
fy_top = 104.9
fy_bot = 352.0

p_fig.draw_rect(fitz.Rect(fx0, fy_top, fx3, fy_bot), color=(0, 0, 0), width=0.8)
p_fig.draw_line(fitz.Point(fx1, fy_top), fitz.Point(fx1, fy_bot), color=(0, 0, 0), width=0.5)
p_fig.draw_line(fitz.Point(fx2, fy_top), fitz.Point(fx2, fy_bot), color=(0, 0, 0), width=0.5)
p_fig.draw_line(fitz.Point(fx0, 125.0), fitz.Point(fx3, 125.0), color=(0, 0, 0), width=0.8)

fig_entries = [
    (138.1, "9"),
    (166.6, "10"),
    (195.1, "10"),
    (223.6, "11"),
    (252.2, "11"),
    (280.6, "12"),
    (323.7, "13"),
]

row_divs = [152.0, 181.0, 209.0, 238.0, 266.0, 309.0]
for rdiv in row_divs:
    p_fig.draw_line(fitz.Point(fx0, rdiv), fitz.Point(fx3, rdiv), color=(0, 0, 0), width=0.4)

for y, val in fig_entries:
    px = 533 if len(val) == 1 else 528
    p_fig.insert_text(fitz.Point(px, y + 10), val, fontname="times-roman", fontsize=11, color=(0, 0, 0))

# 5. Draw normal black table borders on Tech Stack Table (Page 8 & Page 9)
p_ts1 = doc[7]
# Outer box
tx0, tx1, tx2, tx3 = 80.4, 205.0, 345.0, 546.0
ty_top1 = 210.8
ty_bot1 = 708.0

p_ts1.draw_rect(fitz.Rect(tx0, ty_top1, tx3, ty_bot1), color=(0, 0, 0), width=0.8)
p_ts1.draw_line(fitz.Point(tx1, ty_top1), fitz.Point(tx1, ty_bot1), color=(0, 0, 0), width=0.5)
p_ts1.draw_line(fitz.Point(tx2, ty_top1), fitz.Point(tx2, ty_bot1), color=(0, 0, 0), width=0.5)

ts1_rows = [255.0, 346.0, 435.0, 522.0, 614.0, 686.0]
for ry in ts1_rows:
    p_ts1.draw_line(fitz.Point(tx0, ry), fitz.Point(tx3, ry), color=(0, 0, 0), width=0.5)

# Page 9 Tech stack continuation
p_ts2 = doc[8]
ty_top2 = 70.0
ty_bot2 = 345.0

p_ts2.draw_rect(fitz.Rect(tx0, ty_top2, tx3, ty_bot2), color=(0, 0, 0), width=0.8)
p_ts2.draw_line(fitz.Point(tx1, ty_top2), fitz.Point(tx1, ty_bot2), color=(0, 0, 0), width=0.5)
p_ts2.draw_line(fitz.Point(tx2, ty_top2), fitz.Point(tx2, ty_bot2), color=(0, 0, 0), width=0.5)

ts2_rows = [130.0, 200.0, 280.0]
for ry in ts2_rows:
    p_ts2.draw_line(fitz.Point(tx0, ry), fitz.Point(tx3, ry), color=(0, 0, 0), width=0.5)

# 6. Draw normal black table borders on Lighthouse Table (Page 12)
p_lh = doc[11]
lx0, lx1, lx2, lx3, lx4 = 81.7, 230.2, 335.0, 445.0, 535.0
ly_top = 133.8
ly_bot = 580.0

p_lh.draw_rect(fitz.Rect(lx0, ly_top, lx4, ly_bot), color=(0, 0, 0), width=0.8)
p_lh.draw_line(fitz.Point(lx1, ly_top), fitz.Point(lx1, ly_bot), color=(0, 0, 0), width=0.5)
p_lh.draw_line(fitz.Point(lx2, ly_top), fitz.Point(lx2, ly_bot), color=(0, 0, 0), width=0.5)
p_lh.draw_line(fitz.Point(lx3, ly_top), fitz.Point(lx3, ly_bot), color=(0, 0, 0), width=0.5)

lh_rows = [175.0, 220.0, 264.0, 308.0, 352.0, 384.0, 425.0, 457.0, 499.0, 542.0]
for ry in lh_rows:
    p_lh.draw_line(fitz.Point(lx0, ry), fitz.Point(lx4, ry), color=(0, 0, 0), width=0.5)

# 7. Add page numbers starting from Introduction as 1 (Page 6 to Page 20)
for p_idx in range(5, len(doc)):
    page = doc[p_idx]
    page_num = str(p_idx - 5 + 1)
    tw = fitz.get_text_length(page_num, fontname="times-roman", fontsize=11)
    cx = page.rect.width / 2.0 - tw / 2.0
    cy = page.rect.height - 35.0
    page.insert_text(fitz.Point(cx, cy), page_num, fontname="times-roman", fontsize=11, color=(0, 0, 0))

output_pdf = "Report format pg-1-2(23-24) (1)-merged.pdf"
doc.save("Report_format_pg-1-2(23-24)_(1)-merged_final.pdf")
print("Saved final PDF successfully!")
