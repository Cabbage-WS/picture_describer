import base64
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(".env")


def describe_picture(
    picture_path,
    text="What is in this image? Please describe the image in detail.",
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

    response = client.chat.completions.create(
        model=model,
        messages=[{
            #     "role":
            #         "system",
            #     "content":
            #         "You are a helpful assistant that can describe images in detail."
            # }, {
            "role":
                "user",
            "content": [{
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "low"
                }
            }, {
                "type": "text",
                "text": text,
            }]
        }],
        max_tokens=512)

    return response.choices[0].message.content
