🧠 Face Recognition Attendance System

This project is a **real-time face recognition-based attendance system** developed using Python, OpenCV, and the `face_recognition` library. It captures faces via webcam, recognizes registered individuals, and automatically logs attendance data into Excel files with timestamps.

---

📌 Features

- 🎥 Real-time face detection and recognition via webcam  
- 📝 Automatically logs attendance with date & time  
- 💾 Stores attendance in timestamped Excel sheets  
- 🔁 Updates known faces from the images folder dynamically  
- 📦 Simple to use, no external database required (Excel-based logs)

---

🛠️ Technologies Used

- Python 3.x  
- OpenCV  
- `face_recognition` (Dlib-based face encoder)  
- Numpy  
- Pandas  
- OpenPyXL (Excel file support)

---

🗂️ Folder Structure

```
face-recognition-attendance/
│
├── Images/                   # Folder for storing student face images
├── attendance_records/       # Automatically generated attendance Excel files
├── EncodeFile.p              # Serialized known face encodings (auto-created)
├── main.py                   # Main Python script to run the project
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore                # Files to be ignored by Git
```

---

🧑‍💻 How to Run (Cloned Repository)

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/face-recognition-attendance.git
cd face-recognition-attendance
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Prepare image dataset:**
- Place face images of students inside the `Images/` folder.
- Filename (without extension) will be used as the student ID or name.  
  Example: `john_doe.jpg` → Name = `john_doe`

4. **Run the project:**
```bash
python main.py
```
> Press `q` to exit the webcam window.

📦 How to Run Without Cloning

1. **Download as ZIP:**
   - Click on the green **“Code”** button on the top right of the repository
   - Choose **“Download ZIP”**
   - Extract the ZIP file to a desired location

2. **Install dependencies manually:**
```bash
pip install opencv-python face_recognition numpy pandas openpyxl
```

3. **Follow the same steps as above:**
   - Add images to `Images/` folder
   - Run `main.py`

📝 Attendance Format

Attendance is saved to Excel files in the `attendance_records/` folder.

**Filename Format:**  
`attendance_YYYY-MM-DD_HH.xlsx`

**Excel Columns:**  
- `Name`: Student name or ID (from image filename)  
- `Time`: Time when detected  
- `Status`: Currently always "Present"

---

⚠️ Notes

- Make sure each image contains only **one clear face**.
- Encoding and detection are sensitive to lighting and face orientation.
- This is a **local system** — no data is uploaded to the cloud.


🔄 Future Improvements (Ideas)

- MongoDB integration for long-term logging  
- GUI or web-based dashboard  
- Entry/Exit recognition with separate timestamps  
- Email or SMS notifications  


🙌 Acknowledgements

- [face_recognition](https://github.com/ageitgey/face_recognition) – Python wrapper around dlib for face recognition.  
- OpenCV – Computer vision library for Python.

