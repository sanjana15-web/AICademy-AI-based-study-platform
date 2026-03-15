# every feature will be treated as class 
    # for that particular feature provided study source will be treated as obj
    # ex pdf provided then obj-pdf of class pdf will be created and then all further operation will be based on class defination 


# some of the functions like embedding , storing data into chroma , retriver will be witten into base class and all other features will inherit the base
# system prompts will be taken for sys_propots which is later editable
# 


#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
from langchain_community.document_loaders import PyPDFLoader

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
