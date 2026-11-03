import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# 1. Load the KPR base template derived from the uploaded .thmx
template_pptx = "kpr_template.pptx"
prs = pptx.Presentation(template_pptx)
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette matching KPR Theme and Modern Engineering APM
COLOR_PRIMARY_NAVY = RGBColor(26, 43, 76)       # #1A2B4C Deep Navy
COLOR_TEAL_ACCENT   = RGBColor(38, 148, 153)     # #269499 KPR Official Teal
COLOR_DARK_TEXT     = RGBColor(33, 37, 41)       # #212529 Charcoal Body Text
COLOR_MUTED_TEXT    = RGBColor(100, 116, 139)    # #64748B Slate Grey
COLOR_CARD_BG       = RGBColor(248, 250, 252)    # #F8FAFC Card Fill
COLOR_CARD_BORDER   = RGBColor(203, 213, 225)    # #CBD5E1 Border Line
COLOR_EMERALD       = RGBColor(22, 163, 74)      # #16A34A Success / Healthy
COLOR_AMBER         = RGBColor(217, 119, 6)      # #D97706 Warning / Slow
COLOR_CRIMSON       = RGBColor(220, 38, 38)      # #DC2626 Critical / Failed

def add_header(slide, title_text, category_text="REAL-TIME API PERFORMANCE MONITORING & DIAGNOSTIC DASHBOARD"):
    """Adds a standard KPR slide header leaving room for the top-right KPR logo."""
    # Category / Super-title
    cat_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.42), Inches(10.5), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Calibri"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_TEAL_ACCENT

    # Main Title
    t_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.72), Inches(10.5), Inches(0.65))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Calibri"
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_PRIMARY_NAVY

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Draws a professional card container for text and metrics."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape

# ==============================================================================
# SLIDE 1: TITLE SLIDE (Layout 0)
# ==============================================================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout with master background & logo

# Department Header Card
hdr_card = add_card(slide1, Inches(1.2), Inches(0.8), Inches(10.9), Inches(1.1), RGBColor(241, 248, 249), COLOR_TEAL_ACCENT)
tf_dept = hdr_card.text_frame
tf_dept.word_wrap = True
p = tf_dept.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "KPR INSTITUTE OF ENGINEERING AND TECHNOLOGY"
p.font.name = "Calibri"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY_NAVY

p2 = tf_dept.add_paragraph()
p2.alignment = PP_ALIGN.CENTER
p2.text = "(Autonomous Institution • Affiliated to Anna University Chennai • Accredited by NAAC 'A' Grade)\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING"
p2.font.name = "Calibri"
p2.font.size = Pt(11)
p2.font.bold = True
p2.font.color.rgb = COLOR_TEAL_ACCENT

# Main Project Title Box
main_box = add_card(slide1, Inches(1.2), Inches(2.1), Inches(10.9), Inches(2.6), RGBColor(255, 255, 255), COLOR_CARD_BORDER)
tf_main = main_box.text_frame
tf_main.word_wrap = True
tf_main.margin_left = tf_main.margin_right = Inches(0.4)
tf_main.margin_top = Inches(0.3)

p_proj = tf_main.paragraphs[0]
p_proj.alignment = PP_ALIGN.CENTER
p_proj.text = "REAL-TIME API PERFORMANCE MONITORING &\nDIAGNOSTIC DASHBOARD"
p_proj.font.name = "Calibri"
p_proj.font.size = Pt(26)
p_proj.font.bold = True
p_proj.font.color.rgb = COLOR_PRIMARY_NAVY

p_sub = tf_main.add_paragraph()
p_sub.alignment = PP_ALIGN.CENTER
p_sub.text = "A Zero-Dependency Observability Platform with Multi-Tenant Workspace Scoping,\nCORS-Resilient Probing, and Full-Stack Relational Telemetry"
p_sub.font.name = "Calibri"
p_sub.font.size = Pt(13)
p_sub.font.italic = True
p_sub.font.color.rgb = COLOR_MUTED_TEXT

# Metadata Cards: Candidate & Supervisor
cand_card = add_card(slide1, Inches(1.2), Inches(4.9), Inches(5.3), Inches(1.8))
tf_c = cand_card.text_frame
tf_c.word_wrap = True
tf_c.margin_left = tf_c.margin_top = Inches(0.25)
p = tf_c.paragraphs[0]
p.text = "SUBMITTED BY:"
p.font.name = "Calibri"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT
p = tf_c.add_paragraph()
p.text = "KAVYANAND J"
p.font.name = "Calibri"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY
p = tf_c.add_paragraph()
p.text = "Roll No: 24CS096\nB.E. Computer Science and Engineering"
p.font.name = "Calibri"; p.font.size = Pt(11.5); p.font.color.rgb = COLOR_DARK_TEXT

