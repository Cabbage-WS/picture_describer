import base64
import os

from dotenv import load_dotenv
from openai import OpenAI

import message_constructor

load_dotenv(".env")


def describe_picture(
    picture_path,
    text="What is in this image? Please describe the image in detail.",
    history=[],
    base_url=os.getenv("VISUAL_BASE_URL"),
    api_key=os.getenv("VISUAL_API_KEY"),
    model=os.getenv("VISUAL_MODEL")):
    """
    使用 OpenAI 客户端库调用 SiliconFlow 视觉大模型描述图片
    """
    # 读取图片并转换为 base64
    with open(picture_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    client = OpenAI(api_key=api_key, base_url=base_url)

    message = message_constructor.construct_image_message(base64_image, text)

    response = client.chat.completions.create(model=model,
                                              messages=history + [message],
                                              max_tokens=512)

    return response.choices[0].message.content, message


def reply_text(text,
               history,
               base_url=os.getenv("VISUAL_BASE_URL"),
               api_key=os.getenv("VISUAL_API_KEY"),
               model=os.getenv("VISUAL_MODEL")):
    client = OpenAI(api_key=api_key, base_url=base_url)

    message = message_constructor.construct_text_message(text)

    response = client.chat.completions.create(model=model,
                                              messages=history + [message],
                                              max_tokens=512)

    return response.choices[0].message.content, message
