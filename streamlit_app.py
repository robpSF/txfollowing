import streamlit as st
from playwright.sync_api import sync_playwright
import os
import base64

# Ensure Playwright browsers are installed
def ensure_playwright_browsers():
    os.system("playwright install chromium")

# Create a download link for debug output
def create_download_link(file_path, file_name):
    with open(file_path, "rb") as file:
        data = file.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="{file_name}">Download debug_output.html</a>'
        return href

# Function to scrape Twitter handles
def scrape_twitter_handles(url):
    try:
        ensure_playwright_browsers()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Use headless=False for debugging
            page = browser.new_page()

            # Navigate to the page
            page.goto(url)
            page.wait_for_timeout(5000)  # Wait for page load

            # Scroll to ensure all content is loaded
            for _ in range(5):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                page.wait_for_timeout(2000)

            # Debug: Save full page content
            content = page.content()
            with open("debug_output.html", "w", encoding="utf-8") as f:
                f.write(content)

            # Look for the timeline
            timeline = page.locator('div[aria-label="Timeline: Following"]')
            handles = []

            # Extract Twitter handles
            if timeline.count() > 0:
                elements = timeline.locator('span:has-text("@")').all()
                for element in elements:
                    text = element.inner_text().strip()
                    if text.startswith('@'):
                        handles.append(text)

            browser.close()
            return list(set(handles)) if handles else ["No handles found."]
    except Exception as e:
        return [f"Error: {e}"]

# Streamlit app
def main():
    st.title("Twitter Following Scraper")
    st.write("Enter the URL of the Twitter following page to extract handles.")

    url = st.text_input("Twitter Following Page URL:", placeholder="https://x.com/username/following")

    if st.button("Scrape Handles"):
        if url:
            st.write("Scraping handles...")
            handles = scrape_twitter_handles(url)
            if handles:
                st.write("Following Handles:")
                for handle in handles:
                    st.write(handle)

            # Provide debug output
            st.write("Debug Output (HTML Content):")
            with open("debug_output.html", "r", encoding="utf-8") as f:
                debug_content = f.read()
                st.text_area("HTML Content", debug_content, height=500)

            # Download debug file
            st.write("Download the debug HTML file:")
            st.markdown(create_download_link("debug_output.html", "debug_output.html"), unsafe_allow_html=True)
        else:
            st.write("Please enter a valid URL.")

if __name__ == "__main__":
    main()
