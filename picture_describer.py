import base64
import os
import logging
from httpx import HTTPStatusError

from dotenv import load_dotenv
from openai import OpenAI

import message_constructor

load_dotenv(".env")

logger = logging.getLogger(__name__)


def describe_picture(
    picture_path,
    text="Please describe the image in detail.",
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

    message = message_constructor.construct_image_message(base64_image, text, role="user")
    
    try:
        response = client.chat.completions.create(model=model,
                                                messages=history + [message],
                                                max_tokens=512)
        return response.choices[0].message.content, message
    except HTTPStatusError as e:
        logger.error(f"API请求失败: {str(e)}")
        error_message = f"抱歉，图像处理服务暂时不可用 (错误: {e.response.status_code} - {e.response.text})"
        return error_message, message
    except Exception as e:
        logger.error(f"处理图像时发生未知错误: {str(e)}")
        return "抱歉，处理您的图像时出现了问题，请稍后再试。", message


def reply_text(text,
               history,
               base_url=os.getenv("VISUAL_BASE_URL"),
               api_key=os.getenv("VISUAL_API_KEY"),
               model=os.getenv("VISUAL_MODEL")):
    client = OpenAI(api_key=api_key, base_url=base_url)

    message = message_constructor.construct_text_message(text, role="user")

    try:
        response = client.chat.completions.create(model=model,
                                                messages=history + [message],
                                                max_tokens=512)
        return response.choices[0].message.content, message
    except HTTPStatusError as e:
        logger.error(f"API请求失败: {str(e)}")
        error_message = f"抱歉，对话服务暂时不可用 (错误: {e.response.status_code})"
        return error_message, message
    except Exception as e:
        logger.error(f"处理文本时发生未知错误: {str(e)}")
        return "抱歉，处理您的消息时出现了问题，请稍后再试。", message
