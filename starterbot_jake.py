import os
import time
import re
from slackclient import SlackClient 
from datetime import datetime, timedelta

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
SLACK_CHANNEL_NAME = "slackbot_test"
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None
#channel_name = os.environ["SLACK_CHANNEL_NAME"]

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
    	if event["type"] == "message" and not "subtype" in event:
    		user_id, message = parse_direct_mention(event["text"])
    		if user_id == starterbot_id:
    			return message, event["channel"]

    return None, None



def parse_direct_mention(message_text):
    
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """

    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    info = slack_client.api_call("channels.info", channel=channel)
    print(channel)
    print(info)
    channel = info['channel']
    latest = channel['latest']
    ts = latest['ts']  
            
    t2 = datetime.now()
    t1 = datetime.fromtimestamp(
                float(ts)
            ).strftime('%Y-%m-%d %H:%M:%S')
            
    t1 = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
            
    print(t1)
    print(t2)
    print(t2-t1)
    
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


def message_alerts(channel):
    
        info = slack_client.api_call("channels.info", channel=channel)
        
        #print(info)           
        chan = info['channel']
        latest = chan['latest']
        ts = latest['ts']  
            
        t2 = datetime.now()
        t1 = datetime.fromtimestamp(
                float(ts)
            ).strftime('%Y-%m-%d %H:%M:%S')
            
        t1 = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
            
        #print(t1)
        #print(t2)
        time_difference = t2-t1
        print(time_difference)
        response="ALERT! NO MESSAGES HAVE BEEN SENT IN 1 MINUTE! TALK MORE!"
        x = 100
        if(time_difference > timedelta(minutes=1)):
            
            #print("true")
            slack_client.api_call(
                "chat.postMessage",
                channel=channel,    
                text=response or default_response
            )

           
        

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")


        channels = slack_client.api_call("channels.list")
        channel_id = None
        

        #find the channel we want
        for channel in channels['channels']:
            if channel['name'] == SLACK_CHANNEL_NAME:
                channel_id = channel['id']
        if channel_id == None:
            raise Exception("cannot find channel " + channel_name)
        print("Got a channel! " + channel_id)



        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            
            command, channel = parse_bot_commands(slack_client.rtm_read())
            message_alerts(channel_id)
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

