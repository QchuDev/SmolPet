
from essentials.gm import GameManager
import user_activity

ALL_ACHIEVEMENTS = {
    # REMEMBER TO ADD THE ACHIEVEMENTS AT THE BOTTOM OF THE DICT

    # name      :       unlocked, condition, desc, source_pos
    'UN VIRUS?!?':          [
        False, 
        lambda: GameManager.first_time == True, 
        'Que descargaste? un regalo...?',
        (0,0)
    ],
    'Lo pario Cuchu?':      [
        False, 
        lambda: GameManager.is_unlocked('dino'), 
        'Desbloquea a Mini-Dino',
        (16,0)
    ],
    'Tiburon? Perro?':      [
        False, 
        lambda: GameManager.is_unlocked('squalo'), 
        'Desbloquea a Mini-Squalo',
        (32,0)
    ],
    'Los hermanitos':       [
        False, 
        lambda: all(GameManager.is_unlocked(name) for name in ['dino', 'squalo']), 
        'Desbloquea a Mini-Squalo y Mini-Dino',
        (48,0)
    ],
    'Mi novio melo':     [
        False, 
        lambda: GameManager.is_unlocked('cuchu'), 
        'Desbloquea a Mini-Cuchu',
        (0,16)
    ],
    'Soy yo, soy yo':       [
        False, 
        lambda: GameManager.is_unlocked('pachu'), 
        'Desbloquea a Mini-Pachu',
        (16,16)
    ],
    'Carboncito':           [
        False, 
        lambda: GameManager.is_unlocked('pol'), 
        'Desbloquea a Mini-Pol',
        (32,16)
    ],
    'La familia reunida':   [
        False, 
        lambda: all(GameManager.is_unlocked(a) for a in ['dino', 'squalo', 'cuchu', 'pachu', 'pol']), 
        'Desbloquea todos los Minis',
        (48,16)
    ],
    'Donde surgio...?':     [
        False, 
        lambda: GameManager.is_unlocked('tiramisu'), 
        'Aparece un tiramisu',
        (0,32)
    ],
    'Dulce o Salado?':      [
        False, 
        lambda: GameManager.is_unlocked('popcorn bucket'), 
        'Aparece pochoclos',
        (16,32)
    ],
    'Diu':                  [
        False, 
        lambda: GameManager.is_unlocked('poop'),  
        'Aparece caca',
        (32,32)
    ],
    'FIESTAA':              [
        False, 
        lambda: GameManager.is_unlocked('balloon'),  
        'Aparece globooos',
        (48,32)
    ],
    'Aprendiendo juntos':   [
        False, 
        lambda: all(GameManager.is_unlocked(name) for name in ['cuchu', 'pachu']) and user_activity.shared_state['is_watching_javierledesma'], 
        'Mira Javier Ledesma con Pachu y Cuchu',
        (0,48)
    ],
    'Hora de la siesta':    [
        False, 
        lambda: GameManager.all_sleeping(),
        'Que todos se vayan a dormir',
        (16,48)
    ],
    'ABSOLUTE CINEMA':      [
        False, 
        lambda: GameManager.is_unlocked('cuchu') and (user_activity.shared_state['is_watching_ytvideo'] or user_activity.shared_state['is_watching_movie']), 
        'Mira un video, pelicula o serie con Cuchu',
        (32,48)
    ],
    'KUCHAU!':              [
        False,
        lambda: GameManager.top_speed() > 8000,
        'Supera los limites de velocidad, veloz como el rayo',
        (48,48)
    ],
    'BOOOM!':               [
        False, 
        lambda: GameManager.game_completed == True, 
        'Termina el juego, una genia <3',
        (0,64)
    ],
    'Gran Maestra':               [
        False, 
        lambda: user_activity.shared_state['is_playing_chess'] == True, 
        'Juega al ajedrez :3',
        (16,64)
    ],
    'No me revolees':               [
        False, 
        lambda: GameManager.lifting_a_mini() == True, 
        'Levanta a un mini',
        (32,64)
    ],



}

# Getting the state of the achievements
def get_save_data():
    return {name: info[0] for name, info in ALL_ACHIEVEMENTS.items()}

# Loading the information stored back to the dictionary
def load_save_data(data):
    for name, unlocked in data.items():
        if name in ALL_ACHIEVEMENTS:
            ALL_ACHIEVEMENTS[name][0] = unlocked