import schedule
import time
from datetime import datetime
import os
from picamera2 import Picamera2
from ndvi_processor import NDVIProcessor
from ndvi_analyser import NDVIAnalyzer
import cv2

def capture_and_process():
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    camera = Picamera2()
    camera.start()
    processor = NDVIProcessor()
    analyzer = NDVIAnalyzer()
    
    try:
        frame = camera.capture_array()
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        
        processed_frame = processor.process_image(frame)
        analysis_results = analyzer.analyze_health(processed_frame)
        visualization = analyzer.visualize_analysis(processed_frame)
        
        timestamp = datetime.now().strftime("%H-%M_%d-%m-%Y")
        visualized_img = f"result-vis-{timestamp}.png"
        analysis_results = f"result-{timestamp}.txt"
        
        cv2.imwrite(os.path.join(results_dir, visualized_img), visualization)
        timestamp_for_txt = datetime.now().strftime("%H:%M_%d/%m/%Y")
        path = os.path.join(results_dir, img)
        cv2.imwrite(path, processed_frame) 
        with open(os.path.join(results_dir, analysis_results), 'w') as f:
            f.write(f"NDVI Analysis Results for {timestamp_for_txt}\n\n")
            f.write(f"Plant Coverage: {analysis_results['plant_percentage']:.1f}% of image\n")
            f.write(f"Overall Health Score: {analysis_results['health_score']:.1f}/100\n\n")
            f.write(f"\nAnalysis:\n{analysis_results['analysis']}")    
        print(f"Captured, analyzed, and saved NDVI data for {timestamp_for_txt}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
    finally:
        camera.stop()

def main():
    print("Starting daily NDVI capture script...")
    schedule.every().day.at("09:00").do(capture_and_process)
    while True:
        schedule.run_pending()
        time.sleep(3600) #here it checks every hour, change accordingly

if __name__ == "__main__":
    main()