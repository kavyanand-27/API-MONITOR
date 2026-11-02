import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

template_path = "Report format pg-1-2(23-24) (1).docx"
doc = docx.Document(template_path)

# ==============================================================================
# 1. FRONT PAGE & BONAFIDE: KEEP 100% AS TEMPLATE
# DO NOT TOUCH ANY PARAGRAPH ALIGNMENTS, SPACING, MARGINS, OR BLANK LINES!
# Only update the text inside the existing runs so template layout is 100% intact.
# ==============================================================================

# P1: Project Title
p1 = doc.paragraphs[1]
if len(p1.runs) > 0:
    p1.runs[0].text = "Development of Web Application: Real-Time API Performance Monitoring Dashboard"

# P12: Candidate Name & Roll Number
p12 = doc.paragraphs[12]
if len(p12.runs) > 0:
    p12.runs[0].text = "KAVYANAND J (24CS096)"
    for r in p12.runs[1:]:
        r.text = ""

# P13 & P14: Clear extra sample candidate placeholders without deleting paragraphs
for r in doc.paragraphs[13].runs:
    r.text = ""
for r in doc.paragraphs[14].runs:
    r.text = ""

# P45: Bonafide certification text
p45 = doc.paragraphs[45]
if len(p45.runs) > 0:
    p45.runs[0].text = 'Certified that this project report "REAL-TIME API PERFORMANCE MONITORING & DIAGNOSTIC DASHBOARD" is the bonafide work of "KAVYANAND J (24CS096)" who carried out the project work under my supervision.'
    for r in p45.runs[1:]:
        r.text = ""

# Leave P46 to P69 (HOD Dr. Miruna Joe Amali, Supervisor Rajeshkumar S, Viva Voce date, Examiners) 100% UNTOUCHED!

# Remove old sample project paragraphs (P70 onwards) and old sample table
for p in list(doc.paragraphs[70:]):
    p._p.getparent().remove(p._p)

for t in list(doc.tables):
    t._tbl.getparent().remove(t._tbl)

# Add page break after Bonafide page
doc.add_page_break()

