import streamlit as st
import random
from datetime import datetime

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="KisaanSmart 🌾",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f5f5dc; }
    .stApp { background: linear-gradient(135deg, #e8f5e9 0%, #fff9c4 100%); }
    h1 { color: #2e7d32; font-family: 'Arial', sans-serif; }
    h2, h3 { color: #388e3c; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #4caf50;
    }
    .tip-box {
        background: #e8f5e9;
        border-left: 4px solid #2e7d32;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
    }
    .warning-box {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─── Data ───────────────────────────────────────────────────────

CROP_DATA = {
    "Wheat (Gehun)": {
        "season": "Rabi (Oct–Mar)",
        "water": "Medium",
        "soil": "Loamy / Clay Loam",
        "fertilizer": "NPK 120:60:40 kg/ha",
        "diseases": ["Rust", "Smut", "Powdery Mildew"],
        "tips": [
            "Sow at 20–25°C for best germination.",
            "First irrigation at Crown Root Initiation stage (21 days).",
            "Use certified seeds for higher yield.",
            "Apply urea in two splits for efficient uptake."
        ],
        "yield": "3.5–5 tonnes/ha",
        "msp": "₹2,275/quintal (2024–25)"
    },
    "Rice (Dhan)": {
        "season": "Kharif (Jun–Nov)",
        "water": "High",
        "soil": "Clay / Silty Clay",
        "fertilizer": "NPK 100:50:50 kg/ha",
        "diseases": ["Blast", "Brown Spot", "Sheath Blight"],
        "tips": [
            "Transplant 25–30 day old seedlings.",
            "Maintain 2–5 cm standing water during tillering.",
            "Drain field 10 days before harvest.",
            "Zinc deficiency is common — apply ZnSO4 25 kg/ha."
        ],
        "yield": "4–6 tonnes/ha",
        "msp": "₹2,300/quintal (2024–25)"
    },
    "Maize (Makka)": {
        "season": "Kharif (Jun–Sep)",
        "water": "Medium",
        "soil": "Well-drained Loamy",
        "fertilizer": "NPK 120:60:60 kg/ha",
        "diseases": ["Leaf Blight", "Stalk Rot", "Smut"],
        "tips": [
            "Plant in rows 60 cm apart, 20 cm between plants.",
            "Top-dress with nitrogen at knee-high stage.",
            "Irrigate at silking and grain-filling stages.",
            "Harvest when husk turns brown and grain is hard."
        ],
        "yield": "5–8 tonnes/ha",
        "msp": "₹2,090/quintal (2024–25)"
    },
    "Soybean": {
        "season": "Kharif (Jun–Sep)",
        "water": "Medium",
        "soil": "Well-drained Black Soil",
        "fertilizer": "NPK 20:80:40 kg/ha",
        "diseases": ["Yellow Mosaic", "Root Rot", "Leaf Spot"],
        "tips": [
            "Treat seeds with Rhizobium culture before sowing.",
            "Avoid waterlogging — it damages roots.",
            "Weed control in first 30 days is critical.",
            "Harvest when 95% pods turn brown."
        ],
        "yield": "1.5–2.5 tonnes/ha",
        "msp": "₹4,892/quintal (2024–25)"
    },
    "Cotton (Kapas)": {
        "season": "Kharif (Apr–Dec)",
        "water": "Medium-High",
        "soil": "Black Cotton Soil",
        "fertilizer": "NPK 150:60:60 kg/ha",
        "diseases": ["Bollworm", "Leaf Curl Virus", "Root Rot"],
        "tips": [
            "Use Bt Cotton varieties to control bollworm.",
            "Do not over-irrigate — it promotes vegetative growth.",
            "Monitor for whitefly which spreads leaf curl virus.",
            "Pick cotton in dry weather to maintain fiber quality."
        ],
        "yield": "2–3 tonnes/ha (seed cotton)",
        "msp": "₹7,121/quintal (2024–25)"
    },
    "Tomato (Tamatar)": {
        "season": "Year-round (best Oct–Mar)",
        "water": "Medium",
        "soil": "Sandy Loam",
        "fertilizer": "NPK 120:80:80 kg/ha",
        "diseases": ["Early Blight", "Late Blight", "Mosaic Virus"],
        "tips": [
            "Transplant 4–6 week old seedlings.",
            "Stake plants for support when they reach 30 cm.",
            "Drip irrigation reduces blight risk.",
            "Remove infected leaves immediately to stop spread."
        ],
        "yield": "25–40 tonnes/ha",
        "msp": "Market price (no MSP)"
    },
    "Onion (Pyaaz)": {
        "season": "Rabi (Oct–Apr)",
        "water": "Medium",
        "soil": "Sandy Loam / Silt Loam",
        "fertilizer": "NPK 100:50:50 kg/ha",
        "diseases": ["Purple Blotch", "Thrips", "Basal Rot"],
        "tips": [
            "Transplant 6–8 week old seedlings.",
            "Stop irrigation 10 days before harvest for good storage.",
            "Cure bulbs in shade for 3–5 days after harvest.",
            "Apply sulphur to control thrips effectively."
        ],
        "yield": "20–30 tonnes/ha",
        "msp": "Market price (no MSP)"
    }
}

MANDI_PRICES = {
    "Wheat": {"Indore": 2310, "Bhopal": 2290, "Nagpur": 2350, "Pune": 2280, "Delhi": 2400},
    "Rice":  {"Indore": 2250, "Bhopal": 2200, "Nagpur": 2300, "Pune": 2180, "Delhi": 2320},
    "Maize": {"Indore": 2100, "Bhopal": 2050, "Nagpur": 2150, "Pune": 2020, "Delhi": 2200},
    "Soybean": {"Indore": 4800, "Bhopal": 4750, "Nagpur": 4900, "Pune": 4700, "Delhi": 4850},
    "Cotton": {"Indore": 7000, "Bhopal": 6950, "Nagpur": 7100, "Pune": 6900, "Delhi": 7050},
    "Tomato": {"Indore": 1800, "Bhopal": 2100, "Nagpur": 1950, "Pune": 2200, "Delhi": 2500},
    "Onion":  {"Indore": 1500, "Bhopal": 1450, "Nagpur": 1600, "Pune": 1700, "Delhi": 1800},
}

WEATHER_DATA = {
    "Indore":  {"temp": 28, "humidity": 65, "rain": "Light rain expected", "condition": "⛅ Partly Cloudy"},
    "Bhopal":  {"temp": 30, "humidity": 60, "rain": "No rain", "condition": "☀️ Sunny"},
    "Nagpur":  {"temp": 33, "humidity": 55, "rain": "No rain", "condition": "🌤️ Mostly Clear"},
    "Pune":    {"temp": 26, "humidity": 70, "rain": "Moderate rain likely", "condition": "🌧️ Rainy"},
    "Delhi":   {"temp": 25, "humidity": 50, "rain": "No rain", "condition": "☀️ Clear Sky"},
    "Jaipur":  {"temp": 29, "humidity": 45, "rain": "No rain", "condition": "☀️ Sunny"},
    "Lucknow": {"temp": 27, "humidity": 68, "rain": "Light drizzle", "condition": "🌦️ Drizzle"},
}

GOVT_SCHEMES = [
    {
        "name": "PM-KISAN Samman Nidhi",
        "benefit": "₹6,000/year direct to bank (3 installments)",
        "eligibility": "All small & marginal farmers with land records",
        "link": "https://pmkisan.gov.in"
    },
    {
        "name": "PM Fasal Bima Yojana (PMFBY)",
        "benefit": "Crop insurance at 1.5–2% premium for Rabi/Kharif",
        "eligibility": "Farmers growing notified crops",
        "link": "https://pmfby.gov.in"
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "benefit": "Low-interest credit up to ₹3 lakh at 4% per annum",
        "eligibility": "All farmers — apply at any bank",
        "link": "https://www.nabard.org"
    },
    {
        "name": "Soil Health Card Scheme",
        "benefit": "Free soil testing + nutrient recommendations",
        "eligibility": "All farmers",
        "link": "https://soilhealth.dac.gov.in"
    },
    {
        "name": "PM Krishi Sinchai Yojana",
        "benefit": "Subsidy on drip/sprinkler irrigation up to 55%",
        "eligibility": "Farmers in notified areas",
        "link": "https://pmksy.gov.in"
    },
    {
        "name": "e-NAM (National Agriculture Market)",
        "benefit": "Sell crops online at best mandi prices nationwide",
        "eligibility": "Registered farmers",
        "link": "https://enam.gov.in"
    },
]

# ─── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/240px-Emblem_of_India.svg.png", width=60)
    st.markdown("## 🌾 KisaanSmart")
    st.markdown("*AI Crop Advisory & Market Tool*")
    st.divider()

    language = st.selectbox("🌐 Language / भाषा", ["English", "हिंदी (Hindi)"])

    st.divider()
    selected_city = st.selectbox("📍 Your Location", list(WEATHER_DATA.keys()))

    # Mini weather widget
    w = WEATHER_DATA[selected_city]
    st.markdown(f"""
    **Weather — {selected_city}**
    - {w['condition']}
    - 🌡️ {w['temp']}°C  💧 {w['humidity']}% humidity
    - 🌧️ {w['rain']}
    """)

    st.divider()
    st.markdown("📞 **Kisan Call Center**")
    st.markdown("**1800-180-1551** *(Free, 24×7)*")

# ─── Header ─────────────────────────────────────────────────────
st.markdown("# 🌾 KisaanSmart")
st.markdown("### AI Crop Advisory & Market Price Tool for Farmers")
st.markdown(f"*{datetime.now().strftime('%A, %d %B %Y')}* | 📍 {selected_city}")
st.divider()

# ─── Tabs ────────────────────────────────────────────────────────
tabs = st.tabs(["🌱 Crop Advisory", "💰 Mandi Prices", "☀️ Weather", "🏛️ Govt Schemes", "🤖 AI Chatbot"])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — CROP ADVISORY
# ══════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("## 🌱 Crop Advisory")
    st.markdown("Get complete information about your crop — sowing, irrigation, fertilizer, diseases & more.")

    col1, col2 = st.columns([1, 2])

    with col1:
        selected_crop = st.selectbox("Select your crop / अपनी फसल चुनें", list(CROP_DATA.keys()))
        data = CROP_DATA[selected_crop]

        st.markdown("---")
        st.markdown(f"**📅 Season:** {data['season']}")
        st.markdown(f"**💧 Water Need:** {data['water']}")
        st.markdown(f"**🪱 Best Soil:** {data['soil']}")
        st.markdown(f"**⚗️ Fertilizer:** {data['fertilizer']}")
        st.markdown(f"**📦 Avg Yield:** {data['yield']}")
        st.markdown(f"**🏷️ MSP 2024–25:** {data['msp']}")

    with col2:
        st.markdown(f"### 💡 Tips for {selected_crop}")
        for tip in data["tips"]:
            st.markdown(f"""<div class="tip-box">✅ {tip}</div>""", unsafe_allow_html=True)

        st.markdown("### ⚠️ Common Diseases")
        for disease in data["diseases"]:
            st.markdown(f"""<div class="warning-box">🔴 {disease}</div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📊 Crop Comparison")
    crops_to_compare = st.multiselect("Compare crops", list(CROP_DATA.keys()), default=["Wheat (Gehun)", "Rice (Dhan)", "Soybean"])

    if crops_to_compare:
        import pandas as pd
        compare_rows = []
        for c in crops_to_compare:
            d = CROP_DATA[c]
            compare_rows.append({
                "Crop": c,
                "Season": d["season"],
                "Water": d["water"],
                "Soil": d["soil"],
                "Avg Yield": d["yield"],
                "MSP": d["msp"]
            })
        st.dataframe(pd.DataFrame(compare_rows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════
# TAB 2 — MANDI PRICES
# ══════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("## 💰 Live Mandi Prices")
    st.markdown("Current wholesale prices at major mandis (₹/quintal)")

    import pandas as pd

    col1, col2 = st.columns(2)
    with col1:
        price_crop = st.selectbox("Select Crop", list(MANDI_PRICES.keys()), key="price_crop")
    with col2:
        st.markdown(f"**MSP Reference:** {CROP_DATA.get(price_crop, CROP_DATA.get(price_crop + ' (Gehun)', {}).get('msp', 'See advisory tab'))}")

    prices = MANDI_PRICES[price_crop]

    # Metric cards
    cols = st.columns(len(prices))
    for idx, (city, price) in enumerate(prices.items()):
        with cols[idx]:
            delta = price - list(prices.values())[0]
            st.metric(label=f"📍 {city}", value=f"₹{price}", delta=f"₹{delta:+d}" if idx > 0 else None)

    st.divider()

    # Price table for all crops
    st.markdown("### 📋 Full Price Table — All Crops")
    all_rows = []
    for crop, cities in MANDI_PRICES.items():
        row = {"Crop": crop}
        row.update(cities)
        best_city = max(cities, key=cities.get)
        row["Best Market"] = f"{best_city} (₹{cities[best_city]})"
        all_rows.append(row)

    df_all = pd.DataFrame(all_rows)
    st.dataframe(df_all, use_container_width=True, hide_index=True)

    st.info("ℹ️ Prices are indicative. Check **eNAM (enam.gov.in)** for real-time official mandi prices.")

# ══════════════════════════════════════════════════════════════════
# TAB 3 — WEATHER
# ══════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("## ☀️ Weather Advisory")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### 📍 {selected_city}")
        w = WEATHER_DATA[selected_city]
        st.markdown(f"# {w['condition']}")
        st.metric("Temperature", f"{w['temp']}°C")
        st.metric("Humidity", f"{w['humidity']}%")
        st.markdown(f"**Rainfall:** {w['rain']}")

    with col2:
        st.markdown("### 🌾 Farming Advice based on Weather")
        temp = w["temp"]
        humidity = w["humidity"]

        if "rain" in w["rain"].lower() or "drizzle" in w["rain"].lower():
            st.markdown("""<div class="warning-box">
            ⚠️ <b>Rain expected</b> — Avoid pesticide/fertilizer spray today.<br>
            🚜 Hold irrigation — natural rain will suffice.<br>
            📦 Store harvested grain in dry place.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="tip-box">
            ✅ <b>No rain today</b> — Good day for spraying.<br>
            💧 Check soil moisture — irrigate if needed.<br>
            🌞 Good conditions for harvesting.
            </div>""", unsafe_allow_html=True)

        if temp > 35:
            st.markdown("""<div class="warning-box">🌡️ <b>High temperature</b> — Irrigate crops in evening to reduce heat stress.</div>""", unsafe_allow_html=True)
        if humidity > 75:
            st.markdown("""<div class="warning-box">💧 <b>High humidity</b> — Risk of fungal diseases. Monitor crops closely.</div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🗓️ 7-Day Forecast (Simulated)")
    import pandas as pd
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    forecast_data = {
        "Day": days,
        "Temp (°C)": [w["temp"] + random.randint(-3, 3) for _ in days],
        "Humidity (%)": [w["humidity"] + random.randint(-5, 5) for _ in days],
        "Condition": random.choices(["☀️ Sunny", "⛅ Cloudy", "🌧️ Rain", "🌤️ Clear"], k=7)
    }
    st.dataframe(pd.DataFrame(forecast_data), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════
# TAB 4 — GOVT SCHEMES
# ══════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("## 🏛️ Government Schemes for Farmers")
    st.markdown("Central government schemes you can apply for right now.")

    for scheme in GOVT_SCHEMES:
        with st.expander(f"📋 {scheme['name']}"):
            st.markdown(f"**💰 Benefit:** {scheme['benefit']}")
            st.markdown(f"**✅ Who can apply:** {scheme['eligibility']}")
            st.markdown(f"**🔗 Official Website:** [{scheme['link']}]({scheme['link']})")
            st.button(f"Apply for {scheme['name']}", key=scheme['name'],
                      help=f"Visit {scheme['link']}")

    st.divider()
    st.info("💡 For help applying to any scheme, call **Kisan Call Center: 1800-180-1551** (Free, 24×7)")

# ══════════════════════════════════════════════════════════════════
# TAB 5 — AI CHATBOT
# ══════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("## 🤖 KisaanSmart Assistant")
    st.markdown("Ask any farming question in Hindi or English.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Namaste Kisan bhai! 🙏\nMain KisaanSmart Assistant hun. Aap mujhse kheti ke baare mein koi bhi sawaal pooch sakte hain — beej, khaad, mausam, mandi bhav, ya sarkari yojana.\n\n*Hello Farmer! Ask me anything about crops, fertilizers, weather, mandi prices, or government schemes.*"}
        ]

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Smart rule-based responses
    def get_response(user_input: str) -> str:
        q = user_input.lower()

        # Mandi / price
        if any(w in q for w in ["mandi", "price", "bhav", "rate", "dam", "daam"]):
            best = {crop: max(prices.values()) for crop, prices in MANDI_PRICES.items()}
            lines = "\n".join([f"• **{c}**: ₹{p}/quintal" for c, p in best.items()])
            return f"📊 **Best mandi prices today:**\n{lines}\n\n🔗 For live rates: [eNAM](https://enam.gov.in)"

        # Weather
        elif any(w in q for w in ["weather", "mausam", "rain", "barish", "temperature"]):
            w = WEATHER_DATA[selected_city]
            return f"☀️ **Weather in {selected_city}:**\n- {w['condition']}\n- 🌡️ {w['temp']}°C, 💧 {w['humidity']}% humidity\n- 🌧️ {w['rain']}"

        # Wheat
        elif any(w in q for w in ["wheat", "gehun", "गेहूं"]):
            d = CROP_DATA["Wheat (Gehun)"]
            return f"🌾 **Wheat Advisory:**\n- Season: {d['season']}\n- Fertilizer: {d['fertilizer']}\n- MSP: {d['msp']}\n- Tip: {d['tips'][0]}"

        # Rice
        elif any(w in q for w in ["rice", "dhan", "paddy", "chawal", "धान"]):
            d = CROP_DATA["Rice (Dhan)"]
            return f"🌾 **Rice Advisory:**\n- Season: {d['season']}\n- Fertilizer: {d['fertilizer']}\n- MSP: {d['msp']}\n- Tip: {d['tips'][0]}"

        # Soybean
        elif any(w in q for w in ["soybean", "soya", "soyabean"]):
            d = CROP_DATA["Soybean"]
            return f"🌾 **Soybean Advisory:**\n- Season: {d['season']}\n- Fertilizer: {d['fertilizer']}\n- MSP: {d['msp']}\n- Tip: {d['tips'][0]}"

        # Fertilizer
        elif any(w in q for w in ["fertilizer", "khad", "khaad", "urea", "npk", "खाद"]):
            return "⚗️ **Fertilizer Tips:**\n- Use soil test results before applying fertilizers\n- Apply NPK as per crop requirement\n- Split urea application improves efficiency\n- Organic manure improves soil health long-term\n\n📍 Get free soil test at **Soil Health Card center** in your district."

        # Disease / pest
        elif any(w in q for w in ["disease", "bimari", "pest", "keet", "fungus", "rot", "blight"]):
            return "🔴 **Disease & Pest Control:**\n- Scout fields regularly (twice a week)\n- Use IPM (Integrated Pest Management)\n- Avoid over-irrigation to prevent fungal diseases\n- Remove infected plants immediately\n- Call Kisan helpline: **1800-180-1551** for expert advice"

        # Schemes / government
        elif any(w in q for w in ["scheme", "yojana", "pm-kisan", "kisan", "insurance", "bima", "loan", "subsidy"]):
            return "🏛️ **Key Govt Schemes:**\n- **PM-KISAN**: ₹6,000/year → pmkisan.gov.in\n- **PMFBY**: Crop insurance → pmfby.gov.in\n- **KCC**: Loan @ 4% interest\n- **Soil Health Card**: Free soil testing\n- **PM Sinchai Yojana**: Drip irrigation subsidy 55%"

        # Irrigation / water
        elif any(w in q for w in ["irrigation", "sinchai", "water", "paani", "drip", "sprinkler"]):
            return "💧 **Irrigation Tips:**\n- Drip irrigation saves 40–50% water\n- Irrigate in morning/evening to reduce evaporation\n- Avoid waterlogging — it damages roots\n- Get 55% subsidy on drip irrigation under PM Krishi Sinchai Yojana"

        # Soil
        elif any(w in q for w in ["soil", "mitti", "land", "zameen"]):
            return "🪱 **Soil Health Tips:**\n- Get soil tested every 3 years (free via Soil Health Card)\n- Add organic matter to improve soil structure\n- pH 6–7 is ideal for most crops\n- Avoid burning crop residue — it destroys soil microbes"

        # Hello / greeting
        elif any(w in q for w in ["hello", "hi", "namaste", "helo", "namaskar", "नमस्ते"]):
            return "🙏 Namaste Kisan bhai! Main KisaanSmart Assistant hun.\n\nAap pooch sakte hain:\n- 🌾 Kisi bhi fasal ki jankari\n- 💰 Mandi ke bhav\n- ☀️ Mausam ki jankari\n- 🏛️ Sarkari yojana\n- 💧 Sinchai aur khad ke tips"

        else:
            return (
                f"🤔 Sorry, I don't have a specific answer for *'{user_input}'* yet.\n\n"
                "You can ask me about:\n"
                "- 🌾 Crop advice (wheat, rice, soybean, cotton...)\n"
                "- 💰 Mandi prices\n"
                "- ☀️ Weather\n"
                "- 🏛️ Government schemes\n"
                "- 💧 Irrigation & fertilizer tips\n\n"
                "📞 For expert advice: **Kisan Call Center 1800-180-1551**"
            )

    # Chat input
    if prompt := st.chat_input("Ask your farming question... (Hindi or English)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = get_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# ─── Footer ─────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align:center; color:#666; font-size:13px;'>
🌾 KisaanSmart — Built for Indian Farmers | MyBharat Hack Social 2024<br>
Data sources: Government of India MSP notifications, eNAM, IMD Weather
</div>
""", unsafe_allow_html=True)
