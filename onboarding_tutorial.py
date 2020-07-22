class OnboardingTutorial:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    def __init__(self, channel):
        self.channel = channel
        self.username = "pythonboardingbot"
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Thank you for using BlackBiblio! :books: \n\n This app recommends books by Black authors.:brain: \n\n Click the button below to get a book!",
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": "https://static1.squarespace.com/static/579ff38346c3c4c4a2eeb3df/57b353b7c534a5407e14c057/5bf5808270a6ad3784655744/1551388279238/44325904_603214363440964_3698277344055441677_n.jpg?format=1500w",
                        "alt_text": "Black woman reading",
                    },
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": ":open_book:"},
                            "value": "click_me_123",
                        }
                    ],
                },
            ],
        }
