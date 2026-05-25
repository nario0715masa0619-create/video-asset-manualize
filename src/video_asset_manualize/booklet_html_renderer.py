'''
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
        return '\n'.join(html_parts)
    
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
            toc_html += f'<h3>Section {section["section"]}: {section["title"]}</h3>\n'
            for chapter in section['chapters']:
                toc_html += f'<div style="margin-left: 20px;">- {chapter["title"]}</div>\n'
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
