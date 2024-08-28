import streamlit as st
from gradio_client import Client, handle_file

# Initiera Gradio-klienten med ditt önskade endpoint
client = Client("Kwai-Kolors/Kolors-Virtual-Try-On")

# Övergripande stil för appen, inklusive bakgrundsfärg, typografi, och layout
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
        padding: 2rem;
    }
    .stButton>button {
        background-color: #000000;
        color: white;
        border-radius: 25px;
        padding: 10px 20px;
        font-size: 1rem;
        width: 50%;
        display: block;
        margin: 20px auto;
    }
    .stButton>button:hover {
        background-color: #333333;
        color: #ffffff;
    }
    .header-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333333;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .subheader-text {
        font-size: 1rem;
        color: #666666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .divider {
        margin: 2rem 0;
        height: 1px;
        background-color: #ddd;
    }
    .icon-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        color: #333333;
        margin-bottom: 1rem;
    }
    .image-preview {
        display: block;
        margin-left: auto;
        margin-right: auto;
        height: 200px;
        width: 200px;
        object-fit: cover;
        border: 1px solid #ddd;
        border-radius: 10px;
    }
    .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .logo img {
        max-width: 200px;
    }
    @media (max-width: 768px) {
        .stApp {
            padding: 1rem;
        }
        .header-text {
            font-size: 2rem;
        }
        .subheader-text {
            font-size: 0.9rem;
        }
        .stButton>button {
            width: auto;
        }
        .icon-header {
            justify-content: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Lägg till logotyp högst upp - Justera logotypens URL till en pålitlig källa eller ladda upp själv
st.markdown('<div class="logo"><img src="https://www.ginatricot.com/assets/logos/ginatricot-logo.svg" alt="Gina Tricot Logo" class="image-preview"></div>', unsafe_allow_html=True)

# Layout likt en modern e-handelswebbplats
st.markdown('<div class="header-text">Virtuell Try-on!</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader-text">Ladda upp en bild på en person och ett plagg för att prova plagget virtuellt.</div>', unsafe_allow_html=True)

# Avgränsare för att separera olika delar av appen
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Använd kolumner för uppladdning av bilder, med dynamisk anpassning för mobil
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="icon-header">👤 Personbild</div>', unsafe_allow_html=True)
    person_img = st.file_uploader("Ladda upp Personbild", type=["png", "jpg", "jpeg"], key="person")

    if person_img is not None:
        st.image(person_img, caption="Förhandsvisning av Personbild", use_column_width=False, width=200)

with col2:
    st.markdown('<div class="icon-header">👗 Plaggbild</div>', unsafe_allow_html=True)
    garment_img = st.file_uploader("Ladda upp Plaggbild", type=["png", "jpg", "jpeg"], key="garment")

    if garment_img is not None:
        st.image(garment_img, caption="Förhandsvisning av Plaggbild", use_column_width=False, width=200)

# Avgränsare före knappen
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Utföra Virtuell Try-on
if st.button("Utför Virtuell Try-on"):
    if person_img is not None and garment_img is not None:
        with st.spinner('Bearbetar...'):
            # Spara uppladdade filer till tillfälliga filer
            with open("person_img.png", "wb") as f:
                f.write(person_img.getbuffer())

            with open("garment_img.png", "wb") as f:
                f.write(garment_img.getbuffer())

            # Skicka förfrågan till Hugging Face API via Gradio-klienten
            result = client.predict(
                person_img=handle_file("person_img.png"),
                garment_img=handle_file("garment_img.png"),
                seed=0,  # Seed är inte viktigt här eftersom vi randomiserar
                randomize_seed=True,  # Alltid randomisera seed
                api_name="/tryon"
            )
        
        # Visa resultatet i Streamlit-appen
        st.image(result[0], caption="Resultatbild", use_column_width=True)
        st.write(f"Använt seed: {result[1]}")
        st.write(f"Svar: {result[2]}")
    else:
        st.warning("Vänligen ladda upp både en personbild och en plaggbild.")
