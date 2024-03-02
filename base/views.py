
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
import yt_dlp as youtube_dl
import os

#kXYiU_JCYtU

# def Main(request,musid):
#     ydl_opts = {
#             'format': 'bestaudio',
#         }

#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         try:
#             info = ydl.extract_info('https://www.youtube.com/watch?v=' + musid, download=True)
#             filename = ydl.prepare_filename(info)
#             os.rename(filename, filename[:-4] + "mp3")  # Rename the file by changing extension
#             with open(filename[:-4] + "mp3", 'rb') as audio_file:
#                 audio_data = audio_file.read()
#             os.remove(filename[:-4] + "mp3")  # Remove the temporary file
#             return HttpResponse(audio_data, content_type='audio/mpeg')
#         except Exception as e:
#             return Response({'error': str(e)}, status=500)

def Main(request, musid):
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': '/tmp/%(title)s.%(ext)s',  # Save file to /tmp directory
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info('https://www.youtube.com/watch?v=' + musid, download=True)
            filename = ydl.prepare_filename(info)
            # File already saved in /tmp directory as per outtmpl
            with open(filename, 'rb') as audio_file:
                audio_data = audio_file.read()
            os.remove(filename)  # Remove the temporary file
            return HttpResponse(audio_data, content_type='audio/mpeg')
        except Exception as e:
            return Response({'error': str(e)}, status=500)