import pandas as pd 
import fsspec
import streamlit as st
import json
import streamlit.components.v1 as components
import datetime

st.set_page_config(layout="wide",
                page_title="Pete's GGR Tracker",
                page_icon = ":sailboat:",
)


date_hour = datetime.datetime.today().strftime('%Y-%m-%d:%H') 

name_dic = {'Kirsten Neuschafer': 'Kirsten_Neuschafer',
            'Abhilash Tomy': 'Abhilash_Tomy'}


@st.cache()
def get_leaderboard(date_hour):
    data = []
    for name in names:
        file = f"s3://ggrtrackerlambdastack-ggrtrackingbucket9c362e67-ir6ft6ut6ucv/results/{name_dic[name]}.json"
        with fs.open(file, 'r') as f:
            data.append(pd.DataFrame(json.load(f), index = [name]))
    df = pd.concat(data).iloc[:,1:]
    df.columns = ['ETA', 'Estimated Time Elapsed', 'Finished']
    sortby = []
    for d in df['Estimated Time Elapsed']:
        sortby.append(pd.Timedelta(d).asm8)
    df['sort_col'] = sortby
    finished = []
    for i, name in enumerate(names):
        if df.iloc[i]['Finished'] == 'true':
            finished.append(True)
        else:
            finished.append(False)
    df['Finished'] = finished
    return df.sort_values('sort_col').iloc[:,:-1], date_hour

@st.cache()
def get_html(name, date_hour):
    file = f"s3://ggrtrackerlambdastack-ggrtrackingbucket9c362e67-ir6ft6ut6ucv/results/{name_dic[name]}.html"
    with fs.open(file, 'rb', encoding = 'utf-8') as f:
        HtmlFile = f.read()
    return HtmlFile, date_hour

@st.cache()
def get_roadbook(name, date_hour):
    file = f"s3://ggrtrackerlambdastack-ggrtrackingbucket9c362e67-ir6ft6ut6ucv/results/{name_dic[name]}.csv"
    with fs.open(file, 'r') as f:
        road_book = pd.read_csv(f)[['time', 'lat', 'lon', 'twd', 'tws', 'heading', 'twa','boat_speed', 'days_elapsed']]
    start = datetime.datetime(2022,9,4,16)
    current = datetime.datetime.strptime(road_book.time[0], '%Y-%m-%d %H:%M:%S')
    elapsed = current - start
    road_book.days_elapsed = road_book.days_elapsed + elapsed.days - round((12 - current.hour)/24,1)  #start was at 1200 UTC
    return road_book, date_hour


st.title(":blue[Pete's GGR Tracker] :earth_africa:")

st.write(':green[The Tracker will update at 8am UTC daily.]')

option = st.selectbox(
    'View:',
    ('Leaderboard', 'Routing Maps'),
    help = '')

fs = fsspec.filesystem('s3')
names = list(name_dic)

if option == 'Leaderboard':
    df, _ = get_leaderboard(date_hour)
    st.dataframe(df, use_container_width=True)
elif option == 'Routing Maps':
    team = st.selectbox(
                        'Team:',
                        names,
                        help = '')
    map = st.selectbox(
                    'Style:',
                    ('Routing Chart', 'Road Book'),
                    help = '')
    if map == 'Routing Chart':
        st.write('Please note these maps do not render nicely on mobile devices')
        HtmlFile, _ = get_html(team, date_hour)
        components.html(HtmlFile, height=900, scrolling = False)
        st.write(':blue[The weather displayed here is the latest 00z GFS forecast]')
    elif map == 'Road Book':
        road_book, _ = get_roadbook(team, date_hour)
        st.dataframe(road_book, use_container_width=True)
        st.write(":blue[I have taken a random guess at what a reasonable polar file is, if somebody has better data please share :) ]")

st.write('')
st.write(':blue[All times are UTC.]')
st.write('')

st.write(':red[This tracker has no affiliation with the GGR, or the YellowBrick tracker.]')


st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')

st.write('For any enquires contact me at petermarsh790@gmail.com')