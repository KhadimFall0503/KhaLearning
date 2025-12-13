import requests
from django.core.files.base import ContentFile

def fetch_youtube_data(youtube_url):
    """
    Récupère automatiquement :
    - le titre
    - la description
    - la miniature YouTube
    """

    # Extraction ID vidéo
    if "v=" in youtube_url:
        video_id = youtube_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_url:
        video_id = youtube_url.split("youtu.be/")[1]
    else:
        return "", "", None

    # API oEmbed (sans clé)
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    response = requests.get(url)

    if response.status_code != 200:
        return "", "", None

    data = response.json()

    title = data.get("title", "")
    description = f"Formation vidéo : {title}"

    # Télécharger la miniature
    thumbnail_url = data.get("thumbnail_url")
    image_content = None

    if thumbnail_url:
        img = requests.get(thumbnail_url)
        if img.status_code == 200:
            image_content = ContentFile(img.content)

    return title, description, image_content
