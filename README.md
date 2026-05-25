# VideoAsset Manualize

動画→JSON→HTML/PDF マニュアル自動生成パイプライン

## 機能

- 動画ファイルから source_evidence を自動生成
- ffprobe で動画メタデータを取得
- Whisper で文字起こしを自動生成
- EasyOCR で OCR を自動生成
- source_evidence から training_asset_spec を自動抽出
- training_asset_spec から HTML/PDF マニュアルを自動生成
- CLI インターフェース (video / extract / build / validate)
- 複数の Provider に対応（Transcript、OCR）

## Phase ロードマップ

Phase 1: training_asset_spec の検証、HTML/PDF 生成
Phase 2: source_evidence の検証、自動抽出
Phase 3: 動画入力インターフェース、抽象 Provider
Phase 4: ffprobe メタデータ、Whisper STT、Provider Factory
Phase 5: EasyOCR 統合、フレーム抽出、OCR provider 切替 ✅

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

### EasyOCR インストール (オプション)

pip install easyocr

EasyOCR 初回実行時にモデルをダウンロードします。
初回は時間がかかる場合があります。

## 使用方法

### 1. 動画 → source_evidence 生成

ダミー provider で実行:
python -m video_asset_manualize.build_asset video input.mp4

Whisper + EasyOCR で実行:
python -m video_asset_manualize.build_asset video input.mp4 --provider whisper --ocr-provider easyocr

### 2. source_evidence → training_asset_spec 抽出

python -m video_asset_manualize.build_asset extract output/exports/extracted_source_evidence.json

### 3. training_asset_spec → HTML/PDF 生成

python -m video_asset_manualize.build_asset build output/exports/asset-{id}_spec.json

### スキーマ検証

python -m video_asset_manualize.build_asset validate input.json

## CLI コマンド一覧

video: 動画 → source_evidence 抽出
  --provider: Transcript provider (dummy, whisper)
  --ocr-provider: OCR provider (dummy, easyocr)
  --whisper-model: Whisper model (tiny, base, small, etc.)
  --ocr-gpu: EasyOCR GPU 使用

extract: source_evidence → training_asset_spec 抽出

build: training_asset_spec → HTML/PDF 生成

validate: JSON スキーマ検証

## ファイル構成

src/video_asset_manualize/
  ├── build_asset.py (CLI メイン)
  ├── build_training_asset_pipeline.py (パイプライン)
  ├── ffprobe_metadata_extractor.py (メタデータ取得)
  ├── whisper_transcript_provider.py (Whisper STT)
  ├── frame_extractor.py (フレーム抽出)
  ├── easyocr_provider.py (EasyOCR 実装)
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

Whisper が見つかない:
→ pip install openai-whisper を実行

EasyOCR が見つからない:
→ pip install easyocr を実行

EasyOCR が遅い:
→ --ocr-gpu を使用して GPU 加速

動画ファイルが無効:
→ 有効な MP4/MKV/AVI ファイルを確認

## 設定ファイル

settings.py で Provider を設定できます:

TRANSCRIPT_PROVIDER_TYPE = "dummy" または "whisper"
WHISPER_MODEL = "base"
WHISPER_LANGUAGE = "ja"

OCR_PROVIDER_TYPE = "dummy" または "easyocr"
EASYOCR_LANGUAGES = ["ja", "en"]
EASYOCR_GPU = False

CLI オプションで上書き可能

## 次フェーズ予定

Phase 6 (LLM 処理):
- 自動要約生成
- 手順自動抽出
- FAQ 候補自動生成

Phase 7 (複数動画):
- マルチビデオ冊子化
- 統合 PDF 生成

## リポジトリ

https://github.com/nario0715masa0619-create/video-asset-manualize
