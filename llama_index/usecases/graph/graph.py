from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

langfuse_callback_manager = LlamaIndexCallbackHandler()
Settings.callback_manager = CallbackManager([langfuse_callback_manager])

# loading data
#from llama_index.core import SimpleDirectoryReader
#documents = SimpleDirectoryReader("data/interest/mbti").load_data()

from llama_index.readers.web import SimpleWebPageReader
documents = SimpleWebPageReader(html_to_text=True).load_data(
    ["https://iemone.jp/article/lifestyle/chian_431810/"]
)

from llama_index.llms.openai import OpenAI
from llama_index.core import PropertyGraphIndex
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

from typing import Literal

llm = OpenAI(model="gpt-4o")

entities = Literal["PERSON"]
relations = Literal["EX_LOVER", "FINAL_LOVER", "FRIEND"]
schema = {
    "PERSON": ["EX_LOVER", "FINAL_LOVER", "FRIEND"],
}
schema_extractor = SchemaLLMPathExtractor(
    llm = llm,
    possible_entities=entities,
    possible_relations=relations,
    kg_validation_schema=schema,
    strict=True,  # if false, will allow triples outside of the schema
    num_workers=2,
    #max_paths_per_chunk=10,
    #show_progres=False,
)
index = PropertyGraphIndex.from_documents(documents, kg_extractors=[schema_extractor])

# uncomment here if you want to visualize the graph
#index.property_graph_store.save_networkx_graph(name="./usecases/graph/kg.html")

retriever = index.as_retriever(
    include_text=False,  # include source text, default True
)

nodes = retriever.retrieve("番組「LOVE TRANSIT」に出演したたかあきの元彼女と、たかあきが最終的に告白した人の名前をそれぞれ教えて(EX_LOVER, FINAL_LOVERは１人しかいない)")

for node in nodes:
    print(node.text)

#index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(
    include_text=False
)

response = query_engine.query("番組「LOVE TRANSIT」に出演したたかあきの元彼女と、たかあきが最終的に好きになった人の名前をそれぞれ教えて(EX_LOVER, FINAL_LOVERは各１人しかいない)")

print(str(response))
