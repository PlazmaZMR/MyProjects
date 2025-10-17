import pygame
import sys
import random


pygame.init()


width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Boss Fight Game")


MAIN_GAME = 'main_game'
VICTORY_ROOM = 'victory_room'
current_room = MAIN_GAME


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)

def reset_game():
    global player_x, player_y, player_hp, boss_hp, game_state, current_room, buffer_active, buffer_start_time, last_buffer_time
    player_x = width // 4
    player_y = height // 2
    player_hp = player_max_hp
    boss_hp = boss_max_hp
    game_state = EXPLORING
    current_room = MAIN_GAME
    buffer_active = False
    buffer_start_time = 0
    last_buffer_time = 0
    return

def update_buffer():
    global buffer_active, buffer_start_time
    current_time = pygame.time.get_ticks()
    
  
    if buffer_active and current_time - buffer_start_time >= buffer_duration:
        buffer_active = False
    
    return buffer_active


player_size = 40
player_x = width // 4
player_y = height // 2
player_speed = 5
player_hp = 100
player_max_hp = 100
player_battle_pos = (200, 400)


boss_size = 60
boss_x = 3 * width // 4
boss_y = height // 2
boss_hp = 125  
boss_max_hp = 125  
boss_battle_pos = (600, 300)


EXPLORING = 'exploring'
BATTLE = 'battle'
game_state = EXPLORING


buffer_active = False
buffer_duration = 3000 
buffer_start_time = 0
buffer_cooldown = 5000 
last_buffer_time = 0
buffer_defense = 0.5 


attacks = {
    'Melee': {'damage': (13, 21), 'accuracy': 0.85},
    'Ranged': {'damage': (8, 17), 'accuracy': 0.90},
    'Magic': {'damage': (17, 26), 'accuracy': 0.75},
    'Psychic': {'damage': (21, 30), 'accuracy': 0.65}
}
current_turn = 'player'
battle_message = ''
battle_options = list(attacks.keys())
selected_option = 0


font = pygame.font.Font(None, 36)

def draw_hp_bar(x, y, width, height, hp, max_hp, color):
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, width + 4, height + 4))
    pygame.draw.rect(screen, RED, (x, y, width, height))
    health_width = int((hp / max_hp) * width)
    pygame.draw.rect(screen, color, (x, y, health_width, height))

