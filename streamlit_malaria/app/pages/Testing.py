import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import time
import json
from io import BytesIO

# images

malari_eye_logo = Image.open('./images/Malaria-Logo.png')

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

# two tabs, 1. upload a photo file and 2.connect to system's webcam
# includes API call for the user to see image with BOUNDING BOXES displayed

# first quickly define the function that transforms bounding boxes coordinates into an image

def get_bounding_box_image(df, image):
# Load the image; Plot the image; print(image.shape); Define the boxes
    resized_cells = []
    img = image.copy()
    for index, row in df.iterrows():
        x = round(row['xmin'])
        y = round(row['ymin'])
        x_max = round(row['xmax'])
        y_max = round(row['ymax'])
        # breakpoint()
        img = cv2.rectangle(img, (x, y), (x_max, y_max), (255,0,0), 2)
        resized_cells.append(image[x:x_max, y:y_max, :])
    # Add the boxes to the plot
    return img, np.array(resized_cells)

### TABS

tab1, tab2, = st.tabs(["UPLOAD A BLOOD SAMPLE", "CONNECT TO MY CAMERA OR WEBCAM"])

with tab1: # upload a photo
    image_file = st.file_uploader(label='')
    if image_file is not None:
        img_bytes = image_file.getvalue()
        uploaded_sample = Image.open(image_file)
        col_text, col_sample = st.columns([3,1])
        with col_sample:
            # output a small image for the user to confirm that it is the right blood sample
            col_sample.image(uploaded_sample, use_column_width=True)
        with col_text:
            st.subheader('This is the blood sample selected.')
            st.subheader('Please confirm if you want to process this file.')
            if 'bounded_image' in st.session_state.keys():
                bounding_boxes = st.session_state['bounded_image']
            st.text('')
            st.text('')
            st.text('')
            # user clicks proceed for bounding boxes to be drawn around cells in sample
            if col_text.button(label='CONFIRM AND PROCEED', key=0):
                st.success('Success! Your sample is being processed...')
                # API CALL
                res = requests.post('http://127.0.0.1:8000' + "/upload_image", files={'img': img_bytes})
                df = pd.DataFrame.from_dict(json.loads(res.content))
                bounding_boxes, resized_cells = get_bounding_box_image(df, np.asarray(uploaded_sample))
                im = Image.fromarray(bounding_boxes).convert('RGB')
                buffered = BytesIO()
                im.save(buffered, format="JPEG")
                byte_im = buffered.getvalue()
                # display bounding_boxes_image with cell count in caption and allow the user to download the file
                cell_count = df.shape[0]
                st.session_state['bounded_image'] = bounding_boxes
                st.image(image=bounding_boxes)
                st.write(f'{cell_count} cells have been detected in the sample.')
                st.write('You can download this image below.')
                st.text('')
                st.text('')
                # allow the user to download the file
                st.download_button(label='DOWNLOAD FILE', data=byte_im, file_name='Bounding-Boxes.png', mime = "image/png")

with tab2: # take a picture
    image_file = st.camera_input(label='')
    if image_file is not None:
        img_bytes = image_file.getvalue()
        uploaded_sample = Image.open(image_file)
    # output the image to the user to confirm that it is the right blood sample
        col_text, col_button = st.columns([3,1])
        col_text.subheader('This is the blood sample that will be uploaded.')
        col_text.subheader('Please click "proceed" below if you want to process this sample:')
        # user clicks proceed for bounding boxes to be drawn around cells in sample
        if 'bounded_image' in st.session_state.keys():
            bounding_boxes = st.session_state['bounded_image']
        col_button.text('')
        col_button.text('')
        col_button.text('')
        if col_button.button('CONFIRM AND PROCEED',key=1):
            st.success('Success! Your sample is being processed...')
            # API CALL
            res = requests.post('http://127.0.0.1:8000' + "/upload_image", files={'img': img_bytes})
            df = pd.DataFrame.from_dict(json.loads(res.content))
            bounding_boxes = get_bounding_box_image(df, np.asarray(uploaded_sample))
            im = Image.fromarray(bounding_boxes).convert('RGB')
            buffered = BytesIO()
            im.save(buffered, format="JPEG")
            byte_im = buffered.getvalue()
            # display bounding_boxes_image with cell count in caption and allow the user to download the file
            cell_count = df.shape[0]
            st.session_state['bounded_image'] = bounding_boxes
            st.image(image=bounding_boxes)
            st.subheader(f'{cell_count} cells have been detected in the sample.')
            st.subheader('You can download this image below.')
            st.text('')
            st.text('')
            # allow the user to download the file
            st.download_button(label='DOWNLOAD FILE', data=byte_im, file_name='Bounding-Boxes.png', mime = "image/png")

###### STEP 2 - OUTPUT

st.header('Step 2')
st.text('')
tab_1 = st.tabs(['DIAGNOSIS GENERATION'])
with tab_1:
    st.write('Our model will determine the infection stage of the patient.')
    st.write('Please click on "generate diagnosis" below to see results.')

st.text('')
st.text('')
st.text('')

# when button is pressed, it will run through the if statement depending on whether an infection has been detected

if st.button(label='GENERATE DIAGNOSIS', key=3):
    categories = df['name'].unique()

    if 'infected' not in categories:
        st.success('No parasitaemia detected in sample!')
    else:
        mask1 = df['name'] == 'uninfected'
        mask2 = df['name'] == 'leukocyte'
        df = df.loc[~mask1]
        df = df.loc[~mask2]

# API call with st.progress displayed for the user to get FINAL OUTPUT i.e. table and graph

# here is the st.progress widget which displays progress as a function of time using the time package while the code is executed (i.e. the API call)
# with st.progress(0, text = 'Operation in progress. Please wait.'):
#     for percent_complete in range(100):
#         time.sleep(0.1)
#         st.progress(0).progress(percent_complete + 1, text='Operation in progress. Please wait.')
#         st.code(code_2) # returns blood_sample_categories dictionary

#### TABLE

# results_df = pd.DataFrame(columns=['Gametocyte', 'Leukocyte', 'Red Blood Cell', 'Ring', 'Schizont','Trophozoite'],data=blood_sample_categories)
# st.table(results_df)

#### GRAPH

cells_graph = sns.load_dataset(results_df)
fig = plt.figure(figsize=(10, 4))
sns.barplot(x=(results_df['columns']), data=results_df)
st.pyplot(fig)
