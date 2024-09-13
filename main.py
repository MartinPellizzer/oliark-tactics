import numpy
import pygame

'''
print(numpy.linspace(0, 300, 20))
quit()
'''


global_scale = 6

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Oliark Tactics')
clock = pygame.time.Clock()
running = True

dt = 0

camera_pos_x = 300
camera_pos_y = 200

n_tiles_x = 8
n_tiles_y = 4
tiles_images = []

tile_image = pygame.image.load('images/test-tile.png').convert()
tile_image_scaled = pygame.transform.scale(tile_image, (32*global_scale, 32*global_scale))

for i in range(n_tiles_x * n_tiles_y):
    tiles_images.append(tile_image_scaled)

player_2 = pygame.image.load('images/char-test-64x64.png').convert_alpha()
player_2_scaled = pygame.transform.scale(player_2, (32*global_scale, 32*global_scale))
player_2_x = 0
player_2_pos_x_end = 0
player_2_pos_y_end = 0
moving = False
player_2_coord_i = 1
player_2_coord_j = 1
player_2_pos_x = 0
player_2_pos_y = 0
moving_dir = 'down'
moving_arr_index = 0
moving_arr = ['r', 'r', 'd', 'r', 'u', 'u', 'l']

player_image_64x64 = pygame.image.load('images/char-test-64x64.png').convert_alpha()
player_image_64x64_scaled = pygame.transform.scale(player_image_64x64, (32*global_scale, 32*global_scale))

player_image_32x32 = pygame.image.load('images/char-test-32x32.png').convert_alpha()
player_image_32x32_scaled = pygame.transform.scale(player_image_32x32, (32*global_scale, 32*global_scale))

enemy_image = pygame.image.load('images/image-test.png').convert()
enemy_image_scaled = pygame.transform.scale(enemy_image, (32*global_scale, 32*global_scale))

