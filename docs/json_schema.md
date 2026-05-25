\# JSON Schema Design



\## 1. このドキュメントの目的



本ドキュメントは、VideoAsset Manualize における正本データ  

\*\*`training\_asset\_spec`\*\* の初期スキーマ設計方針を定義するためのものである。



本スキーマは、既存の研修動画・業務手順動画・マニュアル動画を、  

単なる視聴コンテンツではなく、\*\*再利用可能な教育資産・業務資産\*\*として扱うための基盤になる。



このドキュメントでは、以下を定義する。



\- `training\_asset\_spec` の役割

\- トップレベル構造

\- 各レイヤの責務

\- 初期フェーズでの必須項目と推奨項目

\- サンプル JSON

\- 将来拡張を見据えた設計意図



\---



\## 2. スキーマの基本方針



`training\_asset\_spec` は、動画 1 本ごとの構造化資産を表す正本データである。  

HTML、PDF、FAQ 候補、チェックリストなどの成果物は、このデータから派生生成する。



\### 2.1 正本データとして扱う理由



構造化 JSON を正本にすることで、以下の利点がある。



\- 出力形式が増えても中核データを共通化できる

\- 要約・手順・証跡の整合性を保ちやすい

\- PDF テンプレート変更時も再生成しやすい

\- 抽出ロジックの改善を反映しやすい

\- FAQ / 検索 / QA ボットへ二次利用しやすい

\- 人手レビュー結果を構造的に反映しやすい



\### 2.2 設計原則



本スキーマは、以下の原則に基づいて設計する。



1\. \*\*動画を直接成果物にしない\*\*

2\. \*\*証跡と利用データを分離する\*\*

3\. \*\*要約と手順抽出を分離する\*\*

4\. \*\*手順は再現可能な粒度で保持する\*\*

5\. \*\*派生物は JSON から生成する\*\*

6\. \*\*初期はシンプルに、拡張は段階的に行う\*\*



\---



\## 3. トップレベル構造



`training\_asset\_spec` は、少なくとも以下のトップレベルオブジェクトを持つ。



| オブジェクト | 役割 |

| --- | --- |

| `asset\_meta` | 資産としての基本情報 |

| `source\_evidence` | 元動画から抽出した証跡情報 |

| `instructional\_core` | 手順・注意点・条件分岐などの中核情報 |

| `derived\_views` | 用途別に再構成した派生ビュー |

| `delivery\_assets` | 実際の出力物や派生ファイル情報 |

| `\_metadata` | 生成処理・レビュー・版管理などの内部メタデータ |



\---



\## 4. スキーマ全体像



```text

training\_asset\_spec

├── asset\_meta

├── source\_evidence

├── instructional\_core

├── derived\_views

├── delivery\_assets

└── \_metadata

```



この構造により、  

\*\*「何の動画か」\*\*、\*\*「どこを根拠にしたか」\*\*、\*\*「どう使う資産にするか」\*\*、\*\*「何を出力したか」\*\* を分離して管理できる。



\---



\## 5. 各トップレベルオブジェクトの設計



\## 5.1 `asset\_meta`



\### 役割



`asset\_meta` は、動画資産そのものの基本情報を保持するレイヤである。  

利用者がこの資産を識別し、対象や目的を理解するための入口情報を持つ。



\### 主な項目



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `asset\_id` | string | 必須 | 資産の一意識別子 |

| `source\_video\_id` | string | 任意 | 元動画を識別するID |

| `title` | string | 必須 | 資産タイトル |

| `purpose` | string | 推奨 | この動画 / 手順の目的 |

| `target\_audience` | array\[string] | 推奨 | 想定利用者 |

| `target\_department` | array\[string] | 任意 | 対象部署 |

| `prerequisites` | array\[string] | 推奨 | 前提条件、必要権限、準備物 |

| `language` | string | 推奨 | 言語コード、例: `ja-JP` |

| `status` | string | 推奨 | `draft` / `reviewed` / `approved` など |

| `version` | string | 推奨 | 版情報 |

| `created\_at` | string | 推奨 | 初回生成日時 |

| `updated\_at` | string | 推奨 | 最終更新日時 |



\### 設計意図



このレイヤは、手順内容とは独立して「資産として何者か」を定義する。  

検索、一覧表示、バージョン管理、部署別配布などの基礎になる。



\---



\## 5.2 `source\_evidence`



\### 役割



