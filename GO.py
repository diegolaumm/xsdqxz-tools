import os
import struct
import lz4.block

def decode_ddd3_file(file_path, output_dir):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        if data[0:4] != b'DDD3':
            return False

        total_uncompressed_size = struct.unpack('<I', data[4:8])[0]
        final_decompressed_data = bytearray()
        offset = 8
        CHUNK_SIZE = 16384  
        chunk_count = 1

        print(f"\n▶ 處理中: {os.path.basename(file_path)}")

        while offset < len(data) and len(final_decompressed_data) < total_uncompressed_size:
            if offset + 4 > len(data):
                break
            
            comp_size = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            
            comp_data = data[offset:offset+comp_size]
            offset += comp_size
            
            expected_uncomp_size = min(CHUNK_SIZE, total_uncompressed_size - len(final_decompressed_data))
            
            dict_data = bytes(final_decompressed_data[-65536:]) if len(final_decompressed_data) > 0 else None
            
            try:
                if dict_data:
                    decomp_data = lz4.block.decompress(comp_data, uncompressed_size=expected_uncomp_size, dict=dict_data)
                else:
                    decomp_data = lz4.block.decompress(comp_data, uncompressed_size=expected_uncomp_size)
            except Exception as e:
                print(f"  ❌ 崩潰！錯誤訊息: {e}")
                return False
                
            final_decompressed_data.extend(decomp_data)
            chunk_count += 1

        # 存檔：把路徑改到指定的 output_dir 裡面
        filename = os.path.basename(file_path)
        output_path = os.path.join(output_dir, filename + ".pkm")
        
        with open(output_path, 'wb') as f:
            f.write(final_decompressed_data)

        print(f"✅ 成功拼接 {chunk_count-1} 塊碎肉，已存入輸出資料夾。")
        return True
        
    except Exception as e:
        print(f"[嚴重錯誤] {os.path.basename(file_path)} 發生例外: {e}")
        return False

def batch_decode(input_folder, output_folder):
    print(f"🔍 終極解包任務啟動！")
    print(f"📥 來源資料夾: {input_folder}")
    print(f"📤 輸出資料夾: {output_folder}\n")
    
    # 如果輸出資料夾不存在，就自動建立一個
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 已自動建立輸出資料夾。")
        
    success_count = 0
    
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            if decode_ddd3_file(file_path, output_folder):
                success_count += 1
                
    print(f"\n🎉 駭客任務完成！共成功完美還原了 {success_count} 張圖片！")
    print(f"👉 請到 {output_folder} 查看你的戰利品！")

# ==========================================
# 🚀 啟動區：設定你的輸入與輸出資料夾
# ==========================================
if __name__ == "__main__":
    # 這裡放你原始 .ddd3 檔案的資料夾
    INPUT_DIR = r"D:\Users\user\Desktop\TT\input" 
    
    # 這裡放你希望解包後 .pkm 檔案存放的資料夾
    OUTPUT_DIR = r"D:\Users\user\Desktop\TT\pkm2png-master\pkmFiles" 
    
    batch_decode(INPUT_DIR, OUTPUT_DIR)
    input("\n按下 Enter 鍵結束程式...")
