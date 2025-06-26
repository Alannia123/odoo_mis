import firebase_admin
from firebase_admin import messaging, credentials
from odoo.tools.config import config

firebase_cred = credentials.Certificate(config.get('firebase_private_key_path'))
firebase_app = firebase_admin.initialize_app(firebase_cred)


def send_firebase_notifications(messages) -> int:
    """
    [
        {'token':'','body':'','title':''},
        {'token':'','body':'','title':''}
    ]
    :param messages:
    :return: successfully send message count
    """
    messages = list(map(lambda msg: messaging.Message(
        notification=messaging.Notification(msg.get('title'), msg.get('body')),
        token=msg.get('token'),
    ), messages))
    response = messaging.send_each(messages)
    return response.success_count
