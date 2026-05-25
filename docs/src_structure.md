# src ディレクトリ構成案

このドキュメントは、**VideoAsset Manualize** における `src/` 配下の初期ディレクトリ構成案を定義するものです。

本プロジェクトでは、既存の研修動画・マニュアル動画を、**構造化 JSON・要約・HTML マニュアル・PDF マニュアル・FAQ 候補・チェックリスト候補**へ展開可能な教育資産・業務資産として扱います。  
そのため、`src/` の構成も単なるスクリプト置き場ではなく、**動画 → 証跡抽出 → 分類 → 構造化 → 正本 JSON 化 → 各種出力生成** の流れを明確に反映する必要があります。

---

## 1. このドキュメントの目的

`src/` 配下の構成は、以下を満たすことを目的とします。

- `training_asset_spec` を正本とする設計思想に整合する
- 要約と手順抽出を分離する
- 証跡と成果物を分離しつつ、相互参照可能にする
- HTML / PDF / テキスト等の出力責務を明確に分ける
- MVP の最小実装から将来拡張まで無理なく育てられる
- README / architecture / json_schema / mvp_scope / prompt_design / manual_template_spec と整合する

---

## 2. 設計方針

`src/` の構成設計では、以下の方針を採用します。

### 2.1 正本データ先行

本プロジェクトでは、動画を直接 PDF やマニュアルに変換するのではなく、  
一度 **`training_asset_spec`** に正規化した上で、そこから各種出力を派生生成します。

そのため、`src/` でも以下の責務分離を前提にします。

- 入力受付
- 証跡抽出
- セグメント分類
- 手順抽出
- 要約抽出
- 正規化 / スキーマ整合
- HTML / PDF レンダリング
- レビュー補助

### 2.2 要約と手順抽出を分ける

本プロジェクトで最重要なのは、**説明部分の要約**と**操作手順の抽出**を分けることです。

したがって `src/` でも、

- 要約系ロジック
- 手順抽出系ロジック
- 注意点抽出系ロジック
- FAQ / チェックリスト派生ロジック

を別責務として配置します。

### 2.3 証跡を独立して保持する

動画の内容を後から検証できるようにするため、

- transcript
- OCR
- screenshot candidate
- speaker segment
- evidence link

などの証跡系処理は独立層として扱います。

### 2.4 MVP では過剰分割しすぎない

将来拡張を見据えつつも、最初から細かく分けすぎると実装負荷が上がるため、  
MVP 段階では**責務の境界が明確な最小構成**から開始します。

---

## 3. `src/` 全体構成案

以下を、初期の標準構成案とします。

