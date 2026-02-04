import streamlit as st
from datetime import date, timedelta

# --- 1. OPSÆTNING ---
st.set_page_config(page_title="DreamTravel", page_icon="✈️", layout="centered")

# --- 2. CSS STYLING (Travy Look + Aktive Radio Knapper) ---
st.markdown("""
    <style>
    /* Import af font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background-color: #F2F5F8; /* Travy baggrundsfarve */
    }

    /* Skjul standard ting */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Header Tekst */
    .header-text {
        font-size: 28px;
        font-weight: 700;
        color: #1A1A1A;
        margin-bottom: 0px;
    }
    .sub-header-text {
        font-size: 16px;
        color: #888;
        margin-bottom: 20px;
    }

    /* --- PILLS DESIGN (Hacker st.radio til at ligne knapper) --- */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        gap: 10px;
        overflow-x: auto;
    }
    
    div[role="radiogroup"] label {
        background-color: white;
        padding: 8px 20px;
        border-radius: 25px;
        border: 1px solid #eee;
        color: #888;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        cursor: pointer;
    }

    /* Når en knap er valgt (Aktiv) */
    div[role="radiogroup"] label[data-checked="true"] {
        background-color: #1A1A1A !important;
        color: white !important;
        border: 1px solid #1A1A1A !important;
    }

    div[role="radiogroup"] label:hover {
        border-color: #ccc;
    }

    /* Skjul den lille cirkel i radio-knappen */
    div[role="radiogroup"] label div:first-child {
        display: none;
    }

    /* --- KORT DESIGN --- */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background-color: white;
        border-radius: 24px;
        padding: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        margin-bottom: 25px;
        border: 1px solid #fff;
    }

    div[data-testid="stImage"] img {
        border-radius: 20px;
        object-fit: cover;
    }

    /* --- KNAPPER (Sort Travy stil) --- */
    div.stButton > button:first-child {
        width: 100%;
        background-color: #1A1A1A;
        color: white;
        font-size: 15px;
        font-weight: 600;
        border-radius: 20px;
        padding: 12px 20px;
        border: none;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        background-color: #333;
        transform: translateY(-2px);
    }

    /* Pris styling */
    .price-tag {
        text-align: right; 
        font-weight: 700; 
        font-size: 18px; 
        color: #1A1A1A; 
        margin-top: 5px;
    }
    
    /* Input felter */
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
    if days_ahead <= 0: days_ahead += 7
    next_friday = today + timedelta(days=days_ahead)
    next_sunday = next_friday + timedelta(days=2)
    return next_friday, next_sunday

def create_travel_link(origin, destination_code, date_out, date_home):
    d_out = date_out.strftime("%d%m")
    d_home = date_home.strftime("%d%m")
    return f"https://rejser.dreamtravel.dk/flights/{origin}{d_out}{destination_code}{d_home}1"

# --- 4. DATA (Med kategorier) ---
# Kategorier: "Storby", "Sol & Strand", "Populær"
DESTINATIONS = [
    {
        "name": "London", "country": "United Kingdom", "code": "LHR", "price": "350 kr.", 
        "tags": ["Storby", "Populær"],
        "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800&q=80"
    },
    {
        "name": "Berlin", "country": "Tyskland", "code": "BER", "price": "450 kr.", 
        "tags": ["Storby"],
        "img": "https://images.unsplash.com/photo-1599946347371-68eb71b16afc?w=800&q=80"
    },
    {
        "name": "Barcelona", "country": "Spanien", "code": "BCN", "price": "800 kr.", 
        "tags": ["Sol & Strand", "Storby", "Populær"],
        "img": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800&q=80"
    },
    {
        "name": "Malaga", "country": "Spanien", "code": "AGP", "price": "950 kr.", 
        "tags": ["Sol & Strand", "Populær"],
        "img": "https://images.unsplash.com/photo-1565259972852-6b95c029676e?w=800&q=80"
    },
    {
        "name": "Nice", "country": "Frankrig", "code": "NCE", "price": "1.100 kr.", 
        "tags": ["Sol & Strand"],
        "img": "https://images.unsplash.com/photo-1533644265780-3575b630dc07?w=800&q=80"
    },
    {
        "name": "Rom", "country": "Italien", "code": "FCO", "price": "600 kr.", 
        "tags": ["Storby", "Populær"],
        "img": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=80"
    },
    {
        "name": "Paris", "country": "Frankrig", "code": "CDG", "price": "750 kr.", 
        "tags": ["Storby"],
        "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=80"
    }
]

# --- 5. APP UI ---

# Header
st.markdown("""
    <div class="header-text">DreamTravel 🌍</div>
    <div class="sub-header-text">Find din næste weekendtur</div>
""", unsafe_allow_html=True)

# KATEGORI VÆLGER (Styleret som Pills)
# Vi bruger st.radio, men CSS gør dem til knapper
kategori = st.radio(
    "Vælg kategori", 
    ["Alle", "Populær", "Storby", "Sol & Strand"], 
    horizontal=True,
    label_visibility="collapsed"
)

st.write("") # Lidt luft

# Dato & Input
fri, sun = get_next_weekend()

c1, c2 = st.columns([3, 1])
with c1:
    lufthavn = st.selectbox("Afrejse", ["CPH", "BLL", "AAL"], 
                            format_func=lambda x: f"📍 {x} (København)" if x == "CPH" else f"📍 {x} (Billund)" if x == "BLL" else f"📍 {x} (Aalborg)")
with c2:
    st.write("") 
    st.markdown(f"<div style='text-align:center; padding-top:10px; font-weight:bold; color:#888;'>{fri.day}/{fri.month}</div>", unsafe_allow_html=True)

st.write("")

# --- FILTRERING OG VISNING ---

# Filtrer listen baseret på valgt kategori
vis_liste = []
for d in DESTINATIONS:
    if kategori == "Alle" or kategori in d["tags"]:
        vis_liste.append(d)

if not vis_liste:
    st.info("Ingen rejser fundet i denne kategori lige nu.")

# Loop gennem de filtrerede rejser
for dest in vis_liste:
    with st.container():
        st.image(dest["img"], use_container_width=True)
        
        col_text, col_price = st.columns([2, 1])
        with col_text:
            st.subheader(dest["name"])
            st.markdown(f"<p style='margin-top:-5px;'>{dest['country']}</p>", unsafe_allow_html=True)
            
        with col_price:
            st.markdown(f"<div class='price-tag'>{dest['price']}</div>", unsafe_allow_html=True)
        
        link = create_travel_link(lufthavn, dest["code"], fri, sun)
        st.link_button("Se flybilletter ➝", link)
