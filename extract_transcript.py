from paddleocr import PaddleOCR
import cv2
import os
from googletrans import Translator
import subprocess
import shutil

def convert_video_to_images(output_folder, video_path):
    os.makedirs("tmp", exist_ok=True)
    
    output_pattern = f"{output_folder}/frame_%04d.png"  # Frame naming pattern

    command = [
        "ffmpeg",
        "-i", video_path,       # Input file
        "-vf", f"fps=3",  # Extract frames at given rate
        output_pattern,         # Output filename pattern
        "-hide_banner",
        "-loglevel", "error"    # Suppress unnecessary output
    ]

    subprocess.run(command, check=True)
    print(f"Frames extracted to {output_folder}")

def ocr_and_translate_images(input_directory, output_path):
    # Khởi tạo PaddleOCR và Translator
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 'ch' cho tiếng Trung, 'en' cho tiếng Anh
    translator = Translator()

    # Mở file đầu ra
    with open(output_path, 'w', encoding='utf-8') as f:
        # Duyệt qua tất cả các file trong thư mục
        for filename in os.listdir(input_directory):
            if filename.endswith(('.png', '.jpg', '.jpeg')):  # Kiểm tra định dạng file hình ảnh
                image_path = os.path.join(input_directory, filename)  # Đường dẫn đầy đủ đến hình ảnh
                print(f"Đang xử lý: {filename}")

                # Đọc hình ảnh
                image = cv2.imread(image_path)

                # Thực hiện nhận diện văn bản
                result = ocr.ocr(image_path, cls=True)

                # Kiểm tra kết quả
                if result is None or (len(result) == 1 and result[0] is None):
                    # f.write(f"{filename}: Không phát hiện văn bản\n")  # Ghi thông báo không có văn bản
                    print(f"Không phát hiện văn bản trong {filename}")
                    continue

                # Gộp kết quả
                ocr_result = ""
                for line in result:
                    for word_info in line:
                        text = word_info[1][0]
                        ocr_result += text + " "  # Gộp các từ lại với nhau

                # Dịch kết quả
                translated_result = translator.translate(ocr_result.strip(), dest='en').text

                # Ghi kết quả vào file
                f.write(f"{filename}: {ocr_result.strip()} ({translated_result})\n")  # Ghi tên file và kết quả OCR

    shutil.rmtree(input_directory)
    print(f"Đã lưu kết quả vào {output_path}")

# Sử dụng hàm
input_directory = 'tmp'  # Đường dẫn đến thư mục chứa hình ảnh

convert_video_to_images(input_directory, 'D:\TIKTOK\DOUYIN\TiAmo_0530\oYY9vtE3yeLioONxAVZ5bQgQDfAlFAgPtBOmdI.mp4')

output_path = 'output.txt'  # Đường dẫn đến file đầu ra

ocr_and_translate_images(input_directory, output_path)