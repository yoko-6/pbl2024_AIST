from pathlib import Path

def make_qa_path_list(dataset_dir_path, output_dir_path, scene, day):
    qa_file_paths = set(dataset_dir_path.glob(f'QA/**/*{scene}_{day}_*.json')) | set(dataset_dir_path.glob(f'QA/**/*{scene}_{day}.json'))
    qa_file_paths = set(p for p in qa_file_paths if scene in p.name)
    qa_file_paths = [str(qa_file_path.relative_to(dataset_dir_path)).replace('\\', '/') for qa_file_path in qa_file_paths]
    qa_file_paths = sorted(qa_file_paths)

    txt_file = output_dir_path / f'{scene}_{day}.txt'
    with txt_file.open(mode='w') as f:
        for qa_file_path in qa_file_paths:
            f.write(qa_file_path + '\n')
    

def make_caption_qa_path_list(dataset_dir_path, output_dir_path, scene):
    qa_file_paths = [p for p in dataset_dir_path.glob(f'QA/MultiChoice/Caption/*{scene}*.json')]
    qa_file_paths = [str(qa_file_path.parent.relative_to(dataset_dir_path)).replace('\\', '/') + '/' + qa_file_path.name for qa_file_path in qa_file_paths]
    qa_file_paths = sorted(qa_file_paths)

    txt_file = output_dir_path / f'{scene}_caption.txt'
    with txt_file.open(mode='w') as f:
        for qa_file_path in qa_file_paths:
            f.write(qa_file_path + '\n')


def main():
    dataset_dir_path = Path.cwd() / 'DataSet'
    output_dir_path = Path.cwd() / 'qa_path'
    output_dir_path.mkdir(exist_ok=True, parents=True)
    
    for scene in [f'scene{i}' for i in range(1, 8)]:
        for day in [f'Day{i}' for i in range(1, 11)]:
            make_qa_path_list(dataset_dir_path, output_dir_path, scene, day)
        
        make_caption_qa_path_list(dataset_dir_path, output_dir_path, scene)


if __name__ == '__main__':
    main()