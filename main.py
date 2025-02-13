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
def download_image(image_url, folder, count):
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f"{folder}/{count}_{timestamp}.jpg", "wb") as file:
                file.write(response.content)
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")


# Scrape images for a given search query
def scrape_images(query, max_images=300):
    driver = get_driver()
    search_url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(2)

    # Scroll to load more images
    for _ in range(5):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(random.uniform(1, 3))

    image_elements = driver.find_elements(By.CSS_SELECTOR, "img")
    image_urls = [img.get_attribute("src") for img in image_elements if img.get_attribute("src")]

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
        "DJI fixed wing drone", "Boeing fixed wing UAV", "Lockheed Martin fixed wing UAV"
    ]

    num_processes = min(len(queries), 4)  # Limit to 4 parallel processes
    with multiprocessing.Pool(num_processes) as pool:
        pool.map(scrape_images, queries)


if __name__ == "__main__":
    main()
