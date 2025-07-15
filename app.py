from flask import Flask, request, render_template, jsonify, Response
import os
import shutil
import test
import cv2
import numpy as np
import time
from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name

app = Flask(__name__)

DEVICE_ID = 0
UPLOAD_FOLDER = 'images/sample'
RESULT_FOLDER = 'static/images'
MODEL_DIR = 'resources/anti_spoof_models'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

predictor = AntiSpoofPredict(DEVICE_ID)
cropper = CropImage()

models = []
for model_name in os.listdir(MODEL_DIR):
    h_in, w_in, m_type, scale = parse_model_name(model_name)
    models.append((model_name, h_in, w_in, scale))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'Resim dosyası gönderilmedi.'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi.'})

    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    result_text = test.test(filename, MODEL_DIR, DEVICE_ID)

    if not result_text:
        return jsonify({'error': 'Model tahmin hatası!'})

    ext = os.path.splitext(filename)[1]
    result_image_name = filename.replace(ext, f"_result{ext}")
    result_path = os.path.join(UPLOAD_FOLDER, result_image_name)
    public_result_path = os.path.join(RESULT_FOLDER, result_image_name)

    shutil.copy(result_path, public_result_path)

    return jsonify({
        "result": result_text,
        "image_url": f"/static/images/{result_image_name}"
    })


def gen_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Webcam açılamadı!")

    prev_time = time.time()
    frame_count = 0
    fps = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        cur_time = time.time()
        if cur_time - prev_time >= 1.0:
            fps = frame_count
            frame_count = 0
            prev_time = cur_time
        
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
            text = f"Real  {score:.2f}"
            color = (255, 0, 0)
        else:  
            text = f"Fake  {score:.2f}"
            color = (0, 0, 255)

        
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 2)
        cv2.putText(frame, text, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.putText(frame, f"{fps} FPS", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        ret2, buffer = cv2.imencode('.jpg', frame, encode_param)
        if not ret2:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

