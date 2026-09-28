import os
import plistlib
import ast
import traceback  # 幫我們抓出詳細死因的法醫模組
from PIL import Image

# ==========================================
# 座標轉換小工具 (千萬不能漏掉這個！)
# ==========================================
def parse_str_to_tuple(string_val):
    # Cocos2D 的座標格式長這樣: "{{89, 412}, {76, 88}}"
    # 我們把它轉換成 Python 看得懂的數字 tuple
    formatted_str = string_val.replace('{', '(').replace('}', ')')
    return ast.literal_eval(formatted_str)

# ==========================================
# 核心切割機
# ==========================================
def cut_sprite_sheet(plist_path, png_path, output_dir):
    print(f"🔪 準備切割: {os.path.basename(png_path)}")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(plist_path, 'rb') as f:
        plist_data = plistlib.load(f)
    
    img = Image.open(png_path)
    frames = plist_data.get('frames', {})

    count = 0
    for frame_name, frame_data in frames.items():
        rect_str = frame_data.get('frame') or frame_data.get('textureRect')
        if not rect_str:
            continue
            
        rect = parse_str_to_tuple(rect_str)
        x, y = rect[0][0], rect[0][1]
        width, height = rect[1][0], rect[1][1]

        rotated = frame_data.get('rotated', False)

        if rotated:
            box = (x, y, x + height, y + width)
            cropped = img.crop(box)
            cropped = cropped.rotate(90, expand=True)
        else:
            box = (x, y, x + width, y + height)
            cropped = img.crop(box)

        save_path = os.path.join(output_dir, frame_name.replace('/', '_'))
        cropped.save(save_path)
        count += 1

    print(f"✅ 成功切出 {count} 張動作畫格！存於: {output_dir}\n")

# ==========================================
# 🚀 啟動區 (加入了防閃退機制)
# ==========================================
if __name__ == "__main__":
    try:
        # 1. 你的來源檔案
        plist_file = r"D:\Users\user\Desktop\TT\pkm2png-master\export\effect_lihui_huangrong.atlas"
        png_file = r"D:\Users\user\Desktop\TT\pkm2png-master\export\effect_lihui_huangrong.png.png"
        
        # 2. 你的輸出資料夾
        output_folder = r"D:\Users\user\Desktop\TT\動起來\成果"
        
        print("🚀 啟動切割程序...")
        cut_sprite_sheet(plist_file, png_file, output_folder)
        
    except Exception as e:
        # 如果發生任何錯誤，這裡會把紅字印出來，絕對不會閃退！
        print("\n❌ 發生嚴重錯誤！死因如下：")
        traceback.print_exc()
        
    finally:
        # 不管成功還是失敗，最後一定會停在這裡等你按 Enter
        input("\n按下 Enter 鍵結束程式...")
