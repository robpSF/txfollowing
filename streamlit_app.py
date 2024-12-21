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
        # Match valid Twitter handles while excluding email-like patterns
        matches = re.findall(r"@([A-Za-z0-9_]+)(?!\.\w+)", line)
        followers.extend(f"@{match}" for match in matches)
    return followers

def fix_split_handles(followers):
    """Fix split handles by intelligently merging parts based on patterns."""
    fixed_followers = []
    skip_next = False

    for i, follower in enumerate(followers):
        if skip_next:
            skip_next = False
            continue

        # If the current handle is incomplete (e.g., ends with '@Lowkey' and next is '0nline')
        if i + 1 < len(followers) and not followers[i + 1].startswith('@') and re.match(r"^[A-Za-z0-9_]+$", followers[i + 1]):
            combined = follower + followers[i + 1]
            fixed_followers.append(combined)
            skip_next = True  # Skip the next element as it's already merged
        else:
            fixed_followers.append(follower)

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

            # Perform OCR with whitelist configuration
            st.write(f"Extracting text from {uploaded_file.name}...")
            custom_config = r"--psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@"
            extracted_text = pytesseract.image_to_string(preprocessed_image, config=custom_config)

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
