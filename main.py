import re
from datetime import time
import pandas as pd
import requests, json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from googletrans import Translator

credentials = dict()
credentials[
    'access_token'] = 'MY_ACESS_TOKEN'  # access token for use with all api calls
credentials['client_id'] = 'MY_CLIENT_ID'  # client id from facebook app IG Graph API Test
credentials['client_secret'] = 'CLIENT_SECRETE'  # client secret from facebook app
credentials['graph_domain'] = 'https://graph.facebook.com/'  # base domain for api calls
credentials['graph_version'] = 'v20.0'  # version of the api we are hitting
credentials['endpoint_base'] = credentials['graph_domain'] + credentials[
    'graph_version'] + '/'  # base endpoint with domain and version
credentials['debug'] = 'yes'  # debug mode for api call
credentials['page_id'] = 'PAGE_ID'  # users page id
credentials['instagram_account_id'] = 'ACCOUNT_ID'  # users instagram account id
credentials['ig_username'] = 'USERNAME'  # ig username
credentials['limit'] = 50


def makeApiCall(url, endpointParams, debug):
    data = requests.get(url, endpointParams)
    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpointParams
    response['endpoint_params_pretty'] = json.dumps(endpointParams, indent=4)
    response['json_data'] = json.loads(data.content)
    response['json_data_pretty'] = json.dumps(response['json_data'], indent=4)
    return response


# Get hashtag id
def getHashtagId(hashtag):
    url = f"{credentials['endpoint_base']}ig_hashtag_search?user_id=" \
          f"{credentials['instagram_account_id']}&q={hashtag}&access_token={credentials['access_token']}"
    data = requests.get(url)
    response = json.loads(data.content)
    hashtagId = response['data'][0]['id']
    return hashtagId


def getTopMedia(hashtag):
    url = f"{credentials['endpoint_base']}{getHashtagId(hashtag)}/top_media/?" \
          f"user_id={credentials['instagram_account_id']}" \
          f"&fields=id,media_type,media_url, caption, timestamp, comments_count, like_count" \
          f"&access_token={credentials['access_token']}" \
          f"&limit={credentials['limit']}"
    data = requests.get(url)
    response = json.loads(data.content)
    return response['data']


def getRecentMedia(hashtag):
    url = f"{credentials['endpoint_base']}{getHashtagId(hashtag)}/recent_media/?" \
          f"user_id={credentials['instagram_account_id']}" \
          f"&fields=id,media_type,media_url, caption,timestamp" \
          f"&access_token={credentials['access_token']}"
    data = requests.get(url)
    response = json.loads(data.content)
    return response['data']


def find_watermelon_emojis(data):
    watermelon_emoji = "🍉"
    filtered_data = []
    for item in data:
        caption = item.get('caption', '')
        if watermelon_emoji in caption:
            filtered_data.append(item)
    return filtered_data


def display_data(data):
    # filtered_data = find_watermelon_emojis(data)
    # for item in data:
    #     # print(f"ID: {item['id']}")
    #     print(f"Media Type: {item['media_type']}")
    #     print(f"Caption: {item['caption']}")
    #     print(f"Media URL: {item['media_url']}")
    #     print(f"Time: {item['timestamp']}")
    #     print("-" * 80)
    for sublist in data:
        for item in sublist:
            if 'caption' in item:
                print(f"Media Type: {item.get('media_type')}")
                print(f"Caption: {item.get('caption')}")
                print(f"Media URL: {item.get('media_url')}")
                print(f"Time: {item.get('timestamp')}")
                print(f"Likes: {item.get('like_count')}")
                print(f"Comments: {item.get('comments_count')}")
                print("-" * 80)
            else:
                print("No caption found")


def find_keywords(data, keywords):
    filtered_data = []
    keywords_lower = [keyword.lower() for keyword in keywords]

    for item in data:
        caption = item.get('caption', '').lower()
        if any(keyword in caption for keyword in keywords_lower):
            filtered_data.append(item)

    return filtered_data


def generate_word_cloud(captions):
    text = ' '.join(captions)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


#
# topMedia = getTopMedia("watermelon")
# print(topMedia)
# containsWatermelonEmoji = find_watermelon_emojis(topMedia)
# keywords = ["Gaza", "Palestine", "Israel", "Palestinian", "Israeli"]
# containsConflictWords = find_keywords(containsWatermelonEmoji, keywords)
# display_data(containsConflictWords)

# print("*" * 100)
# Word cloud for top media with #watermelon
# topCaptions = [item['caption'] for item in topMedia if 'caption' in item]
# generate_word_cloud(topCaptions)

# # Word cloud for top media with #watermelon
# topCaptions = [item['caption'] for item in containsConflictWords if 'caption' in item]
# print(topCaptions)
# generate_word_cloud(topCaptions)

def find_watermelon_emojis(data):
    watermelon_emoji = "🍉"
    filtered_data = []
    for sublist in data:
        for item in sublist:
            if 'caption' in item and watermelon_emoji in item['caption']:
                filtered_data.append(item)
    return filtered_data


