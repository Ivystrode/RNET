import numpy as np
import tensorflow as tf
from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

class DetectionModelBuilder():
    """
    Builds a new NN to detect custom objects. Use auto-downloader to download image data.
    Scalability in question...
    """

    def __init__(self):
        self.training_set = None
        self.test_set = None
        self.subject = None
        self.cnn = None

    def get_data(self, subject):
        self.subject = subject
        
        train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)
        self.training_set = train_datagen.flow_from_directory(f'datasets/{subject}', target_size = (64, 64), batch_size = 32, class_mode = 'binary')

        test_datagen = ImageDataGenerator(rescale = 1./255)
        self.test_set = test_datagen.flow_from_directory(f'datasets/{subject}', target_size = (64, 64), batch_size = 32, class_mode = 'binary')
        
        print("Training and test sets created")
        self.create_model(self.subject)
        
    def create_model(self, subject):
        self.cnn = tf.keras.models.Sequential()

        self.cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=[64, 64, 3]))
        self.cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
        self.cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
        self.cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
        self.cnn.add(tf.keras.layers.Flatten())
        self.cnn.add(tf.keras.layers.Dense(units=128, activation='relu'))
        self.cnn.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

        self.cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
        self.cnn.fit(x = self.training_set, validation_data = self.test_set, epochs = 30)
        
        print("Model trained")
        save = input("Save model? y/n\n")
        if save.lower() == "y":
            self.cnn.save(f"{self.subject}_detmod.hd5")

    def predict(self, pic): # model
        # model = load_model(f"{model}_detmod.hd5")
        
        pic = image.load_img(f'{pic}', target_size = (64, 64))
        pic = image.img_to_array(pic)
        pic = np.expand_dims(pic, axis = 0)
        
        # for testing:
        result = self.cnn.predict(pic)
        
        # result = model.predict(pic)
        
        if result[0][0] == 1:
            prediction = f'{self.subject} detected!!'
        else:
            prediction = f'not detected'
        print(prediction)
        
        
# ==== TEST =====
if __name__ == '__main__':
    new_model = DetectionModelBuilder()
    new_model.get_data("quadcopter")
    
    # testing...
    new_model.predict("quad.jpg")
    new_model.predict("blackpaint.jpg")
    
    new_model.predict("bebop.jpg")
    new_model.predict("fruit.jpg")
    
    new_model.predict("racingdrone.jpg")
    new_model.predict("shopfront.jpg")
    # seems to work alright, more data would be good though (smash autodownloader sometime)