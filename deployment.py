import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sn
import time
from matplotlib import pyplot as plt
import plotly.express as px
from config import api_key


channel_ids=['UCn3YGmLvUXFkHIT9_z4mRTQ',    #Neeti Mohan
'UCZRdNleCgW-BGUJf-bbjzQg',                 #Diljit Dosanjh
'UCnrG75VRwdlp2wtwfpOCBRQ',                 #Sanam
'UCigV1clokmoz4LZrGL9fRNw',                #Hansraj
'UC1GBYS8_8cXRDM3yOYHeyWw',                #Armaan Malik
'UCicMnWThgzNjUmqpd-nUTXQ',                #Neha kakkar
'UCF4uIIqbIy05Cmzx3rRt_8g',                 #Atif Aslam
'UCzqQvVAkCEFrWI2VOPzFpeg']                  #Jubin Nautiyal

youtube=build('youtube','v3',developerKey=api_key)

# MULTIPLE ID'S
def get_multi_channel_stats(youtube,channel_ids):
    all_data=[]
    request = youtube.channels().list(part="snippet,contentDetails,statistics",id=','.join(channel_ids))
    response = request.execute()
    # return response
    for i in range(len(response['items'])):
        data=dict(Channel_name=response['items'][i]['snippet']['title'],
                subscribers=response['items'][i]['statistics']['subscriberCount'],
                Views=response['items'][i]['statistics']['viewCount'],
                total_videoes=response['items'][i]['statistics']['videoCount'],
                playlist_id_link=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])

        all_data.append(data)
    return all_data


##Single id
def get_single_channel_stats(youtube,channel_id):
    request = youtube.channels().list(part="snippet,contentDetails,statistics",id=channel_id)
    response = request.execute()
    # return response
    data=dict(Channel_name=response['items'][0]['snippet']['title'],
    # Channel_Description=response['items'][0]['snippet']['description'],
    # custom_url=response['items'][0]['snippet']['customUrl'],                                            
    subscribers=response['items'][0]['statistics']['subscriberCount'],
    Views=response['items'][0]['statistics']['viewCount'],
    total_videoes=response['items'][0]['statistics']['videoCount'],
    playlist_id_link=response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])

    return data

#Extracting Video details from playlist id
def get_video_ids(youtube,playlist_id):
    request=youtube.playlistItems().list(part='contentDetails',playlistId=playlist_id,maxResults=50)
    response=request.execute()
    # return response
    video_ids=[]

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
    return video_ids

def get_vdo_details(youtube,video_ids):
    all_video_stats=[]
    request=youtube.videos().list(part="snippet,statistics",id=video_ids)
    response=request.execute()
    # return response
    for video in response['items']:
        video_stats=dict(Title=video['snippet']['title'],
                    # Published_date=video['snippet']['publishedAt'],
                    Likes=video['statistics']['likeCount'],
                    Comments=video['statistics']['commentCount'],
                    Views=video['statistics']['viewCount'])
        all_video_stats.append(video_stats)

    return all_video_stats

def plot_videoes(video_df):
        st.subheader("Videoes Graph")
        fig,ax=plt.subplots(figsize=(15,10))
        ax.scatter(video_df['Title'],video_df["Likes"])
        # st.pyplot(fig, width='0.1')
        st.pyplot()

def analyze(name,cid):    
    this=get_single_channel_stats(youtube,cid)   
    a,b=st.columns(2)
    with a:
        st.subheader("Channel Name")
        st.markdown(f"{this['Channel_name']}")
    # st.subheader("Channel Description")
    with b:
    # st.markdown(f"{this['Channel_Description']}")
    #   st.subheader("Custom URL")
    # st.markdown(f"{this['custom_url']}")
        st.subheader("Total no. of Subscribers")
        st.markdown(f"{this['subscribers']}")
    a,b=st.columns(2)
    with a:
        st.subheader("Views Count")
        st.markdown(f"{this['Views']}")
    with b:
        st.subheader("Total Videoes") 
        st.markdown(f"{this['total_videoes']}")

    pid=this['playlist_id_link'] 

    video_ids=get_video_ids(youtube,pid)

    videoes_stats=get_vdo_details(youtube,video_ids)
    # for i in videoes_stats['Title']:
    #     i.str.split('|')

    video_df=pd.DataFrame(videoes_stats)
    st.subheader("\n Video Stats: ")
    st.dataframe(video_df)
    
    # Modification of data types
    # video_df['Published_date']=pd.to_numeric(video_df['Published_date']).dt.date
    video_df['Views']=pd.to_numeric(video_df['Views'])
    video_df['Likes']=pd.to_numeric(video_df['Likes'])
    video_df['Comments']=pd.to_numeric(video_df['Comments'])

    def show_most_liked_vdo(video_df):
        temp=video_df.sort_values(by='Likes',ascending=False).head()["Title"]
        temp
    def show_most_viewed_vdo():
        temp=video_df.sort_values(by='Views',ascending=False).head()["Title"]
        temp
    def show_most_commented_vdo():
        temp=video_df.sort_values(by='Comments',ascending=False).head()["Title"]
        temp
        
    # def show_most_commented_video(video_df):
    #     most_commented_df=video_df.sort_values(by='Comments').head()
    #     st.dataframe(most_commented_df[:,1:])
    st.subheader("Top 5 most Liked Videoes")
    show_most_liked_vdo(video_df)             #function calling     

    st.subheader("\n Top 5 most Viewed Videoes")      
    show_most_viewed_vdo()

    st.subheader("\n Top 5 most Commented Videoes")    
    show_most_commented_vdo()



