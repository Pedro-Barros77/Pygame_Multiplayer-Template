import pygame, sys, socket, threading, time, json, jsonpickle

from domain.models.network_data import Data as NetData


playing = False

def handle_events(game):
    """Iterates through each event and call it's appropriate function.
    Args:
        game (Game): The currently running game.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_app()
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event.key, game)
        elif event.type == pygame.KEYUP:
            handle_keyup(event.key, game)
                
                
def handle_keydown(key, game):
    """Decides what to do with the key pressed by the user.
    Args:
        key (int): The pygame keycode of the key.
        game (Game): The currently running game.
    """
    if key not in game.pressed_keys:
        game.pressed_keys.append(key)
    

def handle_keyup(key, game):
    """Decides what to do with the key released by the user.
    Args:
        key (int): The pygame keycode of the key.
        game (Game): The currently running game.
    """
    if key in game.pressed_keys:
        game.pressed_keys.remove(key)

def quit_app():
    """Stops the game and closes application.
    """
    pygame.display.quit()
    pygame.quit()
    sys.exit()


    
def host_game(game, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    client, addr = server.accept()
    
    #define game objects
    game.player_conn_id = 1
    
    #implementar handle connection
    threading.Thread(target=handle_connection, args=(client, game.player_conn_id)).start()
    
def enter_game(game, host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    #define game objects
    game.player_conn_id = 2
    
    #implementar handle connection
    threading.Thread(target=handle_connection, args=(client, game.player_conn_id)).start()
    
def handle_connection(client: socket.socket, player_id):
    while playing:
        
        data_to_send = NetData(message = f"Hello from player {player_id}")
        
        client.send(class_to_json(data_to_send))
        data: NetData = json_to_class(client.recv(1024))
        
        if not data:
            continue
        else:
            print(data.message)
            
        time.sleep(0.5)
        print('while:', player_id)
                
    client.close()
    
    
def class_to_json(data):
    return jsonpickle.encode(data).encode('utf-8')

def json_to_class(data):
    return jsonpickle.decode(data.decode('utf-8'))