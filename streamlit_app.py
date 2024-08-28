import streamlit as st
from gradio_client import Client, handle_file

# Initiera Gradio-klienten med ditt önskade endpoint
client = Client("Kwai-Kolors/Kolors-Virtual-Try-On")

# Övergripande stil för appen
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 2rem;
    }
    .stButton>button {
        background-color: #000000;
        color: white;
        border-radius: 5px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #333333;
    }
    .header-text {
        font-size: 2rem;
        font-weight: bold;
        color: #333333;
    }
    .subheader-text {
        font-size: 1.2rem;
        color: #666666;
        margin-bottom: 1.5rem;
    }
    .divider {
        margin: 2rem 0;
        height: 1px;
        background-color: #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# Layout likt en modern e-handelswebbplats
st.markdown('<div class="header-text">Virtuell Try-on!</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader-text">Ladda upp en bild på en person och ett plagg för att prova plagget virtuellt.</div>', unsafe_allow_html=True)

# Avgränsare för att separera olika delar av appen
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Använd kolumner för uppladdning av bilder, likt en e-handelsproduktlista
col1, col2 = st.columns(2)

with col1:
    st.subheader("Personbild")
    person_img = st.file_uploader("Ladda upp Personbild", type=["png", "jpg", "jpeg"], key="person")

    if person_img is not None:
        st.image(person_img, caption="Förhandsvisning av Personbild", use_column_width=True)

with col2:
    st.subheader("Plaggbild")
    garment_img = st.file_uploader("Ladda upp Plaggbild", type=["png", "jpg", "jpeg"], key="garment")

    if garment_img is not None:
        st.image(garment_img, caption="Förhandsvisning av Plaggbild", use_column_width=True)

# Avgränsare före knappen
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Utföra Virtuell Try-on
if st.button("Utför Virtuell Try-on"):
    if person_img is not None and garment_img is not None:
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
        st.image(result[0], caption="Resultatbild")
        st.write(f"Använt seed: {result[1]}")
        st.write(f"Svar: {result[2]}")
    else:
        st.warning("Vänligen ladda upp både en personbild och en plaggbild.")