def home():
    st.image("ytl.png")
    st.title("Singers Analysis")
    a,b,c,d=st.columns(4)
    with a:
        st.image("Sanam Puri.jpeg")
    with b:
        st.image("Neeti Mohan.jpeg")
    with c:
        st.image("Hansraj Raghuwanshi.jpeg")
    with d:
        st.image("Diljit Dosanjh.jpeg")
    a,b,c,d=st.columns(4)
    with a:
        st.image("Jubin Nautiyal.jpeg")
    with b:
        st.image("Armaan Malik.jpeg")
    with c:
        st.image("Atif Aslam.jpeg")
    with d:
        st.image("Neha Kakkar.jpeg")
    
    st.markdown("YouTube analytics provides a range of metrics that singers can use to track the performance of their videos. These metrics include views, watch time, engagement, and demographic data.")
    st.markdown("By analyzing these metrics, singers can make informed decisions about their content strategy, identify their audience, and create content that resonates with them. The insights provided by YouTube analytics can help singers to increase their reach, engagement, and overall success on the platform.")
  

    
 



def plots(type):
        st.subheader(f"Channel Name VS {type}")
        # fig,ax=plt.subplots(figsize=(6,4))
        # ax.barh(comp_df['Channel_name'],comp_df[type],color=['blue','black','#A890F0','red','green','#6890F0','purple',"#a9f971"])

        # # st.pyplot(fig, width='0.1')
        # st.pyplot()

    # Create a horizontal bar chart using Plotly Express
        fig = px.bar(comp_df, x=type, y='Channel_name', color=type, orientation='h',color_discrete_sequence=["#a9f971"])

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

                                  
#--------USER-----------           
choice=st.sidebar.radio("Go To -",('HOME 🏠','SELECT ARTIST 🎤','ALL ARTIST STATS'))
if choice == 'HOME 🏠':
    home()
elif choice=="SELECT ARTIST 🎤":
    st.sidebar.title("Select Artist")
    artist_name=st.sidebar.selectbox("",['Sanam Puri','Neeti Mohan','Hansraj Raghuwanshi','Diljit Dosanjh',"Neha kakkar","Armaan Malik","Atif Aslam","Jubin Nautiyal"])
                
    analyze_btn=st.sidebar.button("Analyse Artist Channel")
    
    if analyze_btn:
        st.title(artist_name)
        # st.image(f"{artist_name}.jpeg")

        if artist_name=="Sanam Puri":
            cid=channel_ids[2]
        elif artist_name=="Neeti Mohan":
            cid=channel_ids[0]
        elif artist_name=="Hansraj Raghuwanshi":
            cid=channel_ids[3]
        elif artist_name=="Diljit Dosanjh":
            cid=channel_ids[1]
        elif artist_name=="Neha kakkar":
            cid=channel_ids[5]
        elif artist_name=="Armaan Malik":
            cid=channel_ids[4]
        elif(artist_name=="Atif Aslam"):
            cid=channel_ids[6]
        elif(artist_name=="Jubin Nautiyal"):
            cid=channel_ids[7]        
        
        analyze(artist_name,cid)
else:
    st.title("ALL ARTIST STATS")
    comp_dict=get_multi_channel_stats(youtube,channel_ids) 
    comp_df=pd.DataFrame(comp_dict)
    # comp_df=pd.DataFrame.from_dict(comp_dict,columns=['CHANNEL NAME','SUBSCRIBERS','VIEW COUNT','TOTAL VIDEOES','PLAYLIST ID'])
    term=st.sidebar.radio("In terms of ",("Data Frame","Total Videoes","No. Of Subscribers","Views Count"))
    
    #   Changing   forms
    comp_df['subscribers']=pd.to_numeric(comp_df['subscribers'])
    comp_df['Views']=pd.to_numeric(comp_df['Views'])
    comp_df['total_videoes']=pd.to_numeric(comp_df['total_videoes'])
    
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # plotting
    if term=="Data Frame":
        st.dataframe(comp_df)
    if term=="Total Videoes":
        plots('total_videoes')
    elif term=="No. Of Subscribers":
        plots("subscribers")
    elif term=="Views Count":
        plots("Views")




























        

