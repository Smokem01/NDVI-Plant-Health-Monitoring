# NDVI Plant Health Monitoring System

This application captures daily images using a Raspberry Pi camera module, processes them to calculate the Normalized Difference Vegetation Index (NDVI), analyzes plant health, and saves both the processed images and analysis results. It features a graphical user interface (GUI) for easy management of the monitoring system and health reports.

## Features

- **Graphical User Interface** with two tabs:
  - Start/Stop monitoring and display the next scheduled task
  - View the latest health analysis and logs
- Automated daily NDVI image capture and processing
- Advanced plant health analysis using color-based NDVI levels
- Visualization of plant areas and health indicators
- Detailed analysis reports including plant coverage and health scores
- Automatic file naming with timestamps
- Robust error handling and logging

## Important Note on Threshold Parameters

**PLEASE NOTE**: The current threshold parameters used in the health analysis are placeholders and do not represent accurate values for plant health assessment. These parameters will be corrected and updated following a precise and thorough data collection process. Users should be aware that current health assessments may not be accurate and should be considered experimental until the parameters are properly calibrated.

## Versions

### Raspberry Pi Version
- Uses Raspberry Pi NoIR Camera Module or HQ Camera Module
- Optimized for 24/7 operation on Raspberry Pi hardware

### PC Version (Coming Soon)
- Will support various USB NIR-capable cameras
- Same functionality as Raspberry Pi version
- Adapted for standard computer hardware
- Will include specific camera recommendations and setup instructions

## Requirements

### For Raspberry Pi Version
#### Hardware:
- Raspberry Pi (any model supporting camera modules, tested on RPi 4 Model B)
- Raspberry Pi NoIR Camera Module or HQ Camera Module or similar

#### Software:
- Python 3.x
- OpenCV
- NumPy
- picamera2
- schedule
- pillow

### For PC Version (Coming Soon)
#### Hardware:
- PC with USB port
- NIR-capable USB camera (specific models to be listed)

#### Software:
- Python 3.x
- OpenCV
- NumPy
- schedule
- pillow
- Additional camera drivers (to be specified)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Smokem01/NDVI-Plant-Health-Monitoring.git
   cd NDVI-Plant-Health-Monitoring
   ```

2. Install the required packages:
   For Raspberry Pi:
   ```
   pip install opencv-python numpy picamera2 schedule pillow
   ```
   
   For PC (Coming Soon):
   ```
   pip install opencv-python numpy schedule pillow
   ```

## Usage

Run the daily checker script:

```
python gui.py
```

By default, the script will:
- Capture an image daily at 9:00 AM
- Process the image for NDVI analysis
- Generate health analysis and visualization
- Save results in the 'results' directory
- Displays latest analysis results in `Latest Results` tab

## File Structure

- `gui.py`: Main interface for starting/stopping the system and viewing logs and analysis
- `daily_checker.py`: Class responsible for scheduling and running daily captures
- `ndvi_processor.py`: Contains the NDVIProcessor class for NDVI calculations
- `ndvi_analyser.py`: Contains the NDVIAnalyzer class for health analysis
- `color_map.py`: Defines the color mapping for NDVI visualization
- `results/`: Directory where processed images and analysis reports are saved

## Output Files

For each capture, the system generates:
- A visualization image with plant area highlighted and health indicators (`result-vis-[timestamp].png`)
- A text file with detailed analysis (`result-[timestamp].txt`)

## Customization

- Modify the capture time in `daily_checker.py` by changing the scheduled time
- Adjust health level thresholds in `ndvi_analyser.py` (Note: current thresholds are placeholders)
- Customize the color map in `color_map.py` for different visualization preferences

## Future Updates

- Release of PC version with support for various USB NIR cameras
- Calibration of accurate threshold parameters based on thorough data collection
- Additional visualization options
- Web interface for remote monitoring (planned)

## Current Limitations

- Health assessment thresholds are currently placeholder values and will be updated
- Analysis results should be considered experimental until proper calibration is completed
