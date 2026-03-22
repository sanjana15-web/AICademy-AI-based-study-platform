from youtube_transcript_api import YouTubeTranscriptApi

from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document


def extract_video_id(url):
    """
    Extract video ID from YouTube URL
    """
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]

    if "youtu.be" in url:
        return url.split("/")[-1]

    raise ValueError("Invalid YouTube URL")


def get_transcript(video_id):

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = " ".join([t["text"] for t in transcript])

    return text


def summarize_text(text):

    docs = [Document(page_content=text)]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    docs = splitter.split_documents(docs)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    chain = load_summarize_chain(
        llm,
        chain_type="map_reduce"
    )

    summary = chain.run(docs)

    return summary


if __name__ == "__main__":

    url = input("Enter YouTube URL: ")

    video_id = extract_video_id(url)

    print("\nFetching transcript...")

    text = get_transcript(video_id)

    print("Generating summary...\n")

    summary = summarize_text(text)

    print("====== SUMMARY ======\n")
    print(summary)