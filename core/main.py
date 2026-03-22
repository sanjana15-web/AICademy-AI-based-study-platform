# every feature will be treated as class 
    # for that particular feature provided study source will be treated as obj
    # ex pdf provided then obj-pdf of class pdf will be created and then all further operation will be based on class defination 


# some of the functions like embedding , storing data into chroma , retriver will be witten into base class and all other features will inherit the base
# system prompts will be taken for sys_propots which is later editable
# 


#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.utilities import SerpAPIWrapper
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
#from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
# from langchain_ollama import OllamaEmbeddings, ChatOllama       //// if adding local agent 
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage,ToolMessage
import json
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class pdf :

    def _init_(self):
        pass 

    def pdf_loader(self , path ) :
        loader = PyPDFLoader(path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(pages)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=GOOGLE_API_KEY)
        vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})  
                
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=GOOGLE_API_KEY
        )
        rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)


    @tool
    def pdf_search(query: str) -> str:
         """Answer pdf questions using the loaded PDF."""
         return rag_chain.invoke(query)["result"]

    @tool
    def web_search(query: str) -> str:
        """Search the web using SerpAPI for up-to-date information."""
        try:
            search = SerpAPIWrapper()
            return search.run(query)
        except Exception as e:
            return f" Failed to search the web: {str(e)}"

    #tool binding
    llm_with_tools = llm.bind_tools([pdf_scholarship_search, web_search])


    ### interactive part starts





# youtube summarizer 
class YouTubeSummarizer:

    def __init__(self, url):
        self.url = url
        self.video_id = self.extract_video_id()
        self.docs = None


    def extract_video_id(self):

        # works for https://www.youtube.com/watch?v=VIDEO_ID
        return self.url.split("v=")[-1]


    def get_transcript(self):

        transcript = YouTubeTranscriptApi.get_transcript(self.video_id)

        text = " ".join([t["text"] for t in transcript])

        self.docs = [Document(page_content=text)]

        return self.docs


    def split_text(self):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )

        self.docs = splitter.split_documents(self.docs)

        return self.docs


    def summarize(self):

        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        chain = load_summarize_chain(
            llm,
            chain_type="map_reduce"
        )

        summary = chain.run(self.docs)

        return summary


if __name__ == "__main__":

    url = "https://www.youtube.com/watch?v=VIDEO_ID"

    yt = YouTubeSummarizer(url)

    yt.get_transcript()
    yt.split_text()

    result = yt.summarize()

    print("\nSummary:\n")
    print(result)