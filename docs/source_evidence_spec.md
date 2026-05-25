\# Source Evidence Specification



\## 1. 目的



このドキュメントは、\*\*VideoAsset Manualize Phase 2\*\* における `source\_evidence` の初期仕様を定義するものです。



`source\_evidence` は、動画から抽出した\*\*証跡データの保持領域\*\*です。  

本プロジェクトでは、最終成果物である HTML / PDF マニュアルだけでなく、\*\*元動画のどの箇所から何を抽出したかを追跡できること\*\*を重視します。



そのため、`source\_evidence` は単なる補助情報ではなく、以下を支える基盤として扱います。



\- 手順抽出の根拠

\- 要約の根拠

\- 注意点抽出の根拠

\- 人手レビュー時の確認材料

\- 将来の再抽出・再学習・改善用データ



\---



\## 2. この仕様の位置づけ



本仕様は、`training\_asset\_spec` 全体のうち、以下の領域を対象とします。



\- `source\_evidence.source\_video`

\- `source\_evidence.transcript\_segments`

\- `source\_evidence.ocr\_segments`

\- `source\_evidence.screenshot\_candidates`

\- `source\_evidence.speaker\_segments`

\- `source\_evidence.evidence\_links`



このドキュメントは、\*\*動画から何をどの形で持つか\*\*を定義するものであり、  

章・手順・ステップなどの業務構造そのものは対象外です。  

それらは `instructional\_core` 側で保持します。



\---



\## 3. 基本方針



\### 3.1 証跡は要約しすぎない



`source\_evidence` では、説明文の要約や手順の再構成を行いません。  

ここではまず、\*\*元動画に近い粒度の証跡\*\*を保持します。



\### 3.2 抽出結果と証跡を分離する



\- 証跡は `source\_evidence`

\- 手順や要約は `instructional\_core`



に分けて保持します。



これにより、後から抽出ロジックが変わっても、証跡さえ残っていれば再構築できます。



\### 3.3 タイムスタンプを必ず持つ



Phase 2 では、少なくとも transcript と OCR について、\*\*開始・終了時刻\*\*を保持します。  

時間情報がないと、元動画へ戻って検証することが難しくなるためです。



\### 3.4 将来拡張に耐えるが、MVPでは持ちすぎない



将来的には、以下のような証跡も扱う可能性があります。



\- フレーム画像

\- UI 要素検出

\- 話者 diarization の詳細情報

\- confidence score の詳細内訳

\- 音声イベント



ただし Phase 2 初期では、まず以下を優先します。



\- 動画メタ情報

\- transcript

\- OCR

\- screenshot candidate

\- 必要最低限の speaker 情報

\- 証跡リンク



\---



\## 4. `source\_evidence` の役割



`source\_evidence` は、動画から抽出した\*\*一次情報の保管場所\*\*です。



\### 4.1 主な用途



\- 手順抽出時に、操作発話の根拠を確認する

\- 注意点抽出時に、画面表示や発話を確認する

\- 人手レビュー時に、元の動画位置へ戻る

\- FAQ やチェックリスト生成時の参照元にする

\- 抽出精度改善時に再利用する



\### 4.2 役割上の非対象



以下は `source\_evidence` の責務ではありません。



\- 手順の章立て

\- 業務上の意味づけ

\- 要約文の最終決定

\- PDF 用の表示整形

\- FAQ 本文の完成版生成



\---



\## 5. トップレベル構造



`training\_asset\_spec` における `source\_evidence` の基本構造は、以下を想定します。



```json

{

&#x20; "source\_evidence": {

&#x20;   "source\_video": {},

&#x20;   "transcript\_segments": \[],

&#x20;   "ocr\_segments": \[],

&#x20;   "screenshot\_candidates": \[],

&#x20;   "speaker\_segments": \[],

&#x20;   "evidence\_links": \[]

&#x20; }

}

```



MVP / Phase 2 初期では、すべてを必須にする必要はありません。  

ただし、以下は\*\*強く推奨\*\*します。



\- `source\_video`

\- `transcript\_segments`



次点で推奨するのは以下です。



\- `ocr\_segments`

\- `evidence\_links`



\---



\## 6. 各フィールド仕様



\## 6.1 `source\_video`



元動画そのものの情報を保持します。



\### 目的



\- どの動画を処理対象としたかを特定する

\- duration などの基礎情報を保持する

