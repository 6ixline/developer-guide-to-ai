from messages import Messages, Message
import tiktoken

class ConversationHistory:
    def __init__(self, system_message: Message):
        self.system_message = system_message
        self.message_history: Messages = []
    
    def add_messages(self, messages: Messages):
        self.message_history.extend(messages)

    def add_message(self, message: Message):
        self.message_history.append(message)

    def get_messages(self):
        messages = [self.system_message]
        messages.extend(self.message_history)

        return messages

    def count_tokens(self):
        encoding = tiktoken.get_encoding('cl100k_base')
        token_count = 0

        for message in self.get_messages():
            tokens = encoding.encode(message['content'])
            token_count += len(tokens)

        return token_count


    def trim_history(self):
        while self.count_tokens > 600 and len(self.message_history) >= 2:
            self.message_history = self.message_history[2:]
        