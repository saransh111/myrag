from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from huggingface_hub import login
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os

app = FastAPI()

class Item(BaseModel):
    query: str
    my_current_context : str

@app.get("/")
async def create_item():
    print("hello")
    return {
        "message": "Server Running",
    }

@app.post("/my_answers/")
async def create_item(item: Item):
    huggingface_embeddings=HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",      #sentence-transformers/all-MiniLM-l6-v2
        model_kwargs={'device':'cpu'},
        encode_kwargs={'normalize_embeddings':True}
    )
    vectorstore = FAISS.load_local("faiss_index/faiss_index", huggingface_embeddings, allow_dangerous_deserialization=True)
    retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":3})
    print(retriever)
    login(token="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")
    from langchain_huggingface import HuggingFaceEndpoint
    hf=HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-v0.1",
        temperature=0.2,
        model_kwargs={"max_length":100}
    )
    prompt_template="""
    Use the following piece of context to answer the question asked.
    Please try to provide the answer only based on the context

    {context}
    Question:{question}

    Helpful Answers:
    """
    prompt=PromptTemplate(template=prompt_template,input_variables=["context","question"])
    qa_with_sources = RetrievalQA.from_chain_type(llm=hf, 
                                                  chain_type="stuff",
                                                  chain_type_kwargs = {"prompt": prompt}, 
                                                  retriever=retriever,
                                                  return_source_documents=True)
    result = qa_with_sources.invoke({"query": item.query})
    ans=result['result']
    return {
        "message": "Item successfully created",
        "query": item.query,
        "answer": ans
    }

if __name__ == "__main__":
    print("drjhkfbgewsrk")
    uvicorn.run(app, host="127.0.0.1", port=8000)