import streamlit as st
from datetime import date, timedelta
import random

# --- 1. OPSÆTNING ---
st.set_page_config(page_title="Love & Travel", page_icon="❤️", layout="centered")

# --- 2. CSS STYLING (GLASSMORPHISM & UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Poppins:wght@400;500;600&display=swap');

    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        font-family: 'Poppins', sans-serif;
    }

    #MainMenu, footer, header {visibility: hidden;}

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

    /* KORT DESIGN */
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

    /* KNAPPER */
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
    
    /* Sekundær knap (Luk Surprise) */
    div.stButton > button.secondary {
        background: transparent;
        border: 1px solid #ccc;
        color: #555;
        box-shadow: none;
    }

    /* PRIS TAG */
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

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        width: 100%;
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.6);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        color: #555;
        font-weight: 600;
        font-size: 16px;
        flex: 1;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stTabs [aria-selected="true"] {
        background-color: #1A1A1A !important;
        color: white !important;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* KATEGORI KNAPPER (Radio - Pills Style) */
    div[role="radiogroup"] {
        display: flex;
        flex-wrap: wrap; /* Tillad ombrydning på små skærme */
        justify-content: center;
        gap: 8px;
    }
    div[role="radiogroup"] label {
        background-color: white !important;
        border: 1px solid #eee;
        padding: 8px 16px;
        border-radius: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        flex: 1;
        min-width: fit-content;
        justify-content: center;
        text-align: center;
    }
    div[role="radiogroup"] label[data-checked="true"] {
        background-color: #1A1A1A !important;
        color: white !important;
        border-color: #1A1A1A;
    }
    div[role="radiogroup"] label p {
        font-weight: 600;
        font-size: 13px;
        margin: 0px;
    }
    div[role="radiogroup"] label[data-checked="true"] p {
        color: white !important;
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

# REJSER (Nu med Sverige, Norge og rettede billeder)
DESTINATIONS = [
    {"name": "Sverige (Stockholm)", "country": "Sverige 🇸🇪", "code": "ARN", "price": "450 kr.", "tags": ["Wellness", "Storby"], "desc": "Skærgård, natur og spa-hoteller.", "img": "https://images.unsplash.com/photo-1509356843151-3e7d96241e11?w=800&q=80"},
    {"name": "Norge (Oslo)", "country": "Norge 🇳🇴", "code": "OSL", "price": "600 kr.", "tags": ["Wellness", "Storby"], "desc": "Fjelde, fjorde og frisk luft.", "img": "https://images.unsplash.com/photo-1507272931001-fc06c17e4f43?w=800&q=80"},
    {"name": "Budapest", "country": "Ungarn 🇭🇺", "code": "BUD", "price": "450 kr.", "tags": ["Wellness", "Storby"], "desc": "Termiske bade og spa-luksus.", "img": "https://images.unsplash.com/photo-1549877452-9c387954fbc2?w=800&q=80"}, # NYT BILLEDE
    {"name": "Malaga", "country": "Spanien 🇪🇸", "code": "AGP", "price": "950 kr.", "tags": ["Sol & Strand", "Storby"], "desc": "Solkysten og lækker tapas.", "img": "https://images.unsplash.com/photo-1582234032585-86d389a4242e?w=800&q=80"}, # NYT BILLEDE
    {"name": "Paris", "country": "Frankrig 🇫🇷", "code": "CDG", "price": "750 kr.", "tags": ["Romantik", "Storby"], "desc": "Byernes by - perfekt til par.", "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=80"},
    {"name": "Gdansk", "country": "Polen 🇵🇱", "code": "GDN", "price": "350 kr.", "tags": ["Wellness", "Storby"], "desc": "Billig spa og smuk havn.", "img": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800&q=80"},
    {"name": "Venedig", "country": "Italien 🇮🇹", "code": "VCE", "price": "950 kr.", "tags": ["Romantik"], "desc": "Gondoltur og italiensk middag.", "img": "https://images.unsplash.com/photo-1514890547357-a9ee288728e0?w=800&q=80"},
    {"name": "Rom", "country": "Italien 🇮🇹", "code": "FCO", "price": "600 kr.", "tags": ["Kultur", "Storby", "Romantik"], "desc": "Evig kærlighed i den evige stad.", "img": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=80"},
    {"name": "Prag", "country": "Tjekkiet 🇨🇿", "code": "PRG", "price": "400 kr.", "tags": ["Storby", "Budget"], "desc": "Brostensgader og hygge.", "img": "https://images.unsplash.com/photo-1519677100203-a0e668c92439?w=800&q=80"},
    {"name": "Santorini", "country": "Grækenland 🇬🇷", "code": "JTR", "price": "1.800 kr.", "tags": ["Luksus", "Sol & Strand", "Romantik"], "desc": "Solnedgang og hvide huse.", "img": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&q=80"},
]

# GAVER
GIFTS = {
    "Til Hende": [
        {"name": "Luksus Gavekurve", "brand": "Gaestus", "price": "Forkælelse", "img": "https://images.unsplash.com/photo-1512909006721-3d6018887383?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=93733"},
        {"name": "Økologisk Hudpleje", "brand": "Naturligolie.dk", "price": "Fra 249,-", "img": "https://images.unsplash.com/photo-1616683693504-3ea7e9ad6fec?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=58130"},
        {"name": "Personlig Indgravering", "brand": "Dahls Gravering", "price": "Unik gave", "img": "https://images.unsplash.com/photo-1617038220319-88af1505d7b1?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=107810"},
        {"name": "Australian Bodycare", "brand": "Tea Tree Oil", "price": "Fra 99,-", "img": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=52884"},
    ],
    "Til Ham": [
        {"name": "Alt til Fodboldfans", "brand": "Fodboldgaver.dk", "price": "Merchandise", "img": "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=115924"},
        {"name": "Zippo & Lightere", "brand": "LighterLand", "price": "Cool Gadgets", "img": "https://images.unsplash.com/photo-1595167332289-54b6d4826848?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=90007"},
        {"name": "Elektronik & Gadgets", "brand": "Proshop", "price": "Kæmpe udvalg", "img": "https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=67785"},
        {"name": "Outdoor Udstyr", "brand": "Pro Outdoor", "price": "Til Eventyret", "img": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=42820"},
        {"name": "Barbering & Pleje", "brand": "Shavesafe", "price": "Fra 149,-", "img": "https://images.unsplash.com/photo-1621607512214-68297480165e?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=75729"},
        {"name": "Gourmet Kaffe", "brand": "KaffeImperiet", "price": "Luksus bønner", "img": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=114886"},
    ],
    "For Begge": [
        {"name": "Eksklusiv Vinklub", "brand": "RareWine Trading", "price": "Investér i vin", "img": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=114954"},
        {"name": "Spa & Wellness Ophold", "brand": "Hotel Viking", "price": "Luksus", "img": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=77692"},
        {"name": "Kærlighed & Leg", "brand": "Private Play", "price": "Frække gaver", "img": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=84227"},
        {"name": "Sjov 'Depresso' Kaffe", "brand": "Depresso Coffee", "price": "Fra 129,-", "img": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600", "link": "https://www.partner-ads.com/dk/klikbanner.php?partnerid=20107&bannerid=79802"},
    ]
}

# --- 5. APP UI LAYOUT ---

st.markdown("""
    <div class="hero-title">DreamTravel ❤️</div>
    <div class="hero-subtitle">Romantiske getaways & gaver til din yndlingsperson</div>
""", unsafe_allow_html=True)

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

    date_out, date_home = calculate_dates(duration)
    st.caption(f"📅 Næste tur: {date_out.day}/{date_out.month} - {date_home.day}/{date_home.month}")
    
    st.divider()

    # --- FILTER KNAPPER ---
    travel_category = st.radio(
        "Filtrer efter type:", 
        ["Alle", "Romantik", "Wellness", "Storby", "Sol & Strand"], 
        horizontal=True,
        label_visibility="collapsed"
    )
    st.write("") 

    # --- PRØV LYKKEN SEKTION ---
    if st.button("🎲 Prøv lykken - Vælg for os"):
        st.session_state['surprise_city'] = random.choice(DESTINATIONS)
    
    # Vis Surprise Kort
    if 'surprise_city' in st.session_state:
        surp = st.session_state['surprise_city']
        
        st.info(f"✨ Vi har valgt en romantisk tur til **{surp['name']}**! ✨")
        
        with st.container():
            st.image(surp["img"], use_container_width=True)
            t1, t2 = st.columns([2, 1])
            with t1:
                st.subheader(surp["name"])
                st.markdown(f"*{surp['desc']}*")
            with t2:
                st.markdown(f"<div style='text-align:right;'><span class='price-tag'>{surp['price']}</span></div>", unsafe_allow_html=True)
            
            link = create_travel_link(origin, surp["code"], date_out, date_home)
            st.link_button(f"Ja tak! Book {surp['name']} ➝", link)
            
            if st.button("❌ Luk (Vis alle)", key="close_surprise", type="secondary"):
                del st.session_state['surprise_city']
                st.rerun()
        
        st.divider()
        st.caption("Eller vælg selv fra listen:")

    # 2. Vis Rejser (Filtreret)
    
    # Filter logik
    filtered_destinations = []
    for d in DESTINATIONS:
        if travel_category == "Alle":
            filtered_destinations.append(d)
        elif travel_category in d["tags"]:
            filtered_destinations.append(d)
    
    if not filtered_destinations:
        st.info("Ingen rejser fundet i denne kategori.")
    
    for dest in filtered_destinations:
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
    st.info("💡 Forkæl din partner før rejsen (eller bare fordi)")
    
    # Kategori vælger (Knapper)
    gift_category = st.radio(
        "Kategori", 
        ["Til Hende", "For Begge", "Til Ham"], 
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.write("")
    
    # Hent gaver fra den valgte kategori
    selected_gifts = GIFTS[gift_category]
    
    # Vis gaver
    for gift in selected_gifts:
        with st.container():
            c_img, c_txt = st.columns([1, 2])
            
            with c_img:
                st.image(gift["img"], use_container_width=True)
            
            with c_txt:
                st.subheader(gift["name"])
                st.caption(f"{gift['brand']}")
                # Pris som fed tekst
                st.markdown(f"**{gift['price']}**")
                
                # Affiliate Link Knap
                st.link_button("Gå til butik 🎁", gift["link"])
