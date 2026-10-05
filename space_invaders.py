import pygame
import random
import math

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 60)

# =========================================================
# PLAYER
# =========================================================

player_width = 60
player_height = 25

player_x = WIDTH // 2 - player_width // 2
player_y = 620

player_speed = 6
lives = 3

# =========================================================
# PLAYER BULLET
# =========================================================

bullet_width = 6
bullet_height = 18

bullet_x = 0
bullet_y = 0

bullet_speed = 10
bullet_active = False

# =========================================================
# ALIEN BULLETS
# =========================================================

alien_bullets = []

alien_bullet_width = 5
alien_bullet_height = 16
alien_bullet_speed = 5

alien_shoot_timer = 0
ALIEN_SHOOT_DELAY = 65

# =========================================================
# ALIENS
# =========================================================

alien_width = 40
alien_height = 28

alien_rows = 5
alien_columns = 11

alien_spacing_x = 58
alien_spacing_y = 45

alien_start_x = 135
alien_start_y = 90

base_alien_speed = 1.0
alien_direction = 1

# =========================================================
# INVASION LINE
# =========================================================

INVASION_LINE = 600

# =========================================================
# BARRIERS
# =========================================================

barriers = []

barrier_y = 530

barrier_positions = [
    120,
    310,
    500,
    690
]

chunk_size = 10

# =========================================================
# GAME
# =========================================================

score = 0
game_state = "playing"

explosion_particles = []


# =========================================================
# CREATE ALIENS
# =========================================================

def create_aliens():

    new_aliens = []

    for row in range(alien_rows):

        for column in range(alien_columns):

            if row == 0:
                alien_type = 3
                points = 30

            elif row <= 2:
                alien_type = 2
                points = 20

            else:
                alien_type = 1
                points = 10

            alien = {
                "x": alien_start_x + column * alien_spacing_x,
                "y": alien_start_y + row * alien_spacing_y,
                "alive": True,
                "type": alien_type,
                "points": points
            }

            new_aliens.append(alien)

    return new_aliens


# =========================================================
# CREATE BARRIERS
# =========================================================

def create_barriers():

    new_barriers = []

    for barrier_x in barrier_positions:

        chunks = []

        for row in range(4):

            for column in range(8):

                # Make a bunker shape instead of full rectangle

                if row == 0 and (
                    column == 0
                    or
                    column == 7
                ):
                    continue

                if (
                    row >= 2
                    and
                    3 <= column <= 4
                ):
                    continue

                chunk = {
                    "x": barrier_x + column * chunk_size,
                    "y": barrier_y + row * chunk_size,
                    "alive": True
                }

                chunks.append(chunk)

        new_barriers.append(chunks)

    return new_barriers


aliens = create_aliens()
barriers = create_barriers()


# =========================================================
# RESET
# =========================================================

def reset_game():

    global player_x
    global bullet_active
    global alien_bullets
    global score
    global lives
    global game_state
    global aliens
    global barriers
    global alien_direction
    global explosion_particles
    global alien_shoot_timer

    player_x = WIDTH // 2 - player_width // 2

    bullet_active = False
    alien_bullets = []

    score = 0
    lives = 3

    game_state = "playing"

    aliens = create_aliens()
    barriers = create_barriers()

    alien_direction = 1

    explosion_particles = []

    alien_shoot_timer = 0


# =========================================================
# EXPLOSION
# =========================================================

def create_explosion(x, y):

    particles = []

    for i in range(20):

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 4)

        particle = {
            "x": x,
            "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": random.randint(15, 30),
            "size": random.randint(2, 5)
        }

        particles.append(particle)

    return particles


def update_explosions():

    global explosion_particles

    for particle in explosion_particles:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["life"] -= 1

        pygame.draw.circle(
            screen,
            (255, 120, 50),
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            particle["size"]
        )

    explosion_particles = [
        particle
        for particle in explosion_particles
        if particle["life"] > 0
    ]


