from pathlib import Path
import json
from shutil import copyfile
import re


def move_movies_by_activity():
    video_dir_path = Path('Videos')
    movie_dir_path = Path('Dataset/Movie')
    
    for movie_path in movie_dir_path.glob('**/*.mp4'):
        movie_stem = movie_path.name.replace(' ', '_')
        base_name = re.sub(r'_\d+\.mp4$', '', movie_stem)
        scene_id = movie_path.parent.parent.name
        output_dir_path = video_dir_path / scene_id /base_name
        output_dir_path.mkdir(exist_ok=True, parents=True)
        
        copyfile(movie_path, output_dir_path / f'{movie_stem}.mp4')
        print("copy: ", movie_path,  output_dir_path / f'{movie_stem}.mp4')
        
def move_movies_by_episode():
    episode_video_dir_path = Path('episodes_videos')
    video_dir_path = Path('Videos')
    activity_dir_path = Path('Dataset') / 'CompleteData' / 'Episodes'
    
    for activity_path in activity_dir_path.glob('*.json'):
        with open(activity_path, 'r') as f:
            data = json.load(f)
        
        scene_id = activity_path.stem.split('_')[0]
        
        input_dir_path = video_dir_path / scene_id
        output_dir_path = episode_video_dir_path / activity_path.stem
        output_dir_path.mkdir(exist_ok=True, parents=True)
            
        activities = data['data']['activities']
        for i, activity in enumerate(activities):
            for video_path in input_dir_path.glob(f'**/{activity}_0.mp4'):
                copyfile(video_path, output_dir_path / f'{i}_{video_path.stem}.mp4')
                print("copy: ", video_path, output_dir_path / f'{i}_{video_path.stem}.mp4')


def main():
    move_movies_by_episode()


if __name__ == '__main__':
    main()