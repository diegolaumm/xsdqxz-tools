import os
import re
import xxtea

# ===== 📁 資料夾自動設定 =====
# 會自動在 Python 腳本同一個目錄下建立這三個資料夾
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LUAC_DIR = os.path.join(BASE_DIR, "01_raw_luac")       # 原始 .luac 放這裡
LUA_DIR = os.path.join(BASE_DIR, "02_decrypted_lua")   # 解密後的 .lua 存放處
TXT_DIR = os.path.join(BASE_DIR, "03_extracted_txt")   # 提取後的 .txt 存放處

# 金鑰與簽章 (維持你找到的終極金鑰)
KEY = b"YOUR_KEY_HERE"
SIGN = b"MQKK"

def setup_folders():
    """自動建立所需資料夾"""
    for folder in [LUAC_DIR, LUA_DIR, TXT_DIR]:
        os.makedirs(folder, exist_ok=True)

def decrypt_luac(luac_path, lua_path):
    """第一階段：解密 .luac 成 .lua"""
    try:
        with open(luac_path, 'rb') as f:
            data = f.read()

        if data.startswith(SIGN):
            data = data[len(SIGN):]  # 切除 MQKK 簽章
            decrypted_data = xxtea.decrypt(data, KEY, padding=False)
            
            with open(lua_path, 'wb') as f:
                f.write(decrypted_data)
            return True
        else:
            print(f"  ⚠️ 跳過 [{os.path.basename(luac_path)}]：找不到 MQKK 簽章")
            return False
    except Exception as e:
        print(f"  ❌ 解密發生錯誤 [{os.path.basename(luac_path)}]: {e}")
        return False

def extract_txt(lua_path, txt_path):
    """第二階段：讀取 .lua 並提取中英文字詞至 .txt"""
    try:
        with open(lua_path, 'rb') as f:
            raw_data = f.read()

        text_data = raw_data.decode('utf-8', errors='ignore')
        matches = re.findall(r'[a-zA-Z0-9\u4e00-\u9fa5]{2,}', text_data)

        with open(txt_path, 'w', encoding='utf-8') as f:
            count = 0
            for word in matches:
                f.write(f"{word}\t")
                count += 1
                if count % 5 == 0:
                    f.write("\n")
        return len(matches)
    except Exception as e:
        print(f"  ❌ 文字提取錯誤 [{os.path.basename(lua_path)}]: {e}")
        return 0

def batch_process():
    setup_folders()
    
    # 搜尋 01_raw_luac 資料夾內所有的 .luac 檔案
    luac_files = [f for f in os.listdir(LUAC_DIR) if f.lower().endswith('.luac')]

    if not luac_files:
        print("📂 找不到可處理的檔案！")
        print(f"👉 請把要處理的 .luac 檔案放進資料夾：\n   {LUAC_DIR}")
        return

    print(f"🚀 開始執行全自動流水線，共偵測到 {len(luac_files)} 個 .luac 檔案...\n" + "-" * 60)

    success_count = 0
    for filename in luac_files:
        file_base = os.path.splitext(filename)[0]
        
        luac_path = os.path.join(LUAC_DIR, filename)
        lua_path = os.path.join(LUA_DIR, f"{file_base}_decrypted.lua")
        txt_path = os.path.join(TXT_DIR, f"{file_base}_decrypted.txt")

        print(f"🔍 處理中: {filename}")

        # 步驟 1: 解密 .luac -> .lua
        if decrypt_luac(luac_path, lua_path):
            # 步驟 2: 提取 .lua -> .txt
            words = extract_txt(lua_path, txt_path)
            print(f"  └─ ✅ 成功！已生成 .lua 與 .txt (共抓出 {words} 個單字)")
            success_count += 1

    print("-" * 60)
    print(f"🎉 批次處理完畢！成功率：{success_count}/{len(luac_files)}")
    print(f"📂 解密 .lua 資料夾：{LUA_DIR}")
    print(f"📂 文字 .txt 資料夾：{TXT_DIR}")

if __name__ == "__main__":
    batch_process()
    input("\n按下 Enter 鍵結束...")
