from video_utils import change_video_metadata
import random
import datetime


def change_video_metadata_dynamic(input_video, output_video):
    # Define the metadata you want to change
    list_of_artists = ["Zoba", "Zobaplays", "zobapubg", "zobapubgmobile", "zobagames"]
    list_of_titles = [
        "سكنات ببجي",
        "ببجي موبايل",
        "ببجي",
        "ببجي موبايل",
        "ببجي",
        "كيفية الحصول على سكنات ببجي",
        "كيفية الحصول على سكنات ببجي موبايل",
        "كيفية الحصول على سكنات ببجي",
        "كيفية الحصول على سكن اسطوري ببجي موبايل",
        "كيفية الحصول على سكن المومياء ببجي",
        "كيفية الحصول على سكن المومياء ببجي موبايل",
        "حساسية ببجي",
        "حساسية ببجي موبايل",
        "ملف تثبيت الايم ببجي",
        "ملف تثبيت الايم ببجي موبايل",
    ]
    title = f"فيديو {random.choice(list_of_titles)}"
    artist = random.choice(list_of_artists)
    new_metadata = {
        "title": title,
        "artist": artist,
        "year": datetime.datetime.now().year,
        "comment": f"this video is a {title} that was created by {artist} in {datetime.datetime.now().year}",
    }

    # Call the function to change metadata
    change_video_metadata(input_video, output_video, new_metadata)

    print(f"Video metadata has been changed successfully to {new_metadata}")
