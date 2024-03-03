
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import yt_dlp as youtube_dl
import os

#kXYiU_JCYtU
#z8M8YZj71NM
#pymusic-zbkh.vercel.app/music/download/

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

# def Main(request, musid):
#     ydl_opts = {
#         'format': 'bestaudio',
#         'outtmpl': '/tmp/%(title)s.%(ext)s',  # Save file to /tmp directory
#     }

#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         try:
#             info = ydl.extract_info('https://www.youtube.com/watch?v=' + musid, download=True)
#             filename = ydl.prepare_filename(info)
#             # File already saved in /tmp directory as per outtmpl
#             with open(filename, 'rb') as audio_file:
#                 audio_data = audio_file.read()
#             os.remove(filename)  # Remove the temporary file
#             return HttpResponse(audio_data, content_type='audio/mpeg')
#         except Exception as e:
#             return Response({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def Main(request, musid):
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': '/tmp/%(title)s.%(ext)s', 
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            video_url = f'https://www.youtube.com/watch?v={musid}'
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            # audio_file_path = f"{filename[:-4]}mp3"
            
            def file_iterator(file_path, chunk_size=8192):
                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk
            
            response = StreamingHttpResponse(file_iterator(filename), content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{musid}.mp3"'
            # os.remove(filename)  # Remove the temporary file
            return response
    except youtube_dl.utils.DownloadError:
        return JsonResponse({'error': 'Unable to download the video.'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
# @csrf_exempt
# @require_POST
# def Main(request, musid):
#     ydl_opts = {
#         'format': 'bestaudio',
#     }

#     try:
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             video_url = f'https://www.youtube.com/watch?v={musid}'
#             info = ydl.extract_info(video_url, download=True)
#             filename = ydl.prepare_filename(info)
#             os.rename(filename, f"{filename[:-4]}mp3")  # Rename the file by changing extension
#             audio_file_path = f"{filename[:-4]}mp3"
            
#             def file_iterator(file_path, chunk_size=8192):
#                 with open(file_path, 'rb') as f:
#                     while True:
#                         chunk = f.read(chunk_size)
#                         if not chunk:
#                             break
#                         yield chunk
            
#             response = StreamingHttpResponse(file_iterator(audio_file_path), content_type='audio/mpeg')
#             response['Content-Disposition'] = f'attachment; filename="{musid}.mp3"'
#             os.remove(audio_file_path)  # Remove the temporary file
#             return response
#     except youtube_dl.utils.DownloadError:
#         return JsonResponse({'error': 'Unable to download the video.'}, status=500)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
    

