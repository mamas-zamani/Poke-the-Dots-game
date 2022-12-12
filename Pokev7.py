# Poke The Dots Version 7
# This is a graphical game where two dots move around
# the screen, bouncing off the edges. The user tries 
# to prevent the dots from colliding by pressing and 
# releasing the mouse button to teleport the dots to 
# a random location. The score is the number of seconds 
# from the start of the game until the dots collide.

from uagame import Window
from random import randint
from math import sqrt
import pygame
from pygame import QUIT, Color, MOUSEBUTTONUP
from pygame.time import Clock, get_ticks
from pygame.event import get as get_events
# from pygame.draw import circle as draw_circle

cat = pygame.image.load('cato.png')
cat = pygame.transform.scale(cat, (62,62))
dog = pygame.image.load('dogo.png')
dog = pygame.transform.scale(dog, (82,82))

# User-defined functions

def main():
    game = Game()
    game.play()
    
# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self):
        # Initialize a Game.
        # - self is the Game to initialize
        
        self._window = Window('Poke the Dots', 800, 600)
        self._adjust_window()
        self._frame_rate = 90  # larger is faster game
        self._close_selected = False
        self._clock = Clock()
        self._smaller_dot = Dot('red', [0,0], 40, [1,2], self._window)
        self._bigger_dot = Dot('red', [0,0], 50, [2,1], self._window)
        self._smaller_dot.randomize()
        self._bigger_dot.randomize()
        while self._smaller_dot.intersects(self._bigger_dot):
            self._bigger_dot.randomize()
        self._small_dot = Dot('red', [self._smaller_dot._center[0],self._smaller_dot._center[1]], 30, [1,2], self._window)
        self._big_dot = Dot('blue', [self._bigger_dot._center[0],self._bigger_dot._center[1]], 40, [2,1], self._window)
        self._score = 0
        self._stored_time = get_ticks()
        self._continue_game = True
        
    def _adjust_window(self):
        # Adjust the window for the game.
        # - self is the Game to adjust the window for
        
        self._window.set_font_name('ariel')
        self._window.set_font_size(64)
        self._window.set_font_color('white')
        self._window.set_bg_color('black')        
    
    def play(self):
        # Play the game until the player presses the close icon
        # and then close the window.
        # - self is the Game to play

        while not self._close_selected:
            # play frame
            self.handle_events()
            self.draw()
            self.update()
        self._window.close()
           
    def handle_events(self):
        # Handle the current game events by changing the game
        # state appropriately.
        # - self is the Game whose events will be handled

        event_list = get_events()
        for event in event_list:
            self.handle_one_event(event)
            
    def handle_one_event(self, event):
        # Handle one event by changing the game state
        # appropriately.
        # - self is the Game whose event will be handled
        # - event is the Event object to handle
            
        if event.type == QUIT:
            self._close_selected = True
        elif self._continue_game and event.type == MOUSEBUTTONUP:
            self.handle_mouse_up(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self._continue_game == False:
                self._close_selected = True
                self._stored_time = get_ticks()
                # print(self._stored_time)
                self.__init__()


    def handle_mouse_up(self, event):
        # Respond to the player releasing the mouse button by
        # taking appropriate actions.
        # - self is the Game where the mouse up occurred
        # - event is the Event object to handle

        # self._small_dot.randomize()
        # self._big_dot.randomize()
        # while self._small_dot.intersects(self._big_dot):
        #       self._big_dot.randomize()
              
        self._smaller_dot.randomize()
        self._bigger_dot.randomize()
        while self._smaller_dot.intersects(self._bigger_dot):
            self._bigger_dot.randomize()
        v = [0,0]
        v[0] = self._small_dot._velocity[0] 
        v[1] = self._small_dot._velocity[1] 
        
        self._small_dot = Dot('red', [self._smaller_dot._center[0],self._smaller_dot._center[1]], 30,[v[0],v[1]], self._window)
        self._big_dot = Dot('blue', [self._bigger_dot._center[0],self._bigger_dot._center[1]], 40, [v[1],v[0]], self._window)

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        
        self._window.clear()
        self.draw_score()
        self._small_dot.draw('cat')
        self._big_dot.draw('dog')
        if not self._continue_game:  # perform game over actions
            self.draw_game_over()
        self._window.update()
                        
    def update(self):
        # Update all game objects with state changes
        # that are not due to user events. Determine if
        # the game should continue.
        # - self is the Game to update

        if self._continue_game:
            # update during game
            self._small_dot.move()
            self._big_dot.move()
            self._ticks = 0
            self._ticks = self._ticks + get_ticks() - self._stored_time
            self._previous_score = self._score
            self._score = self._ticks // 1000 
            # print(self._score-self._previous_score)
            # print(self._score, self._previous_score)
        if  self._score % 5 == 0 and self._ticks != 0 and self._previous_score != self._score:
            self._big_dot.increase_speed()
            self._small_dot.increase_speed()

        self._clock.tick(self._frame_rate)
        
        # decide continue
        if self._small_dot.intersects(self._big_dot):
            self._continue_game = False

    def draw_game_over(self):
        # Draw GAME OVER in the lower left corner of the
        # surface, using the small dot's color for the font
        # and the big dot's color as the background.
        # - self is the Game to draw for
        
        self.draw_score()
        string = 'GAME OVER'
        rstart = 'Hit R to restart the game'

        font_color = self._small_dot.get_color()
        bg_color = self._big_dot.get_color()
        original_font_color = self._window.get_font_color()
        original_bg_color = self._window.get_bg_color()
        self._window.set_font_color(font_color)
        self._window.set_bg_color(bg_color)

        height = self._window.get_height() - self._window.get_font_height()
        self._window.draw_string(string, 0, height)

        self._window.set_font_color('Green')
        self._window.set_bg_color(original_bg_color)

        weidth = self._window.get_width()-self._window.get_string_width(rstart)
        self._window.draw_string(rstart, weidth/2, (height+ self._window.get_font_height()) // 2)
        self._window.set_font_color(original_font_color)

    def draw_score(self):
        # Draw the time since the game began as a score.
        # - self is the Game to draw for.
        
        string = 'Score: ' + str(self._score)
        self._window.draw_string(string, 0, 0)

class Dot:
    # An object in this class represents a colored circle
    # that can move.

    def __init__(self, color, center, radius, velocity, window):
        # Initialize a Dot.
        # - self is the Dot to initialize
        # - color is the str color of the dot
        # - center is a list containing the x and y int
        # coords of the center of the dot
        # - radius is the int pixel radius of the dot
        # - velocity is a list containing the x and y components
        # - window is the game's Window

        self._color = color
        self._center = center
        self._radius = radius
        self._velocity = velocity
        self._window = window
        self._clock = Clock()
        self._frame_rate = 90

    def increase_speed(self):
        # Increase speed per 5 second passed
        for index in range(0, 2):
            self._velocity[index] = self._velocity[index] * 1.12
            # print ("speed increased")

    def move(self):
        # Change the location and the velocity of the Dot so it
        # remains on the surface by bouncing from its edges.
        # - self is the Dot

        size = (self._window.get_width(), self._window.get_height())
        for index in range(0, 2):
            # update center at index
            self._center[index] = self._center[index] + self._velocity[index]
            # dot perimeter outside window?
            if (self._center[index] < self._radius) or (self._center[index] + self._radius > size[index]):
                # change direction
                self._velocity[index] = - self._velocity[index]

    def draw(self, img):
        # Draw the dot on the surface.
        # - self is the Dot
        surface = self._window.get_surface()
        # color = Color(self._color)
        if img == 'cat':
            surface.blit(cat, [self._center[0]-self._radius,self._center[1]-self._radius])
        elif img == 'dog':
            surface.blit(dog, [self._center[0]-self._radius,self._center[1]-self._radius])
        # draw_circle(surface, color, self._center, self._radius)

    def intersects(self, dot):
        # Return True if the two dots intersect and False if
        # they do not.
        # - self is a Dot
        # - dot is the other Dot

        distance = sqrt((self._center[0] - dot._center[0])**2 + (self._center[1] - dot._center[1])**2)
        return distance <= self._radius + dot._radius

    def get_color(self):
        # Return a str that represents the color of the dot.
        # - self is the Dot
        
        return self._color
    
    def randomize(self):
        # Change the dot so that its center is at a random
        # point on the surface. Ensure that no part of a dot
        # extends beyond the surface boundary.
        # - self is the Dot

        size = (self._window.get_width(), self._window.get_height())
        for index in range(0, 2):
            self._center[index] = randint(self._radius, size[index] - self._radius)
main()