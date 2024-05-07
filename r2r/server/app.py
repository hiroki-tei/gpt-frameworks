from os.path import dirname
from r2r.main import E2EPipelineFactory, R2RConfig, configure_logging
from r2r.pipelines import BasicIngestionPipeline
from r2r.core.ingestors import Ingestor
from r2r.core import (
    IngestionType,
    DocumentPage
)
from typing import Union
import json
import string
from io import BytesIO
from typing import Any, Generator, Generic, TypeVar, Union
import uvicorn

path = f"{dirname(__file__)}/configs/default.json"


class CustomIngestionPipeline(BasicIngestionPipeline):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingestors[IngestionType.PDF] = CustomPDFAdapter()

    def process_data(self, entry_type: IngestionType, entry_data: Union[bytes, str]):
        if entry_type not in self.ingestors:
            raise ValueError(
                f"Ingestor for {entry_type} not found in `BasicIngestionPipeline`."
            )
        Ingestor = self.ingestors[entry_type]
        texts = Ingestor.ingest(entry_data)
        for iteration, text in enumerate(texts):
            yield DocumentPage(
                document_id=self.document_id,
                page_number=iteration,
                text=text,
                metadata=self.metadata,
            )

class CustomPDFAdapter(Ingestor[str]):
    def __init__(self):
        from pypdf import PdfReader
        self.PdfReader = PdfReader

    def ingest(self, data: bytes) -> Generator[str, None, None]:
        pdf = self.PdfReader(BytesIO(data))
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text is not None:
                yield page_text

app = E2EPipelineFactory.create_pipeline(
    config=R2RConfig.load_config(path),
    ingestion_pipeline_impl=CustomIngestionPipeline
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
