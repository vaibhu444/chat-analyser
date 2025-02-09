from urlextract import URLExtract
from wordcloud import WordCloud
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):
    urlExtract = URLExtract()

    if selected_user!='overall':
        df = df[df['user']==selected_user]

    num_message = df.shape[0]

    # number of words
    words=[]
    for message in df['message']:
        words.extend(message.split(' '))   


    # number of media message 
    num_media_message = df[df['message']=='<Media omitted>\n'].shape[0]

    # number of urls 
    links = []
    for m in df['message']:
        links.extend(urlExtract.find_urls(m))
    num_links = len(links)


    return num_message, len(words), num_media_message, num_links


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0]) * 100, 2).reset_index().rename(columns={'user': 'name', 'count': 'percent'})
    return x, df



def create_wordcloud(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']==selected_user]

    temp = df[df['message']!= 'group_notification']
    temp = temp[temp['message']!='<Media omitted>\n']

    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']==selected_user]

    temp = df[df['message']!= 'group_notification']
    temp = temp[temp['message']!='<Media omitted>\n']
    
    stop_words = stopwords.words('english')
    temp['message'] = temp['message'].apply(lambda m: m.replace('\n', ''))

    words=[]
    not_needed = ['', 'null']
    for m in temp['message']:
        for w in m.lower().split(' '):
            if w not in stop_words and  w not in not_needed:
                words.append(w)
    
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']==selected_user]
    
    emojis=[]
    for m in df['message']:
        emojis.extend([c for c in m if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(20))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']==selected_user]
    
    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+' - '+ str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']==selected_user]
    
    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']==selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']==selected_user]
    
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0) 
    return user_heatmap