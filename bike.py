import pygame

pygame.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Bike Game")
clock = pygame.time.Clock()

x = 200
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= 5
    if keys[pygame.K_RIGHT]:
        x += 5

    x = max(30, min(370, x))

    screen.fill((245, 175, 100))

    pygame.draw.polygon(screen, (60, 60, 65), [
        (190, 150), (210, 150),
        (400, 600), (0, 600)
    ])

    pygame.draw.rect(
        screen, (255, 70, 30),
        (x - 15, 450, 30, 60)
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
