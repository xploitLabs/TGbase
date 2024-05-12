from pyrogram import Client
from moduls.utils.utils import getVAR, load_json

from apps.basics import welcome
from apps.basics import api_sample

from apps.llm import iaUse

CONFIG_LLM = load_json("llmConfig")

@Client.on_callback_query()
async def controler(cliente, data_response):
    data = data_response.data
    function_name, postdata = data.split("-")[0], 0 if len(data.split("-")) == 1 else data.split("-")[1]

    if data_response.message.reply_to_message.from_user.id == data_response.from_user.id:
        if postdata.startswith("VAR"):
            postdata = getVAR(postdata)

        else:
            postdata = int(postdata) if str(postdata).isdigit() else postdata

        if function_name == "start":
            await welcome.start(cliente, data_response.message, postdata)

        elif function_name == "ipQ":
            await api_sample.ipQuery(cliente, data_response.message, postdata)

        elif function_name == "rm":
            await data_response.message.delete()

        elif function_name == CONFIG_LLM["COMMAND"]:
            await iaUse.llmUse(cliente, data_response.message, postdata)

        else:
            await cliente.answer_callback_query(
                callback_query_id=data_response.id,
                text=f"""⚠️ Function not set.\nFunction: {function_name}, postdata: {postdata}""",
                show_alert="true"
            )
    else:
        await cliente.answer_callback_query(
            callback_query_id=data_response.id,
            text=f"""⚠️ This button belongs to another user.\nFunction: {function_name}, postdata: {postdata}""",
            show_alert="true"
        )
