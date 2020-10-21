import pygame
from car import Car
from walls import Walls
import tensorflow as tf

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 1000  # ширина игрового окна
HEIGHT = 800  # высота игрового окна
FPS = 30  # частота кадров в секунду

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("riders on the storm")
clock = pygame.time.Clock()

pygame.draw.line(screen, WHITE, [10, 30], [290, 15], 3)

pygame.display.update()

car_image = pygame.image.load('car.png')
car1 = Car(car_image, 200, 110, pygame, screen)
# Цикл игры

with tf.Session() as sess:
    a = tf.constant(1.0)
    print(sess.run(a))



running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False

    car1.activate_controls()
    # Обновление
    # all_sprites.update()
    screen.fill(GRAY)

    car1.car_surf = pygame.transform.scale(car1.car_surf, (50, 50))
    screen.blit(car1.car_surf, car1.car_rect)

    for wall in Walls:
        car1.radar(wall)
        pygame.draw.aaline(screen, BLUE, [wall['x1'], wall['y1']], [wall['x2'], wall['y2']], 4)

    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()
pygame.quit()
