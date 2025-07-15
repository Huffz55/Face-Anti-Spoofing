# Silent Face Anti‑Spoofing – Web & Desktop Suite

Real‑time liveness detection powered by the **MiniVision “Silent‑Face Anti‑Spoofing”** model. Use it straight from your browser **or** as lightweight desktop tools.

---

## ✨ Features

| Mode                   | Script      | What it does                                                                                                                                                                                              |
| ---------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Web UI**             | `app.py`    | Launches a Flask web server where you can<br>▪ **Upload a photo** **or**<br>▪ **Open your webcam** directly in the browser.<br>The frame is analysed and returns **REAL / FAKE** with confidence overlay. |
| **Real‑time webcam**   | `webcam.py` | Opens your default camera in a window, performs live anti‑spoofing on each frame. <br>**Press `q`** to quit.                                                                                              |
| **Screenshot watcher** | `main.py`   | Every second grabs a screenshot of your desktop, scans faces, and saves annotated results to `captures/`. <br>**Press `c`** to clear saved images, **`q`** to quit.                                       |

---

## 🔧 Requirements

* Python ≥ 3.9
* OpenCV, NumPy, Flask (see `requirements.txt`)
* ONNX Runtime **OR** OpenVINO Runtime (optional, for acceleration)
* Model weights from the MiniVision repository

```bash
pip install -r requirements.txt
```

---

## 📥 Model Weights

1. Download **`anti-spoof-mn3.onnx`** (or any supported Silent‑Face variant) from the original project: [https://github.com/minivision-ai/Silent-Face-Anti-Spoofing-APK](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing-APK)
2. Place the file in **`resources/anti_spoof_models/`** (keep the default name or edit `config.py`).

```
Face-Anti-Spoofing/
├─ resources/
│  └─ anti_spoof_models/
│     └─ anti-spoof-mn3.onnx
```

---

## 🚀 Quick Start

### 1 · Clone & set up

```bash
git clone https://github.com/Huffz55/Face-Anti-Spoofing.git
cd Face-Anti-Spoofing
python -m venv venv           # optional but recommended
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2 · Run the Web UI

```bash
python app.py
```

Now browse to **[http://localhost:5000](http://localhost:5000)** ─ upload an image *or* click **“Open Webcam”**.

### 3 · Run the real‑time webcam tester

```bash
python webcam.py
```

Press **`q`** to exit.

### 4 · Run the screenshot watcher

```bash
python main.py
```

Every second a screenshot is saved to `captures/`. Press **`c`** to clear the folder, **`q`** to quit.

---

## 🗂️ Project Structure

```
.
├── app.py            # Flask web server
├── main.py           # Screenshot‑surveillance script
├── webcam.py         # Real‑time webcam CLI
├── src/              # Model helpers, preprocessing utils
├── templates/        # Jinja2 HTML pages for web UI
├── static/           # CSS/JS assets
├── resources/
│   └── anti_spoof_models/  # ONNX weights
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuration

* **Camera index**: edit `config.py` or pass `--device 1` when supported.
* **Confidence threshold**: change `THRESHOLD` in `src/config.py`.
* **Inference backend**: default is ONNX Runtime; set the `--openvino` flag (if implemented) to use OpenVINO.

---

## 🖼️ Demo

> Add your own GIF or screenshots here showing:
>
> 1. Web UI detecting a live face vs. photo.
> 2. Terminal window of `webcam.py`.
> 3. Auto‑saved screenshots from `main.py`.

---

## 📚 References & Acknowledgements

* **Silent‑Face Anti‑Spoofing** — MiniVision AI · MIT License · [https://github.com/minivision-ai/Silent-Face-Anti-Spoofing-APK](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing-APK)
* Thanks to the authors for the pre‑trained **MN3** liveness model.

---

## 📝 License

This repository is distributed under the **MIT License**.  See `LICENSE` for details.

---

## 🤝 Contributing

Pull requests are welcome! If you find a bug or have an idea, please open an issue first to discuss changes.
