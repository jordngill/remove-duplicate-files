from pyrogram import Client, filters 
from pyrogram.enums.messages_filter import MessagesFilter
import asyncio

# Edit your credentials here

api_id = 26763788
api_hash = '5bd46d55b597eeced05298b19ba786be'
session_str = 'BQGYYgwAt_acUeuvKUhGGC6ScPbOm1C2MZ-u4CWzaqRYZ6UFOECI3-Oz2Deyj5zL1MH6MCQyHHydo-xw6tEJ2lSFEVkSUZQX3LklafHCF6CAAdaxjr374UiQbCONUPBUfEnOx5dGCx_3hBFa7b0KNFMnCEtRpbmlpmKGU-Wne2SUwImvBXaL3v0m7tf1ZM3cgKLKfcqAf_U6YAuR2DI8OONKZ18kAp9Syt-u0SJToMTgqAY588X5HOEvCJObRGUzdIeEKcjqOe2FlzeHINVnzdS0pLKw54pjnv8c_CnW6ZUD_m2gh1az9JlZd6WTuNARqisC-XUvYNrlfKQKCgyGlVBgVy8RPgAAAAE2fl32AA'

app = Client('bot', api_id, api_hash, session_string=session_str)
print('Waiting for command...')

@app.on_message((filters.group | filters.channel) & filters.command(['remove_duplicate']))
async def remove(_, message):
    chat_id = message.chat.id

    messages = await app.search_messages_count(chat_id)
    videos = await app.search_messages_count(chat_id, filter=MessagesFilter.VIDEO)
    docs = await app.search_messages_count(chat_id, filter=MessagesFilter.DOCUMENT)
    audios = await app.search_messages_count(chat_id, filter=MessagesFilter.AUDIO)
    photos = await app.search_messages_count(chat_id, filter=MessagesFilter.PHOTO)

    print((
        f'Total messages : {messages} | '
        f'Documents : {docs} | '
        f'Videos : {videos} | '
        f'Audios : {audios} | '
        f'Photos : {photos}'
    ))

    existing_file_ids = []
    scanned, removed, failed = 0, 0, 0

    async for message in app.search_messages(chat_id):
        media = None

        if message.document:
            media = message.document

        elif message.video:
            media = message.video

        elif message.audio:
            media = message.audio

        elif message.photo:
            media = message.photo

        if media:
            file_id = media.file_unique_id

            if file_id not in existing_file_ids:
                existing_file_ids.append(file_id)

            else:
                try:
                    await message.delete()
                    removed += 1

                except Exception:
                    failed += 1

                finally:
                    await asyncio.sleep(2)

        scanned += 1
        print(f'Scanned : {scanned}/{messages} | Removed : {removed} | Failed : {failed}', end='\r' if scanned != messages else '\n')

        await asyncio.sleep(0.2)

app.run()


