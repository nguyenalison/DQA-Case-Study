# Import Libraries
from logging import debug

import requests, json, datetime, pandas as pd
# params = dict();
# params[
#     'access_token'] = 'EAAXFN4uIoUABO0QnsK8ZBdPmZAFaWsWo33T57wsCzZAEboye0bBvLwYXw3cJHwcxwKtgHzFL8dVsMv7NUndYn3ZCOCBxoV2MhNJtZAvSjKF64y627LciyePEWrZBGF3JZBlOxlOnBcgPP2tjofmZBB0fvnvVW1Qt8vMdzugLUBzeY80GTdmQVNroIsnvuu2FyZCUZCTz5NzWUfnB8JvpXmMaw9wDOZAMagZD'
# params['client_id'] = '1624217238413632'
# params['client_secret'] = 'd09126e08688737d484b43c09277eb9e'
# params['graph_domain'] = 'https://graph.facebook.com'
# params['graph_version'] = 'v20.0'
# params['endpoint_base'] = params['graph_domain'] + '/' + params['graph_version'] + '/'
# params['page_id'] = '281781558362843'
# params['instagram_account_id'] = '1626662358185769'
# params['ig_username'] = 'miss.nailbitz'
# params['debug'] = 'no'
#
# # Define Endpoint Parameters
# endpointParams = dict()
# endpointParams['input_token'] = params['access_token']
# endpointParams['access_token'] = params['access_token']
#
# # Define URL
# url = params['graph_domain'] + '/debug_token'
#
# # Requests Data
# data = requests.get(url, endpointParams)
# access_token_data = json.loads(data.content)
#
# # Define URL
# url = params['endpoint_base'] + 'oauth/access_token'
#
# # Define Endpoint Parameters
# endpointParams = dict()
# endpointParams['grant_type'] = 'fb_exchange_token'
# endpointParams['client_id'] = params['client_id']
# endpointParams['client_secret'] = params['client_secret']
# endpointParams['fb_exchange_token'] = params['access_token']
#
# # Requests Data
# data = requests.get(url, endpointParams)
# long_lived_token = json.loads(data.content)
# long_lived_token
# # access_token = long_lived_token['access_token']
# hashtags = ['🍉', 'Israel', 'Palestine']
# username = params['ig_username']
#
def getCreds():
    creds = dict()  # dictionary to hold everything
    creds[
        'access_token'] = 'EAAXFN4uIoUABOybmU7nknz9GG2ifjduZAy16Cx7u7MnnovLVkpxuK2lQpLPEkZAQZC5BBihaBNFd7tRNqcu2uoHmxQSJmnLWdDKLj3SZCCMjsrxZCk7mjLxiC1Rmr1XEJ5SBZClVyGq4UwKR9fxlyhtVPrqwOZBgwFhJ8ksOAEeOJjLFTZAk6ZB1F9QZAXrjiDGC7EwcQMTi87A1sMGTPZBvwZDZD-TOKEN'  # access token for use with all api calls
    creds['client_id'] = '1624217238413632'  # client id from facebook app IG Graph API Test
    creds['client_secret'] = 'd09126e08688737d484b43c09277eb9e'  # client secret from facebook app
    creds['graph_domain'] = 'https://graph.facebook.com/'  # base domain for api calls
    creds['graph_version'] = 'v20.0'  # version of the api we are hitting
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/'  # base endpoint with domain and version
    creds['debug'] = 'no'  # debug mode for api call
    # creds['page_id'] = '281781558362843'  # users page id
    # creds['instagram_account_id'] = '1626662358185769'  # users instagram account id
    # creds['ig_username'] = 'miss.nailbitz'  # ig username

    return creds


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
    """ Print out to cli response from api call """

    print("\nURL: ")  # title
    print(response['url'])  # display url hit
    print("\nEndpoint Params: ")  # title
    print(response['endpoint_params_pretty'])  # display params passed to the endpoint
    print("\nResponse: ")  # title
    print(response['json_data_pretty'])  # make look pretty for cli

# def debugAccessToken(params):
#       endpointParams = dict()
#       endpointParams['input_token'] = params['access_token']
#       endpointParams['access_token'] = params['access_token']
#
#       url = params['graph_domain'] + '/debug_token'
#
#       return makeApiCall(url, params['debug'])


def debugAccessToken(params):
      """ Get info on an access token

      API Endpoint:
          https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}

      Returns:
          object: data from the endpoint

      """

      endpointParams = dict()  # parameter to send to the endpoint
      endpointParams['input_token'] = params['access_token']  # input token is the access token
      endpointParams['access_token'] = params['access_token']  # access token to get debug info on

      url = params['graph_domain'] + '/debug_token'  # endpoint url
      test = " http://graph.facebook.com/oauth/access_token?client_id=1624217238413632&client_secret=d09126e08688737d484b43c09277eb9e&grant_type=client_credentials"
      #  http://graph.facebook.com/oauth/access_token?client_id=123456789012345&client_secret=ZYxwVUTSRqpONMLKjiHGfeDCbA&grant_type=client_credentials
      return makeApiCall(test, endpointParams, params['debug'])  # make the api call


params = getCreds()  # get creds
params['debug'] = 'yes'  # set debug
response = debugAccessToken(params)  # hit the api for some data!
displayApiCallData(response)