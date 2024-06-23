import pygame
import sys
import math
import time

start_time = time.time()

pygame.init()

screen_width = 640
screen_height = 440

grid_width = 32
grid_height = 22

cell_size = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid with Robot")

def draw_robot(robot_x, robot_y):
    for y in range(5):
        for x in range(5):
            if (y == 2) or (x == 2):
                pass
            else:
                pygame.draw.rect(screen, RED, ((robot_x + x) * cell_size, (robot_y + y) * cell_size, cell_size, cell_size))

def draw_custom_numbers(numbers):
    for (x, y), number in numbers.items():
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(number), True, BLACK)
        text_rect = text.get_rect(center=(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2))
        screen.blit(text, text_rect)


def decrease_custom_number(numbers, x, y):
    for dx in range(2):
        for dy in range(2):
            if (x + dx, y + dy) in numbers:
                numbers[(x + dx, y + dy)] -= 1
                if numbers[(x + dx, y + dy)] == 0:
                    del numbers[(x + dx, y + dy)]
    
    for dx in range(3,5):
        for dy in range(2):
            if (x + dx, y + dy) in numbers:
                numbers[(x + dx, y + dy)] -= 1
                if numbers[(x + dx, y + dy)] == 0:
                    del numbers[(x + dx, y + dy)]
    
    for dx in range(2):
        for dy in range(3, 5):
            if (x + dx, y + dy) in numbers:
                numbers[(x + dx, y + dy)] -= 1
                if numbers[(x + dx, y + dy)] == 0:
                    del numbers[(x + dx, y + dy)]
    
    for dx in range(3,5):
        for dy in range(3,5):
            if (x + dx, y + dy) in numbers:
                numbers[(x + dx, y + dy)] -= 1
                if numbers[(x + dx, y + dy)] == 0:
                    del numbers[(x + dx, y + dy)]

    return None

robot_x = 0
robot_y = grid_height - 5
step = 0 

custom_numbers = {
    (2, 3): 1, (2, 4): 1, (2, 5): 1, (3, 3): 1, (3, 4): 1, (3, 5): 1, (4, 3): 1, (4, 4): 1, (4, 5): 1,
    (6, 4): 1, (6, 5): 1, (6, 6): 1, (7, 4): 1, (7, 5): 1, (7, 6): 1, (8, 4): 1, (8, 5): 1, (8, 6): 1,
    (18, 3): 1, (18, 4): 1, (18, 5): 1, (19, 3): 1, (19, 4): 1, (19, 5): 1, (20, 3): 1, (20, 4): 1, (20, 5): 1,
    (23, 1): 1, (23, 2): 1, (23, 3): 1, (24, 1): 1, (24, 2): 1, (24, 3): 1, (25, 1): 1, (25, 2): 1, (25, 3): 1,
    (10, 10): 2, (10, 11): 2, (10, 12): 2, (11, 10): 2, (11, 11): 2, (11, 12): 2, (12, 10): 2, (12, 11): 2, (12, 12): 2,
    (24, 14): 1, (24, 15): 1, (24, 16): 1, (25, 14): 1, (25, 15): 1, (25, 16): 1, (26, 14): 1, (26, 15): 1, (26, 16): 1,

    (2, 9): 1, (2, 10): 1, (3, 9): 1, (3, 10): 1,
    (2, 15): 1, (2, 16): 1, (3, 15): 1, (3, 16): 1,
    (7, 10): 2, (7, 11): 2, (8, 10): 2, (8, 11): 2,
    (6, 16): 1, (6, 17): 1, (7, 16): 1, (7, 17): 1,
    (15, 10): 1, (15, 11): 1, (16, 10): 1, (16, 11): 1,    
    (15, 16): 3, (15, 17): 3, (16, 16): 3, (16, 17): 3,
    (18, 9): 1,  (18, 10): 1, (19, 9): 1,  (19, 10): 1,
    (18, 15): 1, (18, 16): 1, (19, 15): 1, (19, 16): 1,

    (6, 4): 3, (9, 13): 2, (12, 19): 2, (8, 20): 3, (13, 16): 2, (4, 8): 1, (4, 2): 2, (18, 7): 3, (7, 19): 2, (19, 12): 2, (21, 6): 1, (31, 5): 2, (10, 14): 2,
    (25, 12): 3, (21, 4): 2, (18, 20): 2, (13, 2): 3, (15, 1): 2, (1, 5): 1, (17, 13): 2, (23, 4): 2, (29, 5): 1, (5, 14): 1, (19, 9): 1, (8, 12): 1, (30, 18): 1,
    (19, 11): 3, (29, 12): 3, (14, 13): 1, (10, 5): 2, (27, 9): 2, (18, 17): 3, (3, 8): 3, (20, 20): 3, (13, 19): 3
}


def closest_point(custom_numbers, robot_x, robot_y):
    min_distance = float('inf')
    closest_point = None
    
    for point, value in custom_numbers.items():
        distance = math.sqrt((robot_x - point[0])**2 + (robot_y - point[1])**2)
        if distance < min_distance:
            min_distance = distance
            closest_point = point
    
    return closest_point
          
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    while custom_numbers:
        closest = closest_point(custom_numbers, robot_x, robot_y)
        if closest:
            closest_x, closest_y = closest
            while True:
                if robot_x != closest_x:
                    if robot_x < closest_x:
                        robot_x += 1
                        step += 1
                    else:
                        robot_x -= 1
                        step += 1
                if robot_y != closest_y:
                    if robot_y < closest_y:
                        robot_y += 1
                        step += 1
                    else:
                        robot_y -= 1
                        step += 1
                decrease_custom_number(custom_numbers, robot_x, robot_y)
                if (robot_x, robot_y) == closest:
                    break 
        else:
            break

    if not custom_numbers:
        while robot_x != 31 or robot_y != 0:
            if robot_x != 31:
                if robot_x < 31:
                    robot_x += 1
                    step += 1
                else:
                    robot_x -= 1
                    step += 1
            if robot_y != 0:
                if robot_y < 0:
                    robot_y += 1
                    step += 1
                else:
                    robot_y -= 1
                    step += 1

    screen.fill(WHITE)

    for y in range(grid_height):
        for x in range(grid_width):
            pygame.draw.rect(screen, BLACK, (x * cell_size, y * cell_size, cell_size, cell_size), 1)

    draw_custom_numbers(custom_numbers)

    draw_robot(robot_x, robot_y)

    pygame.display.flip()
pygame.quit()

end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time, "seconds")
print("Steps:", step)
print("Final Position of Robot:", robot_x, ",", robot_y)
sys.exit()