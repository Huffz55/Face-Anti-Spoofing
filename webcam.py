import cv2
import os
import time
import numpy as np

from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name

MODEL_DIR = "resources/anti_spoof_models"
DEVICE_ID = 0                                
SHOW_FPS   = True                           

predictor = AntiSpoofPredict(DEVICE_ID)
cropper   = CropImage()

models = []
for model_name in os.listdir(MODEL_DIR):
    h_in, w_in, m_type, scale = parse_model_name(model_name)
    models.append((model_name, h_in, w_in, scale))
print(f"Loaded {len(models)} models.")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Webcam açılamadı!")

prev_time = time.time()
fps = 0
frame_idx = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kare okunamadı, çıkılıyor...")
            break

        frame_idx += 1

        bbox = predictor.get_bbox(frame)

        prediction = np.zeros((1, 3))
        for model_name, h_in, w_in, scale in models:
            param = {
                "org_img": frame,
                "bbox": bbox,
                "scale": scale,
                "out_w": w_in,
                "out_h": h_in,
                "crop": scale is not None,
            }
            img = cropper.crop(**param)
            prediction += predictor.predict(img, os.path.join(MODEL_DIR, model_name))

        label = np.argmax(prediction)
        score = prediction[0][label] / 2

        if label == 1:  
            text  = f"Real  {score:.2f}"
            color = (255, 0, 0)  
        else:           
            text  = f"Fake  {score:.2f}"
            color = (0, 0, 255)

        cv2.rectangle(frame,
                      (bbox[0], bbox[1]),
                      (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                      color, 2)
        cv2.putText(frame, text,
                    (bbox[0], bbox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, color, 2)

        
        if SHOW_FPS:
            cur_time = time.time()
            if cur_time - prev_time >= 1.0:
                fps = frame_idx
                frame_idx = 0
                prev_time = cur_time
            cv2.putText(frame, f"{fps}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        
        cv2.imshow("Anti face Spoofing", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release() 
    cv2.destroyAllWindows()
