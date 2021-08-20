import numpy as np
import streamlit as st
import pandas as pd
from user_heatmap import get_heatmap, get_starmap, get_heat_matrix, get_aspectmap, get_seibetsu, get_shozoku, get_nenrei, get_kyojuchi, get_hoshi, get_sentiment_bar

st.write('店舗画面')
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
    v4 = st.button('来客者性別情報円グラフ')
    if v4:
        get_seibetsu(file)
    v5 = st.button('来客者所属情報円グラフ')
    if v5:
        get_shozoku(file)
    v6 = st.button('来客者年齢情報円グラフ')
    if v6:
        get_nenrei(file)
    v7 = st.button('来客者居住地情報円グラフ')
    if v7:
        get_kyojuchi(file)
    v8 = st.button('来客者星評価情報円グラフ')
    if v8:
        get_hoshi(file)
    v9 = st.button('項目別店舗評価')
    if v9:
        get_sentiment_bar(file)
        


    
    
