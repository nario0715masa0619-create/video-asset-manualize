'''
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
