import streamlit as st
import pandas as pd
import plotly.express as px


st.title("My Spotify Dashboard")
st.write("Discover my listening habits, favourite artists, top tracks, and music trends over time 🎧🌷✨")

df = pd.read_csv("my_spotify_data/processed/spotify_data.csv", low_memory=False)

# Create tabs
tab1, tab2 = st.tabs(["My listening habits 🍀", "My music trends 🎧"])

# TAB 1 -------------
with tab1:
    # Overal metrics
    st.subheader("Overview")
    col1, col2, col3, col4 = st.columns(4)

    total_hours = round((df["minutes"].sum())/60)
    with col1:
        with st.container(border=True):
            st.metric(label="Total Listening Hours", value=total_hours)

    with col2:
        daily_listen = df.groupby("date")["minutes"].sum()
        avg_daily_listen = round(daily_listen.mean()/60, 2)
        with st.container(border=True):
            st.metric(label="Daily Listening Hours", value=avg_daily_listen)

    with col3:
            with st.container(border=True):
                unq_tracks = len(df["track_name"].unique())
                st.metric(label="Unique Tracks", value=unq_tracks)

    with col4:
                with st.container(border=True):
                    unq_artists = len(df["artist"].unique())
                    st.metric(label="Unique Artists", value=unq_artists)
    
    # Spotify analysis
    st.subheader("Listening habits")

    col5, col6 = st.columns(2)
    with col5:

        # Distribution of songs per year (unique songs)
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        song_analysis = df.groupby("year")["spotify_track_uri"].nunique().reset_index(name="num_songs")
        fig_song = px.bar(song_analysis, x="year", y="num_songs", title="Number Of Unique Songs Per Year")
        fig_song.update_layout(xaxis_title="Year", yaxis_title="Songs Count", showlegend = False)
        st.plotly_chart(fig_song)
        st.write("In general, I listened to the most songs during 2020 and 2021. Afterwards, there was a sharp decrease in my listening habits." \
        "However, my listening activity recovered in 2026.")

        # Distribution of devices
        device_analysis = df["device"].value_counts().reset_index()
        device_analysis.columns = ["device", "count"]
        fig_device = px.pie(device_analysis, names="device", values="count",
                            title="Listening by Device")
        st.plotly_chart(fig_device)
        fig_device.update_traces(domain=dict(x=[0, 0.8], y=[0, 0.8]))
        st.write("My most used device for Spotify is laptop/computer, following by phone/tablet. In contrast, I hardly listened to music on TV.")

        # Distribution of reasons to start
        rts_analysis = df["reason_start"].value_counts().reset_index(name="count")
        fig_rts = px.pie(rts_analysis, names="reason_start", values="count",
                            title="Reason to start analysis")
        fig_rts.update_traces(domain=dict(x=[0, 0.8], y=[0, 1]),textposition='inside')
        fig_rts.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
        st.plotly_chart(fig_rts)
        st.write("I mostly started the tracks automatically after the previous song finished (52.5\% of the time). Meanwhile, 32.5\% of the time, I manually picked songs from the playlist.")

    with col6:

        # Distribution of artists per year (unique artists)
        artist_analysis = df.groupby("year")["artist"].nunique().reset_index(name="num_artists")
        fig_artist = px.bar(artist_analysis, x="year", y="num_artists", title="Number Of Unique Artists Per Year")
        fig_artist.update_layout(xaxis_title="Year", yaxis_title="Artists Count", showlegend = False)
        st.plotly_chart(fig_artist)
        st.write("My artist discovery shows similar trends over time. I discovered the most artists " \
        "during 2020 and 2021, following by a significant decline. In 2026, my artist discovery trend gradually recovered.")

        # Distribution of time listening to music
        time_analysis = df["time_of_day"].value_counts().reset_index()
        time_analysis.columns = ["time_of_day", "count"]
        fig_time = px.pie(time_analysis, names="time_of_day", values="count",
                          title="Listening By Time of Day")
        fig_time.update_traces(domain=dict(x=[0, 0.85], y=[0, 1]))
        st.plotly_chart(fig_time)
        st.write("I listened to music the most during the day, such as morning and afternoon. Whereas, I hardly listened to music at night.")

        # Distribution of different modes
        shuffle_rate = df["shuffle"].value_counts(normalize=True)*100
        skipped_rate = df["skipped"].value_counts(normalize=True)*100
        mode_analysis = pd.DataFrame({"Shuffle":shuffle_rate, "Skipped":skipped_rate})
        mode_analysis = mode_analysis.T
        fig_mode = px.bar(mode_analysis, barmode="stack", y=[True, False], text_auto=".1f",
                          title="Mode analysis")
        fig_mode.update_layout(xaxis_title="Mode", yaxis_title="Percentage (%)", showlegend = True)
        st.plotly_chart(fig_mode)
        st.write("I used shuffle mode a lot while listening to music (46\% of the time). In addition, I preferred listening to music continously and rarely skipped songs, with 12\% of skipped rate.")
    pass

# TAB 2 -------------
with tab2:
    # Visualize listening counts over time

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
    fig2 = px.bar(top_artist, title="My Top 5 Artists During This Period")
    fig2.update_layout(xaxis_title="Artists", yaxis_title="Listens Count", showlegend = False)
    st.plotly_chart(fig2)

    # Add figure to display top songs over time (top 5)
    song_analysis = selected_df.groupby("track_name").size()
    top_song = song_analysis.sort_values(ascending=False)[:5]
    fig3 = px.bar(top_song, title="My Top 5 Songs During This Period")
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
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                    title="My Daily Activities During This Period")
    st.plotly_chart(fig4)
    pass
