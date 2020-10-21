import pygame, math
class Vector:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Car:
    speed = 10
    alpha = 0
    angle = 9
    height = 50
    width = 50
    vector_iterator = speed / 10

    def __init__(self, image, start_x , start_y, pygame, screen):
        self.pygame = pygame
        self.screen = screen
        self.car = self.pygame.transform.scale(image, (self.width, self.height))
        self.car_surf = self.car
        self.car_rect = self.car.get_rect(center=(start_x, start_y))
        self.start_x = start_x
        self.start_y = start_y
        self.screen.blit(self.car, self.car_rect)
        self.vector = Vector(self.speed, 0)

    def reset(self):
        self.alpha = 0
        self.vector.x = self.speed
        self.vector.y = 0
        self.car_surf = self.pygame.transform.rotate(self.car, 0)
        self.car_rect.x = self.start_x - self.width/2
        self.car_rect.y = self.start_y - self.height/2

    def move_forward(self):
        self.car_rect.x += self.vector.x
        self.car_rect.y += self.vector.y

    def move_back(self):
        self.car_rect.x -= self.vector.x
        self.car_rect.y -= self.vector.y

    def change_vector(self, delta_x, delta_y):
        self.vector.x += delta_x
        self.vector.y += delta_y

    def turn_left(self):
        if self.vector.x >= 0:
            self.alpha += self.angle
            self.car_surf = self.pygame.transform.rotate(self.car, self.alpha)
            if self.vector.y > 0:
                self.change_vector(self.vector_iterator, -self.vector_iterator)
            elif self.vector.y > -self.speed:
                self.change_vector(-self.vector_iterator, -self.vector_iterator)
        if self.vector.x <= 0:
            self.alpha += self.angle
            self.car_surf = self.pygame.transform.rotate(self.car, self.alpha)
            if self.vector.y >= 0:
                self.change_vector(self.vector_iterator, self.vector_iterator)
            elif self.vector.y < 0:
                self.change_vector(-self.vector_iterator, self.vector_iterator)

    def turn_right(self):
        if self.vector.x >= 0:
            self.alpha -= self.angle
            self.car_surf = self.pygame.transform.rotate(self.car, self.alpha)
            if self.vector.y < 0:
                 self.change_vector(self.vector_iterator, self.vector_iterator)
            elif self.vector.y < self.speed:
                 self.change_vector(-self.vector_iterator, self.vector_iterator)
        if self.vector.x <= 0:
            self.alpha -= self.angle
            self.car_surf = self.pygame.transform.rotate(self.car, self.alpha)
            if self.vector.y > 0:
                self.change_vector(-self.vector_iterator, -self.vector_iterator)
            elif self.vector.y > -self.speed:
                self.change_vector(self.vector_iterator, -self.vector_iterator)


    def activate_controls(self):
        keys = self.pygame.key.get_pressed()
        if keys[self.pygame.K_UP]:
            self.move_forward()
        elif keys[self.pygame.K_DOWN]:
            self.move_back()
        if keys[self.pygame.K_RIGHT]:
            self.turn_right()
        elif keys[self.pygame.K_LEFT]:
            self.turn_left()

    def radar(self, wall):
        coords = dict()
        coords['start_x_cord'] = self.car_rect.x + (self.width/2)
        coords['start_y_cord'] = self.car_rect.y + (self.height/2)
        coords['end_x_cord'] = coords['start_x_cord'] + self.vector.x * 100
        coords['end_y_cord'] = coords['start_y_cord'] + self.vector.y * 100
        self.pygame.draw.aaline(self.screen, RED, [coords['start_x_cord'], coords['start_y_cord']], [coords['end_x_cord'], coords['end_y_cord']], 3)
        a1 = wall['y2'] - wall['y1']
        b1 = wall['x1'] - wall['x2']
        c1 = -wall['x1'] * wall['y2'] + wall['y1'] * wall['x2']
        a2 = coords['end_y_cord'] - coords['start_y_cord']
        b2 = coords['start_x_cord'] - coords['end_x_cord']
        c2 = -coords['start_x_cord'] * coords['end_y_cord'] + coords['start_y_cord'] * coords['end_x_cord']
        seg1_line2_start = a2 * wall['x1'] + b2 * wall['y1'] + c2
        seg1_line2_end = a2 * wall['x2'] + b2 * wall['y2'] + c2
        seg2_line1_start = a1 * coords['start_x_cord'] + b1 * coords['start_y_cord'] + c1
        seg2_line1_end = a1 * coords['end_x_cord'] + b1 * coords['end_y_cord'] + c1
        if seg1_line2_start * seg1_line2_end >= 0 or seg2_line1_start * seg2_line1_end >= 0:
            return False
        X = round((b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1))
        Y = round((a2 * c1 - a1 * c2) / (a1 * b2 - a2 * b1))
        self.pygame.draw.circle(self.screen, BLACK, (X, Y), 5)
        range = round(math.sqrt((X - (self.car_rect.x + self.width/2))**2 + (Y - (self.car_rect.y + self.height/2))**2))
        if range - self.width/2 < 10:
            self.reset()
        return range
