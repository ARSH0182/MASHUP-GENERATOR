import urllib.request
import re
import random
from pytube import YouTube
from pydub import AudioSegment
import sys
import os


def create_mashup(singer_name, num_videos, duration, output_filename):
    singer_name = singer_name.lower()
    singer_name = singer_name.replace(" ", "") + "videosongs"

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + singer_name)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    url = []
    for i in range(num_videos):
        url.append("https://www.youtube.com/watch?v=" + video_ids[random.randint(0, len(video_ids) - 1)])

    final_aud = AudioSegment.empty()
    for i in range(num_videos):   
        audio = YouTube(url[i]).streams.filter(only_audio=True).first()
        audio.download(filename='Audio-' + str(i) + '.mp3')
        print("\n\t\t\t\tAudio-" + str(i) + " Downloaded successfully")
        aud_file = str(os.getcwd()) + "/Audio-" + str(i) + ".mp3"
        file1 = AudioSegment.from_file(aud_file)
        extracted_file = file1[:duration * 1000]
        final_aud += extracted_file
        final_aud.export(output_filename, format="mp3")
    print("\n\t\t\t\t\tMashup Created ♫♫")


if __name__ == '__main__':
    if len(sys.argv) == 5:
        singer_name = sys.argv[1]
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
        output_filename = sys.argv[4]
        create_mashup(singer_name, num_videos, duration, output_filename)
    else:
        print("Incorrect number of arguments")
