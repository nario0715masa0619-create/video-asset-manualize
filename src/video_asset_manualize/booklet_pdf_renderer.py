'''
Booklet PDF Renderer
'''

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from video_asset_manualize.compiled_training_asset_builder import CompiledTrainingAsset


class BookletPDFRenderer:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._register_fonts()
        self._setup_custom_styles()
        
    def _register_fonts(self):
        self.jp_font_name = 'JP'
        try:
            from reportlab.pdfbase.cidfonts import CIDFont
            font_paths = [
                'C:/Windows/Fonts/meiryo.ttc',
                'C:/Windows/Fonts/msgothic.ttc',
                'C:/Windows/Fonts/yugothic.ttf',
                '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc'
            ]
            
            font_registered = False
            for font_path in font_paths:
                if Path(font_path).exists():
                    try:
                        pdfmetrics.registerFont(TTFont('JP', font_path))
                        font_registered = True
                        break
                    except:
                        continue
            
            if not font_registered:
                pdfmetrics.registerFont(CIDFont('HeiseiKakuGo-W5'))
                self.jp_font_name = 'HeiseiKakuGo-W5'
        except:
            pass

    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#000000'),
            spaceAfter=32,
            fontName=self.jp_font_name,
            alignment=TA_CENTER,
        ))
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#000000'),
            spaceAfter=24,
            fontName=self.jp_font_name,
        ))
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#007bff'),
            spaceAfter=20,
            spaceBefore=28,
            fontName=self.jp_font_name,
            fontBold=True,
        ))
        self.styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=16,
            spaceBefore=20,
            fontName=self.jp_font_name,
            fontBold=True,
        ))
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=20,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            alignment=TA_LEFT,
            fontName=self.jp_font_name,
        ))
    
    def render_to_file(self, compiled_asset: CompiledTrainingAsset, output_path: str):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        doc = SimpleDocTemplate(str(output_path), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)
        story = []
        
        story.append(Spacer(1, 3*cm))
        story.append(Paragraph(compiled_asset.title, self.styles['CustomTitle']))
        story.append(Spacer(1, 1*cm))
        
        story.append(PageBreak())
        story.append(Paragraph("目次 (Table of Contents)", self.styles['CustomHeading1']))
        
        toc = compiled_asset.get_table_of_contents()
        for section in toc:
            story.append(Paragraph(f"Section {section['section']}: {section['title']}", self.styles['CustomHeading3']))
            for chapter in section['chapters']:
                story.append(Paragraph(f"• {chapter['title']}", self.styles['CustomNormal']))
        
        for idx, asset in enumerate(compiled_asset.assets, 1):
            story.append(PageBreak())
            asset_meta = asset.get('asset_meta', {})
            instructional_core = asset.get('instructional_core', {})
            
            story.append(Paragraph(f"Section {idx}: {asset_meta.get('title', 'Untitled')}", self.styles['CustomHeading1']))
            story.append(Paragraph(f"Asset ID: {asset_meta.get('asset_id', 'unknown')}", self.styles['CustomNormal']))
            story.append(Spacer(1, 0.5*cm))
            
            for chapter in instructional_core.get('chapters', []):
                story.append(Paragraph(chapter.get('title', 'Chapter'), self.styles['CustomHeading2']))
                for procedure in chapter.get('procedures', []):
                    story.append(Paragraph(procedure.get('title', 'Procedure'), self.styles['CustomHeading3']))
                    for step in procedure.get('steps', []):
                        story.append(Paragraph(f"アクション: {step.get('action', 'N/A')}", self.styles['CustomNormal']))
                        story.append(Spacer(1, 2*mm))
        
        doc.build(story)
