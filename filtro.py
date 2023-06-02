import os
from tensorflow import keras
from keras import layers
import os
from tensorflow import keras
import os
from tensorflow import keras

import os
from PIL import Image
import numpy as np
from tensorflow import keras

# Define los parámetros y rutas de los directorios
batch_size = 16
image_height = 224
image_width = 224
train_data_dir = "carpeta01"
validation_data_dir = "carpeta00"

# Lee las imágenes de entrenamiento
train_images = []
train_labels = []
for filename in os.listdir(train_data_dir):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image = Image.open(os.path.join(train_data_dir, filename))
        image = image.resize((image_width, image_height))
        image = np.array(image) / 255.0
        train_images.append(image)
        train_labels.append(1)  # Etiqueta para imágenes buenas

# Lee las imágenes de validación
validation_images = []
validation_labels = []
for filename in os.listdir(validation_data_dir):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image = Image.open(os.path.join(validation_data_dir, filename))
        image = image.resize((image_width, image_height))
        image = np.array(image) / 255.0
        validation_images.append(image)
        validation_labels.append(0)  # Etiqueta para imágenes malas

# Convierte las listas de imágenes y etiquetas a arrays numpy
train_images = np.array(train_images)
train_labels = np.array(train_labels)
validation_images = np.array(validation_images)
validation_labels = np.array(validation_labels)

# Crea el generador de datos de entrenamiento y validación
train_datagen = keras.preprocessing.image.ImageDataGenerator()
train_ds = train_datagen.flow(train_images, train_labels, batch_size=batch_size)
validation_datagen = keras.preprocessing.image.ImageDataGenerator()
validation_ds = validation_datagen.flow(validation_images, validation_labels, batch_size=batch_size)

# Crea el modelo de la red neuronal convolucional (CNN)
model = keras.Sequential([
    layers.Rescaling(1./255, input_shape=(image_height, image_width, 3)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compila el modelo
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Entrena el modelo
epochs = 10
model.fit(train_ds, validation_data=validation_ds, epochs=epochs)

# Guarda los pesos y la arquitectura del modelo en un archivo
model.save('modelo.h5')
