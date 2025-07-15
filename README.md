# Silent Face Anti‑Spoofing – Web & Desktop Suite

Real‑time liveness detection powered by the **MiniVision “Silent‑Face Anti‑Spoofing”** model. Use it straight from your browser **or** as lightweight desktop tools.

---

## ✨ Features

| Mode                   | Script      | What it does                                                                                                                                                                                  |
| ---------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Web UI**             | `app.py`    | Launches a Flask web server where you can▪ **Upload a photo** **or**▪ **Open your webcam** directly in the browser.The frame is analysed and returns **REAL / FAKE** with confidence overlay. |
| **Real‑time webcam**   | `webcam.py` | Opens your default camera in a window, performs live anti‑spoofing on each frame. \*\*Press \*\***`q`** to quit.                                                                              |
| **Screenshot watcher** | `main.py`   | Every second grabs a screenshot of your desktop, scans faces, and saves annotated results to **`images/sample/`**. Press **`c`** to clear the folder, **`q`** to quit.                        |

---

## 🔧 Requirements

* Python ≥ 3.9
* OpenCV, NumPy, Flask — install via `requirements.txt`

```bash
pip install -r requirements.txt
```

---

## 📥 Model Weights

The pre‑trained **anti‑spoof‑mn3.onnx** file is **already included** in this repository inside
`resources/anti_spoof_models/`. No extra download is required.

> Original source & paper: [https://github.com/minivision-ai/Silent-Face-Anti-Spoofing](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing)
>
> For the best accuracy, supply portraits with a **3 : 4 aspect ratio** (e.g., 720 × 960).

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

Every second a screenshot is saved to `images/sample/`. Press **`c`** to clear the folder, **`q`** to quit.

---

## 🗂️ Project Structure

```
.
├── app.py            # Flask web server
├── main.py           # Screenshot‑surveillance script
├── webcam.py         # Real‑time webcam CLI
├── src/              # Model helpers, preprocessing utils
├── templates/        # HTML pages for web UI
├── static/           # Result images
├── resources/
│   └── anti_spoof_models/  # ONNX weights
├── requirements.txt
└── README.md
```
---
## 🖼️ Demo

> Add your own GIF or screenshots here showing:
>
> 1. Web UI detecting a live face vs. photo.
> 2. Terminal window of `webcam.py`.
> 3. Auto‑saved screenshots from `main.py`.

---

## 📚 References & Acknowledgements

* **Silent‑Face Anti‑Spoofing** — MiniVision AI · MIT License · [https://github.com/minivision-ai/Silent-Face-Anti-Spoofing](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing)
* Thanks to the authors for the pre‑trained **MN3** liveness model.

---

## 📝 License

This repository is distributed under the **MIT License**.  See `LICENSE` for details.

---

## 🤝 Contributing

Pull requests are welcome! If you find a bug or have an idea, please open an issue first to discuss changes.
