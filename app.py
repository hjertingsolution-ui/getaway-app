import streamlit as st
from datetime import date, timedelta

# --- KONFIGURATION ---
st.set_page_config(page_title="DreamTravel Getaway", page_icon="✈️", layout="centered")

# INDSÆT DIT EGET BREDE "HERO" BILLEDE LINK HER:
HERO_IMAGE_URL = "https://unsplash.com/photos/a-sandy-beach-next-to-a-rocky-cliff-zR7WyBMZ4AQ"

# --- DESIGN MAGI (CSS) ---
st.markdown(f"""
    <style>
    /* --- GENERELT --- */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stApp {{
        background-color: #f8f9fa; /* Meget lys grå baggrund */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}
    
    /* --- HERO HEADER (Toppen) --- */
    .hero-container {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.5)), url('{HERO_IMAGE_URL}');
        background-size: cover;
        background-position: center;
        padding: 60px 20px;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-top: -60px; /* Trækker den op over standard margin */
        margin-bottom: 30px;
        color: white;
    }}
    .hero-title {{
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    .hero-subtitle {{
        font-size: 18px;
        font-weight: 400;
        opacity: 0.9;
    }}

    /* --- DESTINATIONS KORT --- */
    /* Dette styler containerne omkring hver by */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {{
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Lækker skygge */
        margin-bottom: 20px;
        transition: transform 0.2s;
    }}
    
    /* --- KNAPPER --- */
    div.stButton > button:first-child {{
        width: 100%;
        background: linear-gradient(135deg, #008080 0%, #005c5c 100%); /* Gradient farve */
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        padding: 14px 24px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,128,128,0.2);
    }}
    div.stButton > button:hover {{
        transform: scale(1.02);
    }}
    
    /* --- DATO BOKS --- */
    div[data-testid="stAlert"] {{
        background-color: #e6f2f2;
        color: #006666;
        border: none;
        border-radius: 12px;
        font-weight: bold;
    }}

    /* Justering af billeder i kortene */
    div[data-testid="stImage"] img {{
        border-radius: 12px;
    }}
    
    h3 {{ margin-top: 0; }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTIONER ---
def get_next_weekend():
    today = date.today()
    days_ahead = 4 - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    next_friday = today + timedelta(days=days_ahead)
    next_sunday = next_friday + timedelta(days=2)
    return next_friday, next_sunday

def create_travel_link(origin, destination_code, date_out, date_home):
    d_out = date_out.strftime("%d%m")
    d_home = date_home.strftime("%d%m")
    # Husk at bruge dit rigtige white label domæne her
    url = f"https://rejser.dreamtravel.dk/flights/{origin}{d_out}{destination_code}{d_home}1"
    return url

# --- DATA ---
DESTINATIONS = [
    {"name": "London", "country": "England 🇬🇧", "code": "LHR", "price_hint": "Fra 350 kr.", "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800&q=80"},
    {"name": "Berlin", "country": "Tyskland 🇩🇪", "code": "BER", "price_hint": "Fra 450 kr.", "img": "https://images.unsplash.com/photo-1599946347371-68eb71b16afc?w=800&q=80"},
    {"name": "Barcelona", "country": "Spanien 🇪🇸", "code": "BCN", "price_hint": "Fra 800 kr.", "img": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800&q=80"},
    {"name": "Rom", "country": "Italien 🇮🇹", "code": "FCO", "price_hint": "Fra 600 kr.", "img": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=80"},
]

# --- APP LAYOUT ---

# HERO SEKTION (Indsat som ren HTML for at style den)
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">DreamTravel Getaway ✈️</div>
        <div class="hero-subtitle">Din næste weekendtur starter her</div>
    </div>
    """, unsafe_allow_html=True)

# DATO & INPUT
fri, sun = get_next_weekend()
st.info(f"📅 Næste weekend: {fri.strftime('%d.')} - {sun.strftime('%d. %B')}")

lufthavn = st.selectbox("", # Tom label for renere look
                        options=["CPH", "BLL", "AAL"], 
                        format_func=lambda x: f"Rejs fra: København (CPH)" if x == "CPH" else f"Rejs fra: Billund (BLL)" if x == "BLL" else f"Rejs fra: Aalborg (AAL)")

st.write("") # Lidt luft

# DESTINATIONER (KORT DESIGN)
for dest in DESTINATIONS:
    # Vi laver en container til hvert "kort"
    with st.container():
        st.image(dest["img"], use_container_width=True)
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader(dest["name"])
            st.caption(dest["country"])
        with c2:
            # Bruger markdown for at gøre prisen grøn og fed
            st.markdown(f"<div style='color:#008080; font-weight:bold; font-size:1.2em; text-align:right;'>{dest['price_hint']}</div>", unsafe_allow_html=True)
        
        link = create_travel_link(lufthavn, dest["code"], fri, sun)
        st.link_button(f"Se fly til {dest['name']}", link)

st.caption("Priser er estimater. Klik for at se live priser på rejser.dreamtravel.dk")
