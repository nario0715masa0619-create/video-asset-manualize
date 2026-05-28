# Canonical Generation Acceptance Criteria
**ファイル名:** \docs/canonical_generation_acceptance_criteria.md\

## 目的

本ドキュメントは、VideoAsset Manualize において生成される \	raining_asset_spec\ を **canonical（正本）として受け入れてよいかを判定する基準** を定義する。  
本基準は、\docs/ai_first_canonical_design.md\ で定義した **「正本 = AI が \source_evidence\ を解釈して生成した structured JSON」** という設計原則に整合するものである。

本ドキュメントの目的は、次の3点にある。

1. \	raining_asset_spec\ を canonical として扱ってよい条件を固定する  
2. fallback / test-only 出力と canonical を明確に区別する  
3. 人手レビューと自動テストの観点を揃え、つぎはぎ実装を防ぐ  

---

## 背景

VIS では、\insight_spec_{id}.json\ が **主・最終正本** であり、AI にそのまま入力できる高純度 structured JSON として扱われている。レポートや GUI は、その JSON から派生生成される。

VideoAsset Manualize でも同様に、\source_evidence\ を素材・証跡層、\	raining_asset_spec\ を AI 生成正本、HTML / PDF / Booklet を派生成果物として整理する方針を採っている。

したがって、本プロジェクトにおける受け入れ判定の中心は、**ファイルが JSON であること**ではなく、**その JSON が AI-first canonical design に適合しているか**である。

---

## 適用範囲

本基準は、以下の出力に適用する。

- \source_evidence\ から生成された \	raining_asset_spec\
- 単一動画処理の canonical generation 出力
- Batch 処理で生成された各 \	raining_asset_spec\
- Booklet の元となる個別 \	raining_asset_spec\

本基準は、以下には直接適用しない。

- \source_evidence\ 自体
- HTML / PDF / Booklet のレイアウト品質そのもの
- テスト用の dummy 出力
- fallback / test-only 経路の暫定 spec

ただし、派生成果物が canonical から再生成可能であることは、canonical 受け入れ条件の一部として扱う。

---

## 用語定義

### Canonical
AI が \source_evidence\ を解釈して生成した、唯一の正本 \	raining_asset_spec\。

### Fallback Output
AI を使わずに暫定生成した spec。  
運用継続や比較検証には使ってよいが、canonical としては扱わない。

### Test Output
dummy provider や mock 入力を使って疎通確認のために作成した spec。  
品質評価対象には含めない。

### Acceptance
生成された \	raining_asset_spec\ を、正本として採用してよいと判断すること。

### Rejection
生成された \	raining_asset_spec\ を、正本としては採用不可と判断すること。

---

## 受け入れ判定レベル

\	raining_asset_spec\ の判定結果は、次の3段階で管理する。

| 判定 | 意味 | 実務利用 |
|---|---|---|
| **Accepted** | canonical として受理可能。派生成果物の源泉として利用してよい | 可 |
| **Accepted with Review** | 構造上は受理可能だが、人手確認または軽微修正を前提とする | 条件付き可 |
| **Rejected** | canonical としては採用不可。fallback または再生成が必要 | 不可 |

原則として、**最終運用投入する JSON は \Accepted\ もしくは \Accepted with Review\ のみ**とする。

---

## 必須要件

以下は **canonical として受け入れるための必須要件** である。  
1つでも満たさない場合、その出力は \Rejected\ とする。

### 1. AI 生成であること
- \	raining_asset_spec\ は **AI canonical generation** により生成されていること
- non-LLM builder 単独生成物を canonical として扱わないこと
- metadata に canonical generation の実行事実が残っていること

### 2. 入力が \source_evidence\ ベースであること
- canonical generation の入力は \source_evidence\ であること
- \source_video\ が存在すること
- \	ranscript_segments\ が存在し、空配列でないこと
- evidence のない完全な想像出力でないこと

### 3. スキーマ整合性を満たすこと
- \	raining_asset_spec\ が現行 schema に整合すること
- JSON として妥当であること
- required fields が欠落していないこと

### 4. 正本としての最低限の意味構造を持つこと
最低限、以下が存在し、空でないこと。

- \sset_meta\
- \source_evidence\
- \instructional_core\
- \derived_views\
- \metadata\ または同等の生成情報

さらに \instructional_core\ には、少なくとも以下のいずれかの意味構造が存在すること。

- summary
- chapter / procedure / step
- caution
- FAQ 候補

### 5. Traceability を失っていないこと
- \source_evidence\ を spec 内に保持していること、または確実に参照可能であること
- step / caution / FAQ が evidence から完全に切り離されていないこと
- 元動画に遡れる最低限の情報（video_id / timestamps / transcript / OCR 等）が残っていること

