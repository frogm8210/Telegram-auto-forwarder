
import asyncio
from telethon.sync import TelegramClient
from telethon.errors import ChatIdInvalidError


class TelegramForwarder:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)

    async def forward_messages_to_channel_pairs(self, chat_pairs, keywords, signature):
        await self.client.connect()

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        # Adjusted to handle three values: source_id, destination_id, and topic_id
        last_message_ids = {source_id: (await self.client.get_messages(source_id, limit=1))[0].id for source_id, _, _ in chat_pairs}

        while True:
            print("Checking for messages and forwarding them...")
            for source_chat_id, destination_chat_id, topic_id in chat_pairs:
                # Get new messages since the last checked message for the current source chat
                messages = await self.client.get_messages(source_chat_id, min_id=last_message_ids[source_chat_id], limit=None)

                for message in reversed(messages):
                    if keywords:
                        if message.text and any(keyword in message.text.lower() for keyword in keywords):
                            print(f"Message contains a keyword: {message.text}")
                            await self.forward_message(destination_chat_id, message.text, signature, topic_id)
                    else:
                        await self.forward_message(destination_chat_id, message.text, signature, topic_id)

                    last_message_ids[source_chat_id] = max(last_message_ids[source_chat_id], message.id)

            await asyncio.sleep(5)

    async def forward_message(self, destination_chat_id, message_text, signature, topic_id=None):
        try:
            entity = await self.client.get_input_entity(destination_chat_id)

            # Convert topic ID if it's out of valid range
            if topic_id is not None:
                topic_id = self.convert_to_signed_integer(topic_id)
                # Only proceed if topic_id is valid
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
        """Convert an unsigned integer to a signed integer."""
        if number > 2147483647:
            return number - 4294967296
        return number

    def is_valid_signed_integer(self, number):
        """Check if the number is within the valid range of a signed 32-bit integer."""
        return -2147483648 <= number <= 2147483647


# Function to read credentials from file
def read_credentials():
    try:
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            api_id = int(lines[0].strip())
            api_hash = lines[1].strip()
            phone_number = lines[2].strip()
            return api_id, api_hash, phone_number
    except FileNotFoundError:
        print("Credentials file not found.")
        return None, None, None

# Function to write credentials to file
def write_credentials(api_id, api_hash, phone_number):
    with open("credentials.txt", "w") as file:
        file.write(str(api_id) + "\n")
        file.write(api_hash + "\n")
        file.write(phone_number + "\n")

async def main():
    api_id, api_hash, phone_number = read_credentials()

    if api_id is None or api_hash is None or phone_number is None:
        api_id = input("Enter your API ID: ")
        api_hash = input("Enter your API Hash: ")
        phone_number = input("Enter your phone number: ")
        write_credentials(api_id, api_hash, phone_number)

    forwarder = TelegramForwarder(api_id, api_hash, phone_number)
    
    print("Choose an option:")
    print("1. List Chats")
    print("2. Forward Messages")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        await forwarder.list_chats()
    elif choice == "2":
        print("Enter pairs of source and destination chat IDs (e.g., 'source_id1:destination_id1:topic_id1, source_id2:destination_id2:topic_id2'):")
        chat_pairs_input = input("Enter the chat ID pairs (comma separated): ")
        
        # Adjusted to handle three values: source_id, destination_id, and topic_id
        chat_pairs = [tuple(map(int, pair.split(':'))) for pair in chat_pairs_input.split(",")]
        
        print("Enter keywords if you want to forward messages with specific keywords, or leave blank to forward every message!")
        keywords = input("Put keywords (comma separated if multiple, or leave blank): ").split(",")
        
        signature = input("Enter your signature: ")

        await forwarder.forward_messages_to_channel_pairs(chat_pairs, keywords, signature)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    jls_extract_var = asyncio
    jls_extract_var.run(main())
