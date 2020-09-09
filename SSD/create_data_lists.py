from __future__ import absolute_import
from pathlib import Path
import json


label_map = {'background': 0, 'text': 1}


def parse_annotation(annotation_path):
    boxes = list()
    labels = list()

    f_txt = open(annotation_path)

    # In ICDAR case, the first line is our ROI coordinate (xmin, ymin)
    line_txt = f_txt.readline()
    coor = line_txt.split(',')
    ROI_x = int(coor[0].strip('\''))
    ROI_y = int(coor[1].strip('\''))

    line_txt = f_txt.readline()

    while line_txt:
        coor = line_txt.split(',')
        #print(coor[0])
        #print(annotation_path)
        if coor[0] !='"\r\n':
            xmin = int(coor[0].strip('\'')) - ROI_x
            ymin = int(coor[1].strip('\'')) - ROI_y
            xmax = int(coor[4].strip('\'')) - ROI_x
            ymax = int(coor[5].strip('\'')) - ROI_y
            # text = coor[8].strip('\n').strip('\'')
            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(label_map['text'])

        line_txt = f_txt.readline()

    return {'boxes': boxes, 'labels': labels}


def create_data_lists(ICDAR_path, output_folder):
    """
    Create lists of images, the bounding boxes and labels of the objects in these images, and save these to file.
    :param ICDAR_path: path to the 'ICDAR' task1 folder
    :param output_folder: folder where the JSONs must be saved
    """
    train_images = list()
    train_objects = list()
    n_objects = 0
    train_path = ICDAR_path/'train.txt'
    test_path = ICDAR_path/'test.txt'

    # Training data
    with  train_path.open() as f:
        ids = f.read().splitlines()
    for id in ids:
        # Parse annotation's txt file
        p = train_path.parent.joinpath('data')/(id+'.txt')
        objects = parse_annotation(p.as_posix())
        if len(objects) == 0:
            continue
        n_objects += len(objects)
        train_objects.append(objects)
        p = train_path.parent.joinpath('data') / (id + '.jpg')
        train_images.append(p.as_posix())

    assert len(train_objects) == len(train_images)

    # Save to file
    TRAIN_images = output_folder / 'TRAIN_images.json'
    TRAIN_objects = output_folder /'TRAIN_objects.json'
    LABEL_MAP = output_folder/ 'label_map.json'

    with TRAIN_images.open('w') as j:
        json.dump(train_images, j)   # store image path
    with TRAIN_objects.open('w') as j:
        json.dump(train_objects, j)  # store objects path
    with LABEL_MAP.open('w') as j:
        json.dump(label_map, j)  # save label map too

    print('\nThere are %d training images containing a total of %d objects. Files have been saved to %s.' % (
        len(train_images), n_objects, output_folder.as_posix()))

    # Testing data
    test_images = list()
    test_objects = list()
    n_objects = 0

    # Find IDs of images in testing data
    with test_path.open() as f:
        ids = f.read().splitlines()

    for id in ids:
        # Parse annotation's txt file
        p = train_path.parent.joinpath('data') / (id + '.txt')
        objects = parse_annotation(p.as_posix())
        if len(objects) == 0:
            continue
        n_objects += len(objects)
        test_objects.append(objects)
        p = train_path.parent.joinpath('data') / (id + '.jpg')
        test_images.append(p.as_posix())

    assert len(test_objects) == len(test_images)

    # Save to file
    TEST_images = output_folder / 'TEST_images.json'
    TEST_objects = output_folder / 'TEST_objects.json'

    with TEST_images.open('w') as j:
        json.dump(test_images, j)
    with TEST_objects.open('w') as j:
        json.dump(test_objects, j)

    print('\nThere are %d validation images containing a total of %d objects. Files have been saved to %s.' % (
        len(test_images), n_objects, output_folder.as_posix() ))

if __name__ == '__main__':
    create_data_lists(
        ICDAR_path= Path(__file__).parent.parent.joinpath('data') ,
        output_folder= Path(__file__).parent.parent.joinpath('data'))