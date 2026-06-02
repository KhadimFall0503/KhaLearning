import html
import json
import re
import requests
from django.core.files.base import ContentFile


def fetch_youtube_data(youtube_url):
    """
    Récupère automatiquement :
    - le titre
    - la description YouTube
    - la miniature YouTube
    """

    # Extraction ID vidéo
    if "v=" in youtube_url:
        video_id = youtube_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_url:
        video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
    else:
        return "", "", None

    # Récupération de l'oEmbed pour le titre et la miniature
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    response = requests.get(oembed_url, timeout=10)

    if response.status_code != 200:
        return "", "", None

    data = response.json()
    title = data.get("title", "")
    thumbnail_url = data.get("thumbnail_url")
    image_content = None

    if thumbnail_url:
        img = requests.get(thumbnail_url, timeout=10)
        if img.status_code == 200:
            image_content = ContentFile(img.content)

    description = _fetch_youtube_description(video_id) or f"Formation vidéo : {title}"
    return title, description, image_content


def _fetch_youtube_description(video_id):
    """Récupère la description YouTube depuis la page de la vidéo."""
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(video_url, headers=headers, timeout=10)
    if response.status_code != 200:
        return None

    html_content = response.text
    match = re.search(r'"shortDescription":"((?:\\.|[^"\\])*)"', html_content)
    if not match:
        return None

    raw_description = match.group(1)
    try:
        return json.loads(f'"{raw_description}"').strip()
    except json.JSONDecodeError:
        cleaned_description = raw_description.replace('\\n', ' ').replace('\\u0026', '&')
        return html.unescape(cleaned_description).strip()
