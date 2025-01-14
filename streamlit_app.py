import streamlit as st
from PIL import Image, ImageEnhance
import pytesseract
import re
from difflib import get_close_matches

# Streamlit App Updates
st.title("Image Follower Extractor")

st.write("Upload images containing follower information, and this app will extract it for you.")

# Known handles for correction (this could be dynamic)
known_handles = ["@Lowkey0nline", "@ExampleHandle", "@AnotherExample"]

# Multi-file uploader
uploaded_files = st.file_uploader("Choose image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Ensure files are uploaded before showing the button
if uploaded_files:
    if st.button("Go"):
        all_followers = []

        for uploaded_file in uploaded_files:
            # Open and display each image
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)

            # Preprocess the image
            preprocessed_image = preprocess_image(image)

            # Perform OCR with adjusted settings
            st.write(f"Extracting text from {uploaded_file.name}...")
            custom_config = r"--psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@"
            raw_text = pytesseract.image_to_string(preprocessed_image, config=custom_config)

            # Clean and reconstruct text into logical lines
            reconstructed_lines = preprocess_text(raw_text)
            st.write("### Reconstructed Lines:")
            st.write(reconstructed_lines)  # Debugging reconstructed lines

            # Extract followers
            followers = extract_followers(reconstructed_lines)
            all_followers.extend(followers)

        if all_followers:
            # Remove duplicates
            unique_followers = list(set(all_followers))
            unique_followers.sort()

            # Correct text using known handles
            corrected_followers = correct_text(unique_followers, known_handles)

            st.write("### Extracted Followers:")
            for idx, follower in enumerate(corrected_followers, 1):
                st.write(f"{idx}. {follower}")

            # Save all followers to a file
            file_name = save_to_file(corrected_followers)
            with open(file_name, "rb") as file:
                st.download_button(
                    label="Download Followers as Text File",
                    data=file,
                    file_name="extracted_followers.txt",
                    mime="text/plain"
                )
        else:
            st.write("No followers found in the uploaded images.")
else:
    st.write("Please upload at least one image.")
