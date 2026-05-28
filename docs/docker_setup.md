## Docker で起動する

このプロジェクトは **Docker / Docker Compose** で起動できます。  
Python や ffmpeg をローカルに直接入れなくても、まずは UI を立ち上げて動作確認できます。

### できること
- Streamlit UI をブラウザで開く
- Single Video / Assets / Batch & Booklet を使う
- CLI コマンドをコンテナ内で実行する
- 生成された HTML / PDF / JSON を `output/exports/` で確認する

---

## 前提条件

事前に以下を用意してください。

- **Docker Desktop**
- **Git**
- （任意）**OpenAI API Key**
  - LLM 機能を使う場合のみ必要です
- （任意）入力動画やサンプルファイル
  - `samples/` 配下のサンプルでも確認できます

> **Windows の場合**  
> Docker Desktop を起動した状態で作業してください。

---

## 1. リポジトリを開く

まず、リポジトリのルートに移動します。

```powershell
cd "D:\AI_スクリプト成果物\video-asset-manualize"
```

---

## 2. `.env` を準備する

`.env.example` がある場合は、それをコピーして `.env` を作成してください。

### PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

必要に応じて `.env` を編集してください。  
たとえば LLM 機能を使う場合は、OpenAI API Key を設定します。

例:

```env
OPENAI_API_KEY=your_api_key_here
```

> **注意**
> - API キーが未設定でも、LLM を使わない範囲の処理は動かせる構成にしている場合があります
> - ただし、LLM 要約・FAQ 生成などを使う場合は API キーが必要です

---

## 3. Docker イメージをビルドする

初回はイメージをビルドします。

```bash
docker compose build --no-cache
```

ビルドに少し時間がかかることがあります。  
エラーが出なければ次へ進んでください。

---

## 4. コンテナを起動する

バックグラウンドで起動します。

```bash
docker compose up -d
```

起動後、ブラウザで以下にアクセスしてください。

```text
http://localhost:8501
```

Streamlit UI が開けば成功です。

---

## 5. UI の動作確認

起動後は、まず以下の順で確認すると迷いにくいです。

### Single Video
- 動画パスを入力
- 必要に応じて Provider を選択
- `Process Video` を実行
- HTML / PDF / JSON が生成されるか確認

### Assets
- 生成済みアセットの一覧確認
- Review State の変更
- PDF / HTML / JSON のダウンロード確認

### Batch & Booklet
- `specs_manifest.json` を指定
- Batch 実行
- Booklet 生成
- `booklet.html` / `booklet.pdf` の確認

---

## 6. 生成ファイルの保存先

生成された成果物は通常、以下に出力されます。

```text
output/exports/
```

主な出力例:

```text
output/exports/
├── extracted_source_evidence.json
├── asset-xxxx_spec.json
├── asset-xxxx_manual.html
├── asset-xxxx_manual.pdf
├── batch/
│   ├── batch_report.json
│   └── ...
└── booklet/
    ├── customer-training_compiled.json
    ├── customer-training_booklet.html
    └── customer-training_booklet.pdf
```

> Docker Compose の設定により、`output/exports/` はホスト側からも確認できます。

---

## 7. CLI を Docker 環境で使う

UI だけでなく、CLI でも処理できます。  
まず起動中のコンテナにコマンドを渡します。

### バリデーション

```bash
docker compose exec app python -m video_asset_manualize.build_asset validate samples/sample_source_evidence.json
```

### 動画から `source_evidence` を生成

```bash
docker compose exec app python -m video_asset_manualize.build_asset video samples/sample_training_video.mp4
```

### `source_evidence` から `training_asset_spec` を生成

```bash
docker compose exec app python -m video_asset_manualize.build_asset extract output/exports/extracted_source_evidence.json
```

### HTML / PDF を生成

```bash
docker compose exec app python -m video_asset_manualize.build_asset build output/exports/phase5_spec.json
```

### Batch 実行

