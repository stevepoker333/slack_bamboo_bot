from slack_messages import SlackMessages, client
from bamboohr import Bamboohr
from flask import Flask, make_response, request
import json
import os
import threading
from time import sleep
from datetime import datetime


app = Flask(__name__)
MAIN_CHANNEL = os.environ["MAIN_CHANNEL"]
TEST_CHANNEL = os.environ["TEST_CHANNEL"]
bamboohr = Bamboohr()
slack_messages = SlackMessages(test_channel=TEST_CHANNEL)


def check():
    today = ''
    while True:
        if today == datetime.today().strftime('%Y-%m-%d'):
            sleep(60)
            continue
        else:
            today = datetime.today().strftime('%Y-%m-%d')
            if bamboohr.check_newbies():
                slack_messages.send_welcome_message()
            if bamboohr.check_anniversary():
                slack_messages.send_anniversary_message()
            if bamboohr.check_hb():
                slack_messages.send_hb_message()


def app_run():
    app.run()


@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    form_json = json.loads(request.form["payload"])
    text = form_json["original_message"]["text"]
    ts = form_json["message_ts"]
    channel = form_json["channel"]["id"]
    if form_json["actions"][0]["value"] == "cancel":
        try:
            photo_url = form_json["original_message"]["attachments"][0]["image_url"]
            client.chat_update(channel=channel, text="`*Canceled*`\n\n" + text, as_user=True,
                               attachments=[{'pretext': '', 'image_url': photo_url}], ts=ts)
        except:
            client.chat_update(channel=channel, text="`*Canceled*`\n\n" + text, as_user=True, ts=ts, attachments='')
    else:
        try:
            photo_url = form_json["original_message"]["attachments"][0]["image_url"]
            client.chat_postMessage(channel=MAIN_CHANNEL, text=text, as_user=True,
                                    attachments=[{'pretext': '', 'image_url': photo_url}])
            client.chat_update(channel=channel, text="`*Posted*`\n\n" + text, as_user=True, attachments=[{'pretext': '', 'image_url': photo_url}], ts=ts)
        except:
            client.chat_postMessage(channel=MAIN_CHANNEL, text=text, as_user=True)
            client.chat_update(channel=channel, text="`*Posted*`\n\n" + text, as_user=True, ts=ts, attachments='')
    return make_response("", 200)


if __name__ == '__main__':
    t1 = threading.Thread(target=check, args=())
    t2 = threading.Thread(target=app_run, args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()
