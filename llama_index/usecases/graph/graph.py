
# loading data
from llama_index.core import SimpleDirectoryReader
documents = SimpleDirectoryReader("data/interest/mbti").load_data()

from llama_index.llms.openai import OpenAI
from llama_index.core import PropertyGraphIndex
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

from typing import Literal

llm = OpenAI(model="gpt-4o")

entities = Literal["PERSONALITY", "STRENGTH", "WEAKNESS"]
relations = Literal["HAS", "IS_A"]
schema = {
    "PERSONALITY": ["HAS"],
    "STRENGTH": ["IS_A"],
    "WEAKNESS": ["IS_A"],
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

query_engine = index.as_query_engine(
    include_text=True,
)

response = query_engine.query("INTPの性格の強みと弱みを教えて")

print(str(response))
