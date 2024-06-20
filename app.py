import streamlit as st
from dotenv import load_dotenv
load_dotenv()  # Load env variables
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi
import re
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a highly skilled AI specialized in summarizing YouTube video content. 
Your task is to create a comprehensive and detailed summary of the video based on its transcript. 
The summary should be structured in the following format:

1. **Introduction**: Briefly introduce the main topic and objectives of the video.
2. **Key Points**: List the main points discussed in the video, providing clear and concise explanations for each point.
3. **Subtopics and Details**: Break down the key points into subtopics, including important details and examples.
4. **Conclusion**: Summarize the conclusions or final thoughts presented in the video.

Please ensure the summary is detailed, well-organized, and captures the essence of the video. Aim for a length of around 250 words. Use bullet points where appropriate to enhance readability.

Here is the transcript text:
"""

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1].split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript_text, video_id
    except Exception as e:
        raise e

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# def display_transcript_with_timestamps(transcript_text, video_id):
#     st.markdown("## Transcript Timestamp")
#     for entry in transcript_text:
#         start = entry['start']
#         minutes, seconds = divmod(start, 60)
#         timestamp = f"{int(minutes):02d}:{int(seconds):02d}"
#         st.markdown(f"[{timestamp}](https://www.youtube.com/watch?v={video_id}&t={int(start)}s) {entry['text']}")

def perform_sentiment_analysis(transcript_text):
    sentiment = TextBlob(transcript_text).sentiment
    return sentiment

def filter_transcript_for_keywords(transcript_text, keywords):
    filtered_transcript = []
    for entry in transcript_text:
        for keyword in keywords:
            if keyword.lower() in entry['text'].lower():
                filtered_transcript.append(entry)
                break
    return filtered_transcript

def cluster_transcript(transcript_text, window_size=3):
    clustered_transcript = []
    for i in range(0, len(transcript_text), window_size):
        window = transcript_text[i:i+window_size]
        text = ' '.join([entry['text'] for entry in window])
        start_time = window[0]['start']
        clustered_transcript.append({'start': start_time, 'text': text})
    return clustered_transcript

def answer_question(question, transcript_text):
    # Use the transcript text to answer the user's question
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Based on the transcript: {transcript_text} \n\n Question: {question}")
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")
keywords = st.text_input("Enter keywords to filter important timestamps (comma-separated):")

if youtube_link:
    try:
        video_id = re.search(r"v=([a-zA-Z0-9_-]+)", youtube_link).group(1)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except Exception as e:
        st.error("Invalid YouTube URL")

if st.button("Get Detailed Notes"):
    try:
        transcript_text, video_id = extract_transcript_details(youtube_link)
        if transcript_text:
            transcript = " ".join([entry['text'] for entry in transcript_text])
            summary = generate_gemini_content(transcript, prompt)
            with st.expander("Detailed Notes"):
                st.markdown("## Detailed Notes:")
                st.write(summary)
            
            # if keywords:
            #     keyword_list = [keyword.strip() for keyword in keywords.split(",")]
            #     filtered_transcript = filter_transcript_for_keywords(transcript_text, keyword_list)
            #     clustered_transcript = cluster_transcript(filtered_transcript)
            #     display_transcript_with_timestamps(clustered_transcript, video_id)
            # else:
            #     display_transcript_with_timestamps(transcript_text, video_id)
        else:
            st.error("Error retrieving transcript or video ID.")
    except Exception as e:
        st.error(f"Error retrieving transcript: {e}")

with st.expander("Ask a Question"):
    question = st.text_input("Ask a question about the video:")
    if st.button("Get Answer"):
        try:
            transcript_text, video_id = extract_transcript_details(youtube_link)
            if transcript_text:
                transcript = " ".join([entry['text'] for entry in transcript_text])
                answer = answer_question(question, transcript)
                st.markdown("## Answer to Your Question:")
                st.write(answer)
            else:
                st.error("Error retrieving transcript or video ID.")
        except Exception as e:
            st.error(f"Error retrieving transcript: {e}")