```text
src/
└── video_asset_manualize/
    ├── __init__.py
    ├── main.py
    │
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── logging.py
    │   └── constants.py
    │
    ├── domain/
    │   ├── __init__.py
    │   ├── asset_meta.py
    │   ├── source_evidence.py
    │   ├── instructional_core.py
    │   ├── derived_views.py
    │   ├── delivery_assets.py
    │   ├── metadata.py
    │   ├── enums.py
    │   └── ids.py
    │
    ├── ingestion/
    │   ├── __init__.py
    │   ├── video_loader.py
    │   ├── input_manifest_loader.py
    │   └── source_video_resolver.py
    │
    ├── evidence/
    │   ├── __init__.py
    │   ├── transcript_extractor.py
    │   ├── ocr_extractor.py
    │   ├── screenshot_candidate_extractor.py
    │   ├── speaker_segment_extractor.py
    │   └── evidence_link_builder.py
    │
    ├── classification/
    │   ├── __init__.py
    │   ├── segment_classifier.py
    │   ├── classification_rules.py
    │   └── classification_postprocessor.py
    │
    ├── extraction/
    │   ├── __init__.py
    │   ├── instruction_extractor.py
    │   ├── summary_extractor.py
    │   ├── caution_extractor.py
    │   ├── common_mistake_extractor.py
    │   ├── checklist_extractor.py
    │   └── faq_candidate_extractor.py
    │
    ├── normalization/
    │   ├── __init__.py
    │   ├── training_asset_spec_builder.py
    │   ├── schema_validator.py
    │   ├── defaults_applier.py
    │   └── integrity_checker.py
    │
    ├── repositories/
    │   ├── __init__.py
    │   ├── training_asset_repository.py
    │   ├── source_video_repository.py
    │   └── export_repository.py
    │
    ├── renderers/
    │   ├── __init__.py
    │   ├── html_manual_renderer.py
    │   ├── pdf_manual_renderer.py
    │   ├── text_asset_renderer.py
    │   └── section_renderers/
    │       ├── __init__.py
    │       ├── cover_renderer.py
    │       ├── toc_renderer.py
    │       ├── summary_renderer.py
    │       ├── chapter_renderer.py
    │       ├── checklist_renderer.py
    │       ├── faq_renderer.py
    │       └── revision_renderer.py
    │
    ├── templates/
    │   └── manual/
    │       ├── base.html
    │       ├── manual.html
    │       ├── partials/
    │       │   ├── cover.html
    │       │   ├── toc.html
    │       │   ├── asset_meta.html
    │       │   ├── summary.html
    │       │   ├── chapter.html
    │       │   ├── checklist.html
    │       │   ├── faq.html
    │       │   └── revision.html
    │       └── styles/
    │           ├── base.css
    │           ├── screen.css
    │           └── print.css
    │
    ├── pipeline/
    │   ├── __init__.py
    │   ├── build_training_asset_pipeline.py
    │   ├── render_manual_pipeline.py
    │   └── jobs.py
    │
    ├── review/
    │   ├── __init__.py
    │   ├── review_summary_builder.py
    │   ├── missing_step_detector.py
    │   ├── caution_gap_detector.py
    │   └── evidence_trace_reporter.py
    │
    ├── prompts/
    │   ├── __init__.py
    │   ├── segment_classification_prompts.py
    │   ├── instruction_extraction_prompts.py
    │   ├── summary_extraction_prompts.py
    │   ├── caution_extraction_prompts.py
    │   └── faq_extraction_prompts.py
    │
    ├── cli/
    │   ├── __init__.py
    │   ├── build_asset.py
    │   ├── render_manual.py
    │   └── validate_asset.py
    │
    └── utils/
        ├── __init__.py
        ├── time_utils.py
        ├── text_utils.py
        ├── file_utils.py
        ├── json_utils.py
        └── id_utils.py
```

---

## 4. ディレクトリごとの役割

### 4.1 `config/`

設定値や環境依存情報を扱う層です。

#### 想定ファイル

- `settings.py`  
  環境変数、パス設定、出力先設定、モデル切替設定などを扱う

- `logging.py`  
  ログフォーマット、ロガー初期化、ログレベル設定

- `constants.py`  
  分類ラベル、ステータス文字列、既定値などを定義

#### 目的

- ハードコードの分散を防ぐ
- 設定変更を局所化する
- 実装コードから環境依存を切り離す

---

### 4.2 `domain/`

プロジェクトの中心となるデータ概念を表現する層です。

#### 想定内容

- `asset_meta.py`
- `source_evidence.py`
- `instructional_core.py`
- `derived_views.py`
- `delivery_assets.py`
- `metadata.py`

#### 目的

- `training_asset_spec` をコード上でも自然に扱えるようにする
- JSON スキーマに対応する内部表現を整理する
- 各モジュール間のデータ受け渡しを明確化する

#### 補足

初期段階では dataclass や TypedDict 相当の軽量構造でもよく、  
MVP では「厳密なドメインモデリング」よりも**責務の見える化**を優先します。

---

### 4.3 `ingestion/`

入力動画や入力マニフェストを受け付ける層です。

#### 想定ファイル

- `video_loader.py`  
  ローカル動画ファイル、保存済みソースなどを読み込む

- `input_manifest_loader.py`  
  バッチ処理用の対象一覧、動画メタ一覧などを読み込む

- `source_video_resolver.py`  
  入力から実動画への解決処理を行う

#### 目的

- 入力元の違いを吸収する
- パイプライン本体が入力形式に依存しないようにする

---

### 4.4 `evidence/`

証跡抽出を担う層です。  
本プロジェクトの重要要素である **元動画との追跡可能性** を支える中核層です。

#### 想定ファイル

- `transcript_extractor.py`  
  文字起こしを抽出する

- `ocr_extractor.py`  
  画面内文字列を抽出する

- `screenshot_candidate_extractor.py`  
  スクリーンショット候補を抽出する

