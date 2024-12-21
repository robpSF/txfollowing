import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Function to scrape Twitter handles
def get_following_handles(url):
    # Configure Selenium for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the WebDriver
    service = Service("/usr/bin/chromedriver")  # Path to ChromeDriver in Streamlit Cloud
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open the Twitter following page
        driver.get(url)
        
        # Wait for the page to load
        time.sleep(5)
        
        # Scroll down to load more accounts (adjust range as needed)
        for _ in range(5):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(2)
        
        # Find elements containing handles
        elements = driver.find_elements(By.CSS_SELECTOR, "div[dir='ltr'] > span")
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