`source\_evidence` は、元動画から抽出された証跡データを保持するレイヤである。  

ここには、文字起こし、OCR、タイムスタンプ、スクリーンショット候補など、  

\*\*中核情報の根拠となる素材\*\*を保持する。



\### 主な項目



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `source\_video` | object | 推奨 | 元動画に関する参照情報 |

| `transcript\_segments` | array\[object] | 推奨 | 時刻付き文字起こしセグメント |

| `ocr\_segments` | array\[object] | 任意 | 画面上テキストの抽出結果 |

| `screenshot\_candidates` | array\[object] | 任意 | マニュアル挿入候補の画面情報 |

| `speaker\_segments` | array\[object] | 任意 | 話者推定結果 |

| `evidence\_links` | array\[object] | 任意 | 中核手順との対応情報 |



\### `transcript\_segments` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `segment\_id` | string | 必須 | セグメントID |

| `start\_ms` | integer | 必須 | 開始時刻（ミリ秒） |

| `end\_ms` | integer | 必須 | 終了時刻（ミリ秒） |

| `speaker\_label` | string | 任意 | 話者ラベル |

| `text` | string | 必須 | 文字起こし本文 |

| `confidence` | number | 任意 | 抽出信頼度 |

| `classification\_hint` | string | 任意 | 暫定分類ヒント |



\### `ocr\_segments` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `ocr\_id` | string | 必須 | OCR断片ID |

| `start\_ms` | integer | 必須 | 開始時刻 |

| `end\_ms` | integer | 必須 | 終了時刻 |

| `text` | string | 必須 | OCR文字列 |

| `screen\_region` | string | 任意 | 画面位置情報 |

| `confidence` | number | 任意 | OCR信頼度 |



\### `screenshot\_candidates` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `screenshot\_id` | string | 必須 | 画像候補ID |

| `at\_ms` | integer | 必須 | キャプチャ時刻 |

| `description` | string | 推奨 | 画像の用途説明 |

| `file\_ref` | string | 任意 | 保存先参照 |

| `related\_step\_ids` | array\[string] | 任意 | 関連ステップID |



\### 設計意図



このレイヤは、レビュー時の「なぜこの手順になったのか」を説明するために不可欠である。  

後から抽出ミスや粒度のズレを修正する際にも、この証跡層が再処理の基盤になる。



\---



\## 5.3 `instructional\_core`



\### 役割



`instructional\_core` は、本プロジェクトの中核レイヤである。  

手順、注意点、条件分岐、ミス対処、チェックリストといった、  

\*\*現場で再利用される業務知識\*\*を保持する。



\### 主な項目



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `summary` | object | 推奨 | 概要説明、目的整理 |

| `chapters` | array\[object] | 必須 | 章構造 |

| `global\_cautions` | array\[string] | 任意 | 全体にかかる注意点 |

| `global\_common\_mistakes` | array\[object] | 任意 | 全体で頻出するミス |

| `global\_checklist` | array\[object] | 任意 | 全体チェック項目 |



\### `summary` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `purpose\_summary` | string | 推奨 | この手順の目的要約 |

| `outcome\_summary` | string | 任意 | 完了時に得られる状態 |

| `audience\_summary` | string | 任意 | 想定読者向け補足 |

| `scope\_notes` | array\[string] | 任意 | 適用範囲・注意範囲 |



> `summary` は説明パートを要約した情報であり、操作手順そのものを圧縮しすぎないことが重要である。



\### `chapters` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `chapter\_id` | string | 必須 | 章ID |

| `title` | string | 必須 | 章タイトル |

| `objective` | string | 推奨 | この章の目的 |

| `procedures` | array\[object] | 必須 | 手順群 |

| `chapter\_cautions` | array\[string] | 任意 | 章全体の注意点 |



\### `procedures` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `procedure\_id` | string | 必須 | 手順ID |

| `title` | string | 必須 | 手順タイトル |

| `goal` | string | 推奨 | この手順で達成する状態 |

| `steps` | array\[object] | 必須 | ステップ群 |

| `conditions` | array\[string] | 任意 | 前提条件や分岐条件 |

| `cautions` | array\[string] | 任意 | 手順単位の注意点 |

| `common\_mistakes` | array\[object] | 任意 | よくあるミス |

| `checkpoints` | array\[string] | 任意 | 完了確認ポイント |



\### `steps` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `step\_id` | string | 必須 | ステップID |

