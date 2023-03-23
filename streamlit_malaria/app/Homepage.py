# imports
import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import time
from streamlit.components.v1 import html

# images:
malaria_parasite_bright = Image.open('streamlit_malaria/app/images/Rounded-Bright-Cells.png')
malaria_parasite_red = Image.open('app/images/Cell-Homepage2.png')
malari_eye_logo = Image.open('app/images/Malaria-Logo.png')
malaria_parasite = Image.open('app/images/Malaria-Parasite.jpeg')
africa_spread = Image.open('app/images/Africa-Spread-PhotoRoom.png')

# page configuration...

# page title, layout

st.set_page_config(page_title='Malari-Eye | AI Diagnostics',
                   page_icon=malari_eye_logo,
                   layout='wide'
)

# malari_eye logo

col_00, col_11 = st.columns([7,1])
col_11.image(malari_eye_logo)

# title

st.markdown("<h1 style='text-align: right; color: black; font-size: 500%; text-shadow: 4px 4px #cfc9c9'>Microscopy results with the speed of RDTs.</h1>",
            unsafe_allow_html=True)

# CSS styling file opening for customisation

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}<style>', unsafe_allow_html=True)

# container with Africa map image and text

with st.container():
    col__1, col__2 = st.columns([3,2])
    with col__1:
        st.image(africa_spread)
    with col__2:
        # empty space
        st.text('')
        st.text('')
        st.text('')
        st.text('')
        st.text('')
        st.text('')
        # text
        st.markdown("<h4 style='text-align: right; color: black; font-size: 250%; text-shadow: 2px 2px #cfc9c9'>1 million people die from malaria every year, primarily in the WHO African Region.</h4>",
                    unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right; color: black; font-size: 150%; text-shadow: 1px 1px #cfc9c9'>We are part of the solution.</h4>",
                    unsafe_allow_html=True)

# space between images and text blocks

st.text('')
st.text('')
st.text('')
st.text('')
st.text('')
st.text('')

# cnn text and shadowed image

# function to make st.buttons take user to pages on side bar

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

with st.container():
    col1, col2 = st.columns([1,2])
    col1.text('')
    col1.text('')
    col1.text('')
    col1.markdown("<h4 style='text-align: left; color: black; font-size: 150%; text-shadow: 1px 1px #cfc9c9; padding: 20px 20px; line-height: 1.5'>Using ANNs (Artificial Neural Networks) for malaria-paratysized cell identification.</h4>",
                    unsafe_allow_html=True)
    col1.text('')
    col1.text('')
    col1.text('')
    if col1.button('READ MORE', key=0):
        nav_page("The Project")
    col2.image(malaria_parasite_bright)

# space between images and text blocks
st.text('')
st.text('')
st.text('')

# text and red cell image
with st.container():
    col_a, col_b = st.columns([2,1])
    col_a.image(malaria_parasite_red)
    col_b.text('')
    col_b.text('')
    col_b.text('')
    col_b.markdown("<h4 style='text-align: left; color: black; font-size: 150%; text-shadow: 1px 1px #cfc9c9; padding: 20px 20px; line-height: 1.5'>Lol something.</h4>",
                    unsafe_allow_html=True)
    col_b.text('')
    col_b.text('')
    col_b.text('')
#   if st.button('CLICK HERE'):
#     nav_page('Testing Area')
    col_b.button('CLICK HERE', key=1)
