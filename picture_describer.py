import base64
import os
import logging
from httpx import HTTPStatusError

from dotenv import load_dotenv
from openai import OpenAI

import message_constructor

load_dotenv(".env")

logger = logging.getLogger(__name__)


def _chat_completion(client, model, messages, service_type="Conversation"):
    """Calls OpenAI-styled chat API and handles error.
    
    Args:
        client: OpenAI client instance
        model: Model name to use
        messages: Message history and current message
        service_type: Error type description, used for error messages
        
    Returns:
        response_content: API response content or error message
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=512
        )
        return response.choices[0].message.content
    except HTTPStatusError as e:
        logger.error(f"API request failed: {str(e)}")
        return f"Sorry, the {service_type} service is temporarily unavailable. " \
            + f"(Error: {e.response.status_code} - {e.response.text})"
    except Exception as e:
        logger.error(f"Unknown error occurred while processing {service_type}: {str(e)}")
        return f"Sorry, there was a problem processing your {service_type}, please try again later."


def reply2picture(
    picture_path,
    text="Please describe the image in detail.",
    history=[],
    base_url=os.getenv("VISUAL_BASE_URL"),
    api_key=os.getenv("VISUAL_API_KEY"),
    model=os.getenv("VISUAL_MODEL")):

    """Calls the OpenAI client to describe the input image.

    Returns:
        picture_description: The description of the input image.
        message: The message to be added to the history.
    """

    # Read image and convert to base64
    with open(picture_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    client = OpenAI(api_key=api_key, base_url=base_url)
    message = message_constructor.construct_image_message(base64_image, text, role="user")
    
    response_content = _chat_completion(
        client, 
        model, 
        history + [message], 
        service_type="Image processing"
    )
    return response_content, message


def reply2text(text,
               history,
               base_url=os.getenv("VISUAL_BASE_URL"),
               api_key=os.getenv("VISUAL_API_KEY"),
               model=os.getenv("VISUAL_MODEL")):

    """Calls the OpenAI client to reply the input text.

    Returns:
        reply_text: The reply text.
        message: The message to be added to the history.
    """
    client = OpenAI(api_key=api_key, base_url=base_url)
    message = message_constructor.construct_text_message(text, role="user")

    response_content = _chat_completion(
        client, 
        model, 
        history + [message], 
        service_type="Conversation"
    )
    return response_content, message
