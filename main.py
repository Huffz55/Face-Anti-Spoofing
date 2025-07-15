import cv2
import os
import time
import uuid
import subprocess
import sys
import numpy as np

SAMPLE_IMAGE_PATH = "./images/sample/"
os.makedirs(SAMPLE_IMAGE_PATH, exist_ok=True)

MODEL_DIR = "./resources/anti_spoof_models"
DEVICE_ID = 0

def resize_to_ratio(image, target_ratio=3/4):
    h, w, _ = image.shape
    current_ratio = w / h
    if abs(current_ratio - target_ratio) < 0.01:
        return image
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        start_x = (w - new_w) // 2
        return image[:, start_x:start_x+new_w, :]
    else:
        new_h = int(w / target_ratio)
        start_y = (h - new_h) // 2
        return image[start_y:start_y+new_h, :, :]

def run_test(image_name):
    python_executable = sys.executable  
    cmd = [
        python_executable, "test.py",
        "--image_name", image_name,
        "--model_dir", MODEL_DIR,
        "--device_id", str(DEVICE_ID)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    return result.stdout.strip() or result.stderr.strip()

def clear_sample_folder(folder_path=SAMPLE_IMAGE_PATH):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Silindi: {filename}")
        except Exception as e:
            print(f"{filename} silinirken hata oluştu: {e}")

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera açılamadı!")
        return

    last_capture = 0
    interval = 1

    label = "Unknown"
    confidence = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kare alınamadı, çıkılıyor.")
            break

       
        frame_cropped = resize_to_ratio(frame, target_ratio=3/4)

        now = time.time()
        if now - last_capture > interval:
            filename = f"{uuid.uuid4().hex}.jpg"
            filepath = os.path.join(SAMPLE_IMAGE_PATH, filename)

            
            cv2.imwrite(filepath, frame_cropped)

            output = run_test(filename)
            print("Model çıktısı:", output)

            
            try:
                if "Real Face" in output:
                    label = "Real"
                    score_part = output.split("Score: ")[1]
                    score_str = score_part.split("\n")[0].rstrip(".")
                    confidence = float(score_str)
                elif "Fake Face" in output:
                    label = "Fake"
                    score_part = output.split("Score: ")[1]
                    score_str = score_part.split("\n")[0].rstrip(".")
                    confidence = float(score_str)
                else:
                    label = "Unknown"
                    confidence = 0.0
            except Exception as e:
                print("Skor ayrıştırma hatası:", e)
                label = "Unknown"
                confidence = 0.0

            last_capture = now

        color = (0, 255, 0) if label == "Real" else (0, 0, 255)
        text = f"{label} ({confidence:.2f})"

        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), color, 3)
        cv2.putText(frame, text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 4)

        cv2.imshow("Live Anti-Spoofing", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  
            print("Programdan çıkılıyor...")
            break
        elif key == ord('c'):  
            print("Sample klasörü temizleniyor...")
            clear_sample_folder()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
