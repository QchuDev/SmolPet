import ctypes
from ctypes import wintypes
import threading
import time

# Cargamos las funciones de Windows una sola vez
user32 = ctypes.windll.user32

def get_active_window_title_fast():
    # Obtener el handle de la ventana enfocada
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return ""
    
    # Obtener la longitud del título
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""
    
    # Crear un buffer y llenarlo con el texto
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value.lower()

def monitor_system(state):
    video_kw = ['netflix', 'vlc', 'disney', 'prime']
    while True:
        try:
            # Usamos la versión rápida de C
            title = get_active_window_title_fast()

            if title:
                state['is_watching_movie'] = any(k in title for k in video_kw)
                state['is_watching_ytvideo'] = '- youtube' in title
                state['is_watching_javierledesma'] = '#bizelaneas' in title
                state['is_playing_chess'] = 'ajedrez' in title
                
                if 'google search' in title or 'buscar con google' in title:
                    state['last_search'] = title.split('-')[0].strip()
        except:
            pass
        
        # Aumentamos el tiempo a 3 segundos. 
        # Para una mascota virtual, no necesitas precisión de milisegundos.
        time.sleep(5)
        
shared_state = {
    "is_watching_video": False,
    "is_watching_ytvideo": False,
    "is_watching_javierledesma" : False,
    "is_playing_chess": False,
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

