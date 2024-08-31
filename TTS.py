import asyncio
import edge_tts
import streamlit as st
import io
import base64
from googletrans import Translator
from gtts import gTTS
# Set page configuration
st.set_page_config(page_title="AI Voice Generator", page_icon="🎙️", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: black;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextArea>div>div>textarea {
        background-color:black;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .stSelectbox>div>div>select {
        background-color: #ffffff;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Available voices grouped by language
VOICE_OPTIONS = {
    "English": {
        "en-AU-NatashaNeural": "Natasha (Australia)",
        "en-CA-LiamNeural": "Liam (Canada)",
        "en-GB-LibbyNeural": "Libby (UK)",
        "en-GB-RyanNeural": "Ryan (UK)",
        "en-IE-ConnorNeural": "Connor (Ireland)",
        "en-IN-NeerjaNeural": "Neerja (India)",
        "en-IN-PrabhatNeural": "Prabhat (India)",
        "en-NZ-MitchellNeural": "Mitchell (New Zealand)",
        "en-US-AriaNeural": "Aria (US)",
        "en-US-ChristopherNeural": "Christopher (US)",
        "en-US-JennyNeural": "Jenny (US)",
        "en-ZA-LeonNeural": "Leon (South Africa)"
    },
    "French": {
        "fr-FR-DeniseNeural": "Denise (France)",
        "fr-CA-SylvieNeural": "Sylvie (Canada)"
    },
    "Spanish": {
        "es-ES-AlvaroNeural": "Alvaro (Spain)",
        "es-MX-DaliaNeural": "Dalia (Mexico)"
    },
    "German": {
        "de-DE-KatjaNeural": "Katja (Germany)",
        "de-AT-JonasNeural": "Jonas (Austria)"
    },
    "Italian": {
        "it-IT-ElsaNeural": "Elsa (Italy)",
        "it-IT-IsabellaNeural": "Isabella (Italy)"
    },
    "Japanese": {
        "ja-JP-NanamiNeural": "Nanami (Japan)",
        "ja-JP-KeitaNeural": "Keita (Japan)"
    },
    "Korean": {
        "ko-KR-SunHiNeural": "Sun-Hi (Korea)",
        "ko-KR-InJoonNeural": "In-Joon (Korea)"
    },
    "Portuguese": {
        "pt-BR-FranciscaNeural": "Francisca (Brazil)",
        "pt-PT-RaquelNeural": "Raquel (Portugal)"
    },
    "Russian": {
        "ru-RU-SvetlanaNeural": "Svetlana (Russia)",
        "ru-RU-DmitryNeural": "Dmitry (Russia)"
    },
    "Chinese": {
        "zh-CN-XiaoxiaoNeural": "Xiaoxiao (Mainland China)",
        "zh-TW-HsiaoChenNeural": "Hsiao-Chen (Taiwan)"
    }
}

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

async def text_to_speech(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.write(chunk["data"])
    return audio_data.getvalue()

def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    return href

# Sidebar for app mode selection
app_mode = st.sidebar.selectbox("Choose the app mode", ["Text to Speech", "About"])

if app_mode == "Text to Speech":
    st.title("🎙️ AI Voice Generator")
    st.markdown("Transform your text into lifelike speech with our cutting-edge AI technology!")

    # Text input with character count
    text_input = st.text_area("Enter your text here:", height=150)
    st.write(f"Character count: {len(text_input)}")

    # Language selection
    languages = list(VOICE_OPTIONS.keys())
    sort_order = st.radio("Sort languages:", ("Alphabetical", "Most Popular"))
    if sort_order == "Most Popular":
        # You can customize this order based on actual usage statistics
        languages = ["English", "Spanish", "French", "German", "Chinese"] + [lang for lang in languages if lang not in ["English", "Spanish", "French", "German", "Chinese"]]
    else:
        languages.sort()

    selected_language = st.selectbox("Choose a language:", languages)

    # Voice selection within the chosen language
    voices = VOICE_OPTIONS[selected_language]
    voice_search = st.text_input("Search for a voice:", "")
    filtered_voices = {k: v for k, v in voices.items() if voice_search.lower() in v.lower()}
    selected_voice = st.selectbox("Choose a voice:", list(filtered_voices.values()), format_func=lambda x: x)
    selected_voice_key = [k for k, v in voices.items() if v == selected_voice][0]

    # Generate speech button
    if st.button("🔊 Generate Speech"):
        if text_input:
            with st.spinner("🎵 Generating audio... Please wait."):
                audio_data = asyncio.run(text_to_speech(text_input, selected_voice_key))
            
            # Display success message
            st.success("🎉 Audio generated successfully!")
            
            # Audio player
            st.audio(audio_data, format="audio/mp3")
            
            # Download button
            st.markdown(get_binary_file_downloader_html(audio_data, 'generated_speech.mp3'), unsafe_allow_html=True)
            
            # Display transcription
            with st.expander("📝 View Transcription"):
                st.write(text_input)
        else:
            st.warning("⚠️ Please enter some text to convert to speech.")

elif app_mode == "About":
    st.title("About AI Voice Generator")
    st.markdown("""
    ## Welcome to AI Voice Generator!

    This application uses cutting-edge AI technology to convert text into natural-sounding speech. 
    With a variety of voices in multiple languages to choose from, you can bring your words to life in seconds.

    ### Features:
    - Multiple AI voices from different regions and languages
    - Real-time audio generation
    - Easy-to-use interface
    - Download option for generated audio
    - Language and voice sorting options

    ### How to use:
    1. Enter your text in the text area
    2. Choose a language
    3. Select a voice from the chosen language
    4. Click 'Generate Speech' to create your audio
    5. Play the audio directly in your browser or download it for later use

    We hope you enjoy using our AI Voice Generator!

    For any questions or feedback, please contact us at support@aivoicegenerator.com
    """)

# Footer
st.markdown("---")
st.markdown("Developed By  ❤️ Sandeep Gudisa")