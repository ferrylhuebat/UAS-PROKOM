#Ferryl Ananda W P
#12220151

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import json

list_codeletter = []                   #daftar list
list_codenum = []
list_organization = []
list_name = []
list_region = []
list_subregion = []


response = open("kode_negara_lengkap.json")
file_json = json.loads(response.read())
df_csv = pd.read_csv("produksi_minyak_mentah.csv")
df_json = pd.DataFrame.from_dict(file_json, orient='columns')

for i in list(df_csv['kode_negara']):                   #list kode negara dari df_csv
    if i not in list_codeletter:
        list_codeletter.append(i)

for i in list_codeletter:                               #kumpulan negara pada list_codeletter
    if i not in list(df_json['alpha-3']):
        list_organization.append(i)

for i in list_organization:                             #Delete kumpulan negara dari df_csv
    df_csv = df_csv[df_csv.kode_negara != i]
    if i in list_codeletter:
        list_codeletter.remove(i)

#Membuat list yang berisi informasi tentang nama negara, kode negara angka, region, dan sub-region dari tiap negara pada df_csv
for i in range(len(list_codeletter)):
    for j in range(len(list(df_json['alpha-3']))):
        if list(df_json['alpha-3'])[j] == list_codeletter[i] and list(df_json['name'])[j] not in list_name:
            list_name.append(list(df_json['name'])[j])
            list_codenum.append(list(df_json['country-code'])[j])
            list_region.append(list(df_json['region'])[j])
            list_subregion.append(list(df_json['sub-region'])[j])

# Membuat dataframe dari list yang isinya informasi tiap negara
df_negara = pd.DataFrame(list(zip(list_name, list_codeletter, list_codenum, list_region, list_subregion)), columns=[
                         'Negara', 'alpha-3', 'Kode_Negara', 'Region', 'Sub-Region'])

