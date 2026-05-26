# VideoAsset Manualize

**動画を再利用可能な教育資産に変換する、エンドツーエンドの自動マニュアル生成プラットフォーム**

## 概要

VideoAsset Manualize は、既存の研修動画やマニュアル動画を、高品質な教育資産（トレーニング資産）として再利用するためのオープンソース・プラットフォームです。

### 出力物

- **source_evidence.json** – 動画から抽出した字幕・OCR・タイムスタンプ
- **training_asset_spec.json** – 標準的な教育資産仕様（canonical source）
- **HTML マニュアル** – ブラウザで閲覧可能なマニュアル
- **PDF マニュアル** – 印刷可能な高品質マニュアル
- **冊子（booklet）** – 複数の動画資産を 1 つの統合マニュアルに

---

## 実装済み機能（Phase 1～9）

| Phase | 内容 | 状態 |
|-------|------|------|
| Phase 1 | training_asset_spec スキーマ、HTML/PDF レンダリング | ✅ |
| Phase 2 | video → source_evidence 抽出（ffprobe, Whisper, EasyOCR） | ✅ |
| Phase 3 | source_evidence → training_asset_spec 変換 | ✅ |
| Phase 4 | CLI インターフェース（validate, video, extract, build） | ✅ |
| Phase 5 | Provider ファクトリー、動的設定管理 | ✅ |
| Phase 6 | LLM ベース FAQ・Caution 自動生成 | ✅ |
| Phase 7 | PDF マニュアル生成 | ✅ |
| Phase 8 | Web UI ダッシュボード（Streamlit） | ✅ |
| Phase 9 | UI から CLI パイプライン直接実行 | ✅ |

---

## 必要環境

- Python 3.11+
- pip
- ffmpeg / ffprobe
- Streamlit 1.28.0+ (Web UI 使用時)

---

## インストール

\\ash
git clone https://github.com/nario0715masa0619-create/video-asset-manualize.git
cd video-asset-manualize
pip install -r requirements.txt
pip install -e .
\
---

## Web UI での処理（Phase 9）

### 起動

\\ash
streamlit run streamlit_app.py
\
ブラウザで **http://localhost:8501** にアクセス

### 画面説明

**Dashboard**
- 統計情報（アセット数、承認済み数、冊子数、承認率）
- 最近のアセット・冊子表示

**Single Video**
- 動画ファイルパス入力
- Transcript Provider 選択（dummy / whisper）
- OCR Provider 選択（dummy / easyocr）
- Process Video ボタン

**Assets**
- 生成済みアセット一覧
- Review State 更新（draft → in_review → approved → rejected）
- コメント入力・保存

**Batch & Booklet**
- Manifest JSON 指定
- バッチビルド・冊子化実行

---

## CLI での処理

### 1. 動画から source_evidence 生成

\\ash
python -m video_asset_manualize.build_asset video samples/sample_training_video.mp4
\
### 2. training_asset_spec 生成

\\ash
python -m video_asset_manualize.build_asset extract output/exports/extracted_source_evidence.json
\
### 3. HTML/PDF 生成

\\ash
python -m video_asset_manualize.build_asset build output/exports/asset-{id}_spec.json
\
---

## トラブルシューティング

**ffprobe が見つからない:**
- Windows: choco install ffmpeg
- macOS: brew install ffmpeg
- Linux: apt-get install ffmpeg

**Streamlit が起動しない:**
- pip install streamlit>=1.28.0

---

**Last Updated**: 2026-05-26 (Phase 9 完成)
