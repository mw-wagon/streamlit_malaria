import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import time

# images:

malaria_parasite_bright = Image.open('/Users/aliciademora/code/aliciademorauk/project/frontend_malaria/streamlit_malaria/app/images/Cells-Background.jpeg')
malari_eye_logo = Image.open('/Users/aliciademora/code/aliciademorauk/project/frontend_malaria/streamlit_malaria/app/images/Malaria-Logo.png')
malaria_parasite = Image.open('/Users/aliciademora/code/aliciademorauk/project/frontend_malaria/streamlit_malaria/app/images/Malaria-Parasite.jpeg')
bounding_boxes_img = Image.open('/Users/aliciademora/code/aliciademorauk/project/frontend_malaria/streamlit_malaria/app/images/Bounding-Boxes.jpeg')
blood_microscope_slide = Image.open('/Users/aliciademora/code/aliciademorauk/project/frontend_malaria/streamlit_malaria/app/images/Blood-Sample-Slide.jpeg')
purple_cells = Image.open('/Users/aliciademora/code/aliciademorauk/project/frontend_malaria/streamlit_malaria/app/images/Purple-Cells-PhotoRoom.png')
arnaud_photo = Image.open('/Users/aliciademora/code/aliciademorauk/project/frontend_malaria/streamlit_malaria/app/images/Arnaud-Circle.png')
alicia_photo = Image.open('/Users/aliciademora/code/aliciademorauk/project/frontend_malaria/streamlit_malaria/app/images/Alicia-Circle.png')
mark_photo = Image.open('/Users/aliciademora/code/aliciademorauk/project/frontend_malaria/streamlit_malaria/app/images/Mark-Circle.png')

# page configuration...

# 1. page title, layout

st.set_page_config(page_title='Malari-Eye | The Project',
                   page_icon=malari_eye_logo,
                   layout='wide'
)

# malari_eye logo

col_00, col_11 = st.columns([7,1])
col_11.image(malari_eye_logo)

# CSS styling file opening for customisation

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}<style>', unsafe_allow_html=True)

# start of page

st.title('About the Project')

# how it works in steps
st.text('')
st.text('')
st.text('')
st.subheader('How it Works')

# how it works - step 1

col11 , col22 = st.columns([2,1])
st.text('')
st.text('')
st.text('')
col11.image(blood_microscope_slide, use_column_width=True)
col22.header('Upload your blood sample.')
col22.write('After extracting and preparing the blood sample, the scientific image can be uploaded for scanning using our Testing Area.')

# how it works - step 2

col111,col222 = st.columns([1,2])
st.text('')
st.text('')
st.text('')
col111.header('Our model will prepare the image for individual cell scanning.')
col111.write('Leveraging YOLO\'s real-time object detection, our product will identify all cells within the image with the use of bounding boxes.')
col222.image(bounding_boxes_img, use_column_width=True)

# how it works - step 3

col1111,col2222 = st.columns([2,1])
st.text('')
st.text('')
st.text('')
col1111.image(purple_cells)
col2222.header('The data will flow through our Convolutional Neural Network.')
col2222.write('Our deep-learning model will take the unique cells within bounding boxes as an input to compare them against what it has learned from a dataset with 80,000 categorized cells.')

# how it works - step 4

col11111,col22222 = st.columns([1,2])
st.text('')
st.text('')
st.text('')
col11111.header('All cells in the scientific sample will be classified into one of six categories.')
col11111.write('Our model will output whether a scanned cell is infected or not, as well as the stage of infection, by displaying the cell category: Gametocyte, Leukocyte, Red Blood Cell, Ring, Schizont, Trophozoite.')
# col22222.image() pending -- want to add an image of the table with the classified cells

# meet the team photos and names

st.subheader('Meet the Team')
meet_the_team_space0, meet_the_team_1, meet_the_team_2, meet_the_team_3, meet_the_team_space4 = st.columns([1,3,3,3,1])
meet_the_team_1.image(alicia_photo)
meet_the_team_1.markdown("<h4 style='text-align: center; color: black;'>Alicia de Mora Losana</h4>", unsafe_allow_html=True)
meet_the_team_2.image(arnaud_photo)
meet_the_team_2.markdown("<h4 style='text-align: center; color: black;'>Arnaud Plantenga</h4>", unsafe_allow_html=True)
meet_the_team_3.image(mark_photo)
meet_the_team_3.markdown("<h4 style='text-align: center; color: black;'>Mark White</h4>", unsafe_allow_html=True)
