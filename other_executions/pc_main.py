import time
import cv2
import numpy as np
from ndvi_processor import NDVIProcessor
from collections import deque
import os

def get_next_id():
    id_file = 'id.txt'
    if os.path.exists(id_file):
        with open(id_file, 'r') as f:
            last_id = int(f.read().strip())
    else:
        last_id = 0
    
    next_id = last_id + 1
    with open(id_file, 'w') as f:
        f.write(str(next_id))
    
    return next_id

def main():
    run_id = get_next_id()
    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return None

    processor = NDVIProcessor()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None 

    max_frames = 108000  # approx. 1hr at 30 FPS, might be inaccurate depending on processing time
    buffer = deque(maxlen=max_frames)

    tot_frames = 0
    start_time = time.time()

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Failed to grab frame")
                break

            if len(frame.shape) == 2:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            elif frame.shape[2] == 4: 
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

            processed_frame = processor.process_image(frame)

            smaller_frame = cv2.resize(processed_frame, (640, 480))
            buffer.append(smaller_frame)
            cv2.imshow('NDVI Stream', processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            tot_frames += 1

            #this is completely optional, just a periodic terminal
            if tot_frames % 30 == 0:  #30 FPS
                elapsed_time = time.time() - start_time
                print(f"Processed {tot_frames} frames. Elapsed time: {elapsed_time:.2f} seconds")

    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        camera.release()
        cv2.destroyAllWindows()
        end_time = time.time()
        duration = end_time - start_time
        print(f"Total frames: {tot_frames}")
        print(f"Total duration: {duration:.2f} seconds")

        if buffer:
            filename = f'output_{run_id}.mp4'
            output_path = os.path.join(output_dir, filename)
            out = cv2.VideoWriter(output_path, fourcc, 30, (640, 480))
            for frame in buffer:
                out.write(frame)
            out.release()
            print(f"Saved in: {output_path}")
        else:
            print("No frames were captured.")

    return output_path

if __name__ == "__main__":
    video_file = main()
    if video_file:
        print(f"Video saved as: {video_file}")
    else:
        print("Failed to create video.")
