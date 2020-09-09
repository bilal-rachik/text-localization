"""
Title: split_train_test
Main Author: Michael Xiu
Time: 2019/3/31
Purpose: Split the dataset in ICDAR
Environment: python3.5.6 pytorch1.0.1 cuda9.0
"""
import random
from pathlib import Path

image_path = Path(__file__).parent.parent.joinpath('data/data')
train_path = image_path / "../train.txt"
test_path = image_path / "../test.txt"

ration_split = 0.8

list_image = list(image_path.glob('*.jpg'))

# train and test split
keys_train = random.sample(list_image, int(len(list_image) * ration_split))
keys_test = [k for k in list_image if k not in keys_train]
random.shuffle(keys_train), random.shuffle(keys_test)
print('{} images in the train folder and {} images in the test folder'.format(len(keys_train), len(keys_test)))
count = 0

if __name__ == "__main__":
    with train_path.open("w") as file:
        for id, key in enumerate(keys_train):
            label0 = key.parent.joinpath(key.stem+".txt")
            if (image_path/label0).exists():
                    file.write(key.stem + "\n")

    with test_path.open("w") as file:
        for id, key in enumerate(keys_test):
            label0 = key.parent.joinpath(key.stem + ".txt")
            if (image_path/label0).exists():
                file.write(key.stem + "\n")




