
# call for everyday 8:00 am from Amazon EventBridge
# to show yesterday statistics

from typing import List
from data import Problem
from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
import os
import logging
from storage import get_leetcode_problem, get_records_after
from datetime import datetime, timedelta

lc_channel_id = os.environ.get("LC_CHANNEL_ID")
slack_token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)


def greeting(event, context):
    try:
        rs = get_records_after(datetime.now() + timedelta(days=-1))  # last 24h
        msg = greeting_script(rs)
        print(msg)
        response = client.chat_postMessage(
            channel=lc_channel_id,
            text=msg
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        # str like 'invalid_auth', 'channel_not_found'
        logging.error(e.response["error"])


def score_of_problems(p: List[Problem]):
    """Assume that 1 hard = 2 medium = 6 easy """
    score = 0
    for i in p:
        if i.difficulty == 'Easy':
            score += 1
        elif i.difficulty == 'Medium':
            score += 3
        else:
            score += 6
    return score


def greeting_script(rs) -> str:
    if(len(rs) == 0):
        return "Nobody done a leetcode problems yesterday. We have to work hard today!"

    us = {}
    for (uid, pid, _) in rs:
        if us.get(uid) is None:
            us[uid] = []
        us[uid].append(get_leetcode_problem(pid))

    user_by_score = sorted([(k, v, score_of_problems(v))
                            for k, v in us.items()], key=lambda i: i[2])

    # get user with max score
    max_people = [i for i in user_by_score if i[2] == user_by_score[-1][2]]
    max_number = len(max_people)

    # assembling script
    msg = "Good morning!"
    if max_number > 3:
        msg += "Everyone worked hard yesterday."
    elif max_number > 1:
        msg += " and ".join(["<@{}>".format(i[0]) for i in max_people])
        msg += " are the best player of yesterday!"
    else:
        u, problems, _ = user_by_score[-1]
        msg += "<@{}> is the best player of yesterday. {} problems are finished yesterday".format(
            u,
            len(problems))

        not_easy_number = sum([i != 'Easy' for i in problems])
        if not_easy_number > 0:
            msg += " and {} of them are medium difficutly above.".format(
                not_easy_number)

    msg += " Let's strive together today!"
    return msg
