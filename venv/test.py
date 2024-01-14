from bs4 import BeautifulSoup
import requests
import re
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def get_youtube_title(url):
    try:
        # Gửi yêu cầu HTTP để lấy nội dung của trang
        response = requests.get(url)
        response.raise_for_status()

        # Phân tích HTML bằng BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tìm thẻ chứa tiêu đề
        title_tag = soup.find('title')

        # Lấy nội dung của thẻ tiêu đề
        if title_tag:
            title = title_tag.text
            return title
        else:
            return None
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")





# url = 'https://www.youtube.com/playlist?list=PL0QkWHYG4UcF82tUfdMAzilqrb5mt2vcA'
url = 'https://www.youtube.com/playlist?list=PL0QkWHYG4UcEYIrazYC9k36dO69krlMMa&page=2'
# url = 'https://www.youtube.com/playlist?list=PL0QkWHYG4UcHSAPfupTM4p-8fzvY0jALX'

driver = webdriver.Chrome()
driver.get(url)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html')

if os.path.exists("htmlCode.txt"):
    os.remove("htmlCode.txt")
with open("htmlCode.txt", "w", encoding="utf-8") as file:
    # Write the prettified HTML to the file
    file.write(soup.prettify())

print(soup.title.string)

position = page.text.find('numVideosText":{"runs":[{"text":"')
videos_count = int(page.text[position+33:page.text.find('"', position+33)])
print(videos_count)

videoLinks = []
position = page.text.find('webCommandMetadata":{"url":"/w', 0)
for index in range (1, videos_count+1):
    # print(position)
    # print(" ")
    # print(page.text[position+29:position+48])
    videoLinks.append("https://www.youtube.com/watch?v=" + page.text[position+37:position+48])

    position = page.text.find('webCommandMetadata":{"url":"/w', position + 1)

for link in videoLinks:
    print(link + " : " + get_youtube_title(link))




