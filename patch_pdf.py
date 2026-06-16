import re
import sys

with open('src/video_asset_manualize/pdf_manual_renderer.py', 'r', encoding='utf-8') as f:
    content = f.read()

replacement1 = """    def _build_document(self, asset_spec: dict) -> list:
        from reportlab.platypus import Image
        
        story = []
        asset_meta = asset_spec.get('asset_meta', {})
        instructional_core = asset_spec.get('instructional_core', {})
        derived_views = asset_spec.get('derived_views', {})
        _metadata = asset_spec.get('_metadata', {})
        
        screenshot_map = {}
        source_evidence = asset_spec.get('source_evidence', {})
        candidates = source_evidence.get('screenshot_candidates', [])
        for cand in candidates:
            if cand.get('image_path') and Path(cand['image_path']).exists():
                screenshot_map[cand['screenshot_id']] = cand['image_path']"""

content = content.replace("""    def _build_document(self, asset_spec: dict) -> list:
        story = []
        asset_meta = asset_spec.get('asset_meta', {})
        instructional_core = asset_spec.get('instructional_core', {})
        derived_views = asset_spec.get('derived_views', {})
        _metadata = asset_spec.get('_metadata', {})""", replacement1)


replacement2 = """                for step in procedure.get('steps', []):
                    order = step.get('order')
                    action = step.get('action', '')
                    step_label = f"ステップ {order}"
                    story.append(Paragraph(step_label, self.styles['StepLabel']))
                    
                    if step.get('primary_screenshot') and step['primary_screenshot'] in screenshot_map:
                        img_path = screenshot_map[step['primary_screenshot']]
                        try:
                            img = Image(img_path)
                            img.drawWidth = 140*mm
                            img.drawHeight = 140*mm * (img.imageHeight / img.imageWidth)
                            story.append(Spacer(1, 2*mm))
                            story.append(img)
                            story.append(Spacer(1, 4*mm))
                        except Exception as e:
                            print(f"Warning: Failed to render image {img_path} in PDF: {e}")

                    story.append(Paragraph(f"<b>操作:</b> {action}", self.styles['CustomNormal']))
                    story.append(Spacer(1, 2*mm))
                    
                    if step.get('target_ui_element'):
                        target = step['target_ui_element']
                        story.append(Paragraph(f"<b>操作対象:</b> {target}", self.styles['CustomNormal']))
                    
                    if step.get('expected_result'):
                        result = step['expected_result']
                        story.append(Paragraph(f"<b>期待される結果:</b> {result}", self.styles['CustomNormal']))
                    
                    if step.get('check_point'):
                        checkpoint = step['check_point']
                        story.append(Paragraph(f"<b>✓ 確認:</b> {checkpoint}", self.styles['SectionLabel']))
                        story.append(Spacer(1, 2*mm))"""

content = content.replace("""                for step in procedure.get('steps', []):
                    order = step.get('order')
                    action = step.get('action', '')
                    step_label = f"ステップ {order}"
                    story.append(Paragraph(step_label, self.styles['StepLabel']))
                    story.append(Paragraph(action, self.styles['CustomNormal']))
                    story.append(Spacer(1, 2*mm))
                    
                    if step.get('expected_result'):
                        result = step['expected_result']
                        story.append(Paragraph(f"<b>期待される結果:</b> {result}", self.styles['CustomNormal']))""", replacement2)

with open('src/video_asset_manualize/pdf_manual_renderer.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched successfully")