\- ローカルファイル / URL / 論理ID の対応を残す



\### 想定構造



```json

{

&#x20; "source\_video": {

&#x20;   "video\_id": "video-001",

&#x20;   "file\_name": "customer\_registration\_training.mp4",

&#x20;   "file\_path": "inputs/customer\_registration\_training.mp4",

&#x20;   "source\_type": "local\_file",

&#x20;   "duration\_ms": 845000,

&#x20;   "language": "ja",

&#x20;   "checksum": null

&#x20; }

}

```



\### 推奨フィールド



\- `video\_id`  

&#x20; プロジェクト内での動画識別子



\- `file\_name`  

&#x20; 元動画ファイル名



\- `file\_path`  

&#x20; 入力パスまたは保存先



\- `source\_type`  

&#x20; 例: `local\_file`, `uploaded\_file`, `url`



\- `duration\_ms`  

&#x20; 動画全長（ミリ秒）



\- `language`  

&#x20; 主言語



\- `checksum`  

&#x20; 将来的な重複判定や整合確認用。初期は null 可



\---



\## 6.2 `transcript\_segments`



音声の文字起こし結果をセグメント単位で保持します。



\### 目的



\- 要約の根拠

\- 手順抽出の根拠

\- 注意点抽出の根拠

\- 動画との照合



\### 基本方針



\- transcript は全文一括文字列ではなく、\*\*セグメント配列\*\*で持つ

\- 各セグメントに\*\*開始時刻・終了時刻\*\*を持たせる

\- 可能なら confidence を持たせる

\- 話者が分かる場合は speaker 情報を保持する



\### 想定構造



```json

{

&#x20; "transcript\_segments": \[

&#x20;   {

&#x20;     "segment\_id": "ts-001",

&#x20;     "start\_ms": 1200,

&#x20;     "end\_ms": 6800,

&#x20;     "text": "まず画面上部のメニューから顧客管理を開きます。",

&#x20;     "speaker\_id": "spk-001",

&#x20;     "confidence": 0.96

&#x20;   }

&#x20; ]

}

```



\### 必須にしたい最小フィールド



\- `segment\_id`

\- `start\_ms`

\- `end\_ms`

\- `text`



\### 推奨フィールド



\- `speaker\_id`

\- `confidence`



\### 注意点



\- `start\_ms < end\_ms` を必須とする

\- 空文字 transcript は保持しない

\- 同一内容の重複セグメントは極力避ける

\- 句読点整形は許容するが、意味改変はしない



\---



\## 6.3 `ocr\_segments`



画面内文字列の抽出結果をセグメント単位で保持します。



\### 目的



\- 画面上のボタン名、項目名、警告文の保持

\- 音声だけでは分からない UI 文言の補完

\- 手順の具体性向上



\### 基本方針



\- OCR 結果も transcript と同様に\*\*時間と紐づいた配列\*\*で持つ

\- 可能なら画面上の位置情報も持つ

\- 全フレームを持つ必要はなく、変化点中心でもよい



\### 想定構造



```json

{

&#x20; "ocr\_segments": \[

&#x20;   {

&#x20;     "ocr\_id": "ocr-001",

&#x20;     "start\_ms": 1500,

&#x20;     "end\_ms": 5000,

&#x20;     "text": "顧客管理",

&#x20;     "bbox": \[120, 40, 260, 88],

&#x20;     "confidence": 0.91

&#x20;   }

&#x20; ]

}

```



\### 推奨フィールド



\- `ocr\_id`

\- `start\_ms`

\- `end\_ms`

\- `text`



\### 任意フィールド



\- `bbox`

\- `confidence`



\### 注意点



\- OCR はノイズが多いため、元結果を保持しつつ後段で使い分ける

\- 1文字単位ではなく、意味のあるまとまりを優先する

\- 同一テキストが長時間継続する場合は、冗長に分割しすぎない



\---



\## 6.4 `screenshot\_candidates`



レビューやマニュアル生成時に使える静止画候補を保持します。



\### 目的



\- 操作画面の視覚的確認

\- 手順書への画像差し込み候補

\- レビュー時の理解補助



\### 基本方針



\- MVP では必須ではない

\- Phase 2 では、まず\*\*候補管理\*\*だけできればよい

\- 実際に PDF に埋め込むかは後段判断



\### 想定構造