| `order` | integer | 必須 | 順序 |

| `action` | string | 必須 | 実際の操作内容 |

| `expected\_result` | string | 任意 | 操作後の期待状態 |

| `button\_labels` | array\[string] | 任意 | ボタン名・UIラベル |

| `input\_fields` | array\[string] | 任意 | 入力項目名 |

| `branch\_condition` | string | 任意 | 条件分岐 |

| `notes` | array\[string] | 任意 | 補足説明 |

| `cautions` | array\[string] | 任意 | ステップ単位の注意点 |

| `evidence\_refs` | array\[string] | 任意 | 証跡参照ID |



\### `common\_mistakes` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `mistake` | string | 必須 | よくあるミス |

| `cause` | string | 任意 | 原因 |

| `impact` | string | 任意 | 影響 |

| `recovery\_action` | string | 推奨 | 対処法 |



\### 設計意図



`instructional\_core` では、  

\*\*説明は読みやすく要約しつつ、操作・条件分岐・注意点はできるだけ粒度を落とさず保持する\*\*。  

これが、単なる要約ではなく「使える手順書」にするための核となる。



\---



\## 5.4 `derived\_views`



\### 役割



`derived\_views` は、中核情報を利用シーン別に再構成したビューを保持するレイヤである。  

ここは正本そのものではなく、\*\*利用形態に合わせた見せ方\*\*を持つ。



\### 主な項目



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `beginner\_view` | object | 任意 | 新人向け簡易版 |

| `checklist\_view` | object | 任意 | 実施確認用チェックリスト |

| `faq\_candidates` | array\[object] | 任意 | FAQ候補 |

| `digest\_view` | object | 任意 | ダイジェスト版 |

| `manager\_view` | object | 任意 | 管理者向け観点 |



\### `faq\_candidates` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `faq\_id` | string | 必須 | FAQ候補ID |

| `question` | string | 必須 | 想定質問 |

| `answer\_draft` | string | 推奨 | 回答草案 |

| `related\_step\_ids` | array\[string] | 任意 | 関連ステップ |

| `priority` | string | 任意 | 優先度 |



\### `checklist\_view` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `title` | string | 推奨 | チェックリスト名 |

| `items` | array\[object] | 推奨 | チェック項目 |

| `usage\_notes` | array\[string] | 任意 | 利用上の注意 |



\### 設計意図



このレイヤを分けることで、  

同じ中核手順から「新人向け」「確認用」「FAQ用」へ派生させやすくなる。  

将来的な検索や QA ボット連携にも接続しやすい。



\---



\## 5.5 `delivery\_assets`



\### 役割



`delivery\_assets` は、実際に生成・配布する成果物や、その参照情報を保持するレイヤである。  

ここには、RAW テキスト、要約、HTML、PDF などを保持する。



\### 主な項目



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `raw\_transcript` | object | 任意 | 生文字起こし出力 |

| `summary\_text` | object | 任意 | 要約出力 |

| `html\_manual` | object | 任意 | HTML出力 |

| `pdf\_manual` | object | 任意 | PDF出力 |

| `exported\_files` | array\[object] | 任意 | 派生ファイル一覧 |



\### `exported\_files` の想定構造



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `asset\_type` | string | 必須 | `html` / `pdf` / `txt` など |

| `file\_ref` | string | 任意 | 保存先参照 |

| `generated\_at` | string | 任意 | 生成日時 |

| `template\_version` | string | 任意 | テンプレート版 |



\### 設計意図



成果物情報を JSON 内に持つことで、  

「何を出したか」「どのテンプレートで出したか」「いつ出したか」を追える。  

ただし、このレイヤ自体を正本とせず、あくまで派生情報として扱う。



\---



\## 5.6 `\_metadata`



\### 役割



`\_metadata` は、システム内部的な生成・レビュー・管理情報を保持するレイヤである。



\### 主な項目



| 項目 | 型 | 必須 | 説明 |

| --- | --- | --- | --- |

| `schema\_version` | string | 必須 | スキーマ版 |

| `generated\_at` | string | 推奨 | 生成日時 |

| `pipeline\_version` | string | 任意 | 処理パイプライン版 |

| `generation\_context` | object | 任意 | 生成条件や処理設定 |

| `review\_status` | string | 推奨 | `unreviewed` / `in\_review` / `approved` など |

