# Chat Analyser Overview  

The **Chat Analyser** extracts insights from chat data using NLP and visualization techniques.  

## Key Features  
- **Statistics (`fetch_stats`)**: Counts messages, words, media, and URLs.  
- **User Activity (`most_busy_users`)**: Identifies top contributors.  
- **Word Cloud (`create_wordcloud`)**: Visualizes frequently used words.  
- **Common Words (`most_common_words`)**: Lists top 20 words (excluding stopwords).  
- **Emoji Analysis (`emoji_helper`)**: Finds top 20 emojis used.  
- **Message Trends**:  
  - **Monthly (`monthly_timeline`)** & **Daily (`daily_timeline`)** message count.  
  - **Weekday (`week_activity_map`)** & **Monthly (`month_activity_map`)** activity.  
  - **Heatmap (`activity_heatmap`)**: Visualizes user activity by time.  

## Libraries  
Uses `URLExtract`, `WordCloud`, `nltk`, `pandas`, `emoji`, `Counter`.  

Perfect for WhatsApp chat analysis! 🚀
