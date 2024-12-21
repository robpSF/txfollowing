import streamlit as st
from playwright.sync_api import sync_playwright

# Function to scrape Twitter handles using Playwright
def scrape_twitter_handles(url):
    try:
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

            # Extract Twitter handles from the page
            content = page.content()
            handles = []
            for line in content.splitlines():
                if '@' in line:
                    start = line.find('@')
                    end = line.find(' ', start)
                    handles.append(line[start:end] if end != -1 else line[start:])

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
        else:
            st.write("Please enter a valid URL.")

if __name__ == "__main__":
    main()
