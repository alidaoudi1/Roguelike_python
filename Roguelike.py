import libtcodpy as libtcod
from input_handlers import handle_keys
from Entity import Entity, get_blocking_entities_at_location
from render_functions import render_all
from render_functions import clear_all
from map_objects.game_map import GameMap
from fov_functions import initialize_fov
from fov_functions import recompute_fov
from components.fighter import Fighter
from components.ai import BasicMonster
from GameStates import GameStates
def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    max_monsters_per_room = 3 
    room_max_size = 10 
    room_min_size = 6
    max_rooms = 30 
    
    
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    
    colors={
            'dark_wall':libtcod.Color(0,0,100),
            'dark_ground':libtcod.Color(50,50,150),
            'light_wall':libtcod.Color(130,110,50),
            'light_ground':libtcod.Color(200,180,50)
            }
    
    fov_recompute = True
    
    key=libtcod.Key()
    mouse = libtcod.Mouse()
    game_state= GameStates.PLAYERS_TURN
    fighter_component = Fighter(hp=30,defense = 2, power = 5 )
    
    player = Entity(30,30,'@',libtcod.white,'Player',blocks=True,fighter = fighter_component)
    entities = [player]
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow,'NPC',blocks=True)
    entities = [npc,player]
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    con = libtcod.console_new(screen_width,screen_height)
    game_map = GameMap(map_width,map_height)
    game_map.make_map(max_rooms,room_min_size,room_max_size,map_width,map_height,player,entities,max_monsters_per_room)
    fov_map = initialize_fov(game_map)

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse) 
        if fov_recompute:
            recompute_fov(fov_map,player.x,player.y,fov_radius,fov_light_walls,fov_algorithm)
        render_all(con,entities,game_map,fov_map,fov_recompute,screen_width,screen_height,colors)
        fov_recompute = False
        libtcod.console_flush()
        clear_all(con,entities)
        
        
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        if move and game_state == GameStates.PLAYERS_TURN:
            dx,dy = move 
            destination_x = player.x+dx
            destination_y = player.y+dy
            if not game_map.is_blocked(destination_x,destination_y):
                target = get_blocking_entities_at_location(entities,destination_x,destination_y)
                if target :
                    player.fighter.attack(target)
                else :
                    player.move(dx,dy)
                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN
            print(game_map.is_blocked(player.x+dx,player.y+dy))
                

        if exit:
            return True
        
        if fullscreen : 
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    entity.ai.take_turn(player,fov_map,game_map,entities)
            game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()