import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise ValueError(f"Invalid YouTube URL: '{url}'")
    return match.group(1)

def get_transcript_as_text(video_url: str) -> str:
    video_id = get_video_id(video_url)
    transcript = YouTubeTranscriptApi().fetch(video_id)
    text = " ".join([entry.text for entry in transcript])
    return text.replace('. ', '.\n')  # one sentence per line

def save_transcript_to_file(text: str, filename="transcript.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    return filename

st.title("YouTube Transcript Downloader")

yt_url = st.text_input("Enter YouTube URL:")

if st.button("Get Transcript"):
    if yt_url:
        try:
            transcript = get_transcript_as_text(yt_url)
            filename = save_transcript_to_file(transcript)
            st.success(f"Transcript saved to {filename}")
            with open(filename, "rb") as f:
                st.download_button(
                    label="Download Transcript",
                    data=f,
                    file_name=filename,
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a YouTube URL.")