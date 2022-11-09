from jaseci.actions.live_actions import jaseci_action  # step 1
from twilio.rest import Client

account_sid = 'AC43ef78c7eeaed4a7946b247ece883c71' 
auth_token = 'a9605ee27aec046269204aaafc84035f' 
client = Client(account_sid, auth_token) 


@jaseci_action(act_group=["twilio"], allow_remote=True)
def twilio_bot(message, phone_number):

    messagess = client.messages.create( 
                                from_='whatsapp:+14155238886',  
                                body=message,
                                to=phone_number
                            ) 
    return messagess

if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server
    launch_server(port=8005)

    



