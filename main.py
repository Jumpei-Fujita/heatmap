import numpy as np
import streamlit as st
import pandas as pd
from user_heatmap import get_heatmap, get_starmap, get_heat_matrix, get_aspectmap


file = st.file_uploader("ファイルアップロード", type='csv')
if file is not None:
    file = pd.read_csv(file)
    st.dataframe(file)
    v1 = st.button('客層ヒートマップ可視化')
    
    heat_matrix = get_heat_matrix(file)
    if v1:
        heat_matrix = get_heatmap(file, heat_matrix)
    v2 = st.button('星評価ヒートマップ可視化')
    if v2:
        get_starmap(file, heat_matrix)
    v3 = st.button('属性項目可視化マップ')
    if v3:
        get_aspectmap(file)
    
    
