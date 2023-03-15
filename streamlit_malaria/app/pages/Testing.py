import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import time

# images

malari_eye_logo = Image.open('/Users/aliciademora/code/aliciademorauk/project/frontend_malaria/streamlit_malaria/app/images/Malaria-Logo.png')

# page configuration...
# page title, layout

st.set_page_config(page_title='Malari-Eye | Testing Area',
                   page_icon=malari_eye_logo,
                   layout='wide'
)

# malari_eye logo top right

col_00, col_11 = st.columns([7,1])
col_11.image(malari_eye_logo)

# CSS styling file opening for customisation

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}<style>', unsafe_allow_html=True)

# 'TESTING AREA'

st.title('Testing Area')
st.text('')
st.text('')
st.text('')
st.subheader('Please follow the steps below to generate a diagnosis.')

###### FILE UPLOADER & BOUNDING BOXES ######

###### STEP 1 - upload file or connect to camera ######

st.header('Step 1')
st.text('')
st.text('')
st.text('')

# two tabs, 1. upload a photo file and 2.connect to system's webcam
# API call for the user to see image with BOUNDING BOXES displayed

tab1, tab2, = st.tabs(["UPLOAD A BLOOD SAMPLE", "CONNECT TO MY CAMERA OR WEBCAM"])

with tab1:
    image_file = st.file_uploader(label='')
    if image_file is not None:
        img_bytes = image_file.getvalue()
        uploaded_sample = Image.open(image_file)
        col_text, col_sample = st.columns([3,1])
        with col_sample:
            # output a small image for the user to confirm that it is the right blood sample
            col_sample.image(uploaded_sample, use_column_width=True)
        with col_text:
            st.write('This is the blood sample selected.')
            st.write('Please click "proceed" if you want to process this file:')
            st.text('')
            st.text('')
            st.text('')
            # user clicks proceed for bounding boxes to be drawn around cells in sample
            if col_text.button('PROCEED', key=0):
                st.success('Success! Your sample is being processed...')
                # API CALL
                res = requests.post('http://127.0.0.1:8000' + "/upload_image", files={'img': img_bytes})
                bounding_boxes = res.content
                # display bounding_boxes_image and allow the user to download the file
                st.image(bounding_boxes)
                st.download_button(label='DOWNLOAD FILE', data=bounding_boxes, file_name='Bounding-Boxes', mime = "image/png")

with tab2:
    image_file = st.camera_input("TAKE A PICTURE")
    if image_file is not None:
        img_bytes = image_file.getvalue()
        uploaded_sample = Image.open(image_file)
    # output the image to the user to confirm that it is the right blood sample
        col_text, col_button = st.columns(2)
        col_text.write('This is the blood sample that will be uploaded.')
        col_text.write('Please click "proceed" below if you want to process this sample:')
        # user clicks proceed for bounding boxes to be drawn around cells in sample
        if col_button.button('PROCEED',key=1):
            st.success('Success! Your sample is being processed...')
            # API CALL
            res = requests.post('http://127.0.0.1:8000' + "/upload_image", files={'img': img_bytes})
            bounding_boxes = res.content
            # display bounding_boxes_image and allow the user to download the file
            st.image(bounding_boxes)
            st.download_button(label='DOWNLOAD FILE', data=bounding_boxes, file_name='Bounding-Boxes', mime = "image/png")

###### STEP 2 - OUTPUT

st.header('Step 2')
st.text('')
st.text('')
st.text('')
st.write('Our model will determine malaria infection levels of the patient. Results will be displayed below.')
st.text('')
st.text('')
st.text('')
st.button('RUN MODEL')

# API call with st.progress displayed for the user to get FINAL OUTPUT i.e. table and graph

# code_2 = '''here is where the API CALL goes which RETURNS the categories/binary ouput'''
    #url = '?' #model on GC
    #myobj = {'filename': image_file.name}
    #blood_sample_categories = requests.post(url, json = myobj).json # here we need the model to return us a dictionary (json) with categories (2) and the number of cells per category.

# here is the st.progress widget which displays progress as a function of time using the time package while the code is executed (i.e. the API call)
# with st.progress(0, text = 'Operation in progress. Please wait.'):
#     for percent_complete in range(100):
#         time.sleep(0.1)
#         st.progress(0).progress(percent_complete + 1, text='Operation in progress. Please wait.')
#         st.code(code_2) # returns blood_sample_categories dictionary

#### TABLE

results_df = pd.DataFrame(columns=['Gametocyte', 'Leukocyte', 'Red Blood Cell', 'Ring', 'Schizont','Trophozoite'],data=blood_sample_categories)
st.table(results_df)

#### GRAPH

cells_graph = sns.load_dataset(results_df)
fig = plt.figure(figsize=(10, 4))
sns.barplot(x=(results_df['columns']), data=results_df)
st.pyplot(fig)
