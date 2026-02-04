import streamlit as st
from datetime import date, timedelta

# --- OPSÆTNING AF APP ---
st.set_page_config(page_title="DreamTravel Getaway", page_icon="✈️", layout="centered")

# --- DESIGN & CSS (Gør det lækkert) ---
# Dette fjerner standard menuer og styler knapperne
st.markdown("""
    <style>
    /* Skjul Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Gør knapperne store og flotte */
    div.stButton > button:first-child {
        width: 100%;
        background-color: #008080; /* Teal/Turkis farve - passer til DreamTravel */
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #006666;
        color: white;
    }
    
    /* Pænere titler */
    h1 { color: #333; font-family: 'Helvetica Neue', sans-serif; }
    h3 { color: #555; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTIONER: GØR DEN SMART ---

def get_next_weekend():
    """Finder datoen for kommende fredag og søndag"""
    today = date.today()
    # 0=Monday, 4=Friday
    days_ahead = 4 - today.weekday()
    if days_ahead <= 0: # Hvis det er fredag-søndag, så find næste uge
        days_ahead += 7
    
    next_friday = today + timedelta(days=days_ahead)
    next_sunday = next_friday + timedelta(days=2)
    return next_friday, next_sunday

def create_travel_link(origin, destination_code, date_out, date_home):
    """
    Bygger linket til din White Label.
    Format: https://rejser.dreamtravel.dk/flights/CPH2005LON22051
    (Oprindelse + DagMåned + Destination + DagMåned + 1 passager)
    """
    d_out = date_out.strftime("%d%m") # F.eks. 2005 for 20. maj
    d_home = date_home.strftime("%d%m")
    
    # URL konstruktion
    url = f"https://rejser.dreamtravel.dk/flights/{origin}{d_out}{destination_code}{d_home}1"
    return url

# --- DATA: DINE DESTINATIONER ---
# Her kan du tilføje flere byer. Husk IATA koden (f.eks. LHR for London)
DESTINATIONS = [
    {
        "name": "London",
        "country": "England 🇬🇧",
        "code": "LHR", # IATA lufthavnskode
        "price_hint": "Fra 350 kr.",
        "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800&q=80"
    },
    {
        "name": "Berlin",
        "country": "Tyskland 🇩🇪",
        "code": "BER",
        "price_hint": "Fra 450 kr.",
        "img": "https://images.unsplash.com/photo-1599946347371-68eb71b16afc?w=800&q=80"
    },
    {
        "name": "Barcelona",
        "country": "Spanien 🇪🇸",
        "code": "BCN",
        "price_hint": "Fra 800 kr.",
        "img": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800&q=80"
    },
    {
        "name": "Rom",
        "country": "Italien 🇮🇹",
        "code": "FCO",
        "price_hint": "Fra 600 kr.",
        "img": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=80"
    },
    {
        "name": "Paris",
        "country": "Frankrig 🇫🇷",
        "code": "CDG",
        "price_hint": "Fra 750 kr.",
        "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=80"
    }
]

# --- APP LAYOUT ---

# Top sektion
st.title("🌍 DreamTravel Getaway")
st.write("Planlæg din næste weekendtur. Vi finder de bedste priser.")

# Dato beregning
fri, sun = get_next_weekend()
str_fri = fri.strftime("%d. %b")
str_sun = sun.strftime("%d. %b")

st.info(f"📅 **Næste weekend:** {str_fri} - {str_sun}")

# Vælg lufthavn
lufthavn = st.selectbox("Hvor rejser du fra?", 
                        options=["CPH", "BLL", "AAL"], 
                        format_func=lambda x: "København (CPH)" if x == "CPH" else "Billund (BLL)" if x == "BLL" else "Aalborg (AAL)")

st.divider()

# Vis destinationerne
for dest in DESTINATIONS:
    with st.container():
        # Billede
        st.image(dest["img"], use_container_width=True)
        
        # Info tekst
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader(dest["name"])
            st.caption(dest["country"])
        with c2:
            st.markdown(f"#### {dest['price_hint']}")
        
        # Generer det dynamiske link
        link = create_travel_link(lufthavn, dest["code"], fri, sun)
        
        # Knap
        st.link_button(f"✈️ Se fly til {dest['name']}", link)
        
        st.write("") # Lidt luft
        st.divider()

# Footer
st.caption("Priser er estimater. Klik for at se live priser på rejser.dreamtravel.dk")
