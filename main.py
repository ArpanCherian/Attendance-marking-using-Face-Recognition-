import cv2 as cv
import face_recognition
import os
import pickle
import numpy as np
from datetime import datetime
import time
import pandas as pd
import openpyxl

# Function to generate face encodings from images
def find_encodings(images_list):
    encodings_list = []
    for img in images_list:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # Convert to RGB
        encodings = face_recognition.face_encodings(img)[0]  # Get face encodings
        encodings_list.append(encodings)
    return encodings_list

def mark_attendance(name):
    timestamp = datetime.now()
    date = timestamp.strftime('%Y-%m-%d')
    time = timestamp.strftime('%H:%M:%S')
    
    # Create the directory if it doesn't exist
    save_path = r"YOUR ATTENDANCE RECORD PATH"
    os.makedirs(save_path, exist_ok=True)
    
    # Create full path for the Excel file
    filename = os.path.join(save_path, f"attendance_{timestamp.strftime('%Y-%m-%d_%H')}.xlsx")
    
    if os.path.exists(filename):
        df = pd.read_excel(filename)
    else:
        df = pd.DataFrame(columns=['Name', 'Time','Status'])
    if name in df['Name'].values:
        idx = df.index[df['Name'] == name].tolist()[0]
        df.at[idx, 'Time'] = time

    else:
        # Add new record
        new_row = {'Name': name, 'Time': time, 'Status': 'Present'}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    df.to_excel(filename,index=False)

# Function to update encodings with new students
def update_encodings(folder_path, encode_file_path):
    # Load existing encodings if the file exists
    if os.path.exists(encode_file_path):
        with open(encode_file_path, 'rb') as file:
            encode_list_known_with_id = pickle.load(file)
        encode_list_known, student_ids = encode_list_known_with_id
    else:
        encode_list_known = []
        student_ids = []

    # Get list of images in the folder
    path_list = os.listdir(folder_path)
    img_list = []
    new_student_ids = []

    # Load new images and extract student IDs from filenames
    for path in path_list:
        if os.path.splitext(path)[0] not in student_ids:  # Check if the student is already encoded
            img_list.append(cv.imread(os.path.join(folder_path, path)))
            new_student_ids.append(os.path.splitext(path)[0])  # Remove file extension

    # Generate encodings for new students
    if img_list:
        print("New students found. Generating encodings...")
        new_encode_list = find_encodings(img_list)
        encode_list_known.extend(new_encode_list)
        student_ids.extend(new_student_ids)

        # Save updated encodings to the file
        with open(encode_file_path, 'wb') as file:
            pickle.dump([encode_list_known, student_ids], file)
        print("Encodings updated and saved.")
    else:
        print("No new students found.")

    return encode_list_known, student_ids

# Step 1: Update encodings with new students
folder_path = r'YOUR IMAGE FOLDER PATH'  # Folder containing images
encode_file_path = "EncodeFile.p"
encode_list_known, student_ids = update_encodings(folder_path, encode_file_path)

# Step 2: Real-Time Face Recognition
# Initialize webcam
cap = cv.VideoCapture(0)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height

# Confidence threshold for face recognition
confidence_threshold = 0.5  # Adjust this value as needed

while True:
    success, img = cap.read()  # Capture frame from webcam
    if not success:
        print("Failed to capture image from webcam.")
        break

    # Resize and convert image to RGB for face recognition
    img_small = cv.resize(img, (0, 0), None, 0.25, 0.25)  # Resize to 1/4th for faster processing
    img_small = cv.cvtColor(img_small, cv.COLOR_BGR2RGB)

    # Detect faces in the current frame
    face_locations = face_recognition.face_locations(img_small)
    face_encodings = face_recognition.face_encodings(img_small, face_locations)

    # Loop through detected faces
    for encode_face, face_loc in zip(face_encodings, face_locations):
        # Compare the current face encoding with known encodings
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_distances = face_recognition.face_distance(encode_list_known, encode_face)
        match_index = np.argmin(face_distances)

        # Check if the match is confident enough
        if matches[match_index] and face_distances[match_index] < confidence_threshold:
            #print("Known face detected")
            #print("Student name:", student_ids[match_index])
            mark_attendance(student_ids[match_index]);

            # Scale face location back to original size
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            # Draw green bounding box around the detected face
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box
            cv.putText(img, f"ID: {student_ids[match_index]}", (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the webcam feed with bounding boxes
    cv.imshow("Face Recognition", img)

    # Exit on 'q' key press
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv.destroyAllWindows()
