import streamlit as st
import os, PyPDF2, groq, datetime

# 1. యాప్ టైటిల్ మరియు డిజైన్
st.set_page_config(page_title="Padma AI Services", layout="wide", page_icon="✨")
st.title("🔮 Padma AI Services")
st.markdown("### మీ జాతకాన్ని గ్రంథాల ఆధారంగా విశ్లేషించుకోండి")

# 2. యూజర్ ఇన్పుట్ బాక్సులు
col1, col2 = st.columns(2)
with col1:
    # ఇక్కడ నీ పేరు తీసేసి జనరల్ గా మార్చాను బావా
    user_name = st.text_input("మీ పేరు నమోదు చేయండి:", placeholder="మీ పేరు ఇక్కడ రాయండి")
    birth_date = st.date_input("మీ పుట్టిన తేదీని ఎంచుకోండి:", 
                               min_value=datetime.date(1900, 1, 1), 
                               max_value=datetime.date(2100, 12, 31))
with col2:
    birth_time = st.time_input("పుట్టిన సమయం (అంచనా):")
    zodiac = st.selectbox("మీ రాశిని ఎంచుకోండి:", [
        'మేషం ♈', 'వృషభం ♉', 'మిథునం ♊', 'కర్కాటకం ♋', 
        'సింహం ♌', 'కన్య ♍', 'తుల ♎', 'వృశ్చికం ♏', 
        'ధనుస్సు ♐', 'మకరం ♑', 'కుంభం ♒', 'మీనం ♓'
    ])

# 3. ఫైల్ అప్‌లోడర్
st.divider()
st.subheader("📁 జాతక గ్రంథాలను అప్‌లోడ్ చేయండి")
files = st.file_uploader("పిడిఎఫ్ (PDF) ఫైల్స్ ఇక్కడ వేయండి", accept_multiple_files=True)

# 4. విశ్లేషణ బటన్
if st.button("జాతక నివేదిక పొందండి", type="primary"):
    if user_name and files:
        with st.spinner("జాతకాన్ని విశ్లేషిస్తున్నాను..."):
            all_text = ""
            for f in files:
                pdf = PyPDF2.PdfReader(f)
                for page in pdf.pages[:50]:
                    all_text += page.extract_text()
            
            client = groq.Groq(api_key="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")
            
            prompt = f"""
            నువ్వు 'పద్మ ఏఐ సర్వీసెస్' జ్యోతిష్యుడివి.
            యూజర్ వివరాలు: పేరు: {user_name}, పుట్టిన తేదీ: {birth_date}, సమయం: {birth_time}, రాశి: {zodiac}.
            టాస్క్: ఇచ్చిన పుస్తకాలలోని ({all_text[:12000]}) పాత సూత్రాలను మరియు నేటి గ్రహాల స్థితిని బట్టి 
            ఈ యూజర్ కి తెలుగులో పూర్తి జాతక ఫలితాలు వివరించు.
            """
            
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            
            st.success("విశ్లేషణ పూర్తయింది!")
            st.markdown(f"## 📜 {user_name} గారి జాతక రిపోర్ట్")
            st.write(res.choices[0].message.content)
            st.balloons()
    else:
        st.warning("దయచేసి పేరు నమోదు చేసి, పుస్తకాలను అప్‌లోడ్ చేయండి!")

st.divider()
st.caption("© 2026 Padma AI Services - వేద మరియు ఆధునిక జ్యోతిష్య విశ్లేషణ")
