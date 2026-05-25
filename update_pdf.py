from pathlib import Path

pdf_code = '''"""
PDF Manual Renderer - Renders training_asset_spec to PDF.
"""

import json
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .settings import settings


class PDFManualRenderer:
    """Renders training_asset_spec JSON to PDF manual."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._register_fonts()
        self._setup_custom_styles()
    
    def _register_fonts(self):
        """Register Japanese fonts."""
        try:
            font_paths = [
                'C:/Windows/Fonts/meiryo.ttc',
                'C:/Windows/Fonts/msmincho.ttc',
                'C:/Windows/Fonts/yugothic.ttf',
            ]
            
            for font_path in font_paths:
                if Path(font_path).exists():
                    try:
                        pdfmetrics.registerFont(TTFont('JP', font_path))
                        break
                    except:
                        continue
        except:
            pass
    
    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#000000'),
            spaceAfter=12,
            fontName='JP',
        ))
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#007bff'),
            spaceAfter=12,
            fontName='JP',
        ))
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6,
            alignment=TA_LEFT,
            fontName='JP',
        ))
    
    def _build_document(self, asset_spec: dict) -> list:
        story = []
        asset_meta = asset_spec.get('asset_meta', {})
        instructional_core = asset_spec.get('instructional_core', {})
        _metadata = asset_spec.get('_metadata', {})
        
        story.append(Paragraph(asset_meta.get('title', 'Manual'), self.styles['CustomTitle']))
        story.append(Spacer(1, 12*mm))
        
        purpose = asset_meta.get('purpose', 'N/A')
        audience = ', '.join(asset_meta.get('target_audience', []))
        meta = f"<b>目的:</b> {purpose}<br/><b>対象者:</b> {audience}"
        story.append(Paragraph(meta, self.styles['CustomNormal']))
        story.append(Spacer(1, 12*mm))
        
        for chapter in instructional_core.get('chapters', []):
            story.append(PageBreak())
            story.append(Paragraph(chapter.get('title', ''), self.styles['CustomHeading2']))
            
            for procedure in chapter.get('procedures', []):
                story.append(Paragraph(procedure.get('title', ''), self.styles['CustomHeading2']))
                
                for step in procedure.get('steps', []):
                    order = step.get('order')
                    action = step.get('action', '')
                    text = f"<b>ステップ {order}:</b> {action}"
                    story.append(Paragraph(text, self.styles['CustomNormal']))
                    
                    if step.get('expected_result'):
                        result = step['expected_result']
                        text = f"期待される結果: {result}"
                        story.append(Paragraph(text, self.styles['CustomNormal']))
                
                story.append(Spacer(1, 6*mm))
        
        story.append(Spacer(1, 12*mm))
        generated_at = _metadata.get('generated_at', 'N/A')
        story.append(Paragraph(f"<i>Generated on {generated_at}</i>", self.styles['Normal']))
        
        return story
    
    def render_to_file(self, asset_spec: dict, output_file: Path) -> Path:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm,
        )
        
        story = self._build_document(asset_spec)
        doc.build(story)
        
        return output_file
'''

with open('src/video_asset_manualize/pdf_manual_renderer.py', 'w', encoding='utf-8') as f:
    f.write(pdf_code)

print('✓ pdf_manual_renderer.py を更新しました')
