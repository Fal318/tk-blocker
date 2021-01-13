import time
import pandas as pd
import multiprocessing
import config
import detector
import collector


def detect_process(img_url, user_id, target_user):
    result = detector.main(img_url)
    if result:
        target_user.append(user_id)


def main():
    manager = multiprocessing.Manager()
    target_user = manager.list()
    collectors = collector.Collector()
    trends = collectors.get_trends()
    links = []
    df = pd.read_csv(config.PATH["csv"])
    blocked_users = list(df["user_id"])
    for trend in trends:
        for l in collectors.collect_tweets(trend):
            if not l[1] in blocked_users:
                links.append(l)
    process_list = []
    for link, user_id in links:
        process = multiprocessing.Process(
            target=detect_process,
            kwargs={
                "img_url": link,
                "user_id": user_id,
                "target_user": target_user
            }
        )
        process_list.append(process)
    while len(process_list) != 0:
        if len(multiprocessing.active_children()) < multiprocessing.cpu_count()*3:
            process = process_list.pop(0)
            process.start()

    while len(multiprocessing.active_children()) > 1:
        continue
    followers = collectors.get_followers(config.MY_ID)
    target_user = list(set(target_user))
    for user in target_user:
        if not(user in followers or user in blocked_users):
            collectors.block_user(user)
            time.sleep(0.2)
    df_block = pd.Series(target_user)
    df_block.to_csv(config.PATH["csv"], mode="a", header=False, index=False)


if __name__ == "__main__":
    main()
