from components.messanger.slack import send_slack_message
import json

json_path = "/Users/yangwoolee/repo/captured/admin/backend/test/test_components/test_messanger/test.json"


def test_send_slack_message():
    with open(json_path, "r") as f:
        json_message = json.load(f)

    formatted_code_block = json.dumps(json_message, indent=2)

    channel_id = "C06D5UGUL6R"
    send_slack_message(channel_id, formatted_code_block)
