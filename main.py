import os
import uuid
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.play import play
from elevenlabs.client import ElevenLabs
import streamlit as st


def text_to_speech_file(text: str, elevenlabs, settings_dict) -> str:

    # Calling the text_to_speech conversion API with detailed parameters
    response = elevenlabs.text_to_speech.convert(
        voice_id="TbxyDreNOTN8JUWUBMkl",  # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",  # use the turbo model for low latency
        # Optional voice settings that allow you to customize the output
        voice_settings=VoiceSettings(
            stability=settings_dict["stability"],
            similarity_boost=settings_dict["similarity_boost"],
            style=settings_dict["style"],
            use_speaker_boost=True,
            speed=settings_dict["speed"],
        ),
    )

    audio_bytes = b"".join(response)

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    # with open(save_file_path, "wb") as f:
    #     f.write(audio_bytes)

    audio_stream = BytesIO()
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)
    audio_stream.seek(0)
    
    st.audio(audio_bytes, autoplay=True)

    # return save_file_path

    # Try to play the audio
    # try:
    #    play(audio_bytes)
    # except Exception as e:
    #     print(f"Error playing audio with elevenlabs.play: {e}")
    #     print("Falling back to system default player.")
    #     if os.name == 'nt': # Windows
    #         os.startfile(save_file_path)

def main():
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    elevenlabs = ElevenLabs(
        api_key=ELEVENLABS_API_KEY,
    )

    st.set_page_config(page_title="ElevenLabs TTS Demo", layout="centered")
    st.title("ElevenLabs Text to Speech Demo")
    input_text = st.text_input("Enter text to convert to speech:", key="input_text")

    with st.sidebar:
        st.header("Settings:")
        speed = st.slider("Speed", 0.7, 1.2, 0.8, 0.1)
        stability = st.slider("Stability", 0.0, 1.0, 0.7, 0.1)
        similarity_boost = st.slider("Similarity Boost", 0.0, 1.0, 0.6, 0.1)
        style = st.slider("Style", 0.0, 1.0, 0.1, 0.1)
    
    settings_dict = {
        "speed": speed,
        "stability": stability,
        "similarity_boost": similarity_boost,
        "style": style,
    }


    if st.button("Convert to Speech"):
        if input_text:
            text_to_speech_file(input_text, elevenlabs, settings_dict)
        else:
            st.warning("Please enter some text to convert.")
    
    left_col, right_col = st.columns(2)
    with left_col:
        st.title("Food and Drink")
        if st.button("Coffee Please"):
            coffee_text = "I'd like a cup of coffee, please."
            text_to_speech_file(coffee_text, elevenlabs, settings_dict)
        if st.button("Tea Please"):
            tea_text = "I'd like a cup of tea, please."
            text_to_speech_file(tea_text, elevenlabs, settings_dict)
    with right_col:
        st.title("Greetings")
        if st.button("Good morning!"):
            hello_text = "Good morning!"
            text_to_speech_file(hello_text, elevenlabs, settings_dict)
        if st.button("How are you today!"):
            goodbye_text = "How are you today?"
            text_to_speech_file(goodbye_text, elevenlabs, settings_dict)

if __name__ == "__main__":
    main()
