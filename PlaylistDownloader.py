from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import math
from pytube import YouTube
import stat
import shutil
from pytube.exceptions import AgeRestrictedError

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

#Lấy số video trong playlist kể cả video đã bị ẩn
def get_videos_count(url):
    page = requests.get(url)

    position = page.text.find('numVideosText":{"runs":[{"text":"')
    videos_count = int(page.text[position+33:page.text.find('"', position+33)])
    return(videos_count)

#Lấy số video trong playlist sau khi đã trừ đi các video ẩn
def get_videos_count_ignore_hidden_videos(htmlCodeFinal):
    position = htmlCodeFinal.rfind(';index=')
    videos_count = int(htmlCodeFinal[position+7:htmlCodeFinal.find('&', position+7)])
    print(videos_count)
    return videos_count

def clean_filename(filename):
    # Loại bỏ các ký tự không phù hợp với tên file
    cleaned_filename = re.sub(r'[^\w\s.-]', '', filename)
    return cleaned_filename

def download_youtube_video(youtube_link, folder_name, video_title):
    try:
        # Tạo đối tượng YouTube
        yt = YouTube(youtube_link)

        # Chọn stream có chất lượng tốt nhất
        video = yt.streams.get_highest_resolution()

        video_title = str(ix) + "_" + clean_filename(video_title) + ".mp4"
        # Tải video về thư mục
        video.download(folder_name, filename=video_title)

        # print(f"Video đã được tải về thành công vào thư mục {folder_name}")
        print("Tải về thành công")

    except AgeRestrictedError:
        print("Lỗi: Video có giới hạn độ tuổi và yêu cầu đăng nhập.")
    except Exception as e:
        print(f"Lỗi: {str(e)}")

# url = 'https://www.youtube.com/playlist?list=PL0QkWHYG4UcF82tUfdMAzilqrb5mt2vcA'
url = 'https://www.youtube.com/playlist?list=PL0QkWHYG4UcEYIrazYC9k36dO69krlMMa'
# url = 'https://www.youtube.com/playlist?list=PL0QkWHYG4UcHSAPfupTM4p-8fzvY0jALX'

#Cài đặt để không hiển thị trình duyệt khi xử lý
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-infobars')

#Khởi tạo trình duyệt
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
videos_count = get_videos_count(url)

#Youtube chỉ hiện 100 video đầu tiên trong playlist. Lăn chuột xuống cuối trang để hiện thêm video
for i in range(1, math.ceil(videos_count / 100) + 1):
    driver.execute_script("window.scrollBy(0, 999999999)","")
    time.sleep(5)

#Lấy mã HTML của trang, lưu vào tệp htmlCode.txt để kiểm tra nếu cần
htmlCode = driver.page_source
# if os.path.exists("htmlCode.txt"):
#     # Nếu tệp tồn tại, xóa nó
#     os.remove("htmlCode.txt")
# with open("htmlCode.txt", 'w', encoding='utf-8') as file:
#     file.write(htmlCode)

#Khởi tạo mảng chứa các link video, lấy vị trí đầu tiên của link video
videoLinks = []
position = htmlCode.find('<a id="video-title" class="yt-simple-endpoint style-scope ytd-playlist-video-renderer" href="', 0)

#video_count bên trên là chưa tính các video ẩn, nên cần chạy hàm này để lấy số video thực tế sau khi đã trừ đi các video ẩn
videos_count = get_videos_count_ignore_hidden_videos(htmlCode)

#Lấy các link video, lưu vào mảng videoLinks
for index in range (1, videos_count + 1):
    videoLinks.append("https://www.youtube.com/watch?v=" + htmlCode[position+102:position+113])
    position = htmlCode.find('<a id="video-title" class="yt-simple-endpoint style-scope ytd-playlist-video-renderer" href="', position + 1)

#Tạo folder chứa video tên là tên playlist
playlist_name = get_youtube_title(url)
print("Playlist name : " + playlist_name)
if os.path.exists(playlist_name):
    # Nếu tệp tồn tại, cấp quyền và xóa nó
    # os.remove(playlist_name)
    shutil.rmtree(playlist_name)
os.mkdir(playlist_name)

ix = 0
for link in videoLinks:
    ix += 1
    video_title = get_youtube_title(link)
    print(str(ix) + " : " + link + " : " + video_title)
    download_youtube_video(link, playlist_name, video_title)




