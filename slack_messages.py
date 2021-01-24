from bamboohr import Bamboohr
import slack as sl
from datetime import datetime
import os


SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
client = sl.WebClient(token=SLACK_BOT_TOKEN)
bamboohr = Bamboohr()


class SlackMessages:
    buttons = [
        {
            "name": "choice",
            "text": "Post this message to #general",
            "type": "button",
            "value": "choice"
        },
        {
            "name": "cancel",
            "text": "Cancel",
            "type": "button",
            "value": "cancel"
        }
    ]

    def __init__(self, test_channel):
        self.test_channel = test_channel

    def send_welcome_message(self):
        newbies_list = bamboohr.check_newbies()
        for i in newbies_list:
            newbie = bamboohr.get_emp_profile_by_id(i).json()
            emp_photo = bamboohr.get_emp_photo_url(i)
            message = f"*Welcome Our Newest Team Member :vgs: *\n" \
                f"*{newbie['firstName']} {newbie['lastName']}*\n" \
                f"\nHey Team, \n\n" \
                f"We are happy to have *{newbie['firstName']} {newbie['lastName']}*" \
                f"join us as *{newbie['jobTitle']}* in :world_map: *{newbie['location']}* office.\n" \
                f"{newbie['firstName']}'s first day is today, so please take the time to say hi and welcome " \
                f"{newbie['firstName']} to the team :hugging_face::raised_hands::rocket:"
            message_attachments = [
                {
                    "fallback": "Upgrade your Slack client to use messages like these.",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "callback_id": "menu_options_2319",
                    "pretext": newbie['firstName'],
                    "image_url": emp_photo,
                    "actions": self.buttons
                }
            ]
            client.chat_postMessage(channel=self.test_channel, text=message, as_user='True',
                                    attachments=message_attachments, unfurl_links=True)

    def send_hb_message(self):
        hb_list = bamboohr.check_hb()
        newbies = bamboohr.check_newbies()
        if len(hb_list) > 2:
            message_full_names = ''
            message_names = ''
            for i in hb_list:
                hb_one = bamboohr.get_emp_profile_by_id(i)
                if hb_one:
                    hb_one = hb_one.json()
                else:
                    continue
                if hb_one['id'] in newbies:
                    continue
                message_full_names += hb_one['firstName'] + ' ' + hb_one['lastName'] + ', '
                message_names += hb_one['firstName'] + ', '
            message_full_names = message_full_names[:-2]
            message = f"Let’s start today’s day with warm congrats to *{message_full_names}*." \
                f"\nWe all wish you an unforgettable day today and a fantastic year ahead!:hugging_face::tada:" \
                f"\nExtremely happy to have you at VGS:vgs::rocket:" \
                f"\nhttp://bestanimations.com/Holidays/Birthday/birthdaygifs/happy-birthday-colorful-type-animated-gif.gif"
            message_attachments = [
                {
                    "fallback": "Upgrade your Slack client to use messages like these.",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "callback_id": "menu_options_2319",
                    "actions": self.buttons
                }
            ]
            client.chat_postMessage(channel=self.test_channel, text=message, as_user='True',
                                    attachments=message_attachments, unfurl_links=True)
        else:
            for i in hb_list:
                hb_one = bamboohr.get_emp_profile_by_id(i)
                emp_photo = bamboohr.get_emp_photo_url(i)
                if hb_one:
                    hb_one = hb_one.json()
                if hb_one in newbies:
                    continue
                message = f"Let’s start today’s day with warm congrats to *{hb_one['firstName']} {hb_one['lastName']}*." \
                    f"\nWe all wish you an unforgettable day today and a fantastic year ahead!:hugging_face::tada:" \
                    f"\nExtremely happy to have you at VGS:vgs::rocket:"
                message_attachments = [
                    {
                        "fallback": "Upgrade your Slack client to use messages like these.",
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "callback_id": "menu_options_2319",
                        "pretext": hb_one['firstName'],
                        "image_url": emp_photo,
                        "actions": self.buttons
                    }
                ]
                client.chat_postMessage(channel=self.test_channel, text=message, as_user='True',
                                        attachments=message_attachments, unfurl_links=True)

    def send_anniversary_message(self):
        anniversary_list = bamboohr.check_anniversary()
        newbies = bamboohr.check_newbies()
        if len(anniversary_list) > 2:
            message_full_names = ''
            message_names = ''
            for i in anniversary_list:
                anniversary_one = bamboohr.get_emp_profile_by_id(i[0])
                if anniversary_one:
                    anniversary_one = anniversary_one.json()
                else:
                    continue
                if anniversary_one['id'] in newbies:
                    continue
                message_full_names += anniversary_one['firstName'] + ' ' + anniversary_one['lastName'] + ', '
                message_names += anniversary_one['firstName'] + ', '
            message_full_names = message_full_names[:-2]
            message_names = message_names[:-2]
            message = f"Let’s take a minute to wish a happy anniversary to *{message_full_names}* at VGS! " \
                f":vgs::hugging_face:" \
                f"\nWe want to say thank you for all your efforts and achievements that help us get where we are now! " \
                f"\n*{message_names}*, let the upcoming year at VGS be even more challenging and significant! " \
                f":wink::sparkles::rocket:" \
                f"\nhttps://tenor.com/view/happyanniversary-gif-13014753"
            message_attachments = [
                {
                    "fallback": "Upgrade your Slack client to use messages like these.",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "callback_id": "menu_options_2319",
                    "actions": self.buttons
                }
            ]
            client.chat_postMessage(channel=self.test_channel, text=message, as_user='True',
                                    attachments=message_attachments, unfurl_links=True)
        else:
            for i in anniversary_list:
                anniversary_one = bamboohr.get_emp_profile_by_id(i[0])
                if anniversary_one:
                    anniversary_one = anniversary_one.json()
                else:
                    continue
                if anniversary_one['id'] in newbies:
                    continue
                emp_photo = bamboohr.get_emp_photo_url(i[0])
                years = str(int(datetime.today().strftime('%Y')) - int(i[1]))
                message = f"Let’s take a minute to wish a happy {years} years anniversary to *{anniversary_one['firstName']} " \
                    f"{anniversary_one['lastName']}* at VGS! :vgs::hugging_face:" \
                    f"\nWe want to say thank you for all your efforts and achievements that help us get where we are now! " \
                    f"\n{anniversary_one['firstName']}, let the upcoming year at VGS " \
                    f"be even more challenging and significant! :wink::sparkles::rocket:"
                message_attachments = [
                    {
                        "fallback": "Upgrade your Slack client to use messages like these.",
                        "color": "#3AA3E3",
                        "pretext": anniversary_one['firstName'],
                        "image_url": emp_photo,
                        "attachment_type": "default",
                        "callback_id": "menu_options_2319",
                        "actions": self.buttons
                    }
                ]
                client.chat_postMessage(channel=self.test_channel, text=message, as_user='True',
                                        attachments=message_attachments, unfurl_links=True)
