import pygame
import random
import sys

# Inisialisasi pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lomba Balap Sepeda")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Konstanta
FINISH_LINE = WIDTH - 50
PLAYER_SPEED = 5
COMPUTER_SPEED_MIN = 2
COMPUTER_SPEED_MAX = 4

# Memuat gambar sepeda
player_bike = pygame.image.load("sepeda.png")
cpu_bike = pygame.image.load("seped.png")

# Mengubah ukuran gambar
player_bike = pygame.transform.scale(player_bike, (50, 50))
cpu_bike = pygame.transform.scale(cpu_bike, (50, 50))

# Posisi awal pemain
players = [
    {"name": "Player", "sprite": player_bike, "x": 50, "y": 50},
    {"name": "CPU1", "sprite": cpu_bike, "x": 50, "y": 100},
    {"name": "CPU2", "sprite": cpu_bike, "x": 50, "y": 150},
    {"name": "CPU3", "sprite": cpu_bike, "x": 50, "y": 200},
    {"name": "CPU4", "sprite": cpu_bike, "x": 50, "y": 250},
]

# Font untuk teks
font = pygame.font.Font(None, 36)

def display_text(text, x, y, color=BLACK):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Game loop
running = True
clock = pygame.time.Clock()
winner = None

while running:
    screen.fill((200, 200, 200))  # Latar abu-abu

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Kontrol pemain
    if keys[pygame.K_SPACE] and players[0]["x"] < FINISH_LINE:
        players[0]["x"] += PLAYER_SPEED

    # Gerakan komputer
    for i in range(1, len(players)):
        if players[i]["x"] < FINISH_LINE:
            players[i]["x"] += random.randint(COMPUTER_SPEED_MIN, COMPUTER_SPEED_MAX)

    # Cek pemenang
    for player in players:
        if player["x"] >= FINISH_LINE and winner is None:
            winner = player["name"]

    # Gambar lintasan dan garis finish
    pygame.draw.line(screen, BLACK, (FINISH_LINE, 0), (FINISH_LINE, HEIGHT), 5)

    # Gambar pemain
    for player in players:
        screen.blit(player["sprite"], (player["x"], player["y"]))

    # Tampilkan pemenang
    if winner:
        display_text(f"{winner} Menang!", WIDTH // 2 - 100, HEIGHT // 2, BLACK)
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    # Update layar
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()