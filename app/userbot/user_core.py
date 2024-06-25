from typing import List
import re
from datetime import datetime, timedelta
from pyrogram import Client
from pyrogram.types import Message
from app.gpt.controller import GPTController
from app.core.settings import get_settings

def remove_links(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[@#]\w+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

async def get_post_list(app: Client, chat_id: str, limit: int) -> List[Message]:
    result = []
    now = datetime.now()
    triggers = get_settings().env.trigger_words
    yesterday = now - timedelta(days=1)
    
    async with app:
        try:
            async for post in app.get_chat_history(
                chat_id=chat_id,
                limit=limit,
                offset_date=now
            ):
                if post.date >= yesterday:
                    if post.text and any(map(lambda x : x.lower() in post.text.lower(), triggers)):
                        continue
                    elif post.caption and any(map(lambda x : x.lower() in post.caption.lower(), triggers)):
                        continue
                    elif (post.photo or post.video) and not post.caption:
                        continue
                    else:
                        result.append(post)
                else:
                    break
        except:
            print(f"Канала {chat_id} не существует")
    return result
            

async def collect_post(app : Client, limit : int, chats : List[str]) -> List[Message]:
    result = []
    for chat in chats:
        posts = await get_post_list(
        app=app,
        chat_id=chat,
        limit=limit)
        result.extend(posts)
    return result

async def convert_message(app : Client, chat_id: int, message: Message, gpt : GPTController, prompt : str) -> str:
    if message.text:
        return gpt.paraphrase_text(remove_links(message.text), prompt=prompt) if message.caption else "", message.entities,
    
    elif message.photo:
        return gpt.paraphrase_text(remove_links(message.caption), prompt=prompt) if message.caption else "", message.caption_entities

    elif message.video:
        return gpt.paraphrase_text(remove_links(message.caption), prompt=prompt) if message.caption else "", message.caption_entities
  
    elif message.document:
        return gpt.paraphrase_text(remove_links(message.caption), prompt=prompt) if message.caption else "", message.caption_entities
    else:
        return "None"

async def send_message(app : Client, chat_id: int, message: Message, gpt : GPTController, prompt : str):
    async with app:
        if message.text:
            try:
                print(f"Сообщение до обработки {message.text}")
                text = gpt.paraphrase_text(remove_links(message.text), prompt=prompt) if message.text else ""
                await app.send_message(
                chat_id,
                text= text,
                entities= None,
                reply_markup=message.reply_markup
            )
                print(f"Сообщение после обработки {text}")
                
            except Exception as e:
                print(e)
                
        elif message.photo:
            try:
                print(f"Сообщение до обработки {message.caption}")
                text = gpt.paraphrase_text(remove_links(message.caption), prompt=prompt) if message.caption else ""
                await app.send_photo(
                chat_id,
                photo=message.photo.file_id,
                caption= text,
                caption_entities= None,
                reply_markup=message.reply_markup,
                disable_notification=True
        )
                print(f"Сообщение после обработки {text}")
                
            except Exception as e:
                print(e)
                
        elif message.video:
            try:
                print(f"Сообщение до обработки {message.caption}")
                text = gpt.paraphrase_text(remove_links(message.caption), prompt=prompt) if message.caption else ""
                await app.send_video(
            chat_id,
            video=message.video.file_id,
            caption= gpt.paraphrase_text(remove_links(message.caption), prompt=prompt) if message.caption else "",
            caption_entities= None,
            reply_markup=message.reply_markup,
            disable_notification=True
        )
                print(f"Сообщение после обработки {text}")
                
            except Exception as e:
                print(e)
                
        elif message.document:
            try:
                await app.send_document(
            chat_id,
            document=message.document.file_id,
            caption=gpt.paraphrase_text(remove_links(message.caption), prompt=prompt) if message.caption else "",
            caption_entities= None,
            reply_markup=message.reply_markup,
            disable_notification=True
        )
            except Exception as e:
                print(e)
                
        elif message.sticker:
            await app.send_sticker(
            chat_id,
            sticker=message.sticker.file_id,
            disable_notification=True
        )
        elif message.animation:
            try:
                await app.send_animation(
            chat_id,
            animation=message.animation.file_id,
            caption=gpt.paraphrase_text(remove_links(message.caption), prompt=prompt) if message.caption else "",
            caption_entities= None,
            reply_markup=message.reply_markup,
            disable_notification=True
        )
            except Exception as e:
                print(e)
                
        elif message.video_note:
            await app.send_video_note(
            chat_id,
            video_note=message.video_note.file_id,
            reply_markup=message.reply_markup,
            disable_notification=True
        )
        else:
            print("Не удалось обработать сообщение.")
        