# NDVI Processing Application

This application captures video from a camera (either a standard webcam or a Raspberry Pi camera module), processes each frame to calculate the Normalized Difference Vegetation Index (NDVI), and saves the processed video. It's designed to run continuously, saving the last hour of footage.

## Features

- Real-time NDVI processing of video frames
- Support for both standard webcams (PC version) and Raspberry Pi camera module
- Circular buffer to store the last hour of footage
- Automatic ID system for naming output files
- Progress tracking and error handling

## Requirements

### For PC Version
#### Software:
- Python 3.x
- OpenCV (`cv2`)
- NumPy
#### Hardware:
- Any USB webcam supporting NIR (Near-Infrared) captures

### For Raspberry Pi Version
#### Software:
- Python 3.x
- OpenCV (`cv2`)
- NumPy
- picamera2
#### Hardware:
- Raspberry Pi Noir or HQ Camera module, or similar

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Smokem01/NDVI-Plant-Health-Monitoring.git
   cd NDVI-Plant-Health-Monitoring
   ```

2. Install the required packages:
   ```
   pip install opencv-python numpy
   ```

   For Raspberry Pi, also install picamera2:
   ```
   pip install picamera2
   ```

## Usage

### PC Version (with standard webcam)

Run the main script:

```
python PC_main.py
```

### Raspberry Pi Version

Run the Raspberry Pi specific script:

```
python RPi_main.py
```

## File Structure

- `main_pc.py`: Main script for PC with standard webcam
- `main_raspberry.py`: Main script for Raspberry Pi
- `ndvi_processor.py`: Contains the NDVIProcessor class for NDVI calculations
- `id.txt`: Stores the current ID for naming output files
- `outputs/`: Directory where processed videos are saved

## Customization

- Adjust the `max_frames` variable in the main scripts to change the duration of saved footage.
- Modify the `process_image` method in `NDVIProcessor` class to change how NDVI is calculated or to add additional processing steps.