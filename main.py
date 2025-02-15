import os
import time
import random
import requests
import multiprocessing
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import base64

"""
Requirements:
1. Python 3.6+
2. Install required packages: pip install requests selenium
3. Download Chrome WebDriver: https://sites.google.com/a/chromium.org/chromedriver/downloads
4. Extract the downloaded file and move the executable to a directory in PATH
5. Run the script: python main.py
"""


# Set up Chrome WebDriver
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)


# Download image from URL
import base64

# Download image from URL (handles Base64 images as well)
def download_image(image_url, folder, count):
    try:
        if image_url.startswith("data:image"):
            # Extract Base64 data from the URL
            base64_data = image_url.split(',')[1]
            image_data = base64.b64decode(base64_data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f"{folder}/{count}_{timestamp}.jpg", "wb") as file:
                file.write(image_data)
        else:
            # For regular image URLs, use requests to download
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(f"{folder}/{count}_{timestamp}.jpg", "wb") as file:
                    file.write(response.content)
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")



# Scrape images for a given search query
def scrape_images(query, max_images=200):
    driver = get_driver()
    search_url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(2)

    # Scroll to load more images
    for _ in range(5):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(random.uniform(1, 3))

    image_elements = driver.find_elements(By.CSS_SELECTOR, "img")

    # Filtreleme: sadece geçerli görsel URL'lerini al
    image_urls = [
        img.get_attribute("src") for img in image_elements
        if img.get_attribute("src") and not img.get_attribute("src").startswith("data:image")
    ]

    driver.quit()

    # Create folder
    folder = f"dataset/{query.replace(' ', '_')}"
    os.makedirs(folder, exist_ok=True)

    # Download images
    for count, img_url in enumerate(image_urls[:max_images]):
        download_image(img_url, folder, count)

    print(f"Downloaded {len(image_urls[:max_images])} images for {query}")


# Parallel execution
def main():
    queries = [
        "fixed wing UAV", "fixed wing drone", "fixed wing unmanned aerial vehicle",
        "military fixed wing drone", "tactical fixed wing UAV", "combat fixed wing UAV",
        "fixed wing surveillance drone", "stealth fixed wing UAV", "fixed wing reconnaissance drone",
        "DJI fixed wing drone", "Boeing fixed wing UAV", "Lockheed Martin fixed wing UAV",
        "sabit kanatlı İHA", "sabit kanatlı drone", "sabit kanatlı insansız hava aracı", "sabit kanat iha",
        "acemi sabit kanat iha", "amatör sabit kanat iha", "amateur fixed wing uav in the sky",
        "askeri sabit kanatlı drone", "taktik sabit kanatlı İHA", "savaş sabit kanatlı İHA",
        "sabit kanatlı gözetleme drone", "gizli sabit kanatlı İHA", "sabit kanatlı keşif drone",
        "DJI sabit kanatlı drone", "Boeing sabit kanatlı İHA", "Lockheed Martin sabit kanatlı İHA",
        "固定翼无人机", "固定翼无人驾驶飞行器", "军事固定翼无人机", "战术固定翼无人机", "隐形固定翼无人机",
        "固定翼侦察无人机", "固定翼监视无人机", "DJI固定翼无人机", "波音固定翼无人机", "洛克希德马丁固定翼无人机",
        "droni ad ala fissa", "velivolo a pilotaggio remoto ad ala fissa", "UAV ad ala fissa",
        "drone militare ad ala fissa", "sorveglianza UAV ad ala fissa", "ricognizione drone ad ala fissa",
        "DJI drone ad ala fissa", "Boeing UAV ad ala fissa", "Lockheed Martin UAV ad ala fissa"
    ]

    num_processes = min(len(queries), 4)  # Limit to 4 parallel processes
    with multiprocessing.Pool(num_processes) as pool:
        pool.map(scrape_images, queries)


if __name__ == "__main__":
    main()
