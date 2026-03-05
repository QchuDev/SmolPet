import datetime
from essentials.basics import SpriteSheet, CharacterData, resource_path

# ===================================================================================================================================
#                                ALL CHARACTER DATAS
# ===================================================================================================================================


# Phrases 
today = datetime.date.today()
pachus_bd = datetime.date(datetime.datetime.now().year, 3, 6)
if pachus_bd < datetime.date.today(): pachus_bd = datetime.date(datetime.datetime.now().year+1, 3, 6)
lucas_wedding = datetime.date(datetime.datetime.now().year, 12, 12)
if lucas_wedding < datetime.date.today(): pachus_bd = datetime.date(datetime.datetime.now().year+1, 3, 6)
anniversary = datetime.date(datetime.datetime.now().year, 8, 8)
if anniversary < datetime.date.today(): pachus_bd = datetime.date(datetime.datetime.now().year+1, 3, 6)

days_left_bd = (pachus_bd - today).days
days_left_wedding = (lucas_wedding - today).days
days_left_anniversary = (anniversary - today).days

CUCHU_PHRASES = [
    'Te amo <3',
    'Estas ocupada amor?',
    'Me encantas jsjsjs',
    'Mandame un mensaje a whatsapp',
    'Te puedo ayudar?',
    'Soy tu principe jeje',
    f'Faltan {days_left_bd} dias para tu cumple!' if days_left_bd > 0 else 'FELIZ CUMPLE AMOR!',
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
    'Quiero tiramisu',
    f'Faltan {days_left_anniversary} dias para mi aniversario con Pachu <3'
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
    'guau guaUu (te amo)',
    'rawr (soy una masita)'
]

SQUALO_PHRASES = [
    'glu glu glu', 
    'nam nam nam', 
    'mamiii', 
    '?',
    'glu glu (gracias por curar mi brazito)'
]

DINO_PHRASES = [
    'rawr', 
    'nam nam nam', 
    'grrr', 
    'y papi?',
    'rawr (no me gusta el chicle)',
    'no busques popo jiji',
    'globos! globos! globos!'
]

PACHU_PHRASES = [
    'Siempre tengo la razon', 
    'Mmmm... faltan tildes', 
    'Tengo que trabajar', 
    'Mi piojito jsjs',
    'BOOM',
    'Quiero sushi',
    'Exijo mimos y besos',
    f'Recorda! Luca y Cami se casan en {days_left_wedding} dias',
    f'Faltan {days_left_anniversary} dias para mi aniversario con Cuchu <3',
    'Sexi quien lea esto'

]


CHARACTERS = []
BOBBY_CHAR_DATA = None
CUCHU_CHAR_DATA = None
PACHU_CHAR_DATA = None
POL_CHAR_DATA = None
DOKI_CHAR_DATA = None
SQUALO_CHAR_DATA = None
DINO_CHAR_DATA = None

def init_characters():
    global CHARACTERS, BOBBY_CHAR_DATA, CUCHU_CHAR_DATA, PACHU_CHAR_DATA, POL_CHAR_DATA, DOKI_CHAR_DATA, SQUALO_CHAR_DATA, DINO_CHAR_DATA
    
    # Spritesheets
    bobby_ss = SpriteSheet(resource_path('resources/images/characters/bobby_16.png'), (16,16), scale_factor=4)
    cuchu_ss = SpriteSheet(resource_path('resources/images/characters/cuchu_16.png'), (16,16), scale_factor=4)
    pol_ss = SpriteSheet(resource_path('resources/images/characters/pol_16.png'), (16,16), scale_factor=4)
    doki_ss = SpriteSheet(resource_path('resources/images/characters/doki_16.png'), (16,16), scale_factor=4)
    squalo_ss = SpriteSheet(resource_path('resources/images/characters/squalo_16.png'), (16,16), scale_factor=4)
    dino_ss = SpriteSheet(resource_path('resources/images/characters/dino_16.png'), (16,16), scale_factor=4)
    pachu_ss = SpriteSheet(resource_path('resources/images/characters/pachu_16.png'), (16,16), scale_factor=4)
    

    CUCHU_CHAR_DATA = CharacterData(cuchu_ss, 'cuchu', CUCHU_PHRASES)
    BOBBY_CHAR_DATA = CharacterData(bobby_ss, 'bobby', BOBBY_PHRASES)
    PACHU_CHAR_DATA = CharacterData(pachu_ss, 'pachu', PACHU_PHRASES)
    POL_CHAR_DATA = CharacterData(pol_ss, 'pol', POL_PHRASES)
    DOKI_CHAR_DATA = CharacterData(doki_ss, 'doki', DOKI_PHRASES)
    SQUALO_CHAR_DATA = CharacterData(squalo_ss, 'squalo', SQUALO_PHRASES)
    DINO_CHAR_DATA = CharacterData(dino_ss, 'dino', DINO_PHRASES)

    # Character DATA
    CHARACTERS = [
        #BOBBY_CHAR_DATA,
        CUCHU_CHAR_DATA,
        POL_CHAR_DATA,
        SQUALO_CHAR_DATA,
        DINO_CHAR_DATA,
        PACHU_CHAR_DATA,
        DOKI_CHAR_DATA
    ]
