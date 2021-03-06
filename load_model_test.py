#!/usr/bin/env python
# coding: utf-8

# In[1]:

def model():
    import GUI
    import os
    import numpy as np
    import pandas as pd
    import cv2
    from io import BytesIO
    from PIL import Image
    import requests
    from keras_preprocessing import image
    from sklearn.model_selection import train_test_split
    from tqdm.notebook import tqdm
    from tensorflow.keras.callbacks import ModelCheckpoint
    from tensorflow.keras import optimizers
    from tensorflow.keras.layers import Dropout, Flatten, Dense
    from tensorflow.keras.models import Sequential, Model, load_model
    from tensorflow.keras import applications
    import matplotlib.pyplot as plt
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from keras.models import load_model
    import tensorflow as tf
    import keras
    import io
    import sys
    # sys.path.append('D:/CODE/python/project/GUI.py')
    model = load_model('D:/keras_envirment/resnet50cls32ac9478.h5')
    ####
    # In[2]:

    # model.summary()

    # In[3]:

    # In[4]:

    translate = {"cane": "Dog", "cavallo": "Horse", "elefante": "Elephant", "farfalla": "Butterfly", "gallina": "Chicken",
                 "gatto": "Cat", "mucca": "Cow", "pecora": "Sheep", "scoiattolo": "Squirrel", "ragno": "Spider", "buffalo": "buffalo",
                 "rhino": "rhino", "zebra": "zebra", "Crab": "Crab", "Deer": "Deer", "Eagle": "Eagle", "Fox": "Fox", "Frog": "Frog", "Giraffe": "Giraffe",
                 "Jellyfish": "Jellyfish", "Lion": "Lion", "Lizard": "Lizard", "Monkey": "Monkey", "Owl": "Owl", "Parrot": "Parrot", "Penguin": "Penguin",
                 "Pig": "Pig", "Polar bear": "Polar bear", "Rabbit": "Rabbit", "Sea lion": "Sea lion", "Sea turtle": "Sea turtle", "Shark": "Shark", "Tiger": "Tiger", "Whale": "Whale"}

    # In[6]:

    from keras.preprocessing import image
    foldernames = os.listdir("D:/CODE/python/project/raw-img/")

    data_x, data_y = [], []
    x_train, y_train, x_test, y_test = [], [], [], []

    for i, folder in enumerate(foldernames):
        filenames = os.listdir("D:/CODE/python/project/raw-img/" + folder)
        for file in filenames:

            data_x.append("D:/CODE/python/project/raw-img/" +
                          folder + "/" + file)
            data_y.append(translate[folder])

    x_train, y_train, x_test, y_test = train_test_split(
        data_x, data_y, test_size=0.3, random_state=0)
    df_x = pd.DataFrame({'Filepath': x_train, 'Target': x_test})
    df_y = pd.DataFrame({'Filepath': y_train, 'Target': y_test})
    train, test = train_test_split(df_x, test_size=0.27, random_state=0)

    # In[7]:

    datagen = ImageDataGenerator(rescale=1./255,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True,
                                 rotation_range=30,
                                 width_shift_range=0.1,
                                 height_shift_range=0.1,
                                 samplewise_center=True,
                                 )
    datagen_test = ImageDataGenerator(rescale=1./255, samplewise_center=True)

    # In[8]:

    train_flow = datagen.flow_from_dataframe(train,
                                             x_col='Filepath',
                                             y_col='Target',
                                             target_size=(224, 224),
                                             interpolation='lanczos',
                                             shuffle=False,  # ??????confusion_matrix???,??????shuffle??????
                                             validate_filenames=False)
    test_flow = datagen_test.flow_from_dataframe(test,
                                                 x_col='Filepath',
                                                 y_col='Target',
                                                 target_size=(224, 224),
                                                 interpolation='lanczos',
                                                 shuffle=False,  # ??????confusion_matrix???,??????shuffle??????
                                                 validate_filenames=False)

    # In[21]:

    f = open('D:/CODE/python/project/path.txt', 'r')
    get_path = f.read()

    images = []
    temp = np.array(image.load_img(get_path,
                                   color_mode="rgb",
                                   target_size=(224, 224),
                                   interpolation="lanczos")) / 255.0
    images.append(temp)
    images = np.array(images)

    # In[29]:

    predictions = model.predict(images)
    # print(predictions)
    pred_ints = predictions.argmax(axis=1)
    out = []
    # print(pred_ints)
    for x in pred_ints:
        labels = train_flow.class_indices
        # print(x)
        # print(labels)
        for label, val in labels.items():
            #print(label, val)
            if val == x:
                out.append(label)

    # In[36]:

    def show():
        sol = out[0]  # 'prediction: ' +
        f = open('D:/CODE/python/project/log.txt', 'w+')
        f.write(sol)
        print(sol)

    show()


def confusion_matrix():
    from sklearn.metrics import classification_report, confusion_matrix
    from sklearn.metrics import plot_confusion_matrix
    import seaborn as sns

    num_of_train_samples = 18692  # 9800
    num_of_test_samples = 6914  # 4200
    batch_size = 32  # flow_from_dataframe??????batch_size???32  ??????:https://gist.github.com/RyanAkilos/3808c17f79e77c4117de35aa68447045

    Y_pred = model.predict_generator(
        test_flow, num_of_test_samples // batch_size+1)
    y_pred = np.argmax(Y_pred, axis=1)
    print('Confusion Matrix')
    #print(confusion_matrix(test_flow.classes, y_pred))
    cnf_matrix = confusion_matrix(test_flow.classes, y_pred)
    #print('Classification Report')
    target_names = ["Dog", "Horse", "Elephant", "Butterfly", "Chicken", "Cat", "Cow", "Sheep", "Squirrel", "Spider", "buffalo", "rhino", "zebra", "Deer", "Eagle", "Fox",
                    "Frog", "Giraffe", "Jellyfish", "Lion", "Lizard", "Monkey", "Owl", "Parrot", "Penguin", "Polar bear", "Rabbit", "Sea lion", "Sea turtle", "Shark", "Tiger", "Whale"]
    print(classification_report(test_flow.classes,
                                y_pred, target_names=target_names))

    plt.figure()
    #plot_confusion_matrix(cnf_matrix, labels=target_names,normalize=True)
    #plot_confusion_matrix(X = test_flow.classes, y_true = y_pred,labels= target_names, normalize=False)
    # ??????:https://stackoverflow.com/questions/60776749/plot-confusion-matrix-without-estimator
    f = sns.heatmap(cnf_matrix, annot=True)


model()


'''plt.title(sol)
plt.axis('off')
plt.imshow(images[0])'''


# In[77]:


# In[20]:


"""
print(out[0])
plt.imshow(images[0])    """


# In[ ]:
