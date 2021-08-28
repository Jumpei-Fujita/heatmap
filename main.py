import numpy as np
import streamlit as st
import pandas as pd
from user_heatmap import get_heatmap, get_starmap, get_heat_matrix, get_aspectmap, get_seibetsu, get_shozoku, get_nenrei, get_kyojuchi, get_hoshi, get_sentiment_bar

st.write('店舗画面')
file = st.file_uploader("ファイルアップロード", type='csv')
if file is not None:
    file = pd.read_csv(file)
    st.dataframe(file)
    
    heat_matrix = get_heat_matrix(file)

    options = st.multiselect(
    '可視化する図を選んでください',
    ['客層ヒートマップ', '星評価ヒートマップ', '属性項目可視化マップ', '来客者性別情報円グラフ', '来客者所属情報円グラフ', '来客者年齢情報円グラフ', '来客者居住地情報円グラフ', '来客者星評価情報円グラフ', '項目別店舗評価'])
    
    left_column, _, _, _, _, _, _, _, _, right_column = st.columns(10)
    column_map = {}
    for i in range(len(options)):
        if i % 2 == 0:
            column_map[options[i]] = left_column
        else:
            column_map[options[i]] = right_column

    if '客層ヒートマップ' in options:
        get_heatmap(file, heat_matrix, column_map['客層ヒートマップ'])

    if '星評価ヒートマップ' in options:
        get_starmap(file, column_map['星評価ヒートマップ'], heat_matrix)

    if '属性項目可視化マップ' in options:
        get_aspectmap(file, column_map['属性項目可視化マップ'])

    if '来客者性別情報円グラフ' in options:
        get_seibetsu(file, column_map['来客者性別情報円グラフ'])
    
    if '来客者所属情報円グラフ' in options:
        get_shozoku(file, column_map['来客者所属情報円グラフ'])
    
    if '来客者年齢情報円グラフ' in options:
        get_nenrei(file, column_map['来客者年齢情報円グラフ'])
    
    if '来客者居住地情報円グラフ' in options:
        get_kyojuchi(file, column_map['来客者居住地情報円グラフ'])
    
    if '来客者星評価情報円グラフ' in options:
        get_hoshi(file, column_map['来客者星評価情報円グラフ'])
    
    if '項目別店舗評価' in options:
        get_sentiment_bar(file, column_map['項目別店舗評価'])


    