proj_info_card = add_card(slide1, Inches(6.8), Inches(4.9), Inches(5.3), Inches(1.8))
tf_i = proj_info_card.text_frame
tf_i.word_wrap = True
tf_i.margin_left = tf_i.margin_top = Inches(0.25)
p = tf_i.paragraphs[0]
p.text = "PROJECT DOMAIN & DETAILS:"
p.font.name = "Calibri"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT
p = tf_i.add_paragraph()
p.text = "Web Application & Cloud Telemetry"
p.font.name = "Calibri"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY
p = tf_i.add_paragraph()
p.text = "Audit Standard: Google Lighthouse Core Web Vitals\nAcademic Session: 2024 – 2025"
p.font.name = "Calibri"; p.font.size = Pt(11.5); p.font.color.rgb = COLOR_DARK_TEXT

# ==============================================================================
# SLIDE 2: PROBLEM STATEMENT & MOTIVATION
# ==============================================================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide2, "The Microservices Reliability Paradox & APM Bottlenecks", "MOTIVATION & PROBLEM STATEMENT")

# Left Column: Paradox Breakdown
c_left = add_card(slide2, Inches(0.9), Inches(1.5), Inches(5.6), Inches(5.2))
tf = c_left.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0.3)
p = tf.paragraphs[0]
p.text = "The Microservices Reliability Paradox"
p.font.name = "Calibri"; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY

p = tf.add_paragraph()
p.text = "• Modern enterprise applications are no longer isolated monolithic runtimes; they orchestrate dozens of distributed REST APIs (Payment gateways, OAuth services, AWS/GCP pipelines)."
p.font.name = "Calibri"; p.font.size = Pt(12.5); p.font.color.rgb = COLOR_DARK_TEXT

p = tf.add_paragraph()
p.text = "• Cascading Failure Vulnerability: When systems become decoupled, operational health becomes tightly interdependent. A 3000ms latency surge in an external payment endpoint causes full application perceived downtime."
p.font.name = "Calibri"; p.font.size = Pt(12.5); p.font.color.rgb = COLOR_DARK_TEXT

p = tf.add_paragraph()
p.text = "• Observability Blindspot: Engineering teams remain blind to transient network degradations until customer churn and severe financial losses occur."
p.font.name = "Calibri"; p.font.size = Pt(12.5); p.font.color.rgb = COLOR_DARK_TEXT

# Right Column: 4 Systemic Bottlenecks
c_right = add_card(slide2, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.2))
tf = c_right.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0.3)
p = tf.paragraphs[0]
p.text = "Acute Bottlenecks in Existing APMs"
p.font.name = "Calibri"; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY

bottlenecks = [
    ("1. Invasive Telemetry Overhead", "Commercial APMs (Datadog, Dynatrace) require heavy background daemons (>500MB RAM) and kernel probe drivers that distort local execution latency."),
    ("2. Multi-Tenant Collision", "Developer tools (Postman, Insomnia) store collections globally, causing endpoint data collisions on shared testing terminals."),
    ("3. Browser CORS Blocking", "Standard web fetch() pings fail when querying cross-origin endpoints without CORS headers, triggering false-negative offline alerts."),
    ("4. Exorbitant Pricing Models", "Consumption-based SaaS licensing prices out independent developers, staging labs, and student researchers.")
]
for title, desc in bottlenecks:
    p = tf.add_paragraph()
    p.text = f"{title}: "
    p.font.name = "Calibri"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT
    r = p.add_run()
    r.text = desc
    r.font.name = "Calibri"; r.font.size = Pt(11.5); r.font.color.rgb = COLOR_DARK_TEXT

# ==============================================================================
# SLIDE 3: ENGINEERING OBJECTIVES
# ==============================================================================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide3, "Primary Technical & Architectural Objectives", "ENGINEERING GOALS")

