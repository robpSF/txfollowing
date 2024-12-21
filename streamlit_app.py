import streamlit as st
from PIL import Image, ImageEnhance
import pytesseract
import re

def preprocess_image(image):
    """Preprocess the image to improve OCR accuracy."""
    # Convert image to grayscale
    image = image.convert("L")
    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    return image

def extract_followers(text):
    """Extract follower information from the text."""
    followers = []
    lines = text.split('\n')
    for line in lines:
        # Match lines containing @ and filter out noise
        match = re.search(r"@[A-Za-z0-9_]+", line)
        if match:
            followers.append(match.group())
    return followers

def save_to_file(followers):
    """Save the list of followers to a text file."""
    file_name = "extracted_followers.txt"
    with open(file_name, "w") as f:
        for follower in followers:
            f.write(follower + "\n")
    return file_name

# Streamlit App
st.title("Image Follower Extractor")

st.write("Upload an image containing follower information, and this app will extract it for you.")

# Upload image
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Perform OCR
    st.write("Extracting text from the image...")
    extracted_text = pytesseract.image_to_string(preprocessed_image)

    # Extract followers
    followers = extract_followers(extracted_text)

    if followers:
        st.write("### Extracted Followers:")
        for idx, follower in enumerate(followers, 1):
            st.write(f"{idx}. {follower}")

        # Save followers to a file
        file_name = save_to_file(followers)
        with open(file_name, "rb") as file:
            btn = st.download_button(
                label="Download Followers as Text File",
                data=file,
                file_name="extracted_followers.txt",
                mime="text/plain"
            )
    else:
        st.write("No followers found in the image.")

st.write("\n---\nDeveloped with ❤️ using Streamlit")
