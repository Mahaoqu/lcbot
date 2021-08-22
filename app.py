import logging
import os
import re

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler


# Initializes your app with your bot token and signing secret
app = App(
    process_before_response=True # must be True when running on FaaS
)

# use logger
@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()

# copy from tutorial
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your _App's Home_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
          }
        ]
      }
    )
  
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

# test metion
@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    logger.info(body)
    say(f"Hi, What's up?")

# test client get name
# TODO: use cache
@app.message("test")
def reply_to_test(client, message, say):
    u = message["user"]
    resp = client.users_info(user=u)
    name = resp.get('user')['real_name']
    say(f"Good test, @{name}. I know you REAL name now.")


@app.message(re.compile("bug"))
def mention_bug(say):
    say("Do you mind filing a ticket?")

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
