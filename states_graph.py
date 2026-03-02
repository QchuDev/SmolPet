from essentials.basics import Transition, State
from essentials.components import AIController, PhysicalBall, Animator
from game_consts import SLIDE_STOP, BOUNCE_STOP


# Creating the states for the NPCS
IDLE_STATE = State('idle',
    [
        Transition('air', lambda ctx: not ctx.phys.is_grounded),
        Transition('hit_floor', lambda ctx: ctx.phys.is_hitting_floor),
        Transition('hit_wall', lambda ctx: ctx.phys.is_hitting_wall),
        Transition('talk', lambda ctx: ctx.aic.plan[0] == 'talk'),
        Transition('go_sleep', lambda ctx: ctx.aic.plan[0] == 'sleep'),
        Transition('go_sit', lambda ctx: ctx.aic.plan[0] == 'sit')
    ]
)
AIR_STATE = State('air',
    [
        Transition('hit_floor', lambda ctx: ctx.phys.is_hitting_floor),
        Transition('hit_wall', lambda ctx: ctx.phys.is_hitting_wall),
        Transition('idle', lambda ctx: ctx.phys.is_grounded and abs(ctx.phys.vel.x) == 0)
    ]
)
HIT_FLOOR_STATE = State('hit_floor',
    [
        Transition('talk', lambda ctx: ctx.anim.is_finished() and ctx.aic.plan[0] == 'talk'),
        Transition('hit_wall', lambda ctx: ctx.anim.is_finished() and ctx.phys.is_hitting_wall), 
        Transition('idle', lambda ctx: ctx.anim.is_finished())
    ]
)
HIT_WALL_STATE = State('hit_wall',
    [
        Transition('talk', lambda ctx: ctx.anim.is_finished() and ctx.aic.plan[0] == 'talk'),
        Transition('hit_floor', lambda ctx: ctx.anim.is_finished() and ctx.phys.is_hitting_floor),
        Transition('air', lambda ctx: ctx.anim.is_finished()) 
    ]
)
TALK_STATE = State('talk',
    [
        Transition('air', lambda ctx: not ctx.phys.is_grounded),
        Transition('idle', lambda ctx: ctx.aic.plan[0] != 'talk')
    ]
)
GO_SLEEP_STATE = State('go_sleep',
    [
        Transition('sleeping', lambda ctx: ctx.anim.is_finished())
    ]
)
SLEEPING_STATE = State('sleeping',
    [
        Transition('air', lambda ctx: not ctx.phys.is_grounded),
        Transition('idle', lambda ctx: ctx.aic.plan[0] != 'sleep')
    ]
)
GO_SIT_STATE = State('go_sit',
    [
        Transition('sit', lambda ctx: ctx.anim.is_finished())
    ]
)
SIT_STATE = State('sit',
    [
        Transition('air', lambda ctx: not ctx.phys.is_grounded),
        Transition('idle', lambda ctx: ctx.aic.plan[0] != 'sit')
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
        Transition('bounce', lambda ctx: ctx.phys.is_hitting_floor),
    ]
)
BOUNCE_STATE = State('bounce',
    [
        Transition('still', lambda ctx: ctx.anim.is_finished()),
    ]
)

PROP_STATES: list[State] = [
    STILL_STATE,
    BOUNCE_STATE
]