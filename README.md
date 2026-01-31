# **🎵 YT Music to MP3 Converter**

A sleek, full-stack web application that allows users to convert YouTube Music links into high-quality MP3 files. This tool automatically embeds the **song title**, **artist name**, and **high-resolution thumbnail** directly into the MP3 metadata.

## 

**🛠 Features**

* **Metadata Embedding:** Automatically attaches thumbnails and ID3 tags.  
* **Clean Filenames:** Downloads files named after the song title, not random strings.  
* **FastAPI Backend:** High-performance Python backend using yt-dlp.  
* **Modern UI:** Built with React and Tailwind CSS for a responsive, dark-mode experience.  
* **Auto-Cleanup:** Temporary server files are deleted immediately after download to save space.

## 

**📂 Project Structure**

Navigate through the codebase using this guide:

Plaintext

yt-mp3-converter/  
├── backend/  
│   ├── main.py            \# FastAPI server, download logic & metadata tagging  
│   ├── requirements.txt   \# Python dependencies (yt-dlp, mutagen, etc.)  
│   └── downloads/         \# Temporary storage (auto-created)  
├── frontend/  
│   ├── src/  
│   │   ├── App.js         \# Main UI logic and API handling  
│   │   └── index.css      \# Tailwind CSS directives  
│   ├── tailwind.config.js \# Tailwind styling configuration  
│   └── package.json       \# React dependencies  
├── install\_project.bat    \# Windows: One-click setup script  
└── run\_project.bat        \# Windows: One-click start script

## 

**🚦 Prerequisites**

Before you begin, ensure you have the following installed:

1. **Python 3.8+**  
2. **Node.js (LTS)**  
3. **FFmpeg** (Essential for audio conversion)  
   * **Windows:** Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/). Extract and add the bin folder to your **System PATH**.  
   * **Mac:** brew install ffmpeg  
   * **Linux:** sudo apt install ffmpeg

## 

**🚀 Getting Started (Windows)**

The easiest way to get started is using the provided automation scripts:

1. **Clone the Repository:**  
   Bash  
   ```
   git clone https://github.com/your-username/your-repo-name.git  
   cd your-repo-name
    ```
2. **Installation:** Double-click install\_project.bat. This will create a Python virtual environment and install all Node modules.  
3. **Run the App:** Double-click run\_project.bat. Two windows will open:  
   * **Backend:** Running at http://localhost:8000  
   * **Frontend:** Running at http://localhost:3000

## 

**🛠 Manual Setup (Linux/Mac/Manual)**

### **1\. Backend Setup**

Bash
```
cd backend  
python \-m venv venv  
source venv/bin/activate  \# Windows: venv\\Scripts\\activate  
pip install \-r requirements.txt  
python main.py
```
### **2\. Frontend Setup**

Bash
```
cd frontend  
npm install  
npm start
```
## 

**💡 How it Works (For Learners)**

1. **The Request:** The React frontend sends the YouTube URL to the FastAPI /convert endpoint.  
2. **The Download:** The backend uses yt-dlp to fetch the audio and the thumbnail image.  
3. **The Processing:** FFmpeg converts the raw audio into a 192kbps MP3.  
4. **The Tagging:** We use the mutagen library (or yt-dlp post-processors) to "stitch" the image and text data into the MP3 file.  
5. **The Stream:** The backend sends the file back as a FileResponse.  
6. **The Cleanup:** Once the user finishes downloading, a BackgroundTasks function in FastAPI deletes the file from the server to keep things tidy.

## 

**⚠️ Disclaimer**

This tool is for educational purposes and personal use only. Please respect the terms of service of the content platforms and the rights of the content creators.