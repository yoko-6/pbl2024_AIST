import cv2
from pathlib import Path
from tqdm import tqdm

def concatenate_videos(folder_path, output_path):
    # 動画ファイルのパスを番号順に取得
    folder = Path(folder_path)
    video_files = sorted(folder.glob("*.mp4"), key=lambda x: int(x.stem.split('_')[0]))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 初期化
    video_streams = []
    frame_width = frame_height = None
    fps = None

    # 動画ファイルを順に読み込み
    for video_file in video_files:
        cap = cv2.VideoCapture(str(video_file))
        if not cap.isOpened():
            print(f"Error opening video file: {video_file}")
            continue
        
        # 最初の動画ファイルでパラメータを取得
        if frame_width is None or frame_height is None or fps is None:
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
        
        video_streams.append(cap)

    # 動画の書き込み
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (frame_width, frame_height))

    for cap in video_streams:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        cap.release()
    
    out.release()

def main():
    episode_video_dir_path = Path('episodes_videos')
    output_dir_path = Path('episodes_videos_concatenated')
    
    video_dir_paths = [p for p in episode_video_dir_path.glob('*') if p.is_dir()]
    
    for video_dir in tqdm(video_dir_paths):
        concatenate_videos(video_dir, output_dir_path / f"{video_dir.stem}.mp4")
    
if __name__ == '__main__':
    main()
