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
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1 { color: #000; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        h2 { color: #007bff; border-left: 4px solid #007bff; padding-left: 10px; margin-top: 30px; }
        h3 { color: #333; margin-top: 20px; }
        .step { margin: 15px 0; padding: 10px; background: #f0f8ff; border-left: 3px solid #007bff; }
        .caution { background: #fff3cd; border: 1px solid #ffc107; padding: 10px; margin: 10px 0; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        .metadata { font-size: 12px; color: #666; margin: 10px 0; }
        footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc; font-size: 11px; color: #999; }
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
            <strong>⚠️ 注意事項</strong>
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
            <div class="step">
                <strong>ステップ {{ step.order }}:</strong> {{ step.action }}
                {% if step.expected_result %}<div><em>期待: {{ step.expected_result }}</em></div>{% endif %}
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
        html = self.template.render(
            asset_meta=asset_spec.get("asset_meta", {}),
            instructional_core=asset_spec.get("instructional_core", {}),
            _metadata=asset_spec.get("_metadata", {}),
        )
        return html
    
    def render_to_file(self, asset_spec: dict, output_file: Path) -> Path:
        html = self.render(asset_spec)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        return output_file
