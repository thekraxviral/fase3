import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing import image_dataset_from_directory

# Ruta de las carpetas de las imágenes
train_dir = 'C:\\Users\\user\\Desktop\\Busqueda-App\\carpeta01'
validation_dir = 'C:\\Users\\user\\Desktop\\Busqueda-App\\carpeta00'

# Parámetros de preprocesamiento
batch_size = 32
img_height = 180
img_width = 180
epochs = 10

# Cargar las imágenes de entrenamiento y validación
train_ds = image_dataset_from_directory(
    train_dir,
    validation_split=0.2, # Esta línea se puede eliminar si no tienes una carpeta de validación separada
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    #color_mode='rgb', # Opcional, si las imágenes son en escala de grises descomenta esta línea
)
# validation_ds = image_dataset_from_directory(
#     validation_dir,
#     validation_split=0.2,
#     subset="validation",
#     seed=123,
#     image_size=(img_height, img_width),
#     batch_size=batch_size,
#     #color_mode='rgb', # Opcional, si las imágenes son en escala de grises descomenta esta línea
# )

# Configuración del modelo
num_classes = 2

model = keras.Sequential([
    layers.experimental.preprocessing.Rescaling(1./255),
    layers.Conv2D(16, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

# Compilar el modelo
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Entrenar el modelo
model.fit(train_ds, epochs=epochs)
