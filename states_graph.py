from basics import Transition, State
from components import AIController, PhysicalBall, Animator
from game_consts import SLIDE_STOP, BOUNCE_STOP

anim = lambda e: e.get_component(Animator)
phys = lambda e: e.get_component(PhysicalBall)
aic = lambda e: e.get_component(AIController)

# Creating the states for the StatesManager 
IDLE_STATE = State('idle',
    [
        Transition('air', lambda e: not phys(e).is_grounded),
        Transition('hit_floor', lambda e: phys(e).is_hitting_floor),
        Transition('hit_wall', lambda e: phys(e).is_hitting_wall),
        Transition('talk', lambda e: aic(e).curr_action == 'talk'),
        Transition('go_sleep', lambda e: aic(e).curr_action == 'sleep')
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
        Transition('idle', lambda e: anim(e).is_finished() and phys(e).is_grounded),
        Transition('talk', lambda e: anim(e).is_finished() and aic(e).curr_action == 'talk'),
        Transition('hit_wall', lambda e: anim(e).is_finished() and phys(e).is_hitting_wall),
        Transition('air', lambda e: anim(e).is_finished()) 
    ]
)
HIT_WALL_STATE = State('hit_wall',
    [
        Transition('idle', lambda e: anim(e).is_finished() and phys(e).is_grounded),
        Transition('talk', lambda e: anim(e).is_finished() and aic(e).curr_action == 'talk'),
        Transition('hit_floor', lambda e: anim(e).is_finished() and phys(e).is_hitting_floor),
        Transition('air', lambda e: anim(e).is_finished()) 
    ]
)
TALK_STATE = State('talk',
    [
        Transition('air', lambda e: not phys(e).is_grounded),
        Transition('idle', lambda e: aic(e).curr_action != 'talk')
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
        Transition('idle', lambda e: aic(e).curr_action != 'sleep')
    ]
)

STATES: list[State] = [
    IDLE_STATE, 
    AIR_STATE, 
    HIT_FLOOR_STATE, 
    HIT_WALL_STATE, 
    TALK_STATE, 
    GO_SLEEP_STATE, 
    SLEEPING_STATE
]