# -*- coding: utf-8 -*-
"""Brain_Tumour_Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HC1K1r9X9M0ZA0u78ZamSjMIlh8UmSun

# <center>Brain Tumor Detection</center>

## Overview:
A brain tumor is an abnormal growth of cells in the brain, which can be either non-cancerous or cancerous. These tumors may originate within the brain or spread from other parts of the body. They can disrupt normal brain functions, leading to symptoms such as headaches, seizures, cognitive impairments, and motor deficits. Treatment options include surgery, radiation therapy, chemotherapy, or a combination, depending on the tumor type, location, and stage. Therefore Early detection is crucial for effective management.

Types of Brain Tumors We've taken for Detection:
* Pituatory Tumor
* Glioma Tumor
* Meningioma Tumor

## Dataset Information:

Brain MRI Dataset: [Kaggle - Brain Tumor Detection](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)

This dataset of size 164MB contains 7023 images of human brain MRI images which are classified into 4 classes: glioma, meningioma, no tumor and, pituitary.

### Training Data:

   * Glioma Tumor: 1321 Images
   * Meningioma Tumor: 1339 Images
   * No Tumor: 1595 Images
   * Pituitary Tumor: 1457 Images
   
### Testing Data:

   * Glioma Tumor: 300 Images
   * Meningioma Tumor: 306 Images
   * No Tumor: 405 Images
   * Pituitary Tumor: 300 Images

# 1. Importing required libraries
* ```Numpy```: A fundamental package for scientific computing in Python. It provides support for multidimensional arrays, along with a collection of mathematical functions to operate on these arrays efficiently. NumPy is widely used in numerical and scientific computing tasks, including data manipulation, linear algebra, statistics, and signal processing.

* ```Pandas```: A powerful library for data manipulation and analysis in Python. It offers data structures and functions for working with structured data, primarily in the form of dataframes. Dataframes are two-dimensional labeled arrays capable of holding heterogeneous data types. Pandas provides tools for reading and writing data from various file formats, reshaping and transforming data, and performing data analysis tasks such as grouping, filtering, and aggregation.

* ```PIL (Python Imaging Library)```: Also known as the Pillow library, it is a Python imaging library that adds support for opening, manipulating, and saving many different image file formats. PIL/Pillow provides functions for basic image processing tasks such as resizing, cropping, rotating, and filtering images.

* ```Matplotlib```: A plotting library for creating visualizations in Python. It provides a MATLAB-like interface for generating a wide range of static, interactive, and animated plots. Matplotlib is highly customizable and supports various plot types, including line plots, scatter plots, bar charts, histograms, and heatmaps.

* ```Seaborn```: Built on top of Matplotlib, Seaborn is a statistical data visualization library that provides an easy-to-use interface for creating informative and visually appealing plots. Seaborn simplifies the process of creating complex statistical visualizations by providing high-level functions for common statistical plots such as scatter plots, box plots, violin plots, and pair plots.

* ```Sklearn```: Scikit-learn is a machine learning library for Python that provides simple and efficient tools for data mining and data analysis. It features various supervised and unsupervised learning algorithms, including classification, regression, clustering, dimensionality reduction, and model evaluation.

* ```TensorFlow```: TensorFlow is an open-source machine learning framework developed by Google. It provides a comprehensive ecosystem of tools, libraries, and resources for building and deploying machine learning models at scale.
"""

import warnings
warnings.filterwarnings("ignore")

import os
import numpy as np
import pandas as pd
from PIL import Image
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, f1_score, recall_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.optimizers import Adamax
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16, EfficientNetB0, Xception, ResNet50, InceptionV3

"""# 2. Preprocessing

## 2.1 Load Data
* Defines functions to create dataframes for training and testing images.
* These functions parse the directory structure to create dataframes containing image paths and corresponding labels.

## 2.2 Split Data
* Splits the testing data into validation and testing subsets using train_test_split function.

## 2.3 Data Preprocessing
* Defines parameters for image data generators.
"""

