import datetime
from essentials.basics import SpriteSheet, CharacterData

# ===================================================================================================================================
#                                ALL CHARACTER DATAS
# ===================================================================================================================================

# Spritesheets
bobby_ss = SpriteSheet('resources/images/characters/bobby_16.png', (16,16), scale_factor=4)
cuchu_ss = SpriteSheet('resources/images/characters/cuchu_16.png', (16,16), scale_factor=4)
pol_ss = SpriteSheet('resources/images/characters/pol_16.png', (16,16), scale_factor=4)
doki_ss = SpriteSheet('resources/images/characters/doki_16.png', (16,16), scale_factor=4)
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
    'My flesh is pixels',
]

POL_PHRASES = [
    'Guau', 
    'Guau Guau', 
    'GUAU', 
    'grr',
    'guau (soy tu pulguita)'
]

DOKI_PHRASES = [
    'Guau', 
    'Guau Guau', 
    'GUAU', 
    'grr',
    'guau guaUu (te amo)'
]

SQUALO_PHRASES = [
    'glu glu glu', 
    'ñam ñam ñam', 
    'mamiii', 
    '?',
    'gracias por curar mi brazito'
]

DINO_PHRASES = [
    'rawr', 
    'nam nam nam', 
    'grrr', 
    'y papi?',
    'no me gusta el chicle'
]

PACHU_PHRASES = [
    'Siempre tengo la razón', 
    'Mmmm... faltan tildes', 
    'Tengo que trabajar', 
    'Mi piojito jsjs',
    'BOOM',
    'Quiero sushi',
    'Exijo mimos y besos'
]

CUCHU_CHAR_DATA = CharacterData(cuchu_ss, 'cuchu', CUCHU_PHRASES)
BOBBY_CHAR_DATA = CharacterData(bobby_ss, 'bobby', BOBBY_PHRASES)
PACHU_CHAR_DATA = CharacterData(pachu_ss, 'pachu', PACHU_PHRASES)
POL_CHAR_DATA = CharacterData(pol_ss, 'pol', POL_PHRASES)
DOKI_CHAR_DATA = CharacterData(doki_ss, 'doki', DOKI_PHRASES)
SQUALO_CHAR_DATA = CharacterData(squalo_ss, 'squalo', SQUALO_PHRASES)
DINO_CHAR_DATA = CharacterData(dino_ss, 'dino', DINO_PHRASES)

# Character DATA
CHARACTERS: list[CharacterData] = [
    #BOBBY_CHAR_DATA,
    CUCHU_CHAR_DATA,
    POL_CHAR_DATA,
    SQUALO_CHAR_DATA,
    DINO_CHAR_DATA,
    PACHU_CHAR_DATA
]
