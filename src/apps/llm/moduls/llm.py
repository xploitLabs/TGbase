import google.generativeai as genai
from moduls.utils.utils import load_json

CONFIG = load_json("llmConfig")
genai.configure(api_key=CONFIG["API_KEY"])
model = genai.GenerativeModel(model_name=CONFIG["model"],
                              generation_config=CONFIG["config_model"],
                              safety_settings=CONFIG["security"])

async def iaSpeech(CONTEXT):
    response = await model.generate_content_async(CONTEXT)
    return response.text