objectives = [
    ("Zero-Dependency Autonomous Execution", 
     "Architect the platform to execute directly in any modern browser simply by opening index.html, requiring zero local server runtimes (Apache, Node.js) or database daemons while ensuring full state persistence via the Web Storage API.", 
     "PORTABILITY"),
    ("High-Resolution Latency Probing Engine", 
     "Engineer an asynchronous diagnostic worker leveraging W3C performance.now() to measure network transport round-trip latency with sub-millisecond precision, guarded by a deterministic 5,000ms AbortController circuit breaker.", 
     "TELEMETRY"),
    ("Strict Multi-Tenant Workspace Scoping", 
     "Implement cryptographic, user-isolated data partitioning where distinct developers (User 1 vs. User 2) maintain completely private endpoint registries, independent diagnostic histories, and customized visual analytics.", 
     "ISOLATION"),
    ("Enterprise Relational Database Depth", 
     "Provide a fully normalized MySQL 8.0 relational schema complete with primary keys, indexed foreign key cascades, and secure PHP 8.x PDO REST controllers utilizing parameterized prepared SQL statements.", 
     "FULL-STACK"),
    ("Empirical Core Web Vitals Auditing", 
     "Subject the client application to automated Google Lighthouse audits, validating sub-0.5s First Contentful Paint (FCP), 0ms Total Blocking Time (TBT), and near-perfect 98+ performance scores across devices.", 
     "VERIFICATION")
]

for idx, (title, desc, badge) in enumerate(objectives):
    y_pos = Inches(1.5 + idx * 1.05)
    c = add_card(slide3, Inches(0.9), y_pos, Inches(11.5), Inches(0.95))
    tf = c.text_frame; tf.word_wrap = True; tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.12)
    p = tf.paragraphs[0]
    p.text = f"[{badge}]  {title}"
    p.font.name = "Calibri"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = "Calibri"; p2.font.size = Pt(11.5); p2.font.color.rgb = COLOR_DARK_TEXT

# ==============================================================================
# SLIDE 4: LITERATURE SURVEY & COMPETITIVE BENCHMARK
# ==============================================================================
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide4, "Comparative Benchmark against Prevailing APM Tooling", "LITERATURE SURVEY & BENCHMARKING")

# Table for benchmarking
rows, cols = 6, 5
tbl_shape = slide4.shapes.add_table(rows, cols, Inches(0.9), Inches(1.5), Inches(11.5), Inches(5.1))
tbl = tbl_shape.table

# Set Column Widths
tbl.columns[0].width = Inches(2.5)
tbl.columns[1].width = Inches(2.4)
tbl.columns[2].width = Inches(2.2)
tbl.columns[3].width = Inches(2.2)
tbl.columns[4].width = Inches(2.2)

headers = ["Evaluation Metric", "Proposed Dashboard", "Datadog / Dynatrace", "Postman / Insomnia", "Prometheus + Grafana"]
for col_idx, h in enumerate(headers):
    cell = tbl.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_PRIMARY_NAVY if col_idx != 1 else COLOR_TEAL_ACCENT
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Calibri"; p.font.size = Pt(11.5); p.font.bold = True; p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = RGBColor(255, 255, 255)

bench_data = [
    ("Telemetry Overhead", "Zero (<50 KB runtime, no daemons)", "Heavy (>500 MB RAM background daemons)", "Medium (Electron Desktop App)", "High (Time-series TSDB daemons)"),
    ("Multi-Tenant Scoping", "Strict User-Isolated Storage Partitioning", "RBAC / Organization Accounts", "No (Global machine storage collision)", "Complex Namespace RBAC"),
    ("Setup Complexity", "Zero-setup (Open index.html directly)", "Complex cloud agent installation", "Desktop application installation", "Extensive YAML & container configs"),
    ("CORS Resilience", "Opaque HEAD Probing + Circuit Breakers", "Agent bypasses browser sandbox", "Desktop client bypasses browser CORS", "Server-to-server HTTP scraping"),
    ("Licensing & Cost", "100% Free / Open-Source Architecture", "High usage-based pricing ($15+/host/mo)", "Freemium tiered subscription", "Free open-source (Cloud hosting cost)")
]

for row_idx, r_data in enumerate(bench_data):
    for col_idx, val in enumerate(r_data):
        cell = tbl.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(241, 248, 249) if col_idx == 1 else (RGBColor(255, 255, 255) if row_idx % 2 == 0 else COLOR_CARD_BG)
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = "Calibri"; p.font.size = Pt(10.5)
        p.font.bold = (col_idx <= 1)
        p.font.color.rgb = COLOR_TEAL_ACCENT if col_idx == 1 else COLOR_DARK_TEXT
        p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 5: SYSTEM ARCHITECTURE & DUAL-MODE ENGINE