player_pos = pygame.Vector2(32*global_scale//2, 32*global_scale//4)

mouse_pos_x = 0
mouse_pos_y = 0

start_mouse_pos_x = 0
start_mouse_pos_y = 0

start_mouse_pos_x_old = 300
start_mouse_pos_y_old = 300

curr_mouse_pos_x = 0
curr_mouse_pos_y = 0

just_clicked = False

player_cell_x = 0
player_cell_y = 0

key_pressed_up = False
key_pressed_down = False
key_pressed_left = False
key_pressed_right = False

char_orientation = 'down'

def tile_pos_from_coord(i, j):
    x = (32*global_scale//2*i - 32*global_scale//2*j) + camera_pos_x
    y = (32*global_scale//4*i + 32*global_scale//4*j) + camera_pos_y
    return x, y

def char_pos_from_coord(i, j):
    x = (32*global_scale//2*i - 32*global_scale//2*j) + camera_pos_x 
    y = (32*global_scale//4*i + 32*global_scale//4*j) + camera_pos_y - (32*global_scale) + (32*global_scale*0.4)
    return x, y

player_2_pos_x, player_2_pos_y = char_pos_from_coord(player_2_coord_i, player_2_coord_j)

moving_sequence_start = False

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.MOUSEWHEEL:
            print(event.x, event.y)
            if event.y == 1: 
                if global_scale < 16:
                    global_scale += 1
            if event.y == -1: 
                if global_scale > 1:
                    global_scale -= 1
            for i in range(n_tiles_x * n_tiles_y):
                tiles_images[i] = pygame.transform.scale(tile_image, (32*global_scale, 32*global_scale))
            player_2_scaled = pygame.transform.scale(player_2, (32*global_scale, 32*global_scale))
            player_image_32x32_scaled = pygame.transform.scale(player_image_32x32, (32*global_scale, 32*global_scale))
            player_image_64x64_scaled = pygame.transform.scale(player_image_64x64, (32*global_scale, 32*global_scale))
            enemy_image_scaled = pygame.transform.scale(enemy_image, (32*global_scale, 32*global_scale))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if moving_sequence_start == False:
                    moving_sequence_start = True

    # TODO: perform series of move one after the other from moving_arr on keypress K_a
    if moving_sequence_start:
        if moving_arr_index < len(moving_arr):
            moving_dir_curr = moving_arr[moving_arr_index]
            if moving_dir_curr == 'l':
                if moving == False:
                    if player_2_coord_i > 0:
                        player_2_coord_i -= 1
                        player_2_pos_x_end, player_2_pos_y_end = char_pos_from_coord(player_2_coord_i, player_2_coord_j)
                        moving = True
                        moving_dir = 'left'
            elif moving_dir_curr == 'r':
                if moving == False:
                    if player_2_coord_i < n_tiles_x-1:
                        player_2_coord_i += 1
                        player_2_pos_x_end, player_2_pos_y_end = char_pos_from_coord(player_2_coord_i, player_2_coord_j)
                        moving = True
                        moving_dir = 'right'
            elif moving_dir_curr == 'u':
                if moving == False:
                    if player_2_coord_j > 0:
                        player_2_coord_j -= 1
                        player_2_pos_x_end, player_2_pos_y_end = char_pos_from_coord(player_2_coord_i, player_2_coord_j)
                        moving = True
                        moving_dir = 'up'
            elif moving_dir_curr == 'd':
                if moving == False:
                    if player_2_coord_j < n_tiles_y-1:
                        player_2_coord_j += 1
                        player_2_pos_x_end, player_2_pos_y_end = char_pos_from_coord(player_2_coord_i, player_2_coord_j)
                        moving = True
                        moving_dir = 'down'
        else:
            moving_arr_index = 0
            moving_sequence_start = False


    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    # print(mouse_pos_x, mouse_pos_y)

    left_button_clicked, middle_button_clicked, right_button_clicked = pygame.mouse.get_pressed()
    if just_clicked == False:
        if middle_button_clicked == True:
            just_clicked = True
            start_mouse_pos_x, start_mouse_pos_y = pygame.mouse.get_pos()
            curr_mouse_pos_x, curr_mouse_pos_y = pygame.mouse.get_pos()
    elif just_clicked == True:
        if middle_button_clicked == False:
            just_clicked = False
            start_mouse_pos_x_old= camera_pos_x
            start_mouse_pos_y_old= camera_pos_y
    
    if just_clicked == True:
        curr_mouse_pos_x, curr_mouse_pos_y = pygame.mouse.get_pos()
        # print(start_mouse_pos_x, start_mouse_pos_y, ' --> ', curr_mouse_pos_x, curr_mouse_pos_y)
        delta_mouse_pos_x = curr_mouse_pos_x - start_mouse_pos_x
        delta_mouse_pos_y = curr_mouse_pos_y - start_mouse_pos_y
        print(delta_mouse_pos_x, delta_mouse_pos_y)
        camera_pos_x = start_mouse_pos_x_old + delta_mouse_pos_x
        camera_pos_y = start_mouse_pos_y_old + delta_mouse_pos_y

    screen.fill('silver')
    # screen.fill('black')
    
    # pygame.draw.circle(screen, 'blue', player_pos, 40)

    keys = pygame.key.get_pressed()
    '''
    if keys[pygame.K_UP]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_DOWN]:
        player_pos.y += 300 * dt
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt
    '''

    player_speed_x = 600 * dt
    player_speed_y = 300 * dt
    if event.type == pygame.KEYDOWN:
        if keys[pygame.K_LEFT]:
            if moving == False:
                if player_2_coord_i > 0:
                    player_2_coord_i -= 1
                    player_2_pos_x_end, player_2_pos_y_end = char_pos_from_coord(player_2_coord_i, player_2_coord_j)
                    moving = True
                    moving_dir = 'left'
        elif keys[pygame.K_RIGHT]:
            if moving == False:
                if player_2_coord_i < n_tiles_x-1:
                    player_2_coord_i += 1
                    player_2_pos_x_end, player_2_pos_y_end = char_pos_from_coord(player_2_coord_i, player_2_coord_j)
                    moving = True
                    moving_dir = 'right'
        elif keys[pygame.K_UP]:
            if moving == False:
                if player_2_coord_j > 0:
                    player_2_coord_j -= 1
                    player_2_pos_x_end, player_2_pos_y_end = char_pos_from_coord(player_2_coord_i, player_2_coord_j)
                    moving = True
                    moving_dir = 'up'
        elif keys[pygame.K_DOWN]:
            if moving == False:
                if player_2_coord_j < n_tiles_y-1:
                    player_2_coord_j += 1
                    player_2_pos_x_end, player_2_pos_y_end = char_pos_from_coord(player_2_coord_i, player_2_coord_j)
                    moving = True
                    moving_dir = 'down'


    if moving == True:
        if moving_dir == 'left':
            if player_2_pos_x > player_2_pos_x_end:
                player_2_pos_x -= player_speed_x
                if player_2_pos_x < player_2_pos_x_end:
                    player_2_pos_x = player_2_pos_x_end
            if player_2_pos_y > player_2_pos_y_end:
                player_2_pos_y -= player_speed_y
                if player_2_pos_y < player_2_pos_y_end:
                    player_2_pos_y = player_2_pos_y_end
            if player_2_pos_x <= player_2_pos_x_end and player_2_pos_y <= player_2_pos_y_end:
                moving = False
                moving_arr_index += 1
        elif moving_dir == 'right':
            if player_2_pos_x < player_2_pos_x_end:
                player_2_pos_x += player_speed_x
                if player_2_pos_x > player_2_pos_x_end:
                    player_2_pos_x = player_2_pos_x_end
            if player_2_pos_y < player_2_pos_y_end:
                player_2_pos_y += player_speed_y
                if player_2_pos_y > player_2_pos_y_end:
                    player_2_pos_y = player_2_pos_y_end
            if player_2_pos_x >= player_2_pos_x_end and player_2_pos_y >= player_2_pos_y_end:
                moving = False
                moving_arr_index += 1
        elif moving_dir == 'up':
            if player_2_pos_x < player_2_pos_x_end:
                player_2_pos_x += player_speed_x
                if player_2_pos_x > player_2_pos_x_end:
                    player_2_pos_x = player_2_pos_x_end
            if player_2_pos_y > player_2_pos_y_end:
                player_2_pos_y -= player_speed_y
                if player_2_pos_y < player_2_pos_y_end:
                    player_2_pos_y = player_2_pos_y_end
            if player_2_pos_x >= player_2_pos_x_end and player_2_pos_y <= player_2_pos_y_end:
                moving = False
                moving_arr_index += 1
        elif moving_dir == 'down':
            if player_2_pos_x > player_2_pos_x_end:
                player_2_pos_x -= player_speed_x
                if player_2_pos_x < player_2_pos_x_end:
                    player_2_pos_x = player_2_pos_x_end
            if player_2_pos_y < player_2_pos_y_end:
                player_2_pos_y += player_speed_y
                if player_2_pos_y > player_2_pos_y_end:
                    player_2_pos_y = player_2_pos_y_end
            if player_2_pos_x <= player_2_pos_x_end and player_2_pos_y >= player_2_pos_y_end:
                moving = False
                moving_arr_index += 1

    if event.type == pygame.KEYUP:
        if key_pressed_up == True:
            key_pressed_up = False
        elif key_pressed_down == True:
            key_pressed_down = False
        elif key_pressed_left == True:
            key_pressed_left = False
        elif key_pressed_right == True:
            key_pressed_right = False

    for i in range(n_tiles_x):
        for j in range(n_tiles_y):
            screen.blit(tiles_images[i], (
                tile_pos_from_coord(i, j)
            ))

    if char_orientation == 'down':
        screen.blit(player_image_64x64_scaled, (
            char_pos_from_coord(player_cell_x, player_cell_y)
        ))
    elif char_orientation == 'right':
        screen.blit(pygame.transform.flip(player_image_64x64_scaled, True, False), (
            (32*global_scale//2*player_cell_x - 32*global_scale//2*player_cell_y) + camera_pos_x, 
            (32*global_scale//4*player_cell_x + 32*global_scale//4*player_cell_y) + camera_pos_y - (32*global_scale) + (32*global_scale*0.4),
        ))
    # screen.blit(enemy_image_scaled, (0, 0))

    screen.blit(player_image_32x32_scaled, (
        32*global_scale//2 + camera_pos_x, 
        32*global_scale//4 + camera_pos_y,
    ))

    screen.blit(player_2_scaled, (
        player_2_pos_x,
        player_2_pos_y,
    ))

    pygame.display.flip()

    dt = clock.tick(60) / 1000
    

pygame.quit()
