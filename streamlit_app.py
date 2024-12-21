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
        # Match all @handles using re.findall to capture multiple occurrences in one line
        matches = re.findall(r"@[A-Za-z0-9_]+", line)
        followers.extend(matches)
    return followers

def fix_split_handles(followers):
    """Fix split handles by intelligently merging parts based on patterns."""
    fixed_followers = []
    i = 0
    while i < len(followers):
        if i + 1 < len(followers) and followers[i + 1].startswith('@'):
            # Check if merging current and next creates a valid handle
            combined = followers[i] + followers[i + 1][1:]  # Remove '@' from the next part
            if re.match(r"@[A-Za-z0-9_]+", combined):
                fixed_followers.append(combined)
                i += 2  # Skip the next part as it's merged
                continue
        fixed_followers.append(followers[i])
        i += 1
    return fixed_followers

def save_to_file(followers):
    """Save the list of followers to a text file."""
    file_name = "extracted_followers.txt"
    with open(file_name, "w") as f:
        for follower in followers:
            f.write(follower + "\n")
    return file_name

# Streamlit App
st.title("Image Follower Extractor")

st.write("Upload images containing follower information, and this app will extract it for you.")

# Multi-file uploader
uploaded_files = st.file_uploader("Choose image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Button to trigger extraction
if st.button("Go"):
    all_followers = []

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Open and display each image
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)

            # Preprocess the image
            preprocessed_image = preprocess_image(image)

            # Perform OCR
            st.write(f"Extracting text from {uploaded_file.name}...")
            extracted_text = pytesseract.image_to_string(preprocessed_image)

            # Extract followers
            followers = extract_followers(extracted_text)
            all_followers.extend(followers)

        if all_followers:
            # Remove duplicates
            unique_followers = list(set(all_followers))
            unique_followers.sort()

            # Fix split handles
            fixed_followers = fix_split_handles(unique_followers)

            st.write("### Extracted Followers:")
            for idx, follower in enumerate(fixed_followers, 1):
                st.write(f"{idx}. {follower}")

            # Save all followers to a file
            file_name = save_to_file(fixed_followers)
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

st.write("\n---\nDeveloped with ❤️ using Streamlit")
