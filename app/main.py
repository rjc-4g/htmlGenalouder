import gradio as gr
from whisper.whisper import speech_to_text
from chatgpt.api import get_html_from_chat_gpt
from history.dto import HistoryDto
from history.service import HistoryService

history_service = HistoryService()


# HTML出力結果構築
def render_row(date, input_text, output_html):
    with gr.Accordion(date, open=False):
        gr.Textbox(value=input_text, label="インプット内容", show_copy_button=True)
        gr.HTML(value=output_html, label="結果としてのHTML")
        gr.Textbox(
            value=output_html, label="HTML結果（テキスト）", show_copy_button=True
        )


# クリア処理
def clear_outputs():
    return "", None  # 空の文字列とNoneのファイルパスを返す


# 履歴タブの更新処理
def update_history_tab():
    with gr.Tab("履歴"):
        model_list = history_service.get_all_histories(reverse_request_id=True)
        for model in model_list:
            date_str = model.created_at.strftime("%Y/%m/%d %H:%M")
            render_row(date_str, model.prompt_ja, model.html)


# HTML生成処理
def process_audio_to_html(audio):
    if audio is None:
        return "<strong>音声入力(Record→Stop)をしてからHTML生成ボタンを押してください！！</strong>"
    text = speech_to_text(audio)
    html_text = get_html_from_chat_gpt(text)
    history_service.register_history(HistoryDto.of(text, html_text))
    return html_text


# 画面レイアウト、イベント定義
with gr.Blocks() as demo:
    gr.Label("音声を入力後(Record→Stop)、HTML生成ボタンを押してください！")

    # HTML出力画面
    with gr.Tab("HTML出力"):
        with gr.Row():
            audio_data = gr.Audio(
                sources=["microphone"], type="filepath", max_length=10
            )
            html_output = gr.HTML()
        html_button = gr.Button("HTML生成")
        clear = gr.Button("クリア")

    # HTML出力ボタンクリック時処理
    html_button.click(
        # HTML生成処理後、最新の履歴処理を取得
        fn=lambda x: [process_audio_to_html(x), update_history_tab()],
        inputs=audio_data,
        outputs=html_output
    )
    # クリアボタンクリック時処理
    clear.click(
        fn=clear_outputs,
        inputs=[],
        outputs=[html_output, audio_data]
    )
    # 初期履歴表示
    update_history_tab()

demo.queue()

if __name__ == "__main__":
    demo.launch()
