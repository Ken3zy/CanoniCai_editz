from jaseci.actions.live_actions import jaseci_action  # step 1
from twilio.rest import Client

account_sid = '' 
auth_token = '' 
client = Client(account_sid, auth_token) 


@jaseci_action(act_group=["twilio"], allow_remote=True)
def twilio_bot(message, phone_number):

    messagess = client.messages.create( 
                                from_='',  
                                body=message,
                                to=phone_number
                            ) 
    return messagess

if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server
    launch_server(port=8005)

    



