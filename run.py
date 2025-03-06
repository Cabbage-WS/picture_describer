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
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def is_picture(file_name):
    return file_name.split(".")[-1].lower() in ["jpg", "png", "jpeg"]


class ChatHistory:

    def __init__(self):
        self.history = []
        SYSTEM_PROMPT = "Please use English in the conversation."
        self.add_message(message_constructor.construct_text_message(text=SYSTEM_PROMPT, role="assistant"))

    def add_message(self, message):
        self.history.append(message)

    def get_history(self):
        return self.history


chat_history = ChatHistory()


def get_response(message, history):

    logging.debug(f"history: {history}")
    logging.debug(f"message: {message}")

    if not message:
        return "The message is empty."

    # Case 1: The user uploads a picture.
    if message["files"]:
        if len(message["files"]) > 1 or not is_picture(message["files"][0]):
            return f"I can only receive one picture (jpg, png, or jpeg) each time. " + \
                f"But the file name is: {message['files'][0]}"

        picture_path = message["files"][0]
        picture_description, message = picture_describer.reply2picture(
            picture_path,
            text=message["text"],
            history=chat_history.get_history())

        chat_history.add_message(message)
        chat_history.add_message(
            message_constructor.construct_text_message(picture_description, role="assistant"))

        yield picture_description

        audio_path = tts.tts(picture_description)
        yield [gr.Audio(audio_path), picture_description]
        return

    #yield f"我听到你刚才说：{message['text']}"

    # Case 2: The user sends a text message.
    reply_text, reply_message = picture_describer.reply2text(
        message["text"], chat_history.get_history())

    chat_history.add_message(
        message_constructor.construct_text_message(message["text"]))
    chat_history.add_message(reply_message)

    yield reply_text
    audio_path = tts.tts(reply_text)
    yield [gr.Audio(audio_path), reply_text]

    return


demo = gr.ChatInterface(
    get_response,
    title="看图说话",
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
