import asyncio
import os
from telethon.sync import TelegramClient
from telethon.errors import ChatIdInvalidError
from dotenv import load_dotenv  # For local testing

# Load environment variables from .env file (for local testing)
load_dotenv()

class TelegramForwarder:
    def __init__(self):
        self.api_id = int(os.getenv('API_ID'))
        self.api_hash = os.getenv('API_HASH')
        self.phone_number = os.getenv('PHONE_NUMBER')
        self.client = TelegramClient('session_' + self.phone_number, self.api_id, self.api_hash)

    async def forward_messages_to_channel_pairs(self, chat_pairs, keywords, signature):
        await self.client.connect()

        # Check authorization status
        if not await self.client.is_user_authorized():
            # Request code and handle `TELEGRAM_CODE`
            await self.client.send_code_request(self.phone_number)
            
            # Check if TELEGRAM_CODE is set
            telegram_code = os.getenv("TELEGRAM_CODE")
            if not telegram_code:
                print("Please set TELEGRAM_CODE as an environment variable with the login code sent to your Telegram.")
                return  # Exit if code is not set to allow updating the environment variable

            await self.client.sign_in(self.phone_number, telegram_code)

        # Dictionary to track the last message IDs processed for each source chat
        last_message_ids = {source_id: (await self.client.get_messages(source_id, limit=1))[0].id for source_id, _, _ in chat_pairs}

        while True:
            print("Checking for new messages to forward...")
            for source_chat_id, destination_chat_id, topic_id in chat_pairs:
                # Fetch new messages since the last checked message for each chat
                messages = await self.client.get_messages(source_chat_id, min_id=last_message_ids[source_chat_id], limit=None)

                for message in reversed(messages):
                    if keywords:
                        if message.text and any(keyword in message.text.lower() for keyword in keywords):
                            await self.forward_message(destination_chat_id, message.text, signature, topic_id)
                    else:
                        await self.forward_message(destination_chat_id, message.text, signature, topic_id)

                    # Update last processed message ID
                    last_message_ids[source_chat_id] = max(last_message_ids[source_chat_id], message.id)

            await asyncio.sleep(5)

    async def forward_message(self, destination_chat_id, message_text, signature, topic_id=None):
        try:
            entity = await self.client.get_input_entity(destination_chat_id)

            if topic_id is not None:
                topic_id = self.convert_to_signed_integer(topic_id)
                if self.is_valid_signed_integer(topic_id):
                    await self.client.send_message(entity, message_text + f"\n\n{signature}", reply_to=topic_id)
                    print(f"Message forwarded to topic {topic_id} in chat {destination_chat_id}")
                else:
                    print(f"Invalid topic ID: {topic_id}, skipping.")
            else:
                await self.client.send_message(entity, message_text + f"\n\n{signature}")
                print(f"Message forwarded to chat {destination_chat_id}")

        except ChatIdInvalidError:
            print(f"Invalid chat ID: {destination_chat_id}.")
        except Exception as e:
            print(f"Failed to forward to {destination_chat_id}: {e}")

    def convert_to_signed_integer(self, number):
        if number > 2147483647:
            return number - 4294967296
        return number

    def is_valid_signed_integer(self, number):
        return -2147483648 <= number <= 2147483647

async def main():
    # Replace these with your actual chat pairs for testing
    chat_pairs = [(123456789, 987654321, None)]  # Format: (source_id, destination_id, topic_id)
    keywords = ["keyword1", "keyword2"]  # Define keywords or leave empty to forward all messages
    signature = "Your Signature"  # Define any signature for forwarded messages

    forwarder = TelegramForwarder()
    await forwarder.forward_messages_to_channel_pairs(chat_pairs, keywords, signature)

if __name__ == "__main__":
    asyncio.run(main())
