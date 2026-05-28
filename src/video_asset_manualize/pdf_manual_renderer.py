"""
PDF Manual Renderer - Renders training_asset_spec to PDF.
"""

import json
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .settings import settings


class PDFManualRenderer:
    """Renders training_asset_spec JSON to PDF manual."""
"""
PDF Manual Renderer - Renders training_asset_spec to PDF.
"""

import json
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
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
        self.jp_font_name = 'JP'
        font_registered = False
        
        try:
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            
            # Known hardcoded paths for Windows and common Linux distributions
            font_paths = [
                'C:/Windows/Fonts/meiryo.ttc',
                'C:/Windows/Fonts/msgothic.ttc',
                'C:/Windows/Fonts/yugothic.ttf',
                '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc'
            ]
            
            # Dynamically find Noto Sans CJK in Linux
            import glob
            linux_font_search_paths = [
                '/usr/share/fonts/**/NotoSansCJK*.ttc',
                '/usr/share/fonts/**/NotoSansCJK*.otf',
                '/usr/share/fonts/**/NotoSansJP*.otf',
                '/usr/share/fonts/**/NotoSansJP*.ttf'
            ]
            for search_path in linux_font_search_paths:
                found_fonts = glob.glob(search_path, recursive=True)
                if found_fonts:
                    font_paths.extend(found_fonts)
            
            # Optional debug: use fc-list if available
            try:
                import subprocess
                result = subprocess.run(['fc-list', ':lang=ja', 'file'], capture_output=True, text=True)
                for line in result.stdout.splitlines():
                    path = line.split(':')[0].strip()
                    if path.endswith(('.ttc', '.ttf', '.otf')) and path not in font_paths:
                        font_paths.append(path)
            except Exception as e:
                import logging
                logging.debug(f"fc-list check skipped: {e}")

            for font_path in font_paths:
                if Path(font_path).exists():
                    try:
                        pdfmetrics.registerFont(TTFont('JP', font_path))
                        font_registered = True
                        break
                    except Exception as e:
                        import logging
                        logging.debug(f"Failed to register font {font_path}: {e}")
                        continue
            
            if not font_registered:
                pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
                self.jp_font_name = 'HeiseiKakuGo-W5'
        except Exception as e:
            import logging
            logging.error(f"Font registration failed completely: {e}")
            pass
    
    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            leading=36,
            spaceBefore=16,
            spaceAfter=28,
            textColor=colors.HexColor('#000000'),
            fontName=self.jp_font_name,
            alignment=TA_CENTER,
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
        self.styles.add(ParagraphStyle(
            name='StepLabel',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#ffffff'),
            backColor=colors.HexColor('#007bff'),
            spaceAfter=6,
            fontName=self.jp_font_name,
            fontBold=True,
            leftIndent=4,
            rightIndent=4,
            topPadding=4,
            bottomPadding=4,
        ))
        self.styles.add(ParagraphStyle(
            name='SectionLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#ffffff'),
            backColor=colors.HexColor('#28a745'),
            spaceAfter=6,
            fontName=self.jp_font_name,
            fontBold=True,
            leftIndent=4,
            rightIndent=4,
            topPadding=3,
            bottomPadding=3,
        ))
        self.styles.add(ParagraphStyle(
            name='CautionLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#ffffff'),
            backColor=colors.HexColor('#dc3545'),
            spaceAfter=6,
            fontName=self.jp_font_name,
            fontBold=True,
            leftIndent=4,
            rightIndent=4,
            topPadding=3,
            bottomPadding=3,
        ))
        self.styles.add(ParagraphStyle(
            name='CautionText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#8b0000'),
            spaceAfter=4,
            fontName=self.jp_font_name,
            leftIndent=12,
        ))
    
    def _build_document(self, asset_spec: dict) -> list:
        story = []
        asset_meta = asset_spec.get('asset_meta', {})
        instructional_core = asset_spec.get('instructional_core', {})
        derived_views = asset_spec.get('derived_views', {})
        _metadata = asset_spec.get('_metadata', {})
        
        story.append(Paragraph(asset_meta.get('title', 'Manual'), self.styles['CustomTitle']))
        story.append(Spacer(1, 12*mm))
        
        purpose = asset_meta.get('purpose', 'N/A')
        audience = ', '.join(asset_meta.get('target_audience', []))
        status = asset_meta.get('status', 'N/A')
        version = asset_meta.get('version', 'N/A')
        
        meta_html = f"<b>目的:</b> {purpose}<br/><b>対象者:</b> {audience}<br/><b>ステータス:</b> {status}<br/><b>バージョン:</b> {version}"
        story.append(Paragraph(meta_html, self.styles['CustomNormal']))
        story.append(Spacer(1, 16*mm))
        
        if asset_meta.get('prerequisites'):
            story.append(Paragraph('前提条件・準備', self.styles['CustomHeading2']))
            for pre in asset_meta['prerequisites']:
                story.append(Paragraph(f"• {pre}", self.styles['CustomNormal']))
            story.append(Spacer(1, 12*mm))
        
        summary = instructional_core.get('summary', {})
        if summary:
            story.append(Paragraph('概要', self.styles['CustomHeading2']))
            if summary.get('purpose_summary'):
                story.append(Paragraph(f"<b>目的:</b> {summary['purpose_summary']}", self.styles['CustomNormal']))
            if summary.get('outcome_summary'):
                story.append(Paragraph(f"<b>期待する成果:</b> {summary['outcome_summary']}", self.styles['CustomNormal']))
            story.append(Spacer(1, 12*mm))
        
        if instructional_core.get('global_cautions'):
            story.append(Paragraph('⚠️ 全体注意事項', self.styles['CustomHeading2']))
            for caution in instructional_core['global_cautions']:
                story.append(Paragraph(f"• {caution}", self.styles['CautionText']))
            story.append(Spacer(1, 12*mm))
        
        for chapter in instructional_core.get('chapters', []):
            story.append(PageBreak())
            story.append(Paragraph(chapter.get('title', ''), self.styles['CustomHeading2']))
            
            if chapter.get('objective'):
                story.append(Paragraph(f"<b>目標:</b> {chapter['objective']}", self.styles['CustomNormal']))
            
            if chapter.get('chapter_cautions'):
                story.append(Paragraph('<b>注意事項</b>', self.styles['CustomHeading3']))
                for caution in chapter['chapter_cautions']:
                    story.append(Paragraph(f"• {caution}", self.styles['CautionText']))
                story.append(Spacer(1, 6*mm))
            
            for procedure in chapter.get('procedures', []):
                story.append(Paragraph(procedure.get('title', ''), self.styles['CustomHeading3']))
                
                if procedure.get('goal'):
                    story.append(Paragraph('ゴール', self.styles['SectionLabel']))
                    story.append(Paragraph(f"{procedure['goal']}", self.styles['CustomNormal']))
                    story.append(Spacer(1, 4*mm))
                
                if procedure.get('conditions'):
                    story.append(Paragraph(f"<b>条件:</b> {'; '.join(procedure['conditions'])}", self.styles['CustomNormal']))
                
                for step in procedure.get('steps', []):
                    order = step.get('order')
                    action = step.get('action', '')
                    step_label = f"ステップ {order}"
                    story.append(Paragraph(step_label, self.styles['StepLabel']))
                    story.append(Paragraph(action, self.styles['CustomNormal']))
                    story.append(Spacer(1, 2*mm))
                    
                    if step.get('expected_result'):
                        result = step['expected_result']
                        story.append(Paragraph(f"<b>期待される結果:</b> {result}", self.styles['CustomNormal']))
                    
                    if step.get('button_labels'):
                        buttons = ', '.join(step['button_labels'])
                        story.append(Paragraph(f"<b>ボタン:</b> {buttons}", self.styles['CustomNormal']))
                    
                    if step.get('input_fields'):
                        fields = ', '.join(step['input_fields'])
                        story.append(Paragraph(f"<b>入力項目:</b> {fields}", self.styles['CustomNormal']))
                    
                    if step.get('notes'):
                        story.append(Paragraph('💡 ノート', self.styles['SectionLabel']))
                        for note in step['notes']:
                            story.append(Paragraph(f"• {note}", self.styles['CustomNormal']))
                    
                    if step.get('cautions'):
                        story.append(Paragraph('⚠️ 注意', self.styles['CautionLabel']))
                        for caution in step['cautions']:
                            story.append(Paragraph(f"• {caution}", self.styles['CautionText']))
                    
                    story.append(Spacer(1, 10*mm))
                
                if procedure.get('cautions'):
                    story.append(Paragraph('<b>手順の注意事項</b>', self.styles['CustomHeading3']))
                    for caution in procedure['cautions']:
                        story.append(Paragraph(f"• {caution}", self.styles['CautionText']))
                    story.append(Spacer(1, 10*mm))
                
                if procedure.get('common_mistakes'):
                    story.append(Paragraph('<b>よくあるミス</b>', self.styles['CustomHeading3']))
                    for mistake in procedure['common_mistakes']:
                        text = f"<b>❌ {mistake.get('mistake', '')}</b>"
                        story.append(Paragraph(text, self.styles['CustomNormal']))
                        if mistake.get('cause'):
                            story.append(Paragraph(f"<b>原因:</b> {mistake['cause']}", self.styles['CustomNormal']))
                        if mistake.get('impact'):
                            story.append(Paragraph(f"<b>影響:</b> {mistake['impact']}", self.styles['CustomNormal']))
                        if mistake.get('recovery_action'):
                            story.append(Paragraph(f"<b>対策:</b> {mistake['recovery_action']}", self.styles['CustomNormal']))
                        story.append(Spacer(1, 6*mm))
                
                if procedure.get('checkpoints'):
                    story.append(Paragraph('<b>✓ チェックポイント</b>', self.styles['CustomHeading3']))
                    for checkpoint in procedure['checkpoints']:
                        story.append(Paragraph(f"☐ {checkpoint}", self.styles['CustomNormal']))
                    story.append(Spacer(1, 10*mm))
        
        if derived_views.get('faq_candidates'):
            story.append(PageBreak())
            story.append(Paragraph('よくある質問（FAQ候補）', self.styles['CustomHeading2']))
            
            for faq in derived_views['faq_candidates']:
                story.append(Paragraph(f"Q: {faq.get('question', '')}", self.styles['CustomHeading3']))
                story.append(Paragraph(f"A: {faq.get('answer_draft', '')}", self.styles['CustomNormal']))
                if faq.get('priority'):
                    story.append(Paragraph(f"<b>優先度:</b> {faq['priority']}", self.styles['CustomNormal']))
                story.append(Spacer(1, 6*mm))
        
        if instructional_core.get('global_checklist'):
            story.append(PageBreak())
            story.append(Paragraph('全体チェックリスト', self.styles['CustomHeading2']))
            
            for item in instructional_core['global_checklist']:
                required = '<b style="color:red;">*必須</b>' if item.get('required') else ''
                story.append(Paragraph(f"☐ {item.get('item')} {required}", self.styles['CustomNormal']))
            
            story.append(Spacer(1, 12*mm))
        
        story.append(Spacer(1, 12*mm))
        generated_at = _metadata.get('generated_at', 'N/A')
        schema_version = _metadata.get('schema_version', 'N/A')
        story.append(Paragraph(
            f"<i>Generated on {generated_at} (Schema v{schema_version})</i>",
            self.styles['Normal']
        ))
        
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

