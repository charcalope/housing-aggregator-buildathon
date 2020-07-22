# make a prediction for a new image.
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model


# load and prepare the image
def load_image(filename):
    # load the image
    img = load_img(filename, target_size=(256, 512))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 3 channels
    img = img.reshape(1, 256, 512, 3)
    return img


# load an image and predict the class
def run_example(filepath):
    # load the image
    img = load_image(filepath)
    # load model
    model = load_model('v3_trained.h5')
    # predict the class
    result = model.predict(img)
    print(result[0])