### 6. 派生成果物を再生成できること
- HTML / PDF / Booklet などが \	raining_asset_spec\ を入力として再生成可能であること
- 派生成果物のために、renderer 外の手作業補正を前提としないこと

### 7. 生成モードが明示されていること
metadata に最低限以下が残ることを推奨し、少なくとも生成コンテキストは必須とする。

- generated_at
- generation mode（canonical / fallback / test）
- provider
- model
- pipeline_version
- review_status

---

## 品質基準

必須要件を満たしたうえで、canonical 品質は以下の観点で評価する。

### 1. 構造品質

#### 合格基準
- JSON 構造が破綻していない
- トップレベルと主要セクションの責務が混在していない
- \instructional_core\ が意味単位として読める
- \derived_views\ が \instructional_core\ と矛盾しない

#### 要注意
- 必須キーはあるが中身がほぼ空
- summary はあるが procedure が実質存在しない
- FAQ や checklist がテンプレート文の繰り返しになっている

#### 失格
- schema violation
- 主要フィールドの欠落
- renderer が読む前提を満たしていない

---

### 2. 意味品質

#### 合格基準
- summary が対象動画の目的・流れを適切に要約している
- procedure / step が業務手順として実行可能な粒度を持つ
- caution が具体的で、単なる一般論に終わっていない
- FAQ が transcript / OCR / step 内容と整合している

#### 要注意
- summary が抽象的すぎる
- step が「クリックします」「入力します」など最低限すぎて判断に使えない
- caution が一般的注意ばかりで動画固有性が弱い
- FAQ が冗長で、実務上の価値が低い

#### 失格
- 意味内容の大半が evidence と無関係
- summary / step / FAQ がほぼ hallucination と判断される
- 手順として実行不能なレベルで情報が欠落している

---

### 3. Traceability 品質

#### 合格基準
- \source_evidence\ が保持されている
- transcript / OCR / timestamp に最低限遡れる
- step や caution が evidence と論理的に対応している

#### 要注意
- evidence はあるが、step との関係が弱い
- timestamp や link の粒度が粗く、追跡に手間がかかる

#### 失格
- evidence が実質参照不能
- \	raining_asset_spec\ が evidence から切断されている
- 元動画と spec の関連が追えない

---

### 4. 業務利用品質

#### 合格基準
- 人が読んで実際の業務手順として使える
- 手順、注意点、FAQ が最低限の実務価値を持つ
- 派生 HTML / PDF で利用しても意味が崩れない

#### 要注意
- 情報はあるが、現場利用には人手補筆が必要
- 手順粒度が荒く、教育利用には不足がある

#### 失格
- 実務資料として機能しない
- 派生成果物にしても意味が成立しない

---

### 5. 一貫性品質

#### 合格基準
- title / summary / steps / cautions / FAQ の間で意味矛盾がない
- asset_meta と instructional_core の内容が整合している
- derived_views が本体と矛盾しない

#### 要注意
- 用語揺れが多い
- summary と procedures の重点がずれている

#### 失格
- section 間で明確に矛盾している
- 一方では必須、他方では不要など、運用上混乱する出力になっている

---

## 失敗条件

以下のいずれかに該当する場合、canonical generation は失敗とみなす。

### 1. 非AI出力を canonical と誤認している
- dummy provider / non-LLM builder の出力を canonical として保存している
- metadata に mode が残っていない
- fallback output が正本扱いされている

### 2. evidence 不足
- \	ranscript_segments\ が空
- \source_video\ が欠落
- OCR / transcript が壊れていて意味のある解釈ができない

### 3. 構造不良
- schema validation 失敗
- required fields 欠落
- renderer が解釈できない構造

### 4. 意味不良
- summary が空
- chapter / procedure / step が実質存在しない
- caution / FAQ が evidence と無関係
- 内容がテンプレート文のみで動画固有性がない

### 5. 派生不能
- HTML / PDF / Booklet を canonical から再生成できない
- 手作業の補正が必須

### 6. traceability 破綻
- evidence と spec の接続が失われている
- 元動画へ戻れない
- review 不能なレベルで出典不明

---

## レビュー観点

人手レビューでは、次の観点を確認する。

### 1. 正本性レビュー
- この出力は本当に AI canonical generation で作られているか
- fallback / test output が混入していないか
- metadata から mode / provider / model を確認できるか

### 2. 内容レビュー
- summary は動画の目的と成果を正しく表しているか
- step は業務実行に十分か
- caution は事故防止・入力ミス防止に役立つか
- FAQ は現場から出そうな疑問をカバーしているか

