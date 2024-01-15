import customtkinter as ctk
import PlaylistDownloader as pldr
import time

# Khởi tạo biến đếm
button_press_count = 0

def on_submit():
    global button_press_count
    button_press_count += 1  # Tăng biến đếm
    user_input = input_box.get()
    print(f"User Input: {user_input}")  # Xử lý input ở đây
    count_label.configure(text=f"Button pressed: {button_press_count} times")  # Cập nhật text của label

def call_download_youtube_playlist():
    print("Đang tải...")
    count_label.configure(text=f"Đang tải...")  # Cập nhật text của label
    print("vui lòng đợi...")
    time.sleep(1)
    user_input = input_box.get()
    pldr.download_youtube_playlist(user_input)
    count_label.configure(text=f"Hoàn thành download")  # Cập nhật text của label

# Thiết lập cửa sổ
WIDTH = 1200
HEIGHT = 1000
app = ctk.CTk()
app.geometry(f"{WIDTH}x{HEIGHT}")
app.title("Playlist Downloader")

# Tạo hộp nhập liệu
input_box = ctk.CTkEntry(app, placeholder_text="Type your youtube playlist link here", width=1100, height=75, font=("", 20))
input_box.pack(pady=40)
input_box.bind("<Return>", lambda event: call_download_youtube_playlist())

# Tạo nút submit
submit_button = ctk.CTkButton(app, text="Download Playlist", command=call_download_youtube_playlist, width=400, height=75, font=("", 20))
submit_button.pack(pady=10)

# Tạo label để hiển thị số lần nút được nhấn
count_label = ctk.CTkLabel(app, text="Button pressed: 0 times", font=("", 15))
count_label.pack(pady=10)

# Vòng lặp chính của ứng dụng
app.mainloop()
