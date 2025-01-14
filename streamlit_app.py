def preprocess_text(ocr_text):
    """Clean and reconstruct the OCR text."""
    # Remove excessive whitespace
    cleaned_text = re.sub(r'\s+', ' ', ocr_text).strip()
    # Split into logical lines by punctuation or excessive spacing
    logical_lines = re.split(r'(?<=[.!?]) +', cleaned_text)
    return logical_lines

def extract_followers(text_lines):
    """Extract follower information from cleaned text lines."""
    followers = []
    debug_lines = []  # Collect lines for debugging

    for line in text_lines:
        # Add current line to debugging
        debug_lines.append(f"Processing line: {line}")

        # Skip email addresses explicitly
        if re.search(r"[^@\\s]+@[^@\\s]+\\.[^@\\s]+", line):
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

# Streamlit App Updates
if st.button("Go"):
    all_followers = []

    if uploaded_files:
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
