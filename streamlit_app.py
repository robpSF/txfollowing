import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import os
import time

# Function to set up Selenium with Chrome
def setup_driver():
    # Automatically download the correct ChromeDriver version
    chromedriver_autoinstaller.install()

    # Download Google Chrome binary
    chrome_path = "/tmp/google-chrome"
    if not os.path.exists(chrome_path):
        os.system(
            "wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/google-chrome.deb"
        )
        os.system("dpkg -x /tmp/google-chrome.deb /tmp/google-chrome")
        os.system("rm /tmp/google-chrome.deb")

    # Configure Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/tmp/google-chrome/opt/google/chrome/google-chrome"

    # Set up WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Function to scrape Twitter handles
def get_following_handles(url):
    try:
        driver = setup_driver()

        # Open the Twitter following page
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)

        # Scroll down to load more accounts (adjust range as needed)
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Extract Twitter handles
        elements = driver.find_elements("xpath", "//div[@dir='ltr']/span")
        handles = [el.text for el in elements if el.text.startswith('@')]

        return handles
    except Exception as e:
        return [f"Error: {e}"]
    finally:
        driver.quit()

# Streamlit app
def main():
    st.title("Twitter Following Scraper")
    st.write("Enter the URL of the Twitter following page to extract handles.")

    # Input URL
    url = st.text_input("Twitter Following Page URL:", placeholder="https://x.com/username/following")

    if st.button("Scrape Handles"):
        if url:
            st.write("Scraping handles...")
            handles = get_following_handles(url)
            if handles:
                st.write("Following Handles:")
                for handle in handles:
                    st.write(handle)
            else:
                st.write("No handles found.")
        else:
            st.write("Please enter a valid URL.")

if __name__ == "__main__":
    main()
