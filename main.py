


def main():
    from essentials.basics import ParticlesManager, SFXManager
    from essentials.gm import GameManager
    from essentials.components import init_components_resources
    from game_config.prefabs import init_prefabs
    from game_config.objects_setup import init_ui
    import pygame
    
    # Import Setup constants
    from essentials.window_setup import RENDERER, TRANSPARENT_COLOR, FPS, SCREEN_CENTER
    # Setup scripts
    # from essentials.debug_tools import monitor
    import game_config.user_activity

    # Execute the entities_setup before reading World
    from game_config.objects_setup import prts_manager, persist_manager
    from essentials.basics import MouseInput, UIManager, World

    # Time Variables
    clock = pygame.time.Clock()
    dt = 0.01
    dt_phys = 1/60  # once per 60FPS
    accumulator = 0.0
    time_playing = 0

    pygame.mixer.init()

    ## MAIN LOOP ======================================================
    GameManager.start()
    SFXManager.start()
    ParticlesManager.start()
    init_components_resources()
    init_prefabs()
    init_ui()

    while GameManager.running:
        # Update delta_time
        dt = clock.tick(FPS) / 1000
        accumulator += dt
        dt = max(0.001, min(0.1, dt))
        
        # Update the GameManager
        GameManager.update(dt)

        # Draw the background
        RENDERER.draw_color = TRANSPARENT_COLOR
        RENDERER.clear()

        # Update mouse inputs
        MouseInput.update()
        
        # To clean the request queue
        for event in pygame.event.get():
            pass
        
        # Update the entities on a constant way, when the accumulator exceeds the dt_phys (delta time for physics)
        while accumulator >= dt_phys:
            # Update entities
            for entity in World.entities:
                entity.update(dt_phys)

            # UI ELEMENTS UPDATE AND DRAW
            for u in UIManager.ui_elements:
                u.update(dt)
            u.pos.x, u.pos.y = SCREEN_CENTER.x, SCREEN_CENTER.y

            accumulator -= dt_phys
            
        time_playing += dt

        # DRAWS
        for entity in World.entities:
            entity.draw()       # Draw entities

        # Particles manager
        prts_manager.update(dt)
        prts_manager.draw()

        for u in UIManager.ui_elements:
            u.draw()

        # Debug tools
        #monitor.clock.tick()
        #monitor.update(dt)
        #monitor.render()

        # SHOW AL RENDERED STUFF
        RENDERER.present()

    persist_manager.save(World.entities)
    pygame.quit()

import traceback
if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Esto guarda el error en un archivo de texto antes de cerrar
        with open("ERROR_LOG.txt", "w") as f:
            f.write(traceback.format_exc())
        # También lo imprime por si tienes la consola abierta
        print(traceback.format_exc())