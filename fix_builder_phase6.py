"""
Phase 6 llm_training_asset_builder 修正スクリプト
"""

from pathlib import Path

builder_file = Path("src/video_asset_manualize/llm_training_asset_builder.py")
content = builder_file.read_text(encoding='utf-8')

# generate メソッド呼び出しを修正
replacements = [
    ('self.summary_generator.generate(transcript_text)', 'self.summary_generator.generate_summary(transcript_text)'),
    ('self.instruction_extractor.extract(transcript_text)', 'self.instruction_extractor.extract_instructions(transcript_text)'),
    ('self.caution_generator.generate(transcript_text)', 'self.caution_generator.generate_cautions(transcript_text)'),
    ('self.faq_generator.generate(transcript_text, instructional_core)', 'self.faq_generator.generate_faqs(transcript_text, instructional_core)'),
]

for old, new in replacements:
    content = content.replace(old, new)

builder_file.write_text(content, encoding='utf-8')
print("✓ Updated: src/video_asset_manualize/llm_training_asset_builder.py")
print("\n✅ llm_training_asset_builder.py が修正されました")
