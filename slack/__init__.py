import logging
from logging import NullHandler

from slack.web.client import WebClient  # noqa
from slack.rtm.client import RTMClient  # noqa
from slack.webhook.client import WebhookClient  # noqa

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
