from time import sleep

import requests
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = "AAAAAAAAAAAAAAAAAAAAAE5XjAEAAAAA8qy3mdrBJqnBAO54oN1YI9aE%2Bvo%3DcEUZiwzA2Ob6sX3RGv1jDPliGYv4SGiMPoFTq9kWDMTlivYcEq"
search_url = "https://api.twitter.com/2/tweets/search/all"


# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params, stream=True)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#(point_radius:[-122.20120871114341 37.60324513543482 24mi] OR point_radius:[-121.89755249314423 37.3326323448069 10mi])   #BayAreaHeat
def main():
    query_params = {'query': '("california heat wave" OR #CaliforniaHeatWave) lang:en',
                    'start_time': "2022-09-03T00:00:00Z",
                    'end_time': "2022-09-09T00:00:00Z",
                    'max_results': 500,
                    'tweet.fields': 'author_id,created_at,geo,lang',}
    outputFile = open("result.txt", "a+", encoding="utf-8")

    count = 0
    while True:
        response = connect_to_endpoint(search_url, query_params)
        meta = response["meta"]
        data = response["data"]
        sleep(3.0)
        for result in data:
            outputFile.write(json.dumps(result, sort_keys=True) + "\n")
            count += 1
        next_token = meta.get("next_token")
        if not next_token:
            break
        else:
            query_params['next_token']=next_token
    print(count)




if __name__ == "__main__":
    main()
