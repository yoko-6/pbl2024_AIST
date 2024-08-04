import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# ロギングの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def create_pdf_from_video_frames(folder_path, frame_interval_sec=None):
    folder_path = Path(folder_path)
    video_files = list(folder_path.glob('*.mp4'))

    base_name = folder_path.stem
    output_pdf = folder_path / f'{base_name}.pdf'

    caps = [cv2.VideoCapture(str(video_file)) for video_file in video_files]

    fps = caps[0].get(cv2.CAP_PROP_FPS)
    interval_frames = int(fps * frame_interval_sec) if frame_interval_sec is not None else int(fps)
    
    frame_counts = [int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) for cap in caps]
    min_frame_count = min(frame_counts)

    images = []
    for idx in range(0, min_frame_count, interval_frames):
        frames_to_save = []
        for cap in caps:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frames_to_save.append(frame)
        
        combined_frame = np.vstack(frames_to_save)
        
        # 画像をメモリ内で処理
        img = Image.fromarray(cv2.cvtColor(combined_frame, cv2.COLOR_BGR2RGB))
        images.append(img)

    # PDFを保存
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])

    for cap in caps:
        cap.release()

def process_activity_dir(activity_dir_path, frame_interval_sec):
    logging.info(f'Starting processing for {activity_dir_path}')
    
    try:
        create_pdf_from_video_frames(activity_dir_path, frame_interval_sec)
        logging.info(f'Completed processing for {activity_dir_path}')
    except Exception as e:
        logging.error(f'Error processing {activity_dir_path}: {e}')

def main():
    video_dir_path = Path.cwd() / 'Videos' / 'scene1'
    
    activity_dirs = [activity_dir_path for activity_dir_path in video_dir_path.iterdir() if activity_dir_path.is_dir()]
    frame_interval_sec = 0.1
    
    # activity_dirs = activity_dirs[:4]
    # create_pdf_from_video_frames(activity_dirs[0], frame_interval_sec)
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_activity_dir, activity_dir_path, frame_interval_sec) for activity_dir_path in activity_dirs]
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f'Error occurred: {e}')

if __name__ == '__main__':
    main()
