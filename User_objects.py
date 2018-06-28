import os
import time
import re
from slackclient import SlackClient

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

#get name for private channel
group_name = os.environ.get('SLACK_GROUP_NAME')

# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

#TEMPORARY GLOBAL
group_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

class User:
    #initialze a user
    def __init__(self, id):
        self.files_shared = 0
        self.links_shared = 0
        self.reactions_made = 0
        self.questions_asked = 0
        self.questions_answered = 0
        #use in combination with group id to identify each user
        self.id = id

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
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

def get_group_id():
    """
        Get the id for the private channel
    """
    groups = slack_client.api_call("groups.list")
    for group in groups['groups']:
        if group['name'] == group_name:
            group_id = group['id']
    if group_id == None:
        raise Exception("cannot find private channel " + group_name)

def get_users():
    """
        Creates a user object for each user in the channel
        to track their activity
        Returns a list of the users
    """
    users = []
    group = slack_client.api_call(
        "groups.info",
        channel=group_id
    )
    for member in group["group"]["members"]
        users.append(User(member))
    return users

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        get_group_id()
        users = get_users()
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
