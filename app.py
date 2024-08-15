import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
df_region = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, df_region)


st.sidebar.title("OLYMPICS ANALYSIS")
st.sidebar.image("https://miro.medium.com/v2/resize:fit:3600/1*2g_uOUQmzmj_02Uh71hYtQ.png")

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f'Medal Tally in {selected_year} Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f'Overall Performance of {selected_country}')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f'Performance of {selected_country} in {selected_year}')

    st.table(medal_tally)

if user_menu == 'Overall Analysis' :
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Event')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Year", y="count")
    st.title('Participating Nations over the Years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time,x='Year', y='count')
    st.title('Number of Events over the years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time,x='Year', y='count')
    st.title('Number of Athletes over the years')
    st.plotly_chart(fig)

    st.title('Number of events over time in Every sport')
    fig, axis = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event',
                                   aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Sports list', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(f'Medal Tally of {selected_country} over the years')
    st.plotly_chart(fig)

    st.title(f'{selected_country} excels in the following sports')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, axis = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title(f'Most Successful Athletes from {selected_country}')
    x = helper.most_successful_athletes(df, selected_country)
    st.table(x)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    famous_sports = ['Basketball', 'Football', 'Athletics',
                     'Swimming', 'Badminton', 'Gymnastics', 'Weightlifting',
                     'Wrestling', 'Hockey', 'Rowing', 'Shooting', 'Boxing',
                     'Taekwondo', 'Cycling', 'Diving', 'Tennis', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby', 'Figure Skating']

    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age of winners with respect to sport')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Sports list', sport_list)
    temp_df = helper.height_weight_comp(df, selected_sport)
    fig, axis = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Height'], y=temp_df['Weight'], hue=temp_df['Medal'], style=temp_df['Sex'])
    st.title(f'Height-Weight comparison for {selected_sport}')
    st.pyplot(fig)

    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    st.title('Men vs Women participation over the years')
    st.plotly_chart(fig)







