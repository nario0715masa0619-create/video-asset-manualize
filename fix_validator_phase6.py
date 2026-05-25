"""
Phase 6 source_evidence_validator 修正スクリプト
"""

from pathlib import Path

validator_file = Path("src/video_asset_manualize/source_evidence_validator.py")
content = validator_file.read_text(encoding='utf-8')

# validate_file メソッドを修正
old_pattern = '''    def validate_file(self, file_path: str):
        """JSON ファイルを検証"""
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")'''

new_pattern = '''    def validate_file(self, file_path):
        """JSON ファイルを検証"""
        file_path = str(file_path)
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")'''

content = content.replace(old_pattern, new_pattern)

validator_file.write_text(content, encoding='utf-8')
print("✓ Updated: src/video_asset_manualize/source_evidence_validator.py")
print("\n✅ source_evidence_validator.py が修正されました")
