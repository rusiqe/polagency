import time

def cache_buster(request):
    return {'cache_buster': int(time.time())}
