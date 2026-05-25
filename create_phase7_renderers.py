"""
Phase 7 Compiled Spec Builder と Booklet Renderer 作成スクリプト（修正版v2）
"""

from pathlib import Path

# ========== 1. compiled_training_asset_builder.py ==========
compiled_builder_code = """'''
Compiled Training Asset Builder
'''

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from uuid import uuid4


class CompiledTrainingAsset:
    def __init__(self, project_id: str, title: str, description: str = ""):
        self.project_id = project_id
        self.title = title
        self.description = description
        self.assets = []
        self.created_at = datetime.utcnow().isoformat() + 'Z'
        self.compiled_id = f"compiled-{uuid4().hex[:8]}"
    
    def add_asset(self, spec: Dict[str, Any]):
        self.assets.append(spec)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'compiled_id': self.compiled_id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'asset_count': len(self.assets),
            'assets': self.assets
        }
    
    def get_table_of_contents(self) -> List[Dict[str, Any]]:
        toc = []
        for idx, asset in enumerate(self.assets, 1):
            asset_meta = asset.get('asset_meta', {})
            instructional_core = asset.get('instructional_core', {})
            chapters = instructional_core.get('chapters', [])
            
            toc.append({
                'section': idx,
                'asset_id': asset_meta.get('asset_id', 'unknown'),
                'title': asset_meta.get('title', 'Untitled'),
                'chapter_count': len(chapters),
                'chapters': [{'chapter_id': ch.get('chapter_id', ''), 'title': ch.get('title', '')} for ch in chapters]
            })
        return toc
    
    def save(self, output_path: str):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)


class CompiledTrainingAssetBuilder:
    @staticmethod
    def compile_specs(specs: List[Dict[str, Any]], project_id: str, title: str, description: str = "") -> CompiledTrainingAsset:
        compiled = CompiledTrainingAsset(project_id, title, description)
        for spec in specs:
            compiled.add_asset(spec)
        return compiled
"""

Path("src/video_asset_manualize/compiled_training_asset_builder.py").write_text(compiled_builder_code, encoding='utf-8')
print("OK: compiled_training_asset_builder.py")

# ========== 2. booklet_html_renderer.py ==========
booklet_html_code = """'''
Booklet HTML Renderer
'''

from pathlib import Path
from datetime import datetime
from video_asset_manualize.compiled_training_asset_builder import CompiledTrainingAsset


class BookletHTMLRenderer:
    def render(self, compiled_asset: CompiledTrainingAsset) -> str:
        assets = compiled_asset.assets
        toc = compiled_asset.get_table_of_contents()
        
        html_parts = []
        html_parts.append(self._get_header(compiled_asset))
        html_parts.append(self._render_toc(toc))
        html_parts.append('<div style="page-break-after: always;"></div>')
        
        for idx, asset in enumerate(assets, 1):
            html_parts.append(self._render_asset_section(idx, asset))
        
        html_parts.append(self._get_footer(compiled_asset))
        return '\\n'.join(html_parts)
    
    def _get_header(self, compiled_asset: CompiledTrainingAsset) -> str:
        title = compiled_asset.title
        desc = compiled_asset.description or "Training Manual"
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        return f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 20px; line-height: 1.6;}}
        .cover {{text-align: center; padding: 100px 20px; border: 2px solid #007bff;}}
        .cover h1 {{font-size: 2.5em; color: #007bff;}}
        .section {{page-break-after: always; margin: 30px 0;}}
        .asset-title {{color: #007bff; border-bottom: 2px solid #007bff; padding: 10px 0;}}
        .chapter {{margin: 20px 0; padding: 10px; border-left: 4px solid #28a745;}}
        .step {{margin: 10px 0; padding: 10px; background: #f8f9fa;}}
        .caution {{background: #fff3cd; padding: 10px; margin: 10px 0;}}
        .toc {{margin: 20px 0;}}
        footer {{text-align: center; margin-top: 40px; color: #999;}}
    </style>
</head>
<body>

<div class="cover">
    <h1>{title}</h1>
    <p>{desc}</p>
    <p style="margin-top: 30px; color: #999;">Generated: {timestamp}</p>
</div>
'''
    
    def _render_toc(self, toc) -> str:
        toc_html = '<div class="toc"><h2>Table of Contents</h2>'
        for section in toc:
            toc_html += f'<h3>Section {section["section"]}: {section["title"]}</h3>\\n'
            for chapter in section['chapters']:
                toc_html += f'<div style="margin-left: 20px;">- {chapter["title"]}</div>\\n'
        toc_html += '</div>'
        return toc_html
    
    def _render_asset_section(self, section_num: int, asset: dict) -> str:
        asset_meta = asset.get('asset_meta', {})
        instructional_core = asset.get('instructional_core', {})
        summary = instructional_core.get('summary', {})
        
        html = f'''<div class="section">
<div class="asset-title"><h2>Section {section_num}: {asset_meta.get('title', 'Untitled')}</h2></div>
<p><strong>Asset ID:</strong> {asset_meta.get('asset_id', 'unknown')}</p>
<p><strong>Purpose:</strong> {summary.get('purpose', 'N/A')}</p>
'''
        
        for chapter in instructional_core.get('chapters', []):
            html += f'<div class="chapter"><h3>{chapter.get("title", "Chapter")}</h3>'
            for procedure in chapter.get('procedures', []):
                html += f'<div><strong>{procedure.get("title", "Procedure")}</strong>'
                for step in procedure.get('steps', []):
                    html += f'<div class="step"><strong>Action:</strong> {step.get("action", "N/A")}<br><strong>Expected:</strong> {step.get("expected_result", "N/A")}</div>'
                html += '</div>'
            html += '</div>'
        
        for caution in instructional_core.get('global_cautions', []):
            html += f'<div class="caution"><strong>Caution:</strong> {caution}</div>'
        
        html += '</div>'
        return html
    
    def _get_footer(self, compiled_asset: CompiledTrainingAsset) -> str:
        title = compiled_asset.title
        asset_count = len(compiled_asset.assets)
        date = datetime.utcnow().strftime('%Y-%m-%d')
        
        return f'''
<footer>
    <p>Compiled Training Manual: {title}</p>
    <p>Total Assets: {asset_count} | Generated: {date}</p>
</footer>

</body>
</html>
'''
    
    def render_to_file(self, compiled_asset: CompiledTrainingAsset, output_path: str):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        html_content = self.render(compiled_asset)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
"""

