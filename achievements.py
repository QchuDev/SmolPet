from essentials.basics import GameManager

ALL_ACHIEVEMENTS = {
    # name      :       unlocked, condition, desc
    'UN VIRUS?!?':          [False, GameManager.first_time, 'Entra por primera vez al virus? juego? regalo?'],
    'Lo pario Cuchu?':      [False, False, 'Desbloquea a Mini-Dino'],
    'Tiburon? Perro?':      [False, False, 'Desbloquea a Mini-Squalo'],
    'Los hermanitos':       [False, False, 'Desbloquea a Mini-Squalo y Mini-Dino'],
    'Mi novio autista':     [False, False, 'Desbloquea a Mini-Cuchu'],
    'Soy yo, soy yo':       [False, False, 'Desbloquea a Mini-Pachu'],
    'Carboncito':           [False, False, 'Desbloquea a Mini-Pol'],
    'Tiburon? Osito?':      [False, False, 'Desbloquea a Mini-Squalo'],
    'La familia reunida':   [False, False, 'Desbloquea todos los Minis'],
    'Donde surgio...?':     [False, False, 'Aparece un tiramisu'],
    'Dulce o Salado?':      [False, False, 'Aparece pochoclos'],
    'Diu':                  [False, False, 'Aparece caca'],
    'FIESTAA':              [False, False, 'Aparece globooos'],
    'Aprendiendo juntos':   [False, False, 'Mira un video de Javier Ledesma con Mini-Pachu y Mini-Cuchu'],
    'Hora de la siesta':    [False, False, 'Que todos se vayan a dormir'],
    'ABSOLUTE CINEMA':      [False, False, 'Mira una pelicula o serie con Cuchu'],
    'BOOOM!':               [False, False, 'Consigue todos los logros, una genia <3']
}

# Getting the state of the achievements
def get_save_data():
    return {name: info[0] for name, info in ALL_ACHIEVEMENTS.items()}

# Loading the information stored back to the dictionary
def load_save_data(data):
    for name, unlocked in data.items():
        if name in ALL_ACHIEVEMENTS:
            ALL_ACHIEVEMENTS[name][0] = unlocked