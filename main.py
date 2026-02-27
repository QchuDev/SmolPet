from essentials.gm import GameManager


if __name__ == '__main__':
    import pygame

    # Import Setup constants
    from essentials.window_setup import RENDERER, TRANSPARENT_COLOR, FPS, SCREEN_CENTER
    # Setup scripts
    from essentials.debug_tools import monitor
    import user_activity

    # Execute the entities_setup before reading World
    from objects_setup import prts_manager, persist_manager
    from essentials.basics import MouseInput, UIManager, World

    # Time Variables
    clock = pygame.time.Clock()
    dt = 0.01
    dt_phys = 1/60  # once per 60FPS
    accumulator = 0.0
    scan_timer=0

    ## MAIN LOOP ======================================================
    while GameManager.running:
        # Update delta_time
        dt = clock.tick(FPS) / 1000
        accumulator += dt
        dt = max(0.001, min(0.1, dt))
        
        # Update the GameManager
        GameManager.update()

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
            accumulator -= dt_phys
        
        # DRAWS
        for entity in World.entities:
            entity.draw()       # Draw entities

        # Particles manager
        prts_manager.update(dt)
        prts_manager.draw()

        # UI ELEMENTS UPDATE AND DRAW
        for u in UIManager.ui_elements:
            u.update(dt)
        

        u.pos.x, u.pos.y = SCREEN_CENTER.x, SCREEN_CENTER.y
        for u in UIManager.ui_elements:
            u.draw()

        # Debug tools
        monitor.clock.tick()
        monitor.update(dt)
        monitor.render()

        # SHOW AL RENDERED STUFF
        RENDERER.present()


    persist_manager.save(World.entities)
    pygame.quit()