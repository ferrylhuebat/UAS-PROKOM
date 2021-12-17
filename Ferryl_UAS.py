'''
Created on Dec 8, 2021
@author: adamz
'''

import json
import urllib

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

list_kodenegarahuruf = []
list_organisasi = []
list_nama = []
list_kodenegaraangka = []
list_region = []
list_subregion = []

url = "https://raw.githubusercontent.com/adamzainuri01/StreamlitProduksiMinyakNegara/main/kode_negara_lengkap.json"
response = urllib.request.urlopen(url)
file_json = json.loads(response.read())
df_csv = pd.read_csv(
    "https://raw.githubusercontent.com/adamzainuri01/StreamlitProduksiMinyakNegara/main/produksi_minyak_mentah.csv")
df_json = pd.DataFrame.from_dict(file_json, orient='columns')

# Membuat list kode negara dari df_csv
for i in list(df_csv['kode_negara']):
    if i not in list_kodenegarahuruf:
        list_kodenegarahuruf.append(i)

# Mencari organisasi/kumpulan negara pada list_kodenegarahuruf
for i in list_kodenegarahuruf:
    if i not in list(df_json['alpha-3']):
        list_organisasi.append(i)

# Menghilangkan organisasi/kumpulan negara dari df_csv
for i in list_organisasi:
    df_csv = df_csv[df_csv.kode_negara != i]
    if i in list_kodenegarahuruf:
        list_kodenegarahuruf.remove(i)

# Membuat beberapa list yang berisi informasi tentang nama negara, kode
# negara angka, region, dan sub-region dari tiap negara pada df_csv
for i in range(len(list_kodenegarahuruf)):
    for j in range(len(list(df_json['alpha-3']))):
        if list(df_json['alpha-3'])[j] == list_kodenegarahuruf[i] and list(df_json['name'])[j] not in list_nama:
            list_nama.append(list(df_json['name'])[j])
            list_kodenegaraangka.append(list(df_json['country-code'])[j])
            list_region.append(list(df_json['region'])[j])
            list_subregion.append(list(df_json['sub-region'])[j])

# Membuat dataframe dari list yang berisi informasi tiap negara pada df_csv
df_negara = pd.DataFrame(list(zip(list_nama, list_kodenegarahuruf, list_kodenegaraangka, list_region, list_subregion)), columns=[
                         'Negara', 'alpha-3', 'Kode_Negara', 'Region', 'Sub-Region'])

# Konfigurasi page pada streamlit
st.set_page_config(page_title='Produksi Minyak Negara',
                   layout='wide', page_icon=':oil_drum:')

# Header streamlit
t1, t2 = st.columns((0.07, 1))
t1.image('https://raw.githubusercontent.com/adamzainuri01/StreamlitProduksiMinyakNegara/main/images/logo_itb_1024.png', width=120)
title = '<p style="font-family: sans-serif; font-size: 40px; text-align: center;"><b>Analisis Data Produksi Minyak Mentah dari Berbagai Negara</b></p>'
t2.markdown(title, unsafe_allow_html=True)

# Option pada streamlit untuk memilih negara dari daftar negara
title1 = '<p style="color:#fe8062; font-size: 30px;">Grafik Jumlah Produksi Minyak Terhadap Waktu dari Suatu Negara</p>'
st.markdown(title1, unsafe_allow_html=True)
N = st.selectbox("Daftar Negara", list_nama)

for i in range(len(list_nama)):
    if list_nama[i] == N:
        kodenegarahuruf = list_kodenegarahuruf[i]
        kodenegaraangka = list_kodenegaraangka[i]
        region = list_region[i]
        subregion = list_subregion[i]

# Membuat list baru untuk menampung data produksi negara dan tahunnya
list_produksi = []
list_tahun = []

# Mengambil data produksi dan tahun berdasarkan negara yang dipilih pada
# option dan memasukkannya ke list yang telah dibuat
for i in range(len(list(df_csv['kode_negara']))):
    if kodenegarahuruf == list(df_csv['kode_negara'])[i]:
        list_produksi.append(list(df_csv['produksi'])[i])
        list_tahun.append(list(df_csv['tahun'])[i])

