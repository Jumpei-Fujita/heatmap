import numpy as np
import streamlit as st
import pandas as pd
from user_heatmap import get_heatmap, get_starmap, get_heat_matrix, get_aspectmap, get_seibetsu, get_shozoku, get_nenrei, get_kyojuchi, get_hoshi, get_sentiment_bar

st.write('店舗画面')
file = st.file_uploader("ファイルアップロード", type='csv')

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 500px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 500px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if file is not None:
    file = pd.read_csv(file)
    st.dataframe(file)
    
    heat_matrix = get_heat_matrix(file)

    options = st.multiselect(
    '可視化する図を選んでください',
    ['客層ヒートマップ', '星評価ヒートマップ', '属性項目可視化マップ', '来客者性別情報円グラフ', '来客者所属情報円グラフ', '来客者年齢情報円グラフ', '来客者居住地情報円グラフ', '来客者星評価情報円グラフ', '項目別店舗評価'])

    options_side = st.sidebar.multiselect(
    '可視化する円グラフを選んでください',
    ['来客者性別情報円グラフ', '来客者所属情報円グラフ', '来客者年齢情報円グラフ', '来客者居住地情報円グラフ', '来客者星評価情報円グラフ'])
    if '来客者性別情報円グラフ' in options_side:
        get_seibetsu(file, st.sidebar, True)
    
    if '来客者所属情報円グラフ' in options_side:
        get_shozoku(file, st.sidebar, True)
    
    if '来客者年齢情報円グラフ' in options_side:
        get_nenrei(file, st.sidebar, True)
    
    if '来客者居住地情報円グラフ' in options_side:
        get_kyojuchi(file, st.sidebar, True)
    
    if '来客者星評価情報円グラフ' in options_side:
        get_hoshi(file, st.sidebar, True)
    
    options2 = options.copy()
    for i in options:
        if i in ['客層ヒートマップ', '星評価ヒートマップ', '属性項目可視化マップ', '項目別店舗評価']:
            options2.remove(i)

    left_column,right_column = st.columns(2)
    column_map = {}
    for i in range(len(options2)):
        if i % 2 == 0:

            column_map[options2[i]] = left_column
        else:

            column_map[options2[i]] = right_column

    if '客層ヒートマップ' in options:
        get_heatmap(file, heat_matrix)

    if '星評価ヒートマップ' in options:
        get_starmap(file, heat_matrix)

    if '属性項目可視化マップ' in options:
        get_aspectmap(file)

    if '来客者性別情報円グラフ' in options:
        get_seibetsu(file, st, False)
    
    if '来客者所属情報円グラフ' in options:
        get_shozoku(file, st, False)
    
    if '来客者年齢情報円グラフ' in options:
        get_nenrei(file, st, False)
    
    if '来客者居住地情報円グラフ' in options:
        get_kyojuchi(file, st, False)
    
    if '来客者星評価情報円グラフ' in options:
        get_hoshi(file, st, False)
    
    if '項目別店舗評価' in options:
        get_sentiment_bar(file)


    