| `review\_notes` | array\[string] | 任意 | レビュー補足 |

| `change\_log` | array\[object] | 任意 | 更新履歴 |



\### 設計意図



このレイヤは、将来的にレビュー運用や再生成運用を安定化させるために重要である。  

初期段階では最小限でもよいが、スキーマ版とレビュー状態だけは早い段階から持っておく価値が高い。



\---



\## 6. 必須項目の初期方針



初期フェーズでは、すべてを必須にしない。  

MVP を成立させるため、最低限以下を必須とする。



\### 6.1 トップレベル必須



\- `asset\_meta`

\- `instructional\_core`

\- `\_metadata`



\### 6.2 `asset\_meta` 必須



\- `asset\_id`

\- `title`



\### 6.3 `instructional\_core` 必須



\- `chapters`



\### 6.4 `chapters` 必須



\- `chapter\_id`

\- `title`

\- `procedures`



\### 6.5 `procedures` 必須



\- `procedure\_id`

\- `title`

\- `steps`



\### 6.6 `steps` 必須



\- `step\_id`

\- `order`

\- `action`



\### 6.7 `\_metadata` 必須



\- `schema\_version`



このようにして、初期段階では「最低限成立する構造」を先に固定し、  

証跡や派生ビューは段階的に厚くしていく。



\---



\## 7. 初期 JSON サンプル



以下は、`training\_asset\_spec` の初期サンプルである。  

説明用サンプルのため、値はダミーである。