# Membuat grafik garis dengan x dari list_tahun dan y dari list_produksi
fig = px.line(x=list_tahun, y=list_produksi, labels={
              "x": "tahun", "y": "produksi"})
fig.update_traces(line_color='#fd6341')
fig.update_layout(margin=dict(l=0, r=10, b=0, t=30),
                  yaxis_title=None, xaxis_title=None)

# Menampilkan grafik pada streamlit
st.plotly_chart(fig, use_container_width=True)

# Membuat kolom pada page streamlit
tl1, tl2 = st.columns(2)
opt1, opt2, opt3 = st.columns((1, 1, 2))
cg1, cg2 = st.columns(2)

# Option pada streamlit untuk memilih tahun produksi minyak
title2 = '<p style="color:#fe8062; font-size: 23px;">Grafik Jumlah Produksi Minyak Terbesar pada Suatu Tahun</p>'
tl1.markdown(title2, unsafe_allow_html=True)
T = int(opt1.selectbox("Tahun", list_tahun))

# Membuat dataframe baru berdasarkan tahun yang dipilih dan diurutkan
# berdasarkan produksi minyak terbesar
df2 = df_csv.loc[df_csv['tahun'] == T].sort_values(
    by=['produksi'], ascending=False)

# Membuat list baru yang berisi nama negara berdasarkan data df2
list_nama_df2 = []

# Memasukkan nama negara dari df_negara ke list_nama_df2 berdasarkan data
# dari df2
for i in range(len(list(df2['kode_negara']))):
    for j in range(len(list(df_negara['alpha-3']))):
        if list(df2['kode_negara'])[i] == list(df_negara['alpha-3'])[j]:
            list_nama_df2.append(list(df_negara['Negara'])[j])

df2['negara'] = list_nama_df2

# Slider pada streamlit untuk memilih banyak negara yang akan tampil pada
# grafik
B1 = int(opt2.number_input("Banyak Negara", min_value=1, max_value=len(df2)))

df2 = df2[:B1]

# Membuat grafik batang jumlah produksi minyak terbesar pada tahun T
fig2 = px.bar(df2, x='negara', y='produksi', template='seaborn')
fig2.update_traces(marker_color='#fe8062')
fig2.update_layout(margin=dict(l=0, r=10, b=0, t=30),
                   yaxis_title=None, xaxis_title=None)

# Menampilkan grafik pada streamlit berdasarkan kolom yang telah dibuat
cg1.plotly_chart(fig2, use_container_width=True)

# Membuat list baru untuk menampung data produksi minyak kumulatif tiap negara
list_sum = []

# Membuat list baru yang berisi nama negara berdasarkan data df3
list_nama_df3 = []

# Menjumlahkan produksi minyak tiap negara dan memasukkannya ke list_sum
for i in list_kodenegarahuruf:
    a = df_csv.loc[df_csv['kode_negara'] == i, 'produksi'].sum()
    list_sum.append(a)

# Membuat dataframe baru dan diurutkan berdasarkan produksi kumulatif
# minyak terbesar
df3 = pd.DataFrame(list(zip(list_kodenegarahuruf, list_sum)),
                   columns=['kode_negara', 'produksi_kumulatif']).sort_values(by=['produksi_kumulatif'], ascending=False)

# Memasukkan nama negara dari df_negara ke list_nama_df3 berdasarkan data
# dari df3
for i in range(len(list(df3['kode_negara']))):
    for j in range(len(list(df_negara['alpha-3']))):
        if list(df3['kode_negara'])[i] == list(df_negara['alpha-3'])[j]:
            list_nama_df3.append(list(df_negara['Negara'])[j])

df3['negara'] = list_nama_df3

