import streamlit as st
from datetime import date, timedelta
import random

# --- 1. OPSÆTNING ---
st.set_page_config(page_title="DreamTravel", page_icon="✈️", layout="centered")

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background-color: #F2F5F8;
    }

    #MainMenu, footer, header {visibility: hidden;}
    
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

    /* --- PILLS DESIGN (Kategorier) --- */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        gap: 10px;
        overflow-x: auto;
        padding-bottom: 5px;
    }
    
    div[role="radiogroup"] label {
        background-color: white !important;
        padding: 8px 20px !important;
        border-radius: 25px !important;
        border: 1px solid #eee !important;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        min-width: fit-content;
    }

    div[role="radiogroup"] label p {
        color: #555 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    div[role="radiogroup"] label[data-checked="true"] {
        background-color: #1A1A1A !important;
        border-color: #1A1A1A !important;
    }
    div[role="radiogroup"] label[data-checked="true"] p {
        color: white !important;
    }

    div[role="radiogroup"] label > div:first-child {
        display: none !important;
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
        height: 200px !important;
    }

    /* --- KNAPPER --- */
    div.stButton > button:first-child {
        width: 100%;
        background-color: #1A1A1A;
        color: white;
        font-size: 15px;
        font-weight: 600;
        border-radius: 20px;
        padding: 12px 20px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #333;
        transform: translateY(-2px);
    }
    
    .price-tag {
        text-align: right; 
        font-weight: 700; 
        font-size: 18px; 
        color: #1A1A1A; 
        margin-top: 5px;
    }
    
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

# --- 4. DATA (MED WELLNESS) ---
DESTINATIONS = [
    {
        "name": "Budapest", "country": "Ungarn 🇭🇺", "code": "BUD", "price": "600 kr.", 
        "tags": ["Wellness", "Storby", "Populær", "Alle"], "desc": "Termiske bade & spa",
        "img": "https://images.unsplash.com/photo-1565426873118-a1dfa58f877d?w=800&q=80"
    },
    {
        "name": "Reykjavik", "country": "Island 🇮🇸", "code": "KEF", "price": "1.800 kr.", 
        "tags": ["Wellness", "Populær", "Alle"], "desc": "Den Blå Lagune & natur",
        "img": "https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=800&q=80"
    },
    {
        "name": "Gdansk", "country": "Polen 🇵🇱", "code": "GDN", "price": "350 kr.", 
        "tags": ["Wellness", "Storby", "Alle"], "desc": "Luksus spa-hoteller",
        "img": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800&q=80"
    },
    {
        "name": "London", "country": "England 🇬🇧", "code": "LHR", "price": "350 kr.", 
        "tags": ["Storby", "Populær", "Alle"], "desc": "Shopping, pubs & fodbold",
        "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800&q=80"
    },
    {
        "name": "Malaga", "country": "Spanien 🇪🇸", "code": "AGP", "price": "950 kr.", 
        "tags": ["Sol & Strand", "Populær", "Alle"], "desc": "Solkysten & tapas",
        "img": "https://images.unsplash.com/photo-1565259972852-6b95c029676e?w=800&q=80"
    },
    {
        "name": "Berlin", "country": "Tyskland 🇩🇪", "code": "BER", "price": "450 kr.", 
        "tags": ["Storby", "Alle"], "desc": "Kultur, historie & natteliv",
        "img": "https://images.unsplash.com/photo-1599946347371-68eb71b16afc?w=800&q=80"
    },
    {
        "name": "Nice", "country": "Frankrig 🇫🇷", "code": "NCE", "price": "1.100 kr.", 
        "tags": ["Sol & Strand", "Alle"], "desc": "Den Franske Riviera",
        "img": "https://images.unsplash.com/photo-1533644265780-3575b630dc07?w=800&q=80"
    },
    {
        "name": "Barcelona", "country": "Spanien 🇪🇸", "code": "BCN", "price": "800 kr.", 
        "tags": ["Sol & Strand", "Storby", "Populær", "Alle"], "desc": "Strand møder storby",
        "img": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800&q=80"
    },
    {
        "name": "Rom", "country": "Italien 🇮🇹", "code": "FCO", "price": "600 kr.", 
        "tags": ["Storby", "Populær", "Alle"], "desc": "Pasta, vin & historie",
        "img": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=80"
    }
]