# ==============================================================================
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide5, "Three-Tier Architecture & Dual-Mode Operational Engine", "SYSTEM ARCHITECTURE")

tiers = [
    ("Tier 1: Presentation & Visualization Layer", 
     "• HTML5 Semantic DOM + CSS Custom Properties with Acrylic Glassmorphism.\n• Responsive Dark/Light dynamic theming and custom multi-tenant trigger popovers.\n• Six hardware-accelerated Chart.js canvas widgets running at fluid 60fps via requestAnimationFrame().",
     Inches(0.9)),
    ("Tier 2: Business Logic & Network Engine", 
     "• Asynchronous diagnostic worker capturing monotonic timing via window.performance.now().\n• W3C CORS-resilient HEAD network dispatcher preventing cross-origin preflight errors.\n• 5,000ms AbortController circuit breaker preventing client socket starvation and thread lockup.",
     Inches(4.8)),
    ("Tier 3: Dual-Mode Persistence Layer", 
     "• Autonomous Mode: Zero-dependency Web Storage API (localStorage) with cryptographic scoping.\n• Enterprise Mode: Decoupled PHP 8.x PDO backend connecting to normalized MySQL 8.0 schema.\n• Parameterized prepared SQL statements preventing SQL injection attacks.",
     Inches(8.7))
]

for title, content, x_pos in tiers:
    c = add_card(slide5, x_pos, Inches(1.5), Inches(3.7), Inches(5.2))
    tf = c.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Calibri"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY
    p2 = tf.add_paragraph()
    p2.text = content
    p2.font.name = "Calibri"; p2.font.size = Pt(11.5); p2.font.color.rgb = COLOR_DARK_TEXT

# ==============================================================================
# SLIDE 6: RELATIONAL DATABASE SCHEMA & DATA MODELS
# ==============================================================================
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide6, "Normalized MySQL 8.0 Schema & Entity Relationships", "DATA PERSISTENCE & MODELS")

tables_data = [
    ("users (Authentication & Workspace Scoping)", 
     "• id (INT, PK, AUTO_INCREMENT)\n• username (VARCHAR(50), UNIQUE, NOT NULL)\n• email (VARCHAR(100), UNIQUE, NOT NULL)\n• password_hash (VARCHAR(255), NOT NULL)\n• role (ENUM('admin', 'developer'), DEFAULT 'developer')\n• created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)",
     Inches(0.9), Inches(1.5)),
    ("api_endpoints (Target Service Catalog)", 
     "• id (INT, PK, AUTO_INCREMENT)\n• user_id (INT, FK -> users.id, ON DELETE CASCADE)\n• name (VARCHAR(100), NOT NULL)\n• url (VARCHAR(500), NOT NULL)\n• method (ENUM('GET','POST','PUT','DELETE'))\n• expected_status (INT, DEFAULT 200)\n• timeout_ms / threshold_ms (INT)\n• is_active (BOOLEAN, DEFAULT TRUE)",
     Inches(6.8), Inches(1.5)),
    ("health_logs (Forensic Telemetry Ring Buffer)", 
     "• id (BIGINT, PK, AUTO_INCREMENT)\n• endpoint_id (INT, FK -> api_endpoints.id, ON DELETE CASCADE)\n• user_id (INT, FK -> users.id, ON DELETE CASCADE)\n• status (ENUM('healthy', 'slow', 'failed'))\n• latency_ms (DECIMAL(8,2), NOT NULL)\n• http_code (INT, NULL)\n• tested_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)",
     Inches(0.9), Inches(4.3)),
    ("performance_metrics (Aggregated Analytical Rollups)", 
     "• id (INT, PK, AUTO_INCREMENT)\n• endpoint_id (INT, FK -> api_endpoints.id, ON DELETE CASCADE)\n• avg_latency_ms / min_latency_ms / max_latency_ms\n• total_checks / success_count / failure_count (INT)\n• uptime_percentage (DECIMAL(5,2))\n• last_calculated (TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)",
     Inches(6.8), Inches(4.3))
]

for title, fields, x, y in tables_data:
    c = add_card(slide6, x, y, Inches(5.6), Inches(2.6))
    tf = c.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Calibri"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT
    p2 = tf.add_paragraph()
    p2.text = fields
    p2.font.name = "Calibri"; p2.font.size = Pt(11); p2.font.color.rgb = COLOR_DARK_TEXT

