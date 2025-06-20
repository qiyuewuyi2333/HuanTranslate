from api.llm_clients import GoogleTranslateClient, DeepSeekClient, OpenAIClient
from config.database import get_db

def get_provider_config(provider: str):
    db = get_db()
    row = db.execute('SELECT api_key, base_url FROM user_config WHERE provider = ? ORDER BY id DESC LIMIT 1', (provider,)).fetchone()
    if row:
        return row['api_key'], row['base_url']
    return '', ''

class TranslatorService:
    def __init__(self):
        pass

    def get_client(self, provider: str):
        api_key, base_url = get_provider_config(provider)
        if provider == 'google':
            return GoogleTranslateClient()
        elif provider == 'deepseek':
            return DeepSeekClient(api_key, base_url)
        elif provider == 'openai':
            return OpenAIClient(api_key, base_url)
        else:
            return GoogleTranslateClient()

    def translate_text(self, text: str, source_lang: str, target_lang: str, provider: str = 'google') -> str:
        client = self.get_client(provider)
        return client.translate(text, source_lang, target_lang)

    def split_long_text(self, text: str, max_length: int = 2000):
        # 简单分段，实际可优化
        return [text[i:i+max_length] for i in range(0, len(text), max_length)]

    def detect_language(self, text: str) -> str:
        # 伪代码，实际可用langdetect等库
        return 'zh' if '\u4e00' <= text[0] <= '\u9fff' else 'en'