### 3. evidence レビュー
- transcript / OCR / timestamp と内容が対応しているか
- 重要手順が evidence に裏づけられているか
- hallucinatory な追加説明が混じっていないか

### 4. 派生成果物レビュー
- HTML / PDF 化しても意味が崩れないか
- 見た目ではなく、内容が canonical に忠実か
- renderer 側の都合で内容が欠落していないか

### 5. 運用レビュー
- この JSON を再利用して Batch / Booklet / FAQ 表示に使えるか
- 次工程で人手補正が過度に必要にならないか
- 実務開始用データ資産として十分か

---

## テスト観点

受け入れ基準を継続的に守るため、少なくとも以下の観点でテストする。

### 1. Unit Test 観点
- schema validation が通る
- metadata に mode / provider / model が入る
- canonical builder と fallback builder を区別できる
- required field の欠落時に適切に失敗する

### 2. Integration Test 観点
- \source_evidence -> training_asset_spec\ が canonical generation として成立する
- \	raining_asset_spec -> HTML / PDF\ が再生成可能
- UI / CLI 両方から同じ canonical generation が通る

### 3. Regression Test 観点
- 既存の accepted sample が引き続き accepted を維持する
- AI-first 化後に dummy / fallback が既定経路へ逆流していない
- schema / renderer 更新で canonical 品質が壊れていない

### 4. Negative Test 観点
- transcript が空のとき reject される
- invalid schema のとき reject される
- provider 未設定 / API key 不備時に canonical 扱いされない
- fallback output が canonical と誤記録されない

### 5. Review Support Test 観点
- review_status を保持できる
- accepted / accepted with review / rejected を記録できる
- 再レビュー時に前回の生成情報が追える

---

## 受け入れ判定フロー

canonical generation の受け入れは、以下の順で判定する。

\\\	ext
1. 生成モード確認
   ↓
2. schema validation
   ↓
3. 必須要件確認
   ↓
4. 品質基準評価
   ↓
5. 派生成果物再生成確認
   ↓
6. 人手レビュー
   ↓
7. Accepted / Accepted with Review / Rejected を決定
\\\

---

## 判定ルール

### Accepted
以下をすべて満たす場合。

- 必須要件をすべて満たす
- 重大な失敗条件に該当しない
- 派生成果物を再生成できる
- 内容が実務利用可能な品質を持つ
- 人手レビューで重大修正不要と判断される

### Accepted with Review
以下のいずれかに該当する場合。

- 必須要件は満たす
- schema / traceability / regeneration は成立している
- ただし summary / step / caution / FAQ の具体性に改善余地がある
- 軽微修正またはレビュー注記つきで運用投入可能

### Rejected
以下のいずれかに該当する場合。

- 必須要件未達
- 失敗条件該当
- canonical generation ではない
- 実務利用に耐えない
- 派生成果物の源泉として信頼できない

---

## 実装への含意

この acceptance criteria を採用する場合、実装は次を満たす必要がある。

1. canonical generation と fallback generation をコード上で区別できること
2. metadata に mode / provider / model / generated_at を残すこと
3. UI / CLI が canonical を標準経路として扱うこと
4. schema validation と acceptance review を分離すること
5. renderer が canonical だけを前提に再生成できること

---

## 非目標

本ドキュメントは次を扱わない。

- LLM provider の最終選定
- OpenAI / Gemini / Claude の優劣比較そのもの
- PDF レイアウトの美観基準
- UI の使いやすさ詳細
- クラウド本番環境の SLO / SLA
- VIS の分析用途 JSON をそのまま再現すること

本ドキュメントの目的は、**canonical 受け入れの基準を固定すること**である。

---

## 暫定結論

VideoAsset Manualize において \	raining_asset_spec\ を canonical として受け入れるためには、  
単に JSON が生成されているだけでは不十分である。

受け入れ対象となるのは、**AI-first canonical design に従い、\source_evidence\ をもとに AI が意味づけ・構造化し、traceability と再生成可能性を備えた \	raining_asset_spec\** のみである。

この基準により、本プロジェクトは

- fallback / test-only 出力
- 単なる中間 JSON
- evidence と切れた見かけ上の spec

を正本から排除し、**高純度 structured JSON を中心資産とする運用**を成立させる。

---

## 参照元

- [AI-First Canonical Design](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/docs/ai_first_canonical_design.md)
- [VIS 踏襲方針メモ](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/docs/vis_inheritance_policy.md)
- [VideoAsset Manualize architecture.md](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/docs/architecture.md)
- [VideoAsset Manualize source_evidence_spec.md](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/docs/source_evidence_spec.md)
- [VIS README](https://github.com/nario0715masa0619-create/video-insight-spec/blob/main/README.md)
