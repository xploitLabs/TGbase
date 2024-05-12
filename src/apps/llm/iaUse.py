# PUEDES MODIFICAR LOS DATOS DE ESTE COMANDO VISITANDO EL ARCHIVO llmConfig.json EN LA CARPETA PRINCIPAL 'config'
from moduls.utils.utils import load_json, loading_message
from pyrogram import Client, filters
from apps.llm.moduls import llm
import json, os
from pyrogram.enums import ChatType 

CONFIG = load_json("llmConfig")

@Client.on_message(filters.command(CONFIG["COMMAND"], CONFIG["prefixes"]))
async def llmUse(clientC, responseR, postdata=0):
    """The postdata must be have the follow syntax:
- <COMMAND_CONFIG>-<param>

Sample:

- llm-rm"""

    TEXT = responseR.text.split()
    ID_CHAT = responseR.chat.id
    
    NAME = responseR.from_user.username if responseR.chat.type == ChatType.PRIVATE else responseR.chat.title
    PROMPT = " ".join(TEXT[1:]) if len(TEXT) > 1 else None

    if not PROMPT:
        await responseR.reply(CONFIG["manual"])
    
    else:
        CHATS = [f.split(".")[0] for f in os.listdir(CONFIG["DIR_CHATS"])]

        PROMPT_INIT = CONFIG["PROMPT"]

        if str(ID_CHAT) in CHATS:

            CONTEXT = json.load(open(f"{CONFIG['DIR_CHATS']}/{ID_CHAT}.json", "r"))
            CONTEXT["chat"] += [f"{CONFIG['name_USER']}: {PROMPT}", f"{CONFIG['name_LLM']}: "]
            TEMPORAL = CONTEXT["chat"].copy()
            TEMPORAL.insert(0, PROMPT_INIT)

            sticker = await loading_message(responseR, CONFIG["sticker_loading"])
            responseIA = await llm.iaSpeech(TEMPORAL)
            await sticker.delete()

            await responseR.reply(responseIA)

            CONTEXT["chat"][-1] += responseIA
            json.dump(CONTEXT, open(f"{CONFIG['DIR_CHATS']}/{ID_CHAT}.json", "w"), indent=4)

        else:
            plantilla = {
                "chat": [
                    f"{CONFIG['name_USER']}: {PROMPT}",
                    f"{CONFIG['name_LLM']}: "
                ]
            }

            if responseR.chat.type == ChatType.PRIVATE:
                plantilla["username"] = NAME
            elif responseR.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
                plantilla["Title Group"] = NAME

            TEMPORAL = plantilla["chat"].copy()
            TEMPORAL.insert(0, PROMPT_INIT)

            sticker = await loading_message(responseR, 0)
            responseIA = await llm.iaSpeech(TEMPORAL)
            await sticker.delete()

            await responseR.reply(responseIA)

            plantilla["chat"][-1] += responseIA
            json.dump(plantilla, open(f"{CONFIG['DIR_CHATS']}/{ID_CHAT}.json", "w"), indent=4)