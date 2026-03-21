import pygame

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer with Boba Collectibles")

# ---------------- CONSTANTS ----------------
PLAYER_W, PLAYER_H = 120, 120
GRAVITY = 0.8
JUMP = -12
SPEED = 4

# ---------------- CAMERA ----------------
camera_x = 0

# ---------------- ASSETS ----------------
background_img = pygame.transform.scale(
    pygame.image.load("bg.png"), (2000, HEIGHT)
)

player_img_right = pygame.transform.scale(
    pygame.image.load("player_right.png"), (PLAYER_W, PLAYER_H)
)
player_img_left = pygame.transform.scale(
    pygame.image.load("player_left.png"), (PLAYER_W, PLAYER_H)
)
player_img = player_img_right

# Boba ball image
boba_img = pygame.image.load("boba.png")
boba_img = pygame.transform.scale(boba_img, (40, 40))

# ---------------- GAME STATE ----------------
game_state = "playing"  # "playing" or "game_over"

# ---------------- PLAYER ----------------
PLAYER_START_X, PLAYER_START_Y = 50, 50
player_x, player_y = PLAYER_START_X, PLAYER_START_Y
player_vel_y = 0
jumps_left = 2

# ---------------- PLATFORMS ----------------
platforms = [
    (300, 450, 200, 12),
    (500, 300, 200, 12),
    (700, 150, 200, 12),
    (900, 350, 200, 12),
    (1100, 250, 200, 12),
    (1300, 400, 200, 12),
    (1500, 300, 200, 12)
]

# ---------------- COLLECTIBLES ----------------
INITIAL_BOBA = [
    pygame.Rect(350, 400, 40, 40),
    pygame.Rect(550, 260, 40, 40),
    pygame.Rect(720, 100, 40, 40),
    pygame.Rect(950, 300, 40, 40)
]

boba_balls = INITIAL_BOBA.copy()

score = 0
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 60)
button_font = pygame.font.SysFont("Arial", 40)


def reset_game():
    """Reset all game variables to initial state"""
    global player_x, player_y, player_vel_y, jumps_left, camera_x, score, boba_balls, game_state, player_img
    player_x, player_y = PLAYER_START_X, PLAYER_START_Y
    player_vel_y = 0
    jumps_left = 2
    camera_x = 0
    score = 0
    boba_balls = [pygame.Rect(b.x, b.y, b.width, b.height) for b in INITIAL_BOBA]
    game_state = "playing"
    player_img = player_img_right


def draw_platforms():
    for x, y, w, h in platforms:
        pygame.draw.rect(win, (194, 178, 128), (x - camera_x, y, w, h))


def draw_player():
    win.blit(player_img, (player_x - camera_x, player_y))


def draw_boba_balls():
    for boba in boba_balls:
        win.blit(boba_img, (boba.x - camera_x, boba.y))


def draw_score():
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(text, (10, 10))


def draw_game_over():
    """Draw the game over screen with Try Again button"""
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    win.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = big_font.render("Game Over!", True, (255, 100, 100))
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    win.blit(game_over_text, text_rect)
    
    # Final score
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    win.blit(score_text, score_rect)
    
    # Try Again button
    button_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 50, 240, 60)
    pygame.draw.rect(win, (100, 200, 100), button_rect, border_radius=10)
    pygame.draw.rect(win, (255, 255, 255), button_rect, width=3, border_radius=10)
    
    button_text = button_font.render("Try Again", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    win.blit(button_text, button_text_rect)
    
    return button_rect


running = True
while running:
    clock.tick(60)
    
    if game_state == "playing":
        win.blit(background_img, (-camera_x, 0))

        prev_y = player_y
        prev_bottom = prev_y + PLAYER_H

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and jumps_left > 0:
                    player_vel_y = JUMP
                    jumps_left -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= SPEED
            player_img = player_img_left
        if keys[pygame.K_RIGHT]:
            player_x += SPEED
            player_img = player_img_right

        camera_x = max(0, min(player_x - 200, background_img.get_width()-WIDTH))

        player_vel_y += GRAVITY
        player_y += player_vel_y

        foot_x = player_x + PLAYER_W // 2
        for px, py, pw, ph in platforms:
            if px <= foot_x <= px + pw:
                if prev_bottom <= py and player_y + PLAYER_H >= py and player_vel_y > 0:
                    player_y = py - PLAYER_H
                    player_vel_y = 0
                    jumps_left = 2

        # Check if player fell off the screen (game over condition)
        if player_y >= HEIGHT + 100:
            game_state = "game_over"
        
        # Ground collision
        if player_y >= HEIGHT - PLAYER_H:
            player_y = HEIGHT - PLAYER_H
            player_vel_y = 0
            jumps_left = 2

        # Collect boba balls
        player_rect = pygame.Rect(player_x, player_y, PLAYER_W, PLAYER_H)
        for boba in boba_balls[:]:
            if player_rect.colliderect(boba):
                boba_balls.remove(boba)
                score += 1

        # Check if all boba collected (win condition)
        if len(boba_balls) == 0:
            game_state = "game_over"

        draw_platforms()
        draw_player()
        draw_boba_balls()
        draw_score()
        
    elif game_state == "game_over":
        # Keep showing the last game frame in background
        win.blit(background_img, (-camera_x, 0))
        draw_platforms()
        draw_player()
        draw_boba_balls()
        draw_score()
        
        # Draw game over screen on top
        button_rect = draw_game_over()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    reset_game()

    pygame.display.update()

pygame.quit()