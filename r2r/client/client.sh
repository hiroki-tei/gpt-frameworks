#!/bin/bash

FILE_PATH=/path/to/file.pdf

function upload() {
  curl -X POST "http://localhost:8000/upload_and_process_file/" \
      -H "Content-Type: multipart/form-data" \
      -F "document_id=pdf_1" \
      -F "file=@${FILE_PATH}"
}

function search() {
  curl -X POST "http://localhost:8000/search/" \
       -H "Content-Type: application/json" \
       -d @./params/search.json
}

function rag_completion() {
  curl -X POST "http://localhost:8000/rag_completion/" \
       -H "Content-Type: application/json" \
       -d @./params/rag_completion.json
}

if [ "$1" = "upload" ]; then
  upload
elif [ "$1" = "search" ]; then
  search
elif [ "$1" = "rag_completion" ]; then
  rag_completion
fi
