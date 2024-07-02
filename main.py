import requests
from bs4 import BeautifulSoup
import sys
import os

URL = "https://www.reddit.com/r/EarthPorn/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
OUTPUT_DIR = './download'

def main():
    
    try:
        web = requests.get(URL, headers=HEADERS)
        web.raise_for_status()
    except requests.RequestException as e:
        sys.exit(f"Error: {e}")

    soup = BeautifulSoup(web.text, "html.parser")
    imgs = soup.find_all('img')
    name = 0

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for img in imgs:
        img_src = img.get("src")
        if img_src and ("preview" not in img_src):
            try:
                jpg = requests.get(img_src, headers=HEADERS)
                jpg.raise_for_status()
                print(img_src)
                img_path = os.path.join(OUTPUT_DIR, f'test_{name}.jpg')

                with open(img_path, 'wb') as f:
                    f.write(jpg.content)
                name += 1
            except requests.RequestException as e:
                print(f"Failed to download images: {e}")

if __name__ == "__main__":
    main()