import logging
import re

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

from script import get_submit_script
from storage import get_leetcode_problem, save_check_in_record

# Initializes your app with your bot token and signing secret
app = App(
    process_before_response=True  # must be True when running on FaaS
)

# user fault or bug..


@app.error
def handle_error(error, logger):
    logger.error(error)
    # say(f'Sorry, your request is failed beacuse of {error}')


@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()


check_int_format = re.compile("#(\d+)")


@app.event("app_mention")
def handle_app_mentions(logger, payload, say):
    try:
        # https://api.slack.com/events/app_mention
        msg = payload["text"]
        uid = payload["user"]
        if '签到' in msg or 'check-in' in msg:
            handle_check_in(uid, msg, say)
        elif '撤销' in msg or 'revoke' in msg:
            handle_reovke_last_check_in()
        else:
            say('Hummmm. How are you today?')  # TODO: random while mentioned
    except Exception as e:
        logger.exception(e)
        say(f'Sorry, your request is failed beacuse of {e}')


def search_check_in_number(body):
    return


def handle_check_in(uid, msg, say):
    # find problem number
    match = check_int_format.search(msg)
    pid = int(match.group()[1:])

    problem = get_leetcode_problem(pid)
    save_check_in_record(uid, pid)
    say(get_submit_script(problem, get_user_mentioned(uid)))


def handle_reovke_last_check_in(uid, pid):
    pass


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def get_user_mentioned(id):
    # resp = client.users_info(user=id)
    # return resp.get('user')['real_name']
    return f'<@{id}>'


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