```json

{

&#x20; "screenshot\_candidates": \[

&#x20;   {

&#x20;     "screenshot\_id": "sc-001",

&#x20;     "timestamp\_ms": 3200,

&#x20;     "image\_path": "artifacts/screenshots/sc-001.png",

&#x20;     "description": "顧客管理メニュー表示時の画面"

&#x20;   }

&#x20; ]

}

```



\### 推奨フィールド



\- `screenshot\_id`

\- `timestamp\_ms`

\- `image\_path`



\### 任意フィールド



\- `description`



\---



\## 6.5 `speaker\_segments`



話者情報を必要最低限保持します。



\### 目的



\- ナレーションと実演者の切り分け

\- 説明主体と操作主体の見分け

\- 将来的な diarization 連携



\### 基本方針



\- Phase 2 初期では任意

\- transcript 側に `speaker\_id` があれば十分な場合も多い

\- 話者ごとの詳細プロファイルまでは不要



\### 想定構造



```json

{

&#x20; "speaker\_segments": \[

&#x20;   {

&#x20;     "speaker\_id": "spk-001",

&#x20;     "start\_ms": 0,

&#x20;     "end\_ms": 120000,

&#x20;     "label": "narrator"

&#x20;   }

&#x20; ]

}

```



\### 推奨フィールド



\- `speaker\_id`

\- `start\_ms`

\- `end\_ms`



\### 任意フィールド



\- `label`



\---



\## 6.6 `evidence\_links`



証跡と抽出結果を結ぶ参照情報です。



\### 目的



\- どの手順がどの transcript / OCR から来たかを追う

\- レビュー時に根拠へ戻る

\- 将来的な traceability report 生成に使う



\### 基本方針



\- `instructional\_core` 側の要素IDと、`source\_evidence` 側の証跡IDを結ぶ

\- 1対1に限らず、1対多 / 多対多も許容する



\### 想定構造



```json

{

&#x20; "evidence\_links": \[

&#x20;   {

&#x20;     "link\_id": "evl-001",

&#x20;     "target\_type": "step",

&#x20;     "target\_id": "step-001",

&#x20;     "evidence\_type": "transcript\_segment",

&#x20;     "evidence\_id": "ts-001"

&#x20;   },

&#x20;   {

&#x20;     "link\_id": "evl-002",

&#x20;     "target\_type": "step",

&#x20;     "target\_id": "step-001",

&#x20;     "evidence\_type": "ocr\_segment",

&#x20;     "evidence\_id": "ocr-001"

&#x20;   }

&#x20; ]

}

```



\### 推奨フィールド



\- `link\_id`

\- `target\_type`

\- `target\_id`

\- `evidence\_type`

\- `evidence\_id`



\### `target\_type` の候補例



\- `summary`

\- `chapter`

\- `procedure`

\- `step`

\- `caution`

\- `faq\_candidate`



\### `evidence\_type` の候補例



\- `transcript\_segment`

\- `ocr\_segment`

\- `screenshot\_candidate`

\- `speaker\_segment`



\---



\## 7. 時刻表現ルール



`source\_evidence` では、時刻は基本的に\*\*ミリ秒整数\*\*で統一します。



\### 7.1 ルール



\- 単位は `ms`

\- 型は整数

\- 相対時刻（動画先頭を 0ms）とする

\- `start\_ms` と `end\_ms` は `start\_ms <= end\_ms`

\- 単一点の場合は `timestamp\_ms` を使う



\### 7.2 理由



\- transcript / OCR / screenshot の相互参照がしやすい

\- 秒表現より細かく扱える

\- 将来的なフレーム近似に拡張しやすい



\---



\## 8. ID 命名ルール



MVP / Phase 2 初期では、可読な接頭辞付き ID を推奨します。



\### 例



\- transcript segment: `ts-001`

\- OCR segment: `ocr-001`

\- screenshot: `sc-001`

\- speaker: `spk-001`

\- evidence link: `evl-001`



\### 方針



\- 一意であれば厳密な連番でなくてもよい

\- 初期は人間が読めることを優先する

\- 将来 UUID 化してもよい



\---



\## 9. 品質要件



`source\_evidence` では、以下を最低限の品質要件とします。



\### 9.1 transcript



\- 主要発話が大きく欠落していない

\- 時刻情報が付いている

\- text が空ではない



\### 9.2 OCR