```json

{

&#x20; "asset\_meta": {

&#x20;   "asset\_id": "asset-001",

&#x20;   "source\_video\_id": "video-001",

&#x20;   "title": "顧客登録手順",

&#x20;   "purpose": "新規顧客をシステムに正しく登録できるようにする",

&#x20;   "target\_audience": \["新入社員", "店舗スタッフ"],

&#x20;   "target\_department": \["営業部", "店舗運営部"],

&#x20;   "prerequisites": \[

&#x20;     "業務システムへのログイン権限を持っていること",

&#x20;     "顧客情報が事前に手元にあること"

&#x20;   ],

&#x20;   "language": "ja-JP",

&#x20;   "status": "draft",

&#x20;   "version": "0.1.0",

&#x20;   "created\_at": "2026-05-25T00:00:00+09:00",

&#x20;   "updated\_at": "2026-05-25T00:00:00+09:00"

&#x20; },

&#x20; "source\_evidence": {

&#x20;   "source\_video": {

&#x20;     "title": "顧客登録研修動画",

&#x20;     "duration\_ms": 540000,

&#x20;     "source\_type": "internal\_training\_video"

&#x20;   },

&#x20;   "transcript\_segments": \[

&#x20;     {

&#x20;       "segment\_id": "ts-001",

&#x20;       "start\_ms": 1000,

&#x20;       "end\_ms": 8000,

&#x20;       "speaker\_label": "trainer",

&#x20;       "text": "まず画面上部のメニューから顧客管理を開きます。",

&#x20;       "confidence": 0.97,

&#x20;       "classification\_hint": "operation"

&#x20;     }

&#x20;   ],

&#x20;   "ocr\_segments": \[

&#x20;     {

&#x20;       "ocr\_id": "ocr-001",

&#x20;       "start\_ms": 2500,

&#x20;       "end\_ms": 5000,

&#x20;       "text": "顧客管理",

&#x20;       "screen\_region": "top\_navigation",

&#x20;       "confidence": 0.93

&#x20;     }

&#x20;   ],

&#x20;   "screenshot\_candidates": \[

&#x20;     {

&#x20;       "screenshot\_id": "sc-001",

&#x20;       "at\_ms": 3200,

&#x20;       "description": "顧客管理メニューが表示されている画面",

&#x20;       "file\_ref": "screenshots/sc-001.png",

&#x20;       "related\_step\_ids": \["step-001"]

&#x20;     }

&#x20;   ],

&#x20;   "evidence\_links": \[

&#x20;     {

&#x20;       "evidence\_ref\_id": "ev-001",

&#x20;       "related\_step\_id": "step-001",

&#x20;       "transcript\_segment\_ids": \["ts-001"],

&#x20;       "ocr\_segment\_ids": \["ocr-001"],

&#x20;       "screenshot\_ids": \["sc-001"]

&#x20;     }

&#x20;   ]

&#x20; },

&#x20; "instructional\_core": {

&#x20;   "summary": {

&#x20;     "purpose\_summary": "顧客管理画面から新規顧客を登録する基本手順を説明する。",

&#x20;     "outcome\_summary": "顧客情報を入力し、登録完了まで進められる状態を目指す。",

&#x20;     "audience\_summary": "新人スタッフ向けの基本操作手順である。",

&#x20;     "scope\_notes": \[

&#x20;       "法人顧客の特別登録は対象外",

&#x20;       "承認フローは別マニュアルを参照"

&#x20;     ]

&#x20;   },

&#x20;   "chapters": \[

&#x20;     {

&#x20;       "chapter\_id": "chapter-001",

&#x20;       "title": "顧客登録の開始",

&#x20;       "objective": "顧客登録画面を開き、新規登録を開始する",

&#x20;       "chapter\_cautions": \[

&#x20;         "誤って既存顧客を上書きしないこと"

&#x20;       ],

&#x20;       "procedures": \[

&#x20;         {

&#x20;           "procedure\_id": "procedure-001",

&#x20;           "title": "顧客管理画面を開く",

&#x20;           "goal": "新規顧客登録を始められる状態にする",

&#x20;           "conditions": \[

&#x20;             "ログイン済みであること"

&#x20;           ],

&#x20;           "cautions": \[

&#x20;             "権限がない場合はメニューが表示されない"

&#x20;           ],

&#x20;           "checkpoints": \[

&#x20;             "顧客管理画面が表示されている"

&#x20;           ],

&#x20;           "common\_mistakes": \[

&#x20;             {

&#x20;               "mistake": "顧客検索画面のまま進めてしまう",

&#x20;               "cause": "メニュー選択を誤る",

&#x20;               "impact": "新規登録ボタンが表示されない",

&#x20;               "recovery\_action": "トップメニューから顧客管理を開き直す"

&#x20;             }

&#x20;           ],

&#x20;           "steps": \[

&#x20;             {

&#x20;               "step\_id": "step-001",

&#x20;               "order": 1,

&#x20;               "action": "画面上部メニューから「顧客管理」を押す",

&#x20;               "expected\_result": "顧客管理画面が表示される",

&#x20;               "button\_labels": \["顧客管理"],

&#x20;               "input\_fields": \[],

&#x20;               "branch\_condition": "",

&#x20;               "notes": \[

&#x20;                 "トップナビゲーションから選択する"

&#x20;               ],

&#x20;               "cautions": \[

&#x20;                 "表示されない場合は権限設定を確認する"

&#x20;               ],

&#x20;               "evidence\_refs": \["ev-001"]

&#x20;             },

&#x20;             {

&#x20;               "step\_id": "step-002",

&#x20;               "order": 2,

&#x20;               "action": "「新規登録」ボタンを押す",

&#x20;               "expected\_result": "顧客入力フォームが開く",

&#x20;               "button\_labels": \["新規登録"],

&#x20;               "input\_fields": \[],

&#x20;               "branch\_condition": "",

&#x20;               "notes": \[],

&#x20;               "cautions": \[

&#x20;                 "既存顧客編集画面と混同しない"

&#x20;               ],

&#x20;               "evidence\_refs": \[]

&#x20;             }

&#x20;           ]

&#x20;         }

&#x20;       ]

&#x20;     }

&#x20;   ],

&#x20;   "global\_cautions": \[

&#x20;     "登録前に重複顧客が存在しないか確認する"

&#x20;   ],

&#x20;   "global\_common\_mistakes": \[

&#x20;     {

&#x20;       "mistake": "入力途中で保存せず画面を閉じる",

&#x20;       "cause": "途中保存の必要性を認識していない",

&#x20;       "impact": "再入力が必要になる",

&#x20;       "recovery\_action": "入力完了前に一時保存できるか確認する"

&#x20;     }

&#x20;   ],

&#x20;   "global\_checklist": \[

&#x20;     {

&#x20;       "item": "登録前に重複顧客を確認した",

&#x20;       "required": true

&#x20;     },

&#x20;     {

&#x20;       "item": "必須項目をすべて入力した",

&#x20;       "required": true

&#x20;     }

&#x20;   ]

&#x20; },

&#x20; "derived\_views": {

&#x20;   "beginner\_view": {

&#x20;     "title": "新人向け簡易版",

&#x20;     "key\_points": \[

&#x20;       "まず顧客管理を開く",

&#x20;       "新規登録を押す",

&#x20;       "重複確認を忘れない"

&#x20;     ]

&#x20;   },

&#x20;   "checklist\_view": {

&#x20;     "title": "顧客登録チェックリスト",

&#x20;     "items": \[

&#x20;       {

&#x20;         "item\_id": "check-001",

&#x20;         "text": "顧客管理画面を開いた",

&#x20;         "required": true

&#x20;       },

&#x20;       {

&#x20;         "item\_id": "check-002",

&#x20;         "text": "重複顧客の確認を行った",

&#x20;         "required": true

&#x20;       }

&#x20;     ],

&#x20;     "usage\_notes": \[

&#x20;       "新人教育時の実施確認に利用する"

&#x20;     ]

&#x20;   },

&#x20;   "faq\_candidates": \[

&#x20;     {

&#x20;       "faq\_id": "faq-001",

&#x20;       "question": "顧客管理メニューが表示されない場合はどうすればよいか",

&#x20;       "answer\_draft": "ログイン権限またはアカウント権限設定を確認し、必要に応じて管理者へ申請する。",

&#x20;       "related\_step\_ids": \["step-001"],

&#x20;       "priority": "high"

&#x20;     }

&#x20;   ],

&#x20;   "digest\_view": {

&#x20;     "title": "ダイジェスト",

&#x20;     "summary\_points": \[

&#x20;       "顧客登録は顧客管理メニューから開始する",

&#x20;       "重複確認を先に行う",

&#x20;       "必須項目を入力して登録する"

&#x20;     ]

&#x20;   }

&#x20; },

&#x20; "delivery\_assets": {

&#x20;   "raw\_transcript": {

&#x20;     "file\_ref": "exports/raw\_transcript\_asset-001.txt"

&#x20;   },

&#x20;   "summary\_text": {

&#x20;     "text": "顧客管理画面から新規顧客を登録する基本手順をまとめた。",

&#x20;     "generated\_at": "2026-05-25T00:00:00+09:00"

&#x20;   },

&#x20;   "html\_manual": {

&#x20;     "file\_ref": "exports/manual\_asset-001.html",

&#x20;     "template\_version": "0.1.0"

&#x20;   },

&#x20;   "pdf\_manual": {

&#x20;     "file\_ref": "exports/manual\_asset-001.pdf",

&#x20;     "template\_version": "0.1.0"

&#x20;   },

&#x20;   "exported\_files": \[

&#x20;     {

&#x20;       "asset\_type": "html",

&#x20;       "file\_ref": "exports/manual\_asset-001.html",

&#x20;       "generated\_at": "2026-05-25T00:00:00+09:00",

&#x20;       "template\_version": "0.1.0"

&#x20;     },

&#x20;     {

&#x20;       "asset\_type": "pdf",

&#x20;       "file\_ref": "exports/manual\_asset-001.pdf",

&#x20;       "generated\_at": "2026-05-25T00:00:00+09:00",

&#x20;       "template\_version": "0.1.0"

&#x20;     }

&#x20;   ]

&#x20; },

&#x20; "\_metadata": {

&#x20;   "schema\_version": "0.1.0",

&#x20;   "generated\_at": "2026-05-25T00:00:00+09:00",

&#x20;   "pipeline\_version": "0.1.0",

&#x20;   "generation\_context": {

&#x20;     "mode": "mvp",

&#x20;     "review\_required": true

&#x20;   },

&#x20;   "review\_status": "unreviewed",

&#x20;   "review\_notes": \[],

&#x20;   "change\_log": \[]

&#x20; }

}

```



