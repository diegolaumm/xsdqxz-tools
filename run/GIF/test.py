import os
import plistlib
import re
from PIL import Image

def parse_cocos_rect(rect_str):
    """把奇怪的字串 '{{x,y},{w,h}}' 轉換成數字陣列 [x, y, w, h]"""
    numbers = [int(n) for n in re.findall(r'\d+', rect_str)]
    return numbers

def make_gif_from_plist(plist_path, png_path, output_gif):
    print(f"🎬 準備讀取劇本: {os.path.basename(plist_path)}")
    
    # 1. 讀取 .plist 劇本檔
    with open(plist_path, 'rb') as f:
        plist_data = plistlib.load(f)
        
    # 2. 讀取 .png 大圖
    sprite_sheet = Image.open(png_path).convert("RGBA")
    
    frames = []
    # 取出所有影格的資料 (Cocos 格式通常存在 'frames' 裡面)
    frame_dict = plist_data.get('frames', {})
    
    # 把檔名排序，確保動畫順序是對的 (例如 run_01, run_02...)
    sorted_frame_names = sorted(frame_dict.keys())
    
    print(f"✂️ 發現 {len(sorted_frame_names)} 張分解動作，開始剪裁...")
    
    for frame_name in sorted_frame_names:
        data = frame_dict[frame_name]
        
        # 讀取座標跟尺寸
        rect = parse_cocos_rect(data['frame']) # [x, y, w, h]
        rotated = data.get('rotated', False)
        
        # 如果圖片在打包時被旋轉了90度省空間，長寬要反過來切
        if rotated:
            box = (rect[0], rect[1], rect[0] + rect[3], rect[1] + rect[2])
        else:
            box = (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
            
        # 喀嚓！剪下來
        cropped_img = sprite_sheet.crop(box)
        
        # 把旋轉的圖片轉回正面
        if rotated:
            cropped_img = cropped_img.rotate(90, expand=True)
            
        frames.append(cropped_img)
        
    # 3. 輸出成 GIF 動畫
    # 3. 輸出成 GIF 動畫
        if frames:
            print(f"🎞️ 正在合成 GIF 動畫: {output_gif}")
            
            # --- 🌟 [去背模式升級版] ---
            # 保留 Alpha 通道 (透明層) 並進行顏色優化
            # duration=100 代表每張圖停留 0.1 秒 (可依喜好調整，例如改成 80 跑得更快)
            
            frames[0].save(
                output_gif,
                save_all=True,
                append_images=frames[1:],
                optimize=True,   # 啟動檔案大小優化
                duration=50,    #分解動作速度 (ms)
                loop=0,          # 無限循環
                disposal=2,      # 💡 這行絕對不能刪，是用來清除前一幀殘影的！
            )
            print("🎉 成功！快去打開你的真・去背 GIF 看看吧！")
        else:
            print("❌ 找不到任何影格資料！")

# ==========================================
# 🚀 執行區
# ==========================================
if __name__ == "__main__":
    # 👉 1. 這裡換成你要處理的 .plist 路徑
    PLIST_FILE = r"D:\Users\user\Desktop\TT\動起來\GIF\input\hero_huangrong_pao.plist"
    
    # 👉 2. 這裡換成跟它同名的 .png 大圖路徑
    PNG_FILE = r"D:\Users\user\Desktop\TT\動起來\GIF\input\hero_huangrong_pao.png.png"
    
    # 👉 3. 輸出的 GIF 檔名
    OUTPUT_GIF = r"D:\Users\user\Desktop\TT\動起來\GIF\hg.gif"    
    make_gif_from_plist(PLIST_FILE, PNG_FILE, OUTPUT_GIF)
