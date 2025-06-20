import requests

class BaseLLMClient:
    def __init__(self, api_key: str = '', base_url: str = ''):
        self.api_key = api_key
        self.base_url = base_url

    def translate(self, text: str, source_lang: str, target_lang: str, **kwargs):
        raise NotImplementedError

class OpenAIClient(BaseLLMClient):
    def translate(self, text: str, source_lang: str, target_lang: str, **kwargs):
        return "[暂不支持ChatGPT翻译]"

class DeepSeekClient(BaseLLMClient):
    def translate(self, text: str, source_lang: str, target_lang: str, **kwargs):
        if not self.api_key or not self.base_url:
            return '[DeepSeek配置缺失]'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        # 构造翻译prompt
        prompt = f"请将以下内容从{source_lang}翻译为{target_lang}：{text}"
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a translation assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return f'[DeepSeek翻译失败] {response.status_code}: {response.text}'
        except Exception as e:
            return f'[DeepSeek请求异常] {str(e)}'

class ClaudeClient(BaseLLMClient):
    def translate(self, text: str, source_lang: str, target_lang: str, **kwargs):
        return f"[Claude翻译]{text}"

class GoogleTranslateClient(BaseLLMClient):
    def translate(self, text: str, source_lang: str, target_lang: str, **kwargs):
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': source_lang if source_lang != 'auto' else 'auto',
            'tl': target_lang,
            'dt': 't',
            'q': text
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            try:
                result = response.json()
                return ''.join([item[0] for item in result[0] if item[0]])
            except Exception:
                return '[谷歌翻译异常]'
        else:
            return '[谷歌翻译失败]'
