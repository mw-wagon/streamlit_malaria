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

if 'df' not in st.session_state.keys():
    st.session_state['df'] = ''

# images

malari_eye_logo = Image.open('streamlit_malaria/app/images/Malaria-Logo.png')
spread_stages = Image.open('streamlit_malaria/app/images/Red-Spread-Stages.png')
img_ring = Image.open('streamlit_malaria/app/images/Ring.png')
img_trophozoite = Image.open('streamlit_malaria/app/images/Trophozoite.png')
img_schizont = Image.open('streamlit_malaria/app/images/Schizont.png')
img_gametocyte = Image.open('streamlit_malaria/app/images/Gametocyte.png')

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

with open('streamlit_malaria/app/style.css') as f:
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
st.markdown("""<hr style="height:1px; border:none; color:#FFFFFF; background-color:#FFFFFF;" /> """, unsafe_allow_html=True)
st.text('')
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
#<<<<<MW        resized_cells.append(image[x:x_max, y:y_max, :])
#>>>>>MW
        resized_cells.append(image[y:y_max,x:x_max, :])
    # Add the boxes to the plot
    return img, np.array(resized_cells)

def get_bounding_infected(df, image):
        resized_cells = []
        for index, row in df.iterrows():
            x = round(row['xmin'])
            y = round(row['ymin'])
            x_max = round(row['xmax'])
            y_max = round(row['ymax'])
#<<<<MW    #breakpoint()
#<<<<MW    #resized_cells.append(cv2.resize(image[x:x_max, y:y_max,:],(200,200)).tolist())
#>>>>>MW
            resized_cells.append(cv2.resize(image[y:y_max,x:x_max,:],(200,200)).tolist())
#>>>>>MW
        # Add the boxes to the plot
        return np.array(resized_cells).astype(np.uint8).flatten()
### TABS

tab1, tab2, = st.tabs(["UPLOAD A BLOOD SAMPLE", "CONNECT TO MY CAMERA OR WEBCAM"])

with tab1: # upload a photo
    image_file = st.file_uploader(label='')
    if image_file is not None:
        img_bytes = image_file.getvalue()
        uploaded_sample = Image.open(image_file)
        col_text, col_sample = st.columns([3,1], gap='medium')
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
            if col_text.button(label='CONFIRM AND PROCEED', key=0) or st.session_state.get("proceeded_upload"):
                st.session_state["proceeded_upload"] = True
                st.success('Success! Your sample is being processed...')
                # API CALL
                res = requests.post('https://malari-eye-ueodddo5aa-ez.a.run.app' + "/upload_image", files={'img': img_bytes})
                st.session_state['df'] = pd.DataFrame.from_dict(json.loads(res.content))
                bounding_boxes, resized_cells = get_bounding_box_image(st.session_state['df'], np.asarray(uploaded_sample))
                im = Image.fromarray(bounding_boxes).convert('RGB')
                buffered = BytesIO()
                im.save(buffered, format="JPEG")
                byte_im = buffered.getvalue()
                # display bounding_boxes_image with cell count in caption and allow the user to download the file
                cell_count = st.session_state['df'].shape[0]
                st.session_state['bounded_image'] = bounding_boxes
                st.image(image=bounding_boxes)
                st.write(f'{cell_count} cells have been detected in the sample.')
                st.write('You can download this image below and continue on to Step 2.')
                st.text('')
                st.text('')
                # allow the user to download the file
                download_button = st.download_button(label='DOWNLOAD FILE', data=byte_im, file_name='Bounding-Boxes.png', mime = "image/png")



