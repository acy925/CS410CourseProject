from time import sleep
import requests
import json


class DataPuller:

    def __init__(self, bearer_token, search_url="https://api.twitter.com/2/tweets/search/all"):
        self.bearer_token = bearer_token
        self.search_url = search_url
        pass

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2FullArchiveSearchPython"
        return r

    def connect_to_endpoint(self, params):
        response = requests.request("GET", self.search_url, auth=self.bearer_oauth, params=params, stream=True)
        print("pulling data...")
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    # (point_radius:[-122.20120871114341 37.60324513543482 24mi] OR point_radius:[-121.89755249314423 37.3326323448069 10mi])   #BayAreaHeat
    def pull_data(self, query, start_time, end_time, max_results, twitter_fields):
        tweets = []
        query_params = {'query': query,
                        'start_time': start_time,
                        'end_time': end_time,
                        'max_results': max_results,
                        'tweet.fields': twitter_fields}
        outputFile = open("tweets.txt", "a+", encoding="utf-8")

        count = 0
        while True:
            response = self.connect_to_endpoint(query_params)
            meta = response["meta"]
            data = response["data"]
            sleep(3.0)
            for result in data:
                outputFile.write(json.dumps(result, sort_keys=True) + "\n")
                tweets.append(result)
                count += 1
            print(f"pulled {count} tweets...")
            next_token = meta.get("next_token")
            if not next_token:
                break
            else:
                query_params['next_token'] = next_token
        print("Finished")
        print("--------------------")
        return tweets
