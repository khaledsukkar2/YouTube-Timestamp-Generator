import time
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from core.functions import get_transcript, get_video_id, get_api_response


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


def logout_user(request):
    """
    This method used to logout the user
    """
    if request.user:
        logout(request)
    response = HttpResponse()
    response.content = """
        <script>
            localStorage.clear();
        </script>
        <meta http-equiv="refresh" content="0;url=/login">
    """
    return response


@login_required
def index(request):
    return render(request, 'core/index.html')


@csrf_exempt
@login_required
def generate_timestamps(request):
    start_time = time.time()
    if request.method == 'POST':
        try:
            url = request.POST.get('url')

            # Check if the URL is valid
            video_id = get_video_id(url)
            if not video_id:
                return render(request, 'core/index.html', {'error': 'Invalid YouTube URL'})

            transcript = get_transcript(video_id)

            prompt = f"""create key moments from this video transcript and include the time of key chapters starting with 0.00 to the end of the video
                the transcript: {transcript}
              """

            response = get_api_response(prompt)

            timestamps = [{"text": timestamp} for timestamp in response.split('\n')]

            timestamps_dict = {idx: ts for idx, ts in enumerate(timestamps, start=1)}
            end_time = time.time()  
            print("total time : ", end_time - start_time) 
            return render(request, 'core/index.html', {'timestamps': list(timestamps_dict.values())[1:]})
        except Exception as e:
            print(e)
            return render(request, 'core/index.html', {'error': 'Something went wrong, please try again'})
    else:
        return render(request, 'core/index.html')