def draw_victory_room():
    screen.fill(BLACK)
    
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        pygame.draw.circle(screen, GOLD, (x, y), 10)
    
   
    victory_text = font.render("Congratulations! You've defeated the boss!", True, WHITE)
    screen.blit(victory_text, (width//2 - victory_text.get_width()//2, height//2))

def handle_battle():
    global current_turn, battle_message, player_hp, boss_hp, game_state, current_room, buffer_active

    if current_turn == 'boss' and boss_hp > 0:  
        buffer_active = update_buffer()
        
       
        attack = random.choice(list(attacks.keys()))
        if random.random() < attacks[attack]['accuracy']:
            damage = random.randint(*attacks[attack]['damage'])

            if buffer_active:
                damage = int(damage * (1 - buffer_defense))
                battle_message = f'Boss used {attack} and dealt {damage} damage! (Buffered)'
            else:
                battle_message = f'Boss used {attack} and dealt {damage} damage!'
            player_hp -= damage
        else:
            battle_message = 'Boss attack missed!'
        
       
        if player_hp <= 0:
            player_hp = 0  
            battle_message = 'Game Over! Boss wins! Press 1 to try again'
            return 'game_over'
        
        current_turn = 'player'
        return None
    elif current_turn == 'victory':
        return 'victory'  
    return None

def draw_battle_screen():
    screen.fill(GRAY)
    
    
    pygame.draw.rect(screen, (50, 120, 50), (0, 450, width, 150))  
    pygame.draw.rect(screen, (100, 100, 200), (0, 0, width, 450))  
    
    
    player_color = (0, 255, 255) if buffer_active else BLUE 
    pygame.draw.rect(screen, player_color, (*player_battle_pos, player_size, player_size))
    pygame.draw.rect(screen, RED, (*boss_battle_pos, boss_size, boss_size))
    
   
    draw_hp_bar(50, 50, 200, 20, player_hp, player_max_hp, GREEN)
    player_hp_text = font.render(f"Player HP: {player_hp}/{player_max_hp}", True, BLACK)
    screen.blit(player_hp_text, (50, 25))
    
    draw_hp_bar(550, 50, 200, 20, boss_hp, boss_max_hp, GREEN)
    boss_hp_text = font.render(f"Boss HP: {boss_hp}/{boss_max_hp}", True, BLACK)
    screen.blit(boss_hp_text, (550, 25))
    

    current_time = pygame.time.get_ticks()
    if buffer_active:
        time_left = (buffer_duration - (current_time - buffer_start_time)) // 1000
        buffer_text = font.render(f"Buffer Active! ({time_left}s)", True, BLACK)
    elif current_time - last_buffer_time < buffer_cooldown:
        cooldown_left = (buffer_cooldown - (current_time - last_buffer_time)) // 1000
        buffer_text = font.render(f"Buffer Cooldown ({cooldown_left}s)", True, BLACK)
    else:
        buffer_text = font.render("Press B for Buffer", True, BLACK)
    screen.blit(buffer_text, (50, 80))
    
    
    pygame.draw.rect(screen, WHITE, (50, 480, width-100, 100))
    message_text = font.render(battle_message, True, BLACK)
    screen.blit(message_text, (width//2 - message_text.get_width()//2, 500))
    
    
    pygame.draw.rect(screen, WHITE, (width-250, 380, 200, 200))
    for i, option in enumerate(battle_options):
        color = WHITE if i == selected_option else BLACK
        pygame.draw.rect(screen, BLACK if i == selected_option else GRAY, 
                        (width-240, 390 + i * 45, 180, 40), 
                        0 if i == selected_option else 1)
        option_text = font.render(option, True, color if i == selected_option else BLACK)
        screen.blit(option_text, (width-230, 395 + i * 45))

def draw_exploring_screen():
    screen.fill(WHITE)
    
    
    pygame.draw.rect(screen, BLACK, (50, 50, width-100, height-100), 2)
    
    
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    
   
    pygame.draw.rect(screen, RED, (boss_x, boss_y, boss_size, boss_size))
    
   
    draw_hp_bar(player_x, player_y - 20, player_size, 5, player_hp, player_max_hp, GREEN)
    draw_hp_bar(boss_x, boss_y - 20, boss_size, 5, boss_hp, boss_max_hp, GREEN)


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_state == BATTLE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(battle_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(battle_options)
                elif event.key == pygame.K_b and current_turn == 'player':
                    current_time = pygame.time.get_ticks()
                    if not buffer_active and current_time - last_buffer_time >= buffer_cooldown:
                        buffer_active = True
                        buffer_start_time = current_time
                        last_buffer_time = current_time
                        battle_message = "Buffer activated! Damage reduced by 50%!"
                elif event.key == pygame.K_RETURN and current_turn == 'player':
                    selected_attack = battle_options[selected_option]
                    if random.random() < attacks[selected_attack]['accuracy']:
                        damage = random.randint(*attacks[selected_attack]['damage'])
                        boss_hp -= damage
                        battle_message = f'You used {selected_attack} and dealt {damage} damage!'
                        
                       
                        if boss_hp <= 0:
                            boss_hp = 0  
                            battle_message = 'Victory! Press 2 to enter treasure room!'
                            current_turn = 'victory'  
                            continue  
                    else:
                        battle_message = 'Your attack missed!'
                    if current_turn != 'victory':  
                        current_turn = 'boss'
    
    if game_state == EXPLORING:
        keys = pygame.key.get_pressed()
        
        
        new_x = player_x
        new_y = player_y
        
        if keys[pygame.K_a]:
            new_x -= player_speed
        if keys[pygame.K_d]:
            new_x += player_speed
        if keys[pygame.K_w]:
            new_y -= player_speed
        if keys[pygame.K_s]:
            new_y += player_speed
            
        
        if 50 < new_x < width-50-player_size:
            player_x = new_x
        if 50 < new_y < height-50-player_size:
            player_y = new_y
            
        
        if (abs(player_x - boss_x) < boss_size and 
            abs(player_y - boss_y) < boss_size and 
            keys[pygame.K_e]):
            game_state = BATTLE
            battle_message = 'Battle Start!'
            current_turn = 'player'
    
    if current_room == VICTORY_ROOM:
        draw_victory_room()
    else:
        if game_state == EXPLORING:
            draw_exploring_screen()
        else:  
            draw_battle_screen()
            battle_result = handle_battle()
            
            
            if battle_result == 'game_over':
                keys = pygame.key.get_pressed()
                if keys[pygame.K_1]:
                    reset_game()
            elif battle_result == 'victory' or boss_hp <= 0:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_2]:
                    current_room = VICTORY_ROOM
    
    pygame.display.flip()
    clock.tick(60)