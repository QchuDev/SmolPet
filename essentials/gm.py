import random
from essentials import components
from essentials.basics import ParticlesManager, SFXManager, World
from essentials.components import AIController, AchievementCycle, CharactersHandler, MouseDrag, create_paragraph_texture
from essentials.window_setup import RENDERER, SCREEN_H, SCREEN_W
from pygame._sdl2 import Texture
import prefabs

class GameManager:
    first_time = False
    # Starting value should be true, if want to play ofc
    running = True
    unlocked_entites = []
    game_completed = False
    _tick = 0
    _tick_speed = 120  # _tick_speed = 60 ticks/sec * (wait ammount)

    # Empty for now, but here goes the achievements_displayer
    achievements_displayer:AchievementCycle = AchievementCycle()
    total_achievements:int = 0
    unlocked_achievements:int = 0

    @classmethod
    def start(cls):
        from achievements import ALL_ACHIEVEMENTS
        for n, a in ALL_ACHIEVEMENTS.items():
            if a[0]:
                cls.unlocked_achievements += 1 

    # The update method of the class calls funcionts in an interspersed manner
    @classmethod
    def update(cls):
        cls._tick += 1

        if cls._tick == 40:
            cls.check_user_activity()
        elif cls._tick == 80:
            for i, e in enumerate(World.entities):
                if not e.active:
                    World.entities.pop(i)
        elif cls._tick >= 120:
            cls.check_for_unlocks()
            cls._tick = 0

    # Checks of game states
    @classmethod
    def check_for_unlocks(cls):
        achievement_left = False
        from achievements import ALL_ACHIEVEMENTS
        for n, a in ALL_ACHIEVEMENTS.items():
            if a[0]: continue
            if n != 'BOOOM!': achievement_left = True   # CHECK FOR EVERY ACHIEVEMENT, but not itself
            condition_met = a[1]()
            if condition_met:
                cls.unlocked_achievements += 1
                a[0] = True
                cls.trigger_achievement_unlock(n,a)
        
        cls.game_completed = not achievement_left
    
    
    @classmethod
    def trigger_achievement_unlock(cls, name:str, a: list):

        # 1. Feedback en consola (opcional)
        print(f"DEBUG: Desbloqueado {name}")
        # 2. Si el displayer está vinculado, agregamos la lista de datos
        if cls.achievements_displayer:
            # im = [time_left, x, y, target_x, target_y, (src_x, src_y), name, desc]
            # Usamos los datos de tu diccionario: a[3] es la pos del icono, a[2] desc
            # Ponemos x inicial fuera de pantalla (ej. SCREEN_W + 50)
            def create_text_texture(text, color=(255, 255, 255)):
                surf = components.pixel_font.render(text, False, color)
                return Texture.from_surface(RENDERER, surf)

            # Cuando agregues el logro a self.showed_img, añade las texturas al final:
            # im = [lifetime, x, y, target_x, target_y, icono, nombre, desc, tex_nombre, tex_desc]
            name_tex = create_text_texture(name, (255, 215, 0)) # Dorado para el título
            desc_tex = create_paragraph_texture(a[2], (255, 255, 255)) # Blanco para la descripción
            progress = create_text_texture(f'{cls.unlocked_achievements}/{cls.total_achievements} achievements')

            target_x = SCREEN_W - 270 # Ajusta según el ancho de tu sprite
            new_popup = [
                10.0,            # time_left
                SCREEN_W + 50,   # x actual
                SCREEN_H*0.8,    # y actual
                target_x,        # target_x
                SCREEN_H*0.8,    # target_y
                a[3],            # source_pos (x, y) del icono
                name_tex,        # textura del Nombre
                desc_tex,        # textura de la Descripción
                True,            # first time
                progress         # progress u/t
            ]
            cls.achievements_displayer.showed_img.append(new_popup)

            # Play sound effect
            SFXManager.play('unlock2')

        else:
            print('No existing achievements displayer')


    SEARCH_KEYWORDS = {
        'dino':     ['dino', 'dinosaurio', 't-rex'],
        'squalo':   ['squalo', 'tiburon', 'shark', 'pez', 'fish'],
        'pachu':    ['pachu', 'yo', 'bombonita', 'sexy'],
        'cuchu':    ['cuchu', 'novio', 'autista', 'lindo' 'ñoño', 'melo', 'bombon', 'piojito'],
        'pol' :     ['pol', 'cachorro', 'bebe', 'carboncito', 'coquito', 'pulguita'],
        'doki' :    ['doki', 'perro', 'gordito', 'fofo'],
        'tiramisu': ['tiramisu', 'torta', 'postre', 'rico'],
        'balloon' : ['globo', 'globos', 'fiesta'],
        'poop':     ['caca', 'popo', 'sorete'],
        'coke':     ['coca', 'coca cola', 'gaseosa', 'delicia', 'manjar'],
        'coffee':   ['cafe', 'submarino', 'te', 'rico']
    }

    start_video = True
    @classmethod
    def check_user_activity(cls):
        # Retrieve the shared_state from the user_activity
        from user_activity import shared_state

        for n, a in cls.SEARCH_KEYWORDS.items():
            if shared_state['last_search'] in a and n not in cls.unlocked_entites:
                if n == 'balloon':
                    ammount = 10
                    balloons = [prefabs.create_entity(n, SCREEN_W*random.uniform(0.2, 0.8), SCREEN_H*random.uniform(0.14, 0.5)) for i in range(ammount)]
                    cls.unlocked_entites.append(n)
                    for b in balloons:
                        World.entities.append(b) 

                else:
                    new_entity = prefabs.create_entity(n, SCREEN_W*0.144, SCREEN_H*0.141)

                    cls.unlocked_entites.append(n)
                    World.entities.append(new_entity)
        
        # when watching a movie or somethin
        if shared_state['is_watching_ytvideo'] or shared_state['is_watching_movie']:
            if not cls.start_video:
                cls.start_video = True
                # if missing bucket of popcorn, then spawn it
                r = random.uniform(0.2, 0.8)
                popcornb_entity = prefabs.create_entity('popcorn bucket', SCREEN_W*r, SCREEN_H*0.4, push=False)

                if 'popcorn bucket' not in cls.unlocked_entites: 
                    cls.unlocked_entites.append('popcorn bucket')

                World.entities.append(popcornb_entity)

                for e in World.entities:
                    aic = e.get_component(AIController)
                    if aic:
                        if aic.plan[0] != 'sleep':
                            aic.plan.append('move')
                            aic.target_setted = True
                            aic.target_x = popcornb_entity.pos.x + random.uniform(-100, 100)
                            aic.plan.append('sit')
                            aic.plan.append('sit')
        else:
            cls.start_video = False

    # For achievement conditions
    @classmethod
    def is_unlocked(cls, name):
        return name in cls.unlocked_entites
    
    @classmethod
    def all_sleeping(cls) -> bool:
        ents = World.entities

        from .components import AIController    # imports can be used inside methods to avoid weird dependency loops
        from characters_setup import CHARACTERS
        count = 0
        for e in ents:
            aic = e.get_component(AIController)
            if aic:
                if aic.plan[0] != 'sleep':
                    return False
                count += 1

        return count == len(CHARACTERS)   # HORRIBLE
    
    @classmethod
    def top_speed(cls) -> float:
        top_speed: float= 0

        from .components import PhysicalBall
        for e in World.entities:
            phys = e.get_component(PhysicalBall)
            if phys:
                top_speed = max(top_speed, phys.vel.magnitude())
                
        return top_speed
    
    @classmethod
    def lifting_a_mini(cls) -> bool:
        for e in World.entities:
            md = e.get_component(MouseDrag)
            ch = e.get_component(CharactersHandler)
            if md and ch:
                if md.is_pulling:
                    return True

        return False