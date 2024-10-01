from urllib import request
import streamlit as st 
import pandas as pd
import numpy as np
import requests

data = requests.get("https://api.mapbox.com/search/searchbox/v1/suggest?q={search_text}").json()

st.write(data)