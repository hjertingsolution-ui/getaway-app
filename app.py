import streamlit as st
from datetime import date, timedelta

# --- 1. OPSÆTNING ---
st.set_page_config(page_title="DreamTravel", page_icon="✈️", layout="centered")

# --- 2. CSS STYLING (Travy Look) ---
st.markdown("""
    <style>
    /* --- IMPORT AF SKRIFTTYPE (Google Fonts - Poppins for det moderne look) --- */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* --- BAGGRUND --- */
    .stApp {
        background-color: #F2F5F8; /* Lys grå/blålig baggrund som i designet */
    }

    /* --- SKJUL STANDARD ELEMENTER --- */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* --- HEADER / TITEL --- */
    .header-text {
        font-size: 28px;
        font-weight: 700;
        color: #1A1A1A;
        margin-bottom: 5px;
    }
    .sub-header-text {
        font-size: 16px;
        color: #888;
        margin-bottom: 20px;
    }

    /* --- KATEGORI PILLS (HTML) --- */
    .category-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        overflow-x: auto;
        padding-bottom: 5px;
    }
    .category-pill {
        background-color: #fff;
        color: #888;
        padding: 8px 20px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: 600;
        border: 1px solid #eee;
        white-space: nowrap;
    }
    .category-pill.active {
        background-color: #1A1A1A; /* Sort aktiv knap */
        color: #fff;
        border: 1px solid #1A1A1A;
    }

    /* --- KORT DESIGN (Container hack) --- */
    /* Vi styler Streamlits containere til at ligne kort */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background-color: white;
        border-radius: 24px; /* Store runde hjørner */
        padding: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04); /* Meget blød skygge */
        margin-bottom: 25px;
        border: 1px solid #fff;
    }

    /* --- BILLEDER --- */
    div[data-testid="stImage"] img {
        border-radius: 20px; /* Runde hjørner på billeder */
        object-fit: cover;
        margin-bottom: 10px;
    }

    /* --- KNAPPER --- */
    div.stButton > button:first-child {
        width: 100%;
        background-color: #1A1A1A; /* Sort knap for kontrast */
        color: white;
        font-size: 16px;
        font-weight: 600;
        border-radius: 20px; /* Pille-form */
        padding: 12px 24px;
        border: none;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #333;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    div.stButton > button:active {
        background-color: #000;
    }

    /* --- PRIS OG TEKST I KORT --- */
    h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 18px !important;
        margin-bottom: 0px;
        padding-top: 5px;
    }
    p {
        color: #888;
        font-size: 14px;
    }
    
    /* --- SELECTBOX (INPUT) --- */
    div[data-baseweb="select"] > div {
        background-color: #fff;
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNKTIONER ---
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
    url = f"https://rejser.dreamtravel.dk/flights/{origin}{d_out}{destination_code}{d_home}1"
    return url

# --- 4. DATA ---
DESTINATIONS = [
    {"name": "London", "country": "United Kingdom", "code": "LHR", "price": "350 kr.", "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800&q=80"},
    {"name": "Berlin", "country": "Tyskland", "code": "BER", "price": "450 kr.", "img": "https://images.unsplash.com/photo-1599946347371-68eb71b16afc?w=800&q=80"},
    {"name": "Barcelona", "country": "Spanien", "code": "BCN", "price": "800 kr.", "img": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800&q=80"},
    {"name": "Rom", "country": "Italien", "code": "FCO", "price": "600 kr.", "img": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=80"},
    {"name": "Paris", "country": "Frankrig", "code": "CDG", "price": "750 kr.", "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=80"}
]

# --- 5. APP UI (Layout) ---

# Custom Header (HTML)
st.markdown("""
    <div class="header-text">DreamTravel 🌍</div>
    <div class="sub-header-text">Find din næste weekendtur</div>
    
    <div class="category-container">
        <div class="category-pill active">All</div>
        <div class="category-pill">Popular</div>
        <div class="category-pill">Recommended</div>
        <div class="category-pill">Europe</div>
    </div>
""", unsafe_allow_html=True)

# Dato & Input
fri, sun = get_next_weekend()

# Vi bruger columns til at skabe lidt luft omkring inputfeltet
c1, c2 = st.columns([3, 1])
with c1:
    lufthavn = st.selectbox("Rejs fra", ["CPH", "BLL", "AAL"], 
                            format_func=lambda x: f"📍 {x} (København)" if x == "CPH" else f"📍 {x} (Billund)" if x == "BLL" else f"📍 {x} (Aalborg)")
with c2:
    st.write("") # Spacer
    st.markdown(f"<div style='text-align:center; padding-top:10px; font-weight:bold; color:#888;'>{fri.day}/{fri.month}</div>", unsafe_allow_html=True)

st.write("") # Lidt luft

# --- DESTINATIONS KORT (LOOP) ---
for dest in DESTINATIONS:
    
    # Her opretter vi "Kortet"
    with st.container():
        # 1. Billede (Fuld bredde i kortet)
        st.image(dest["img"], use_container_width=True)
        
        # 2. Info sektion (Tekst til venstre, Pris til højre)
        col_text, col_price = st.columns([2, 1])
        
        with col_text:
            st.subheader(dest["name"])
            st.markdown(f"<p style='margin-top:-5px;'>{dest['country']}</p>", unsafe_allow_html=True)
            
        with col_price:
            # Pris som en "Highlight"
            st.markdown(f"<div style='text-align:right; font-weight:700; font-size:18px; color:#1A1A1A; margin-top:5px;'>{dest['price']}</div>", unsafe_allow_html=True)
        
        # 3. Knappen (Action)
        link = create_travel_link(lufthavn, dest["code"], fri, sun)
        st.link_button("Book Now ➝", link)
