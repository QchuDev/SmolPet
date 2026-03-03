import random


from characters_setup import BOBBY_CHAR_DATA, CHARACTERS, CUCHU_CHAR_DATA, DINO_CHAR_DATA, PACHU_CHAR_DATA, POL_CHAR_DATA, SQUALO_CHAR_DATA
from essentials.basics import Animation, Entity, ParticlesManager, SFXManager, SpriteSheet
from essentials.components import AIController, Animator, CharactersHandler, MouseDrag, ParticlesEmitter, PhysicalBall, PlayOnHit, PropDuration, StatesManager, TextBubble
from essentials.math_custom import Vector2D
from states_graph import NPC_STATES, PROP_STATES

# PARTICLE PREFABS
# name =        [texture, lifetime,ammount, force, accy]
POPCORN_PRTS =  ['popcorn', 0.8,    8,      3,      0.2     ]
SPARK_PRTS =    ['spark',   2,    8,      3,      0       ]
HEART_PRTS =    ['heart',   0.8,    8,      3,      -0.05   ]
CHOCOLATE_PRTS =['chocolate',  0.8,    8,      3,      0.2 ]

EXTRA_CHOCOLATE_PRTS =['chocolate',  0.8,    20,      4,       0.05 ]
POPCORN_BREAK_PRTS = ['popcorn_break', 0.8,    8,      3,       0.05     ]
CHOCOLATE_BREAK_PRTS = ['tiramisu_break', 0.8,    8,      4,      0.05     ]

# ENTITY PREFABS ================================================================================================================================================================
# NPC ANIMATIONS
NPC_ANIMATIONS = [
    Animation('idle',       [0, 1, 2],      frame_duration=0.2),
    Animation('hit_floor',  [3, 4, 5],      frame_duration=0.08,    loop=False),
    Animation('air',        [6, 7, 8],      frame_duration=0.2),
    Animation('talk',       [9, 10, 11],    frame_duration=0.2),
    Animation('hit_wall',   [12, 13, 14],   frame_duration=0.08,    loop=False),
    Animation('go_sleep',   [15, 16, 17],   frame_duration=0.2,     loop=False),
    Animation('sleeping',   [18, 19, 20],   frame_duration=0.3),
    Animation('go_sit',     [21,22,23],     frame_duration=0.2,     loop=False),
    Animation('sit',        [24,25,26],     frame_duration=0.3)
]
PROP_ANIMATIONS = [
    Animation('still',      [0, 1, 2],      frame_duration=0.2),
    Animation('bounce',     [3, 4, 5],      frame_duration=0.08,    loop=False),
]

play_on_hit_comp = PlayOnHit()
animator_comp = Animator(anims = NPC_ANIMATIONS)
aic_comp = AIController(timer_range=(0.5, 2))
mouse_drag = MouseDrag()
npc_state_manager = StatesManager(NPC_STATES)
text_bubble =  TextBubble()
# CHARACTERS
BOBBY_PREFAB = Entity(
    name=f'bobby',
    components= [
        PhysicalBall(radius=30, air_resist=0.0005, mass=1, retention_y=0.45),
        mouse_drag,
        animator_comp,  # sleeping WIP
        aic_comp,
        npc_state_manager,
        text_bubble,
        CharactersHandler([BOBBY_CHAR_DATA]),
        play_on_hit_comp
    ]
)
CUCHU_PREFAB = Entity(
    name=f'cuchu',
    components= [
        PhysicalBall(radius=30, air_resist=0.0005, mass=1.4, retention_y=0.45),
        mouse_drag,
        animator_comp,  # sleeping WIP
        aic_comp,
        npc_state_manager,
        text_bubble,
        CharactersHandler([CUCHU_CHAR_DATA]),
        play_on_hit_comp
    ]
)
PACHU_PREFAB = Entity(
    name=f'pachu',
    components= [
        PhysicalBall(radius=30, air_resist=0.0005, mass=1.3, retention_y=0.45),
        mouse_drag,
        animator_comp,  # sleeping WIP
        aic_comp,
        npc_state_manager,
        text_bubble,
        CharactersHandler([PACHU_CHAR_DATA]),
        play_on_hit_comp
    ]
)
POL_PREFAB = Entity(
    name=f'pol',
    components= [
        PhysicalBall(radius=30, air_resist=0.0005, mass=1.1, retention_y=0.45),
        mouse_drag,
        animator_comp,  # sleeping WIP
        aic_comp,
        npc_state_manager,
        text_bubble,
        CharactersHandler([POL_CHAR_DATA]),
        play_on_hit_comp
    ]
)
SQUALO_PREFAB = Entity(
    name=f'squalo',
    components= [
        PhysicalBall(radius=30, air_resist=0.0005, mass=1, retention_y=0.45),
        mouse_drag,
        animator_comp,  # sleeping WIP
        aic_comp,
        npc_state_manager,
        text_bubble,
        CharactersHandler([SQUALO_CHAR_DATA]),
        play_on_hit_comp
    ]
)
DINO_PREFAB = Entity(
    name=f'dino',
    components= [
        PhysicalBall(radius=30, air_resist=0.0005, mass=1, retention_y=0.45),
        mouse_drag,
        animator_comp,  # sleeping WIP
        aic_comp,
        npc_state_manager,
        text_bubble,
        CharactersHandler([DINO_CHAR_DATA]),
        play_on_hit_comp
    ]
)