keywords = ["Gaza", "Palestine", "Israel", "Palestinian", "Israeli"]
keywordsId = ['17843784049044435', '17843870389043902', '17841596584074200', '17841562624126713', '17841563635109795']


def getAllMediaContainKeywords(keywords):
    rtn = []
    for keyword in keywords:
        url = f"{credentials['endpoint_base']}{keyword}/top_media/?" \
              f"user_id={credentials['instagram_account_id']}" \
              f"&fields=id,media_type,media_url, caption, timestamp,like_count, comments_count" \
              f"&access_token={credentials['access_token']}" \
              f"&limit={credentials['limit']}"
        data = requests.get(url)
        response = json.loads(data.content)
        rtn.append(response['data'])
    return rtn


# print(captionsWithWatermelon)
# print(allMediaContainingKeywords)
def get_captions_from_data(data):
    return [item['caption'] for item in data]


# captions = get_captions_from_data(captionsWithWatermelon)


def translate_arabic_to_english(caption):
    translator = Translator()
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    arabic_parts = arabic_pattern.findall(caption)

    # Retry translation if an error occurs
    retries = 3
    for _ in range(retries):
        try:
            for arabic_part in arabic_parts:
                translated_part = translator.translate(arabic_part, dest='en').text
                caption = caption.replace(arabic_part, translated_part)
            return caption
        except AttributeError:
            time.sleep(1)  # Wait for 1 second before retrying
    return caption  # Return original caption if retries fail


def cleanCaption(caption):
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F]+')
    caption = re.sub(arabic_pattern, '', caption)
    # Remove new lines
    caption = caption.replace('\n', ' ')

    # Remove bullet points
    caption = re.sub(r'•', '', caption)

    # Remove special characters except emojis and hashtags
    caption = re.sub(r'[^\w\s#🍉]', '', caption)

    # Tokenize the text
    tokens = caption.split()

    # Lowercase the text
    tokens = [token.lower() for token in tokens]

    # Join tokens back into a string
    clean_caption = ' '.join(tokens)

    return clean_caption


# sanitizedCaptions = cleanCaption(captions)

def analyze_sentiment(text):
    # Create a TextBlob object
    blob = TextBlob(text)

    # Get the sentiment polarity
    sentiment_polarity = blob.sentiment.polarity

    # Classify the sentiment
    if sentiment_polarity > 0:
        return "Positive"
    elif sentiment_polarity < 0:
        return "Negative"
    else:
        return "Neutral"


def sentiment_scores(caption):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # Polarity_scores method of SentimentIntensityAnalyzer object gives a sentiment dictionary,
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(caption)
    return sentiment_dict


# def getAllSentiments(captions):
#     for i in range(len(captions)):
#         print("*" * 100)
#         print(sanitizedCaptions[i])
#         print(analyze_sentiment(sanitizedCaptions[i]))
#         print(sentiment_scores(sanitizedCaptions[i]))

def process_posts(posts):
    data = []

    for post in posts:
        for item in post:
            caption = item.get('caption', 0)
            likes = item.get('like_count', 0)
            comments = item.get('comments_count', 0)
            # print(caption)
            cleanedCaption = cleanCaption(caption)
            # print(type(cleanedCaption))
            sentiment_dict = sentiment_scores(cleanedCaption)
            hasHateAdultContent = find_hate_speech_and_adult_content(cleanedCaption)
            any_hate_adult_content = any(hasHateAdultContent)

            data.append({
                'caption': cleanedCaption,
                'likes': likes,
                'comments': comments,
                'positive_score': sentiment_dict['pos'],
                'negative_score': sentiment_dict['neg'],
                'neutral_score': sentiment_dict['neu'],
                'sentiment': sentiment_dict['compound'],
                'hate_adult_content': any_hate_adult_content
            })
    pd.set_option('display.max_rows', 300)
    pd.set_option('display.max_columns', 300)
    pd.set_option('display.width', 1500)
    pd.set_option('display.float_format', '{:.2f}'.format)
    sorted = pd.DataFrame(data).sort_values(by='likes', ascending=False).drop_duplicates()
    return sorted


# allMediaContainingKeywords = getAllMediaContainKeywords(keywordsId)
# captionsWithWatermelon = (find_watermelon_emojis(allMediaContainingKeywords))
# captionsWithWatermelonDF = process_posts(captionsWithWatermelon)
# print(captionsWithWatermelon)
# print()
# print()
# print('!'*100)
# allMediaDF = process_posts(allMediaContainingKeywords)

# print(allMediaDF)

# Map sentiment to numerical values
# sentiment_mapping = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
# captionsWithWatermelonDF['sentiment_numeric'] = captionsWithWatermelonDF['sentiment'].map(sentiment_mapping)
#
# # Create scatter plot
# plt.figure(figsize=(10, 6))
# plt.scatter(captionsWithWatermelonDF['comments'], captionsWithWatermelonDF['sentiment_numeric'], color='blue')
# plt.xlabel('Number of comments')
# plt.ylabel('Sentiment')
# plt.title('Correlation between Number of Comments and Sentiment')
# plt.xticks(rotation=45)
# plt.yticks([-1, 0, 1], ['Negative', 'Neutral', 'Positive'])
# plt.grid(True)
# plt.show()

