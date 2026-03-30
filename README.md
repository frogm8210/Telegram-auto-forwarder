# Telegram-auto-forwarder

A Python-based automated message forwarding tool for Telegram that monitors source chats and channels, forwarding messages to destination channels with optional keyword filtering and custom signatures. Supports multiple chat pairs with topic/thread routing and handles Telegram's topic ID validation.

## Features

- ✅ **Multi-pair forwarding** – Forward from multiple source chats to multiple destinations
- ✅ **Keyword filtering** – Optional filtering to only forward messages containing specific keywords
- ✅ **Custom signatures** – Append signatures to forwarded messages
- ✅ **Topic support** – Route messages to specific Telegram topics/threads
- ✅ **Async architecture** – Built with asyncio and Telethon for efficient operation
- ✅ **Polling-based** – Continuously monitors for new messages with 5-second intervals

## Requirements

- Python 3.7 or higher
- Telegram API credentials (API ID and API Hash)
- Your Telegram phone number

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/frogm8210/Telegram-auto-forwarder.git
   cd Telegram-auto-forwarder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Telegram API credentials**
   - Go to https://my.telegram.org/apps
   - Log in with your Telegram account
   - Create a new application
   - Copy your **API ID** and **API Hash**

## Usage

### First-time Setup

Run the script for the first time:
```bash
python main.py
```

On first run, you'll be prompted to enter:
- **API ID** – From https://my.telegram.org/apps
- **API Hash** – From https://my.telegram.org/apps
- **Phone Number** – Your Telegram phone number (with country code, e.g., +1234567890)

These credentials will be saved to `credentials.txt` for future runs.

### Running the Forwarder

1. Execute the script:
   ```bash
   python main.py
   ```

2. Choose an option:
   ```
   Choose an option:
   1. List Chats
   2. Forward Messages
   ```

3. **Option 1 - List Chats:** Displays all your available chats and channels (useful for finding chat IDs)

4. **Option 2 - Forward Messages:** 
   - Enter chat ID pairs in the format: `source_id:destination_id:topic_id` (comma-separated for multiple pairs)
     - `source_id` – Chat/channel to monitor
     - `destination_id` – Chat/channel to forward to
     - `topic_id` – Telegram topic/thread ID (use 0 if no specific topic)
   
   - Example:
     ```
     -1001234567890:987654321:0, -1009876543210:123456789:5
     ```

5. **Enter keywords** (optional):
   - Leave blank to forward ALL messages
   - Enter comma-separated keywords to filter messages
   - Example: `alert,important,urgent`

6. **Enter your signature**:
   - Text to append to every forwarded message
   - Example: `Forwarded by AutoBot`

The forwarder will then continuously monitor the source chats and forward matching messages every 5 seconds.

## How to Get Chat IDs

1. Run the script and select option `1. List Chats`
2. The script will display all your chats with their IDs
3. Use these IDs in the forwarding configuration

## Configuration File

Your credentials are saved in `credentials.txt` in the following format:
```
<API_ID>
<API_HASH>
<PHONE_NUMBER>
```

⚠️ **Keep this file secure** – It contains your Telegram credentials!

## Example Workflow

```
$ python main.py

Choose an option:
1. List Chats
2. Forward Messages

Enter your choice: 2
Enter pairs of source and destination chat IDs (e.g., 'source_id1:destination_id1:topic_id1, source_id2:destination_id2:topic_id2'):
Enter the chat ID pairs (comma separated): -1001234567890:987654321:0
Enter keywords if you want to forward messages with specific keywords, or leave blank to forward every message!
Put keywords (comma separated if multiple, or leave blank): 
Enter your signature: Forwarded by AutoBot

Checking for messages and forwarding them...
```

## Error Handling

The forwarder handles common errors:
- **Invalid chat ID** – Logs error and continues
- **Invalid topic ID** – Skips invalid topic IDs
- **Authentication failure** – Prompts for 2FA code
- **Network errors** – Continues monitoring

## Troubleshooting

- **"Credentials file not found"** – Run the script again to create credentials
- **"Invalid chat ID"** – Verify the chat ID using Option 1 (List Chats)
- **Messages not forwarding** – Check if keywords are too restrictive or source chat has no new messages

## License

This project is for personal use only.
