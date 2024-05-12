# PUEDES MODIFICAR LOS DATOS DE ESTE COMANDO VISITANDO EL ARCHIVO llmConfig.json EN LA CARPETA PRINCIPAL 'config'
from moduls.utils.utils import load_json
from pyrogram import Client, filters

CONFIG = load_json("llmConfig")

@Client.on_message(filters.command(CONFIG["COMMAND"], CONFIG["prefixes"]))
async def llmUse(clientC, responseR, postdata=0):
    """The postdata must be have the follow syntax:
- <COMMAND_CONFIG>-<param>

Sample:

- llm-rm"""

    TEXT = responseR.text.split()
    ID_CHAT = responseR.chat.id
    COMANDO = " ".join(TEXT[1:]) if len(TEXT) > 1 else None

    if not COMANDO:
        await responseR.reply(CONFIG["manual"])
    
    else:
        await responseR.reply(COMANDO)