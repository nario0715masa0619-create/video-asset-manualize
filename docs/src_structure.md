# src Structure

## 1. 目的

このドキュメントは、**VideoAsset Manualize** の MVP を実装するための、`src/` 配下の初期ディレクトリ構成案を定義するものです。

本プロジェクトでは、既存の研修動画・マニュアル動画を、**構造化 JSON・要約・HTML / PDF マニュアル**へ変換可能な教育資産として扱います。  
そのため `src/` の構成も、単なるスクリプト置き場ではなく、**動画入力 → 証跡抽出 → 分類 → 抽出 → 正規化 → 出力** の流れが分かる形にする必要があります。

---

## 2. 基本方針

`src/` の構成は、以下の方針に従います。

### 2.1 `training_asset_spec` を正本とする

最終的な正本データは `training_asset_spec` とし、HTML / PDF はそこから派生生成します。  
そのため、出力ロジックより先に、**正本 JSON を安定して作るための構成**を優先します。

### 2.2 要約と手順抽出を分離する

説明の要約と、実務で使う手順抽出は役割が異なるため、同じ責務にまとめません。  
構成上も、両者が別モジュールになるようにします。

### 2.3 証跡を独立して扱う

transcript、OCR、タイムスタンプなどは補助情報ではなく、レビューや再確認のための基盤です。  
そのため、証跡抽出は独立した責務として扱います。

### 2.4 MVP では過剰設計しない

将来拡張は意識しつつも、初期段階ではモジュールを細かく分けすぎません。  
まずは **1動画 → 1構造化JSON → 1要約 → 1HTML / PDF** を成立させるための最小構成に絞ります。

---

## 3. 初期ディレクトリ構成

MVP の初期構成案は以下の通りです。

```text
src/
└── video_asset_manualize/
    ├── __init__.py
    ├── main.py
    │
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py
    │   └── logging.py
    │
    ├── ingestion/
    │   ├── __init__.py
    │   └── video_loader.py
    │
    ├── evidence/
    │   ├── __init__.py
    │   ├── transcript_extractor.py
    │   ├── ocr_extractor.py
    │   └── evidence_link_builder.py
    │
    ├── classification/
    │   ├── __init__.py
    │   └── segment_classifier.py
    │
    ├── extraction/
    │   ├── __init__.py
    │   ├── instruction_extractor.py
    │   ├── summary_extractor.py
    │   └── caution_extractor.py
    │
    ├── normalization/
    │   ├── __init__.py
    │   ├── training_asset_spec_builder.py
    │   └── schema_validator.py
    │
    ├── repositories/
    │   ├── __init__.py
    │   └── training_asset_repository.py
    │
    ├── renderers/
    │   ├── __init__.py
    │   ├── html_manual_renderer.py
    │   └── pdf_manual_renderer.py
    │
    ├── pipeline/
    │   ├── __init__.py
    │   └── build_training_asset_pipeline.py
    │
    ├── cli/
    │   ├── __init__.py
    │   ├── build_asset.py
    │   └── validate_asset.py
    │
    └── utils/
        ├── __init__.py
        ├── file_utils.py
        ├── json_utils.py
        └── id_utils.py
```

---

## 4. 各ディレクトリの役割

### 4.1 `config/`

設定値を管理するためのディレクトリです。

#### 主な役割

- 環境変数の読み込み
- 入出力先の設定
- ログ設定

#### 想定ファイル

- `settings.py`
- `logging.py`

---

### 4.2 `ingestion/`

入力動画を受け付けるためのディレクトリです。

#### 主な役割

- 動画ファイルの読み込み
- 実行対象の解決
- 入力元の違いの吸収

#### 想定ファイル

- `video_loader.py`

---

### 4.3 `evidence/`

動画から証跡を抽出するためのディレクトリです。

#### 主な役割

- transcript 抽出
- OCR 抽出
- transcript / OCR / 手順の対応づけ
- タイムスタンプ保持

#### 想定ファイル

- `transcript_extractor.py`
- `ocr_extractor.py`
- `evidence_link_builder.py`

#### 補足

MVP 段階ではスクリーンショット候補や話者分離を必須にしません。  
必要になった時点で拡張します。

---

### 4.4 `classification/`

動画内容を分類するためのディレクトリです。

#### 主な役割

- explanation
- operation
- caution

などの最低限の分類を行うことです。

#### 想定ファイル

- `segment_classifier.py`

#### 補足

MVP ではまず、  
**説明 / 操作 / 注意点**  
の最低限分類ができれば十分です。

---

### 4.5 `extraction/`

分類済み情報から、実際に使う構造を抽出するためのディレクトリです。

#### 主な役割

- 手順抽出
- 要約抽出
- 注意点抽出

#### 想定ファイル

- `instruction_extractor.py`
- `summary_extractor.py`
- `caution_extractor.py`

#### 重要な方針

- `summary_extractor.py` は説明系を扱う
- `instruction_extractor.py` は操作系を扱う

この分離を明確に保つことが重要です。

---

### 4.6 `normalization/`

抽出結果を `training_asset_spec` に正規化するためのディレクトリです。

#### 主な役割

- JSON 構造への統合
- 必須項目の整形
- スキーマ検証

#### 想定ファイル

- `training_asset_spec_builder.py`
- `schema_validator.py`

