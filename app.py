import streamlit as st
from datetime import date, timedelta
import random

# --- 1. OPSÆTNING ---
st.set_page_config(page_title="Love & Travel", page_icon="❤️", layout="centered")

# --- 2. CSS STYLING (GLASSMORPHISM & BREDE KNAPPER) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Poppins:wght@400;500;600&display=swap');

    /* Baggrund: En lækker varm gradient */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        font-family: 'Poppins', sans-serif;
    }

    /* Skjul standard ting */
    #MainMenu, footer, header {visibility: hidden;}

    /* --- TYPOGRAFI --- */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #2c3e50;
    }
    
    .hero-title {
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        color: #1A1A1A;
        margin-bottom: 5px;
    }
    .hero-subtitle {
        font-size: 16px;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
        font-style: italic;
    }

    /* --- GLASSMORPHISM KORT --- */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }

    div[data-testid="stImage"] img {
        border-radius: 15px;
        object-fit: cover;
        height: 220px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* --- KNAPPER --- */
    div.stButton > button:first-child {
        width: 100%;
        background: linear-gradient(45deg, #1A1A1A, #4a4a4a);
        color: white;
        font-size: 15px;
        font-weight: 600;
        border-radius: 50px;
        padding: 12px 24px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        background: linear-gradient(45deg, #000, #333);
    }

    /* --- PRIS TAG --- */
    .price-tag {
        background-color: #f8f9fa;
        padding: 5px 12px;
        border-radius: 10px;
        font-weight: 700;
        color: #2c3e50;
        font-size: 16px;
        display: inline-block;
        border: 1px solid #eee;
    }

    /* --- TABS STYLING (OPDATERET: BREDE KNAPPER) --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        width: 100%; /* Sikrer containeren fylder ud */
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.6); /* Lidt gennemsigtig */
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        color: #555;
        font-weight: 600;
        font-size: 16px;
        flex: 1; /* MAGIEN: Dette tvinger knapperne til at dele pladsen ligeligt (50/50) */
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Den aktive fane */
    .stTabs [aria-selected="true"] {
        background-color: #1A1A1A !important;
        color: white !important;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNKTIONER ---

def calculate_dates(duration_type):
    today = date.today()
    days_until_friday = 4 - today.weekday()
    if days_until_friday <= 0: days_until_friday += 7
    friday = today + timedelta(days=days_until_friday)
    
    if duration_type == "Weekend (Fre-Søn)":
        outbound = friday
        inbound = friday + timedelta(days=2)
    elif duration_type == "Forlænget (Tors-Søn)":
        outbound = friday - timedelta(days=1)
        inbound = friday + timedelta(days=2)
    else: # 5 Dage (Ons-Søn)
        outbound = friday - timedelta(days=2)
        inbound = friday + timedelta(days=2)
        
    return outbound, inbound

def create_travel_link(origin, destination_code, date_out, date_home):
    d_out = date_out.strftime("%d%m")
    d_home = date_home.strftime("%d%m")
    return f"https://rejser.dreamtravel.dk/flights/{origin}{d_out}{destination_code}{d_home}1"

# --- 4. DATA ---

DESTINATIONS = [
    {"name": "Paris", "country": "Frankrig", "code": "CDG", "price": "750 kr.", "tag": "Romantik", "desc": "Byernes by - perfekt til par.", "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=80"},
    {"name": "Venedig", "country": "Italien", "code": "VCE", "price": "950 kr.", "tag": "Romantik", "desc": "Gondoltur og italiensk middag.", "img": "https://images.unsplash.com/photo-1514890547357-a9ee288728e0?w=800&q=80"},
    {"name": "Rom", "country": "Italien", "code": "FCO", "price": "600 kr.", "tag": "Kultur", "desc": "Evig kærlighed i den evige stad.", "img": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=80"},
    {"name": "Budapest", "country": "Ungarn", "code": "BUD", "price": "450 kr.", "tag": "Spa", "desc": "Luksus spa-ophold til lavpris.", "img": "https://images.unsplash.com/photo-1565426873118-a1dfa58f877d?w=800&q=80"},
    {"name": "Prag", "country": "Tjekkiet", "code": "PRG", "price": "400 kr.", "tag": "Budget", "desc": "Brostensgader og hygge.", "img": "https://images.unsplash.com/photo-1541849546-2165492d06b1?w=800&q=80"},
    {"name": "Santorini", "country": "Grækenland", "code": "JTR", "price": "1.800 kr.", "tag": "Luksus", "desc": "Solnedgang og hvide huse.", "img": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&q=80"},
]

GIFTS = {
    "Hende": [
        {"name": "Luksus Spa Dag", "brand": "DuGlemmerDetAldrig", "price": "899,-", "img": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=600", "link": "LINK_HER"},
        {"name": "Parfume Abonnement", "brand": "Goodiebox", "price": "199,-", "img": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=600", "link": "LINK_HER"},
        {"name": "Weekendtaske Læder", "brand": "CarrieAlong", "price": "1.200,-", "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600", "link": "LINK_HER"},
    ],
    "Ham": [
        {"name": "Kør Lamborghini", "brand": "DuGlemmerDetAldrig", "price": "1.495,-", "img": "https://images.unsplash.com/photo-1544614471-ebc48f6d1311?w=600", "link": "LINK_HER"},
        {"name": "Gin Smagning", "brand": "Smagning.dk", "price": "399,-", "img": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=600", "link": "LINK_HER"},
        {"name": "Støjdæmpende høretelefoner", "brand": "Proshop", "price": "1.800,-", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600", "link": "LINK_HER"},
    ]
}

# --- 5. APP UI LAYOUT ---

# HEADER
st.markdown("""
    <div class="hero-title">DreamTravel ❤️</div>
    <div class="hero-subtitle">Romantiske getaways & gaver til din yndlingsperson</div>
""", unsafe_allow_html=True)

# TABS (Hovedmenu)
tab_rejser, tab_gaver = st.tabs(["✈️ Rejser", "🎁 Gaveidéer"])

# --- FANE 1: REJSER ---
with tab_rejser:
    st.write("") 
    
    # 1. Konfiguration
    c1, c2 = st.columns([1, 1])
    with c1:
        origin = st.selectbox("Afrejse", ["CPH", "BLL", "AAL"], format_func=lambda x: f"📍 {x}")
    with c2:
        duration = st.selectbox("Varighed", ["Weekend (Fre-Søn)", "Forlænget (Tors-Søn)", "Miniferie (Ons-Søn)"])

    # Beregn datoer
    date_out, date_home = calculate_dates(duration)
    st.caption(f"📅 Næste tur: {date_out.day}/{date_out.month} - {date_home.day}/{date_home.month}")
    
    st.write("") # Lidt luft

    # 2. Vis Rejser
    for dest in DESTINATIONS:
        with st.container():
            st.image(dest["img"], use_container_width=True)
            
            t1, t2 = st.columns([2, 1])
            with t1:
                st.subheader(dest["name"])
                st.markdown(f"<span style='color:#666; font-size:14px;'>{dest['desc']}</span>", unsafe_allow_html=True)
            with t2:
                st.markdown(f"<div style='text-align:right;'><span class='price-tag'>{dest['price']}</span></div>", unsafe_allow_html=True)
            
            link = create_travel_link(origin, dest["code"], date_out, date_home)
            st.link_button(f"Book {duration.split(' ')[0]} i {dest['name']} ➝", link)

# --- FANE 2: GAVEIDÉER ---
with tab_gaver:
    st.write("")
    st.info("💡 Mangler du gaven til turen? Her er vores favoritter.")
    
    gift_gender = st.radio("Hvem er gaven til?", ["Hende", "Ham"], horizontal=True)
    
    st.write("")
    
    selected_gifts = GIFTS[gift_gender]
    
    for gift in selected_gifts:
        with st.container():
            c_img, c_txt = st.columns([1, 2])
            
            with c_img:
                st.image(gift["img"], use_container_width=True)
            
            with c_txt:
                st.subheader(gift["name"])
                st.caption(f"Fra {gift['brand']}")
                st.markdown(f"**{gift['price']}**")
                st.link_button("Køb nu 🎁", gift["link"])
