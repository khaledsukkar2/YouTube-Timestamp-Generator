from django.conf import settings
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_extractor import extract_video_id_from_url
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_api_response(prompt:str):
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{prompt}"}],
            temperature=0,
        )

    message_content = response.choices[0].message.content
    return message_content

def get_video_id(url):
    try:
        video_id = extract_video_id_from_url(url)
        return video_id
    except:
        return False

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join([i['text'] for i in transcript])
    return full_transcript


