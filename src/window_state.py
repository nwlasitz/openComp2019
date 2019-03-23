from state import State
from primitives import rect
from collections import deque
import pygame
import time

class WindowState:
    def __init__(self, state_str, state):
        self.state_str = state_str
        self.state = state

    def __str__(self):
        return self.state_str

    def __cmp__(self, other):
        return cmp(self.state_str, other.state_str)

    def __hash__(self):
        return hash(self.state_str)


class MainMenuState (State):
    def __init__(self, window):
        self.window = window

        green = (0,255,0)
        width = self.window.get_width()
        height = self.window.get_height()
        self.play_button = rect(width/2,height*2/5,30,15,window.__surface__,'green')

    def run(self):
        self.draw_buttons()
        self.window.update()

    def next(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if self.play_button.intersect(pos):
                    #print("State: {}".format(WindowState.game))
                    self.draw_bg()
                    return WindowState.game

                #elif self.settings_button.clicked(pos):
                #    return WindowState.settings
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.draw_bg()
                return WindowState.game

        return WindowState.main_menu

    def draw_buttons(self):
        width = self.window.get_width()
        height = self.window.get_height()
        self.play_button.draw()
        self.window.set_font_size(40)
        self.window.draw_string('Play', width/2, height*2/5)
        self.window.draw_string('Settings', width/2-12, height*2/5+20)

    def draw_bg(self):
        color = (35,99,47,100)
        self.window.__surface__.fill(color)

class SettingsState (State):
    pass

class GameState (State):
    def __init__(self, window):
        self.window = window
        self.frame = 0;
        self.fire_rate = 100
        self.queue = deque([100,200,400, 500, 650])
        self.bullet_count = 1000
        self.enemies = []
        self.projectiles = []

        height = self.window.get_height()
        red = (255,0,255)
        self.player = rect(50,height*4/5,50,200,window.__surface__, 'yellow')

    def run(self):
        self.window.clear()
        self.draw_bg()
        self.print_bullet_count()
        self.draw()
        #self.generate_enemy()
        self.update_enemies()
        self.update_projectiles()
        self.check_collision()
        self.fire_bullet()
        self.frame += 1
        time.sleep(0.0001) # set game velocity by pausing

    def draw_bg(self):
        color = (35,99,47,100)
        self.window.__surface__.fill(color)

    def print_bullet_count(self):
        self.window.draw_string('Bullets: ' + str(self.bullet_count), 0, 0)


    def fire_bullet(self):
        if self.fire_rate <= self.frame:
            self.spawn_bullet()
            self.frame = 0
        else:
            self.frame += 1

    def next(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.fire_rate > 10:
                        self.fire_rate -= 10
                if event.key == pygame.K_l:
                    if self.fire_rate < 100:
                        self.fire_rate += 10

        return WindowState.game
    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
        for projectile in self.projectiles:
            projectile.draw()

        self.player.draw()


    def generate_enemy(self):
        while(self.queue[0] < self.frame):
            self.queue.popleft()
            self.spawn_enemy()


    def spawn_enemy(self):
        height = self.window.get_height()
        width = self.window.get_width()
        enemy = rect(width-50,height*4/5,50,200,self.window.__surface__, 'red')
        self.enemies.append(enemy)

    def spawn_bullet(self):
        height = self.window.get_height()
        bullet = rect(100,height*4/5+25,30,5,self.window.__surface__, 'pink')
        self.projectiles.append(bullet)
        self.bullet_count -= 1

    def update_enemies(self):
        for enemy in self.enemies:
            pygame.Rect.move_ip(enemy.rectangle, -1, 0)

    def update_projectiles(self):
        height = self.window.get_height()

        for projectile in self.projectiles:
            pygame.Rect.move_ip(projectile.rectangle, 10, 0)

            if(pygame.Rect.collidepoint(projectile.rectangle, 1280, height*4/5+26)):
                self.projectiles.pop(0)

    def check_collision(self):
        try:
            if( pygame.Rect.colliderect(self.enemies[0].rectangle, self.projectiles[0].rectangle) ):
                self.projectiles.pop(0)
                self.enemies.pop(0)

        except Exception as e:
                #print("BROKE {}".format(e))
                pass
