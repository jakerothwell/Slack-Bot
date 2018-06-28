import os
import time
import re
from slackclient import SlackClient
from datetime import datetime, timedelta


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
auth_token = SlackClient(os.environ.get('AUTH_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
SLEEP_TIME = 30
SLACK_CHANNEL_NAME = "slackbot_test"
HELP_COMMAND = "help"
STATUS_COMMAND = "status"
DETAILS_COMMAND = "details"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
LEVEL_UP_THRESHOLD = 66
LEVEL_DOWN_THRESHOLD = 33
STATES = ('content','sleepy','inquisitive','emotive','hard-working','silly')


class Bot:
    def __init__(self, state, level):
        
        self.state = state
        self.level = level
        # Read bot's user ID by calling Web API method `auth.test`
        self.id = slack_client.api_call("auth.test")["user_id"]

    def get_state(self):
        return self.state

    def get_level(self):
        return self.level

def parse_bot_commands(slack_events, bot):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == bot.id:
                
                print("bot command found")
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

def status_update(channel, bot):
    file_name = "Sprites/" + bot.get_state() + str(bot.get_level()) +  ".gif"
    print(file_name)
    response = "I am currently level " + str(bot.get_level()) + " and in " + bot.get_state() + " state."
    slack_client.api_call(
        "files.upload",
        channels=channel,
        as_user=True,
        filename="status.gif",
        initial_comment=response,
        file=open(file_name, "rb"),
    )

def handle_command(command, channel, bot):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(HELP_COMMAND)

    # Finds and executes the given command, filling in response
    response = None

    status = False

    # This is where you start to implement more commands!
    if command.startswith(HELP_COMMAND):
        response = "Try the status or details commands"
    elif command.startswith(STATUS_COMMAND):
        print("status")
        response = "I am currently level " + str(bot.get_level()) + " and in " + bot.get_state() + " state."
        status = True
    elif command.startswith(DETAILS_COMMAND):
        response = "Current favourite user(s) - \nCurrent neglectful user(s) - \n# of links sent - \n# of media uploaded - \n# of questions asked - \n# of questions answered -"

    if not status:
        # Sends the response back to the channel
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

    # Sends a status image back to the channel if requested
    else:
        status_update(channel, bot)

def convert_timestamp(ts):

    t1 = datetime.fromtimestamp(
                float(ts)
            ).strftime('%Y-%m-%d %H:%M:%S')
    return t1


def message_alerts(channel, bot):
    
        history = auth_token.api_call("channels.history", channel=channel)        
        msglist = history['messages']
        val = bot.id
        
        latest_ts = 0
        latest_msg = None
        
        for d in msglist:
            
            user_id, message = parse_direct_mention(d['text'])
            #print(user_id)
            ts = float(d['ts'])
            
            if 'bot_id' in d: 
                pass
                
            elif user_id == bot.id:
                #print("direct mention found")
                pass

            elif ts > float(latest_ts):
                latest_ts = ts
                latest_msg = d
            
            
           
        
        #print(latest_msg)
        
        latest = convert_timestamp(latest_ts)
        latest = datetime.strptime(latest, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        #print(latest)
        
        time_difference = now-latest
        print(time_difference)
        
        if(time_difference > timedelta(seconds=SLEEP_TIME)):
            
            bot.state = 'sleepy'
            response="ChitChet is now feeling sleepy. zzzzz...."
            
        else:
            
            bot.state = 'content'
            response = "ChitChet is now content. :D"
        
        
        slack_client.api_call(
                "chat.postMessage",
                channel=channel,    
                text=response or default_response
            )
        
        
if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        
        print("Starter Bot connected and running!")
        
        bot = Bot("content", 1)
        channels = slack_client.api_call("channels.list")
        channel_id = None
        

        #find the channel we want
        for channel in channels['channels']:
            if channel['name'] == SLACK_CHANNEL_NAME:
                channel_id = channel['id']
        if channel_id == None:
            raise Exception("cannot find channel " + channel_name)
        print("Got a channel! " + channel_id)

        while True:
            
            events = slack_client.rtm_read()
            command, channel = parse_bot_commands(events, bot)
            message_alerts(channel_id, bot)
            if command:
                
                handle_command(command, channel, bot)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