# ==============================================================================
# SLIDE 7: MATHEMATICAL ENGINES & CORS PROBING ALGORITHMS
# ==============================================================================
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide7, "Mathematical Telemetry Formulation & Probing Circuit Breakers", "CORE ENGINES")

# Left Column: Mathematical Formulation
c1 = add_card(slide7, Inches(0.9), Inches(1.5), Inches(5.6), Inches(5.2))
tf = c1.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0.25)
p = tf.paragraphs[0]
p.text = "Mathematical Formulations"
p.font.name = "Calibri"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY

p = tf.add_paragraph()
p.text = "1. Monotonic Latency Round-Trip Time:\n   T_rt = t_response - t_request\n   (via window.performance.now() to avoid system clock skew)"
p.font.name = "Calibri"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT

p = tf.add_paragraph()
p.text = "2. Deterministic Health Classification Function H(t):"
p.font.name = "Calibri"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT

tiers_list = [
    ("• Healthy (Emerald):", "T_rt < 500 ms (Meets strict consumer SLAs)"),
    ("• Slow (Amber):", "500 ms <= T_rt <= 1500 ms (Congestion warning)"),
    ("• Critical (Orange):", "1500 ms < T_rt <= 5000 ms (Severe degradation)"),
    ("• Failed (Crimson):", "T_rt > 5000 ms or Timeout / Network Drop")
]
for t_lbl, t_val in tiers_list:
    p = tf.add_paragraph()
    p.text = f"   {t_lbl} {t_val}"
    p.font.name = "Calibri"; p.font.size = Pt(11); p.font.color.rgb = COLOR_DARK_TEXT

p = tf.add_paragraph()
p.text = "3. Empirical Uptime Metric U(t):\n   U = (Total Successes / Total Probes) * 100%"
p.font.name = "Calibri"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT

# Right Column: CORS & Circuit Breaker Workflow
c2 = add_card(slide7, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.2))
tf = c2.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0.25)
p = tf.paragraphs[0]
p.text = "CORS-Resilient Probing & Circuit Breakers"
p.font.name = "Calibri"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY

p = tf.add_paragraph()
p.text = "• The CORS Problem: Browser security blocks client-side fetch() responses when target APIs omit Access-Control-Allow-Origin headers, inducing false-positive offline alerts."
p.font.name = "Calibri"; p.font.size = Pt(12); p.font.color.rgb = COLOR_DARK_TEXT

p = tf.add_paragraph()
p.text = "• Innovative Solution (mode: 'no-cors' + HEAD): The browser performs full TCP and TLS handshakes in an opaque transport request. While JS cannot read payload bodies, performance.now() measures exact transport round-trip timing."
p.font.name = "Calibri"; p.font.size = Pt(12); p.font.color.rgb = COLOR_DARK_TEXT

p = tf.add_paragraph()
p.text = "• 5,000ms AbortController Circuit Breaker: Binds an AbortSignal to every probe. If the remote socket stalls past 5 seconds, controller.abort() triggers immediately, neutralizing client socket leaks and thread lockup."
p.font.name = "Calibri"; p.font.size = Pt(12); p.font.color.rgb = COLOR_DARK_TEXT

# ==============================================================================
# HELPER: SCREENSHOT DISPLAY SLIDE
# ==============================================================================
def create_screenshot_slide(prs, title, super_title, img_path, bullets, fig_label):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, title, super_title)
    
    # Left: Screenshot Container
    c_img = add_card(slide, Inches(0.9), Inches(1.5), Inches(6.8), Inches(5.2), RGBColor(255, 255, 255))
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(1.05), Inches(1.65), width=Inches(6.5))
    
    # Right: Technical Analysis Container
    c_desc = add_card(slide, Inches(8.0), Inches(1.5), Inches(4.4), Inches(5.2))
    tf = c_desc.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0.25)
    
    p = tf.paragraphs[0]
    p.text = fig_label
    p.font.name = "Calibri"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY
    
    for b_title, b_desc in bullets:
        p = tf.add_paragraph()
        p.text = f"{b_title}: "
        p.font.name = "Calibri"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT
        r = p.add_run()
        r.text = b_desc
        r.font.name = "Calibri"; r.font.size = Pt(11); r.font.color.rgb = COLOR_DARK_TEXT
        
    return slide

