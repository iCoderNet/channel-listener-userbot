from pyrogram import Client, filters
from pyrogram.types import Message
from func import parse_to_json

api_id = '28077292'  # Telegram API ID
api_hash = 'de55ea73d0e1e9bf441f47ce23758048'  # Telegram API hash
CHANNELS = ['@CallAnalyser',"@icodernetuz", -1002474433707] # Список каналов

app = Client("userbot", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.chat(CHANNELS) & filters.text & filters.regex('First Call'))
def handle_new_message(client, message: Message):
    markdown_text = message.text.markdown
    parsed_json = parse_to_json(markdown_text)
    print(parsed_json)
    client.send_message("@NinetyDev", "```json\n" + str(parsed_json) + "\n```")

app.run()
