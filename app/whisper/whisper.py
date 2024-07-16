import openai


# 音声変換
def speech_to_text(input_audio):
    audio_file = open(input_audio, "rb")
    # OpenAPI 1.x以上でのAPIを使用
    response = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return response.text
