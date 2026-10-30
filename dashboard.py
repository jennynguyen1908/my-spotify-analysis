import streamlit as st
import pandas as pd
import plotly.express as px


st.title("My Spotify Dashboard")
st.write("Discover my listening habits, favourite artists, top tracks, and music trends over time 🎧🌷✨")

df = pd.read_csv("my_spotify_data/processed/spotify_data.csv", low_memory=False)

# Visualize listening counts over time
df["date"] = pd.to_datetime(df["date"])

# Create slider
start_year, end_year = st.slider(
    "Select time period:", min_value=2019, max_value=2026, value=(2019,2026))

# Filter data based on selected years
selected_df = df[(df["date"].dt.year >= start_year) & 
                 (df["date"].dt.year <= end_year)]

# Add figure to display music trend over time
music_over_time = selected_df.set_index("date").resample("W").size().reset_index(name="listens")
fig1 = px.line(music_over_time, x="date", y="listens",
              title="My Spotify Listening Trends Over Time")
fig1.update_layout(xaxis_title="Periods", yaxis_title="Listens Count")
st.plotly_chart(fig1)

# Add figure to display top artists over time (top 5)
artist_analysis = selected_df.groupby("artist").size()
top_artist = artist_analysis.sort_values(ascending=False)[:5]
fig2 = px.bar(top_artist, title="My Top 5 Artists")
fig2.update_layout(xaxis_title="Artists", yaxis_title="Listens Count", showlegend = False)
st.plotly_chart(fig2)

# Add figure to display top songs over time (top 5)
song_analysis = selected_df.groupby("track_name").size()
top_song = song_analysis.sort_values(ascending=False)[:5]
fig3 = px.bar(top_song, title="My Top 5 Songs")
fig3.update_layout(xaxis_title="Songs", yaxis_title="Listens Count", showlegend=False)
st.plotly_chart(fig3)

# Add heatmap to listening counts
selected_df["month"] = selected_df["date"].dt.month
selected_df["weekday"] = selected_df["date"].dt.day_name()

daily_listen = selected_df.groupby(["weekday", "month"]).size().reset_index(name="listens")
heatmap_data = daily_listen.pivot(
    index="weekday", columns="month", values="listens"
)
heatmap_data = heatmap_data.reindex([
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
])

heatmap_data = heatmap_data.reindex(columns=range(1, 13))
fig4 = px.imshow(heatmap_data,
                 labels={"x":"Month", "y":"Weekday", "color":"Listening Count"},
                 x=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
st.plotly_chart(fig4)