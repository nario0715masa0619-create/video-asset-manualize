"""
Phase 6 provider_factory 拡張スクリプト
"""

from pathlib import Path

factory_file = Path("src/video_asset_manualize/provider_factory.py")
content = factory_file.read_text(encoding='utf-8')

# LLM プロバイダー作成メソッドを追加
if "create_llm_provider" not in content:
    llm_method = '''
    @staticmethod
    def create_llm_provider(provider_type='dummy', **kwargs):
        """LLM プロバイダーを作成"""
        if provider_type == 'openai':
            try:
                from .openai_llm_provider import OpenAILLMProvider
                api_key = kwargs.get('api_key') or os.getenv('OPENAI_API_KEY')
                model = kwargs.get('model', 'gpt-3.5-turbo')
                if not api_key:
                    raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
                return OpenAILLMProvider(api_key=api_key, model=model)
            except ImportError:
                raise ImportError("OpenAI library not found. Install with: pip install openai")
        else:
            from .llm_provider import DummyLLMProvider
            return DummyLLMProvider()
'''
    
    # クラスの最後（最後の method の後）に追加
    if "class ProviderFactory:" in content:
        # 最後の @staticmethod の後に追加
        insertion_point = content.rfind("        return")
        if insertion_point != -1:
            # 次の改行を見つける
            insertion_point = content.find("\n", insertion_point) + 1
            content = content[:insertion_point] + llm_method + "\n" + content[insertion_point:]
    
    factory_file.write_text(content, encoding='utf-8')
    print("✓ Updated: src/video_asset_manualize/provider_factory.py (LLM provider method added)")
else:
    print("⚠ create_llm_provider already present")

print("\n✅ provider_factory.py の LLM プロバイダー機能が追加されました")
