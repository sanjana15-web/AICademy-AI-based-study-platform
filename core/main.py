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

from pypdf import PdfReader  # For PDF
import pandas as pd          # For DataFrame
from typing import List      # For type hints
import time                  # For sleep


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


class WebScraper:
    """Web scraping for educational content"""
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_single_url(self, url: str) -> List[str]:
        """Scrape one URL (HTML/PDF) - core from your notebook"""
        try:
            if url.lower().endswith('.pdf'):
                resp = requests.get(url, stream=True, timeout=20, headers=self.headers)
                resp.raise_for_status()  # ✅ ADD THIS: check HTTP errors
                reader = PdfReader(resp.raw)
                texts = []
                for page in reader.pages:
                    t = page.extract_text()
                    if t and 60 < len(t) < 1000:
                        texts.append(' '.join(t.split()))
                return texts
            else:
                resp = requests.get(url, headers=self.headers, timeout=self.timeout)
                resp.raise_for_status()  # ✅ ADD THIS: check HTTP errors
                soup = BeautifulSoup(resp.text, 'html.parser')
                # Clean: remove script/style/nav
                for tag in soup(['script', 'style', 'nav', 'footer']):
                    tag.decompose()
                texts = []
                for el in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']):
                    text = el.get_text(strip=True)
                    if 60 < len(text) < 500:
                        texts.append(text)
                return texts
        except Exception as e:
            print(f"Scrape error for {url}: {e}")  # ✅ BETTER ERROR MSG
            return []

    def scrape_multiple(self, urls: List[str]) -> pd.DataFrame:
        """Main method: Scrape list of URLs"""
        records = []
        for url in urls:
            print(f"Scraping {url}")
            texts = self.scrape_single_url(url)
            for t in texts:
                records.append({'text': t, 'url': url})
            time.sleep(1.5)  # Rate limit
        return pd.DataFrame(records)