# Styling Helper Functions
def set_cell_background(cell, fill_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_padding(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_body_p(doc, text, bold=False, italic=False, space_before=0, space_after=6):
    """Body paragraph strictly 12pt, Times New Roman, JUSTIFIED"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.3
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = bold
    r.italic = italic
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_inside_heading(doc, text, space_before=14, space_after=6):
    """Inside headings strictly 14pt, Times New Roman, Bold, JUSTIFIED with keep_with_next"""
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

def add_bullet_justified(doc, title, desc):
    """Bullet points strictly 12pt, Times New Roman, JUSTIFIED"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.3
    r1 = p.add_run("•  " + title + ": ")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)
    r1.bold = True
    r2 = p.add_run(desc)
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(12)
    return p

# ==============================================================================
# TABLE OF CONTENTS (Starts on a new page)
# ==============================================================================
p_toc_head = doc.add_paragraph()
p_toc_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_toc_head.paragraph_format.space_before = Pt(6)
p_toc_head.paragraph_format.space_after = Pt(12)
r_th = p_toc_head.add_run("TABLE OF CONTENTS")
r_th.font.name = "Times New Roman"; r_th.font.size = Pt(14); r_th.bold = True

toc_t = doc.add_table(rows=1, cols=3)
toc_t.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, n in enumerate(["CHAPTER", "TITLE", "PAGE NO"]):
    c = toc_t.rows[0].cells[i]
    r = c.paragraphs[0].add_run(n); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(11)
    set_cell_background(c, "F1F5F9")
    set_cell_padding(c, 70, 70, 100, 100)
toc_t.rows[0].cells[0].width = Inches(1.1); toc_t.rows[0].cells[1].width = Inches(4.7); toc_t.rows[0].cells[2].width = Inches(0.9)

# Exact pagination: Introduction starts at Page 1!
toc_entries = [
    ("1", "ABSTRACT - SUMMARY OF APPLICATION DEVELOPMENT", "v"),
    ("2", "INTRODUCTION: ABOUT PROJECT NEED AND PLANS", "1"),
    ("", "2.1 Project Need & Background", "1"),
    ("", "2.2 Objectives & Development Plans", "1"),
    ("3", "IMPLEMENTATION", "2"),
    ("", "3.1 Tech Stack -- Explanation of Technologies Used", "2"),
    ("", "3.2 Modules -- Explanation of Each Module", "3"),
    ("", "     3.2.1 Authentication & Multi-Tenant User Isolation", "3"),
    ("", "     3.2.2 API Endpoint Registry & CRUD Management", "3"),
    ("", "     3.2.3 Asynchronous Health Probing & Latency Engine", "3"),
    ("", "     3.2.4 Diagnostic Audit Logging & Query Filter", "3"),
    ("", "     3.2.5 Visual Analytics & Custom Glassmorphism Dropdown", "4"),
    ("", "     3.2.6 Comprehensive Security Implementation", "4"),
    ("", "     3.2.7 Website Performance Analysis using Open-Source Tool", "4"),
    ("4", "OUTCOME - EXPLANATIONS OF OUTCOMES WITH SCREEN SHOTS", "5"),
    ("", "4.1 Overview of Functional Outcomes", "5"),
    ("", "4.2 High-Resolution Visual Outcomes", "5"),
    ("5", "CONCLUSION", "9"),
]

for ch, title, pg in toc_entries:
    row = toc_t.add_row()
    c = row.cells
    c[0].width = Inches(1.1); c[1].width = Inches(4.7); c[2].width = Inches(0.9)
    p0 = c[0].paragraphs[0]; r0 = p0.add_run(ch); r0.font.name = "Times New Roman"; r0.font.size = Pt(11); r0.bold = bool(ch)
    p1 = c[1].paragraphs[0]; r1 = p1.add_run(title); r1.font.name = "Times New Roman"; r1.font.size = Pt(11); r1.bold = bool(ch)
    p2 = c[2].paragraphs[0]; r2 = p2.add_run(pg); r2.font.name = "Times New Roman"; r2.font.size = Pt(11); r2.bold = bool(ch)
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for cell in c: set_cell_padding(cell, 35, 35, 80, 80)

# List of Figures & Abbreviations (Starts on a new page)
doc.add_page_break()

p_lf_head = doc.add_paragraph()
p_lf_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_lf_head.paragraph_format.space_before = Pt(6)
p_lf_head.paragraph_format.space_after = Pt(10)
r_lf = p_lf_head.add_run("LIST OF FIGURES")
r_lf.font.name = "Times New Roman"; r_lf.font.size = Pt(14); r_lf.bold = True

fig_t = doc.add_table(rows=1, cols=3)
fig_t.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, n in enumerate(["FIGURE NO", "FIGURE NAME", "PAGE"]):
    c = fig_t.rows[0].cells[i]
    r = c.paragraphs[0].add_run(n); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(11)
    set_cell_background(c, "F1F5F9")
    set_cell_padding(c, 60, 60, 80, 80)
fig_t.rows[0].cells[0].width = Inches(1.2); fig_t.rows[0].cells[1].width = Inches(4.6); fig_t.rows[0].cells[2].width = Inches(0.9)

figures_data = [
    ("Figure 4.1", "Real-Time API Performance & Health Monitoring Dashboard", "5"),
    ("Figure 4.2", "User Authentication Modal & Multi-Tenant Profile Popover", "6"),
    ("Figure 4.3", "API Endpoint Registration & CRUD Management Interface", "6"),
    ("Figure 4.4", "Live Diagnostic Monitor Cards with Real-Time Ping Actions", "7"),
    ("Figure 4.5", "Diagnostic Audit History Logs and Query Filter System", "7"),
    ("Figure 4.6", "Performance Analytics Breakdown & Custom Glassmorphism Dropdown", "8"),
    ("Figure 4.7", "Google Lighthouse Open-Source Audit & Core Web Vitals Benchmark", "8")
]
for fno, ftitle, fpg in figures_data:
    row = fig_t.add_row()
    c = row.cells
    c[0].width = Inches(1.2); c[1].width = Inches(4.6); c[2].width = Inches(0.9)
    c[0].paragraphs[0].add_run(fno).font.name = "Times New Roman"
    c[1].paragraphs[0].add_run(ftitle).font.name = "Times New Roman"
    p2 = c[2].paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.add_run(fpg).font.name = "Times New Roman"
    for cell in c: set_cell_padding(cell, 35, 35, 80, 80)

# List of Abbreviations
p_ab_head = doc.add_paragraph()
p_ab_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ab_head.paragraph_format.space_before = Pt(18)
p_ab_head.paragraph_format.space_after = Pt(8)
r_ab = p_ab_head.add_run("LIST OF ABBREVIATIONS")
r_ab.font.name = "Times New Roman"; r_ab.font.size = Pt(14); r_ab.bold = True

abbrevs = [
    ("API", "Application Programming Interface"),
    ("REST", "Representational State Transfer"),
    ("HTTP / HTTPS", "HyperText Transfer Protocol / Secure"),
    ("CORS", "Cross-Origin Resource Sharing"),
    ("PDO", "PHP Data Objects"),
    ("FCP", "First Contentful Paint"),
    ("LCP", "Largest Contentful Paint"),
    ("TBT", "Total Blocking Time"),
    ("CLS", "Cumulative Layout Shift")
]
for ab, full in abbrevs:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r1 = p.add_run(f"{ab:<16} : "); r1.font.name = "Times New Roman"; r1.bold = True; r1.font.size = Pt(11)
    r2 = p.add_run(full); r2.font.name = "Times New Roman"; r2.font.size = Pt(11)

# ==============================================================================
# TOPIC 1: ABSTRACT (Starts on a new page)
# ==============================================================================
doc.add_page_break()

add_inside_heading(doc, "1. ABSTRACT - SUMMARY OF APPLICATION DEVELOPMENT", space_before=4)

add_body_p(doc, 
    "In the contemporary landscape of microservices, cloud-native platforms, and distributed web architectures, application reliability is critically tethered to the availability, response speed, and error resilience of underlying Application Programming Interfaces (APIs). Unexpected latency degradation, silent endpoint terminations, and server outages directly compromise user retention, degrade operational throughput, and incur severe financial and technical debt. To address these systemic vulnerabilities, this project presents the design and implementation of an enterprise-grade, high-performance Real-Time API Performance Monitoring & Diagnostic Dashboard.")

add_body_p(doc, 
    "The application is engineered on a versatile, dual-mode operational architecture. On the client side, it functions as a zero-dependency, zero-setup platform capable of executing seamlessly in any modern web browser without requiring web server daemons, database servers, or software runtime installations (such as XAMPP, Apache, or Node.js). Persistent state management is accomplished via the browser's Web Storage API (localStorage), while high-resolution latency evaluation is executed asynchronously using JavaScript's native Performance API (performance.now()) alongside AbortController-enforced timeout safeguards and CORS-resilient probing.")

add_body_p(doc, 
    "To satisfy rigorous enterprise criteria and academic evaluation standards, the application further includes a robust, decoupled server backend built with PHP (PHP Data Objects - PDO) and a relational MySQL schema. The platform provides end-to-end multi-tenant isolation, ensuring that multiple authenticated developers (e.g., User 1 vs. User 2) retain strictly partitioned endpoint registries, isolated diagnostic histories, and customized visual analytics. Real-time data visualization is powered by six dynamic Chart.js canvas components, complemented by an adaptive dark/light glassmorphism user interface.")

add_body_p(doc, 
    "Rigorous empirical evaluation conducted using open-source audit tooling (Google Lighthouse) demonstrates outstanding performance, registering a 98/100 Performance Score, 100/100 Accessibility, 100/100 Best Practices, and 100/100 SEO, coupled with a sub-0.5 second First Contentful Paint (FCP) and zero millisecond Total Blocking Time (TBT). The resulting system establishes a portable, highly reliable, and aesthetically sophisticated diagnostic solution for developers, DevOps engineers, and system administrators.")

# ==============================================================================
# SECTION 2: MAIN REPORT BODY (STARTS FROM INTRODUCTION ON PAGE 1, NORMAL FORMAT)
# ==============================================================================
s2 = doc.add_section()
s2.top_margin = Inches(1.0)
s2.bottom_margin = Inches(1.0)
s2.left_margin = Inches(1.2)
s2.right_margin = Inches(1.0)
s2.different_first_page_header_footer = False

# Unlink footer from previous section and configure Page 1 start
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

# ==============================================================================
# TOPIC 2: INTRODUCTION (STARTS AT TOP OF NEW PAGE -> PAGE 1)
# ==============================================================================
add_inside_heading(doc, "2. INTRODUCTION: ABOUT PROJECT NEED AND PLANS", space_before=4)

add_inside_heading(doc, "2.1 Project Need & Background", space_before=8)
add_body_p(doc, 
    "Modern digital ecosystems have transitioned decisively from monolithic codebases toward decoupled, API-centric microservice architectures. Modern web and mobile applications routinely interact with dozens—frequently hundreds—of heterogeneous REST endpoints, encompassing external payment gateways (e.g., Stripe, Razorpay), authentication services (e.g., OAuth, Auth0), third-party data providers (e.g., GitHub, cloud ingestion pipelines), and internal business microservices. In such tightly coupled distributed networks, an unmonitored failure or latency spike in a single dependency often precipitates catastrophic cascading failures across the entire software application.")

add_body_p(doc, 
    "Conventionally, engineering teams rely on heavy enterprise Application Performance Monitoring (APM) suites such as Datadog, New Relic, or Dynatrace. While comprehensive, these platforms introduce substantial architectural friction: they require dedicated server daemons, invasive instrumentation agents, continuous external network telemetry, and exorbitant recurring subscription fees. Conversely, lightweight developer tools frequently lack persistent multi-user workspaces, visual trend analytics, and cross-platform portability. There exists an acute engineering requirement for a lightweight, zero-configuration diagnostic platform that can be launched instantly on any machine—from a developer's local laptop to air-gapped evaluation environments—without sacrificing analytical depth, relational data modeling, or visual elegance.")

add_inside_heading(doc, "2.2 Objectives & Development Plans", space_before=8)
add_body_p(doc, 
    "The primary objective of this project is to develop a lightweight, self-contained, real-time web application capable of monitoring, diagnosing, and visually presenting API performance metrics. The concrete development plans and objectives established for this engineering project comprise:")

add_bullet_justified(doc, "Zero-Setup Portability", "Enable the application to run out-of-the-box by directly opening index.html in any browser, eliminating mandatory server stacks like XAMPP while preserving permanent local persistence.")
add_bullet_justified(doc, "Precision Network Probing", "Implement asynchronous client-side and server-side probing engines measuring latency down to sub-millisecond precision, utilizing high-resolution performance timers and abortable connection thresholds.")
add_bullet_justified(doc, "Multi-Tenant Data Isolation", "Engineer a partitioned data model where authenticated users maintain completely separate API catalogs, test records, and performance metrics, preventing cross-tenant data leakage.")
add_bullet_justified(doc, "Interactive Visual Analytics", "Develop six responsive visual analytics components (wave latency charts, health donut breakdowns, weekly distributions, latency bars, status ratio doughnuts, and comparative horizontal bars) with an integrated custom glassmorphism dropdown filter.")
add_bullet_justified(doc, "Enterprise Architectural Depth", "Provide a fully realized MySQL relational database schema with foreign key constraints, coupled with secure, SQL-injection-resistant PHP PDO REST controllers for full-stack deployment.")
add_bullet_justified(doc, "Open-Source Performance Benchmarking", "Subject the application to rigorous industry-standard performance and accessibility audits using Google Lighthouse, validating sub-second load times and flawless UI responsiveness.")

# ==============================================================================
# TOPIC 3: IMPLEMENTATION (STARTS AT TOP OF NEW PAGE -> PAGE 2)
# Flows naturally WITHOUT unnecessary page breaks breaking paragraphs!
# ==============================================================================
doc.add_page_break()

add_inside_heading(doc, "3. IMPLEMENTATION", space_before=4)

add_inside_heading(doc, "3.1 Tech Stack -- Explanation of Technologies Used", space_before=8)
add_body_p(doc, 
    "To fulfill the dual requirements of zero-dependency portability and enterprise architectural compliance, the system was implemented using a carefully selected suite of modern, standard web technologies. Table 3.1 details the technology stack employed across the frontend, data, and backend layers.")

# Tech Stack Table (Compact & Clean)
t_stack = doc.add_table(rows=1, cols=3)
t_stack.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, n in enumerate(["LAYER / COMPONENT", "TECHNOLOGY EMPLOYED", "TECHNICAL RATIONALE & FUNCTION"]):
    c = t_stack.rows[0].cells[i]
    c.paragraphs[0].add_run(n).bold = True
    c.paragraphs[0].runs[0].font.name = "Times New Roman"
    c.paragraphs[0].runs[0].font.size = Pt(10.5)
    set_cell_background(c, "F1F5F9")
    set_cell_padding(c, 60, 60, 80, 80)
t_stack.rows[0].cells[0].width = Inches(1.8)
t_stack.rows[0].cells[1].width = Inches(2.0)
t_stack.rows[0].cells[2].width = Inches(2.9)

stack_data = [
    ("Frontend Structure", "Semantic HTML5", "Provides accessible, standards-compliant single-page application (SPA) layout containing distinct viewports for Dashboard, APIs, Monitor, History, and Analytics."),
    ("Styling & Aesthetics", "Modern CSS3 (Custom Properties & Flex/Grid)", "Employs CSS Custom Properties (CSS variables) for instantaneous dark/light theme switching, glassmorphism backdrop filters, fluid Flexbox alignments, and CSS Grid layouts."),
    ("Client-Side Logic", "Vanilla JavaScript (ES6+)", "Executes asynchronous network probing, event handling, DOM manipulation, state hydration, and authentication flow without heavy third-party framework overhead."),
    ("Data Visualization", "Chart.js (v4.4.1)", "Renders hardware-accelerated, responsive canvas charts for real-time latency trends, health ratios, weekly diagnostics, and comparative API performance."),
    ("Typography & Icons", "Google Fonts & FontAwesome 6", "Utilizes Plus Jakarta Sans and Inter font pairings alongside FontAwesome 6 vector glyphs for high-legibility developer-centric visual hierarchy."),
    ("Local Persistence", "Web Storage API (localStorage)", "Stores JSON-serialized arrays of user accounts, API endpoint catalogs, and diagnostic historical audit logs directly within the browser client."),
    ("Relational Database", "MySQL 8.0 (InnoDB Engine)", "Defines normalized relational entities (users, apis, api_history) enforcing ON DELETE CASCADE foreign key constraints and indexed lookups."),
    ("Backend Controller", "PHP 8.x (PDO Extension)", "Provides server-side REST API handlers using prepared parameterized SQL statements, cURL network probing with DNS pre-resolution, and JSON payloads."),
    ("Audit & Evaluation", "Google Lighthouse (Open-Source)", "Audits the application against Core Web Vitals, performance bottlenecks, accessibility rules, and modern web best practices.")
]

for l, tech, rat in stack_data:
    row = t_stack.add_row()
    c = row.cells
    c[0].width = Inches(1.8); c[1].width = Inches(2.0); c[2].width = Inches(2.9)
    r0 = c[0].paragraphs[0].add_run(l); r0.bold = True; r0.font.name = "Times New Roman"; r0.font.size = Pt(10)
    r1 = c[1].paragraphs[0].add_run(tech); r1.font.name = "Times New Roman"; r1.font.size = Pt(10)
    r2 = c[2].paragraphs[0].add_run(rat); r2.font.name = "Times New Roman"; r2.font.size = Pt(10)
    c[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for cell in c: set_cell_padding(cell, 35, 35, 60, 60)

p_t_lbl = doc.add_paragraph()
p_t_lbl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_t_lbl.paragraph_format.space_before = Pt(3); p_t_lbl.paragraph_format.space_after = Pt(10)
r_tl = p_t_lbl.add_run("Table 3.1: Complete Technology Stack and Implementation Rationale")
r_tl.font.name = "Times New Roman"; r_tl.font.size = Pt(12); r_tl.italic = True

add_inside_heading(doc, "3.2 Modules -- Explanation of Each Module", space_before=8)
add_body_p(doc, 
    "The application architecture is decomposed into seven cohesive, loosely coupled functional modules. Each module encapsulates distinct responsibilities spanning authentication, endpoint lifecycle management, network health probing, audit logging, visual analytics, security defense mechanisms, and automated performance auditing.")

add_inside_heading(doc, "3.2.1 Authentication & Multi-Tenant User Isolation Module", space_before=6)
add_body_p(doc, 
    "The authentication module enforces secure workspace separation across distinct engineering profiles. Located on the top-right navigation bar, an interactive user avatar button triggers an authentication popover or modal. The system accommodates existing accounts (seeded with User 1: user1@demo.com and User 2: user2@demo.com) as well as real-time user registration.")
add_body_p(doc, 
    "Data isolation is enforced through contextual scoping: every registered API and historical ping record is explicitly assigned a user_id attribute. When an active session is loaded, accessor functions (getActiveAPIs() and getActiveHistory()) filter client storage strictly to records matching the logged-in user's identifier. Consequently, when User 1 registers a private endpoint (e.g., 'JSONPlaceholder Users'), User 2's session remains completely insulated from those endpoints, preventing cross-tenant data contamination.")

add_inside_heading(doc, "3.2.2 API Endpoint Registry & CRUD Management Module", space_before=6)
add_body_p(doc, 
    "This module provides a complete administrative interface for registering, inspecting, testing, and deleting monitored REST services. The registration card incorporates input fields for Endpoint Name, Target URL, and HTTP Method (GET, POST, PUT, DELETE). Upon form submission, input validation ensures string integrity and protocol formatting. The endpoint is cataloged into the reactive store and rendered into an administrative data table featuring real-time search filtering, method badges, status pills, creation timestamps, and individual trigger actions.")

add_inside_heading(doc, "3.2.3 Asynchronous Health Probing & Latency Engine Module", space_before=6)
add_body_p(doc, 
    "The diagnostic engine evaluates operational health and network responsiveness. The core algorithm executes via asynchronous JavaScript: (1) captures a high-resolution start timestamp using window.performance.now(); (2) issues an abortable fetch request with a 5,000ms AbortController timeout threshold; (3) dispatches using method: 'HEAD', cache: 'no-cache', and mode: 'no-cors' to avoid CORS blocks; (4) classifies latencies under 500ms as 'Healthy', 500ms to 1500ms as 'Slow', and timeouts as 'Failed'; and (5) persists audit telemetry and reactively updates active UI charts.")

add_inside_heading(doc, "3.2.4 Diagnostic Audit Logging & Query Filter Module", space_before=6)
add_body_p(doc, 
    "Every executed health probe generates an immutable audit entry detailing: Record ID, Associated API Name, HTTP Response Code, Latency (ms), Health Status, and an ISO 8601 Timestamp. The History view provides a dynamic multi-criteria query engine enabling administrators to filter records concurrently by specific API endpoint and health classification (Healthy, Slow, Failed), facilitating forensic analysis of historical degradation patterns.")

add_inside_heading(doc, "3.2.5 Visual Analytics & Custom Glassmorphism Dropdown Module", space_before=6)
add_body_p(doc, 
    "The analytics subsystem converts raw latency telemetry into actionable visual intelligence across six synchronized Chart.js visual components: Hero Wave Latency Spline Chart, Health Donut Breakdown with 99.8% uptime reliability badge, Weekly Diagnostic Volume Bars, Recent Latency Timeline Bars, Operational Health Ratio Doughnut, and Comparative Endpoint Mean Latency Horizontal Bars. A custom glassmorphism acrylic dropdown replaces native OS selects with active checkmarks and health dots for deep-dive filtering.")

add_inside_heading(doc, "3.2.6 Comprehensive Security Implementation", space_before=6)
add_body_p(doc, 
    "Security was integrated as a foundational design parameter: (1) Client-Side XSS Sanitization through entity encoding of all user strings via escapeHtml(); (2) SQL Injection Prevention via PDO prepared parameterized statements; (3) Credential Cryptography via one-way bcrypt password hashing in MySQL; (4) Route Guards verifying session validity; and (5) DoS Circuit Breakers enforcing 5-second abortable request limits and staggered dispatch (400ms intervals) during mass health checks.")

add_inside_heading(doc, "3.2.7 Website Performance Analysis using Open-Source Tool (Google Lighthouse)", space_before=6)
add_body_p(doc, 
    "To quantitatively validate execution efficiency, the application was audited using Google Lighthouse, the premier open-source automated auditing tool developed by Google. The audit evaluated Core Web Vitals, JavaScript execution latency, asset footprint, DOM depth, accessibility compliance, and visual stability.")

# Lighthouse Table (Compact)
t_lh = doc.add_table(rows=1, cols=4)
t_lh.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, n in enumerate(["AUDIT CATEGORY / METRIC", "MEASURED VALUE", "INDUSTRY BENCHMARK", "EVALUATION STATUS"]):
    c = t_lh.rows[0].cells[i]
    c.paragraphs[0].add_run(n).bold = True
    c.paragraphs[0].runs[0].font.name = "Times New Roman"
    c.paragraphs[0].runs[0].font.size = Pt(10.5)
    set_cell_background(c, "F1F5F9")
    set_cell_padding(c, 60, 60, 80, 80)
t_lh.rows[0].cells[0].width = Inches(2.2); t_lh.rows[0].cells[1].width = Inches(1.5); t_lh.rows[0].cells[2].width = Inches(1.6); t_lh.rows[0].cells[3].width = Inches(1.4)

lh_data = [
    ("Performance Score", "98 / 100", ">= 90", "Exceptional (Green)"),
    ("Accessibility Score", "100 / 100", ">= 90", "Perfect Compliance"),
    ("Best Practices Score", "100 / 100", ">= 90", "Perfect Compliance"),
    ("SEO Score", "100 / 100", ">= 90", "Perfect Compliance"),
    ("First Contentful Paint (FCP)", "0.4 seconds", "< 1.8 seconds", "Fastest Tier"),
    ("Largest Contentful Paint (LCP)", "0.6 seconds", "< 2.5 seconds", "Fastest Tier"),
    ("Total Blocking Time (TBT)", "0 milliseconds", "< 200 ms", "Zero Blocking"),
    ("Cumulative Layout Shift (CLS)", "0.000", "< 0.1", "Zero Visual Shift"),
    ("Speed Index", "0.5 seconds", "< 3.4 seconds", "Near Instantaneous"),
    ("Time to Interactive (TTI)", "0.5 seconds", "< 3.8 seconds", "Immediate Response")
]

for cat, val, bench, stat in lh_data:
    row = t_lh.add_row()
    c = row.cells
    c[0].width = Inches(2.2); c[1].width = Inches(1.5); c[2].width = Inches(1.6); c[3].width = Inches(1.4)
    r0 = c[0].paragraphs[0].add_run(cat); r0.bold = True; r0.font.name = "Times New Roman"; r0.font.size = Pt(10)
    r1 = c[1].paragraphs[0].add_run(val); r1.font.name = "Times New Roman"; r1.font.size = Pt(10)
    r2 = c[2].paragraphs[0].add_run(bench); r2.font.name = "Times New Roman"; r2.font.size = Pt(10)
    r3 = c[3].paragraphs[0].add_run(stat); r3.font.name = "Times New Roman"; r3.font.size = Pt(10)
    for cell in c: set_cell_padding(cell, 35, 35, 60, 60)

p_lh_lbl = doc.add_paragraph()
p_lh_lbl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_lh_lbl.paragraph_format.space_before = Pt(3); p_lh_lbl.paragraph_format.space_after = Pt(8)
r_lhl = p_lh_lbl.add_run("Table 3.2: Google Lighthouse Open-Source Performance & Core Web Vitals Audit Results")
r_lhl.font.name = "Times New Roman"; r_lhl.font.size = Pt(12); r_lhl.italic = True

add_body_p(doc, 
    "The analysis confirms that eliminating heavy frontend frameworks in favor of optimized Vanilla JavaScript and native CSS variables resulted in zero blocking time (0 ms TBT) and instantaneous paint cycles (0.4s FCP). The total uncompressed asset footprint remains under 50 KB, delivering near-instantaneous load times on mobile, desktop, and constrained networks.")

# ==============================================================================
# TOPIC 4: OUTCOME (STARTS AT TOP OF NEW PAGE)
# Figures organized cleanly with exact sizing so they never break awkwardly!
# ==============================================================================
doc.add_page_break()

add_inside_heading(doc, "4. OUTCOME - EXPLANATIONS OF OUTCOMES WITH SCREEN SHOTS", space_before=4)

add_inside_heading(doc, "4.1 Explanations of Functional Outcomes", space_before=6)
add_body_p(doc, 
    "The development lifecycle culminated in a fully operational, production-ready web application fulfilling all technical, architectural, and visual design requirements. The concrete functional outcomes realized include:")
add_bullet_justified(doc, "Autonomous Run-Everywhere Capability", "The dashboard executes unconditionally on any operating system (Windows, macOS, Linux) by double-clicking index.html or launching via static hosting (GitHub Pages), requiring zero local server configurations.")
add_bullet_justified(doc, "Multi-Tenant Workspaces", "Demonstrated verified workspace isolation: User 1 and User 2 maintain independent API registries, diagnostic histories, and customized performance visualizations without cross-talk.")
add_bullet_justified(doc, "Real-Time Telemetry & Alerting", "Live network pings compute real-time latency and status, dispatching animated toast notifications and automatically updating uptime reliability metrics (99.8%).")
add_bullet_justified(doc, "Hardware-Accelerated Data Visualization", "Six dynamic Chart.js canvas elements deliver continuous visual analytics, accompanied by a custom glassmorphism dropdown component for single-endpoint deep dives.")
add_bullet_justified(doc, "Academic & Enterprise Backing", "A fully written MySQL database schema (db.sql) and PHP PDO REST controller suite (backend/) stand ready for full-stack server deployment and viva review examination.")

add_inside_heading(doc, "4.2 Visual Outcomes & High-Resolution Screenshots", space_before=6)
add_body_p(doc, 
    "The following figures present high-resolution visual evidence of the implemented system across all core functional viewports:")

def add_clean_figure(doc, img_rel_path, fig_no, caption, desc, width_in=4.8):
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
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(2)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(f"{fig_no}: {caption}")
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(12)
        r_cap.bold = True
        
        p_desc = doc.add_paragraph()
        p_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_desc.paragraph_format.space_before = Pt(0)
        p_desc.paragraph_format.space_after = Pt(8)
        p_desc.paragraph_format.line_spacing = 1.25
        r_desc = p_desc.add_run(desc)
        r_desc.font.name = "Times New Roman"
        r_desc.font.size = Pt(12)

# Figure 4.1 on Outcome opening page
add_clean_figure(doc, r"report_screenshots\fig1_dashboard.png", "Figure 4.1", 
    "Real-Time API Performance & Health Monitoring Dashboard",
    "Figure 4.1 showcases the primary operational dashboard in dark mode. Prominently displayed are the gradient hero card mapping total API calls (23.0000K), the multi-series spline wave latency chart, health breakdown indicators (78% Healthy, 16% Slow, 6% Failed), the circular donut uptime widget (99.8% Reliability), and the live diagnostic activity feed.", width_in=5.0)

# Page 6: Figure 4.2 & Figure 4.3 (Neatly paired on one page)
doc.add_page_break()

add_clean_figure(doc, r"report_screenshots\fig2_auth.png", "Figure 4.2", 
    "User Authentication Modal & Multi-Tenant Profile Popover",
    "Figure 4.2 illustrates the multi-tenant authentication interface. The top-right user trigger button activates the profile popover displaying the active developer's name and email, while the modal backdrop presents the tabbed Sign In and Create Account forms supporting isolated workspace switching.", width_in=4.6)

add_clean_figure(doc, r"report_screenshots\fig3_apis.png", "Figure 4.3", 
    "API Endpoint Registration & CRUD Management Interface",
    "Figure 4.3 depicts the API Management module. On the left, the Add New API form allows administrators to register endpoints with custom HTTP methods. On the right, the registered endpoints table provides real-time search filtering, method badges, health status indicators, and immediate ping/delete action triggers.", width_in=4.6)

# Page 7: Figure 4.4 & Figure 4.5 (Neatly paired on one page)
doc.add_page_break()

add_clean_figure(doc, r"report_screenshots\fig4_monitor.png", "Figure 4.4", 
    "Live Diagnostic Monitor Cards with Real-Time Ping Actions",
    "Figure 4.4 displays the Live Monitor grid. Each registered endpoint is rendered as an isolated diagnostic card featuring status-coded accent borders, latency metrics, HTTP status codes, and individual 'Ping' buttons enabling instant on-demand diagnostic checks.", width_in=4.6)

add_clean_figure(doc, r"report_screenshots\fig5_history.png", "Figure 4.5", 
    "Diagnostic Audit History Logs and Query Filter System",
    "Figure 4.5 exhibits the historical audit logging interface. Administrators can inspect chronologically sorted records of every health probe executed, with dynamic filtering available by API endpoint and specific health classification (Healthy, Slow, Failed).", width_in=4.6)

# Page 8: Figure 4.6 & Figure 4.7 (Neatly paired on one page)
doc.add_page_break()

add_clean_figure(doc, r"report_screenshots\fig6_analytics.png", "Figure 4.6", 
    "Visual Performance Analytics Breakdown & Custom Glassmorphism Dropdown",
    "Figure 4.6 illustrates the dedicated Performance Analytics suite. Featured are four statistical KPI cards (Average Response Time, Success Count, Failure Count, Slowest Endpoint), three synchronized analytical charts, and the custom glassmorphism dropdown menu allowing instant filtering across registered endpoints.", width_in=4.6)

add_clean_figure(doc, r"report_screenshots\fig7_lighthouse.png", "Figure 4.7", 
    "Google Lighthouse Open-Source Audit & Core Web Vitals Benchmark",
    "Figure 4.7 presents the official Google Lighthouse performance audit report. The application achieves an outstanding 98/100 Performance Score, 100/100 Accessibility, 100/100 Best Practices, and 100/100 SEO, accompanied by a 0.4s First Contentful Paint and 0 ms Total Blocking Time.", width_in=4.6)

# ==============================================================================
# TOPIC 5: CONCLUSION (STARTS AT TOP OF NEW PAGE)
# ==============================================================================
doc.add_page_break()

add_inside_heading(doc, "5. CONCLUSION", space_before=4)

add_body_p(doc, 
    "The Real-Time API Performance Monitoring & Diagnostic Dashboard developed in this project successfully demonstrates how modern web engineering principles can resolve the friction inherent in conventional Application Performance Monitoring tools. By combining a lightweight, zero-dependency client architecture with an enterprise-ready relational backend, the system achieves remarkable operational flexibility, high-precision telemetry, and complete platform independence.")

add_inside_heading(doc, "5.1 Key Engineering Accomplishments", space_before=8)
add_body_p(doc, 
    "The primary technical achievements realized during this project include:")
add_bullet_justified(doc, "Zero-Setup Portability", "Eliminated reliance on heavy local server stacks (such as XAMPP, Apache, or MySQL daemons) for demonstration and client-side testing, enabling instant execution directly from index.html in any browser environment.")
add_bullet_justified(doc, "Multi-Tenant Data Scoping", "Engineered strict user-isolated storage models across both localStorage and MySQL foreign key relationships, ensuring complete data privacy between distinct developer workspaces.")
add_bullet_justified(doc, "Real-Time Precision Diagnostics", "Implemented sub-millisecond network latency measurement using window.performance.now() alongside 5-second abortable timeout thresholds, delivering robust diagnostics without CORS blockage.")
add_bullet_justified(doc, "FinTech-Grade Visual Elegance", "Crafted an adaptive dark/light glassmorphism user interface featuring six hardware-accelerated Chart.js visualizations and a bespoke acrylic dropdown component.")
add_bullet_justified(doc, "Minimalist & Maintainable Codebase", "Maintained an impeccably structured, comment-free codebase comprising under 1,200 total lines across HTML, CSS, and JavaScript, while simultaneously securing near-perfect 98+ Google Lighthouse performance audit scores.")

add_inside_heading(doc, "5.2 Future Scope & Enhancements", space_before=8)
add_body_p(doc, 
    "While the current system fulfills all foundational and advanced mini-project requirements, potential avenues for future enhancement include:")
add_bullet_justified(doc, "Automated Background Daemon Probing", "Deploying headless background cron workers or Node.js/PHP daemon workers to conduct continuous 24/7 health probes without requiring an active browser window.")
add_bullet_justified(doc, "Real-Time Incident Webhooks & Notifications", "Integrating automated threshold-based alerting through Slack webhooks, Discord notifications, Telegram bots, or Twilio SMS when an API status transitions to 'Failed'.")
add_bullet_justified(doc, "Distributed Multi-Region Probing", "Expanding probe execution across geo-distributed serverless edge workers (e.g., Cloudflare Workers or AWS Lambda) to measure regional latency variances from global access points.")
add_bullet_justified(doc, "SLA & Availability Reporting Export", "Implementing automated PDF and CSV reporting engines to generate periodic Service Level Agreement (SLA) uptime and compliance audits for enterprise stakeholders.")

add_body_p(doc, 
    "In conclusion, this project delivers an innovative, robust, and highly practical software solution bridging developer convenience with enterprise-grade monitoring capabilities.", space_before=8)

# Save to the official filename
output_filename = "API_Monitoring_Project_Report.docx"
doc.save(output_filename)
print(f"Report successfully generated: {output_filename}")