# ==============================================================================
# SLIDE 8: FIGURE 5.1 - PRIMARY DASHBOARD
# ==============================================================================
create_screenshot_slide(
    prs, 
    "Live Screen Output: Real-Time APM Dashboard Viewport", 
    "SYSTEM IMPLEMENTATION & OUTPUTS",
    "report_screenshots/fig1_dashboard.png",
    [
        ("Gradient Hero Card", "Displays aggregate throughput (23.00K+ logged evaluations) with real-time status pulses."),
        ("24-Hour Latency Wave", "Multi-series spline chart rendering microsecond-accurate RTT fluctuations with Bézier easing."),
        ("Health Counters", "Emerald for Healthy (78%), Amber for Slow (16%), and Crimson for Outages (6%)."),
        ("Circular Donut Gauge", "Visualizes overall infrastructure reliability (99.8% Uptime SLA)."),
        ("Architectural Impact", "Maintains 60fps canvas animations with zero main-thread contention.")
    ],
    "Figure 5.1: Primary Dashboard"
)

# ==============================================================================
# SLIDE 9: FIGURE 5.2 - MULTI-TENANT AUTHENTICATION
# ==============================================================================
create_screenshot_slide(
    prs, 
    "Live Screen Output: Multi-Tenant Workspace Partitioning", 
    "SYSTEM IMPLEMENTATION & OUTPUTS",
    "report_screenshots/fig2_auth.png",
    [
        ("Profile Popover", "Acrylic glassmorphism trigger showing active developer credentials and role badge."),
        ("Tenant Switching", "Enables instantaneous switching between isolated environments (User 1 vs. User 2)."),
        ("Storage Scoping", "Cryptographically partitions localStorage keys and MySQL user_id foreign keys."),
        ("Zero Data Contamination", "Eliminates endpoint collisions on shared testing terminals and lab machines."),
        ("Session Security", "Protected dashboard features enforce strict session guards and token verification.")
    ],
    "Figure 5.2: Multi-Tenant Scoping"
)

# ==============================================================================
# SLIDE 10: FIGURE 5.3 - API ENDPOINT MANAGEMENT
# ==============================================================================
create_screenshot_slide(
    prs, 
    "Live Screen Output: API Endpoint CRUD Registration", 
    "SYSTEM IMPLEMENTATION & OUTPUTS",
    "report_screenshots/fig3_apis.png",
    [
        ("Registration Form", "Allows instant onboarding of endpoints with HTTP verbs (GET, POST, PUT, DELETE)."),
        ("URL Validation & XSS", "Client-side regex enforces strict http:// and https:// schemes, neutralizing XSS attacks."),
        ("Administrative Data Table", "Renders active service catalog with method pills and status indicators."),
        ("Live String Filtering", "Search bar enables instantaneous sub-millisecond filtering across registered endpoints."),
        ("Reactive State Update", "Persists changes simultaneously to local storage and MySQL PDO backend.")
    ],
    "Figure 5.3: API Management"
)

# ==============================================================================
# SLIDE 11: FIGURE 5.4 - LIVE MONITOR CARDS & TARGETED PINGS
# ==============================================================================
create_screenshot_slide(
    prs, 
    "Live Screen Output: Diagnostic Monitor Cards & Pings", 
    "SYSTEM IMPLEMENTATION & OUTPUTS",
    "report_screenshots/fig4_monitor.png",
    [
        ("Autonomous Monitor Cards", "Glassmorphism cards representing individual microservice health."),
        ("Isolated Ping Actions", "On-demand 'Ping' button enables targeted health checks without full system sweeps."),
        ("State Transitioning", "Visual card borders dynamically glow green (<500ms), amber (500-1500ms), or red (>5000ms)."),
        ("Head-of-Line Prevention", "Lightweight HEAD probing reduces client bandwidth consumption by 95%."),
        ("AbortController Signal", "Hardware timer terminates dead connections precisely at 5.0 seconds.")
    ],
    "Figure 5.4: Live Monitor Cards"
)

