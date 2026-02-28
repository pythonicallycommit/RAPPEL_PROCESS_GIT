import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

block_size = 20 # Taille des blocs réduite
gravity = 0.5
jump_power = -7.5
player_velocity_y = 5
on_ground = False

grass_color = (80, 200, 120)
sky_color = (135, 206, 235)
player_color = (255, 100, 100)
target_color = (255, 255, 0)

terrain = [[1 if y == 12 else 0 for x in range(20)] for y in range(15)]

player_x = 5
player_y = 10
player_speed = 5 # Vitesse du joueur augmentée

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            target_y = int(player_y + 1)
            target_x = player_x
            if 0 <= target_y < len(terrain) and 0 <= target_x < len(terrain[0]):
                if event.button == 1:  # clic gauche = casser
                    terrain[target_y][target_x] = 0
                elif event.button == 3:  # clic droit = poser
                    terrain[target_y][target_x] = 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x = max(0, player_x - player_speed)
    if keys[pygame.K_RIGHT]:
        player_x = min(len(terrain[0]) - 1, player_x + player_speed)
    if keys[pygame.K_UP] and on_ground:
        player_velocity_y = jump_power
        on_ground = False

    player_velocity_y += gravity
    next_y = player_y + player_velocity_y * dt * 10

    if next_y >= 11 or terrain[int(next_y + 1)][player_x] == 1:
        next_y = 11
        player_velocity_y = 0
        on_ground = True

    player_y = next_y

    screen.fill(sky_color)

    # Affichage du terrain
    for y in range(len(terrain)):
        for x in range(len(terrain[y])):
            if terrain[y][x] == 1:
                pygame.draw.rect(screen, grass_color, (x * block_size, y * block_size, block_size, block_size))

    # Zone cible (pour pose/casse)
    pygame.draw.rect(screen, target_color, ((player_x) * block_size, int(player_y + 1) * block_size, block_size, block_size), 2)

    # Joueur
    pygame.draw.rect(screen, player_color, (player_x * block_size, int(player_y) * block_size, block_size, block_size))
    pygame.display.flip()

pygame.quit()