"""Sync variant of the example for generating audio with a predefined voice"""

import edge_tts


def test_tts():
    """Test the TTS function"""
    text = "Hello World!"
    output_file = "test.mp3"
    tts(text, output_file=output_file)


def tts(text, voice="en-US-EmmaNeural", output_file="output.mp3"):
    """TTS function"""
    communicate = edge_tts.Communicate(text, voice)
    communicate.save_sync(output_file)

    return output_file


if __name__ == "__main__":
    test_tts()
