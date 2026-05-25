# README.md を更新

from pathlib import Path

readme_file = Path("README.md")

new_readme = """# VideoAsset Manualize

動画→JSON→HTML/PDF マニュアル自動生成パイプライン

## 機能

- 動画ファイルから source_evidence を自動生成
- source_evidence から training_asset_spec を自動抽出
- training_asset_spec から HTML/PDF マニュアルを自動生成
- CLI インターフェース (video / extract / build / validate)
- 複数の Transcript Provider に対応

## Phase ロードマップ

Phase 1: training_asset_spec の検証、HTML/PDF 生成
Phase 2: source_evidence の検証、自動抽出
Phase 3: 動画入力インターフェース、抽象 Provider
Phase 4: ffprobe メタデータ、Whisper STT、Provider Factory

## セットアップ

### 必須環境
- Python 3.11+
- pip

### 基本インストール

git clone https://github.com/nario0715masa0619-create/video-asset-manualize.git
cd video-asset-manualize
pip install -r requirements.txt
pip install -e .

### ffprobe インストール

ffprobe は ffmpeg に含まれています。

Windows:
choco install ffmpeg
または https://ffmpeg.org/download.html からダウンロード

macOS:
brew install ffmpeg

Linux:
apt-get install ffmpeg

### Whisper インストール (オプション)

pip install openai-whisper

## 使用方法

### 1. 動画 → source_evidence 生成

ダミー provider で実行:
python -m video_asset_manualize.build_asset video input.mp4

Whisper で実行:
python -m video_asset_manualize.build_asset video input.mp4 --provider whisper --whisper-model base

### 2. source_evidence → training_asset_spec 抽出

python -m video_asset_manualize.build_asset extract output/exports/extracted_source_evidence.json

### 3. training_asset_spec → HTML/PDF 生成

python -m video_asset_manualize.build_asset build output/exports/asset-{id}_spec.json

### スキーマ検証

python -m video_asset_manualize.build_asset validate input.json

## CLI コマンド一覧

video: 動画 → source_evidence 抽出
extract: source_evidence → training_asset_spec 抽出
build: training_asset_spec → HTML/PDF 生成
validate: JSON スキーマ検証

## ファイル構成

src/video_asset_manualize/
  ├── build_asset.py (CLI メイン)
  ├── build_training_asset_pipeline.py (パイプライン)
  ├── ffprobe_metadata_extractor.py (メタデータ取得)
  ├── whisper_transcript_provider.py (Whisper STT)
  ├── provider_factory.py (Provider 生成)
  ├── transcript_provider.py (Transcript 抽象)
  ├── ocr_provider.py (OCR 抽象)
  ├── video_source_evidence_builder.py (動画ビルダー)
  ├── source_evidence_validator.py (Validator)
  ├── training_asset_spec_builder.py
  ├── schema_validator.py
  ├── html_manual_renderer.py
  ├── pdf_manual_renderer.py
  ├── settings.py
  └── __init__.py

schemas/
  ├── training_asset_spec.schema.json
  └── source_evidence.schema.json

samples/
  ├── sample_training_video.mp4
  ├── sample_training_asset_spec.json
  └── sample_source_evidence.json

## トラブルシューティング

ffprobe が見つからない:
→ ffmpeg をインストール

Whisper が見つからない:
→ pip install openai-whisper を実行

動画ファイルが無効:
→ 有効な動画ファイルを確認

## 次フェーズ予定

Phase 5: OCR 統合 (EasyOCR など)
Phase 6: AI 処理 (LLM による要約・抽出)

## リポジトリ

https://github.com/nario0715masa0619-create/video-asset-manualize
"""

with open(readme_file, "w", encoding="utf-8") as f:
    f.write(new_readme)

print("✓ README.md を更新しました")
