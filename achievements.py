from essentials.basics import GameManager
import user_activity

ALL_ACHIEVEMENTS = {
    # name      :       unlocked, condition, desc
    'UN VIRUS?!?':          [
        False, 
        lambda: GameManager.first_time == True, 
        'Entra por primera vez al virus? juego? regalo?'
    ],
    'Lo pario Cuchu?':      [
        False, 
        lambda: GameManager.is_unlocked('dino'), 
        'Desbloquea a Mini-Dino'
    ],
    'Tiburon? Perro?':      [
        False, 
        lambda: GameManager.is_unlocked('squalo'), 
        'Desbloquea a Mini-Squalo'
    ],
    'Los hermanitos':       [
        False, 
        lambda: all(GameManager.is_unlocked(name) for name in ['dino', 'squalo']), 
        'Desbloquea a Mini-Squalo y Mini-Dino'
    ],
    'Mi novio autista':     [
        False, 
        lambda: GameManager.is_unlocked('cuchu'), 
        'Desbloquea a Mini-Cuchu'
    ],
    'Soy yo, soy yo':       [
        False, 
        lambda: GameManager.is_unlocked('pachu'), 
        'Desbloquea a Mini-Pachu'
    ],
    'Carboncito':           [
        False, 
        lambda: GameManager.is_unlocked('pol'), 
        'Desbloquea a Mini-Pol'
    ],
    'La familia reunida':   [
        False, 
        lambda: GameManager.is_unlocked('dino'), 
        'Desbloquea todos los Minis'
    ],
    'Donde surgio...?':     [
        False, 
        lambda: GameManager.is_unlocked('tiramisu'), 
        'Aparece un tiramisu'
    ],
    'Dulce o Salado?':      [
        False, 
        lambda: GameManager.is_unlocked('popcorn bucket'), 
        'Aparece pochoclos'
    ],
    'Diu':                  [
        False, 
        lambda: GameManager.is_unlocked('poop'),  
        'Aparece caca'
    ],
    'FIESTAA':              [
        False, 
        lambda: GameManager.is_unlocked('balloon'),  
        'Aparece globooos'
    ],
    'Aprendiendo juntos':   [
        False, 
        lambda: False, 
        'Mira un video de Javier Ledesma con Mini-Pachu y Mini-Cuchu'
    ],
    'Hora de la siesta':    [
        False, 
        lambda: GameManager.all_sleeping(),
        'Que todos se vayan a dormir'
    ],
    'ABSOLUTE CINEMA':      [
        False, 
        lambda: GameManager.is_unlocked('cuchu') and user_activity.shared_state['is_watching_video'], 
        'Mira una pelicula o serie con Cuchu'
    ],
    'KUCHAU!':              [
        False,
        lambda: GameManager.top_speed() > 10000,
        'Supera los limites de velocidad, veloz como el rayo'
    ],
    'BOOOM!':               [
        False, 
        lambda: GameManager.game_completed == True, 
        'Termina el juego, una genia <3'
    ]
}

# Getting the state of the achievements
def get_save_data():
    return {name: info[0] for name, info in ALL_ACHIEVEMENTS.items()}

# Loading the information stored back to the dictionary
def load_save_data(data):
    for name, unlocked in data.items():
        if name in ALL_ACHIEVEMENTS:
            ALL_ACHIEVEMENTS[name][0] = unlocked