import threading
import time 
import pygetwindow as gw

# Checking for the activity of the user
# if watching a video
# if its afk
# the last search they made 

def monitor_system(state):
    while True:
        try:
            # Obtain active window
            active_window = gw.getActiveWindow()

            if active_window:
                title = active_window.title.lower()
                video_kw = ['netflix', 'vlc', 'disney', 'prime']
                state['is_watching_movie']      = any(k in title for k in video_kw)
                state['is_watching_ytvideo']    = '- Youtube' in title

                if 'google search' in title or 'buscar con google' in title:
                    state['last_search'] = title.split('-')[0].strip()

        except Exception:
            pass
        
        #print(f'Shared State:{state}')
        time.sleep(3)   # wait 3 seconds 

shared_state = {
    "is_watching_video": False,
    "is_watching_ytvideo": False,
    "is_afk": False,
    "last_search": ""
}

# Crear y lanzar el hilo
monitor_thread = threading.Thread(
    target=monitor_system, 
    args=(shared_state,), 
    daemon=True
)
monitor_thread.start()

print(f'Secondary thread started...')

