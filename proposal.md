# SENG 435 Project Proposal
Alison Goshulak V00806939 | Jake Rothwell V00813277 | Jonathan Grandfield V00823227

***Abstract* -The problem domain is to identify and develop a solution for encouraging collaboration in Slack, in the form of a bot which would change state based on the activity of the channel.**

## Problem Description
Our project proposal is to develop a bot, which we are calling ChitChet for now, to support collaboration. The target application is Slack, where the users would be any group or team wanting to increase activity in their channel. The main technique for promoting activity would be gamification, where members of the group are encouraged to participate in the Slack channel to maintain the well being or “level” of the bot. The gamification elements are encompassed by the bot’s state - where the bot would be “upgraded” to a healthier state when the channels activity increases. Another goal we have for ChitChet is to have it evolve based on the different types of activity occurring on the channel. For instance, the bot could enter an “inquisitive” state if many questions are detected within the channel. As a deterrent from letting a channel grow “stale” (depending on the needs of the particular channel) penalties for long periods of inactivity could be represented as the bot becoming unhappy, sick, and potentially even losing progress by devolving.

## Project Goals
The first major development milestone will be the brainstorming phase. As a group we need to generate a list of possible features and actions that ChitChet is able to perform, as well as the different states that the bot could be in. In order to achieve this, we can analyze other similar projects for inspiration. It is also important that we define a clear set of use cases within a domain, as well as a manageable scope. There is high potential for feature creep with an open ended project of this nature, so we must make sure to define a clear domain. After we solidify a list of features for the Slack bot, the next step will be learning and successfully implementing the Slack API using Python in order to parse the Slack commands and channel state.  Assets used to represent the varying states of ChitChet will also need to be created in order for the user to become more invested in the bot. 
Due to the potentially large scope of this collaborative bot, an important goal that we have set is to provide a customizable interface to allow administrators to pick which features they would like to use based on a number of factors, including:
* Group size
* Level of synchronicity
* Specific goals or personal preferences of the group and its administrators

To elaborate, a larger group would most likely prefer to set different parameters than a smaller group might, such as the number of messages ChitChet would consider adequate to be posted in a period of time. The bot should be customisable in order to act differently based on the level of synchronicity between group members. For instance, the bot should not pester the group to collaborate synchronously if group members are asynchronous due to differing time zones, schedules, or locations.

Another issue we need to address early in development is the amount of information (textually or visually) to be displayed by the bot. We need to find a balance between cluttering the channel with too much information and giving too little information to let the user tell the bots general state at a glance. A solution we are considering is to display a limited amount of information (probably through the caricature of ChitChet itself) and to let the users find out more about the status of the bot by either a direct user request or by a scheduled update. We will assess how well we have achieved this balance during the evaluation stage through feedback from the surveys (discussed later in the report).

## Implementation
As noted previously, we will be using the Slack API in conjunction with Python in order to implement the Slack bot, and we will be using Piskel for artwork. Some available features for the bot will include:

Alerting the channel if no messages have occured in x hours
Changing state to “inquisitive” if x questions have been asked in the last x hours
“Evolving” based on the content of the channel - links, polls, documents, etc.

After the brainstorming phase, which we plan on having complete within the next week, the next step will be a large amount of articulation work involving learning the Slack API in order to implement some proposed features. Once we have a solid set of features implemented, we want to mimic an agile style of development in order to continually iterate upon our bot with the goal of refining our set of use cases.

## Evaluation
After we have completed the implementation of ChitChet, or at least a working prototype with a set of basic features, the next step will be to evaluate how well the bot operates, and to determine if the bot is an adequate solution to our problem statement. Methods of evaluation we have brainstormed include user testing of the prototype, which may involve inviting a subset of users in a Slack channel with the bot active and providing them with sample dialogue or allowing for natural, dynamic dialog. Observations would be recorded and analyzed during the session, while surveys would be taken from the participants afterwards to gather evaluation data. Along with making observations, we may include mouse tracking technology in the tests to measure if the productivity of the participants decreases while the bot is active.

## Anticipated Risks
There are a few risks we think could occur in the development of ChitChet. First, the bot we design could end up being annoying to the users and disruptive to their work. This could lead to some users avoiding the Slack channel containing the bot, which would mean less participation from users, counter to our design goals. In a corporate environment, the gamification aspects of ChitChet, such as any incentives to level-up it up, could distract employees from other important job responsibilities. Also, channel users could abuse the system by posting tons of meaningless information and messages to receive rewards from the bot, counterproductive to meaningful collaboration. Finally, a risk we foresee for our planned evaluation methods is that the tracking technology could be too intrusive to our test participants, possibly discouraging them from taking part in the tests at all.

