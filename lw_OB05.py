import pygame
pygame.init()
import time


window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Тестовый проект")

image_1 = pygame.image.load("img/picPython_1.png")
image_rect_1 = image_1.get_rect()

image_2 = pygame.image.load("img/picPython_2.png")
image_rect_2 = image_2.get_rect()

# speed = 0.5

run = True


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = pygame.mouse.get_pos()
            image_rect_1.x = mouseX - 25
            image_rect_1.y = mouseY - 25

    if image_rect_1.colliderect(image_rect_2):
        print("Произошло столкновение")
        time.sleep(1)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT]:
    #     image_rect.x -= speed
    # if keys[pygame.K_RIGHT]:
    #     image_rect.x += speed
    # if keys[pygame.K_UP]:
    #     image_rect.y -= speed
    # if keys[pygame.K_DOWN]:
    #     image_rect.y += speed

    screen.fill((0, 0, 0))
    screen.blit(image_1, image_rect_1)
    screen.blit(image_2, image_rect_2)
    pygame.display.update()

pygame.quit()