- `speaker_segment_extractor.py`  
  話者セグメントを扱う

- `evidence_link_builder.py`  
  手順や注意点と transcript / OCR / screenshot を結びつける

#### 目的

- 後段の分類・抽出処理に必要な生証跡を揃える
- 最終成果物に対する根拠追跡を可能にする

---

### 4.5 `classification/`

動画内セグメントを、説明・背景・実操作・注意点などに分類する層です。

#### 想定ファイル

- `segment_classifier.py`  
  セグメント分類の中心処理

- `classification_rules.py`  
  ルールベース補助や補正条件

- `classification_postprocessor.py`  
  分類結果の整形、前後文脈を考慮した補正

#### 目的

- `prompt_design.md` で定義した分類方針をコードに反映する
- 要約対象と保持対象を切り分ける前処理を担う

#### 重要な前提

ここでの分類品質が、その後の

- 手順抽出
- 要約抽出
- 注意点抽出
- FAQ 候補生成

の品質を大きく左右します。

---

### 4.6 `extraction/`

分類済みセグメントから、教育資産として必要な構造を抽出する層です。

#### 想定ファイル

- `instruction_extractor.py`  
  章・手順・ステップを抽出する

- `summary_extractor.py`  
  説明・背景・補足から要約を生成する

- `caution_extractor.py`  
  注意点・禁止事項・事故防止情報を抽出する

- `common_mistake_extractor.py`  
  よくあるミスを抽出する

- `checklist_extractor.py`  
  チェックリスト候補を抽出する

- `faq_candidate_extractor.py`  
  FAQ 候補を生成する

#### 目的

- 「説明」「操作」「注意点」を混ぜずに処理する
- `instructional_core` と `derived_views` の元データを作る

#### 重要な前提

`summary_extractor.py` と `instruction_extractor.py` は分離し、  
**同じ入力から違う粒度・違う目的の情報を作る**構成にします。

---

### 4.7 `normalization/`

抽出結果を `training_asset_spec` に正規化する層です。

#### 想定ファイル

- `training_asset_spec_builder.py`  
  各抽出結果をまとめて正本 JSON 相当の構造へ組み立てる

- `schema_validator.py`  
  JSON Schema への適合性を確認する

- `defaults_applier.py`  
  デフォルト値の補完や省略値の整形を行う

- `integrity_checker.py`  
  参照切れ、ID 重複、空章、順序不整合などを確認する

#### 目的

- 抽出ロジックと最終 JSON 仕様を分離する
- 後段のレンダリング処理を安定させる
- `schemas/training_asset_spec.schema.json` との整合性を担保する

---

### 4.8 `repositories/`

データ入出力を扱う層です。

#### 想定ファイル

- `training_asset_repository.py`  
  `training_asset_spec` JSON の保存・読込

- `source_video_repository.py`  
  ソース動画の参照や管理

- `export_repository.py`  
  HTML / PDF / テキスト等の生成物管理

#### 目的

- ファイル I/O をビジネスロジックから分離する
- 今後、ローカル保存から別保存先へ切り替える余地を残す

---

### 4.9 `renderers/`

正本 JSON から表示用成果物を生成する層です。

#### 想定ファイル

- `html_manual_renderer.py`  
  HTML マニュアルを生成する

- `pdf_manual_renderer.py`  
  HTML またはレンダリング済み内容を基に PDF を生成する

- `text_asset_renderer.py`  
  テキスト成果物や要約テキストを整形出力する

- `section_renderers/`  
  各セクション単位の描画責務を分離する

#### 目的

- `manual_template_spec.md` の仕様を実装に落とす
- JSON と表示を直結させず、中間責務として描画層を置く
- HTML / PDF の責務分離を維持する

---

### 4.10 `templates/`

HTML テンプレートや CSS を置く層です。

#### 想定内容

- `base.html`
- `manual.html`
- `partials/`
- `styles/`

#### 目的

- レンダラー本体から見た目を分離する
- PDF と HTML の両立を見据えたテンプレート構成を取る
- `manual_template_spec.md` との対応関係を保つ

#### 補足

MVP 段階では装飾よりも、

- 読めること
- セクションが壊れないこと
- 改ページが破綻しないこと

を優先します。

---

### 4.11 `pipeline/`

処理フロー全体を接続する層です。

#### 想定ファイル

