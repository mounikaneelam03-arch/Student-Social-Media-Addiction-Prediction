import streamlit as st
import pickle
import numpy as np
import base64
import os

# ------------------ Page Configuration ------------------
st.set_page_config(
    page_title="Student Social Media Addiction Predictor",
    page_icon="📱",
    layout="wide", 
    
)

# ------------------ Load Model ------------------
model = pickle.load(open("RF_model.pkl", "rb"))
scaler = pickle.load(open("scalar.pkl", "rb"))

# ------------------ Background Image ------------------
st.set_page_config(layout="wide")

bg_image_url = "https://images.zwierciadlo.pl/_resource/res/path/0c/88/0c889bf4-1755-4ca3-b441-27ad2f253e4d"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)



# Add custom CSS for better visibility
st.markdown("""
<style>
/* Style input containers with semi-transparent background */
.stSlider, .stSelectbox, .stButton {
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
}

/* Style labels to be dark and readable */
label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 16px !important;
}

/* Style columns container */
.stColumns {
        gap: 20px;
}

/* Make the input section cleaner */
[data-testid="column"] {
        background-color: rgba(245, 245, 245, 0.98) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
}

/* --- Animations for result banners --- */
@keyframes floatUpDown {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
}

@keyframes pulseGlow {
    0% { transform: scale(1); box-shadow: 0 0 0 rgba(255,255,255,0); }
    50% { transform: scale(1.05); box-shadow: 0 8px 24px rgba(255,255,255,0.12); }
    100% { transform: scale(1); box-shadow: 0 0 0 rgba(255,255,255,0); }
}

@keyframes shake {
    0% { transform: translateX(0); }
    25% { transform: translateX(-6px); }
    50% { transform: translateX(6px); }
    75% { transform: translateX(-4px); }
    100% { transform: translateX(0); }
}

@keyframes popIn {
    0% { transform: scale(0.96); opacity: 0; }
    60% { transform: scale(1.02); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
}

@keyframes btnBounce {
    0% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0); }
}

.header-emoji { font-size: 56px; margin-right:12px; vertical-align:middle; animation: floatUpDown 3s ease-in-out infinite; }
.title-text { display:inline-block; vertical-align:middle; animation: popIn 0.8s ease-out both; }
.subtitle { animation: floatUpDown 4.4s ease-in-out infinite; opacity:0.95; }

/* Animate the Streamlit button (predict) */
.stButton>button {
    animation: btnBounce 2.4s ease-in-out infinite;
    border-radius: 10px;
}

/* Apply an entrance animation to result banners */
.result-banner { animation: popIn 0.6s ease-out both; }

.float-emoji {
    animation: floatUpDown 3.2s ease-in-out infinite;
    font-size: 40px;
}

.pulse-emoji {
    animation: pulseGlow 2.2s ease-in-out infinite;
    font-size: 38px;
}

.shake-emoji {
    animation: shake 0.9s ease-in-out infinite;
    font-size: 42px;
}

.result-deco {
    position: absolute; top: -18px; right: 18px; z-index: 10;
}

.result-banner { position: relative; }

</style>
""", unsafe_allow_html=True)