\---



\## 8. 初期スキーマにおける型・命名の方針



\### 8.1 ID 命名



ID は初期段階では人間が追いやすい形式でよい。



例:



\- `asset-001`

\- `chapter-001`

\- `procedure-001`

\- `step-001`

\- `ts-001`

\- `ocr-001`

\- `ev-001`



将来的に UUID 化してもよいが、初期フェーズでは可読性を優先する。



\### 8.2 日時表現



日時は基本的に ISO 8601 文字列で保持する。



例:



\- `2026-05-25T00:00:00+09:00`



\### 8.3 時刻情報



動画内参照時刻は、初期段階では \*\*ミリ秒整数\*\* で統一する。



例:



\- `start\_ms`

\- `end\_ms`

\- `at\_ms`



理由は、ステップ単位や OCR 断片との照合がしやすいためである。



\### 8.4 配列と単数値の使い分け



複数になりうる項目は、初期段階から配列で持つ。



例:



\- `target\_audience`

\- `prerequisites`

\- `chapters`

\- `steps`

\- `cautions`

\- `faq\_candidates`



これにより、将来的な拡張時に型変更が起きにくくなる。



\---



\## 9. スキーマ設計上の重要な考え方



\## 9.1 要約は `instructional\_core.summary` に閉じ込める