# --- 5. APP UI ---

# Header med Surprise Knap
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
        <div class="header-text">DreamTravel 🌍</div>
        <div class="sub-header-text">Find din næste rejse</div>
    """, unsafe_allow_html=True)
with col_h2:
    if st.button("🎲 Prøv lykken"):
        # Vi gemmer valget i session_state, så det huskes!
        st.session_state['surprise_city'] = random.choice(DESTINATIONS)
        # Vi sletter eventuelt valgt kategori for at fokusere på overraskelsen
        st.session_state['kategori_valg'] = "Alle"

# KATEGORI VÆLGER
# Opdateret med Wellness
kategori = st.radio(
    "Vælg kategori", 
    ["Alle", "Populær", "Storby", "Sol & Strand", "Wellness"], 
    horizontal=True,
    label_visibility="collapsed",
    key='kategori_valg' # Nøgle så vi kan nulstille den
)

st.write("") 

# DATO & INPUT
fri, sun = get_next_weekend()
c1, c2 = st.columns([3, 1])
with c1:
    lufthavn = st.selectbox("Afrejse", ["CPH", "BLL", "AAL"], 
                            format_func=lambda x: f"📍 {x} (København)" if x == "CPH" else f"📍 {x} (Billund)" if x == "BLL" else f"📍 {x} (Aalborg)")
with c2:
    st.write("") 
    st.markdown(f"<div style='text-align:center; padding-top:10px; font-weight:bold; color:#888;'>{fri.day}/{fri.month}</div>", unsafe_allow_html=True)

st.write("")

# --- LOGIK: SURPRISE ---

# Tjek om vi har en surprise gemt i hukommelsen
if 'surprise_city' in st.session_state and st.session_state['surprise_city']:
    surp = st.session_state['surprise_city']
    
    # Vis en speciel boks
    st.info(f"✨ Skæbnen foreslår: **{surp['name']}**! ✨")
    
    with st.container():
        st.image(surp["img"], use_container_width=True)
        t1, t2 = st.columns([2, 1])
        with t1:
            st.subheader(surp["name"])
            st.markdown(f"<p style='margin-top:-5px; color:#555;'>{surp['desc']}</p>", unsafe_allow_html=True)
        with t2:
            st.markdown(f"<div class='price-tag'>{surp['price']}</div>", unsafe_allow_html=True)
        
        link = create_travel_link(lufthavn, surp["code"], fri, sun)
        st.link_button(f"Ja tak! Book {surp['name']} ➝", link)
    
    # Knap til at fjerne overraskelsen og se listen igen
    if st.button("❌ Luk og vis alle rejser"):
        del st.session_state['surprise_city']
        st.rerun() # Genstart siden for at fjerne boksen
    
    st.divider()
    st.caption("Eller vælg selv herunder:")

# --- FILTRERING AF LISTE ---
vis_liste = [d for d in DESTINATIONS if kategori in d["tags"]]

if not vis_liste:
    st.info("Ingen rejser fundet i denne kategori lige nu.")

for dest in vis_liste:
    with st.container():
        st.image(dest["img"], use_container_width=True)
        
        col_text, col_price = st.columns([2, 1])
        with col_text:
            st.subheader(dest["name"])
            st.markdown(f"<p style='margin-top:-5px; font-size:14px; color:#666;'>{dest['country']} • {dest['desc']}</p>", unsafe_allow_html=True)
            
        with col_price:
            st.markdown(f"<div class='price-tag'>{dest['price']}</div>", unsafe_allow_html=True)
        
        link = create_travel_link(lufthavn, dest["code"], fri, sun)
        st.link_button("Se flybilletter ➝", link)
