import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Layout

aspects = ['Location#Transportation', 'Location#Downtown',
        'Location#Easy_to_find', 'Service#Queue', 'Service#Hospitality',
        'Service#Parking', 'Service#Timely', 'Price#Level',
        'Price#Cost_effective', 'Price#Discount', 'Ambience#Decoration',
        'Ambience#Noise', 'Ambience#Space', 'Ambience#Sanitary', 'Food#Portion',
        'Food#Taste', 'Food#Appearance', 'Food#Recommend']

aspects_japanese = ["場所#アクセスの良さ","場所#都心・繁華街にあるか","場所#見つけやすいか", "サービス#入店までの待ち時間", "サービス#接客", "サービス#駐車場の利便性", 
                    "サービス#料理の提供時間", "価格#水準", "価格#コストパフォーマンス", "価格#割引について", "雰囲気#装飾・雰囲気", "雰囲気#音楽・ノイズ", "雰囲気#店内・席の広さ",
                    "雰囲気#清潔感", "料理#分量", "料理#味", "料理#見た目", "料理#おすすめできるか"]

data = {'10' : 0, '20' : 1, '30' : 2, '40' : 3, '50' : 4, '60' : 5, '会社員/団体職員' : 6, 'パート/アルバイト' : 7, '自営業/個人事業主' : 8, '主婦/主夫' : 9, '学生' : 10, '契約社員/派遣社員' : 11,
    '会社役員/団体役員' : 12, '専門職(医師/弁護士/会計士/税理士等)' : 13, '退職された方' : 14, '公務員' : 15, '男性': 16, '女性' : 17}

columns = []
indexes = []
for k in data.keys():
    columns.append(k)
    indexes.append(k)

def get_heat_matrix(reviews):
    heat_matrix = np.zeros((18, 18))
    for i in range(len(reviews)):
        age = reviews['年齢'][i]
        zokusei = reviews['属性'][i]
        seibetsu = reviews['性別'][i]

        age = str(10 * int(age / 10))
        heat_matrix[data[age], data[age]] += 1
        heat_matrix[data[age], data[zokusei]] += 1
        heat_matrix[data[age], data[seibetsu]] += 1

        heat_matrix[data[zokusei], data[zokusei]] += 1
        heat_matrix[data[zokusei], data[age]] += 1
        heat_matrix[data[zokusei], data[seibetsu]] += 1

        heat_matrix[data[seibetsu], data[seibetsu]] += 1
        heat_matrix[data[seibetsu], data[zokusei]] += 1
        heat_matrix[data[seibetsu], data[age]] += 1
    return heat_matrix
    
def get_heatmap(reviews, heat_matrix):
    
    df = pd.DataFrame(data=heat_matrix, columns=columns, index=indexes)
    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=df, x=df.columns, y=df.index, colorscale='blues'))
    fig.update_layout(height=800,width=700, title='客層ヒートマップ')
    st.plotly_chart(fig)


def get_starmap(reviews, heat_matrix=None):
    
    s_m_5 = np.zeros((5, 18))
    for i in range(len(reviews)):
        age = reviews['年齢'][i]
        zokusei = reviews['属性'][i]
        seibetsu = reviews['性別'][i]
        age = str(10 * int(age / 10))
        star = int(reviews['星評価'][i] - 1)

        d_age = data[age]
        d_z = data[zokusei]
        d_s = data[seibetsu]

        age_len = heat_matrix[d_age, d_age]
        z_len = heat_matrix[d_z, d_z]
        s_len = heat_matrix[d_s, d_s]
        

        s_m_5[star, d_age] += 1
        s_m_5[star, d_z] += 1
        s_m_5[star, d_s] += 1
    
    s_map = pd.DataFrame(s_m_5, columns=columns, index=[i + 1 for i in range(5)])
    for c in columns:
        if np.sum(s_map[c]) != 0:
            s_map[c] = s_map[c] / np.sum(s_map[c])
    
    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=s_map, x=s_map.columns, y=s_map.index, colorscale='blues'))
    fig.update_layout(height=600,width=700, title='星評価ヒートマップ')
    st.plotly_chart(fig)

