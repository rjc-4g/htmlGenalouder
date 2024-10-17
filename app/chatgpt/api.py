import os
from openai import OpenAI
from dotenv import load_dotenv
import deepl

load_dotenv()
translator = deepl.Translator(os.environ.get("DEEPL_API_KEY"))
client = OpenAI( api_key = os.environ.get("OPENAI_API_KEY"))

model_name = "gpt-4o"
source_lang = "JA"
target_lang = "EN-US"

def get_html_from_chat_gpt(request):

    # system prompt
    system_prompt1 = "Webブラウザで表示したい画面構成を指定した要求がされます。\n"
    system_prompt2 = "使用するブラウザはGoogle Chromeです。\n"
    system_prompt3 = "要求を満たす画面構成をHTML形式、かつHTMLコードの部分のみ返してください。\n"
    system_prompt = system_prompt1 + system_prompt2 + system_prompt3

    # user prompt
    prompt_user_request = request

    # 翻訳（日本語→英語）
    system_prompt_en = translator.translate_text(system_prompt, source_lang=source_lang, target_lang=target_lang).text
    prompt_user_request_en = translator.translate_text(prompt_user_request, source_lang=source_lang, target_lang=target_lang).text

    # APIリクエスト
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt_en},
            {"role": "user", "content": prompt_user_request_en}
        ],
        n           = 1,                # 返答数
        temperature = 0,                # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
    )

    # 不要なレスポンスを加工
    response_all = response.choices[0].message.content
    response_lstrip = response_all.lstrip('```html\n')
    response_rstrip = response_lstrip.rstrip('```\n')
    
    return response_rstrip
