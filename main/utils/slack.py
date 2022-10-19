import slack
import yaml


class SlackClient:
    """
    Client to interact with the Slack API.
    """

    def __init__(self):
        with open("./config/default.yml", "r") as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)
        self.slack_client = slack.WebClient(token=self.conf["slack"]["token"])

    """
    Send a slack message to a specific channel.
    """
    def send_slack_message(self, message):
        self.slack_client.chat_postMessage(channel=self.conf["slack"]["channel"], text=message)
