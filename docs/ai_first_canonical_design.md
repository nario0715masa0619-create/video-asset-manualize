# AI-First Canonical Design
**ファイル名:** \docs/ai_first_canonical_design.md\

## 目的

本ドキュメントは、VideoAsset Manualize における **AI-first canonical design** を定義する。  
ここでいう canonical とは、最終成果物の源泉となる**正本データ**を指し、本プロジェクトではそれを **AI が \source_evidence\ を解釈して生成する structured JSON (\	raining_asset_spec\)** と定義する。  
本方針は、[video-insight-spec](https://github.com/nario0715masa0619-create/video-insight-spec) で採用されている「AI接続前提の高純度 structured JSON を中核資産に置く」思想を、VideoAsset Manualize の業務マニュアル生成ドメインに適用するものである。

---

## 背景

VIS では、\insight_spec_{id}.json\ が単なる中間生成物ではなく、**AIにそのまま入力できる主・最終正本**として扱われ、narrative、report、GUI、PDF などの成果物はそこから派生生成される構造になっている。

VideoAsset Manualize でも、\	raining_asset_spec\ を正本とする思想自体はすでに存在するが、現状の一部実装・運用では LLM 経路が optional 扱いになっており、**正本が AI 生成 structured JSON である**という設計中心がまだ十分に固定されていない。

このドキュメントは、そのブレをなくし、以後の実装判断を一貫させるための基準文書である。

---

## 設計原則

### 1. 正本は AI 生成の structured JSON とする
本プロジェクトにおける canonical asset は **\	raining_asset_spec\** である。  
ただし、単に JSON 形式であれば canonical なのではなく、**AI が \source_evidence\ を解釈・要約・構造化して生成した \	raining_asset_spec\** を canonical とみなす。

### 2. \source_evidence\ は証跡・素材層であり、正本ではない
\source_evidence\ は transcript、OCR、timestamp、screenshot、speaker 情報などを保持する evidence base である。  
これは traceability のために不可欠だが、**そのまま最終成果物や業務資産の正本とはみなさない**。  
意味づけされた主成果物は \	raining_asset_spec\ である。

### 3. 派生成果物はすべて canonical から作る
HTML、PDF、Booklet、FAQ 表示、checklist、manager view、UI 表示データなど、**最終利用物はすべて \	raining_asset_spec\ から派生生成する**。  
これにより、出力形式が増えても再生成可能性と整合性を維持できる。

### 4. 非AI経路は fallback / test-only とする
AI が使えない、または AI 出力が不十分な場合に備え、ルールベースまたは簡易 builder を残してよい。  
ただしそれは **canonical generation の代替ではなく fallback** であり、正本生成の主経路としては扱わない。

---

## 用語定義

### Canonical
本プロジェクトにおける「正本」。  
AI が \source_evidence\ を解釈して生成した \	raining_asset_spec\ を指す。

### Evidence
元動画由来の証跡データ。  
transcript、OCR、timestamp、speaker、screenshot など。

### Derived Asset
canonical から派生生成される成果物。  
例: HTML manual、PDF manual、Booklet、FAQ 表示、チェックリスト。

### Fallback Generation
AI を使わずに暫定的な spec を構築する補助経路。  
開発中の比較、障害時の最低限出力、テスト用途に限定する。

---

## システム境界

### システム内で扱うもの
- 動画入力または \source_evidence\
- AI による \	raining_asset_spec\ 生成
- \	raining_asset_spec\ からの派生物生成
- traceability のための evidence 保持
- UI / CLI / Batch / Booklet での canonical 利用

### システム境界の外に置くもの
- YouTube 競合分析
- KPI 可視化中心の分析ダッシュボード
- narrative / executive report を主成果物に置く構成
- 営業提案資料生成に最適化された JSON スキーマ
- 認証、マルチテナント、クラウド本番配備、DB 主体設計

これらは VIS の特徴として参考になる場合はあるが、本プロジェクトの canonical design の中核には含めない。

---

## 責務定義

### 1. \source_evidence\ の責務
\source_evidence\ の責務は以下に限定する。

- 元動画の事実を近い粒度で保持する
- transcript / OCR / timestamp / screenshot / speaker を保持する
- 抽出結果を evidence として追跡可能にする
- AI が \	raining_asset_spec\ を生成するための入力素材になる

**責務に含めないもの**
- 最終マニュアル構成の確定
- 要約の正本
- 手順の正本
- FAQ の正本
- 業務観点で意味付けされた最終成果物

### 2. \	raining_asset_spec\ の責務
\	raining_asset_spec\ は canonical asset として以下を担う。

- 業務・教育文脈で意味づけされた構造化データである
- summary / chapter / procedure / step / caution / FAQ を一貫した schema に保持する
- \source_evidence\ との関連を保ち、traceability を失わない
- 派生成果物の唯一の源泉となる
- 人間にも AI にも再利用しやすい

**責務に含めないもの**
- 元動画の生 transcript の完全保存
- OCR の低レベル結果そのもの
- PDF / HTML 表現のレイアウト情報そのもの
- 一時的な UI 状態

### 3. Renderer / Exporter の責務
Renderer / Exporter は以下のみを担う。

- canonical (\	raining_asset_spec\) を読んで表示用に変換する
- HTML / PDF / Booklet / Text を生成する
- layout / typography / page break など表示層の責務を扱う

**責務に含めないもの**
- summary の意味解釈
- procedure の抽出
- caution / FAQ の生成
- canonical JSON の品質改善

### 4. UI / CLI の責務
UI / CLI は以下のみを担う。

- 入力受付
- canonical generation の起動
- evidence / spec / derived assets の参照
- 実行状態の表示
- review 状態の補助的管理

**責務に含めないもの**
- canonical の定義変更
- AI 出力品質の意味判断
- schema の主導的定義

---

## 入出力契約

### 入力

canonical generation の主入力は **\source_evidence\** である。

最低限含むべきもの:

- \source_video\
- \	ranscript_segments\

推奨:

- \ocr_segments\
- \screenshot_candidates\
- \speaker_segments\
- \vidence_links\

この入力は「素材」であり、「答え」ではない。

### 出力

canonical generation の主出力は **\	raining_asset_spec\** である。

最低限期待される構成:

- \sset_meta\
- \source_evidence\
- \instructional_core\
- \derived_views\
- \metadata\ または \_metadata\ 系の生成情報

この JSON は、**そのまま downstream の manual / booklet / AI 利用に使える品質**を目指す。

---

## 正本生成パイプライン

理想的な canonical generation は、概ね次の流れを取る。

\\\	ext
video
  ↓
source_evidence
  ↓
AI canonical generation
  ↓
training_asset_spec
  ↓
HTML / PDF / Booklet / UI views / FAQ / checklist
\\\

このとき重要なのは、  
**\source_evidence -> training_asset_spec\ の変換こそが中核工程**であること。  
動画の取り込みや PDF 出力は重要だが、設計上の中心ではない。

---

## canonical generation モード

### 1. Canonical Mode
標準経路。  
LLM を用いて \source_evidence\ から \	raining_asset_spec\ を生成する。  
本プロジェクトの通常運用では、この経路を既定とする。

### 2. Fallback Mode
AI 利用不可、API 障害、実験、ローカル簡易検証などのための補助経路。  
canonical を代替するものではなく、**暫定生成**として扱う。

### 3. Test Mode
dummy provider や mock データを使ってパイプライン疎通だけを確認する経路。  
品質評価対象には含めない。

---

## 品質境界

canonical と見なすためには、少なくとも以下を満たす必要がある。

- summary が空でない
- chapter / procedure / step が最低限構造化されている
- caution / FAQ が生成されている、または未生成理由が明示されている
- evidence との関連を失っていない
- \	raining_asset_spec\ 単体から HTML / PDF / Booklet を再生成できる
- 生成情報（生成時刻、provider、model、mode 等）が metadata に保持される

この品質基準の詳細は別紙の acceptance criteria に委ねるが、本ドキュメントでは「canonical は AI が高純度に意味づけした structured JSON である」という原則だけを固定する。

---

## 境界条件

### 境界 1: AI は正本生成に使うが、元証跡を改ざんしない
AI は \source_evidence\ を解釈して \	raining_asset_spec\ を生成するが、  
元証跡の transcript / OCR / timestamp そのものを canonical の都合で書き換えない。

### 境界 2: evidence は正本を支えるが、正本に優越しない
証跡は重要だが、最終成果物の責務は \	raining_asset_spec\ にある。  
「証跡があるから正本」とはならない。  
「証跡に基づいて AI が意味づけした structured JSON」が正本である。

### 境界 3: 表示と意味を分離する
PDF や HTML の layout 改善は重要だが、それは canonical の定義とは別の問題である。  
意味構造は \	raining_asset_spec\、見た目は renderer が担当する。

---

## 非目標

本ドキュメントで定義する AI-first canonical design は、以下を目標にしない。

- VIS の YouTube 分析ドメインをそのまま移植すること
- narrative / executive report を主成果物にすること
- 分析営業向け JSON をそのまま流用すること
- クラウド本番環境や認証基盤の設計
- DB 主体のデータプラットフォーム化
- すべての出力品質問題を一度に解決すること
- ただちに Gemini / OpenAI / その他 LLM の最終勝者を決めること
- すべての non-LLM 経路を即時削除すること

このドキュメントの目的は、**まず canonical の定義を固定し、今後の実装がつぎはぎにならないようにすること**である。

---

## 実装への含意

この設計を採用する場合、以後の実装は次の方針に従う。

1. \xtract\ の主経路は canonical generation として整理する
2. non-LLM builder は fallback / test-only に位置づけ直す
3. UI / CLI の既定値は canonical generation を自然に通るように見直す
4. README / docs は「AI で正本を作る」前提で再記述する
5. schema の改善は canonical 定義に従って行う

---

## 将来拡張

将来的には、以下をこの canonical design の上に積むことができる。

- provider 切り替え戦略（OpenAI / Gemini / others）
- structured output の厳格化
- acceptance criteria の自動検証
- review workflow における canonical 品質判定
- canonical JSON からの検索・再編集・差分管理

これらは本設計の上位拡張であり、本ドキュメントの成立条件ではない。

---

## 暫定結論

VideoAsset Manualize の canonical asset は、  
**AI が \source_evidence\ を解釈して生成する \	raining_asset_spec\** である。

\source_evidence\ は証跡・素材層、  
HTML / PDF / Booklet は派生物であり、  
本プロジェクトの中核は **高純度な AI 生成 structured JSON をどう安定生成するか** にある。

この定義により、VideoAsset Manualize は VIS の本質である  
**「AI-generated structured JSON as the primary asset」**  
をドメイン適合した形で継承する。

---

## 参照元

- [video-insight-spec リポジトリ](https://github.com/nario0715masa0619-create/video-insight-spec)
- [VideoAsset Manualize VIS 踏襲方針メモ](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/docs/vis_inheritance_policy.md)
- [VideoAsset Manualize architecture.md](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/docs/architecture.md)
- [VideoAsset Manualize project_overview.md](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/docs/project_overview.md)
- [VideoAsset Manualize source_evidence_spec.md](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/docs/source_evidence_spec.md)
