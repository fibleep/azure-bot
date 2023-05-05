# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from message_parser import MessageParser

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    # See https://platform.openai.com/docs/tutorials/web-qa-embeddings for parsing information
    
    def __init__(self) -> None:
        super().__init__()
        self.parser = MessageParser()

    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(f"{self.parser.promptOpenAi(turn_context.activity.text)}")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello! I have knowledge about a certain website, ask me questions about it!")