def get_aspectmap(reviews):
    reviews2 = reviews.copy()
    for i in range(len(reviews)):
        reviews2['年齢'][i] = int(reviews2['年齢'][i] / 10) * 10

    data2 = {'10' : 0, '20' : 1, '30' : 2, '40' : 3, '50' : 4, '60' : 5, '会社員/団体職員' : 6, 'パート/アルバイト' : 7, '自営業/個人事業主' : 8, '主婦/主夫' : 9, '学生' : 10, '契約社員/派遣社員' : 11,
            '会社役員/団体役員' : 12, '専門職(医師/弁護士/会計士/税理士等)' : 13, '退職された方' : 14, '公務員' : 15, '男性': 16, '女性' : 17}

    n = 0
    for k in data2.keys():
        d = {}
        d['emb'] = n
        for a in aspects:
            d[a] = {'positive' : 0, 'negative' : 0}
        data2[k] = d
        n += 1

    for v in reviews2['年齢'].unique():

        v_df = reviews2[reviews2['年齢'] == v]
        for a in aspects:
            data2[str(v)][a]['positive'] = len(v_df[v_df[a]=='positive'])
            data2[str(v)][a]['negative'] = len(v_df[v_df[a]=='negative'])

    for v in reviews2['性別'].unique():

        v_df = reviews2[reviews2['性別'] == v]
        for a in aspects:
            data2[str(v)][a]['positive'] = len(v_df[v_df[a]=='positive'])
            data2[str(v)][a]['negative'] = len(v_df[v_df[a]=='negative'])

    for v in reviews2['属性'].unique():

        v_df = reviews2[reviews2['属性'] == v]
        for a in aspects:
            data2[str(v)][a]['positive'] = len(v_df[v_df[a]=='positive'])
            data2[str(v)][a]['negative'] = len(v_df[v_df[a]=='negative'])


    a_m = np.zeros((18, 18))
    a_m_sub = np.zeros((18, 18))

    for i in range(len(reviews2)):
        age = reviews['年齢'][i]
        zokusei = reviews['属性'][i]
        seibetsu = reviews['性別'][i]
        age = str(10 * int(age / 10))

        d_a = data2[age]['emb']
        d_z = data2[zokusei]['emb']
        d_s = data2[seibetsu]['emb']

        for a in range(len(aspects)):
            s = reviews[aspects[a]][i]
            if s == 'positive':
                a_m[a, d_a] += 1 / (data2[age][aspects[a]]['positive'] + data2[age][aspects[a]]['negative'] + 1)
                a_m[a, d_s] += 1 / (data2[seibetsu][aspects[a]]['positive'] + data2[seibetsu][aspects[a]]['negative'] + 1)
                a_m[a, d_z] += 1 / (data2[zokusei][aspects[a]]['positive'] + data2[zokusei][aspects[a]]['negative'] + 1)

                a_m_sub[a, d_a] += 1 
                a_m_sub[a, d_s] += 1 
                a_m_sub[a, d_z] += 1 
            if s == 'negative':

                a_m_sub[a, d_a] += 1 
                a_m_sub[a, d_s] += 1 
                a_m_sub[a, d_z] += 1 

    a_m2 = a_m * 2 - 1
    for i in range(18):
        for j in range(18):
            if a_m_sub[i][j] == 0:
                a_m2[i][j] = None
    
    aspect_df = pd.DataFrame(data=a_m2, columns=columns, index=aspects_japanese)
    layout = Layout(plot_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Heatmap(z=aspect_df, x=aspect_df.columns, y=aspect_df.index, colorscale='blues'))
    fig.update_layout(height=800,width=700, title='星評価ヒートマップ')
    st.plotly_chart(fig)


