"""
Prompt Templates - LLM プロンプトテンプレート
"""


class PromptTemplates:
    """LLM プロンプトテンプレート集"""
    
    @staticmethod
    def summary_prompt(evidence_text: str) -> str:
        """Summary 生成用プロンプト"""
        return f"""以下は動画の文字起こしや画面テキスト(OCR)を含む抽出ログです。

{evidence_text}

このコンテンツの要約を作成してください。以下の形式で答えてください：
- 目的: このコンテンツの主な目的
- 成果物: 完了時の期待結果
- 対象者: 想定される対象ユーザー

簡潔に、日本語で答えてください。"""
    
    @staticmethod
    def instruction_prompt(evidence_text: str) -> str:
        """Step/Procedure 抽出用プロンプト"""
        
        return f"""以下は動画の文字起こしや画面テキスト(OCR)を含む抽出ログです。

{evidence_text}

このコンテンツから、以下の操作手順を抽出してください。

JSON 形式で以下の構造で答えてください：
{{
  "chapters": [
    {{
      "title": "章タイトル",
      "procedures": [
        {{
          "title": "手順タイトル",
          "steps": [
            {{
              "order": 1,
              "action": "実施する操作",
              "target_ui_element": "操作対象のUI要素（例：設定ボタン）",
              "expected_result": "期待される結果",
              "check_point": "操作完了の確認ポイント（例：画面遷移、メッセージ表示）",
              "evidence_refs": ["関連する証拠のID（ts-001, ocr-001 など複数可）"]
            }}
          ]
        }}
      ]
    }}
  ]
}}

各ステップは実行可能で、確認可能な粒度にしてください。"""
    
    @staticmethod
    def caution_prompt(evidence_text: str) -> str:
        """Caution/注意点 抽出用プロンプト"""
        return f"""以下は動画の文字起こしや画面テキスト(OCR)を含む抽出ログです。

{evidence_text}

このコンテンツで重要な注意点や警告、よくある間違いを抽出してください。

JSON 形式で以下の構造で答えてください：
{{
  "cautions": [
    "注意点1",
    "注意点2"
  ],
  "common_mistakes": [
    {{
      "mistake": "よくある間違い",
      "cause": "原因",
      "impact": "影響",
      "solution": "対策"
    }}
  ]
}}"""
    
    @staticmethod
    def faq_prompt(evidence_text: str, instructional_core: str) -> str:
        """FAQ 候補生成用プロンプト"""
        return f"""以下は動画の文字起こし・抽出ログと、抽出された手順です。

抽出ログ:
{evidence_text}

抽出された手順:
{instructional_core}

これらのコンテンツをもとに、よくある質問と回答を生成してください。

JSON 形式で以下の構造で答えてください：
{{
  "faqs": [
    {{
      "question": "質問内容",
      "answer": "回答内容",
      "priority": "high"
    }}
  ]
}}

3-5 個のよくある質問を生成してください。"""
