import streamlit as st
from gradio_client import Client, handle_file

# Initiera Gradio-klienten med ditt önskade endpoint
client = Client("Kwai-Kolors/Kolors-Virtual-Try-On")

# Streamlit app inställningar
st.title("Virtuell Try-on!")

# Bilduppladdning för person och plagg
person_img = st.file_uploader("Ladda upp Personbild", type=["png", "jpg", "jpeg"])
garment_img = st.file_uploader("Ladda upp Plaggbild", type=["png", "jpg", "jpeg"])

# Slider för seed-värde och checkbox för att slumpa seed
seed = st.slider("Välj Seed-värde", 0, 100, 0)
randomize_seed = st.checkbox("Slumpa Seed", value=True)

# När användaren klickar på knappen "Utför"
if st.button("Utför Virtuell Tryon"):
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
            seed=seed,
            randomize_seed=randomize_seed,
            api_name="/tryon"
        )
        
        # Visa resultatet i Streamlit-appen
        st.image(result[0], caption="Resultatbild")
        st.write(f"Använt seed: {result[1]}")
        st.write(f"Svar: {result[2]}")
    else:
        st.warning("Vänligen ladda upp både en personbild och en plaggbild.")
