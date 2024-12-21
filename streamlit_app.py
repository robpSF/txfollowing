import streamlit as st
from playwright.sync_api import sync_playwright
import os
import base64

# Ensure Playwright browsers are installed
def ensure_playwright_browsers():
    os.system("playwright install chromium")

# Function to create a download link for debug HTML
def create_download_link(file_path, file_name):
    with open(file_path, "rb") as file:
        data = file.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="{file_name}">Download debug_output.html</a>'
        return href

# Function to scrape Twitter handles using Playwright
def scrape_twitter_handles(url):
    try:
        ensure_playwright_browsers()  # Ensure browsers are installed
        with sync_playwright() as p:
            # Launch a headless browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to the Twitter page
            page.goto(url)
            page.wait_for_timeout(5000)  # Wait for the page to load

            # Scroll down multiple times to load all content
            for _ in range(5):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                page.wait_for_timeout(2000)

            # Debug: Save the full page content
            content = page.content()
            with open("debug_output.html", "w", encoding="utf-8") as f:
                f.write(content)

            # Locate the primary container
            timeline = page.locator('div[aria-label="Timeline: Following"]')
            handles = []

            # Extract Twitter handles
            if timeline.count() > 0:
                st.write("Timeline Content:")
                st.write(timeline.inner_html())  # Debug: Log timeline HTML
                elements = timeline.locator('span').all()
                for element in elements:
                    text = element.inner_text().strip()
                    if text.startswith('@') and len(text) > 1:
                        handles.append(text)

            browser.close()
            return list(set(handles))  # Remove duplicates
    except Exception as e:
        return [f"Error: {e}"]

# Streamlit app
def main():
    st.title("Twitter Following Scraper (Playwright)")
    st.write("Enter the URL of the Twitter following page to extract handles.")

    # Input URL
    url = st.text_input("Twitter Following Page URL:", placeholder="https://x.com/username/following")

    if st.button("Scrape Handles"):
        if url:
            st.write("Scraping handles...")
            handles = scrape_twitter_handles(url)
            if handles:
                st.write("Following Handles:")
                for handle in handles:
                    st.write(handle)
            else:
                st.write("No handles found or an error occurred.")

            # Provide debug HTML content
            st.write("Debug Output (HTML Content):")
            with open("debug_output.html", "r", encoding="utf-8") as f:
                debug_content = f.read()
                st.text_area("HTML Content", debug_content, height=500)

            # Provide a download link for the debug file
            st.write("Download the debug HTML file:")
            st.markdown(create_download_link("debug_output.html", "debug_output.html"), unsafe_allow_html=True)
        else:
            st.write("Please enter a valid URL.")

if __name__ == "__main__":
    main()
