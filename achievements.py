from essentials.basics import GameManager

ALL_ACHIEVEMENTS = {
    # name      :       unlocked, condition, desc
    'UN VIRUS?!?':          [
        False, 
        lambda: GameManager.first_time, 
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
        lambda: GameManager.is_unlocked('dino'), 
        'Desbloquea a Mini-Pachu'
    ],
    'Carboncito':           [
        False, 
        lambda: GameManager.is_unlocked('dino'), 
        'Desbloquea a Mini-Pol'
    ],
    'Tiburon? Osito?':      [
        False, 
        lambda: GameManager.is_unlocked('dino'), 
        'Desbloquea a Mini-Squalo'
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
        lambda: False, 
        'Mira una pelicula o serie con Cuchu'
    ],
    'BOOOM!':               [
        False, 
        lambda: False, 
        'Consigue todos los logros, una genia <3'
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