# Slider pada streamlit untuk memilih banyak negara yang akan tampil pada
# grafik
title3 = '<p style="color:#fe8062; font-size: 23px;">Grafik Jumlah Produksi Kumulatif Minyak Terbesar</p>'
tl2.markdown(title3, unsafe_allow_html=True)
B2 = int(opt3.number_input("Banyak Negara", min_value=1,
                           max_value=len(df3), key="kumulatif"))

df3 = df3[:B2]

# Membuat grafik batang jumlah produksi minyak kumulatif terbesar
fig3 = px.bar(df3, x='negara', y='produksi_kumulatif', template='seaborn')
fig3.update_traces(marker_color='#fe8062')
fig3.update_layout(margin=dict(l=0, r=10, b=0, t=30),
                   yaxis_title=None, xaxis_title=None)

# Menampilkan grafik pada streamlit berdasarkan kolom yang telah dibuat
cg2.plotly_chart(fig3, use_container_width=True)

# Option pada streamlit untuk memilih tahun produksi minyak
title4 = '<p style="color:#fe8062; font-size: 30px;">Informasi Produksi Minyak Negara</p>'
st.markdown(title4, unsafe_allow_html=True)
T2 = int(st.selectbox("Tahun", list_tahun, key="Tahun"))

# Membuat dataframe baru dari df_csv berdasarkan tahun yang dipilih
df4 = df_csv.loc[df_csv['tahun'] == T2]
df4 = df4.drop(['tahun'], axis=1)
df4 = df4.rename(columns={
                 'produksi': 'produksi_tahun-{}'.format(T2), 'kode_negara': 'kode_negara_huruf'})

# Membuat list baru untuk menampung informasi negara berdasarkan df4
list_kodenegaraangka_df4 = []
list_nama_df4 = []
list_region_df4 = []
list_subregion_df4 = []

# Membuat beberapa list yang berisi informasi tentang nama negara, kode
# negara angka, region, dan sub-region dari tiap negara pada df4
for i in range(len(list(df4['kode_negara_huruf']))):
    for j in range(len(list(df_negara['alpha-3']))):
        if list(df4['kode_negara_huruf'])[i] == list(df_negara['alpha-3'])[j]:
            list_kodenegaraangka_df4.append(list(df_negara['Kode_Negara'])[j])
            list_nama_df4.append(list(df_negara['Negara'])[j])
            list_region_df4.append(list(df_negara['Region'])[j])
            list_subregion_df4.append(list(df_negara['Sub-Region'])[j])

# Membuat kolom baru pada df4 yang berisikan data dari list yang telah dibuat
df4['nama'] = list_nama_df4
df4['region'] = list_region_df4
df4['sub-region'] = list_subregion_df4
df4['kode_negara_angka'] = list_kodenegaraangka_df4

# Definisi ulang df4 dengan tambahan kolom baru dan diurutkan berdasarkan
# produksi pada tahun yang dipilih
df4 = df4[['nama', 'kode_negara_huruf', 'kode_negara_angka', 'region',
           'sub-region', 'produksi_tahun-{}'.format(T2)]].sort_values(by=['produksi_tahun-{}'.format(T2)], ascending=False)

# Membuat dataframe baru yang berisi produksi kumulatif minyak negara
df5 = pd.DataFrame(list(zip(list_kodenegarahuruf, list_sum)),
                   columns=['kode_negara_huruf', 'produksi_kumulatif'])

# Membuat kolom baru pada df5 yang berisikan data dari list yang telah dibuat
df5['nama'] = list(df_negara['Negara'])
df5['region'] = list(df_negara['Region'])
df5['sub-region'] = list(df_negara['Sub-Region'])
df5['kode_negara_angka'] = list(df_negara['Kode_Negara'])

# Definisi ulang df5 dengan tambahan kolom baru dan diurutkan berdasarkan
# produksi kumulatif
df5 = df5[['nama', 'kode_negara_huruf', 'kode_negara_angka', 'region',
           'sub-region', 'produksi_kumulatif']].sort_values(by=['produksi_kumulatif'], ascending=False)
