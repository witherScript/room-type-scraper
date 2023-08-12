"""
Scraper Class
Description: A web scraping class to collect images of different rooms. This script is part of a larger project to distinguish room types.
Usage: Instantiate the KitchenScraper class and call the scrape() method with the appropriate URL.
Dependencies: Selenium
License: MIT License
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import urllib.request
import requests
from PIL import Image
import time
import os
import io
from datetime import datetime as dt

PATH = '/usr/local/bin/chromedriver'


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=PATH)
        self.max_images = 100
        self.delay = 1

    def get_images_from_google(self, query: str, wd: webdriver):
        max_images = self.max_images
        delay = 1

        def scroll_down(wd):
            wd.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay)

        url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
        wd.get(url.format(q=query))

        image_urls = set()
        skips = 0
        while len(image_urls) + skips < max_images:
            scroll_down(wd)
            thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

            for img in thumbnails[len(image_urls) + skips:max_images]:
                try:
                    img.click()
                    time.sleep(delay)
                except:
                    continue
                images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
                for image in images:
                    if image.get_attribute('src') in image_urls:
                        max_images += 1
                        skips += 1
                        break

                    if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                        image_urls.add(image.get_attribute('src'))
                image_count = len(image_urls)
                if len(image_urls) >= max_images:
                    print(f"Found: {len(image_urls)} image links, done!")
                    break
                else:
                    print("Found:", len(image_urls),
                          "image links, looking for more ...")
                    time.sleep(30)
                    return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script(
                    "document.querySelector('.mye4qd').click();")

        return image_urls

    def download_image(self, down_path, url, file_name, image_type='JPEG',
                       verbose=True):
        try:
            time = dt.now()
            curr_time = time.strftime('%H:%M:%S')
            # Content of the image will be a url
            img_content = requests.get(url).content
            # Get the bytes IO of the image
            img_file = io.BytesIO(img_content)
            # Stores the file in memory and convert to image file using Pillow
            image = Image.open(img_file)
            file_pth = down_path + file_name

            with open(file_pth, 'wb') as file:
                image.save(file, image_type)

            if verbose == True:
                print(
                    f'The image: {file_pth} downloaded successfully at {curr_time}.')
        except Exception as e:
            print(
                f'Unable to download image from Google Photos due to\n: {str(e)}')

    def do_scrape(self, query_file_path):
        df = pd.read_csv(query_file_path)
        for ind in df.index:
            q = df['query'][ind]
            print(f'Querying {q}...')
            down_path = df['down_path'][ind]
            images = self.get_images_from_google(
                q, self.max_images, self.driver, self.delay)
            print(f'Found {len(images)} images for {q}')

            i = 0
            x = df['pwidth'][ind]
            y = df['pheight'][ind]
            print('the resolution is: ', x, y)
            try:
                for url in images:
                    i += 1
                    res = requests.get(url)
                    img = Image.open(io.BytesIO(res.content))
                    img = img.resize((x, y), Image.ANTIALIAS)
                    img.save(down_path + q + str(i) + '.jpg')
                    print(f'Image {i} saved')
                    i = 0
            except Exception as e:
                print('error: ', e)
                pass
