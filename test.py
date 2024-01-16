import tkinter as tk
import time

def run_function():
    for i in range(10):
        text_area.insert(tk.END, f"Đang chạy bước {i+1}\n")
        window.update_idletasks()
        time.sleep(1)

window = tk.Tk()
window.title("Cập nhật Trạng Thái")

text_area = tk.Text(window, height=10, width=30)
text_area.pack()

run_button = tk.Button(window, text="Chạy Hàm", command=run_function)
run_button.pack()

window.mainloop()
