"""
HTML Manual Renderer - Renders training_asset_spec to HTML.
"""

import json
from pathlib import Path
from datetime import datetime
from jinja2 import Template

from .settings import settings


class HTMLManualRenderer:
    """Renders training_asset_spec JSON to HTML manual."""
    
    DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{{ asset_meta.title }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: #eef2f5; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; font-size: 2.2em; }
        h2 { color: #2980b9; border-left: 5px solid #3498db; padding-left: 15px; margin-top: 40px; background: #f8fbfe; padding-top: 5px; padding-bottom: 5px;}
        h3 { color: #34495e; margin-top: 30px; font-size: 1.4em; border-bottom: 1px solid #eee; padding-bottom: 5px; }
        
        .step-card { display: flex; flex-direction: column; margin: 20px 0; border: 1px solid #e1e8ed; border-radius: 8px; overflow: hidden; background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .step-header { background: #3498db; color: white; padding: 10px 15px; font-weight: bold; font-size: 1.1em; }
        .step-body { display: flex; flex-direction: row; padding: 15px; gap: 20px; }
        .step-content { flex: 1; }
        .step-visual { flex: 1; max-width: 450px; }
        .step-visual img { width: 100%; border-radius: 4px; border: 1px solid #ddd; }
        
        .action-text { font-size: 1.15em; font-weight: bold; margin-bottom: 15px; color: #2c3e50; }
        .target-ui { display: inline-block; background: #e8f4f8; color: #0277bd; padding: 3px 8px; border-radius: 4px; font-size: 0.9em; margin-bottom: 10px; border: 1px solid #b3e5fc; }
        
        .checkpoint { background: #e8f5e9; border-left: 4px solid #4caf50; padding: 10px; margin: 10px 0; border-radius: 0 4px 4px 0; }
        .checkpoint::before { content: '✓ 確認: '; font-weight: bold; color: #2e7d32; }
        
        .caution { background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 10px 0; border-radius: 0 4px 4px 0; }
        .caution::before { content: '⚠️ 注意: '; font-weight: bold; color: #f57c00; }
        
        .metadata { font-size: 13px; color: #666; margin: 15px 0; background: #f9f9f9; padding: 15px; border-radius: 6px; }
        footer { margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #999; text-align: center; }
        
        @media (max-width: 768px) {
            .step-body { flex-direction: column; }
            .step-visual { max-width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ asset_meta.title }}</h1>
        <div class="metadata">
            <div><strong>目的:</strong> {{ asset_meta.purpose or 'N/A' }}</div>
            <div><strong>対象者:</strong> {{ asset_meta.target_audience | join(', ') or 'N/A' }}</div>
            <div><strong>ステータス:</strong> {{ asset_meta.status }}</div>
        </div>
        
        {% if asset_meta.prerequisites %}
        <h2>前提条件</h2>
        <ul>
        {% for pre in asset_meta.prerequisites %}
            <li>{{ pre }}</li>
        {% endfor %}
        </ul>
        {% endif %}
        
        {% if instructional_core.global_cautions %}
        <div class="caution">
            <ul>
            {% for caution in instructional_core.global_cautions %}
                <li>{{ caution }}</li>
            {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        {% for chapter in instructional_core.chapters %}
        <h2>{{ chapter.title }}</h2>
        {% for procedure in chapter.procedures %}
            <h3>{{ procedure.title }}</h3>
            {% for step in procedure.steps %}
            <div class="step-card">
                <div class="step-header">ステップ {{ step.order }}</div>
                <div class="step-body">
                    <div class="step-content">
                        <div class="action-text">{{ step.action }}</div>
                        
                        {% if step.target_ui_element %}
                        <div class="target-ui">操作対象: {{ step.target_ui_element }}</div>
                        {% endif %}
                        
                        {% if step.expected_result %}
                        <div><em>期待される結果: {{ step.expected_result }}</em></div>
                        {% endif %}
                        
                        {% if step.check_point %}
                        <div class="checkpoint">{{ step.check_point }}</div>
                        {% endif %}
                        
                        {% if step.cautions %}
                            {% for c in step.cautions %}
                            <div class="caution">{{ c }}</div>
                            {% endfor %}
                        {% endif %}
                    </div>
                    {% if step.primary_screenshot and screenshot_map.get(step.primary_screenshot) %}
                    <div class="step-visual">
                        <img src="{{ screenshot_map[step.primary_screenshot] }}" alt="Step Screenshot">
                    </div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        {% endfor %}
        {% endfor %}
        
        <footer>
            <p>Generated on {{ _metadata.generated_at }} (Schema v{{ _metadata.schema_version }})</p>
        </footer>
    </div>
</body>
</html>"""
    
    def __init__(self):
        self.template = Template(self.DEFAULT_TEMPLATE)
    
    def render(self, asset_spec: dict) -> str:
        import base64
        import mimetypes
        
        screenshot_map = {}
        source_evidence = asset_spec.get("source_evidence", {})
        candidates = source_evidence.get("screenshot_candidates", [])
        
        for cand in candidates:
            path = cand.get("image_path")
            if path and Path(path).exists():
                try:
                    with open(path, "rb") as img_f:
                        encoded = base64.b64encode(img_f.read()).decode('utf-8')
                        mime, _ = mimetypes.guess_type(path)
                        if not mime:
                            mime = "image/jpeg"
                        screenshot_map[cand["screenshot_id"]] = f"data:{mime};base64,{encoded}"
                except Exception as e:
                    print(f"Warning: Could not encode image {path}: {e}")
                    
        html = self.template.render(
            asset_meta=asset_spec.get("asset_meta", {}),
            instructional_core=asset_spec.get("instructional_core", {}),
            _metadata=asset_spec.get("_metadata", {}),
            screenshot_map=screenshot_map
        )
        return html
    
    def render_to_file(self, asset_spec: dict, output_file: Path) -> Path:
        html = self.render(asset_spec)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        return output_file
