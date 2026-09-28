import os
import tkinter as tk
from PIL import Image, ImageTk

# ==========================================
# 🚀 設定區
# ==========================================
# 這是你剛才切出小圖的資料夾
FRAMES_FOLDER = r"D:\Users\user\Desktop\TT\動起來\成果"
# 播放速度 (毫秒)，50ms 大約等於每秒 20 幀 (20 FPS)
DELAY = 50 

def play_animation():
    # 建立主視窗
    root = tk.Tk()
    root.title("洪七公跑步模擬器 🏃‍♂️")
    root.configure(bg='gray') # 設定灰色背景，比較好觀察透明 PNG

    # 讀取並自動排序資料夾裡所有的 png 圖片
    files = sorted([f for f in os.listdir(FRAMES_FOLDER) if f.endswith('.png')])
    
    if not files:
        print("資料夾裡沒有找到 PNG 圖片喔！")
        return

    print(f"🎬 成功載入 {len(files)} 張畫格，準備播放！")

    # 將圖片轉換成 Tkinter 看得懂的格式
    frames = []
    for file in files:
        img_path = os.path.join(FRAMES_FOLDER, file)
        img = Image.open(img_path)
        # 如果圖片太小可以取消下一行的註解來放大它
        # img = img.resize((img.width * 2, img.height * 2), Image.Resampling.NEAREST)
        frames.append(ImageTk.PhotoImage(img))

    # 建立用來顯示圖片的標籤
    label = tk.Label(root, bg='gray')
    label.pack(padx=20, pady=20)

    # 動畫核心邏輯：切換圖片的函數
    def update_frame(idx):
        # 換上第 idx 張圖片
        label.configure(image=frames[idx])
        # 計算下一張的索引 (播到最後一張就回到 0)
        next_idx = (idx + 1) % len(frames)
        # 設定 DELAY 毫秒後，呼叫自己播放下一張
        root.after(DELAY, update_frame, next_idx)

    # 啟動第一張圖的播放
    update_frame(0)

    # 啟動視窗迴圈
    root.mainloop()

if __name__ == "__main__":
    play_animation()
