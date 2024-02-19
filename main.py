import streamlit as st
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import tensorflow as tf

import base64
import numpy as np



# ---------------Requied Data-----------------

def predict(model, img):
    class_names = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']

    img_array = tf.keras.preprocessing.image.img_to_array(img.numpy())
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = model.predict(img_array)

    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class, confidence

@st.cache_data
def Load_Model():
  model=load_model('model_50_epochs')
  return model

model=Load_Model()

def set_bg_hack(main_bg):
   '''
   A function to unpack an image from root folder and set as bg.

   Returns
   -------
   The background.
   '''
   # set bg name
   main_bg_ext = "png"

   st.markdown(
      f"""
        <style>
        .stApp {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
            background-size: cover

        }}
        </style>
        """,
      unsafe_allow_html=True
   )
set_bg_hack('potato.jpg')



page_bg="""
<style>


    [data-testid="stVerticalBlock"]{
        background-color: #EEEDEB;
        opacity: 0.85;
    }
    
    [data-testid="stVerticalBlockBorderWrapper"]{
        background-color: #EEEDEB;
        opacity: 0.85;
    }
    
    [data-testid="stHeader"]{
        background-color:rgba(0,0,0,0)
    }
    
</style>
"""
# data-testid="block-container"
st.markdown(page_bg,unsafe_allow_html=True)





def save_file(img):
    try:
        with open(os.path.join('uploaded',img.name),'wb') as f:
            f.write(img.getbuffer())
        return 1
    except:
        return 0

# Web Devlopment
st.markdown(f'<h1 style="color:black;font-size:64px;">{"Potato Leaf Care"}</h1>', unsafe_allow_html=True)

input_type=st.selectbox('Type',['Upload from Gallery','Upload by Camera'])

if input_type=='Upload by Camera':
    uploaded_img = st.camera_input("Take a picture")

else:
    uploaded_img = st.file_uploader('Upload Image')



if uploaded_img is not None:

    st.markdown(f'<h1 style="color:black;">{"Image Uploaded"}</h1>', unsafe_allow_html=True)

    if save_file(uploaded_img):

        img = image.load_img(os.path.join('uploaded',uploaded_img.name), target_size=(256, 256))
        st.image(img)
        img_array = image.img_to_array(img)
        img_tf = tf.convert_to_tensor(img_array)
        class_,confidence=predict(model,img_tf)

        if confidence>50:
            st.markdown(f'<h2 style="color:black;">Potato Type={class_}</h2>', unsafe_allow_html=True)
            st.markdown(f'<h2 style="color:black;">Confidence=<spam style="color:green;">{confidence}</spam></h2>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h2 style="color:black;">Potato Type={class_}</h2>', unsafe_allow_html=True)
            st.markdown(f'<h2 style="color:black;">Confidence=<spam style="color:red;">{confidence}</spam></h2>',unsafe_allow_html=True)

    else:
        st.write('Error')







