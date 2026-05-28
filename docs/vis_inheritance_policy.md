# VIS 踏襲方針メモ  
**ファイル名:** docs/vis_inheritance_policy.md

## 目的

本ドキュメントは、[video-insight-spec](https://github.com/nario0715masa0619-create/video-insight-spec)（以下、VIS）を参照したうえで、**VideoAsset Manualize が何を踏襲し、何を踏襲しないか**を整理するための意思決定メモである。

目的は、既存の高精度な AI 活用設計のうち、**本プロジェクトに本当に必要な中核部分だけを継承**し、ドメインや成果物の違いによるズレを避けることにある。

---

## 結論

VIS から踏襲すべき中核は、**AI が生成する高純度の構造化 JSON を中心資産に置く思想**である。  
一方で、**YouTube 分析・競合分析・narrative レポート中心のドメイン文脈**は、そのままは踏襲しない。

つまり、VideoAsset Manualize は次の方針を採る。

- **踏襲する:** AI生成の高純度 structured JSON を正本に据える
- **踏襲する:** その JSON から複数成果物を派生生成する
- **踏襲する:** CLI と Web UI の両立
- **踏襲しない:** YouTube 競合分析中心のユースケース
- **踏襲しない:** narrative / executive report を主成果物とする構成
- **踏襲しない:** VIS 固有の分析用途最適化 JSON 設計

---

## 前提理解

VIS は公開リポジトリ上の情報から、以下の特徴を持つ。

- AI で利用・生成される構造化 JSON（insight_spec_{id}.json）を中核に置く
- その JSON をもとに narrative、report、GUI、PDF などを派生生成する
- CLI と Web GUI の両方を持つ
- AI 活用ユースケースや deliverables を強く意識した構成になっている

一方、VideoAsset Manualize は以下を中核とする。

- source_evidence を証跡データとして保持する
- 	raining_asset_spec を正本データとして扱う
- HTML / PDF / Booklet / FAQ / checklist などを派生生成する
- 業務手順・教育マニュアル・再利用可能な教材資産の生成を目的とする

---

## VIS から踏襲するもの・しないもの 比較表

| 区分 | 項目 | VISでの位置づけ | VideoAsset Manualizeへの示唆 | 推奨判断 |
|---|---|---|---|---|
| 踏襲する | **AI生成の高純度構造化JSONを中核資産にする** | insight_spec_{id}.json が AI 活用・成果物生成の源泉データとして機能している | 	raining_asset_spec も単なる出力用 JSON ではなく、**AI が意味理解して生成する正本**として位置づけるべき | **全面踏襲** |
| 踏襲する | **JSONから複数成果物を派生生成する設計** | JSON を起点に report / narrative / GUI / PDF へ展開する構図 | HTML / PDF / Booklet / FAQ / checklist などはすべて 	raining_asset_spec 派生に統一する | **全面踏襲** |
| 踏襲する | **CLI と Web UI の両立** | CLI と Streamlit Web GUI を併存させている | VideoAsset Manualize も CLI / Streamlit 両立を維持する | **維持して踏襲** |
| 踏襲しない | **YouTube競合分析・KPI可視化中心のドメイン文脈** | YouTube SaaS / competitor analytics / executive report の色が強い | VideoAsset Manualize の中心は **業務手順・教育マニュアル化** であり、ドメインは切り離すべき | **非踏襲** |
| 踏襲しない | **Narrative / レポートを主成果物に置く構成** | NarrativeEngine やレポート生成が主役に近い | VideoAsset Manualize の主成果物は manual / booklet / structured spec であり、narrative は補助に留める | **非踏襲** |
| 踏襲しない | **分析用途に最適化されたJSON責務** | 分析・営業・レポート用途を強く意識した JSON 設計 | 	raining_asset_spec は **作業手順・注意点・FAQ・証跡連携** に最適化すべきで、同一責務を持たせない | **非踏襲** |

---

## 踏襲方針の要約

### 1. AI生成の structured JSON を正本にする
本プロジェクトでは、単に JSON を保存するのではなく、**AI が source_evidence を解釈して生成した 	raining_asset_spec を中核資産に置く**。  
これは VIS の「AI 生成 JSON を源泉データとする」思想を継承するものである。

### 2. 派生成果物はすべて正本 JSON から作る
HTML、PDF、Booklet、FAQ、checklist などは、**すべて 	raining_asset_spec から派生生成する**。  
これにより、出力形式が増えても、常に同じ正本から再生成できる。

### 3. source_evidence は証跡・素材層に徹する
source_evidence は transcript、OCR、timestamp、screenshot などの証跡を保持する層であり、**最終的な意味付け済み成果物そのものではない**。  
主役は 	raining_asset_spec であり、source_evidence はその根拠を支える。

---

## 踏襲しない方針の要約

### 1. YouTube分析中心の文脈は持ち込まない
VIS の競合分析・YouTube チャンネル分析・KPI 可視化などの用途は、本プロジェクトの目的とは異なる。  
VideoAsset Manualize は、教育・業務マニュアル資産化に集中する。

### 2. narrative レポート中心にはしない
VIS では narrative や report が目立つが、本プロジェクトでは manual / handbook / booklet が中心であり、narrative は補助情報に留める。

### 3. 分析用途向け JSON 設計は流用しない
VIS の JSON 設計は分析・営業・提案資料生成に最適化されている可能性が高い。  
本プロジェクトでは、**手順・注意点・FAQ・証跡の追跡可能性** を優先した構造を採用する。

---

## この方針から導く設計判断

この踏襲方針を採る場合、VideoAsset Manualize は次の設計判断を取る。

### 設計判断 1
	raining_asset_spec は、**AI 生成正本**として扱う。  
非 AI 経路は fallback またはテスト用途に留める。

### 設計判断 2
source_evidence は証跡保持のために残すが、**正本ではない**。  
主成果物は 	raining_asset_spec である。

### 設計判断 3
UI / CLI / PDF / HTML / Booklet の議論より先に、**高純度な 	raining_asset_spec をどう生成するか** を最優先で設計する。

---

## 今後の検討ポイント

今後は、この方針に基づいて以下を順に検討する。

1. 	raining_asset_spec を AI-first に再定義するか
2. xtract 処理を AI 標準経路に戻すか
3. non-LLM 経路を fallback / test-only に寄せるか
4. 	raining_asset_spec スキーマを、AI 再利用しやすい形に再設計するか
5. OpenAI / Gemini / 他 LLM Provider の採用方針をどうするか

---

## 暫定結論

VideoAsset Manualize が VIS から継承すべきなのは、  
**「AI が生成した高純度 structured JSON を中核資産とし、そこからすべての成果物を派生生成する」という設計思想**である。

逆に、YouTube 分析、競合分析、narrative レポート中心の成果物設計は踏襲対象ではない。

この方針により、VideoAsset Manualize は **ドメイン固有性を維持しつつ、VIS の強みである AI 中心のデータ資産化思想だけを継承する**。

---

## 参照元

- [video-insight-spec リポジトリ](https://github.com/nario0715masa0619-create/video-insight-spec)
- [VideoAsset Manualize README](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/README.md)
- [VideoAsset Manualize architecture.md](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/docs/architecture.md)
- [VideoAsset Manualize project_overview.md](https://github.com/nario0715masa0619-create/video-asset-manualize/blob/main/docs/project_overview.md)