# ==============================================================================
# SLIDE 12: FIGURE 5.5 - DIAGNOSTIC AUDIT LOGS & FILTERING
# ==============================================================================
create_screenshot_slide(
    prs, 
    "Live Screen Output: Forensic Telemetry Audit History", 
    "SYSTEM IMPLEMENTATION & OUTPUTS",
    "report_screenshots/fig5_history.png",
    [
        ("Forensic Audit Ledger", "Chronologically ordered log capturing atomic diagnostic snapshots."),
        ("Ring Buffer Architecture", "Fixed-capacity buffer (500 records) prevents unbounded client memory growth."),
        ("Multi-Criteria Querying", "Dual-dropdown menus allow simultaneous filtering by Service Name and Status."),
        ("Export Engine", "One-click CSV / JSON export for compliance audits and post-mortem incident reports."),
        ("Root Cause Analysis", "Differentiates transient network drops from systemic backend server crashes.")
    ],
    "Figure 5.5: Diagnostic Audit Logs"
)

# ==============================================================================
# SLIDE 13: FIGURE 5.6 - VISUAL PERFORMANCE ANALYTICS
# ==============================================================================
create_screenshot_slide(
    prs, 
    "Live Screen Output: Visual Performance Analytics Breakdown", 
    "SYSTEM IMPLEMENTATION & OUTPUTS",
    "report_screenshots/fig6_analytics.png",
    [
        ("Four Statistical KPI Cards", "Average Latency, Total Successes, Failure Incident Tally, and Slowest Endpoint."),
        ("Tri-Chart Pipeline", "24-hr Latency Trend Line, Status Doughnut, and Comparative Horizontal Bar Chart."),
        ("Custom Glassmorphism Filter", "Acrylic dropdown enables instant per-endpoint deep dives in under 5ms."),
        ("Hardware Rasterization", "Chart.js canvas pipeline maintains smooth cubic Bézier easing transitions."),
        ("SLA Verification", "Provides technical leads with objective mathematical proof for contractual uptime verification.")
    ],
    "Figure 5.6: Performance Analytics"
)

# ==============================================================================
# SLIDE 14: FIGURE 5.7 - GOOGLE LIGHTHOUSE AUDIT
# ==============================================================================
create_screenshot_slide(
    prs, 
    "Empirical Verification: Google Lighthouse Audit Benchmark", 
    "VERIFICATION & PERFORMANCE AUDIT",
    "report_screenshots/fig7_lighthouse.png",
    [
        ("Performance Score (98/100)", "Confirms near-zero execution overhead on desktop and mobile viewports."),
        ("Accessibility (100/100)", "Strict adherence to ARIA standards and high-contrast color ratios."),
        ("Best Practices & SEO (100/100)", "Modern HTTPS standards, clean semantics, and zero console warnings."),
        ("First Contentful Paint (0.4s)", "Renders initial UI in 400ms, outperforming Google's <1.8s threshold by 4x."),
        ("Total Blocking Time (0 ms)", "Main thread is completely non-blocking, ensuring instant UI responsiveness.")
    ],
    "Figure 5.7: Lighthouse Audit"
)

# ==============================================================================
# SLIDE 15: SECURITY, RELIABILITY & VERIFICATION MATRIX
# ==============================================================================
slide15 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide15, "Security Framework & Diagnostic Verification Suite", "SECURITY & RELIABILITY")

# Security Controls Card
c_sec = add_card(slide15, Inches(0.9), Inches(1.5), Inches(5.6), Inches(5.2))
tf = c_sec.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0.25)
p = tf.paragraphs[0]
p.text = "Implemented Security Controls"
p.font.name = "Calibri"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY

sec_items = [
    ("Parameterized SQL Prepared Statements", "PHP PDO controllers bind all query parameters, completely preventing SQL Injection (SQLi) vulnerabilities."),
    ("Strict XSS Neutralization", "All user-supplied endpoint names and URLs undergo regex protocol validation and HTML entity escaping before DOM injection."),
    ("Workspace Data Partitioning", "Cryptographic namespacing ensures User 1 cannot view, probe, or delete User 2's registered microservice endpoints."),
    ("Denial-of-Service Circuit Breakers", "Sequential batch probing enforces a 400ms delay interval, preventing client socket flooding and remote rate-limit firewalls.")
]
for title, desc in sec_items:
    p = tf.add_paragraph()
    p.text = f"• {title}: "
    p.font.name = "Calibri"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT
    r = p.add_run()
    r.text = desc
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.color.rgb = COLOR_DARK_TEXT

# Verification Matrix Table
rows, cols = 5, 4
tbl_shape = slide15.shapes.add_table(rows, cols, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.2))
tbl = tbl_shape.table
tbl.columns[0].width = Inches(1.5)
tbl.columns[1].width = Inches(1.5)
tbl.columns[2].width = Inches(1.7)
tbl.columns[3].width = Inches(0.9)