```bash
docker compose exec app python -m video_asset_manualize.build_asset batch-specs samples/specs_manifest.json --output-dir output/exports/batch
```

### Booklet 生成

```bash
docker compose exec app python -m video_asset_manualize.build_asset booklet-build samples/specs_manifest.json --output-dir output/exports/booklet --project-id customer-training --project-title "Customer Service Training Manual"
```

> `app` は `docker-compose.yml` のサービス名です。  
> サービス名が違う場合は、その名前に読み替えてください。

---

## 8. コンテナの状態確認

起動中コンテナを確認するには:

```bash
docker compose ps
```

ログを見るには:

```bash
docker compose logs -f
```

アプリのログだけ見たい場合:

```bash
docker compose logs -f app
```

---

## 9. 停止・再起動する

### 停止

```bash
docker compose down
```

### 再起動

```bash
docker compose up -d
```

### イメージを再ビルドして起動し直す

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## 10. よくあるトラブル

### 1. `http://localhost:8501` が開けない

以下を確認してください。

```bash
docker compose ps
docker compose logs -f app
```

確認ポイント:
- コンテナが起動しているか
- `8501` ポートが公開されているか
- Streamlit の起動エラーが出ていないか

---

### 2. PDF 生成時にフォントエラーが出る

日本語 PDF の生成にはフォント設定が重要です。  
このプロジェクトでは Docker 環境向けのフォント設定を反映済みですが、もしエラーが出る場合は以下を確認してください。

- `pdf_manual_renderer.py` のフォント設定が最新になっているか
- Docker イメージを再ビルドしたか

```bash
docker compose build --no-cache
docker compose up -d
```

---

### 3. OpenAI API Key エラーが出る

LLM 機能を使う場合は `.env` に API キーを設定してください。

```env
OPENAI_API_KEY=your_api_key_here
```

設定後は再起動してください。

```bash
docker compose down
docker compose up -d
```

---

### 4. 出力ファイルが見つからない

まず `output/exports/` を確認してください。

```powershell
Get-ChildItem .\output\exports\ -Recurse
```

または:

```bash
ls -R output/exports
```

ログも確認してください。

```bash
docker compose logs -f app
```

---

### 5. サンプル動画や manifest が見つからない

以下が存在するか確認してください。

```text
samples/sample_training_video.mp4
samples/sample_source_evidence.json
samples/specs_manifest.json
```

ファイル名が違う場合は、実在するパスを指定してください。

---

## 11. 初心者向けの最短手順

迷ったら、まずこの順で進めてください。

### Step 1: `.env` 作成

```powershell
Copy-Item .env.example .env
```

### Step 2: ビルド

```bash
docker compose build --no-cache
```

### Step 3: 起動

```bash
docker compose up -d
```

### Step 4: ブラウザを開く

```text
http://localhost:8501
```

### Step 5: Single Video で試す
- サンプルファイルを使う
- `Process Video` を押す
- PDF / HTML / JSON が出ることを確認する

### Step 6: 出力確認

```powershell
Get-ChildItem .\output\exports\ -Recurse
```

---

## 12. CLI と UI の使い分け

### UI を使うとよい場面
- まず試しに動かしたい
- ファイルを見ながら確認したい
- ダウンロードやレビュー操作をしたい

### CLI を使うとよい場面
- 処理手順を固定したい
- バッチ処理したい
- ログを見ながら再現性高く実行したい
- テストや自動化に組み込みたい

---

## 13. 補足

- Docker 化の目的は、**ローカルで同じ実行環境を再現しやすくすること**です
- まずは CPU 前提での安定動作を優先しています
- GPU 対応やクラウド本番配備は別フェーズで扱います
- 生成物は通常 `output/exports/` に保存されます

---

## 14. 起動確認の完了条件

以下ができれば、Docker 実行は成功です。

- `docker compose up -d` が成功する
- `http://localhost:8501` が開く
- Single Video から処理を実行できる
- PDF / HTML / JSON が生成される
- `output/exports/` に成果物が出る
