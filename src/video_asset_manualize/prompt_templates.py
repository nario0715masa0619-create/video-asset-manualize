"""
Prompt Templates - LLM プロンプトテンプレート
"""


class PromptTemplates:
    """LLM プロンプトテンプレート集"""
    
    @staticmethod
    def summary_prompt(transcript: str) -> str:
        """Summary 生成用プロンプト"""
        return f"""以下は動画の文字起こしです。

{transcript}

このコンテンツの要約を作成してください。以下の形式で答えてください：
- 目的: このコンテンツの主な目的
- 成果物: 完了時の期待結果
- 対象者: 想定される対象ユーザー

簡潔に、日本語で答えてください。"""
    
    @staticmethod
    def instruction_prompt(transcript: str, ocr_text: str = "") -> str:
        """Step/Procedure 抽出用プロンプト"""
        ocr_context = f"OCR テキスト:\n{ocr_text}\n\n" if ocr_text else ""
        
        return f"""以下は動画の文字起こしです。

{transcript}

{ocr_context}このコンテンツから、以下の操作手順を抽出してください。

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
              "expected_result": "期待される結果"
            }}
          ]
        }}
      ]
    }}
  ]
}}

各ステップは実行可能で、確認可能な粒度にしてください。"""
    
    @staticmethod
    def caution_prompt(transcript: str) -> str:
        """Caution/注意点 抽出用プロンプト"""
        return f"""以下は動画の文字起こしです。

{transcript}

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
    def faq_prompt(transcript: str, instructional_core: str) -> str:
        """FAQ 候補生成用プロンプト"""
        return f"""以下は動画の文字起こしと抽出された手順です。

文字起こし:
{transcript}

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