def train_df(tr_path):
    classes, class_paths = zip(*[(label, os.path.join(tr_path, label, image))
                                 for label in os.listdir(tr_path) if os.path.isdir(os.path.join(tr_path, label))
                                 for image in os.listdir(os.path.join(tr_path, label))])

    tr_df = pd.DataFrame({'Class Path': class_paths, 'Class': classes})
    return tr_df

def test_df(ts_path):
    classes, class_paths = zip(*[(label, os.path.join(ts_path, label, image))
                                 for label in os.listdir(ts_path) if os.path.isdir(os.path.join(ts_path, label))
                                 for image in os.listdir(os.path.join(ts_path, label))])

    ts_df = pd.DataFrame({'Class Path': class_paths, 'Class': classes})
    return ts_df

import kagglehub

# Download latest version
path = kagglehub.dataset_download("masoudnickparvar/brain-tumor-mri-dataset")

print("Path to dataset files:", path)



tr_df = train_df('/root/.cache/kagglehub/datasets/masoudnickparvar/brain-tumor-mri-dataset/versions/1/Training')

tr_df["Class Path"][0]

ts_df = test_df('/root/.cache/kagglehub/datasets/masoudnickparvar/brain-tumor-mri-dataset/versions/1/Testing')

ts_df

plt.figure(figsize=(15,7))
ax = sns.countplot(data=tr_df , y=tr_df['Class'])

plt.xlabel('')
plt.ylabel('')
plt.title('Count of images in each class', fontsize=20)
ax.bar_label(ax.containers[0])
plt.show()

plt.figure(figsize=(15, 7))
ax = sns.countplot(y=ts_df['Class'], palette='viridis')

ax.set(xlabel='', ylabel='', title='Count of images in each class')
ax.bar_label(ax.containers[0])

plt.show()

valid_df, ts_df = train_test_split(ts_df, train_size=0.5, random_state=20, stratify=ts_df['Class'])

valid_df

batch_size = 32
img_size = (299, 299)

_gen = ImageDataGenerator(rescale=1/255,brightness_range=(0.8, 1.2))

ts_gen = ImageDataGenerator(rescale=1/255)


tr_gen = _gen.flow_from_dataframe(tr_df, x_col='Class Path',
                                  y_col='Class', batch_size=batch_size,
                                  target_size=img_size)

valid_gen = _gen.flow_from_dataframe(valid_df, x_col='Class Path',
                                     y_col='Class', batch_size=batch_size,
                                     target_size=img_size)

ts_gen = ts_gen.flow_from_dataframe(ts_df, x_col='Class Path',
                                  y_col='Class', batch_size=16,
                                  target_size=img_size, shuffle=False)

class_dict = tr_gen.class_indices
classes = list(class_dict.keys())
images, labels = next(ts_gen)

plt.figure(figsize=(20, 20))

for i, (image, label) in enumerate(zip(images, labels)):
    plt.subplot(4,4, i + 1)
    plt.imshow(image)
    class_name = classes[np.argmax(label)]
    plt.title(class_name, color='k', fontsize=15)

plt.show()

"""# 3. Building Deep Learning Model

## 3.1 XCeption Model Training and Evaluation
"""

from tensorflow.keras.metrics import Precision, Recall

img_shape=(299,299,3)
xception = Xception(include_top= False, weights= "imagenet",input_shape= img_shape, pooling= 'max')

xception_model = Sequential([xception,
                    Flatten(),
                    Dropout(rate= 0.3),
                    Dense(128, activation= 'relu'),
                    Dropout(rate= 0.25),
                    Dense(4, activation= 'softmax')
                   ])

xception_model.compile(Adamax(learning_rate= 0.001),loss= 'categorical_crossentropy',metrics= ['accuracy',Precision(),Recall()])
xception_model.summary()



tf.keras.utils.plot_model(xception_model, show_shapes=True)