# PROPS
POPCORN_PREFAB = Entity( 
    name='popcorn bucket',
    components= [
        PhysicalBall(radius=30, air_resist=0.001, mass=1, retention_y=0.3, directed=False),
        mouse_drag,
        ParticlesEmitter(POPCORN_PRTS, 'in_hit', offset= (0, -2)),
        Animator(SpriteSheet('resources/images/popcorn_bucket_16.png', (16,16), scale_factor=4), anims=PROP_ANIMATIONS),
        StatesManager(PROP_STATES),
        PropDuration(7, POPCORN_BREAK_PRTS),
        play_on_hit_comp
    ]
)

TIRAMISU_PREFAB = Entity( 
    name='tiramisu',
    components= [
        PhysicalBall(radius=30, air_resist=0.001, mass=1, retention_y=0.2, directed=False),
        mouse_drag,
        ParticlesEmitter(CHOCOLATE_PRTS, 'in_hit', offset= (0, -2)),
        Animator(SpriteSheet('resources/images/tiramisu_16.png', (16,16), scale_factor=4), anims=PROP_ANIMATIONS),
        StatesManager(PROP_STATES),
        PropDuration(6,CHOCOLATE_BREAK_PRTS),
        play_on_hit_comp
    ]
)

POOP_PREFAB = Entity( 
    name='poop',
    components= [
        PhysicalBall(radius=30, air_resist=0.001, mass=1, retention_y=0.2, directed=False),
        mouse_drag,
        ParticlesEmitter(CHOCOLATE_PRTS, 'in_hit', offset= (0, -1)),
        Animator(SpriteSheet('resources/images/poop_16.png', (16,16), scale_factor=4), anims=PROP_ANIMATIONS),
        StatesManager(PROP_STATES),
        PropDuration(3,EXTRA_CHOCOLATE_PRTS),
        play_on_hit_comp
    ]
)

balloon_phys = PhysicalBall(radius=15, air_resist=0.005, mass=1, retention_y=0.6, grav_scale=0.02, directed=False)

RED_BALLOON_PREFAB = Entity( 
    name='red balloon',
    components= [
        balloon_phys,
        mouse_drag,
        Animator(SpriteSheet(f'resources/images/balloons/balloon0_16.png', (16,16), scale_factor=4), anims=PROP_ANIMATIONS),
        StatesManager(PROP_STATES)
    ]
)
BLUE_BALLOON_PREFAB = Entity( 
    name='blue balloon',
    components= [
        balloon_phys,
        mouse_drag,
        Animator(SpriteSheet(f'resources/images/balloons/balloon1_16.png', (16,16), scale_factor=4), anims=PROP_ANIMATIONS),
        StatesManager(PROP_STATES)
    ]
)
YELLOW_BALLOON_PREFAB = Entity( 
    name='yellow balloon',
    components= [
        balloon_phys,
        mouse_drag,
        Animator(SpriteSheet(f'resources/images/balloons/balloon2_16.png', (16,16), scale_factor=4), anims=PROP_ANIMATIONS),
        StatesManager(PROP_STATES)
    ]
)
GREEN_BALLOON_PREFAB = Entity( 
    name='green balloon',
    components= [
        balloon_phys,
        mouse_drag,
        Animator(SpriteSheet(f'resources/images/balloons/balloon3_16.png', (16,16), scale_factor=4), anims=PROP_ANIMATIONS),
        StatesManager(PROP_STATES)
    ]
)

ALL_PREFABS = {
    'bobby': BOBBY_PREFAB,
    'cuchu': CUCHU_PREFAB,
    'pachu': PACHU_PREFAB,
    'pol': POL_PREFAB,
    'squalo': SQUALO_PREFAB,
    'dino': DINO_PREFAB,
    'popcorn bucket': POPCORN_PREFAB,
    'tiramisu': TIRAMISU_PREFAB,
    'red balloon': RED_BALLOON_PREFAB,
    'blue balloon': BLUE_BALLOON_PREFAB,
    'yellow balloon': YELLOW_BALLOON_PREFAB,
    'green balloon': GREEN_BALLOON_PREFAB,
    'poop': POOP_PREFAB
}

# Creates the entity at posistion x,y with a vfx
def create_entity(prefab_name:str, x,y, push:bool = True) -> Entity:
    # Call the necessary prefab to spawn 
        if prefab_name != 'balloon':
            new_ent = ALL_PREFABS[prefab_name].clone()
        else:
            random_ballon = ['red balloon', 'blue balloon', 'yellow balloon', 'green balloon'][random.randrange(0,4)]
            new_ent = ALL_PREFABS[random_ballon].clone()

        new_ent.pos.x = x
        new_ent.pos.y = y
        
        # Call start method of entity for setup
        new_ent.start()

        if push:
            phys = new_ent.get_component(PhysicalBall)
            if phys: phys.applyForce(Vector2D(random.uniform(-8000, 8000), -8000))
        
        ParticlesManager.emit(new_ent.pos.x, new_ent.pos.y, *SPARK_PRTS)
        SFXManager.play('sparks', 0.6)

        return new_ent