# sentiment_mapping = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
# allMediaDF['sentiment_numeric'] = allMediaDF['sentiment'].map(sentiment_mapping)
# # Create scatter plot
# plt.figure(figsize=(10, 6))
# plt.scatter(allMediaDF['likes'], allMediaDF['sentiment_numeric'], color='blue')
# plt.xlabel('Number of Likes')
# plt.ylabel('Sentiment')
# plt.title('Correlation between Number of Likes and Sentiment for All Conflict Related Posts')
# plt.xticks(rotation=45)
# plt.yticks([-1, 0, 1], ['Negative', 'Neutral', 'Positive'])
# plt.grid(True)
# plt.show()

def process_posts_watermelon(posts):
    data = []
    for post in posts:
        # caption = post['caption']
        # likes = post['like_count']
        # comments = post['comments_count']
        caption = post.get('caption', '')
        likes = post.get('like_count', 0)
        comments = post.get('comments_count', 0)
        # print(caption)
        cleanedCaption = cleanCaption(caption)
        # print(type(cleanedCaption))
        sentiment_dict = sentiment_scores(cleanedCaption)
        hasHateAdultContent = find_hate_speech_and_adult_content(cleanedCaption)
        any_hate_adult_content = any(hasHateAdultContent)
        data.append({
            'caption': cleanedCaption,
            'likes': likes,
            'comments': comments,
            'positive_score': sentiment_dict['pos'],
            'negative_score': sentiment_dict['neg'],
            'neutral_score': sentiment_dict['neu'],
            'sentiment': sentiment_dict['compound'],
            'hate_adult_content': any_hate_adult_content
        })
    pd.set_option('display.max_rows', 300)
    pd.set_option('display.max_columns', 300)
    pd.set_option('display.width', 1500)
    pd.set_option('display.float_format', '{:.2f}'.format)
    sorted = pd.DataFrame(data).sort_values(by='likes', ascending=False).drop_duplicates()
    return sorted


# allMediaContainingKeywords = getAllMediaContainKeywords(keywordsId)
# captionsWithWatermelon = (find_watermelon_emojis(allMediaContainingKeywords))
# captionsWithWatermelonDF = process_posts_watermelon(captionsWithWatermelon)
# sns.scatterplot(data=captionsWithWatermelonDF, x='negative_score', y='likes')
# plt.ylabel('Likes')
# plt.xlabel('Negative Score')
# plt.title('Relation between Likes and Negative Score of Captions with Watermelon Emoji')
# plt.show()

def find_hate_speech_and_adult_content(text):
    # Define lists of keywords for hate speech and adult content
    sensitive_keywords = ['terrorist', 'infidel', 'zionist', 'antisemitic', 'jew', 'islamophobe',
                          'apartheid', 'genocide', 'colonizer', 'kill', 'murder',
                          'destroy', 'exterminate', 'bomb', 'jihad', 'intifada', 'ethnic cleansing',
                          'racist', 'supremacist', 'hate', 'violence', 'discrimination', 'oppression']
    adult_content_keywords = ['adult', 'explicit', 'sexual', 'nude', 'porn', 'erotic']
    spam_keywords = [ 'buy now', 'click here', 'subscribe', 'discount', 'sale', 'promo',
        'limited time', 'offer', 'earn money', 'work from home', 'win', 'congratulations', 'prize']
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()

    # Check for hate speech
    sensitive_content_dected = any(keyword in text_lower for keyword in sensitive_keywords)

    # Check for adult content
    adult_content_detected = any(keyword in text_lower for keyword in adult_content_keywords)

    spam_content_dected = any(keyword in text_lower for keyword in spam_keywords)
    # Return True if hate speech or adult content is detected, False otherwise
    return sensitive_content_dected, adult_content_detected, spam_content_dected


allMediaContainingKeywords = getAllMediaContainKeywords(keywordsId)
# allMedia = process_posts(allMediaContainingKeywords)
# print(allMedia)
captionsWithWatermelon = (find_watermelon_emojis(allMediaContainingKeywords))
captionsWithWatermelonDF = process_posts_watermelon(captionsWithWatermelon)
print(captionsWithWatermelonDF)

# Create the scatter plot
# plt.figure(figsize=(10, 6))
# sns.scatterplot(data=captionsWithWatermelonDF, x='sentiment',
#                 y='likes', hue='hate_adult_content',
#                 palette={False: 'red', True: 'blue'},
#                 style='hate_adult_content',
#                 markers={False: 'o', True: 'o'})
# # Customize the plot
# plt.title(
#     'Correlation between Sentiment Compound Score and Inclusion of Hate/Adult Content Captions with Watermelon Emoji')
# plt.xlabel('Sentiment Compound Score')
# plt.ylabel('Likes')
# plt.legend(title='Contains Hate/Adult Content', loc='upper right', labels=['No', 'Yes'])
#
# # Show the plot
# plt.show()