# ------------------ Title ------------------
st.markdown("""
<div style='text-align:center;'>
    <span class='header-emoji'>📱</span>
    <span class='title-text'><h1 style='display:inline-block; color:black; text-shadow:2px 2px black; margin:0;'>Student Social Media Addiction Predictor</h1></span>
    <p class='subtitle' style='color:black; font-size:20px; margin-top:8px;'>AI-powered system to analyze addiction risk — get personalized tips ✨</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------ Input Section ------------------
st.markdown("<h2 style='color:white; text-align:center; text-shadow:2px 2px black;'>📋 Enter Your Information</h2>", unsafe_allow_html=True)

age = st.slider("🎂 Age", 10, 60, 20)
gender = st.selectbox("👤 Gender", ["Male", "Female"])
academic_level = st.selectbox("📚 Academic Level", ["High School", "Undergraduate", "Graduate"])
country = st.selectbox("🌍 Country", ["Afghanistan", "Albania", "Andorra", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Belarus", "Belgium", "Bhutan", "Bolivia", "Bosnia", "Brazil", "Bulgaria", "Canada", "Chile", "China", "Colombia", "Costa Rica", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Ecuador", "Egypt", "Estonia", "Finland", "France", "Georgia", "Germany", "Ghana", "Greece", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kosovo", "Kuwait", "Kyrgyzstan", "Latvia", "Lebanon", "Liechtenstein", "Lithuania", "Luxembourg", "Malaysia", "Maldives", "Malta", "Mexico", "Moldova", "Monaco", "Montenegro", "Morocco", "Nepal", "Netherlands", "New Zealand", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Panama", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "San Marino", "Serbia", "Singapore", "Slovakia", "Slovenia", "South Africa", "South Korea", "Spain", "Sri Lanka", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Thailand", "Trinidad", "Turkey", "UAE", "UK", "USA", "Ukraine", "Uruguay", "Uzbekistan", "Vatican City", "Venezuela", "Vietnam", "Yemen"])
daily_usage = st.slider("📱 Daily Usage Hours", 0.0, 12.0, 4.0)
platform = st.selectbox("🌐 Most Used Platform", ["Facebook", "Instagram", "KakaoTalk", "LINE", "LinkedIn", "Snapchat", "TikTok", "Twitter", "VKontakte", "WeChat", "WhatsApp", "YouTube"])
academic_impact = st.selectbox("📊 Affects Academic Performance", ["No", "Yes"])
sleep_hours = st.slider("😴 Sleep Hours per Night", 3, 10, 7)
mental_health = st.slider("🧠 Mental Health Score (1–10)", 1, 10, 5)
relationship = st.selectbox("💑 Relationship Status", ["Single", "In Relationship"])
conflicts = st.slider("⚠️ Conflicts Over Social Media (1–5)", 1, 5, 2)

# Encoding using LabelEncoder logic (alphabetical order)
gender_encoded = 0 if gender == "Female" else 1

# Academic Level: alphabetical - Graduate=0, High School=1, Undergraduate=2
academic_map = {"Graduate": 0, "High School": 1, "Undergraduate": 2}
academic_level_encoded = academic_map[academic_level]

# Country: alphabetically sorted
countries = ["Afghanistan", "Albania", "Andorra", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Belarus", "Belgium", "Bhutan", "Bolivia", "Bosnia", "Brazil", "Bulgaria", "Canada", "Chile", "China", "Colombia", "Costa Rica", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Ecuador", "Egypt", "Estonia", "Finland", "France", "Georgia", "Germany", "Ghana", "Greece", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kosovo", "Kuwait", "Kyrgyzstan", "Latvia", "Lebanon", "Liechtenstein", "Lithuania", "Luxembourg", "Malaysia", "Maldives", "Malta", "Mexico", "Moldova", "Monaco", "Montenegro", "Morocco", "Nepal", "Netherlands", "New Zealand", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Panama", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "San Marino", "Serbia", "Singapore", "Slovakia", "Slovenia", "South Africa", "South Korea", "Spain", "Sri Lanka", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Thailand", "Trinidad", "Turkey", "UAE", "UK", "USA", "Ukraine", "Uruguay", "Uzbekistan", "Vatican City", "Venezuela", "Vietnam", "Yemen"]
country_encoded = countries.index(country)

# Platform: alphabetically - Facebook=0, Instagram=1, KakaoTalk=2, etc.
platforms = ["Facebook", "Instagram", "KakaoTalk", "LINE", "LinkedIn", "Snapchat", "TikTok", "Twitter", "VKontakte", "WeChat", "WhatsApp", "YouTube"]
platform_encoded = platforms.index(platform)

# Affects Academic Performance: No=0, Yes=1
academic_impact_encoded = 0 if academic_impact == "No" else 1

# Relationship Status: alphabetically - Complicated=0, In Relationship=1, Single=2
relationship_map = {"Complicated": 0, "In Relationship": 1, "Single": 2}
relationship_encoded = relationship_map[relationship]

# ------------------ Prediction Button ------------------
col_button_left, col_button_center, col_button_right = st.columns([1, 1, 1])
with col_button_center:
    if st.button("🔍 Predict Addiction Level", use_container_width=True):
        input_data = np.array([[age, gender_encoded, academic_level_encoded, country_encoded,
                                 daily_usage, platform_encoded, academic_impact_encoded,
                                 sleep_hours, mental_health, relationship_encoded, conflicts]])

        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]

        st.markdown("---")

        # ------------------ RESULT DISPLAY ------------------
        # make center column wider so the result box can expand
        result_col1, result_col2, result_col3 = st.columns([1, 6, 1])
        
        with result_col2:
            if prediction < 4:
                st.success("✅ LOW ADDICTION LEVEL")
                # Celebration: balloons and congratulatory banner
                try:
                    st.balloons()
                except Exception:
                    pass

                st.markdown(f"""
                <div class='result-banner' style='max-width:1000px; min-height:200px; margin:16px auto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 22px; border-radius: 14px; text-align: center; box-shadow: 0 10px 24px rgba(0,0,0,0.35); display:flex; flex-direction:column; justify-content:center; align-items:center;'>
                    <div class='result-deco'><span class='float-emoji'>🌱✅😊🎈🎉</span></div>
                    <h1 style='color: #fff; margin: 0; font-size: 48px; font-weight: 800;'>🎉 Congratulations!</h1>
                    <p style='color: #f0f5ff; margin: 8px 0 12px 0; font-size: 18px;'>You have a LOW addiction level</p>
                    <h2 style='color: white; margin: 6px 0 0 0; font-size: 56px; font-weight: 900;'>{prediction:.2f}</h2>
                    <p style='color: #e0e0e0; margin: 6px 0 6px 0; font-size: 14px;'>Addiction Score</p>
                    <ul style='text-align:left; color:#f0f5ff; margin:12px 0 0 0; padding-left:22px; font-size:15px;'>
                        <li>🎯📚 Focus on your studies and personal goals</li>
                        <li>🛌 Prioritize sleep — aim for consistent hours</li>
                        <li>⏱️ Set small daily screen-time limits</li>
                        <li>💬 Keep social time balanced with offline activities</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                # Optional celebration animation if available
                if os.path.exists("assests/animation.gif"):
                    st.image("assests/animation.gif", width=700)

            elif prediction < 7:
                st.warning("⚠️ MODERATE ADDICTION LEVEL")
                st.markdown(f"""
                <div class='result-banner' style='max-width:1000px; min-height:200px; margin:16px auto; background: linear-gradient(135deg, #ffefba 0%, #ffffff 100%); padding: 20px; border-radius: 14px; text-align: center; box-shadow: 0 10px 24px rgba(0,0,0,0.18); display:flex; flex-direction:column; justify-content:center; align-items:center;'>
                    <div class='result-deco' style='right:auto; left:18px;'><span class='pulse-emoji'>📵🔔⏳🧠⚠️</span></div>
                    <h1 style='color: #8a6d3b; margin: 0; font-size: 42px; font-weight: 700;'>⚠️ Keep an Eye on Usage</h1>
                    <p style='color: #6b4f2f; margin: 8px 0 12px 0; font-size: 16px;'>Moderate addiction level — consider reducing screen time</p>
                    <h2 style='color: #5a3e1b; margin: 6px 0 0 0; font-size: 48px; font-weight: 800;'>{prediction:.2f}</h2>
                    <p style='color: #6b4f2f; margin: 6px 0 0 0; font-size: 14px;'>Addiction Score</p>
                    <ul style='text-align:left; color:#6b4f2f; margin:12px 0 0 0; padding-left:22px; font-size:15px;'>
                        <li>📵 Try scheduled no-phone periods (study/meal times)</li>
                        <li>⏲️ Use app timers or screen-time controls</li>
                        <li>🏃 Add short physical breaks and hobbies</li>
                        <li>📝 Track usage for a week to spot patterns</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                # subtle caution animation if available
                if os.path.exists("assests/animation.gif"):
                    st.image("assests/animation.gif", width=600)

            else:
                st.error("🚨 HIGH ADDICTION ALERT!")
                st.markdown(f"""
                <div class='result-banner' style='max-width:1000px; min-height:200px; margin:16px auto; background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%); padding: 20px; border-radius: 14px; text-align: center; box-shadow: 0 10px 24px rgba(0,0,0,0.35); display:flex; flex-direction:column; justify-content:center; align-items:center;'>
                    <div class='result-deco'><span class='shake-emoji'>🚨📵☠️🚨❗</span></div>
                    <h1 style='color: #fff; margin: 0; font-size: 44px; font-weight: 800;'>🚨 High Addiction — Take Action</h1>
                    <p style='color: #fdecea; margin: 8px 0 12px 0; font-size: 16px;'>This indicates a high addiction score — consider seeking support and setting strict limits.</p>
                    <h2 style='color: #fff; margin: 6px 0 0 0; font-size: 48px; font-weight: 800;'>{prediction:.2f}</h2>
                    <p style='color: #ffe6e0; margin: 6px 0 0 0; font-size: 14px;'>Addiction Score</p>
                    <ul style='text-align:left; color:#fff; margin:12px 0 0 0; padding-left:22px; font-size:15px;'>
                        <li>📞 Consider speaking with a counselor or healthcare professional</li>
                        <li>🔒 Use app blockers and strict screen-time limits</li>
                        <li>🧑‍⚕️ Spend more time with family and friends</li>
                        <li>📆 Create a gradual reduction plan with clear goals</li>
                        <li>📵 Avoid using your phone before sleeping</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                # show a stronger visual hint if a danger image exists
                if os.path.exists("assests/image.jpg"):
                    st.image("assests/image.jpg", width=700)

# ------------------ Footer ------------------
st.markdown("""
<hr>
<p style='text-align:center;color:white;'>
Made with ❤️ using Machine Learning & Streamlit
</p>
""", unsafe_allow_html=True)
