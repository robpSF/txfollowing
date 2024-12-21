import streamlit as st
from PIL import Image
import pytesseract
import re

# Set Tesseract path (adjust the path to your system)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Example for Linux/Ubuntu

def extract_followers(text):
    """Extract follower information from the text."""
    followers = []
    lines = text.split('\n')
    for line in lines:
        if '@' in line:
            followers.append(line.strip())
    return followers

# Streamlit App
st.title("Image Follower Extractor")

st.write("Upload an image containing follower information, and this app will extract it for you.")

# Upload image
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Perform OCR
    st.write("Extracting text from the image...")
    extracted_text = pytesseract.image_to_string(image)

    # Extract followers
    followers = extract_followers(extracted_text)

    if followers:
        st.write("### Extracted Followers:")
        followers_list = "\n".join(followers)
        st.text_area("Copy-paste the list below:", followers_list, height=200)

        # Provide a download option
        st.download_button(
            label="Download Followers List",
            data=followers_list,
            file_name="followers_list.txt",
            mime="text/plain"
        )
    else:
        st.write("No followers found in the image.")

st.write("\n---\nDeveloped with ❤️ using Streamlit")