xception_hist = xception_model.fit(tr_gen,epochs=10,validation_data=valid_gen,shuffle= False)

tr_acc = xception_hist.history['accuracy']
tr_loss = xception_hist.history['loss']
val_acc = xception_hist.history['val_accuracy']
val_loss = xception_hist.history['val_loss']

index_loss = np.argmin(val_loss)
val_lowest = val_loss[index_loss]
index_acc = np.argmax(val_acc)
acc_highest = val_acc[index_acc]


Epochs = [i + 1 for i in range(len(tr_acc))]
loss_label = f'Best epoch = {str(index_loss + 1)}'
acc_label = f'Best epoch = {str(index_acc + 1)}'


plt.figure(figsize=(20, 12))
plt.style.use('fivethirtyeight')


plt.subplot(2, 2, 1)
plt.plot(Epochs, tr_loss, 'r', label='Training loss')
plt.plot(Epochs, val_loss, 'g', label='Validation loss')
plt.scatter(index_loss + 1, val_lowest, s=150, c='blue', label=loss_label)
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(Epochs, tr_acc, 'r', label='Training Accuracy')
plt.plot(Epochs, val_acc, 'g', label='Validation Accuracy')
plt.scatter(index_acc + 1, acc_highest, s=150, c='blue', label=acc_label)
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.suptitle('Model Training Metrics Over Epochs', fontsize=16)
plt.show()

train_score = xception_model.evaluate(tr_gen, verbose=1)
valid_score = xception_model.evaluate(valid_gen, verbose=1)
test_score = xception_model.evaluate(ts_gen, verbose=1)

print(f"Train Loss: {train_score[0]:.4f}")
print(f"Train Accuracy: {train_score[1]*100:.2f}%")
print('-' * 20)
print(f"Validation Loss: {valid_score[0]:.4f}")
print(f"Validation Accuracy: {valid_score[1]*100:.2f}%")
print('-' * 20)
print(f"Test Loss: {test_score[0]:.4f}")
print(f"Test Accuracy: {test_score[1]*100:.2f}%")

y_pred_xception = np.argmax(xception_model.predict(ts_gen), axis=1)

# Calculate metrics
acc_xception = accuracy_score(ts_gen.classes, y_pred_xception)
prec_xception = precision_score(ts_gen.classes, y_pred_xception, average='weighted')
recall_xception = recall_score(ts_gen.classes, y_pred_xception, average='weighted')
f1_xception = f1_score(ts_gen.classes, y_pred_xception, average='weighted')

# Print metrics
print("Xception Model Metrics:")
print(f"Accuracy: {acc_xception}")
print(f"Precision: {prec_xception}")
print(f"Recall: {recall_xception}")
print(f"F1 Score: {f1_xception}")

xception_results = pd.DataFrame({
    'Model': ['Xception'],
    'Accuracy': [acc_xception],
    'Precision': [prec_xception],
    'Recall': [recall_xception],
    'F1 Score': [f1_xception]
})
xception_results

"""## 3.2 Resnet-50 Model Training and Evaluation"""

resnet = ResNet50(weights='imagenet', include_top=False, input_shape=img_shape)

resnet_model = Sequential([
    resnet,
    Flatten(),
    Dropout(rate=0.3),
    Dense(128, activation='relu'),
    Dropout(rate=0.25),
    Dense(4, activation='softmax')
])