#### 補足

この層が、抽出結果と最終 JSON 仕様の間をつなぐ責務を持ちます。

---

### 4.7 `repositories/`

ファイル保存・読み込みを担当するディレクトリです。

#### 主な役割

- `training_asset_spec` JSON の保存
- 将来の読み込み・再利用の入口

#### 想定ファイル

- `training_asset_repository.py`

#### 補足

MVP ではローカルファイル保存だけで十分です。

---

### 4.8 `renderers/`

正本 JSON から成果物を生成するためのディレクトリです。

#### 主な役割

- HTML マニュアル生成
- PDF マニュアル生成

#### 想定ファイル

- `html_manual_renderer.py`
- `pdf_manual_renderer.py`

#### 方針

レンダラーは、抽出ロジックに直接依存せず、  
**正規化済みの `training_asset_spec` を受け取って出力する**形にします。

---

### 4.9 `pipeline/`

処理全体をつなぐためのディレクトリです。

#### 主な役割

- 動画入力から JSON 出力までの接続
- 実行順序の定義

#### 想定ファイル

- `build_training_asset_pipeline.py`

#### 補足

MVP では、まず単一のパイプラインだけあれば十分です。

---

### 4.10 `cli/`

コマンドライン実行の入口です。

#### 主な役割

- 変換処理の実行
- JSON 検証の実行

#### 想定ファイル

- `build_asset.py`
- `validate_asset.py`

#### 補足

初期段階では GUI よりも CLI の方が実装と検証がしやすいため、まずはこちらを優先します。

---

### 4.11 `utils/`

共通ユーティリティを置くディレクトリです。

#### 主な役割

- ファイル操作
- JSON 操作
- ID 補助処理

#### 想定ファイル

- `file_utils.py`
- `json_utils.py`
- `id_utils.py`

#### 注意点

`utils/` に何でも集めすぎると責務が崩れるため、  
**ドメイン判断を含まない補助処理だけ**に限定します。

---

## 5. MVP で最低限必要なファイル

初期実装では、次のファイルが揃えば MVP 開始に十分です。

```text
src/video_asset_manualize/
├── main.py
├── config/settings.py
├── ingestion/video_loader.py
├── evidence/transcript_extractor.py
├── evidence/ocr_extractor.py
├── evidence/evidence_link_builder.py
├── classification/segment_classifier.py
├── extraction/instruction_extractor.py
├── extraction/summary_extractor.py
├── extraction/caution_extractor.py
├── normalization/training_asset_spec_builder.py
├── normalization/schema_validator.py
├── repositories/training_asset_repository.py
├── renderers/html_manual_renderer.py
├── renderers/pdf_manual_renderer.py
├── pipeline/build_training_asset_pipeline.py
├── cli/build_asset.py
└── cli/validate_asset.py
```

---

## 6. 推奨する依存方向

モジュール間の依存関係は、できるだけ一方向に保ちます。

```text
ingestion
  ↓
evidence
  ↓
classification
  ↓
extraction
  ↓
normalization
  ↓
repositories / renderers
  ↓
pipeline / cli
```

### 原則

- `renderers` は `extraction` に直接依存しない
- `extraction` は HTML / PDF の知識を持たない
- `classification` は出力形式を知らない
- `normalization` が JSON 構造の最終責任を持つ

---

## 7. 命名規則

ファイル名は、責務が見て分かることを優先します。

### 推奨パターン

- `*_extractor.py`  
  何かを抽出する処理

- `*_builder.py`  
  複数情報をまとめて構造化する処理

- `*_renderer.py`  
  表示用成果物を生成する処理

- `*_repository.py`  
  保存・読み込みを担当する処理

- `*_validator.py`  
  妥当性確認を行う処理

### 例

- `instruction_extractor.py`
- `training_asset_spec_builder.py`
- `html_manual_renderer.py`
- `training_asset_repository.py`
- `schema_validator.py`

---

## 8. この構成で守りたいこと

初期構成では、特に以下を崩さないことを重視します。

### 8.1 正本は JSON

あらゆる成果物は `training_asset_spec` から派生生成することを原則とします。

### 8.2 要約と手順を混ぜない

説明の整理と操作の保持は分離し、構造としても別モジュールに保ちます。

### 8.3 証跡を後回しにしない

transcript と時刻情報の保持は MVP の段階から扱います。

### 8.4 出力より先に構造を固める

見た目の作り込みより、JSON と手順品質の安定を優先します。

---

## 9. 将来の拡張余地

MVP 後には、以下の拡張が考えられます。

- FAQ 候補抽出の強化
- チェックリスト生成の強化
- スクリーンショット候補管理
- 複数動画統合
- レビュー補助機能
- ブランド別テンプレート
- API / 管理画面対応

その場合でも、初期構成の責務分離を保ったまま拡張できるようにしておくことが重要です。

---

## 10. まとめ

VideoAsset Manualize の `src/` は、  
**動画を再利用可能な教育資産へ変換する処理責務を明確に分けた構成**として設計します。

MVP では、過剰な分割や過剰な将来設計を避け、まずは以下を安定して成立させることを優先します。

**1動画 → 1構造化JSON → 1要約 → 1HTML / PDF**

そのための最小構成として、本ドキュメントのディレクトリ案を採用します。
