from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from components.env import dev_env


client = WebClient(token=dev_env.SLACK_TOKEN)


def send_slack_message(channel_id: str, text: str):
    try:
        client.chat_postMessage(channel=channel_id, text=text)
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")
