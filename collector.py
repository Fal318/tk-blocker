import json
from requests_oauthlib import OAuth1Session
import urls
import config


class Collector:
    def __init__(self):
        self.oath = OAuth1Session(
            config.API_KEY,
            config.API_KEY_SECRET,
            config.ACCESS_TOKEN,
            config.ACCESS_TOKEN_SECRET
        )

    def collect_tweets(self, keyword: str, count: int = 200) -> list:
        url = urls.url["search"]
        params = {
            "q": keyword + " filter:native_video exclude:nativeretweets",
            "local": "ja",
            "result_type": "mixed",
            "count": count,
        }
        response = self.oath.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"status_code is {response.status_code}")
        tweets = json.loads(response.text)
        media_url = []
        for tweet in tweets["statuses"]:
            if "extended_entities" in tweet.keys():
                media_url.append(
                    [tweet["extended_entities"]["media"][0]["media_url"],
                     tweet["user"]["id"]]
                )
        return media_url

    def block_user(self, user_id: int) -> bool:
        url = urls.url["block"]
        params = {"user_id": user_id}
        response = self.oath.post(url, params=params)
        if response.status_code != 200:
            raise Exception(f"status_code is {response.status_code}")
        return True

    def get_followers(self, user_id: int) -> list:
        url = urls.url["followers"]
        params = {"user_id": user_id}
        response = self.oath.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"status_code is {response.status_code}")
        return json.loads(response.text)["ids"]

    def get_trends(self, woeid: int = 23424856) -> list:
        url = urls.url["trends"]
        trends = []
        params = {"id": woeid}
        response = self.oath.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"status_code is {response.status_code}")
        for trend in json.loads(response.text)[0]["trends"]:
            trends.append(trend["name"])
        return trends

    def get_rate_limits(self):
        url = urls.url["limits"]
        response = self.oath.get(url)
        if response.status_code != 200:
            raise Exception(f"status_code is {response.status_code}")
        text = json.loads(response.text)["resources"]
        for classes in json.loads(response.text)["resources"]:
            for rate in text[classes]:
                limit = text[classes][rate]['limit']
                remaining = text[classes][rate]['remaining']
                if limit != remaining:
                    print(
                        f"{rate}: {text[classes][rate]['remaining']}/{text[classes][rate]['limit']}")

    def get_block_list(self):
        url = urls.url["block_list"]
        response = self.oath.get(url)
        block_list = []
        if response.status_code != 200:
            raise Exception(f"status_code is {response.status_code}")
        text = json.loads(response.text)
        for user in text["users"]:
            block_list.append(user["id_str"])
        return block_list


if __name__ == "__main__":
    pass
