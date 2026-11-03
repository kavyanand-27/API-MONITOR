import os, zipfile, shutil

thmx_dir = 'thmx_extracted'
base_dir = 'kpr_pptx_base'
if os.path.exists(base_dir):
    shutil.rmtree(base_dir)
os.makedirs(base_dir)

# 1. Copy and rename theme -> ppt
shutil.copytree(os.path.join(thmx_dir, 'theme'), os.path.join(base_dir, 'ppt'))
if os.path.exists(os.path.join(thmx_dir, 'docProps')):
    shutil.copytree(os.path.join(thmx_dir, 'docProps'), os.path.join(base_dir, 'docProps'))
else:
    os.makedirs(os.path.join(base_dir, 'docProps'))

# 2. _rels/.rels
os.makedirs(os.path.join(base_dir, '_rels'), exist_ok=True)
rels_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail" Target="docProps/thumbnail.jpeg"/>
</Relationships>"""
with open(os.path.join(base_dir, '_rels', '.rels'), 'w', encoding='utf-8') as f:
    f.write(rels_content)

# 3. [Content_Types].xml
with open(os.path.join(thmx_dir, '[Content_Types].xml'), 'r', encoding='utf-8') as f:
    ct_content = f.read().replace('/theme/', '/ppt/')
with open(os.path.join(base_dir, '[Content_Types].xml'), 'w', encoding='utf-8') as f:
    f.write(ct_content)

# 4. In ppt/presentation.xml, ensure sldIdLst exists
pres_xml_path = os.path.join(base_dir, 'ppt', 'presentation.xml')
with open(pres_xml_path, 'r', encoding='utf-8') as f:
    pres_xml = f.read()

if '<p:sldIdLst>' not in pres_xml and '<p:sldIdLst/>' not in pres_xml:
    idx = pres_xml.find('</p:sldMasterIdLst>') + len('</p:sldMasterIdLst>')
    pres_xml = pres_xml[:idx] + '<p:sldIdLst/>' + pres_xml[idx:]
    with open(pres_xml_path, 'w', encoding='utf-8') as f:
        f.write(pres_xml)

# 5. Pack into kpr_template.pptx
zip_path = 'kpr_template.pptx'
if os.path.exists(zip_path):
    os.remove(zip_path)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, base_dir)
            z.write(full_path, arcname)

print("Created kpr_template.pptx successfully!")

# Now test opening with python-pptx!
import pptx
prs = pptx.Presentation(zip_path)
print(f"python-pptx loaded kpr_template.pptx successfully! Layouts count: {len(prs.slide_layouts)}")
for i, l in enumerate(prs.slide_layouts):
    print(f"Layout {i}: {l.name}")

# Try adding a slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
print(f"Added slide successfully! Shapes on slide: {len(slide.shapes)}")
prs.save("test_out.pptx")
print("Saved test_out.pptx successfully!")
