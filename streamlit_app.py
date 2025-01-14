import streamlit as st
from PIL import Image, ImageEnhance
import pytesseract
import re
from difflib import get_close_matches

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
    debug_lines = []  # Collect lines for debugging

    for line in lines:
        # Add current line to debugging
        debug_lines.append(f"Processing line: {line}")

        # Skip email addresses explicitly
        if re.search(r"[^@\s]+@[^@\s]+\.[^@\s]+", line):
            continue  # Skip email addresses

        # Match valid Twitter handles
        matches = re.findall(r"@(?:[A-Za-z0-9_]+)", line)  # Handles starting with @
        if matches:
            debug_lines.append(f"Raw matches: {matches}")  # Debug: Show raw matches
            followers.extend(matches)  # Add all matches in the line

    # Filter out handles less than 4 characters, @gmailcom, and handles ending with bskysocial
    followers = [
        handle for handle in followers
        if len(handle) >= 4
        and handle.lower() != "@gmailcom"
        and not handle.lower().endswith("bskysocial")
    ]
    debug_lines.append(f"Filtered followers: {followers}")  # Debug: Show filtered results

    # Display debugging information in Streamlit
    st.write("### Debugging Information")
    for debug_line in debug_lines:
        st.write(debug_line)

    return followers


def save_to_file(followers):
    """Save the list of followers to a text file."""
    file_name = "extracted_followers.txt"
    with open(file_name, "w") as f:
        for follower in followers:
            f.write(follower + "\n")
    return file_name

def correct_text(extracted, known_handles):
    """Correct misinterpreted text using known handles."""
    corrected = []
    for handle in extracted:
        matches = get_close_matches(handle, known_handles, n=1, cutoff=0.8)
        if matches:
            corrected.append(matches[0])
        else:
            corrected.append(handle)
    return corrected

# Streamlit App
st.title("Image Follower Extractor")

st.write("Upload images containing follower information, and this app will extract it for you.")

# Known handles for correction (this could be dynamic)
known_handles = ["@Lowkey0nline", "@ExampleHandle", "@AnotherExample"]

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

st.write("\n---\nDeveloped with ❤️ using Streamlit")
