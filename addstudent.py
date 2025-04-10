import os
import cv2
def save_image_from_camera():
    base_path = "Images"
    
    # Ensure the 'Images' folder exists
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    # Ask the user for their name and check for duplicates
    while True:
        name = input("Enter your name: ").strip()
        if not name:
            print("Name cannot be empty. Please try again.")
            continue
        
        # Check if any file with the same name already exists
        duplicate_found = False
        for file in os.listdir(base_path):
            if file.startswith(name):
                duplicate_found = True
                break
        
        if duplicate_found:
            print(f"Name '{name}' already exists. Please enter a different name.")
        else:
            break  # Exit the loop if the name is unique
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    print("Press SPACE to capture an image, ESC to exit.")
    image_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Add information text to the display
        display_frame = frame.copy()
        cv2.putText(display_frame, f"Images captured: {image_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, f"Name: {name}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, "SPACE: capture | ESC: exit", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow("Camera", display_frame)
        key = cv2.waitKey(1)
        
        if key == 27:  # ESC key to exit
            break
        elif key == 32:  # SPACE key to capture image
            image_count += 1
            image_path = os.path.join(base_path, f"{name}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Image {image_count} saved at {image_path}")
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"Total images captured for {name}: {image_count}")
    print("Process completed!")

# Corrected main guard
if __name__ == "__main__":
    save_image_from_camera()