要約文は便利だが、手順全体を要約へ寄せると再現性が失われる。  

そのため、要約は `summary` に閉じ込め、手順本体は章・手順・ステップで保持する。



\## 9.2 UI ラベルや条件分岐を落とさない



業務マニュアル化で重要なのは、次のような情報である。



\- ボタン名

\- 入力項目名

\- 画面名

\- 確認ポイント

\- 分岐条件

\- 注意点

\- よくあるミス



これらは「説明より細かいから省く」のではなく、むしろ優先して保持する。



\## 9.3 証跡を参照可能にする



各ステップが、どの transcript / OCR / screenshot に対応するかを追えるようにする。  

これにより、レビューと改善が現実的になる。



\## 9.4 派生ビューは中核を複製しすぎない



`derived\_views` では、`instructional\_core` の完全コピーを作るのではなく、  

利用目的に応じた要点整理や再構成に留める。  

中核情報の二重管理を避けるためである。



\---



\## 10. 将来拡張を見据えたポイント



本スキーマは、初期段階ではシンプルに始めるが、以下へ拡張しやすい構造を意識している。



\### 10.1 FAQ / QA ボット再利用



\- `faq\_candidates`

\- `common\_mistakes`

\- `recovery\_action`

\- `checkpoints`



これらは、そのまま FAQ や質問応答の材料になりやすい。



\### 10.2 検索基盤再利用



\- `title`

\- `purpose`

\- `chapter.title`

\- `procedure.title`

\- `step.action`

\- `button\_labels`

\- `input\_fields`



これらを検索インデックス化することで、  

動画を見る前に必要な手順へ到達しやすくなる。



\### 10.3 チェックリスト化



\- `global\_checklist`

\- `checkpoints`

\- `checklist\_view`



これらを持っておくことで、実務確認や教育完了確認へ転用しやすい。



\### 10.4 冊子化・複数動画統合



動画 1 本単位で構造化しておけば、  

将来的に複数の `training\_asset\_spec` を束ねて、部門別冊子や業務別ハンドブックへ発展させやすい。



\---



\## 11. 初期フェーズでの非ゴール



初期スキーマ設計では、以下をまだ含めない、または必須にしない。



\- すべての UI 座標情報の厳密保持

\- 画面レイアウトの完全再現

\- 動画編集用メタデータ

\- 複雑な承認ワークフロー定義

\- 権限体系の完全モデル化

\- 全業種共通の汎用完全スキーマ化



まずは、\*\*1 動画を 1 資産として手順書化できる最小構造\*\*を優先する。



\---



\## 12. 初期バージョニング方針



\### 12.1 スキーマ版



`\_metadata.schema\_version` でスキーマ版を管理する。



初期値例:



\- `0.1.0`



\### 12.2 テンプレート版



HTML / PDF のテンプレート版は `delivery\_assets` 側で管理する。



例:



\- `template\_version: "0.1.0"`



\### 12.3 パイプライン版



抽出処理や整形処理の差分を追いたい場合は、  

`\_metadata.pipeline\_version` に記録する。



\---



\## 13. まとめ



`training\_asset\_spec` は、VideoAsset Manualize における正本データである。  

このスキーマの目的は、動画を単なる視聴素材ではなく、  

\*\*証跡付きの構造化資産\*\*として扱えるようにすることにある。



本スキーマの要点は以下である。



\- `asset\_meta` で資産の基本情報を持つ

\- `source\_evidence` で元動画の証跡を保持する

\- `instructional\_core` で手順・注意点・条件分岐を保持する

\- `derived\_views` で FAQ やチェックリスト向けの再構成を持つ

\- `delivery\_assets` で HTML / PDF などの派生物を管理する

\- `\_metadata` で生成・レビュー・版管理を行う



この構造により、  

\*\*要約と手順抽出を分離しつつ、将来の検索・FAQ・チェックリスト再利用に耐えるデータ基盤\*\*を整備することができる。