- `build_training_asset_pipeline.py`  
  動画から `training_asset_spec` を作る流れを束ねる

- `render_manual_pipeline.py`  
  JSON から HTML / PDF を生成する流れを束ねる

- `jobs.py`  
  ジョブ単位・実行単位の制御を行う

#### 目的

- 個別機能をつなぐ実行順序を明示する
- CLI や将来の UI / API から使いやすい入口を用意する

---

### 4.12 `review/`

MVP で重要となる、人手レビュー補助のための層です。

#### 想定ファイル

- `review_summary_builder.py`  
  レビュー観点をまとめる

- `missing_step_detector.py`  
  手順抜けの疑いを検知する

- `caution_gap_detector.py`  
  注意点不足の疑いを検知する

- `evidence_trace_reporter.py`  
  証跡リンクの確認レポートを出す

#### 目的

- 完全自動化前提ではなく、レビュー前提のプロセスを支える
- MVP の受け入れ基準に直結する確認観点をコード化する

---

### 4.13 `prompts/`

抽出・分類に使うプロンプト定義を集約する層です。

#### 想定ファイル

- `segment_classification_prompts.py`
- `instruction_extraction_prompts.py`
- `summary_extraction_prompts.py`
- `caution_extraction_prompts.py`
- `faq_extraction_prompts.py`

#### 目的

- `prompt_design.md` と実装の対応を明確にする
- 抽出品質調整をコード変更と切り分ける
- 将来的なプロンプト改善履歴を管理しやすくする

---

### 4.14 `cli/`

コマンドライン実行の入口です。

#### 想定ファイル

- `build_asset.py`
- `render_manual.py`
- `validate_asset.py`

#### 目的

- MVP では GUI より先に CLI で動作確認しやすくする
- 単発実行・検証・再生成をやりやすくする

---

### 4.15 `utils/`

共通ユーティリティをまとめる層です。

#### 想定ファイル

- `time_utils.py`
- `text_utils.py`
- `file_utils.py`
- `json_utils.py`
- `id_utils.py`

#### 目的

- 小さな共通処理を集約する
- ドメインロジックに混入しがちな補助処理を分離する

#### 注意点

`utils/` は便利ですが、何でも入れると責務が崩れるため、  
**ドメイン判断を含まない汎用処理のみ**を置きます。

---

## 5. MVP で最低限必要な構成

初期段階ですべてを実装する必要はありません。  
MVP では、以下の最小構成から始めるのが現実的です。

```text
src/
└── video_asset_manualize/
    ├── __init__.py
    ├── main.py
    ├── config/
    │   ├── settings.py
    │   └── logging.py
    ├── ingestion/
    │   └── video_loader.py
    ├── evidence/
    │   ├── transcript_extractor.py
    │   ├── ocr_extractor.py
    │   └── evidence_link_builder.py
    ├── classification/
    │   └── segment_classifier.py
    ├── extraction/
    │   ├── instruction_extractor.py
    │   ├── summary_extractor.py
    │   └── caution_extractor.py
    ├── normalization/
    │   ├── training_asset_spec_builder.py
    │   └── schema_validator.py
    ├── repositories/
    │   └── training_asset_repository.py
    ├── renderers/
    │   ├── html_manual_renderer.py
    │   └── pdf_manual_renderer.py
    ├── pipeline/
    │   └── build_training_asset_pipeline.py
    ├── cli/
    │   ├── build_asset.py
    │   └── validate_asset.py
    └── utils/
        ├── file_utils.py
        ├── json_utils.py
        └── id_utils.py
```

この最小構成で、まず以下を成立させることを目標にします。

- 1 本の動画を入力する
- transcript / OCR を取得する
- セグメント分類する
- 手順と要約を別処理で抽出する
- `training_asset_spec` を生成する
- HTML / PDF を出力する

---

## 6. 推奨する依存方向

依存関係は、できるだけ一方向に保ちます。

推奨する概念上の流れは以下です。

```text
config / utils
        ↓
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
 repositories
        ↓
   renderers
        ↓
    pipeline / cli
```

### 原則

- `renderers` は `extraction` に直接依存しない  
  必ず正規化済みの `training_asset_spec` を受け取る

- `extraction` は PDF や HTML の知識を持たない

- `classification` は出力レイアウトを意識しない