# =========================================================
# DRAW ALIEN
# =========================================================

def draw_alien(alien):

    x = int(alien["x"])
    y = int(alien["y"])

    if alien["type"] == 3:

        color = (255, 100, 120)

        pygame.draw.rect(
            screen,
            color,
            (x + 10, y, 20, 8)
        )

        pygame.draw.rect(
            screen,
            color,
            (x + 5, y + 8, 30, 10)
        )

        pygame.draw.rect(
            screen,
            color,
            (x, y + 18, 40, 8)
        )

    elif alien["type"] == 2:

        color = (120, 220, 255)

        pygame.draw.rect(
            screen,
            color,
            (x + 5, y, 30, 8)
        )

        pygame.draw.rect(
            screen,
            color,
            (x, y + 8, 40, 12)
        )

        pygame.draw.rect(
            screen,
            color,
            (x + 10, y + 20, 8, 8)
        )

        pygame.draw.rect(
            screen,
            color,
            (x + 22, y + 20, 8, 8)
        )

    else:

        color = (120, 255, 120)

        pygame.draw.rect(
            screen,
            color,
            (x, y + 5, 40, 18)
        )

        pygame.draw.rect(
            screen,
            color,
            (x + 5, y, 8, 8)
        )

        pygame.draw.rect(
            screen,
            color,
            (x + 27, y, 8, 8)
        )


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if (
                    game_state == "playing"
                    and
                    not bullet_active
                ):

                    bullet_active = True

                    bullet_x = (
                        player_x
                        + player_width // 2
                        - bullet_width // 2
                    )

                    bullet_y = player_y

            if event.key == pygame.K_r:

                if game_state != "playing":
                    reset_game()

    # =====================================================
    # PLAYER MOVEMENT
    # =====================================================

    keys = pygame.key.get_pressed()

    if game_state == "playing":

        if keys[pygame.K_a]:
            player_x -= player_speed

        if keys[pygame.K_d]:
            player_x += player_speed

        if player_x < 0:
            player_x = 0

        if player_x > WIDTH - player_width:
            player_x = WIDTH - player_width

    # =====================================================
    # PLAYER BULLET
    # =====================================================

    if bullet_active:

        bullet_y -= bullet_speed

        if bullet_y < 0:
            bullet_active = False

    # =====================================================
    # ALIVE ALIENS
    # =====================================================

    alive_aliens = [
        alien
        for alien in aliens
        if alien["alive"]
    ]

    alive_count = len(alive_aliens)

    total_aliens = alien_rows * alien_columns

    # =====================================================
    # ALIEN SPEED
    # =====================================================

    speed_multiplier = (
        1
        +
        (total_aliens - alive_count)
        * 0.035
    )

    alien_speed = (
        base_alien_speed
        * speed_multiplier
    )

    # =====================================================
    # ALIEN MOVEMENT
    # =====================================================

    if game_state == "playing":

        hit_edge = False

        for alien in aliens:

            if alien["alive"]:

                alien["x"] += (
                    alien_speed
                    * alien_direction
                )

                if (
                    alien["x"] <= 0
                    or
                    alien["x"] + alien_width >= WIDTH
                ):
                    hit_edge = True

        if hit_edge:

            alien_direction *= -1

            for alien in aliens:

                if alien["alive"]:

                    alien["y"] += 22

                    alien["x"] += (
                        alien_speed
                        * alien_direction
                    )

    # =====================================================
    # ALIEN SHOOTING
    # =====================================================

    if (
        game_state == "playing"
        and
        alive_count > 0
    ):

        alien_shoot_timer += 1

        if alien_shoot_timer >= ALIEN_SHOOT_DELAY:

            alien_shoot_timer = 0

            shooter = random.choice(
                alive_aliens
            )

            alien_bullets.append(
                {
                    "x":
                        shooter["x"]
                        + alien_width / 2,

                    "y":
                        shooter["y"]
                        + alien_height
                }
            )

    # =====================================================
    # MOVE ALIEN BULLETS
    # =====================================================

    for alien_bullet in alien_bullets:

        alien_bullet["y"] += (
            alien_bullet_speed
        )

    alien_bullets = [
        bullet
        for bullet in alien_bullets
        if bullet["y"] < HEIGHT
    ]

    # =====================================================
    # PLAYER BULLET VS ALIENS
    # =====================================================

    if (
        bullet_active
        and
        game_state == "playing"
    ):

        bullet_rect = pygame.Rect(
            bullet_x,
            bullet_y,
            bullet_width,
            bullet_height
        )

        for alien in aliens:

            if alien["alive"]:

                alien_rect = pygame.Rect(
                    alien["x"],
                    alien["y"],
                    alien_width,
                    alien_height
                )

                if bullet_rect.colliderect(
                    alien_rect
                ):

                    alien["alive"] = False

                    bullet_active = False

                    score += alien["points"]

                    explosion_particles += create_explosion(
                        alien["x"]
                        + alien_width / 2,

                        alien["y"]
                        + alien_height / 2
                    )

                    break

    # =====================================================
    # PLAYER BULLET VS BARRIER CHUNKS
    # =====================================================

    if bullet_active:

        bullet_rect = pygame.Rect(
            bullet_x,
            bullet_y,
            bullet_width,
            bullet_height
        )

        for barrier in barriers:

            for chunk in barrier:

                if chunk["alive"]:

                    chunk_rect = pygame.Rect(
                        chunk["x"],
                        chunk["y"],
                        chunk_size,
                        chunk_size
                    )

                    if bullet_rect.colliderect(
                        chunk_rect
                    ):

                        chunk["alive"] = False
                        bullet_active = False

                        break

            if not bullet_active:
                break

    # =====================================================
    # ALIEN BULLETS VS BARRIER CHUNKS
    # =====================================================

    for alien_bullet in alien_bullets[:]:

        bullet_rect = pygame.Rect(
            alien_bullet["x"],
            alien_bullet["y"],
            alien_bullet_width,
            alien_bullet_height
        )

        hit_chunk = False

        for barrier in barriers:

            for chunk in barrier:

                if chunk["alive"]:

                    chunk_rect = pygame.Rect(
                        chunk["x"],
                        chunk["y"],
                        chunk_size,
                        chunk_size
                    )

                    if bullet_rect.colliderect(
                        chunk_rect
                    ):

                        chunk["alive"] = False
                        hit_chunk = True

                        break

            if hit_chunk:
                break

        if hit_chunk:

            alien_bullets.remove(
                alien_bullet
            )

    # =====================================================
    # ALIEN BULLETS VS PLAYER
    # =====================================================

    if game_state == "playing":

        player_rect = pygame.Rect(
            player_x,
            player_y,
            player_width,
            player_height
        )

        for alien_bullet in alien_bullets[:]:

            alien_bullet_rect = pygame.Rect(
                alien_bullet["x"],
                alien_bullet["y"],
                alien_bullet_width,
                alien_bullet_height
            )

            if alien_bullet_rect.colliderect(
                player_rect
            ):

                alien_bullets.remove(
                    alien_bullet
                )

                lives -= 1

                explosion_particles += create_explosion(
                    player_x
                    + player_width / 2,
                    player_y
                )

                if lives <= 0:

                    game_state = "game_over"

                    bullet_active = False

                break

    # =====================================================
    # CHECK WIN
    # =====================================================

    alive_count = sum(
        1
        for alien in aliens
        if alien["alive"]
    )

    if (
        alive_count == 0
        and
        game_state == "playing"
    ):

        game_state = "won"

        bullet_active = False

    # =====================================================
    # CHECK INVASION LINE
    # =====================================================

    if game_state == "playing":

        for alien in aliens:

            if alien["alive"]:

                alien_bottom = (
                    alien["y"]
                    + alien_height
                )

                if alien_bottom >= INVASION_LINE:

                    game_state = "game_over"

                    bullet_active = False

                    break

    # =====================================================
    # DRAW BACKGROUND
    # =====================================================

    screen.fill(
        (10, 10, 25)
    )

    # =====================================================
    # INVASION LINE
    # =====================================================

    pygame.draw.line(
        screen,
        (80, 80, 100),
        (0, INVASION_LINE),
        (WIDTH, INVASION_LINE),
        1
    )

    # =====================================================
    # PLAYER
    # =====================================================

    if lives > 0:

        pygame.draw.rect(
            screen,
            (100, 220, 120),
            (
                player_x,
                player_y,
                player_width,
                player_height
            )
        )

        pygame.draw.rect(
            screen,
            (100, 220, 120),
            (
                player_x + 25,
                player_y - 12,
                10,
                12
            )
        )

    # =====================================================
    # PLAYER BULLET
    # =====================================================

    if bullet_active:

        pygame.draw.rect(
            screen,
            (255, 240, 120),
            (
                bullet_x,
                bullet_y,
                bullet_width,
                bullet_height
            )
        )

    # =====================================================
    # ALIEN BULLETS
    # =====================================================

    for alien_bullet in alien_bullets:

        pygame.draw.rect(
            screen,
            (255, 100, 100),
            (
                alien_bullet["x"],
                alien_bullet["y"],
                alien_bullet_width,
                alien_bullet_height
            )
        )

    # =====================================================
    # ALIENS
    # =====================================================

    for alien in aliens:

        if alien["alive"]:
            draw_alien(alien)

    # =====================================================
    # BARRIERS
    # =====================================================

    for barrier in barriers:

        for chunk in barrier:

            if chunk["alive"]:

                pygame.draw.rect(
                    screen,
                    (100, 220, 120),
                    (
                        chunk["x"],
                        chunk["y"],
                        chunk_size,
                        chunk_size
                    )
                )

    # =====================================================
    # EXPLOSIONS
    # =====================================================

    update_explosions()

    # =====================================================
    # SCORE + LIVES
    # =====================================================

    score_text = font.render(
        f"Score: {score}",
        True,
        (240, 240, 240)
    )

    lives_text = font.render(
        f"Lives: {lives}",
        True,
        (240, 240, 240)
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    screen.blit(
        lives_text,
        (20, 55)
    )

    # =====================================================
    # WIN
    # =====================================================

    if game_state == "won":

        win_text = big_font.render(
            "YOU WIN!",
            True,
            (120, 255, 140)
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            (230, 230, 230)
        )

        screen.blit(
            win_text,
            win_text.get_rect(
                center=(WIDTH / 2, 330)
            )
        )

        screen.blit(
            restart_text,
            restart_text.get_rect(
                center=(WIDTH / 2, 380)
            )
        )

    # =====================================================
    # GAME OVER
    # =====================================================

    if game_state == "game_over":

        game_over_text = big_font.render(
            "GAME OVER",
            True,
            (255, 80, 80)
        )

        restart_text = font.render(
            "Press R to try again",
            True,
            (230, 230, 230)
        )

        screen.blit(
            game_over_text,
            game_over_text.get_rect(
                center=(WIDTH / 2, 330)
            )
        )

        screen.blit(
            restart_text,
            restart_text.get_rect(
                center=(WIDTH / 2, 380)
            )
        )

    # =====================================================
    # CONTROLS
    # =====================================================

    controls_text = font.render(
        "A/D: move    SPACE: shoot",
        True,
        (150, 150, 170)
    )

    screen.blit(
        controls_text,
        (
            WIDTH
            - controls_text.get_width()
            - 20,
            20
        )
    )

    # =====================================================
    # SHOW FRAME
    # =====================================================

    pygame.display.flip()

    clock.tick(60)

pygame.quit()