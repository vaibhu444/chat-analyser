import streamlit as st
import preprosessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title('whatsapp chat analyzer')

upload_file = st.sidebar.file_uploader("choose a file")
if upload_file:
    byte_data = upload_file.getvalue()
    data = byte_data.decode('utf-8')
    df = preprosessor.preprocess(data)
    # st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'overall')

    selected_user = st.sidebar.selectbox('show analysis wrt user',user_list)

    if st.sidebar.button('show analysis'):
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        num_message, words, num_media_message, num_links = helper.fetch_stats(selected_user, df)
        with col1:
            st.header('Total Messages')
            st.title(num_message)
        
        with col2:
            st.header('Total Words')
            st.title(words)
        
        with col3:
            st.header('Media Shared')
            st.title(num_media_message)
        
        with col4:
            st.header('Link Shared')
            st.title(num_links)

        #timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map 
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        # weekly activity map 
        st.title('Weekly Activity Map')
        user_heatmap = helper.activity_heatmap(selected_user, df)
        print(user_heatmap)
        plot = sns.heatmap(user_heatmap)
        st.pyplot(plot.get_figure())

        # finding the busiest user in the group 
        if selected_user=='overall':
            busy_user, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            st.title('Most Busy User')
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(busy_user.index, busy_user.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
            
        # wordcloud 
        st.title('wordcloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common word 
        st.title('Most Common Words')
        most_common_df = helper.most_common_words(selected_user, df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.dataframe(most_common_df)


        # emoji analysis
        st.title('Emoji Analysis')

        col1,col2 = st.columns(2)
        with col1:
            emoji_df = helper.emoji_helper(selected_user, df)
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%0.2f')
            st.pyplot(fig)


        
        
