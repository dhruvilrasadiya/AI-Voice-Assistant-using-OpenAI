import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai 
import base64

def setup_openai_client(api_key):

    return openai.OpenAI(api_key=api_key)

def transcribe_audio(client, audio_path):
    with open(audio_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file= audio_file)
        return transcript.text
    
def fetch_ai_responce(client, input_text):
    messages = [{"role":"user", "content":input_text}]
    responce = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
    return responce.choices[0].message.content


def text_to_audio(client,text, audio_path):
    responce = client.audio.speech.create(model="tts-1", voice="nova" , input=text)
    responce.stream_to_file(audio_path)


def auto_play_audio(audio_file):
    with open(audio_file, 'rb') as audio_file:
        audio_bytes = audio_file.read()
    base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
    audio_html = f'<audio src="data:audio/mp3;base64,{base64_audio}" controls autoplay>'
    st.markdown(audio_html, unsafe_allow_html=True)
def main():

    st.sidebar.title("API KEY CONFIGRATION")
    api_key = st.sidebar.text_input("Enter you Open AI API key", type="password")

    st.title("Talk to me about anything...")

    if api_key:
        client = setup_openai_client(api_key)
        recorded_audio = audio_recorder()
        if recorded_audio:
            audio_file = "audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(recorded_audio)
            transcribed_text = transcribe_audio(client, audio_file)
            st.write("Transcribed text : ", transcribed_text)

            ai_responce = fetch_ai_responce(client, transcribed_text)
            responce_audio_file = "audio_response.mp3"
            text_to_audio(client, ai_responce, responce_audio_file)
            auto_play_audio(responce_audio_file)
            st.write("AI responce : ", ai_responce)


if __name__ == "__main__":
    main()