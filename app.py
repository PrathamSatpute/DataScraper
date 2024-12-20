import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from typing import List

class WebScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.data = []

    def fetch_html(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to fetch {url}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    def parse_business_data(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract the title
        title = soup.find('h1').text.strip() if soup.find('h1') else "N/A"
        
        # Extract paragraphs
        paragraphs = soup.find_all('p')
        content = []
        for p in paragraphs:
            content.append(p.text.strip())
        
        # Store the data
        self.data.append({
            "Title": title,
            "Content": " ".join(content)  # Join all paragraphs into a single string
        })

    def clean_data(self) -> pd.DataFrame:
        df = pd.DataFrame(self.data)
        df.drop_duplicates(inplace=True)
        df.fillna("N/A", inplace=True)
        return df

    def save_data(self, df: pd.DataFrame, filename: str = "output.csv"):
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def display_data(self, df: pd.DataFrame):
        if df.empty:
            print("No data found.")
        else:
            print(df)

    def scrape(self, urls: List[str]):
        for url in urls:
            print(f"Scraping {url}...")
            html = self.fetch_html(url)
            if html:
                self.parse_business_data(html)  # Call the updated method without parameters
            time.sleep(random.uniform(1, 3))  # Politeness delay
        df = self.clean_data()
        self.display_data(df)
        self.save_data(df)

if __name__ == "__main__":
    scraper = WebScraper()
    urls = input("Enter the URL to scrape: ").split(',')
    urls = [url.strip() for url in urls]
    scraper.scrape(urls)