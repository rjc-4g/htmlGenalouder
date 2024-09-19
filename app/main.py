import gradio as gr
import datetime
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


# 履歴一覧生成処理
def create_html_table(model_list):
    html_content = '<table style="width:100%; table-layout: fixed;">'
    html_content += "<tr><th>入力音声</th><th>出力結果</th></tr>"
    for model in model_list:
        # HistoryDtoの属性に合わせて修正
        html_content += f'<tr><td style="word-wrap: break-word;">{model.prompt_ja}</td><td style="word-wrap: break-word;">{model.html}</td></tr>'
    html_content += "</table>"
    return html_content


# クリア処理
def clear_outputs():
    # HTML出力と音声入力をクリア
    return "", None


# 画面レイアウト、イベント定義
with gr.Blocks() as demo:
    gr.Label("音声を入力後(Record→Stop)、HTML生成ボタンを押してください！")

    # HTML出力画面
    with gr.Tab("HTML出力"):
        with gr.Row():
        # 音声入力エリア
            audio_data = gr.Audio(
                sources=["microphone"], type="filepath", max_length=10
            )
            # HTML出力エリア
            html_output = gr.HTML()
        # HTML生成ボタン
        html_button = gr.Button("HTML生成")
        # Clearボタン
        clear = gr.Button("クリア")
    # 履歴画面
    with gr.Tab("履歴"):
        model_list = history_service.get_all_histories()
        # 日付でソート（降順）、Noneは最後に
        sorted_model_list = sorted(
            model_list, 
            key=lambda model: model.created_at if model.created_at is not None else datetime.datetime.min, 
            reverse=True
        )
        for model in sorted_model_list:
            date_str = (
                model.created_at.strftime("%Y/%m/%d %H:%M")
                if model.created_at
                else "日付不明"
            )
            render_row(date_str, model.prompt_ja, model.html)

    def process_audio_to_html(audio):
        if audio is None:
            return "<strong>音声入力(Record→Stop)をしてからHTML生成ボタンを押してください！！</strong>"
        # 音声 → 文字 変換
        text = speech_to_text(audio)
        # 文字 → HTML 変換
        htmlText = get_html_from_chat_gpt(text)
        # HistoryDtoオブジェクトを生成して履歴データ登録
        history_service.register_history(HistoryDto.of(text, htmlText))
        return htmlText

    # HTML出力ボタンクリック時処理
    html_button.click(fn=process_audio_to_html, inputs=audio_data, outputs=html_output)

    # クリアボタンクリック時処理
    clear.click(
        fn=clear_outputs,
        inputs=[],
        outputs=[
            html_output,
            audio_data,
        ],
    )
    demo.queue()

if __name__ == "__main__":
    demo.launch()
