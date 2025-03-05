def construct_text_message(text, role="user"):
    return {
        "role": role,
        "content": [{
            "type": "text",
            "text": text,
        }]
    }


def construct_image_message(base64_image, text="", role="user"):
    return {
        "role":
            role,
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
    }