st.set_page_config(page_title='UAS Prokom Ferryl 12220151', layout='wide'')

title = '<p style="font-family: sans-serif; font-size: 40px; text-align: center;"><b>Produksi Minyak Mentah</b></p>'
st.markdown(title, unsafe_allow_html=True)

# Option pada streamlit untuk memilih negara dari daftar negara
N = st.sidebar.selectbox("Daftar Negara", list_name)

for i in range(len(list_name)):
    if list_name[i] == N:
        kodenegarahuruf = list_codeletter[i]
        kodenegaraangka = list_codenum[i]
        region = list_region[i]
        subregion = list_subregion[i]

list_production = []              #LNew list
list_year = []

# Mengambil data produksi dan tahun berdasarkan negara yang dipilih pada option dan memasukkannya ke list yang telah dibuat
for i in range(len(list(df_csv['kode_negara']))):
    if kodenegarahuruf == list(df_csv['kode_negara'])[i]:
        list_production.append(list(df_csv['produksi'])[i])
        list_year.append(list(df_csv['tahun'])[i])

fig = px.line(x=list_year, y=list_production, labels={          # Membuat grafik garis dengan x dari list_year dan y dari list_production
              "x": "tahun", "y": "produksi"})
fig.update_traces(line_color='#fd6341')
fig.update_layout(margin=dict(l=0, r=10, b=0, t=30),
                  yaxis_title=None, xaxis_title=None)

st.plotly_chart(fig, use_container_width=True)          #Menampilkan grafik pada streamlit
tl1, tl2 = st.columns(2)                                #kolom pada page streamlit
cg1, cg2 = st.columns(2)

# Option pada streamlit untuk memilih tahun produksi minyak
title2 = '<p style="color:#62fee9; font-size: 25px;">Grafik Jumlah Produksi Minyak Terbesar pada Suatu Tahun</p>'
tl1.markdown(title2, unsafe_allow_html=True)
T = int(st.sidebar.selectbox("Tahun", list_year))

# Membuat dataframe baru berdasarkan tahun yang dipilih dan diurutkan berdasarkan produksi minyak terbesar
df2 = df_csv.loc[df_csv['tahun'] == T].sort_values(
    by=['produksi'], ascending=False)

list_name_df2 = []              # Membuat list baru yang berisi nama negara berdasarkan data df2

for i in range(len(list(df2['kode_negara']))):              # Memasukkan nama negara dari df_negara ke list_name_df2 berdasarkan data dari df2
    for j in range(len(list(df_negara['alpha-3']))):
        if list(df2['kode_negara'])[i] == list(df_negara['alpha-3'])[j]:
            list_name_df2.append(list(df_negara['Negara'])[j])

df2['negara'] = list_name_df2

# Slider pada streamlit untuk memilih banyak negara yang akan tampil pada grafik
B1 = int(st.sidebar.number_input("Banyak Negara", min_value=1, max_value=len(df2)))

df2 = df2[:B1]
fig2 = px.bar(df2, x='negara', y='produksi', template='seaborn')    # Membuat grafik batang jumlah produksi minyak terbesar pada tahun T
fig2.update_traces(marker_color='#62fee9')
fig2.update_layout(margin=dict(l=0, r=10, b=0, t=30),
                   yaxis_title=None, xaxis_title=None)

# Menampilkan grafik pada streamlit berdasarkan kolom yang telah dibuat
cg1.plotly_chart(fig2, use_container_width=True)

list_sum = []                   # Membuat list baru untuk menampung data produksi minyak kumulatif tiap negara
list_name_df3 = []              # Membuat list baru yang berisi nama negara berdasarkan data df3

for i in list_codeletter:       # Menjumlahkan produksi minyak tiap negara dan memasukkannya ke list_sum
    a = df_csv.loc[df_csv['kode_negara'] == i, 'produksi'].sum()
    list_sum.append(a)

#dataframe baru dan diurutkan berdasarkan produksi kumulatif minyak terbesar
df3 = pd.DataFrame(list(zip(list_codeletter, list_sum)),
                   columns=['kode_negara', 'produksi_kumulatif']).sort_values(by=['produksi_kumulatif'], ascending=False)

#Memasukkan nama negara dari df_negara ke list_name_df3 berdasarkan data dari df3
for i in range(len(list(df3['kode_negara']))):
    for j in range(len(list(df_negara['alpha-3']))):
        if list(df3['kode_negara'])[i] == list(df_negara['alpha-3'])[j]:
            list_name_df3.append(list(df_negara['Negara'])[j])

df3['negara'] = list_name_df3

#Slider pada streamlit untuk memilih banyak negara yang akan tampil padagrafik
title3 = '<p style="color:#fe8062; font-size: 23px;">Grafik Jumlah Produksi Kumulatif Minyak Terbesar</p>'
tl2.markdown(title3, unsafe_allow_html=True)

df3 = df3[:B1]

fig3 = px.bar(df3, x='negara', y='produksi_kumulatif', template='seaborn')          #grafik bar jumlah produksi minyak kumulatif terbesar
fig3.update_traces(marker_color='#fe8062')
fig3.update_layout(margin=dict(l=0, r=10, b=0, t=30),
                   yaxis_title=None, xaxis_title=None)

cg2.plotly_chart(fig3, use_container_width=True)                                    #Menampilkan grafik di streamlit berdasarkan kolom

title4 = '<p style="color:#62fee9; font-size: 30px;">Informasi Produksi Minyak Negara</p>'      #Option streamlit untuk memilih tahun produksi minyak
st.markdown(title4, unsafe_allow_html=True)

df4 = df_csv.loc[df_csv['tahun'] == T]                                             # Membuat dataframe baru dari df_csv berdasarkan tahun yang dipilih
df4 = df4.drop(['tahun'], axis=1)
df4 = df4.rename(columns={
                 'produksi': 'produksi_tahun-{}'.format(T), 'kode_negara': 'kode_negara_huruf'})

list_codenum_df4 = []                                       #list baru untuk menampung informasi negara berdasarkan df4
list_name_df4 = []
list_region_df4 = []
list_subregion_df4 = []

# Membuat beberapa list yang berisi informasi tentang nama negara, kode negara angka, region, dan sub-region dari tiap negara pada df4
for i in range(len(list(df4['kode_negara_huruf']))):
    for j in range(len(list(df_negara['alpha-3']))):
        if list(df4['kode_negara_huruf'])[i] == list(df_negara['alpha-3'])[j]:
            list_codenum_df4.append(list(df_negara['Kode_Negara'])[j])
            list_name_df4.append(list(df_negara['Negara'])[j])
            list_region_df4.append(list(df_negara['Region'])[j])
            list_subregion_df4.append(list(df_negara['Sub-Region'])[j])

df4['nama'] = list_name_df4                         # Membuat kolom baru pada df4 yang berisikan data dari list yang telah dibuat
df4['region'] = list_region_df4
df4['sub-region'] = list_subregion_df4
df4['kode_negara_angka'] = list_codenum_df4

#Mendefinisikan ulang df4 dengan kolom baru dan diurutkan berdasarkan produksi pada tahun yang dipilih
df4 = df4[['nama', 'kode_negara_huruf', 'kode_negara_angka', 'region',
           'sub-region', 'produksi_tahun-{}'.format(T)]].sort_values(by=['produksi_tahun-{}'.format(T)], ascending=False)

df5 = pd.DataFrame(list(zip(list_codeletter, list_sum)),             #dataframe baru berisi produksi kumulatif minyak negara
                   columns=['kode_negara_huruf', 'produksi_kumulatif'])

df5['nama'] = list(df_negara['Negara'])                              #kolom baru pada df5 yang berisikan data dari list yang telah dibuat
df5['region'] = list(df_negara['Region'])
df5['sub-region'] = list(df_negara['Sub-Region'])
df5['kode_negara_angka'] = list(df_negara['Kode_Negara'])

#Mendefinisikan ulang df5 dengan tambahan kolom baru dan diurutkan berdasarkan produksi kumulatif
df5 = df5[['nama', 'kode_negara_huruf', 'kode_negara_angka', 'region',
           'sub-region', 'produksi_kumulatif']].sort_values(by=['produksi_kumulatif'], ascending=False)

#dataframe baru dari df4 dengan menghilangkan data bernilai 0 dan diurutkan berdasarkan produksi dari yang terkecil
df_nozero = df4[df4['produksi_tahun-{}'.format(T)] != 0].sort_values(
    by=['produksi_tahun-{}'.format(T)], ascending=True)

#Membuat dataframe baru dari df5 dengan menghilangkan data bernilai 0 dan diurutkan berdasarkan produksi kumulatif dari yang terkecil
df_minproduksikumulatif = df5[df5['produksi_kumulatif'.format(T)] != 0].sort_values(
    by=['produksi_kumulatif'], ascending=True)

#Membuat kolom pada page streamlit
col1, col2 = st.columns(2)

#Menampilkan data berdasarkan kolom yang telah dibuat
with col1:
    st.write("Produksi Minyak Terbesar Tahun {}".format(     
        T), df4.iloc[0]['produksi_tahun-{}'.format(T)])
    # Caption untuk menampilkan informasi mengenai negara pada metric
    st.markdown("Negara: {}  \nKode Negara: {} {}  \nRegion: {}  \nSub-Region: {}".format(
        df4.iloc[0]['nama'], df4.iloc[0]['kode_negara_huruf'], df4.iloc[0]['kode_negara_angka'], df4.iloc[0]['region'], df4.iloc[0]['sub-region']))
    st.write("Produksi Minyak Terkecil Tahun {}".format(        
        T), df_nozero.iloc[0]['produksi_tahun-{}'.format(T)])
    st.markdown("Negara: {}  \nKode Negara: {} {}  \nRegion: {}  \nSub-Region: {}".format(        # Caption untuk menampilkan informasi mengenai negara pada metric
        df_nozero.iloc[0]['nama'], df_nozero.iloc[0]['kode_negara_huruf'], df_nozero.iloc[0]['kode_negara_angka'], df_nozero.iloc[0]['region'], df_nozero.iloc[0]['sub-region']))
with col2:
    st.write("Produksi Minyak Kumulatif Terbesar",              
              round(df5.iloc[0]['produksi_kumulatif'], 3))
    st.markdown("Negara: {}  \nKode Negara: {} {}  \nRegion: {}  \nSub-Region: {}".format(       # Caption untuk menampilkan informasi mengenai negara pada metric
        df5.iloc[0]['nama'], df5.iloc[0]['kode_negara_huruf'], df5.iloc[0]['kode_negara_angka'], df5.iloc[0]['region'], df5.iloc[0]['sub-region']))
    st.write("Produksi Minyak Kumulatif Terkecil",             
              df_minproduksikumulatif.iloc[0]['produksi_kumulatif'])
    # Caption untuk menampilkan informasi mengenai negara pada metric
    st.markdown("Negara: {}  \nKode Negara: {} {}  \nRegion: {}  \nSub-Region: {}".format(df_minproduksikumulatif.iloc[0]['nama'], df_minproduksikumulatif.iloc[0][
        'kode_negara_huruf'], df_minproduksikumulatif.iloc[0]['kode_negara_angka'], df_minproduksikumulatif.iloc[0]['region'], df_minproduksikumulatif.iloc[0]['sub-region']))