Path("src/video_asset_manualize/booklet_html_renderer.py").write_text(booklet_html_code, encoding='utf-8')
print("OK: booklet_html_renderer.py")

# ========== 3. booklet_pdf_renderer.py ==========
booklet_pdf_code = """'''
Booklet PDF Renderer
'''

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from video_asset_manualize.compiled_training_asset_builder import CompiledTrainingAsset


class BookletPDFRenderer:
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def render_to_file(self, compiled_asset: CompiledTrainingAsset, output_path: str):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        doc = SimpleDocTemplate(str(output_path), pagesize=A4)
        story = []
        
        story.append(Spacer(1, 3*cm))
        story.append(Paragraph(compiled_asset.title, self.styles['Heading1']))
        story.append(Spacer(1, 1*cm))
        
        story.append(PageBreak())
        story.append(Paragraph("Table of Contents", self.styles['Heading1']))
        
        toc = compiled_asset.get_table_of_contents()
        for section in toc:
            story.append(Paragraph(f"Section {section['section']}: {section['title']}", self.styles['Heading3']))
            for chapter in section['chapters']:
                story.append(Paragraph(f"- {chapter['title']}", self.styles['Normal']))
        
        for idx, asset in enumerate(compiled_asset.assets, 1):
            story.append(PageBreak())
            asset_meta = asset.get('asset_meta', {})
            instructional_core = asset.get('instructional_core', {})
            
            story.append(Paragraph(f"Section {idx}: {asset_meta.get('title', 'Untitled')}", self.styles['Heading1']))
            story.append(Paragraph(f"Asset ID: {asset_meta.get('asset_id', 'unknown')}", self.styles['Normal']))
            story.append(Spacer(1, 0.5*cm))
            
            for chapter in instructional_core.get('chapters', []):
                story.append(Paragraph(chapter.get('title', 'Chapter'), self.styles['Heading2']))
                for procedure in chapter.get('procedures', []):
                    story.append(Paragraph(procedure.get('title', 'Procedure'), self.styles['Heading3']))
                    for step in procedure.get('steps', []):
                        story.append(Paragraph(f"Action: {step.get('action', 'N/A')}", self.styles['Normal']))
                        story.append(Spacer(1, 0.2*cm))
        
        doc.build(story)
"""

Path("src/video_asset_manualize/booklet_pdf_renderer.py").write_text(booklet_pdf_code, encoding='utf-8')
print("OK: booklet_pdf_renderer.py")

print("\nOK: Phase 7 modules created")
