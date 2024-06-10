import requests, json, datetime, pandas as pd

credentials = dict()
credentials['access_token'] = '[]]'  # access token for use with all api calls
credentials['client_id'] = '[]]'  # client id from facebook app IG Graph API Test
credentials['client_secret'] = '[secret]'  # client secret from facebook app
credentials['graph_domain'] = 'https://graph.facebook.com/'  # base domain for api calls
credentials['graph_version'] = 'v20.0'  # version of the api we are hitting
credentials['endpoint_base'] = credentials['graph_domain'] + credentials['graph_version'] + '/'  # base endpoint with domain and version
credentials['debug'] = 'yes'  # debug mode for api call
credentials['page_id'] = '[]'  # users page id
credentials['instagram_account_id'] = '[]]'  # users instagram account id
credentials['ig_username'] = 'miss.nailbitz'  # ig username



def makeApiCall(url, endpointParams, debug):
    data = requests.get(url, endpointParams)
    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpointParams
    response['endpoint_params_pretty'] = json.dumps(endpointParams, indent=4)
    response['json_data'] = json.loads(data.content)
    response['json_data_pretty'] = json.dumps(response['json_data'], indent=4)

    if ('yes' == debug):  # display out response info
          displayApiCallData(response)  # display response
    return response

def displayApiCallData(response):
    print("\nURL: ")  # title
    print(response['url'])  # display url hit
    print("\nEndpoint Params: ")  # title
    print(response['endpoint_params_pretty'])  # display params passed to the endpoint
    print("\nResponse: ")  # title
    print(response['json_data_pretty'])  # make look pretty for cli

# Get hashtag id
def getHashtagId(hashtag):
    url = f"{credentials['endpoint_base']}ig_hashtag_search?user_id=" \
          f"{credentials['instagram_account_id']}&q={hashtag}&access_token={credentials['access_token']}"
    data = requests.get(url)
    response = json.loads(data.content)
    hashtagId = response['data'][0]['id']
    return hashtagId

def getTopMedia(hashTag):
    url = f"{credentials['endpoint_base']}{getHashtagId(hashTag)}/top_media/?" \
          f"user_id={credentials['instagram_account_id']}" \
          f"&access_token={credentials['access_token']}"
    data = requests.get(url)
    response = json.loads(data.content)
    print(url)
    # postsIdList = [item['id'] for item in response['data']]
    # return postsIdList
    return response

print(getTopMedia("watermelon"))
