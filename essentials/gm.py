from essentials import components
from essentials.basics import ParticlesManager, World
from essentials.components import AchievementCycle, create_paragraph_texture
from essentials.window_setup import RENDERER, SCREEN_H, SCREEN_W
from pygame._sdl2 import Texture

import prefabs

class GameManager:
    # Starting value should be true, if want to play ofc
    first_time = False
    running = True
    unlocked_entites = []
    game_completed = False

    _tick = 0
    _tick_speed = 120  # _tick_speed = 60 ticks/sec * (wait ammount)

    # Empty for now, but here goes the achievements_displayer
    achievements_displayer:AchievementCycle = AchievementCycle()
    
    # The update method of the class calls funcionts in an interspersed manner
    @classmethod
    def update(cls):
        cls._tick += 1

        if cls._tick == 60:
            cls.check_user_activity()
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
            achievement_left = True
            condition_met = a[1]()
            if condition_met:
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

            target_x = SCREEN_W - 270 # Ajusta según el ancho de tu sprite
            new_popup = [
                10.0,            # time_left
                SCREEN_W + 50,   # x actual
                SCREEN_H*0.8,    # y actual (el update lo bajará si hay otros)
                target_x,        # target_x
                SCREEN_H*0.8,    # target_y
                a[3],            # source_pos (x, y) del icono
                name_tex,        # textura del Nombre
                desc_tex         # textura de la Descripción
            ]
            cls.achievements_displayer.showed_img.append(new_popup)
        else:
            print('No existing achievements displayer')


    SEARCH_KEYWORDS = {
        'dino': ['dino', 'dinosaurio', 't-rex'],
        'squalo': ['squalo', 'tiburon', 'shark', 'pez', 'fish'],
        'pachu': ['pachu', 'yo', 'bombon'],
        'cuchu': ['cuchu', 'novio', 'autista', 'lindo' 'ñoño'],
        'pol' : ['pol', 'perro', 'bebe', 'carboncito', 'coquito'],
        'tiramisu': ['tiramisu', 'torta', 'postre'],
        'balloon' : ['globos', 'fiesta']
    }

    @classmethod
    def check_user_activity(cls):
        # Retrieve the shared_state from the user_activity
        from user_activity import shared_state

        for n, a in cls.SEARCH_KEYWORDS.items():
            if shared_state['last_search'] in a and n not in cls.unlocked_entites:
                new_entity = prefabs.create_entity(n, SCREEN_W*0.144, SCREEN_H*0.141)
                cls.unlocked_entites.append(n)
                World.entities.append(new_entity)

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
                if aic.curr_action != 'sleep':
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
  