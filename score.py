import pickle
import cv2 
import tensorflow as tf
import numpy as np
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import os
import seaborn as sns
import matplotlib.pyplot as plt
st.set_page_config(page_title='Clock Drawing Test', initial_sidebar_state = 'auto')

st.set_option('deprecation.showfileUploaderEncoding', False)
st.title("Clock Image Classifier")

st.text("select clock Image for prediction")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
@st.cache(allow_output_mutation=True)
def load_model():
  model = tf.keras.models.load_model('./')
  return model

with st.spinner('Loading Model Into Memory....'):
  model = load_model()

classes=['demented','normal']

def scale(image):
  image = tf.cast(image, tf.float32)
  image /= 255.0

  return tf.image.resize(image,[128,128])

def decode_img(image):
  img = tf.image.decode_jpeg(image, channels=3)
  img = scale(img)
  return np.expand_dims(img, axis=0)



# st.title("Upload + Classification Example")
types= ["png","jpg"]
uploaded_file = st.file_uploader("Choose an image...", type=types )
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    

    image = image.convert("RGB")
    image = np.asarray(image, dtype=np.float32) / 255
    image = image[:, :, :3]
    image = cv2.resize(image, (128, 128))
    
    st.write("")
    st.write("Classifying...")
    res = model.predict(np.array([image]))
    st.write("likelihood for dementia:") 
    st.write(res[0][0]) 
    label =np.argmax(res,axis=1)
#     st.write(classes[label[0]]) 
    
    with open('hist.pkl','rb') as f:
         x = pickle.load(f)
    p = res[0][0]
    fig, ax = plt.subplots()
    ax=sns.distplot(x, hist = False, kde = True,
                     kde_kws = {'linewidth': 3},
                     label = "likelihood for dementia")
    ax.axvline(p, 0,5)
    ax.text(p, 5, 'your score')
    st.pyplot(fig)
