import cv2
import numpy as np


def apply_beautiful_blur(input_video, output_video, blur_strength=50):
    # Open the input video
    cap = cv2.VideoCapture(input_video)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Calculate blur kernel size based on blur strength (0-100%)
        kernel_size = int((blur_strength / 100) * min(width, height) / 10) * 2 + 1

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)

        # Write the blurred frame
        out.write(blurred)

        # Print progress
        frame_count += 1
        print(f"Processing frame {frame_count}")

    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()
