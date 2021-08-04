import os
from policy import *
from raycast import *
from level import *
from colors import *
from walls import *
from Seeker import *
from Hider import *
import pygame
import pickle
import pygame.freetype  # Import the freetype module.
import tkinter as tk

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# total game screen_coordinates = (640,480)
# [1536, 864] - Shrushti's Screen
size = [width, height]
print(size)
pygame.init()

screen = pygame.display.set_mode(size)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "0"
pygame.init()

GAME_FONT = pygame.freetype.Font("font.ttf", 16)
GAME_FONT_LARGE = pygame.freetype.Font("font.ttf", 24)

# Set up the display
pygame.display.set_caption("HIDE N SEEK")

clock = pygame.time.Clock()

parse_level(level)
esc = 0
episodes = 0
number_of_episodes = 4

while episodes < number_of_episodes and esc == 0:

    hider1 = Hider()  # Create the player
    hider2 = Hider()
    seeker1 = Seeker()

    hider_objs = [hider1, hider2]
    seeker_objs = [seeker1]
    running = True
    x = 0
    while running:

        clock.tick(60)
        # print(width, height)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
                esc = 1
            if e.type == pygame.KEYDOWN:
                # Move the player if an arrow key is pressed
                key = pygame.key.get_pressed()
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    if pov_switch.collidepoint(e.pos):
                        x = (x + 1) % len(agent_lines)
                elif e.button == 3:
                    if pov_switch.collidepoint(e.pos):
                        x = (x - 1) % len(agent_lines)
                        pass

        action_list_hider = []
        for h in hider_objs:
            hider_direction, hider_rotation = h.agent_hider.get_action()
            h.act(hider_direction, hider_rotation)
            action_list_hider.append([hider_direction, hider_rotation])

        action_list_seeker = []
        for s in seeker_objs:
            seeker_direction, seeker_rotation = s.agent_seeker.get_action()
            s.act(seeker_direction, seeker_rotation)
            action_list_seeker.append([seeker_direction, seeker_rotation])

        hider_cords = get_cords(hider_objs)
        seeker_cords = get_cords(seeker_objs)

        hider_temp = []
        for h in hider_objs:
            hider_temp = action_list_hider.pop(0)
            hider_direction = hider_temp[0]
            hider_reward = h.reward(seeker_objs, seeker_cords)
            h.agent_hider.update(hider_direction, hider_reward)

        seeker_temp = []
        for s in seeker_objs:
            seeker_temp = action_list_seeker.pop(0)
            seeker_direction = seeker_temp[0]
            seeker_reward, catch = seeker1.reward(hider_objs, hider_cords)
            if catch:
                hider_objs.remove(catch)
                del catch
            seeker1.agent_seeker.update(seeker_direction, seeker_reward)

        # Draw the scene
        screen.fill((0, 0, 0))
        floor = pygame.image.load('floor.jpg', "r")
        screen.blit(floor, (800, 400))
        floor = pygame.image.load('sky.jpg', "r")
        screen.blit(floor, (800, 0))

        for wall in walls:
            pygame.draw.rect(screen, white, wall.rect)

        for h in hider_objs:
            for line in h.vision:
                mx, my, px, py = line
                pygame.draw.aaline(screen, light_green, (mx, my), (px, py))

        for s in seeker_objs:
            for line in seeker1.vision:
                mx, my, px, py = line
                pygame.draw.aaline(screen, light_purple, (mx, my), (px, py))

        pov_switch = pygame.draw.rect(screen, (45, 43, 23), pygame.Rect(20, 780, 180, 100))
        eye = pygame.image.load('eye.png', "r")
        screen.blit(eye, (20, 780))
        #text_surface, rect = GAME_FONT.render("Left Click for next Agent", light_green)
        #screen.blit(text_surface, (150, 840))
        #text_surface, rect = GAME_FONT.render("Right Click for Previous Agent", light_green)
        #screen.blit(text_surface, (400, 840))
        text_surface, rect = GAME_FONT.render(f"Number of Episodes Completed  = {episodes}", grey)
        screen.blit(text_surface, (350, 818))
        #text_surface, rect = GAME_FONT_LARGE.render(f"Hiders are Green", forest_green)
        #screen.blit(text_surface, (700, 840))
        #text_surface, rect = GAME_FONT_LARGE.render(f"Seekers are Purple", purple)
        #screen.blit(text_surface, (1000, 840))

        temp = 0
        for h in hider_objs:
            text_surface, rect = GAME_FONT.render(f"Hider (Green) Rewards are {str(h.agent_hider.total_reward)[:6]}",
                                                  light_green)
            screen.blit(text_surface, (700, 815+ temp))
            temp += 20

        for s in seeker_objs:
            text_surface, rect = GAME_FONT.render(f"Seeker (Purple) Rewards are {str(s.agent_seeker.total_reward)[:6]}",cyan)
            screen.blit(text_surface, (1000, 818))

        for h in hider_objs:
            pygame.draw.rect(screen, forest_green, h.rect)
        for s in seeker_objs:
            pygame.draw.rect(screen, purple, s.rect)

        agent_lines = []
        for h in hider_objs:
            h_lines = Raycast(h).get_lines()
            agent_lines.append(h_lines)
        for s in seeker_objs:
            s_lines = Raycast(s).get_lines()
            agent_lines.append(s_lines)

        px = 0
        color = (3, 73, 252)
        for l in agent_lines[x]:
            if l['orientation'] == 'v':
                color = (168, 168, 168)
                pygame.draw.line(screen, color, (800 + px, 400 + l['length'] / 2),
                                 (800 + px, 400 - l['length'] + l['length'] / 2), width=3)
                px += 2
                pygame.draw.line(screen, (0, 0, 0), (800 + px, 400 + l['length'] / 2),
                                 (800 + px, 400 - l['length'] + l['length'] / 2), width=1)
                px += 2
            elif l['orientation'] == 'h':
                color = (107, 107, 107)
                pygame.draw.line(screen, color, (800 + px, 400 + l['length'] / 2),
                                 (800 + px, 400 - l['length'] + l['length'] / 2), width=3)
                px += 2
                pygame.draw.line(screen, (0, 0, 0), (800 + px, 400 + l['length'] / 2),
                                 (800 + px, 400 - l['length'] + l['length'] / 2), width=1)
                px += 2
            elif l['orientation'] == 'e':  # edge
                color = (0, 0, 0)
                pygame.draw.line(screen, color, (800 + px, 400 + l['length'] / 2),
                                 (800 + px, 400 - l['length'] + l['length'] / 2), width=3)
                px += 2
                pygame.draw.line(screen, (0, 0, 0), (800 + px, 400 + l['length'] / 2),
                                 (800 + px, 400 - l['length'] + l['length'] / 2), width=1)
                px += 2
            elif l['orientation'] == 'i':  # inf
                px += 4
                pass

        if seeker1.game_no == seeker1.game_prevno + 1:
            seeker1.game_prevno = seeker1.game_no

        if not hider_objs:
            episodes += 1
            running = False

        if episodes == number_of_episodes:
            for s in seeker_objs:
                pickle_s = open("seeker_qtable.pickle", "wb")
                pickle.dump(s.agent_seeker.q_table, pickle_s)
                pickle_s.close()

            for h in hider_objs:
                pickle_h = open("hider_qtable.pickle", "wb")
                pickle.dump(h.agent_hider.q_table, pickle_h)
                pickle_h.close()

            print("Pickle updated")

        pygame.display.flip()
