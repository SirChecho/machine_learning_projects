import matplotlib.pyplot as plt
import numpy as np

#for splitdata
import os
import glob
from sklearn.model_selection import train_test_split
import shutil
import csv

from tensorflow.keras.preprocessing.image import ImageDataGenerator

def split_data(path_data, train_folder, val_folder, split_size=0.15):

    folders = os.listdir(path_data) #gives a list of all the folders in the directory

    for folder in folders:
        full_path = os.path.join(path_data,folder)
        images_paths = glob.glob(os.path.join(full_path, '*.png'))

        x_train, x_val = train_test_split(images_paths, test_size=split_size)

        for x in x_train:

            path_to_folder = os.path.join(train_folder, folder)
            if not os.path.isdir(path_to_folder):
                os.makedirs(path_to_folder)

            shutil.copy(x, path_to_folder)

        for x in x_val:

            path_to_folder = os.path.join(val_folder, folder)
            if not os.path.isdir(path_to_folder):
                os.makedirs(path_to_folder)

            shutil.copy(x, path_to_folder)


def display_examples(examples, labels):

    plt.figure(figsize=(8,8))
    for i in range(25):
        idx = np.random.randint(0,examples.shape[0]-1)
        img = examples[idx]
        label = labels[idx]
        plt.subplot(5,5,i+1)
        plt.title(str(label))
        plt.tight_layout()
        plt.imshow(img, cmap='gray')

    plt.show()

def order_test_set(files_path, csv_path):

    try:
        with open(csv_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter= ',')
            for i,row in enumerate(reader):
                if i==0:
                    continue
                img_name = row[-1].replace('Test/', '')
                label = row[-2]

                path_to_folder = os.path.join(files_path, label)

                if not os.path.isdir(path_to_folder):
                    os.makedirs(path_to_folder)

                image_full_path = os.path.join(files_path,img_name)

                shutil.move(image_full_path, path_to_folder)

    except:
        print('[INFO] : Error reading csv file')

def create_generators(batch_size, train_data_path, val_data_path, test_data_path):

    preprocessor = ImageDataGenerator(
        rescale = 1 / 255
    )

    train_generator = preprocessor.flow_from_directory(
        train_data_path,
        class_mode = 'categorical',
        target_size = (60,60),
        color_mode = 'rgb',
        shuffle = True,
        batch_size = batch_size
    )

    val_generator = preprocessor.flow_from_directory(
        val_data_path,
        class_mode = 'categorical',
        target_size = (60,60),
        color_mode = 'rgb',
        shuffle = False,
        batch_size = batch_size
    )

    test_generator = preprocessor.flow_from_directory(
        test_data_path,
        class_mode = 'categorical',
        target_size = (60,60),
        color_mode = 'rgb',
        shuffle = False,
        batch_size = batch_size
    )

    return train_generator, val_generator, test_generator