resnet_model.compile(optimizer=Adamax(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy', Precision(), Recall()])
resnet_model.summary()

tf.keras.utils.plot_model(resnet_model, show_shapes=True)

resnet_hist = resnet_model.fit(tr_gen,epochs=10,validation_data=valid_gen,shuffle= False)

tr_acc = resnet_hist.history['accuracy']
tr_loss = resnet_hist.history['loss']

val_acc = resnet_hist.history['val_accuracy']
val_loss = resnet_hist.history['val_loss']


index_loss = np.argmin(val_loss)
val_lowest = val_loss[index_loss]
index_acc = np.argmax(val_acc)
acc_highest = val_acc[index_acc]


Epochs = [i + 1 for i in range(len(tr_acc))]
loss_label = f'Best epoch = {str(index_loss + 1)}'
acc_label = f'Best epoch = {str(index_acc + 1)}'



plt.figure(figsize=(20, 12))
plt.style.use('fivethirtyeight')


plt.subplot(2, 2, 1)
plt.plot(Epochs, tr_loss, 'r', label='Training loss')
plt.plot(Epochs, val_loss, 'g', label='Validation loss')
plt.scatter(index_loss + 1, val_lowest, s=150, c='blue', label=loss_label)
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(Epochs, tr_acc, 'r', label='Training Accuracy')
plt.plot(Epochs, val_acc, 'g', label='Validation Accuracy')
plt.scatter(index_acc + 1, acc_highest, s=150, c='blue', label=acc_label)
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.suptitle('Model Training Metrics Over Epochs', fontsize=16)
plt.show()

train_score = resnet_model.evaluate(tr_gen, verbose=1)
valid_score = resnet_model.evaluate(valid_gen, verbose=1)
test_score  = resnet_model.evaluate(ts_gen, verbose=1)

print(f"Train Loss: {train_score[0]:.4f}")
print(f"Train Accuracy: {train_score[1]*100:.2f}%")
print('-' * 20)
print(f"Validation Loss: {valid_score[0]:.4f}")
print(f"Validation Accuracy: {valid_score[1]*100:.2f}%")
print('-' * 20)
print(f"Test Loss: {test_score[0]:.4f}")
print(f"Test Accuracy: {test_score[1]*100:.2f}%")

y_pred_resnet = np.argmax(resnet_model.predict(ts_gen), axis=1)

# Calculate metrics
acc_resnet = accuracy_score(ts_gen.classes, y_pred_resnet)
prec_resnet = precision_score(ts_gen.classes, y_pred_resnet, average='weighted')
recall_resnet = recall_score(ts_gen.classes, y_pred_resnet, average='weighted')
f1_resnet = f1_score(ts_gen.classes, y_pred_resnet, average='weighted')

# Print metrics
print("ResNet-50 Model Metrics:")
print(f"Accuracy: {acc_resnet}")
print(f"Precision: {prec_resnet}")
print(f"Recall: {recall_resnet}")
print(f"F1 Score: {f1_resnet}")

resnet_results = pd.DataFrame({
    'Model': ['ResNet-50'],
    'Accuracy': [acc_resnet],
    'Precision': [prec_resnet],
    'Recall': [recall_resnet],
    'F1 Score': [f1_resnet]
})
resnet_results

"""## 3.3 InceptionV3 Model Training and Evaluation"""

inception = InceptionV3(weights='imagenet', include_top=False, input_shape=img_shape)

inception_model = Sequential([
    inception,
    Flatten(),
    Dropout(rate=0.3),
    Dense(128, activation='relu'),
    Dropout(rate=0.25),
    Dense(4, activation='softmax')
])

inception_model.compile(optimizer=Adamax(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy', Precision(), Recall()])
inception_model.summary()

tf.keras.utils.plot_model(inception_model, show_shapes=True)

incepton_hist = inception_model.fit(tr_gen,epochs=10,validation_data=valid_gen,shuffle= False)

tr_acc = incepton_hist.history['accuracy']
tr_loss = incepton_hist.history['loss']

val_acc = incepton_hist.history['val_accuracy']
val_loss = incepton_hist.history['val_loss']


index_loss = np.argmin(val_loss)
val_lowest = val_loss[index_loss]
index_acc = np.argmax(val_acc)
acc_highest = val_acc[index_acc]


Epochs = [i + 1 for i in range(len(tr_acc))]
loss_label = f'Best epoch = {str(index_loss + 1)}'
acc_label = f'Best epoch = {str(index_acc + 1)}'


plt.figure(figsize=(20, 12))
plt.style.use('fivethirtyeight')


plt.subplot(2, 2, 1)
plt.plot(Epochs, tr_loss, 'r', label='Training loss')
plt.plot(Epochs, val_loss, 'g', label='Validation loss')
plt.scatter(index_loss + 1, val_lowest, s=150, c='blue', label=loss_label)
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(Epochs, tr_acc, 'r', label='Training Accuracy')
plt.plot(Epochs, val_acc, 'g', label='Validation Accuracy')
plt.scatter(index_acc + 1, acc_highest, s=150, c='blue', label=acc_label)
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.suptitle('Model Training Metrics Over Epochs', fontsize=16)
plt.show()

train_score = inception_model.evaluate(tr_gen, verbose=1)
valid_score = inception_model.evaluate(valid_gen, verbose=1)
test_score  = inception_model.evaluate(ts_gen, verbose=1)

print(f"Train Loss: {train_score[0]:.4f}")
print(f"Train Accuracy: {train_score[1]*100:.2f}%")
print('-' * 20)
print(f"Validation Loss: {valid_score[0]:.4f}")
print(f"Validation Accuracy: {valid_score[1]*100:.2f}%")
print('-' * 20)
print(f"Test Loss: {test_score[0]:.4f}")
print(f"Test Accuracy: {test_score[1]*100:.2f}%")

y_pred_inception = np.argmax(inception_model.predict(ts_gen), axis=1)

# Calculate metrics
acc_inception = accuracy_score(ts_gen.classes, y_pred_inception)
prec_inception = precision_score(ts_gen.classes, y_pred_inception, average='weighted')
recall_inception = recall_score(ts_gen.classes, y_pred_inception, average='weighted')
f1_inception = f1_score(ts_gen.classes, y_pred_inception, average='weighted')

# Print metrics
print("InceptionV3 Model Metrics:")
print(f"Accuracy: {acc_inception}")
print(f"Precision: {prec_inception}")
print(f"Recall: {recall_inception}")
print(f"F1 Score: {f1_inception}")

inception_results = pd.DataFrame({
    'Model': ['InceptionV3'],
    'Accuracy': [acc_inception],
    'Precision': [prec_inception],
    'Recall': [recall_inception],
    'F1 Score': [f1_inception]
})
inception_results

"""## 3.4 EfficentNet-B0 Model Training and Evaluation"""

efficent = EfficientNetB0(weights='imagenet', include_top=False, input_shape=img_shape)

efficent_model = Sequential([
    efficent,
    Flatten(),
    Dropout(rate=0.3),
    Dense(128, activation='relu'),
    Dropout(rate=0.25),
    Dense(4, activation='softmax')
])

efficent_model.compile(optimizer=Adamax(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy', Precision(), Recall()])
efficent_model.summary()

tf.keras.utils.plot_model(efficent_model, show_shapes=True)

efficent_hist = efficent_model.fit(tr_gen,epochs=10,validation_data=valid_gen,shuffle= False)

tr_acc = efficent_hist.history['accuracy']
tr_loss = efficent_hist.history['loss']
val_acc = efficent_hist.history['val_accuracy']
val_loss = efficent_hist.history['val_loss']


index_loss = np.argmin(val_loss)
val_lowest = val_loss[index_loss]
index_acc = np.argmax(val_acc)
acc_highest = val_acc[index_acc]


Epochs = [i + 1 for i in range(len(tr_acc))]
loss_label = f'Best epoch = {str(index_loss + 1)}'
acc_label = f'Best epoch = {str(index_acc + 1)}'



plt.figure(figsize=(20, 12))
plt.style.use('fivethirtyeight')


plt.subplot(2, 2, 1)
plt.plot(Epochs, tr_loss, 'r', label='Training loss')
plt.plot(Epochs, val_loss, 'g', label='Validation loss')
plt.scatter(index_loss + 1, val_lowest, s=150, c='blue', label=loss_label)
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(Epochs, tr_acc, 'r', label='Training Accuracy')
plt.plot(Epochs, val_acc, 'g', label='Validation Accuracy')
plt.scatter(index_acc + 1, acc_highest, s=150, c='blue', label=acc_label)
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.suptitle('Model Training Metrics Over Epochs', fontsize=16)
plt.show()

train_score = efficent_model.evaluate(tr_gen, verbose=1)
valid_score = efficent_model.evaluate(valid_gen, verbose=1)
test_score = efficent_model.evaluate(ts_gen, verbose=1)

print(f"Train Loss: {train_score[0]:.4f}")
print(f"Train Accuracy: {train_score[1]*100:.2f}%")
print('-' * 20)
print(f"Validation Loss: {valid_score[0]:.4f}")
print(f"Validation Accuracy: {valid_score[1]*100:.2f}%")
print('-' * 20)
print(f"Test Loss: {test_score[0]:.4f}")
print(f"Test Accuracy: {test_score[1]*100:.2f}%")

y_pred_efficent = np.argmax(efficent_model.predict(ts_gen), axis=1)

# Calculate metrics
acc_efficent = accuracy_score(ts_gen.classes, y_pred_efficent)
prec_efficent = precision_score(ts_gen.classes, y_pred_efficent, average='weighted')
recall_efficent = recall_score(ts_gen.classes, y_pred_efficent, average='weighted')
f1_efficent = f1_score(ts_gen.classes, y_pred_efficent, average='weighted')

# Print metrics
print("EfficientNet-B0 Model Metrics:")
print(f"Accuracy: {acc_efficent}")
print(f"Precision: {prec_efficent}")
print(f"Recall: {recall_efficent}")
print(f"F1 Score: {f1_efficent}")

efficent_results = pd.DataFrame({
    'Model': ['EfficientNet-B0'],
    'Accuracy': [acc_efficent],
    'Precision': [prec_efficent],
    'Recall': [recall_efficent],
    'F1 Score': [f1_efficent]
})
efficent_results

Results = pd.concat([xception_results, resnet_results, inception_results, efficent_results], ignore_index=True)
Results

preds = xception_model.predict(ts_gen)
y_pred = np.argmax(preds, axis=1)

cm = confusion_matrix(ts_gen.classes, y_pred)
labels = list(class_dict.keys())
plt.figure(figsize=(10,8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted Label')
plt.ylabel('Truth Label')
plt.show()

clr = classification_report(ts_gen.classes, y_pred)
print(clr)

"""## 5.2 Testing"""

def predict(img_path):
    import numpy as np
    import matplotlib.pyplot as plt
    from PIL import Image
    label = list(class_dict.keys())
    plt.figure(figsize=(12, 12))
    img = Image.open(img_path)
    resized_img = img.resize((299, 299))
    img = np.asarray(resized_img)
    img = np.expand_dims(img, axis=0)
    img = img / 255
    predictions = xception_model.predict(img)
    probs = list(predictions[0])
    labels = label
    plt.subplot(2, 1, 1)
    plt.imshow(resized_img)
    plt.subplot(2, 1, 2)
    bars = plt.barh(labels, probs)
    plt.xlabel('Probability', fontsize=15)
    ax = plt.gca()
    ax.bar_label(bars, fmt = '%.2f')
    plt.show()

predict('/root/.cache/kagglehub/datasets/masoudnickparvar/brain-tumor-mri-dataset/versions/1/Training/meningioma/Tr-meTr_0004.jpg')

# Save the models as .h5 files
xception_model.save('xception_model.keras')
resnet_model.save('resnet_model.keras')
inception_model.save('inception_model.keras')
efficent_model.save('efficent_model.keras')

predict('/root/.cache/kagglehub/datasets/masoudnickparvar/brain-tumor-mri-dataset/versions/1/Training/notumor/Tr-noTr_0004.jpg')

