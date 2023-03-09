import traceback
from io import StringIO
from html.parser import HTMLParser
from flask_mail import Message

from zou.app import mail, app


def send_email(subject, html, recipient_email, body=None):
    """
    Send an email with given subject and body to given recipient.
    """
    if body is None:
        body = strip_html_tags(html)
    mail_default_sender = app.config["MAIL_DEFAULT_SENDER"]
    message = {
        "sender":"Kitsu Bot <%s>" % mail_default_sender,
        "body":body,
        "html":html,
        "subject":subject,
        "recipients":[recipient_email],
    }
    url = 'http://localhost:4200/api/email'
    x = requests.post(url, json = message)


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_html_tags(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()
