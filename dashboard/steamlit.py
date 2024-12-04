import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load data
@st.cache
def load_data():
    day_data = pd.read_csv("dashboard/clean_day.csv")
    hour_data = pd.read_csv("dashboard/clean_hour.csv")
    return day_data, hour_data

# Map seasons and years for better readability
#def preprocess_data(day_data, hour_data):
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    year_mapping = {0: 2011, 1: 2012}

    day_data['season'] = day_data['season'].map(season_mapping)
    day_data['yr'] = day_data['yr'].map(year_mapping)

    hour_data['season'] = hour_data['season'].map(season_mapping)
    hour_data['yr'] = hour_data['yr'].map(year_mapping)

    return day_data, hour_data

# Visualization for Question 1
def plot_seasonal_patterns(day_data):
    seasonal_data = day_data.groupby(['season', 'yr'])['cnt'].agg(['mean', 'sum']).reset_index()

    # Bar plot
    st.subheader("Pola Musiman dalam Penyewaan Sepeda (Perbandingan Tahunan)")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=seasonal_data, x='season', y='mean', hue='yr', palette='coolwarm')
    plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Musim dan Tahun")
    plt.xlabel("Musim")
    plt.ylabel("Rata-Rata Penyewaan (cnt)")
    plt.legend(title="Tahun")
    st.pyplot(plt)

    # Line plot
    st.subheader("Total Penyewaan Sepeda Berdasarkan Musim dan Tahun")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=seasonal_data, x='season', y='sum', hue='yr', marker='o', palette='coolwarm')
    plt.title("Total Penyewaan Sepeda Berdasarkan Musim dan Tahun")
    plt.xlabel("Musim")
    plt.ylabel("Total Penyewaan (cnt)")
    plt.legend(title="Tahun")
    st.pyplot(plt)

    st.subheader("Penyewaan Sepeda Harian berdasarkan Musim dan Tahun")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=day_data, x='season', y='cnt', hue='yr', palette='coolwarm')
    plt.title("Penyewaan Sepeda Harian berdasarkan Musim dan Tahun")
    plt.xlabel("Musim")
    plt.ylabel("Total Penyewaan (cnt)")
    plt.legend(title="Tahun")
    st.pyplot(plt)

# Visualization for Question 2
def plot_hourly_patterns(hour_data):
    hourly_trends = hour_data.groupby(['hr', 'season', 'yr'])['cnt'].mean().reset_index()

    # Line plot
    st.subheader("Penyewaan Sepeda Per Jam Berdasarkan Musim dan Tahun")
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=hourly_trends, x='hr', y='cnt', hue='season', style='yr', markers=True, palette='coolwarm')
    plt.title("Penyewaan Sepeda Per Jam Berdasarkan Musim dan Tahun")
    plt.xlabel("Jam dalam sehari")
    plt.ylabel("Rata-Rata Penyewaan (cnt)")
    plt.legend(title="Musim-Tahun", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt)

    # Line plots for individual seasons
    for season in hourly_trends['season'].unique():
        st.subheader(f"Sewa Per Jam di {season} (Perbandingan berdasarkan Tahun)")
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=hourly_trends[hourly_trends['season'] == season],
                     x='hr', y='cnt', hue='yr', marker='o', palette='coolwarm')
        plt.title(f"Penyewaan Sepeda Per Jam di {season} berdasarkan Tahun")
        plt.xlabel("Jam dalam sehari")
        plt.ylabel("Rata-Rata Penyewaan (cnt)")
        plt.legend(title="Tahun")
        st.pyplot(plt)

# Streamlit App Layout
st.title("Analisis Penyewaan Sepeda")
st.markdown("""
Aplikasi ini menganalisis dataset bike-sharing untuk mengungkap tren musiman dan per jam dalam permintaan penyewaan sepeda.
Anda dapat menjelajah:
1. **Pola musiman dalam permintaan penyewaan sepeda dan variasinya berdasarkan tahun.**
2. **Pola penyewaan sepeda per jam selama musim yang berbeda dan bagaimana variasinya dari tahun ke tahun.**
""")

# Load and preprocess data
day_data, hour_data = load_data()
#day_data, hour_data = preprocess_data(day_data, hour_data)

# Navigation
question = st.sidebar.radio(
    "Pilih Analisis:",
    ("Pola Musiman dalam Penyewaan", "Pola Penyewaan Per Jam")
)

if question == "Pola Musiman dalam Penyewaan":
    plot_seasonal_patterns(day_data)
elif question == "Pola Penyewaan Per Jam":
    plot_hourly_patterns(hour_data)
