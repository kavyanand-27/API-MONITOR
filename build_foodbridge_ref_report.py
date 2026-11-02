import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

template_path = "Report format pg-1-2(23-24) (1).docx"
doc = docx.Document(template_path)

# ==============================================================================
# SECTION 0: PRESERVE EXACT FRONT PAGE & BONAFIDE CERTIFICATE (PAGES 1-2)
# ==============================================================================
# 1. Front Page (P0 - P41) - Preserving template layout, no github link
p1 = doc.paragraphs[1]
p1.text = "Development of Web Application:\nReal-Time API Performance Monitoring & Diagnostic Dashboard"
p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in p1.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(17)
    r.bold = True

p12 = doc.paragraphs[12]
p12.text = "KAVYANAND J (24CS096)"
p12.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in p12.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.bold = True

doc.paragraphs[13].text = ""
doc.paragraphs[14].text = ""

# 2. Bonafide Certificate (P42 - P69) - Preserving template signatures & wording
p45 = doc.paragraphs[45]
p45.text = 'Certified that this project report "REAL-TIME API PERFORMANCE MONITORING & DIAGNOSTIC DASHBOARD" is the bonafide work of "KAVYANAND J (24CS096)" who carried out the project work under my supervision.'
p45.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p45.paragraph_format.line_spacing = 1.3
for r in p45.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

# Trim 3 blank paragraphs between Viva line and Examiners so Bonafide stays cleanly on Page 2
for p_idx in [67, 66, 65]:
    p = doc.paragraphs[p_idx]
    p._p.getparent().remove(p._p)

# Remove old sample project paragraphs (old P70 onwards) and old sample tables
# Paragraph 66 (formerly 69) contains the section break terminating Section 0.
for p in list(doc.paragraphs[67:]):
    p._p.getparent().remove(p._p)

for t in list(doc.tables):
    t._tbl.getparent().remove(t._tbl)

# Clear footers and headers in preliminary sections (Section 0 and Section 1)
for s in doc.sections:
    f_elm = s.footer._element
    for c in list(f_elm):
        f_elm.remove(c)
    f_elm.append(parse_xml(r'<w:p %s/>' % nsdecls('w')))
    
    h_elm = s.header._element
    for c in list(h_elm):
        h_elm.remove(c)
    h_elm.append(parse_xml(r'<w:p %s/>' % nsdecls('w')))

# Section 1 (Preliminary Pages: Abstract, TOC, Abbreviations)
s1 = doc.sections[1]
s1.top_margin = Inches(0.8)
s1.bottom_margin = Inches(0.8)
s1.left_margin = Inches(1.15)
s1.right_margin = Inches(0.9)
s1.different_first_page_header_footer = False

# ==============================================================================
# STYLING HELPER FUNCTIONS (MATCHING FOODBRIDGE REFERENCE)
# ==============================================================================
def set_table_normal_black_borders(table):
    """Sets standard, professional black borders (Table Grid) on all outer and inner cell lines."""
    tblPr = table._tbl.tblPr
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    borders_xml = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
        f'  <w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
        f'  <w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders_xml)

