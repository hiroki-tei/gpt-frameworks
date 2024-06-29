import os
from pathlib import Path
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

from chainlit.server import app
import chainlit as cl


repository_root = os.environ.get('HOME') + "/" + "Repository/private/gpt-frameworks" + "/"
docs_folder = repository_root + "raw_data" + "/" + "documents" + "/"
mbti_data_folder = docs_folder + "/interest/mbti"
print(mbti_data_folder)

@cl.on_chat_start
async def on_chat_start():
    documents = SimpleDirectoryReader(mbti_data_folder).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(streaming=True, similartity_top_k=3)
    cl.user_session.set("query_engine", query_engine)

@cl.on_message
async def on_message(message: cl.Message):
    query_engine = cl.user_session.get("query_engine")
    msg = cl.Message(content="")

    answer = query_engine.query(message.content)
    for part in answer.response_gen:
        await msg.stream_token(part)
    
    await msg.update()
