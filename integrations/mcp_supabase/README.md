## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   Create a `.env` file in the project root with the following variables:
   ```
   SUPABASE_ACCESS_TOKEN=your_supabase_access_token
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   ```

4. **Run the script:**
   ```bash
   python main.py
   ```

   The script will run continuously, executing the main task every morning at 6:00 AM.

## Customization

- **Change Schedule:**  
  To run at a different time, modify the `hour` and `minute` in `scheduler.add_job` in `main.py`.

- **Change Telegram Message Format:**  
  Edit the formatting logic in the CrewAI task description or in the `send_telegram_message` function.

## How it Works

- At the scheduled time, the script:
  1. Connects to Supabase using the MCP server.
  2. Retrieves the last 5 records from the `habits` table.
  3. Summarizes the habits and selects a quote from "Atomic Habits".
  4. Sends the formatted summary to the configured Telegram chat.

## Requirements

- Python 3.12+
- Node.js (for MCP server)
- Supabase account and access token
- Telegram bot and chat ID