import datetime
from basics import SpriteSheet, CharacterData

# ===================================================================================================================================
#                                ALL CHARACTER DATAS
# ===================================================================================================================================

# Spritesheets
bobby_ss = SpriteSheet('resources/images/bobby_16.png', (16,16), scale_factor=4)
cuchu_ss = SpriteSheet('resources/images/cuchu_16.png', (16,16), scale_factor=4)
pol_ss = SpriteSheet('resources/images/pol_16.png', (16,16), scale_factor=4)

# Phrases 
pachus_bd = datetime.date(datetime.datetime.now().year, 3, 6)
CUCHU_PHRASES = [
        'Te amo <3',
        'Estas ocupada amor?',
        'Me encantas jsjsjs',
        'Mandame un mensaje a whatsapp',
        'Te puedo ayudar?',
        'Soy tu principe jeje',
        f'Faltan {(pachus_bd - datetime.date.today()).days} dias para tu cumple!',
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

# Character DATA
CHARACTERS: list[CharacterData] = [
    CharacterData(bobby_ss, 'Bobby', BOBBY_PHRASES),
    CharacterData(cuchu_ss, 'Cuchu', CUCHU_PHRASES),
    CharacterData(pol_ss, 'Pol', POL_PHRASES)
]