with tab2: # take a picture
    image_file = st.camera_input(label='')
    if image_file is not None:
        img_bytes = image_file.getvalue()
        uploaded_sample = Image.open(image_file)
        img_array = np.array(uploaded_sample)
    # output the image to the user to confirm that it is the right blood sample
        col_text, col_button = st.columns([3,1])
        col_text.text('')
        col_text.subheader('This is the blood sample that will be uploaded.')
        col_text.subheader('Please confirm and proceed if you want to process this sample:')
        col_text.text('')
        # user clicks proceed for bounding boxes to be drawn around cells in sample
        if 'bounded_image' in st.session_state.keys():
            bounding_boxes = st.session_state['bounded_image']
        col_button.text('')
        col_button.text('')
        col_button.text('')
        if col_button.button('CONFIRM AND PROCEED',key=1) or st.session_state.get("proceeded_webcam"):
            st.session_state["proceeded_webcam"] = True
            st.success('Success! Your sample is being processed...')
            # API CALL
            res = requests.post('https://malari-eye-ueodddo5aa-ez.a.run.app' + "/upload_image", files={'img': img_bytes})
            st.session_state['df'] = pd.DataFrame.from_dict(json.loads(res.content))
            # df = pd.DataFrame.from_dict(json.loads(res.content))
            # bounding_boxes = get_bounding_box_image(st.session_state['df'], np.asarray(uploaded_sample))
            bounding_boxes, resized_cells = get_bounding_box_image(st.session_state['df'], np.asarray(uploaded_sample))
            im = Image.fromarray(bounding_boxes).convert('RGB')
            buffered = BytesIO()
            im.save(buffered, format="JPEG")
            byte_im = buffered.getvalue()
            # display bounding_boxes_image with cell count in caption and allow the user to download the file
            cell_count = st.session_state['df'].shape[0]
            # cell_count = df.shape[0]
            st.session_state['bounded_image'] = bounding_boxes
            st.image(image=bounding_boxes)
            st.write(f'{cell_count} cells have been detected in the sample.')
            st.write('You can download this image below and continue on to Step 2.')
            st.text('')
            st.text('')
            # allow the user to download the file
            st.download_button(label='DOWNLOAD FILE', data=byte_im, file_name='Bounding-Boxes.png', mime = "image/png")

            ###### STEP 2 - OUTPUT

st.header('Step 2')
st.markdown("""<hr style="height:1px; border:none; color:#FFFFFF; background-color:#FFFFFF;" /> """, unsafe_allow_html=True)
st.text('')
st.text('')

st.write('Our model will determine the infection stage of the patient.')
st.write('Please click on "generate diagnosis" below to see predicted results based on the blood sample provided above.')

st.text('')
st.text('')
st.text('')

# when button is pressed, it will run through the if statement depending on whether an infection has been detected

