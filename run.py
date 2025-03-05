import logging
import os
import ssl

import picture_describer
import tts

os.environ['NUMPY_EXPERIMENTAL_ARRAY_FUNCTION'] = '0'
import gradio as gr
import message_constructor
# 增强日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def is_picture(file_name):
    return file_name.split(".")[-1].lower() in ["jpg", "png", "jpeg"]


class ChatHistory:

    def __init__(self):
        self.history = []

    def add_message(self, message):
        self.history.append(message)

    def get_history(self):
        return self.history


chat_history = ChatHistory()


def slow_echo(message, history):

    print(f"history: {history}")
    print(f"message: {message}")

    if not message:
        return "请输入有效的消息。"

    if message["files"]:
        if len(message["files"]) > 1 or not is_picture(message["files"][0]):
            return f"当前支持每次对话只上传一张图片（格式为jpg, png或jpeg）。" + \
                f"但是当前收到的文件名是：{message['files'][0]}"

        picture_path = message["files"][0]
        picture_description, message = picture_describer.describe_picture(
            picture_path,
            text=message["text"],
            history=chat_history.get_history())

        chat_history.add_message(message)
        chat_history.add_message(
            message_constructor.construct_text_message(picture_description))

        yield picture_description

        audio_path = tts.tts(picture_description)
        yield [gr.Audio(audio_path), picture_description]
        return

    #yield f"我听到你刚才说：{message['text']}"

    # Input is text
    reply_text, reply_message = picture_describer.reply_text(
        message["text"], chat_history.get_history())

    chat_history.add_message(
        message_constructor.construct_text_message(message["text"]))
    chat_history.add_message(reply_message)

    yield reply_text

    #print(f"history: {history}")


demo = gr.ChatInterface(
    slow_echo,
    title="图片描述",
    multimodal=True,
    type="messages",
    flagging_mode="manual",
    flagging_options=["Like", "Spam", "Inappropriate", "Other"],
    # save_history=True,
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        share=False,  # 关闭share可能会减少一些问题
        max_file_size="6mb",
        show_error=True,
        debug=False,  # 关闭debug模式，避免自动重载冲突
        favicon_path=None,
        # ssl_verify=False,
        quiet=False,
        # ssl_keyfile="/Users/guosaiwang/.keys/key.pem",
        # ssl_certfile="/Users/guosaiwang/.keys/cert.pem"
    )
