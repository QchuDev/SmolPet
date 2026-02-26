import datetime
from essentials.basics import SpriteSheet, CharacterData

# ===================================================================================================================================
#                                ALL CHARACTER DATAS
# ===================================================================================================================================

# Spritesheets
bobby_ss = SpriteSheet('resources/images/characters/bobby_16.png', (16,16), scale_factor=4)
cuchu_ss = SpriteSheet('resources/images/characters/cuchu_16.png', (16,16), scale_factor=4)
pol_ss = SpriteSheet('resources/images/characters/pol_16.png', (16,16), scale_factor=4)
squalo_ss = SpriteSheet('resources/images/characters/squalo_16.png', (16,16), scale_factor=4)
dino_ss = SpriteSheet('resources/images/characters/dino_16.png', (16,16), scale_factor=4)
pachu_ss = SpriteSheet('resources/images/characters/pachu_16.png', (16,16), scale_factor=4)

# Phrases 
today = datetime.date.today()
pachus_bd = datetime.date(datetime.datetime.now().year, 3, 6)
if pachus_bd < datetime.date.today(): pachus_bd = datetime.date(datetime.datetime.now().year+1, 3, 6)
days_left = (pachus_bd - today).days
CUCHU_PHRASES = [
        'Te amo <3',
        'Estas ocupada amor?',
        'Me encantas jsjsjs',
        'Mandame un mensaje a whatsapp',
        'Te puedo ayudar?',
        'Soy tu principe jeje',
        f'Faltan {days_left} dias para tu cumple!' if days_left > 0 else 'FELIZ CUMPLE AMOR!',
        'aiiiiiiiiiii',
        ':V',
        'OMG',
        'XD',
        'ñam ñam',
        'Vemos Javier Ledesma?',
        'Quiero refrescos...',
        'Te quiero mucho mucho <3',
        'Mi loquitaaAaAa',
        'Sos perfecta <3',
        'Mi bombonita <3',
        'Its showtime',
        'PaachUUuU PaAchUuuUu',
        'Te morfo <3',
        'Tirameee',
        'Quiero tiramisu'
]

BOBBY_PHRASES = [
    'Im a little piece of art', 
    'I cant feel a thing', 
    'My flesh is pixels'
]

POL_PHRASES = [
    'Guau', 
    'Guau Guau', 
    'GUAU', 
    'grr'
]

SQUALO_PHRASES = [
    'glu glu glu', 
    'ñam ñam ñam', 
    'mamiii', 
    '?'
]

DINO_PHRASES = [
    'rawr', 
    'ñam ñam ñam', 
    'grrr', 
    'y papi?'
]

PACHU_PHRASES = [
    'Siempre tengo la razón', 
    'Mmmm... faltan tildes', 
    'Tengo que trabajar', 
    'Mi piojito jsjs',
    'BOOM',
    'Quiero sushi'
]

CUCHU_CHAR_DATA = CharacterData(cuchu_ss, 'Cuchu', CUCHU_PHRASES)
BOBBY_CHAR_DATA = CharacterData(bobby_ss, 'Bobby', BOBBY_PHRASES)
PACHU_CHAR_DATA = CharacterData(pachu_ss, 'Pachu', PACHU_PHRASES)
POL_CHAR_DATA = CharacterData(pol_ss, 'Pol', POL_PHRASES)
SQUALO_CHAR_DATA = CharacterData(squalo_ss, 'Squalo', SQUALO_PHRASES)
DINO_CHAR_DATA = CharacterData(dino_ss, 'Dino', DINO_PHRASES)

# Character DATA
CHARACTERS: list[CharacterData] = [
    BOBBY_CHAR_DATA,
    CUCHU_CHAR_DATA,
    POL_CHAR_DATA,
    SQUALO_CHAR_DATA,
    DINO_CHAR_DATA,
    PACHU_CHAR_DATA
]
