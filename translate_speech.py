import streamlit as st
from deep_translator import GoogleTranslator as gt
from gtts import gTTS
import gtts.lang
from pydub import AudioSegment as AS
import tempfile
import os
import speech_recognition as sr


st.set_page_config(page_title='Simply! Translate',
                   page_icon='translator-icon.png',
                   layout='wide',
                   initial_sidebar_state='expanded')

st.markdown(
    "<h1 style='text-align:center; color:grey;'>Speech To Speech Translator</h1>",
    unsafe_allow_html=True
)


c1, c3, c2 = st.columns(3)


def text_to_speech(text, accent="en"):

    supported_languages = gtts.lang.tts_langs()

    if accent not in supported_languages:

        st.error(f"Speech generation not supported for language code: {accent}")

        return None

    tts = gTTS(text=text, lang=accent)

    tts.save("output.mp3")

    return "output.mp3"

def transcribe(uploaded_file):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:

        file_path = temp_file.name

        temp_file.write(uploaded_file.read())

    c1.audio(uploaded_file, format="audio/wav")

    audio = AS.from_file(file_path)

    audio = audio.set_frame_rate(16000).set_channels(1)

    audio.export(file_path, format="wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:

        c2.write("Transcribing... Please wait")

        audio_data = recognizer.record(source)

        try:
            with c2.spinner("Transcribing audio..."):
                text = recognizer.recognize_google(audio_data)

                c2.success("Transcription Successful")

                c2.text_area("Transcribed Text:", text)

            return text

        except sr.UnknownValueError:

            c2.error("Couldn't understand the audio")

        except sr.RequestError:

            c2.error("Connection Failed")

    os.remove(file_path)
    return "error"

languages = {
    "afrikaans": "af",
    "albanian": "sq",
    "amharic": "am",
    "arabic": "ar",
    "armenian": "hy",
    "assamese": "as",
    "aymara": "ay",
    "azerbaijani": "az",
    "bambara": "bm",
    "basque": "eu",
    "belarusian": "be",
    "bengali": "bn",
    "bhojpuri": "bho",
    "bosnian": "bs",
    "bulgarian": "bg",
    "catalan": "ca",
    "cebuano": "ceb",
    "chichewa": "ny",
    "chinese (simplified)": "zh-cn",
    "chinese (traditional)": "zh-tw",
    "corsican": "co",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dhivehi": "dv",
    "dogri": "doi",
    "dutch": "nl",
    "english": "en",
    "esperanto": "eo",
    "estonian": "et",
    "ewe": "ee",
    "filipino": "tl",
    "finnish": "fi",
    "french": "fr",
    "frisian": "fy",
    "galician": "gl",
    "georgian": "ka",
    "german": "de",
    "greek": "el",
    "guarani": "gn",
    "gujarati": "gu",
    "haitian creole": "ht",
    "hausa": "ha",
    "hawaiian": "haw",
    "hebrew": "iw",
    "hindi": "hi",
    "hmong": "hmn",
    "hungarian": "hu",
    "icelandic": "is",
    "igbo": "ig",
    "ilocano": "ilo",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    "japanese": "ja",
    "javanese": "jw",
    "kannada": "kn",
    "kazakh": "kk",
    "khmer": "km",
    "kinyarwanda": "rw",
    "konkani": "gom",
    "korean": "ko",
    "krio": "kri",
    "kurdish (kurmanji)": "ku",
    "kurdish (sorani)": "ckb",
    "kyrgyz": "ky",
    "lao": "lo",
    "latin": "la",
    "latvian": "lv",
    "lingala": "ln",
    "lithuanian": "lt",
    "luganda": "lg",
    "luxembourgish": "lb",
    "macedonian": "mk",
    "maithili": "mai",
    "malagasy": "mg",
    "malay": "ms",
    "malayalam": "ml",
    "maltese": "mt",
    "maori": "mi",
    "marathi": "mr",
    "meiteilon (manipuri)": "mni-mtei",
    "mizo": "lus",
    "mongolian": "mn",
    "myanmar": "my",
    "nepali": "ne",
    "norwegian": "no",
    "odia (oriya)": "or",
    "oromo": "om",
    "pashto": "ps",
    "persian": "fa",
    "polish": "pl",
    "portuguese": "pt",
    "punjabi": "pa",
    "quechua": "qu",
    "romanian": "ro",
    "russian": "ru",
    "samoan": "sm",
    "sanskrit": "sa",
    "scots gaelic": "gd",
    "sepedi": "nso",
    "serbian": "sr",
    "sesotho": "st",
    "shona": "sn",
    "sindhi": "sd",
    "sinhala": "si",
    "slovak": "sk",
    "slovenian": "sl",
    "somali": "so",
    "spanish": "es",
    "sundanese": "su",
    "swahili": "sw",
    "swedish": "sv",
    "tajik": "tg",
    "tamil": "ta",
    "tatar": "tt",
    "telugu": "te",
    "thai": "th",
    "tigrinya": "ti",
    "tsonga": "ts",
    "turkish": "tr",
    "turkmen": "tk",
    "twi": "ak",
    "ukrainian": "uk",
    "urdu": "ur",
    "uyghur": "ug",
    "uzbek": "uz",
    "vietnamese": "vi",
    "welsh": "cy",
    "xhosa": "xh",
    "yiddish": "yi",
    "yoruba": "yo",
    "zulu": "zu"
}

input_text = c1.selectbox("Choose Input Format", ("Text", "Audio File", "MIC"))

text = ""
if input_text == "Text":
    text = c1.text_area("Enter Text: ")

elif input_text == "MIC":
    uploaded_file = c1.audio_input("Record a voice message")
    if uploaded_file:
        if c2.button("Transcribe Audio"):
            text = transcribe(uploaded_file)

else:
    uploaded_file = c1.file_uploader(
        "Upload an audio file",
        type=["mp4", "wav", "m4a"]
    )
    if uploaded_file:
        if c2.button("Transcribe Audio"):
            text = transcribe(uploaded_file)

option = c1.selectbox("Output Language:", 
                      ['afrikaans',
 'albanian',
 'amharic',
 'arabic',
 'armenian',
 'assamese',
 'aymara',
 'azerbaijani',
 'bambara',
 'basque',
 'belarusian',
 'bengali',
 'bhojpuri',
 'bosnian',
 'bulgarian',
 'catalan',
 'cebuano',
 'chichewa',
 'chinese (simplified)',
 'chinese (traditional)',
 'corsican',
 'croatian',
 'czech',
 'danish',
 'dhivehi',
 'dogri',
 'dutch',
 'english',
 'esperanto',
 'estonian',
 'ewe',
 'filipino',
 'finnish',
 'french',
 'frisian',
 'galician',
 'georgian',
 'german',
 'greek',
 'guarani',
 'gujarati',
 'haitian creole',
 'hausa',
 'hawaiian',
 'hebrew',
 'hindi',
 'hmong',
 'hungarian',
 'icelandic',
 'igbo',
 'ilocano',
 'indonesian',
 'irish',
 'italian',
 'japanese',
 'javanese',
 'kannada',
 'kazakh',
 'khmer',
 'kinyarwanda',
 'konkani',
 'korean',
 'krio',
 'kurdish (kurmanji)',
 'kurdish (sorani)',
 'kyrgyz',
 'lao',
 'latin',
 'latvian',
 'lingala',
 'lithuanian',
 'luganda',
 'luxembourgish',
 'macedonian',
 'maithili',
 'malagasy',
 'malay',
 'malayalam',
 'maltese',
 'maori',
 'marathi',
 'meiteilon (manipuri)',
 'mizo',
 'mongolian',
 'myanmar',
 'nepali',
 'norwegian',
 'odia (oriya)',
 'oromo',
 'pashto',
 'persian',
 'polish',
 'portuguese',
 'punjabi',
 'quechua',
 'romanian',
 'russian',
 'samoan',
 'sanskrit',
 'scots gaelic',
 'sepedi',
 'serbian',
 'sesotho',
 'shona',
 'sindhi',
 'sinhala',
 'slovak',
 'slovenian',
 'somali',
 'spanish',
 'sundanese',
 'swahili',
 'swedish',
 'tajik',
 'tamil',
 'tatar',
 'telugu',
 'thai',
 'tigrinya',
 'tsonga',
 'turkish',
 'turkmen',
 'twi',
 'ukrainian',
 'urdu',
 'uyghur',
 'uzbek',
 'vietnamese',
 'welsh',
 'xhosa',
 'yiddish',
 'yoruba',
 'zulu'])

value = languages[option]

if c2.button("Translate Text"):
    if input_text != "input_text":
        text = transcribe(uploaded_file)

    if text=="":
        c2.warning("Please **enter text...**")
    else:
        translated_text = gt(target = value).translate(text)
        c2.title("Translated Text is: ")
        c2.write(translated_text)
        c2.success("translation is successful...")

if c2.button("Convert to Speech"):
    if input_text != "Text":
        text = transcribe(uploaded_file)
    
    if text:
        translated_text = gt(target = value).translate(text)
    
        if translated_text.strip():
            audio_file = text_to_speech(translated_text, value)
            if audio_file:
                c2.audio(audio_file, format="audio/mp3")





