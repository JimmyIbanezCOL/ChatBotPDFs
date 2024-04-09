import os
import chromadb
import PyPDF2
from document import Document
import uuid

def create_embeddings(chatbot_id, file_name):
    #Extraer texto del pdf
    with open(os.path.join('pdf_files',file_name), 'rb') as pdf_file:
        pdf_reader=PyPDF2.PdfReader(pdf_file)

        documents=[]
        for page_num,page in enumerate(pdf_reader.pages):
            document= Document(
                doc_id=str(uuid.uuid4()),
                content=page.extract_text(),
                metadata={'page_number':page_num}
            )
            print(document.id, document.content, document.metadata)
            documents.append(document)
        

    client=chromadb.Client()
    collection=client.create_collection('chatbot_id')
    collection.add