if st.button(label='GENERATE DIAGNOSIS', key=3):
    categories = st.session_state['df']['name'].unique()

    if 'infected' not in categories:
        st.text('')
        st.text('')
        st.success(f'No parasitaemia detected in any of the {cell_count} cells in the blood sample!')
    else:
        mask1 = st.session_state['df']['name'] == 'infected'
        df_infected = st.session_state['df'][st.session_state['df']['name']=='infected']
        # st.write(df_infected)
        resized_cells = get_bounding_infected(df_infected, np.asarray(uploaded_sample))
        # st.write(resized_cells.shape)
        res = requests.post('https://malari-eye-ueodddo5aa-ez.a.run.app' + "/cell_predict", json=json.dumps({"stuff":resized_cells.tolist()}))
        df = pd.DataFrame(json.loads(res.content).items())
        df = df.rename(columns={0:'Cell Stage', 1: 'Number of Cells in Sample'})
        df['Cell Stage'] = df['Cell Stage'].apply(lambda x: x.capitalize())
        no_gametocytes = df['Cell Stage'] == 'Gametocyte'
        sum_no_gametocytes = no_gametocytes.sum()
        df = df.set_index('Cell Stage',)
        st.subheader('Based on the sample provided, these are your results:')
        st.text('')
        # specific if statement if the patient is contagious i.e. has a gametocyte
        if sum_no_gametocytes > 0:
            col_warning, col_df = st.columns(2,gap='medium')
            # column with warning
            col_warning.text('')
            col_warning.text('')
            col_warning.error('WARNING: THE PATIENT IS INFECTED. THE PATIENT IS CONTAGIOUS AND IS AT RISK OF SPREADING THE DISEASE DUE TO THE PRESENCE OF GAMETOCYTES.')
            # results column with warning download button
            col_df.text('')
            col_df.text('')
            col_df.write(df)
            col_df.text('')
            col_df.text('')
            df_csv = df.to_csv().encode('utf-8')
            col_df.download_button(label="DOWNLOAD RESULTS TO CSV FILE AND EXIT", data=df_csv, file_name="Malaria-Detection-Results.csv", mime="text/csv", key='download-csv')
            # show cell stage images with count
            st.text('')
            st.text('')
            colimg_1, colimg_2, colimg_3, colimg_4 = st.columns(4)
            colimg_1.image(img_ring)
            colimg_1.write('Ring')
            if 'Ring' in list(df.index.values):
                colimg_1.write(df.loc['Ring', 'Number of Cells in Sample'])
            else:
                colimg_1.write(0)
            colimg_2.image(img_trophozoite)
            colimg_2.write('Trophozoite')
            if 'Trophozoite' in list(df.index.values):
                colimg_2.write(df.loc['Trophozoite','Number of Cells in Sample'])
            else:
                colimg_2.write(0)
            colimg_3.image(img_schizont)
            colimg_3.write('Schizont')
            if 'Schizont' in list(df.index.values):
                colimg_3.write(df.loc['Schizont','Number of Cells in Sample'])
            else:
                colimg_3.write(0)
            colimg_4.image(img_gametocyte)
            colimg_4.write('Gametocyte')
            if 'Schizont' in list(df.index.values):
                colimg_4.write(df.loc['Gametocyte','Number of Cells in Sample'])
            else:
                colimg_4.write(0)

        #  if statement if the patient is not-contagious i.e. has a gametocyte
        else:
            col_small_warning, col_small_df = st.columns(2,gap='medium')
            # column with warning
            col_small_warning.text('')
            col_small_warning.text('')
            col_small_warning.error('WARNING: THE PATIENT IS INFECTED. THE PATIENT IS NOT YET AT RISK OF SPREADING THE DISEASE.')
            # results column with warning download button
            col_small_df.text('')
            col_small_df.text('')
            col_small_df.write(df)
            col_small_df.text('')
            col_small_df.text('')
            df_csv = df.to_csv().encode('utf-8')
            col_small_df.download_button(label="DOWNLOAD RESULTS TO CSV FILE AND EXIT", data=df_csv, file_name="Malaria-Detection-Results.csv", mime="text/csv", key='download-csv')
            # show cell stage images with count
            st.text('')
            st.text('')
            colimg_1, colimg_2, colimg_3, colimg_4 = st.columns(4)
            colimg_1.image(img_ring)
            colimg_1.write('Ring')
            if 'Ring' in list(df.index.values):
                colimg_1.write(df.loc['Ring', 'Number of Cells in Sample'])
            else:
                colimg_1.write(0)
            colimg_2.image(img_trophozoite)
            colimg_2.write('Trophozoite')
            if 'Trophozoite' in list(df.index.values):
                colimg_2.write(df.loc['Trophozoite','Number of Cells in Sample'])
            else:
                colimg_2.write(0)
            colimg_3.image(img_schizont)
            colimg_3.write('Schizont')
            if 'Schizont' in list(df.index.values):
                colimg_3.write(df.loc['Schizont','Number of Cells in Sample'])
            else:
                colimg_3.write(0)
            colimg_4.image(img_gametocyte)
            colimg_4.write('Gametocyte')
            if 'Schizont' in list(df.index.values):
                colimg_4.write(df.loc['Gametocyte','Number of Cells in Sample'])
            else:
                colimg_4.write(0)
