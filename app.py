import numpy as np
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# =====================================================================
# 1. USER LOGIN CONFIGURATION
# =====================================================================
credentials = {
    "usernames": {
        "admin": {
            "name": "Carbon Researcher",
            "password": "password123"
        }
    }
}

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="carbon_capture_cookie",
    cookie_key="some_signature_key_123",
    cookie_expiry_days=30
)

# =====================================================================
# 2. AI CARBON CAPTURE ML MODEL DATA
# =====================================================================
@st.cache_data
def load_and_prep_data():
    np.random.seed(42)
    n_samples = 500
    nanocellulose_ratio = np.random.uniform(1.0, 5.0, n_samples)
    amine_loading_wt = np.random.uniform(5.0, 40.0, n_samples)
    temperature = np.random.uniform(15.0, 75.0, n_samples)
    pressure = np.random.uniform(0.01, 1.0, n_samples)
    humidity = np.random.uniform(0.0, 90.0, n_samples)

    co2_capacity = (
        150 
        - 15 * (nanocellulose_ratio - 3.0)**2 
        + 8 * amine_loading_wt - 0.15 * (amine_loading_wt**2)
        - 2.5 * (temperature - 25) 
        + 120 * pressure 
        + 0.5 * humidity
        + np.random.normal(0, 15, n_samples)
    )
    return pd.DataFrame({
        'nanocellulose_ratio': nanocellulose_ratio, 'amine_loading_wt': amine_loading_wt,
        'temperature': temperature, 'pressure': pressure, 'humidity': humidity, 'co2_capacity': np.clip(co2_capacity, 0, None)
    })

def train_model(df):
    X = df[['nanocellulose_ratio', 'amine_loading_wt', 'temperature', 'pressure', 'humidity']]
    y = df['co2_capacity']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    return model, scaler, model.score(scaler.transform(X_test), y_test)

# =====================================================================
# 3. EXPANDED INTELLIGENT ASSISTANT ENGINE (SMARTECH CORE)
# =====================================================================
def get_bot_response(user_query):
    query_lower = user_query.lower()
    
    # Core Definition Checks
    if "what is carbon capture" in query_lower or "define carbon capture" in query_lower:
        return (
            "*Carbon Capture* is a suite of technologies designed to trap carbon dioxide ($CO_2$) "
            "emissions directly from industrial sources (like power plants) or directly out of ambient air "
            "(Direct Air Capture). The goal is to prevent the greenhouse gas from entering the atmosphere, "
            "subsequently compressing and storing it permanently underground, or recycling it into useful products."
        )
    elif "how does direct air capture work" in query_lower or "dac" in query_lower:
        return (
            "*Direct Air Capture (DAC)* uses large chemical filters or fans to strip $CO_2$ directly from "
            "the ambient sky. Liquid systems pass air through chemical solutions (like potassium hydroxide), "
            "while solid systems use solid sorbent materials chemically treated with amines—exactly like the "
            "nanocellulose-chitosan matrix modeled on your Predictor Panel!"
        )
    elif "hello" in query_lower or "hi" in query_lower:
        return "Hello! I am Smartech Research Assistant. I can help you define carbon capture concepts, explain DAC mechanics, or parse out your biopolymer matrix components."
    elif "nanocellulose" in query_lower or "chitosan" in query_lower:
        return "Nanocellulose acts as a high-surface-area matrix template, while chitosan adds structural stability and auxiliary amino groups. Together, they create an optimal porous structure for loading heavy amines like TEPA or PEI."
    elif "amine" in query_lower or "loading" in query_lower:
        return "Optimal amine loading for this biopolymer blend typically peaks between 15% and 25% weight. Pushing beyond this threshold clogs the internal microscopic pores and blocks gas diffusion pathways, which decreases total capture capability."
    elif "humidity" in query_lower or "moisture" in query_lower:
        return "Moisture is advantageous for solid amine sorbents! Water vapor alters the absorption pathway from carbamate formation to bicarbonate formation, which theoretically doubles the maximum $CO_2$ reaction efficiency per nitrogen site."
    else:
        return (
            f"I process scientific inquiries regarding carbon mitigation strategies. Regarding '{user_query}', "
            "this specific framework can be explored further using the multi-variable controls on your "
            "*AI Predictor Panel* tab to calculate exact empirical limits."
        )

# =====================================================================
# 4. MAIN INTERFACE (TABS SYSTEM)
# =====================================================================
def main_dashboard():
    # Setup Tabs
    tab1, tab2 = st.tabs(["🔬 AI Predictor Panel", "💬 Smartech AI Chatbot"])
    
    # --- TAB 1: PREDICTOR ---
    with tab1:
        st.title("🌱 Material Parameter Optimizer")
        df = load_and_prep_data()
        model, scaler, score = train_model(df)
        
        st.sidebar.header("🔬 Composition Adjustments")
        nc_ratio = st.sidebar.slider("Nanocellulose-to-Chitosan Ratio (X : 1)", 1.0, 5.0, 3.0, 0.1)
        amine_load = st.sidebar.slider("Amine Loading (wt%)", 5.0, 40.0, 15.0, 0.5)
        
        st.sidebar.header("🌤️ Environmental Settings")
        temp = st.sidebar.slider("Temperature (°C)", 15.0, 75.0, 25.0, 1.0)
        press = st.sidebar.slider("Pressure (bar)", 0.01, 1.00, 0.05, 0.01)
        hum = st.sidebar.slider("Relative Humidity (%)", 0.0, 90.0, 40.0, 1.0)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            input_data = np.array([[nc_ratio, amine_load, temp, press, hum]])
            prediction = model.predict(scaler.transform(input_data))[0]
            st.metric(label="Predicted $CO_2$ Adsorption Capacity", value=f"{prediction:.2f} mg/g")
        with col2:
            st.metric(label="AI Model R² Score", value=f"{score:.2f}")

    # --- TAB 2: SMARTECH RESEARCH ASSISTANT ---
    with tab2:
        st.title("🤖 Smartech Research Assistant")
        st.caption("Ask questions about carbon capture definitions, mechanics, or specific composite settings.")

        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Welcome back! Ask me a question about carbon capture matrices or definitions."}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Ask Smartech anything..."):
            st.chat_message("user").write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            response = get_bot_response(prompt)
            
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# =====================================================================
# 5. INITIAL ENTRYPOINT
# =====================================================================
st.set_page_config(page_title="Smartech Carbon Panel", layout="wide")
authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    main_dashboard()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please log in using your administrator credentials.')
