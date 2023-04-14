import os
import time
from AENE import stats
from AENE import main

def SBMnet_test(root_path, category_list):
    # Performs foreground mask and background generation for the categories
    # listed in category_list, assuming the SBMnet dataset is available in
    # the directory root_path

    parser = main.create_parser()
    args = parser.parse_args()

    start_time = time.time()

    rootpaths = {}
    rootpaths['dataset'] = root_path
    rootpaths['masks'] = os.path.join(root_path, 'results')
    rootpaths['backgrounds'] = os.path.join(root_path, 'backgrounds')
    rootpaths['models'] = os.path.join(root_path, 'models')

    for (_, path) in rootpaths.items():
        if not os.path.exists(path):
            os.mkdir(path)

    messages = []

    for category in category_list:
        category_paths = {k: os.path.join(path, category) for (k, path) in rootpaths.items()}

        for (_, path) in category_paths.items():
            if not os.path.exists(path):
                os.mkdir(path)

        video_names = [video_name for video_name in os.listdir(category_paths['dataset'])
                       if os.path.isdir(os.path.join(category_paths['dataset'], video_name))]

        for video_name in video_names:
            video_paths = {k: os.path.join(path, video_name) for (k, path) in category_paths.items()}
            video_paths['test_dataset'] = video_paths['dataset']
            video_paths['train_dataset'] = video_paths['dataset']
            video_paths['GT'] = video_paths['dataset']

            video_start_time = time.time()

            for (_, path) in video_paths.items():
                if not os.path.exists(path):
                    os.mkdir(path)

            print(f'processing {video_name}')
            main.compute_dynamic_backgrounds_and_masks(args, video_paths)

            video_end_time = time.time()
            print(f"video folder {video_paths['dataset']} processing finished, computation time {video_end_time - video_start_time}")

        message = f'end of category {category}' + 400 * ' '
        print(message)

    end_time = time.time()
    print(f'computation time : {end_time - start_time}')
    print(messages)

    print(f"foreground masks are stored in the directory {rootpaths['masks']}\n"
          f" reconstructed backgrounds are stored in the directory {rootpaths['backgrounds']}")


if __name__ == '__main__':
    root_path = '/content/gdrive/MyDrive/SBMnet_dataset/'

    category_list = ['backgroundMotion', 'basic', 'clutter', 'illuminationChanges',
                     'intermittentMotion', 'jitter', 'veryLong', 'veryShort']
    SBMnet_test(root_path, category_list)