- `repositories` はドメイン判断を持たない

この分離によって、後から

- 出力形式追加
- 抽出方式変更
- プロンプト更新
- 保存先変更

をしやすくします。

---

## 7. 命名規則

命名は、役割が読めることを優先します。

### 推奨サフィックス

- `*Extractor`  
  何かを抽出する責務

- `*Classifier`  
  分類する責務

- `*Builder`  
  複数要素をまとめて構造化する責務

- `*Validator`  
  妥当性確認

- `*Renderer`  
  描画・出力整形

- `*Repository`  
  保存・読込

- `*Reporter` / `*Detector`  
  レビュー補助

### 例

- `instruction_extractor.py`
- `training_asset_spec_builder.py`
- `schema_validator.py`
- `html_manual_renderer.py`
- `training_asset_repository.py`

---

## 8. この構成で守りたいこと

この `src/` 構成では、特に以下を崩さないことを重視します。

### 8.1 正本は `training_asset_spec`

どんな出力も、最終的には `training_asset_spec` から派生することを原則とします。

### 8.2 要約と手順を混ぜない

`summary_extractor` と `instruction_extractor` は統合しません。  
両者は目的も品質評価軸も異なるためです。

### 8.3 証跡の紐付けを後回しにしない

Transcript や OCR は補助情報ではなく、  
レビューと再検証のための基盤です。  
MVP 段階から扱えるようにします。

### 8.4 レンダリングを正本生成より先に複雑化しない

見た目の凝った PDF よりも先に、

- 構造が破綻しない
- 手順が抜けにくい
- 注意点が落ちにくい
- 元動画に戻れる

という品質を優先します。

---

## 9. 初期実装順の推奨

最初の着手順としては、以下を推奨します。

### Step 1

最小の CLI 入口を作る

- `cli/build_asset.py`
- `pipeline/build_training_asset_pipeline.py`

### Step 2

入力と証跡抽出をつなぐ

- `ingestion/video_loader.py`
- `evidence/transcript_extractor.py`
- `evidence/ocr_extractor.py`

### Step 3

分類と抽出を最小実装する

- `classification/segment_classifier.py`
- `extraction/instruction_extractor.py`
- `extraction/summary_extractor.py`
- `extraction/caution_extractor.py`

### Step 4

正規化して保存する

- `normalization/training_asset_spec_builder.py`
- `normalization/schema_validator.py`
- `repositories/training_asset_repository.py`

### Step 5

HTML / PDF 出力へつなぐ

- `renderers/html_manual_renderer.py`
- `renderers/pdf_manual_renderer.py`

---

## 10. 将来拡張を見据えた余地

この構成は、以下の拡張を視野に入れています。

- 複数動画の統合処理
- FAQ / 検索向けデータ生成の強化
- ブランド別テンプレート差し替え
- レビュー UI や承認フロー対応
- 管理画面 / API 化
- バッチ投入や案件単位管理
- モデル切替や抽出ルール差し替え

MVP では使わないモジュールがあっても、  
構造として置いておくことで成長余地を確保できます。

---

## 11. このドキュメントの位置づけ

このドキュメントは、`src/` の**完成確定図**ではなく、  
現時点の README と仕様群に整合する**初期標準構成案**です。

今後、実装を進める中で、

- 責務が重すぎるモジュールの分割
- 不要な層の統合
- テンプレートやパイプラインの整理
- CLI から API / UI への展開

などに応じて見直される可能性があります。

ただし、以下の原則は維持します。

- 正本 JSON 先行
- 要約と手順抽出の分離
- 証跡重視
- 出力責務分離
- MVP から拡張可能な構造

---

## 12. まとめ

VideoAsset Manualize の `src/` は、単なるスクリプト群ではなく、  
**動画を再利用可能な教育資産へ変換する処理責務を明確化した構造**として設計します。

中心となる流れは次の通りです。

**動画入力 → 証跡抽出 → セグメント分類 → 手順 / 要約 / 注意点抽出 → `training_asset_spec` 正規化 → HTML / PDF / 派生データ生成**

この構成により、MVP では

**1動画 → 1構造化JSON → 1要約 → 1HTML / 1PDF**

を安定して成立させ、  
将来的には FAQ、検索、チェックリスト、複数動画統合へと拡張しやすい基盤を作ります。
