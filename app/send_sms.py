from twilio.rest import Client
import config

# Account details
account_sid = config.ACCOUNT_SID
auth_token = config.AUTH_TOKEN

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+15017122661',
                     to='+15558675310'
                 )

print(message.sid)