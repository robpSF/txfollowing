import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to scrape Twitter handles
def scrape_twitter_handles(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    
    try:
        # Fetch the page content
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract handles from the page
        handles = []
        for span in soup.find_all('span'):
            text = span.get_text()
            if text.startswith('@'):
                handles.append(text)
        
        return handles

    except requests.exceptions.RequestException as e:
        return [f"Error fetching data: {e}"]

# Streamlit app
def main():
    st.title("Twitter Following Scraper (BeautifulSoup)")
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
                st.write("No handles found.")
        else:
            st.write("Please enter a valid URL.")

if __name__ == "__main__":
    main()
