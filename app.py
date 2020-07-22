import os
import logging
import json
import random

# from googleapiclient import discovery
from flask import Flask, request, make_response
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from onboarding_tutorial import OnboardingTutorial
from recommend_book import RecommendBook

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app
)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

onboarding_tutorials_sent = {}


def start_onboarding(user_id: str, channel: str):
    # Create a new onboarding tutorial.
    onboarding_tutorial = OnboardingTutorial(channel)

    # Get the onboarding message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the onboarding message in Slack
    response = slack_web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    onboarding_tutorial.timestamp = response["ts"]

    # Store the message sent in onboarding_tutorials_sent
    if channel not in onboarding_tutorials_sent:
        onboarding_tutorials_sent[channel] = {}
    onboarding_tutorials_sent[channel][user_id] = onboarding_tutorial


# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack_events_adapter.on("message")
def message(payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if text and text.lower() == "start":
        return start_onboarding(user_id, channel_id)


@app.route("/slack/interactive-endpoint", methods=["POST"])
def book_rec():
    book_payload = json.loads(request.form["payload"])
    # print(book_payload)
    recBook = RecommendBook()
    book = recBook.get_book_payload()
    title = book["items"][0]["volumeInfo"]["title"]
    author = book["items"][0]["volumeInfo"]["authors"][0]
    link = book["items"][0]["volumeInfo"]["previewLink"]
    message = "*Title*: {} \n*Author*: {} \n {}".format(title, author, link)

    slack_web_client.chat_postMessage(
        channel=book_payload["channel"]["id"],
        ts=book_payload["container"]["message_ts"],
        text=message,
    )
    return make_response("hello", 200)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
