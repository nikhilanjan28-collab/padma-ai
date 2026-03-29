import streamlit as st
import os, PyPDF2, groq, datetime, requests
from gtts import gTTS
import base64
from io import BytesIO
from duckduckgo_search import DDGS

# 1. యాప్ సెట్టింగ్స్ & డిజైన్
st.set_page_config(page_title="Padma AI Global Astrology", layout="wide", page_icon="🔮")

st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin: 5px; background-color: #f1f3f4; border-left: 5px solid #0047AB; }
    div.stButton > button { background-color: #0047AB; color: white; border-radius: 10px; height: 50px; font-weight: bold; }
    </style>""", unsafe_allow_html=True)

# వాయిస్ ఫంక్షన్
def speak_now(text):
    try:
        tts = gTTS(text=text, lang='te')
        tts.save("reply.mp3")
        with open("reply.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio controls autoplay style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
    except: pass

# ఆన్లైన్ సెర్చ్ (తాజా గ్రహ స్థితి కోసం)
def search_online(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(f"astrology prediction {query}", max_results=2)]
            return "\n".join(results)
    except: return ""

# 2. నీ 6 పుస్తకాల కనెక్షన్ (IDs అప్‌డేట్ చేశాను బావా)
BOOK_IDS = {
    "Book 1": "1CSmVy8uZ-uOOJ0BIJhfIUJWn4XoZUu__",
    "Book 2": "1DkZiBSBXR-3iJpkqRjC_nU0uK6Of0QxM",
    "Book 3": "1Nm6gs0gVUBLr7d-hnpw8Ou5qSuXM-gIr",
    "Book 4": "1Rq2OV_d_ZUs22Kqdgi1qJBuWH1ivbzT0",
    "Book 5": "1S7w0VGj2be5D8ZAcIPO9i_45RA8g4SsX",
    "Book 6": "1gPQQDpz7KAUty4j6JYrFWZolH_G2egPY"
}

@st.cache_data
def load_all_books():
    all_text = ""
    for name, fid in BOOK_IDS.items():
        try:
            url = f"https://drive.google.com/uc?export=download&id={fid}"
            res = requests.get(url)
            pdf = PyPDF2.PdfReader(BytesIO(res.content))
            # ప్రతి పుస్తకం నుండి ముఖ్యమైన 20 పేజీలు తీసుకుంటున్నాం
            for page in pdf.pages[:20]:
                all_text += page.extract_text()
        except: continue
    return all_text

# రాశి ఫోటోలు
ZODIAC_IMAGES = {
    'మేషం ♈': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/aries.png',
    'వృషభం ♉': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/taurus.png',
    'మిథునం ♊': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/gemini.png',
    'కర్కాటకం ♋': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/cancer.png',
    'సింహం ♌': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/leo.png',
    'కన్య ♍': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/virgo.png',
    'తుల ♎': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/libra.png',
    'వృశ్చికం ♏': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/scorpio.png',
    'ధనుస్సు ♐': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/sagittarius.png',
    'మకరం ♑': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/capricorn.png',
    'కుంభం ♒': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/aquarius.png',
    'మీనం ♓': 'https://raw.githubusercontent.com/amit-bvp/astro-images/main/pisces.png'
}

# 3. యూజర్ ఇంటర్ఫేస్
st.title("🔮 పద్మ ఏఐ - సంపూర్ణ జాతక వేదిక")
st.caption("6 పురాతన గ్రంథాలు మరియు ఆన్లైన్ సెర్చ్ ఆధారంగా మీ జీవిత విశ్లేషణ")

with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        u_name = st.text_input("మీ పేరు:")
        u_dob = st.date_input("పుట్టిన తేదీ:", min_value=datetime.date(1900, 1, 1))
    with c3:
        zod = st.selectbox("మీ రాశిని ఎంచుకోండి:", list(ZODIAC_IMAGES.keys()))
        if zod: st.image(ZODIAC_IMAGES[zod], width=100)

st.divider()

# చాట్ హిస్టరీ
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "నమస్కారం అండి! మీ వివరాలు ఇచ్చారు కదా, మీ జీవితం గురించి ఏదైనా సందేహం ఉంటే ఇక్కడ అడగండి."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ప్రశ్న అడిగినప్పుడు
if prompt := st.chat_input("మీ ప్రశ్న ఇక్కడ అడగండి..."):
    if not u_name:
        st.error("బావా, ముందుగా పేరు నమోదు చేయి అండి!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("గ్రహ గతులను మరియు గ్రంథాలను విశ్లేషిస్తున్నాను..."):
                books_context = load_all_books()
                online_context = search_online(prompt)
                
                client = groq.Groq(api_key="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")
                
                sys_prompt = f"""
                నీ పేరు పద్మ ఏఐ. ఒక గొప్ప జ్యోతిష్యుడివి.
                యూజర్: {u_name}, పుట్టిన తేదీ: {u_dob}, రాశి: {zod}.
                అడ్మిన్ ఇచ్చిన 6 గ్రంథాల డేటా: {books_context[:7000]}
                ఆన్లైన్ లో దొరికిన తాజా డేటా: {online_context[:2000]}
                యూజర్‌ని 'అండి' అని పిలుస్తూ తెలుగులో జవాబివ్వు. పాజిటివ్ గా ఉండాలి.
                """
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}]
                )
                
                final_res = response.choices[0].message.content
                st.markdown(final_res)
                st.session_state.messages.append({"role": "assistant", "content": final_res})
                speak_now(final_res)