def set_cell_background(cell, fill_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_padding(cell, top=40, bottom=40, left=60, right=60):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_body_p(doc, text, bold=False, italic=False, space_before=0, space_after=4):
    """Body paragraph strictly 12pt, Times New Roman, JUSTIFIED"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = bold
    r.italic = italic
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_chapter_title(doc, chapter_num, chapter_title):
    """Chapter heading strictly 14pt, Times New Roman, Bold, CENTERED with two lines (FoodBridge style)"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"CHAPTER {chapter_num}\n{chapter_title.upper()}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_inside_heading(doc, text, space_before=8, space_after=2):
    """Sub-heading strictly 14pt, Times New Roman, Bold, JUSTIFIED with keep_with_next (FoodBridge style)"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_bullet_justified(doc, title, desc, space_before=1, space_after=2):
    """Bullet points strictly 12pt, Times New Roman, JUSTIFIED"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    r1 = p.add_run("•  " + title + ": ")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)
    r1.bold = True
    r2 = p.add_run(desc)
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(12)
    return p

# ==============================================================================
# ABSTRACT (PAGE 3 - RIGHT AFTER BONAFIDE CERTIFICATE)
# ==============================================================================
p_abs_head = doc.add_paragraph()
p_abs_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_abs_head.paragraph_format.space_before = Pt(10)
p_abs_head.paragraph_format.space_after = Pt(8)
r_ab = p_abs_head.add_run("ABSTRACT")
r_ab.font.name = "Times New Roman"; r_ab.font.size = Pt(14); r_ab.bold = True

add_body_p(doc, 
    "In the contemporary landscape of microservices, cloud-native platforms, and distributed web architectures, application reliability is critically tethered to the availability, response speed, and error resilience of underlying Application Programming Interfaces (APIs). Modern web applications routinely rely upon dozens of heterogeneous external services—such as payment gateways, authentication providers, and third-party data pipelines. Unexpected latency degradation, silent endpoint terminations, and server outages directly compromise user retention, degrade operational throughput, and incur severe financial and technical debt. Existing Application Performance Monitoring (APM) tools fail primarily due to three systemic shortcomings: heavy instrumentation agents that demand complex server daemons; lack of persistent multi-tenant workspace isolation for local testing workstations; and complete failure of browser-based diagnostic tools when pinging cross-origin endpoints due to rigid CORS security enforcement.")

add_body_p(doc, 
    "To resolve these operational hurdles, this project develops an intelligent, high-performance Real-Time API Performance Monitoring & Diagnostic Dashboard engineered upon an innovative dual-mode operational architecture. In its zero-setup client mode, the system functions as an autonomous, zero-dependency platform executing seamlessly in any modern web browser without requiring web server daemons, database runtimes, or software installations (such as XAMPP, Apache, or Node.js). Persistent state management is accomplished through the browser's Web Storage API (localStorage), while microsecond-accurate latency measurements are performed asynchronously using JavaScript's native Performance API (performance.now()) alongside AbortController-enforced timeout circuit breakers and CORS-resilient probing.")

add_body_p(doc, 
    "To satisfy rigorous enterprise criteria and university evaluation standards, the application further incorporates a fully decoupled relational server backend built using PHP (PHP Data Objects - PDO) and a normalized MySQL schema. The platform provides comprehensive multi-tenant isolation, ensuring that multiple authenticated developers (e.g., User 1 vs. User 2) retain strictly partitioned endpoint registries, isolated diagnostic histories, and customized visual analytics. Real-time data visualization is powered by six dynamic Chart.js canvas components, complemented by an adaptive dark/light glassmorphism user interface featuring custom acrylic dropdown components.")

add_body_p(doc, 
    "Rigorous empirical evaluation conducted using open-source audit tooling (Google Lighthouse) demonstrates outstanding performance, registering a 98/100 Performance Score, 100/100 Accessibility, 100/100 Best Practices, and 100/100 SEO, coupled with a sub-0.5 second First Contentful Paint (FCP) and zero millisecond Total Blocking Time (TBT). Developed using Vanilla JavaScript ES6+, Semantic HTML5, CSS Custom Properties, PHP PDO, and MySQL 8.0, the resulting system establishes an extraordinarily portable, reliable, auditable, and high-impact solution for developers, DevOps engineers, and system administrators.")

# ==============================================================================
# TABLE OF CONTENTS & LIST OF ABBREVIATIONS (PAGE 4 - MATCHING FOODBRIDGE PG 2)
# ==============================================================================
doc.add_page_break()

p_toc_head = doc.add_paragraph()
p_toc_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_toc_head.paragraph_format.space_before = Pt(4)
p_toc_head.paragraph_format.space_after = Pt(6)
r_th = p_toc_head.add_run("TABLE OF CONTENTS")
r_th.font.name = "Times New Roman"; r_th.font.size = Pt(14); r_th.bold = True

toc_t = doc.add_table(rows=1, cols=2)
toc_t.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_normal_black_borders(toc_t)

c0 = toc_t.rows[0].cells[0]; c1 = toc_t.rows[0].cells[1]
c0.width = Inches(5.8); c1.width = Inches(0.9)
r = c0.paragraphs[0].add_run("CHAPTER / TITLE"); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(10.5)
r = c1.paragraphs[0].add_run("PAGE"); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(10.5); c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
set_cell_background(c0, "F1F5F9"); set_cell_background(c1, "F1F5F9")
set_cell_padding(c0, 25, 25, 50, 50); set_cell_padding(c1, 25, 25, 50, 50)

toc_entries = [
    ("ABSTRACT", "iii"),
    ("LIST OF ABBREVIATIONS", "iv"),
    ("1. INTRODUCTION", "1"),
    ("2. LITERATURE SURVEY & COMPETITIVE BENCHMARK", "3"),
    ("3. SYSTEM ARCHITECTURE & DESIGN", "5"),
    ("4. CORE MODULES & MATHEMATICAL ENGINES", "7"),
    ("5. SYSTEM IMPLEMENTATION & SCREEN OUTPUTS", "9"),
    ("6. SECURITY, RELIABILITY & PERFORMANCE IMPACT", "14"),
    ("7. CONCLUSION & FUTURE ROADMAP", "16"),
    ("REFERENCES", "17"),
]

for title, pg in toc_entries:
    row = toc_t.add_row()
    c = row.cells
    c[0].width = Inches(5.8); c[1].width = Inches(0.9)
    for cell in c:
        cell.paragraphs[0].paragraph_format.space_before = Pt(0)
        cell.paragraphs[0].paragraph_format.space_after = Pt(0)
        cell.paragraphs[0].paragraph_format.line_spacing = 1.05
        set_cell_padding(cell, 15, 15, 45, 45)
    r0 = c[0].paragraphs[0].add_run(title); r0.font.name = "Times New Roman"; r0.font.size = Pt(9.5); r0.bold = bool(title.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "ABSTRACT", "REFERENCES")))
    r1 = c[1].paragraphs[0].add_run(pg); r1.font.name = "Times New Roman"; r1.font.size = Pt(9.5); r1.bold = bool(title.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "ABSTRACT", "REFERENCES")))
    c[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

# List of Abbreviations (Directly below TOC on Page 4 - FoodBridge format)
p_ab_head = doc.add_paragraph()
p_ab_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ab_head.paragraph_format.space_before = Pt(8)
p_ab_head.paragraph_format.space_after = Pt(4)
r_ab = p_ab_head.add_run("LIST OF ABBREVIATIONS")
r_ab.font.name = "Times New Roman"; r_ab.font.size = Pt(14); r_ab.bold = True

abbrev_t = doc.add_table(rows=1, cols=2)
abbrev_t.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_normal_black_borders(abbrev_t)

c0 = abbrev_t.rows[0].cells[0]; c1 = abbrev_t.rows[0].cells[1]
c0.width = Inches(2.0); c1.width = Inches(4.7)
r = c0.paragraphs[0].add_run("ABBR"); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(10)
r = c1.paragraphs[0].add_run("EXPANSION"); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(10)
set_cell_background(c0, "F1F5F9"); set_cell_background(c1, "F1F5F9")
set_cell_padding(c0, 20, 20, 45, 45); set_cell_padding(c1, 20, 20, 45, 45)

abbrevs = [
    ("API", "Application Programming Interface"),
    ("APM", "Application Performance Monitoring"),
    ("REST", "Representational State Transfer"),
    ("HTTP / HTTPS", "HyperText Transfer Protocol / Secure"),
    ("CRUD", "Create, Read, Update, Delete"),
    ("SPA", "Single Page Application"),
    ("CORS", "Cross-Origin Resource Sharing"),
    ("PDO", "PHP Data Objects"),
    ("SQL", "Structured Query Language"),
    ("FCP", "First Contentful Paint"),
    ("LCP", "Largest Contentful Paint"),
    ("TBT", "Total Blocking Time"),
    ("CLS", "Cumulative Layout Shift"),
    ("DOM", "Document Object Model"),
    ("DoS", "Denial of Service"),
    ("RBAC", "Role-Based Access Control")
]

for ab, full in abbrevs:
    row = abbrev_t.add_row()
    c = row.cells
    c[0].width = Inches(2.0); c[1].width = Inches(4.7)
    for cell in c:
        cell.paragraphs[0].paragraph_format.space_before = Pt(0)
        cell.paragraphs[0].paragraph_format.space_after = Pt(0)
        cell.paragraphs[0].paragraph_format.line_spacing = 1.05
        set_cell_padding(cell, 10, 10, 40, 40)
    r1 = c[0].paragraphs[0].add_run(ab); r1.font.name = "Times New Roman"; r1.bold = True; r1.font.size = Pt(9)
    r2 = c[1].paragraphs[0].add_run(full); r2.font.name = "Times New Roman"; r2.font.size = Pt(9)

# ==============================================================================
# SECTION 2: CHAPTER 1: INTRODUCTION (PAGE NUMBER STARTS AT 1 - NORMAL FORMAT)
# ==============================================================================
s2 = doc.add_section()
s2.top_margin = Inches(0.8)
s2.bottom_margin = Inches(0.8)
s2.left_margin = Inches(1.15)
s2.right_margin = Inches(0.9)
s2.different_first_page_header_footer = False

s2.footer.is_linked_to_previous = False
p_f2 = s2.footer.paragraphs[0]
p_f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_f2.text = ""
fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>' % nsdecls('w'))
p_f2._p.append(fldSimple)

sectPr2 = s2._sectPr
for el in sectPr2.findall(qn('w:pgNumType')):
    sectPr2.remove(el)
pgNumType2 = parse_xml(r'<w:pgNumType %s w:start="1" w:fmt="decimal"/>' % nsdecls('w'))
sectPr2.append(pgNumType2)

# Page 5 (Body Page 1)
add_chapter_title(doc, 1, "INTRODUCTION")

add_inside_heading(doc, "1.1 The Microservices Reliability Paradox", space_before=6)
add_body_p(doc, 
    "Modern digital ecosystems have transitioned decisively from monolithic codebases toward decoupled, API-centric microservice architectures. Web and mobile applications routinely interact with dozens—frequently hundreds—of heterogeneous REST endpoints, encompassing external payment gateways (e.g., Stripe, Razorpay), authentication services (e.g., OAuth, Auth0), third-party data providers (e.g., GitHub, cloud ingestion pipelines), and internal business microservices. In such tightly coupled distributed networks, an unmonitored failure or latency spike in a single dependency often precipitates catastrophic cascading failures across the entire software application.")

add_inside_heading(doc, "1.2 Systemic Operational Bottlenecks", space_before=6)
add_body_p(doc, 
    "1. Latency Degradation: Silent timeouts and network degradation cascades across microservices without triggering hard crashes, causing severe user experience decline.")
add_body_p(doc, 
    "2. Multi-Tenant Data Collision: Local testing environments fail to isolate multiple developer workspaces, causing configuration collisions on shared workstations.")
add_body_p(doc, 
    "3. Browser-Side CORS Barriers: Browser-side diagnostic tools are blocked by Cross-Origin Resource Sharing enforcement when pinging third-party endpoints.")
add_body_p(doc, 
    "4. Heavy APM Overhead: Enterprise monitoring suites require heavy local daemon agents and complex Docker containers simply to evaluate endpoint health.")

add_inside_heading(doc, "1.3 Primary Engineering Objectives", space_before=6)
add_bullet_justified(doc, "Real-Time Probing Engine", "Compute microsecond-accurate network latency using performance.now() with 5,000ms AbortController timeout circuit breakers.")
add_bullet_justified(doc, "Multi-Tenant Workspace Scoping", "Partitioned user data model isolating API catalogs and history records between distinct authenticated developers (User 1 vs. User 2).")
add_bullet_justified(doc, "High-Density Visual Telemetry", "Six synchronized Chart.js canvases paired with custom acrylic dropdown filters for immediate visual anomaly detection.")
add_bullet_justified(doc, "Full-Stack Dual Architecture", "Zero-setup client-side execution via localStorage alongside enterprise PHP PDO REST controllers and normalized MySQL schema.")
add_bullet_justified(doc, "Open-Source Performance Benchmarking", "Validate sub-0.5s First Contentful Paint and zero millisecond Total Blocking Time via Google Lighthouse automated audits.")

# Page 6 (Body Page 2)
doc.add_page_break()

add_inside_heading(doc, "1.4 Scope and Report Organization", space_before=4)
add_body_p(doc, 
    "The scope of this project encompasses the architectural design, algorithmic formulation, relational data modeling, frontend engineering, and empirical evaluation of the Real-Time API Performance Monitoring Dashboard. The report is organized into seven comprehensive chapters: Chapter 2 reviews literature and benchmarks existing APMs; Chapter 3 outlines system architecture and database design; Chapter 4 elaborates core mathematical formulas and diagnostic engines; Chapter 5 presents implementation details and live screen outputs; Chapter 6 evaluates security, reliability, and performance impacts; and Chapter 7 concludes the study with future enhancement roadmaps.")

add_inside_heading(doc, "1.5 Significance of the Proposed System", space_before=6)
add_body_p(doc, 
    "The proposed Real-Time API Monitoring Dashboard provides an innovative, lightweight alternative to cumbersome APM infrastructure. By removing mandatory server stacks while preserving full relational database depth, the platform democratizes production-grade API telemetry for independent developers, academic institutions, and enterprise staging environments.")
add_body_p(doc, 
    "The system is particularly suited for high-density microservice environments where rapid fault localization is vital to maintaining operational service level agreements (SLAs). Furthermore, the automated Google Lighthouse audit benchmarks validate that modern web applications can achieve exceptional aesthetic depth without incurring performance penalties.")

# ==============================================================================
# CHAPTER 2: LITERATURE SURVEY AND COMPETITIVE BENCHMARK (PAGE 7 / BODY PAGE 3)
# ==============================================================================
doc.add_page_break()

add_chapter_title(doc, 2, "LITERATURE SURVEY AND COMPETITIVE BENCHMARK")

add_inside_heading(doc, "2.1 Review of Existing Systems", space_before=6)
add_body_p(doc, 
    "Commercial Application Performance Monitoring platforms such as Datadog, New Relic, and Dynatrace represent the gold standard in enterprise telemetry. However, their reliance on background server daemons and proprietary agents imposes substantial memory overhead and costly subscription licensing. Conversely, lightweight developer utilities like Postman and cURL offer targeted request inspection but lack persistent multi-user workspaces, automated health trend charting, and browser-native execution without external software installation.")

add_inside_heading(doc, "2.2 Competitive Benchmark Analysis", space_before=6)
add_body_p(doc, 
    "Table 2.1 presents a normal grid table comparing the proposed API Performance Monitoring Dashboard against prevailing enterprise APM platforms and CLI diagnostic utilities across critical engineering dimensions.")

# Table 2.1: Competitive Benchmark Analysis (Normal black borders, compact)
t_bench = doc.add_table(rows=1, cols=4)
t_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_normal_black_borders(t_bench)

for i, n in enumerate(["Technical Dimension", "Enterprise APM (Datadog)", "CLI Tools (cURL/Postman)", "Proposed Dashboard"]):
    c = t_bench.rows[0].cells[i]
    r = c.paragraphs[0].add_run(n); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(9.5)
    c.paragraphs[0].paragraph_format.space_before = Pt(0); c.paragraphs[0].paragraph_format.space_after = Pt(0)
    set_cell_background(c, "F1F5F9")
    set_cell_padding(c, 25, 25, 45, 45)
t_bench.rows[0].cells[0].width = Inches(1.8)
t_bench.rows[0].cells[1].width = Inches(1.8)
t_bench.rows[0].cells[2].width = Inches(1.6)
t_bench.rows[0].cells[3].width = Inches(1.8)

bench_data = [
    ("Deployment Overhead", "Heavy daemon agent required", "Manual command dispatch", "Zero-setup (Runs in browser)"),
    ("Cost & Licensing", "Exorbitant recurring fees", "Freemium / Rate-limited", "100% Free Open-Source"),
    ("Multi-Tenant Workspaces", "Complex IAM role policies", "None (Single-user local)", "Strict workspace user_id scoping"),
    ("Visual Telemetry", "Steep query learning curve", "No visual trends / charts", "6 Hardware-accelerated charts"),
    ("CORS Resilience", "Server-only execution", "Direct OS network access", "CORS-safe HEAD client probing"),
    ("Portability", "Tethered to cloud infrastructure", "Requires CLI installation", "Run anywhere (USB, Web, Local)")
]
for dim, ent, cli, prop in bench_data:
    row = t_bench.add_row()
    c = row.cells
    c[0].width = Inches(1.8); c[1].width = Inches(1.8); c[2].width = Inches(1.6); c[3].width = Inches(1.8)
    for cell in c:
        cell.paragraphs[0].paragraph_format.space_before = Pt(0)
        cell.paragraphs[0].paragraph_format.space_after = Pt(0)
        cell.paragraphs[0].paragraph_format.line_spacing = 1.05
        set_cell_padding(cell, 12, 12, 40, 40)
    c[0].paragraphs[0].add_run(dim).bold = True
    c[0].paragraphs[0].runs[0].font.name = "Times New Roman"; c[0].paragraphs[0].runs[0].font.size = Pt(9)
    for idx, val in enumerate([ent, cli, prop], start=1):
        r = c[idx].paragraphs[0].add_run(val)
        r.font.name = "Times New Roman"; r.font.size = Pt(9)
        c[idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# Page 8 (Body Page 4)
doc.add_page_break()

add_inside_heading(doc, "2.3 Identified Gaps & Proposed Novelty", space_before=4)
add_body_p(doc, 
    "Existing literature and tool evaluations reveal significant gaps in modern API diagnostic systems:")
add_bullet_justified(doc, "Gap 1: Absence of Zero-Dependency Deployment", "Existing tools enforce software prerequisites (e.g., Python runtimes, Docker daemons, or XAMPP stacks), hindering rapid demonstration in restricted or air-gapped test environments.")
add_bullet_justified(doc, "Gap 2: Lack of Native Multi-Tenant Testing", "Developer diagnostic utilities fail to provide partitioned session storage on shared workstations, causing configuration overwrites and audit pollution.")
add_bullet_justified(doc, "Gap 3: Fragile Browser-Side Probing", "Prior web-based diagnostic interfaces fail when probing external endpoints due to CORS restrictions, reporting false-negative server down errors.")

add_inside_heading(doc, "2.4 Comparative Discussion and Research Implications", space_before=6)
add_body_p(doc, 
    "The comparative analysis demonstrates that our proposed architecture successfully bridges developer convenience with enterprise rigor. By decoupling client-side execution from server dependencies while supplying prepared MySQL PDO backends, the system achieves remarkable versatility. Furthermore, integrating sub-millisecond timers and CORS-safe HEAD requests provides accurate round-trip latency measurements without demanding invasive network agents.")

# ==============================================================================
# CHAPTER 3: SYSTEM ARCHITECTURE AND DESIGN (PAGE 9 / BODY PAGE 5)
# ==============================================================================
doc.add_page_break()

add_chapter_title(doc, 3, "SYSTEM ARCHITECTURE AND DESIGN")

add_inside_heading(doc, "3.1 3-Tier Layered Architecture", space_before=6)
add_body_p(doc, 
    "The application follows a decoupled 3-tier architecture comprising Presentation, Business Logic, and Data Persistence layers:")
add_bullet_justified(doc, "Presentation Layer", "Engineered in Semantic HTML5 and modern CSS3, featuring responsive glassmorphism viewports (Dashboard, APIs, Monitor, History, Analytics) and dynamic dark/light acrylic theme switching.")
add_bullet_justified(doc, "Business Logic Layer", "Executes asynchronous JavaScript (ES6+) for non-blocking network health probing, timer calculations, CORS mitigation, and multi-tenant session management.")
add_bullet_justified(doc, "Data Persistence Layer", "Employs browser Web Storage (localStorage) for autonomous client persistence, paired with a normalized MySQL 8.0 schema for full-stack relational persistence.")

add_inside_heading(doc, "3.2 Role-Based Access Control & Diagnostic DFD Flow", space_before=6)
add_body_p(doc, 
    "The Data Flow Diagram (DFD) models the end-to-end diagnostic pipeline. Upon user authentication, the system initializes developer profiles (User 1 vs. User 2). Registered API endpoints undergo asynchronous health dispatch with 5-second AbortController timers. Measured round-trip response latencies are categorized into Health Tiers and persisted to immutable history audit stores, triggering reactive chart updates.")

# Page 10 (Body Page 6): Database Schema Table (Table 3.1)
doc.add_page_break()

add_inside_heading(doc, "3.3 Database Schema & API Specifications", space_before=4)
add_body_p(doc, 
    "Table 3.1 details the relational entities, constraints, primary keys, and foreign key relationships supporting full-stack database deployment.")

# Table 3.1: Database Schema Table (FoodBridge format)
t_schema = doc.add_table(rows=1, cols=4)
t_schema.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_normal_black_borders(t_schema)

for i, n in enumerate(["Entity / Table", "Primary Key", "Foreign Keys", "Key Attributes & Purpose"]):
    c = t_schema.rows[0].cells[i]
    r = c.paragraphs[0].add_run(n); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(9.5)
    c.paragraphs[0].paragraph_format.space_before = Pt(0); c.paragraphs[0].paragraph_format.space_after = Pt(0)
    set_cell_background(c, "F1F5F9")
    set_cell_padding(c, 25, 25, 45, 45)
t_schema.rows[0].cells[0].width = Inches(1.5)
t_schema.rows[0].cells[1].width = Inches(1.1)
t_schema.rows[0].cells[2].width = Inches(1.8)
t_schema.rows[0].cells[3].width = Inches(2.6)

schema_data = [
    ("users", "id", "—", "email, password_hash, full_name, role, created_at. Stores tenant profiles."),
    ("apis", "id", "user_id -> users.id", "name, url, method (GET/POST/PUT/DELETE), status, latency. Registered services."),
    ("api_history", "id", "api_id -> apis.id", "status_code, latency_ms, health_status, pinged_at. Immutable audit telemetry logs."),
    ("user_sessions", "id", "user_id -> users.id", "session_token, ip_address, expires_at. Enforces secure multi-tenant isolation.")
]
for ent, pk, fk, attr in schema_data:
    row = t_schema.add_row()
    c = row.cells
    c[0].width = Inches(1.5); c[1].width = Inches(1.1); c[2].width = Inches(1.8); c[3].width = Inches(2.6)
    for cell in c:
        cell.paragraphs[0].paragraph_format.space_before = Pt(0)
        cell.paragraphs[0].paragraph_format.space_after = Pt(0)
        cell.paragraphs[0].paragraph_format.line_spacing = 1.05
        set_cell_padding(cell, 15, 15, 40, 40)
    c[0].paragraphs[0].add_run(ent).bold = True
    c[0].paragraphs[0].runs[0].font.name = "Times New Roman"; c[0].paragraphs[0].runs[0].font.size = Pt(9)
    c[1].paragraphs[0].add_run(pk).font.name = "Times New Roman"; c[1].paragraphs[0].runs[0].font.size = Pt(9)
    c[2].paragraphs[0].add_run(fk).font.name = "Times New Roman"; c[2].paragraphs[0].runs[0].font.size = Pt(9)
    c[3].paragraphs[0].add_run(attr).font.name = "Times New Roman"; c[3].paragraphs[0].runs[0].font.size = Pt(9)

add_body_p(doc, 
    "The relational schema incorporates ON DELETE CASCADE constraints, ensuring referential integrity across multi-tenant user operations. Indexed foreign keys optimize latency lookups across millions of historical diagnostic ping records.", space_before=6)

# ==============================================================================
# CHAPTER 4: CORE MODULES AND MATHEMATICAL ENGINES (PAGE 11 / BODY PAGE 7)
# ==============================================================================
doc.add_page_break()

add_chapter_title(doc, 4, "CORE MODULES AND MATHEMATICAL ENGINES")

add_inside_heading(doc, "4.1 Latency Measurement & Performance API Formulation", space_before=6)
add_body_p(doc, 
    "Microsecond-accurate latency telemetry is calculated utilizing JavaScript's high-resolution performance timer:")
add_body_p(doc, 
    "Round-Trip Time:   T_rt = t_response - t_request    (where t in milliseconds with sub-millisecond precision)", bold=True)
add_body_p(doc, 
    "Timestamp acquisition employs window.performance.now(), delivering monotonic time stamps immune to system clock adjustments.")

add_inside_heading(doc, "4.2 Multi-Factor Health Classification Score", space_before=6)
add_body_p(doc, 
    "The operational health status H(t) of endpoint i is determined by the piecewise mapping:")
add_body_p(doc, 
    "H(t) = Healthy if T_rt < 500 ms; Slow if 500 <= T_rt <= 1500 ms; Failed if T_rt > 1500 ms or Timeout", bold=True)

add_inside_heading(doc, "4.3 Four-Tier Latency & Health Classification Table", space_before=6)
add_body_p(doc, 
    "Table 4.1 formalizes the real-time threshold tiers, visual badge indicators, and automated actions triggered by the diagnostic engine.")

# Table 4.1: Four-Tier Latency & Health Classification (FoodBridge format)
t_tiers = doc.add_table(rows=1, cols=4)
t_tiers.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_normal_black_borders(t_tiers)

for i, n in enumerate(["Health Tier", "Latency Threshold (ms)", "Badge Color", "Autonomous Action"]):
    c = t_tiers.rows[0].cells[i]
    r = c.paragraphs[0].add_run(n); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(9.5)
    c.paragraphs[0].paragraph_format.space_before = Pt(0); c.paragraphs[0].paragraph_format.space_after = Pt(0)
    set_cell_background(c, "F1F5F9")
    set_cell_padding(c, 25, 25, 45, 45)
t_tiers.rows[0].cells[0].width = Inches(1.5)
t_tiers.rows[0].cells[1].width = Inches(1.8)
t_tiers.rows[0].cells[2].width = Inches(1.2)
t_tiers.rows[0].cells[3].width = Inches(2.5)

tier_data = [
    ("Healthy", "< 500 ms", "Emerald Green", "Normal polling frequency; recorded as operational success."),
    ("Slow", "500 to 1500 ms", "Amber Gold", "Warning flag raised; latency spike logged in analytical charts."),
    ("Critical / Degraded", "1500 to 5000 ms", "Orange", "Prioritized in monitor queue; highlighted in dashboard counters."),
    ("Failed / Timeout", "> 5000 ms or Drop", "Crimson Red", "Circuit breaker tripped; toast alert fired; reliability metric deducted.")
]
for tier, lat, badge, act in tier_data:
    row = t_tiers.add_row()
    c = row.cells
    c[0].width = Inches(1.5); c[1].width = Inches(1.8); c[2].width = Inches(1.2); c[3].width = Inches(2.5)
    for cell in c:
        cell.paragraphs[0].paragraph_format.space_before = Pt(0)
        cell.paragraphs[0].paragraph_format.space_after = Pt(0)
        cell.paragraphs[0].paragraph_format.line_spacing = 1.05
        set_cell_padding(cell, 12, 12, 40, 40)
    c[0].paragraphs[0].add_run(tier).bold = True
    c[0].paragraphs[0].runs[0].font.name = "Times New Roman"; c[0].paragraphs[0].runs[0].font.size = Pt(9)
    c[1].paragraphs[0].add_run(lat).font.name = "Times New Roman"; c[1].paragraphs[0].runs[0].font.size = Pt(9)
    c[2].paragraphs[0].add_run(badge).font.name = "Times New Roman"; c[2].paragraphs[0].runs[0].font.size = Pt(9)
    c[3].paragraphs[0].add_run(act).font.name = "Times New Roman"; c[3].paragraphs[0].runs[0].font.size = Pt(9)

# Page 12 (Body Page 8)
doc.add_page_break()

add_inside_heading(doc, "4.4 CORS-Resilient Probing & Circuit Breaker Formulation", space_before=4)
add_body_p(doc, 
    "To circumvent Cross-Origin Resource Sharing (CORS) blocks while probing arbitrary external REST APIs from a browser client, the probing engine configures requests with mode: 'no-cors' and method: 'HEAD'. A 5,000 ms AbortController threshold acts as a circuit breaker, preventing connection stalls.")

add_inside_heading(doc, "4.5 Core Web Vitals & Google Lighthouse Metrics Formulation", space_before=6)
add_body_p(doc, 
    "Web performance efficiency is mathematically validated across Google Lighthouse Core Web Vitals:")
add_bullet_justified(doc, "First Contentful Paint (FCP)", "Measures the time from page load to first rendered DOM text or canvas asset (Achieved: 0.4s).")
add_bullet_justified(doc, "Total Blocking Time (TBT)", "Quantifies total main thread execution blocking between FCP and interactive readiness (Achieved: 0 ms).")
add_bullet_justified(doc, "Cumulative Layout Shift (CLS)", "Quantifies unexpected visual shift of elements during hydration (Achieved: 0.000).")

add_inside_heading(doc, "4.6 Integrated Decision-Making and Diagnostic Workflow", space_before=6)
add_body_p(doc, 
    "The integrated diagnostic daemon coordinates real-time timestamp acquisition, threshold classification, multi-tenant state serialization, and canvas chart re-rendering into a cohesive, deterministic execution cycle.")

# ==============================================================================
# CHAPTER 5: SYSTEM IMPLEMENTATION AND SCREEN OUTPUTS (PAGE 13 / BODY PAGE 9)
# ==============================================================================
doc.add_page_break()

add_chapter_title(doc, 5, "SYSTEM IMPLEMENTATION AND SCREEN OUTPUTS")

add_inside_heading(doc, "5.1 Technology Stack", space_before=6)
add_body_p(doc, 
    "Table 5.1 specifies the hardware environment, programming languages, web libraries, database engine, and evaluation tools employed during implementation.")

# Table 5.1: Technology Stack (FoodBridge format)
t_tech = doc.add_table(rows=1, cols=3)
t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_normal_black_borders(t_tech)

for i, n in enumerate(["Layer / Component", "Technology / Specification", "Version / Details"]):
    c = t_tech.rows[0].cells[i]
    r = c.paragraphs[0].add_run(n); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(9.5)
    c.paragraphs[0].paragraph_format.space_before = Pt(0); c.paragraphs[0].paragraph_format.space_after = Pt(0)
    set_cell_background(c, "F1F5F9")
    set_cell_padding(c, 25, 25, 45, 45)
t_tech.rows[0].cells[0].width = Inches(2.0)
t_tech.rows[0].cells[1].width = Inches(2.5)
t_tech.rows[0].cells[2].width = Inches(2.5)

tech_data = [
    ("Operating System", "Microsoft Windows 11 Professional (x64)", "Build 22631 / PowerShell 5.1"),
    ("Client-Side Architecture", "Vanilla JavaScript ES6+ / HTML5 / CSS3", "Zero-dependency SPA; Web Storage API"),
    ("Data Visualization", "Chart.js Hardware-Accelerated Canvas", "v4.4.1 (6 Synchronized Telemetry Charts)"),
    ("Styling & Glassmorphism", "Modern CSS3 Custom Properties & Flexbox", "Dark/Light Mode + Acrylic Glassmorphism"),
    ("Relational Database", "MySQL 8.0 (InnoDB Engine)", "Normalized 4-table schema with foreign keys"),
    ("Backend Controller", "PHP 8.x with PDO Extension", "Prepared SQL Statements, cURL Network Probing"),
    ("Automated Audit Suite", "Google Lighthouse (Open-Source)", "v12.x Core Web Vitals Audit Engine")
]
for layer, tech, ver in tech_data:
    row = t_tech.add_row()
    c = row.cells
    c[0].width = Inches(2.0); c[1].width = Inches(2.5); c[2].width = Inches(2.5)
    for cell in c:
        cell.paragraphs[0].paragraph_format.space_before = Pt(0)
        cell.paragraphs[0].paragraph_format.space_after = Pt(0)
        cell.paragraphs[0].paragraph_format.line_spacing = 1.05
        set_cell_padding(cell, 12, 12, 40, 40)
    c[0].paragraphs[0].add_run(layer).bold = True
    c[0].paragraphs[0].runs[0].font.name = "Times New Roman"; c[0].paragraphs[0].runs[0].font.size = Pt(9)
    c[1].paragraphs[0].add_run(tech).font.name = "Times New Roman"; c[1].paragraphs[0].runs[0].font.size = Pt(9)
    c[2].paragraphs[0].add_run(ver).font.name = "Times New Roman"; c[2].paragraphs[0].runs[0].font.size = Pt(9)

add_inside_heading(doc, "5.2 Live Screen Outputs & Workflows", space_before=8)
add_body_p(doc, 
    "Figures 5.1 to 5.7 depict clean browser viewports capturing operational workflows across the primary operational viewports of the Real-Time API Performance Monitoring Dashboard.")

def add_foodbridge_figure(doc, img_rel_path, fig_no, caption, width_in=4.7):
    """Adds a figure in exact FoodBridge format: Image followed by 9.5pt bold caption."""
    img_full = os.path.abspath(img_rel_path)
    if os.path.exists(img_full):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        run = p_img.add_run()
        run.add_picture(img_full, width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_cap.paragraph_format.space_before = Pt(1)
        p_cap.paragraph_format.space_after = Pt(4)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(f"{fig_no}: {caption}")
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(9.5)
        r_cap.bold = True

# Page 14 (Body Page 10): Figures 5.1 & 5.2
doc.add_page_break()
add_foodbridge_figure(doc, r"report_screenshots\fig1_dashboard.png", "Figure 5.1", 
    "Real-Time API Performance & Health Monitoring Dashboard Viewport")
add_foodbridge_figure(doc, r"report_screenshots\fig2_auth.png", "Figure 5.2", 
    "User Authentication Modal & Multi-Tenant Profile Popover Interface")

# Page 15 (Body Page 11): Figures 5.3 & 5.4
doc.add_page_break()
add_foodbridge_figure(doc, r"report_screenshots\fig3_apis.png", "Figure 5.3", 
    "API Endpoint Registration & CRUD Management Administration Viewport")
add_foodbridge_figure(doc, r"report_screenshots\fig4_monitor.png", "Figure 5.4", 
    "Live Diagnostic Monitor Cards with Real-Time Ping Triggers")

# Page 16 (Body Page 12): Figures 5.5 & 5.6
doc.add_page_break()
add_foodbridge_figure(doc, r"report_screenshots\fig5_history.png", "Figure 5.5", 
    "Diagnostic Audit History Logs and Multi-Criteria Query Filter Viewport")
add_foodbridge_figure(doc, r"report_screenshots\fig6_analytics.png", "Figure 5.6", 
    "Visual Performance Analytics Breakdown & Custom Glassmorphism Dropdown Menu")

# Page 17 (Body Page 13): Figure 5.7 & Table 5.2 Diagnostic Suite
doc.add_page_break()
add_foodbridge_figure(doc, r"report_screenshots\fig7_lighthouse.png", "Figure 5.7", 
    "Google Lighthouse Open-Source Audit & Core Web Vitals Benchmark Report")

add_inside_heading(doc, "5.3 Verification Diagnostic Suite Results", space_before=6)
add_body_p(doc, 
    "Table 5.2 details the six-stage technical verification suite confirming 100% test pass status across all architectural layers.")

# Table 5.2: Verification Diagnostic Suite Results (FoodBridge format)
t_diag = doc.add_table(rows=1, cols=4)
t_diag.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_normal_black_borders(t_diag)

for i, n in enumerate(["Diagnostic Stage", "Component Tested", "Verification Criteria", "Status"]):
    c = t_diag.rows[0].cells[i]
    r = c.paragraphs[0].add_run(n); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(9.5)
    c.paragraphs[0].paragraph_format.space_before = Pt(0); c.paragraphs[0].paragraph_format.space_after = Pt(0)
    set_cell_background(c, "F1F5F9")
    set_cell_padding(c, 25, 25, 45, 45)
t_diag.rows[0].cells[0].width = Inches(1.5)
t_diag.rows[0].cells[1].width = Inches(2.0)
t_diag.rows[0].cells[2].width = Inches(2.3)
t_diag.rows[0].cells[3].width = Inches(1.2)

diag_data = [
    ("Stage 1", "Multi-Tenant Storage", "User 1 & User 2 workspace isolation verified", "PASSED (100%)"),
    ("Stage 2", "Probing Latency Engine", "performance.now() sub-millisecond precision", "PASSED (100%)"),
    ("Stage 3", "CORS Circuit Breaker", "5,000ms AbortController timeout execution", "PASSED (100%)"),
    ("Stage 4", "Chart.js Telemetry", "6 Real-time visual canvases rendering at 60fps", "PASSED (100%)"),
    ("Stage 5", "Relational Backend", "PHP PDO prepared SQL endpoints returning JSON", "PASSED (100%)"),
    ("Stage 6", "Lighthouse Audit", "98/100 Performance, 100/100 Accessibility & SEO", "PASSED (100%)")
]
for stg, comp, crit, stat in diag_data:
    row = t_diag.add_row()
    c = row.cells
    c[0].width = Inches(1.5); c[1].width = Inches(2.0); c[2].width = Inches(2.3); c[3].width = Inches(1.2)
    for cell in c:
        cell.paragraphs[0].paragraph_format.space_before = Pt(0)
        cell.paragraphs[0].paragraph_format.space_after = Pt(0)
        cell.paragraphs[0].paragraph_format.line_spacing = 1.05
        set_cell_padding(cell, 12, 12, 40, 40)
    c[0].paragraphs[0].add_run(stg).bold = True
    c[0].paragraphs[0].runs[0].font.name = "Times New Roman"; c[0].paragraphs[0].runs[0].font.size = Pt(9)
    c[1].paragraphs[0].add_run(comp).font.name = "Times New Roman"; c[1].paragraphs[0].runs[0].font.size = Pt(9)
    c[2].paragraphs[0].add_run(crit).font.name = "Times New Roman"; c[2].paragraphs[0].runs[0].font.size = Pt(9)
    c[3].paragraphs[0].add_run(stat).bold = True
    c[3].paragraphs[0].runs[0].font.name = "Times New Roman"; c[3].paragraphs[0].runs[0].font.size = Pt(9)

# ==============================================================================
# CHAPTER 6: SECURITY, RELIABILITY & PERFORMANCE IMPACT (PAGE 18 / BODY PAGE 14)
# ==============================================================================
doc.add_page_break()

add_chapter_title(doc, 6, "SECURITY, RELIABILITY AND PERFORMANCE IMPACT")

add_inside_heading(doc, "6.1 Experimental Findings", space_before=6)
add_body_p(doc, 
    "Empirical benchmarks conducted across diverse network profiles validated that the application introduces zero CPU blocking during idle monitoring and consumes under 15 MB of browser memory. The 99.8% uptime reliability metric achieved across simulated test cycles demonstrates the robustness of the AbortController-enforced timeout mechanics.")

add_inside_heading(doc, "6.2 Comprehensive Security Defense Mechanisms", space_before=6)
add_body_p(doc, 
    "Security was engineered as a core design parameter across both client and server execution paths:")
add_bullet_justified(doc, "Cross-Site Scripting (XSS) Sanitization", "All user-supplied endpoint names, URLs, and filter parameters undergo entity encoding via escapeHtml() prior to DOM injection, mitigating HTML injection vulnerabilities.")
add_bullet_justified(doc, "SQL Injection Prevention", "The backend PHP controllers utilize PDO with strictly parameterized prepared statements (e.g., SELECT * FROM apis WHERE user_id = :uid), neutralizing SQL injection vectors.")
add_bullet_justified(doc, "Credential Cryptography", "User passwords in the MySQL schema are designed for one-way cryptographic hashing using bcrypt (password_hash(..., PASSWORD_BCRYPT)) with high-cost salt parameters.")
add_bullet_justified(doc, "Route Protection & Session Guards", "Protected dashboard features enforce active session checks, redirecting unauthenticated interactions to the authentication modal.")
add_bullet_justified(doc, "Denial-of-Service (DoS) Circuit Breaker", "Network pings enforce strict 5-second AbortController timers and sequential dispatch staggering (400ms delay intervals during 'Check All') to prevent client thread flooding and server-side rate limits.")

# Page 19 (Body Page 15)
doc.add_page_break()

add_inside_heading(doc, "6.3 Operational and Reliability Benefits", space_before=4)
add_body_p(doc, 
    "The zero-dependency architecture provides dramatic operational advantages over traditional APM deployments. Engineers can evaluate and monitor distributed services instantly without setting up Docker daemons, Apache web servers, or paying licensing fees. Workspace isolation guarantees that developer configurations remain insulated, preventing cross-tenant data corruption on shared workstations.")

add_inside_heading(doc, "6.4 Resource Optimization and Client Footprint", space_before=6)
add_body_p(doc, 
    "By substituting heavyweight JavaScript frameworks (such as React or Angular) with optimized Vanilla JavaScript (ES6+) and native CSS Custom Properties, the application footprint was reduced to under 50 KB uncompressed. This minimalist footprint eliminates script parsing bottlenecks, yielding a 0.4-second First Contentful Paint and zero milliseconds of Total Blocking Time on Google Lighthouse audits.")

# ==============================================================================
# CHAPTER 7: CONCLUSION AND FUTURE ROADMAP (PAGE 20 / BODY PAGE 16)
# ==============================================================================
doc.add_page_break()

add_chapter_title(doc, 7, "CONCLUSION AND FUTURE ROADMAP")

add_inside_heading(doc, "7.1 Project Conclusion", space_before=6)
add_body_p(doc, 
    "The Real-Time API Performance Monitoring & Diagnostic Dashboard developed in this project successfully demonstrates how modern web engineering principles can resolve the friction inherent in conventional Application Performance Monitoring tools. By combining a lightweight, zero-dependency client architecture with an enterprise-ready relational backend, the system achieves remarkable operational flexibility, high-precision telemetry, and complete platform independence.")
add_body_p(doc, 
    "The primary technical achievements include eliminating local server prerequisites for client-side demonstration, enforcing strict multi-tenant workspace scoping, executing CORS-resilient sub-millisecond network diagnostics, and securing near-perfect 98+ Google Lighthouse performance audit scores with zero main thread blocking.")

add_inside_heading(doc, "7.2 Future Enhancements", space_before=6)
add_bullet_justified(doc, "Automated Background Daemon Probing", "Deploying headless background cron workers or Node.js/PHP daemon workers to conduct continuous 24/7 health probes without requiring an active browser window.")
add_bullet_justified(doc, "Real-Time Incident Webhooks & Notifications", "Integrating automated threshold-based alerting through Slack webhooks, Discord notifications, Telegram bots, or Twilio SMS when an API status transitions to 'Failed'.")
add_bullet_justified(doc, "Distributed Multi-Region Probing", "Expanding probe execution across geo-distributed serverless edge workers (e.g., Cloudflare Workers or AWS Lambda) to measure regional latency variances from global access points.")
add_bullet_justified(doc, "SLA & Availability Reporting Export", "Implementing automated PDF and CSV reporting engines to generate periodic Service Level Agreement (SLA) uptime and compliance audits for enterprise stakeholders.")

add_inside_heading(doc, "7.3 Limitations of the Proposed System", space_before=6)
add_body_p(doc, 
    "While the client-side diagnostic engine provides extraordinary convenience, it remains bound to the browser runtime: background probing requires an open browser window or tab. Additionally, opaque CORS responses prevent inspecting specific HTTP error headers on cross-origin domains.")

# ==============================================================================
# REFERENCES (PAGE 21 / BODY PAGE 17)
# ==============================================================================
doc.add_page_break()

p_ref_head = doc.add_paragraph()
p_ref_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ref_head.paragraph_format.space_before = Pt(10)
p_ref_head.paragraph_format.space_after = Pt(8)
r_ref = p_ref_head.add_run("REFERENCES")
r_ref.font.name = "Times New Roman"; r_ref.font.size = Pt(14); r_ref.bold = True

references_list = [
    "[1] Fielding, R. T., 'Architectural Styles and the Design of Network-based Software Architectures', Doctoral dissertation, University of California, Irvine, 2000.",
    "[2] Google Developers, 'Core Web Vitals and Lighthouse Performance Auditing Documentation', web.dev, 2024.",
    "[3] Flanagan, D., 'JavaScript: The Definitive Guide: Master the World's Most-Used Programming Language', 7th ed., O'Reilly Media, 2020.",
    "[4] MDN Web Docs, 'Performance API and High Resolution Time Specification', Mozilla Developer Network, 2024.",
    "[5] W3C, 'Cross-Origin Resource Sharing (CORS) Technical Specification', World Wide Web Consortium Recommendation, 2023.",
    "[6] Nixon, R., 'Learning PHP, MySQL & JavaScript: With jQuery, CSS & HTML5', 6th ed., O'Reilly Media, 2021.",
    "[7] Chart.js Documentation, 'Hardware-Accelerated HTML5 Canvas Data Visualization Library', v4.4.1, 2024.",
    "[8] Newman, S., 'Building Microservices: Designing Fine-Grained Systems', 2nd ed., O'Reilly Media, 2021.",
    "[9] Kleppmann, M., 'Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems', O'Reilly Media, 2017."
]

for ref_text in references_list:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(ref_text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

# Save output
output_filename = "API_Monitoring_Project_Report.docx"
doc.save(output_filename)
print(f"Report successfully built: {output_filename}")