\- 明らかな UI 文言や警告文を拾える

\- ノイズだけの結果で埋まらない

\- transcript の補助として機能する



\### 9.3 evidence link



\- 少なくとも主要な step の一部が transcript と結びついている

\- 人手レビュー時に根拠へ戻れる



\---



\## 10. Phase 2 初期の必須・推奨・任意



\## 10.1 必須



\- `source\_video`

\- `transcript\_segments`



\## 10.2 強く推奨



\- `ocr\_segments`

\- `evidence\_links`



\## 10.3 任意



\- `screenshot\_candidates`

\- `speaker\_segments`



\---



\## 11. 最小サンプル



Phase 2 初期で成立する最小の `source\_evidence` 例は以下です。



```json

{

&#x20; "source\_evidence": {

&#x20;   "source\_video": {

&#x20;     "video\_id": "video-001",

&#x20;     "file\_name": "customer\_registration\_training.mp4",

&#x20;     "file\_path": "inputs/customer\_registration\_training.mp4",

&#x20;     "source\_type": "local\_file",

&#x20;     "duration\_ms": 845000,

&#x20;     "language": "ja"

&#x20;   },

&#x20;   "transcript\_segments": \[

&#x20;     {

&#x20;       "segment\_id": "ts-001",

&#x20;       "start\_ms": 1200,

&#x20;       "end\_ms": 6800,

&#x20;       "text": "まず画面上部のメニューから顧客管理を開きます。"

&#x20;     },

&#x20;     {

&#x20;       "segment\_id": "ts-002",

&#x20;       "start\_ms": 6900,

&#x20;       "end\_ms": 11800,

&#x20;       "text": "新規登録ボタンを押してください。"

&#x20;     }

&#x20;   ],

&#x20;   "ocr\_segments": \[

&#x20;     {

&#x20;       "ocr\_id": "ocr-001",

&#x20;       "start\_ms": 1500,

&#x20;       "end\_ms": 5000,

&#x20;       "text": "顧客管理"

&#x20;     },

&#x20;     {

&#x20;       "ocr\_id": "ocr-002",

&#x20;       "start\_ms": 7000,

&#x20;       "end\_ms": 11000,

&#x20;       "text": "新規登録"

&#x20;     }

&#x20;   ],

&#x20;   "evidence\_links": \[

&#x20;     {

&#x20;       "link\_id": "evl-001",

&#x20;       "target\_type": "step",

&#x20;       "target\_id": "step-001",

&#x20;       "evidence\_type": "transcript\_segment",

&#x20;       "evidence\_id": "ts-001"

&#x20;     },

&#x20;     {

&#x20;       "link\_id": "evl-002",

&#x20;       "target\_type": "step",

&#x20;       "target\_id": "step-002",

&#x20;       "evidence\_type": "ocr\_segment",

&#x20;       "evidence\_id": "ocr-002"

&#x20;     }

&#x20;   ]

&#x20; }

}

```



\---



\## 12. 非ゴール



Phase 2 初期では、以下はこの仕様の対象外とします。



\- 完全な話者 diarization 詳細管理

\- フレーム単位の映像解析標準化

\- UI 要素検出の完全構造化

\- 全 OCR 候補の高精度クレンジング

\- 全証跡に対する厳密スコアリング

\- 画像埋め込みの最終レイアウト仕様

\- 動画フォーマット変換仕様



\---



\## 13. 将来拡張の方向



将来的には、以下の拡張が考えられます。



\- `frame\_reference` の導入

\- `ui\_elements` の構造化

\- `audio\_events` の追加

\- `confidence\_breakdown` の追加

\- screenshot 自動選定ルールの高度化

\- evidence link の重みづけ

\- step 単位の複数証跡スコアリング



\---



\## 14. まとめ



`source\_evidence` は、VideoAsset Manualize における\*\*証跡の基盤層\*\*です。



ここで重視するのは、見た目の整った成果物ではなく、以下が成立することです。



\- 元動画に戻れる

\- transcript と OCR を保持できる

\- 抽出結果と証跡を結びつけられる

\- 後から再抽出・再検証できる



Phase 2 初期では、まず



\- `source\_video`

\- `transcript\_segments`

\- `ocr\_segments`

\- `evidence\_links`



を中心に整備し、  

その上で手順抽出・要約・HTML / PDF 生成の精度を高めていく方針とします。