diag_headers = ["Stage", "Component", "Criteria", "Status"]
for col_idx, h in enumerate(diag_headers):
    cell = tbl.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_PRIMARY_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Calibri"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

diag_rows = [
    ("Network Engine", "Latency Probing", "W3C performance.now() sub-ms precision", "PASSED"),
    ("Fault Tolerance", "Circuit Breaker", "5,000ms AbortController timeout execution", "PASSED"),
    ("Data Isolation", "Multi-Tenant", "Strict User 1 vs User 2 storage scoping", "PASSED"),
    ("Core Web Vitals", "Lighthouse Audit", "Score >= 95, FCP < 0.5s, TBT = 0ms", "PASSED")
]
for row_idx, r_data in enumerate(diag_rows):
    for col_idx, val in enumerate(r_data):
        cell = tbl.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(241, 248, 249) if row_idx % 2 == 1 else RGBColor(255, 255, 255)
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = "Calibri"; p.font.size = Pt(10)
        p.alignment = PP_ALIGN.CENTER if col_idx in [0, 3] else PP_ALIGN.LEFT
        if col_idx == 3:
            p.font.bold = True
            p.font.color.rgb = COLOR_EMERALD

# ==============================================================================
# SLIDE 16: CONCLUSION & FUTURE ENHANCEMENTS
# ==============================================================================
slide16 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide16, "Project Accomplishments, Future Scope & Acknowledgments", "CONCLUSION & ROADMAP")

# Left Column: Project Conclusion
c_conc = add_card(slide16, Inches(0.9), Inches(1.5), Inches(5.6), Inches(5.2))
tf = c_conc.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0.25)
p = tf.paragraphs[0]
p.text = "Key Project Achievements"
p.font.name = "Calibri"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY

achievements = [
    ("Zero-Dependency Portability", "Delivered an autonomous APM dashboard that runs instantly in any browser without mandatory server daemons."),
    ("Microsecond-Accurate Telemetry", "Engineered non-blocking monotonic latency probing with 5-second circuit breaker fault tolerance."),
    ("Multi-Tenant Workspace Scoping", "Eliminated data collisions on shared developer workstations through cryptographic user scoping."),
    ("Full-Stack Decoupled Architecture", "Paired client portability with an enterprise MySQL 8.0 schema and secure PHP PDO REST controllers."),
    ("Lighthouse Validation", "Secured a 98/100 Performance score, 0.4s FCP, and 0ms TBT on Google Lighthouse.")
]
for title, desc in achievements:
    p = tf.add_paragraph()
    p.text = f"• {title}: "
    p.font.name = "Calibri"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_TEAL_ACCENT
    r = p.add_run()
    r.text = desc
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.color.rgb = COLOR_DARK_TEXT

# Right Column: Future Roadmap & Closing
c_fut = add_card(slide16, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.2))
tf = c_fut.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0.25)
p = tf.paragraphs[0]
p.text = "Future Enhancement Roadmap"
p.font.name = "Calibri"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY

roadmap = [
    ("Headless Background Daemon Probing", "Deploying Node.js or PHP cron workers for continuous 24/7 background telemetry collection."),
    ("Real-Time Incident Webhooks", "Automating instant outage notifications via Slack, Discord, Telegram bots, or Twilio SMS."),
    ("Geo-Distributed Multi-Region Edge Probing", "Deploying probes across serverless edge workers (Cloudflare Workers / AWS Lambda) for global latency mapping."),
    ("Automated PDF SLA Auditing", "Generating scheduled monthly uptime and SLA compliance audit reports for enterprise stakeholders.")
]
for title, desc in roadmap:
    p = tf.add_paragraph()
    p.text = f"• {title}: "
    p.font.name = "Calibri"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_NAVY
    r = p.add_run()
    r.text = desc
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.color.rgb = COLOR_DARK_TEXT

p_q = tf.add_paragraph()
p_q.alignment = PP_ALIGN.CENTER
p_q.text = "\nTHANK YOU!\nQuestions & Discussion"
p_q.font.name = "Calibri"; p_q.font.size = Pt(16); p_q.font.bold = True; p_q.font.color.rgb = COLOR_TEAL_ACCENT

# ==============================================================================
# SAVE PRESENTATIONS
# ==============================================================================
output_filename = "API_Monitoring_Project_Presentation.pptx"
prs.save(output_filename)
print(f"Presentation successfully built: {output_filename} (16 Slides)")
