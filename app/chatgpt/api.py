import openai
from openai import OpenAI
import deepl

client = OpenAI( api_key = "" )
model_name = "gpt-3.5-turbo"

DEEPL_API_KEY = ""
source_lang = "JA"
target_lang = "EN-US"
translator = deepl.Translator(DEEPL_API_KEY)

def get_html_from_chat_gpt(request):

    print(request)

    # syatem prompt
    system_prompt1 = "Webブラウザで表示したい画面構成を指定した要求がされます。\n"
    system_prompt2 = "使用するブラウザはGoogle Chromeです。\n"
    system_prompt3 = "要求を満たす画面構成をHTML形式で返してください。\n"
    system_prompt = system_prompt1 + system_prompt2 + system_prompt3

    #user prompt
    prompt_user_request = request.data
    #prompt_user_request = "画面中央にボタン1つ"

    #output = translator.translate_text(system_prompt, target_lang=target_lang)
    #print("翻訳結果\n" + output.text)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": translator.translate_text(system_prompt, source_lang=source_lang, target_lang=target_lang).text},
            {"role": "user", "content": translator.translate_text(prompt_user_request, source_lang=source_lang, target_lang=target_lang).text}
        ],
        n           = 1,                # 返答数
        temperature = 0,                # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
    )
    response_all = response.choices[0].message.content
    response_a = response_all[7:]
    response_b = response_a[:-3]
    return response_all

#html_res = createPrompt('s')
#print(html_res)


