from essentials.basics import Transition, State
from essentials.components import AIController, PhysicalBall, Animator
from game_consts import SLIDE_STOP, BOUNCE_STOP

anim = lambda e: e.get_component(Animator)
phys = lambda e: e.get_component(PhysicalBall)
aic = lambda e: e.get_component(AIController)

# Creating the states for the NPCS
IDLE_STATE = State('idle',
    [
        Transition('air', lambda e: not phys(e).is_grounded),
        Transition('hit_floor', lambda e: phys(e).is_hitting_floor),
        Transition('hit_wall', lambda e: phys(e).is_hitting_wall),
        Transition('talk', lambda e: aic(e).plan[0] == 'talk'),
        Transition('go_sleep', lambda e: aic(e).plan[0] == 'sleep'),
        Transition('go_sit', lambda e: aic(e).plan[0] == 'sit')
    ]
)
AIR_STATE = State('air',
    [
        Transition('hit_floor', lambda e: phys(e).is_hitting_floor),
        Transition('hit_wall', lambda e: phys(e).is_hitting_wall),
        Transition('idle', lambda e: phys(e).is_grounded and abs(phys(e).vel.x) == 0)
    ]
)
HIT_FLOOR_STATE = State('hit_floor',
    [
        Transition('talk', lambda e: anim(e).is_finished() and aic(e).plan[0] == 'talk'),
        Transition('hit_wall', lambda e: anim(e).is_finished() and phys(e).is_hitting_wall), 
        Transition('idle', lambda e: anim(e).is_finished())
    ]
)
HIT_WALL_STATE = State('hit_wall',
    [
        Transition('talk', lambda e: anim(e).is_finished() and aic(e).plan[0] == 'talk'),
        Transition('hit_floor', lambda e: anim(e).is_finished() and phys(e).is_hitting_floor),
        Transition('air', lambda e: anim(e).is_finished()) 
    ]
)
TALK_STATE = State('talk',
    [
        Transition('air', lambda e: not phys(e).is_grounded),
        Transition('idle', lambda e: aic(e).plan[0] != 'talk')
    ]
)
GO_SLEEP_STATE = State('go_sleep',
    [
        Transition('sleeping', lambda e: anim(e).is_finished())
    ]
)
SLEEPING_STATE = State('sleeping',
    [
        Transition('air', lambda e: not phys(e).is_grounded),
        Transition('idle', lambda e: aic(e).plan[0] != 'sleep')
    ]
)
GO_SIT_STATE = State('go_sit',
    [
        Transition('sit', lambda e: anim(e).is_finished())
    ]
)
SIT_STATE = State('sit',
    [
        Transition('air', lambda e: not phys(e).is_grounded),
        Transition('idle', lambda e: aic(e).plan[0] != 'sit')
    ]
)

NPC_STATES: list[State] = [
    IDLE_STATE, 
    AIR_STATE, 
    HIT_FLOOR_STATE, 
    HIT_WALL_STATE, 
    TALK_STATE, 
    GO_SLEEP_STATE, 
    SLEEPING_STATE,
    GO_SIT_STATE,
    SIT_STATE
]

# =================================================================================================================================

# State graph for the ITEMS
STILL_STATE = State('still',
    [
        Transition('bounce', lambda e: phys(e).is_hitting_floor),
    ]
)
BOUNCE_STATE = State('bounce',
    [
        Transition('still', lambda e: anim(e).is_finished()),
    ]
)

PROP_STATES: list[State] = [
    STILL_STATE,
    BOUNCE_STATE
]