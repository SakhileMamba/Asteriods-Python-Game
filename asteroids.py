"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others

This program implements the asteroids game.
"""
import arcade
import random
from abc import ABC, abstractmethod
import math 

# These are Global constants to use throughout the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.75
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5 
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

class Point:
    """This class defines a point in the window in x and y coordinates, a point object is used to position the ball and the paddle
    in this program."""

    def __init__(self):
        """This method initializes the x and y coordinates of this point class"""
        self.x = 0
        self.y = 0

class Velocity:
    """This class defines the velocity of a ball object"""
    
    def __init__(self):
        """This method initializes the velocity of a ball object along the x and y coordinates."""
        
        self.dx = 0
        self.dy = 0

class Flying_Objects(ABC):
    """This is a base class definition with attributes and methods common to all flying objects(bullets and targets)"""

    def __init__(self):
        """This method initializes the attributes common in all flying objects"""
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0.0
        self.alive = True #this is not defined in requirements for bullet class, remove later.
        self.lives = 1
        self.angle = 0.0
        self.rotation_angle = 0
        self.drawing_path = ""
    
    
    def advance(self):
        """This method moves a flying object on the screen"""
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    #@abstractmethod
    def rotate(self):
        """This method rotates the objects of this class"""
        self.angle += self.rotation_angle

    @abstractmethod
    def draw(self):
        """This method draws an object on the screen, a string file path is passes in as an arguement to determen the png file to draw""" 
        img = self.drawing_path
        texture = arcade.load_texture(img)

        width = texture.width
        height = texture.height
        alpha = 255 # For transparency, 1 means not transparent

        x = self.center.x
        y = self.center.y
        angle = self.angle

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)  

    #@abstractmethod
    def hit(self):
        """This methods return an int value when a hit is detected"""
        self.alive = False
        return 1
        

    @abstractmethod
    def wrap_screen(self, screen_width, screen_height):
        """This methods tests to see if a flying object in on the screen"""  
        if self.center.x > screen_width + self.radius :
            self.center.x = screen_width - screen_width -self.radius
        
        elif self.center.x < screen_width - screen_width - self.radius:
            self.center.x = screen_width + self.radius

        if self.center.y > screen_height + self.radius:
            self.center.y = screen_height - screen_height - self.radius
        
        elif self.center.y < screen_height - screen_height - self.radius:
            self.center.y = screen_height + self.radius
            

class Big_Rock(Flying_Objects):
    """This class defines a Big Rock that breaks in smaller rocks only after 1 short, it gives off 
    1 point"""
    
    def __init__(self):
        """This method initializes the attributes common in all flying objects"""
        super().__init__()
        self.center.x = random.uniform(0 , SCREEN_WIDTH)
        self.center.y = random.uniform(0 , SCREEN_HEIGHT)
        self.velocity.dx = random.choice([BIG_ROCK_SPEED * -1, BIG_ROCK_SPEED])
        self.velocity.dy = random.choice([BIG_ROCK_SPEED * -1, BIG_ROCK_SPEED])
        self.radius = BIG_ROCK_RADIUS
        #self.alive = True #this is not defined in requirements for bullet class, remove later.
        #self.lives = 1
        #self.angle = 0.0
        self.rotation_angle = BIG_ROCK_SPIN
        self.drawing_path = "images/meteorGrey_big1.png"
        
    
    def advance(self):
        """This method moves a flying object on the screen"""
        super().advance()

    
    def rotate(self):
        """This method rotates the objects of this class"""
        super().rotate()

    
    def draw(self):
        """This method draws an object on the screen, a string file path is passes in as an arguement to determen the png file to draw""" 
        super().draw()

    
    def hit(self):
        """This methods return an int value when a hit is detected, it breaks down rock by forming three new smaller rocks"""
        self.alive = False

        medium_rock_1_created = Medium_Rock()
        medium_rock_2_created = Medium_Rock()
        small_rock_created = Small_Rock()

        medium_rock_1_created.center.x = self.center.x
        medium_rock_1_created.center.y = self.center.y
        medium_rock_1_created.velocity.dx = self.velocity.dx
        medium_rock_1_created.velocity.dy = self.velocity.dy + 2

        medium_rock_2_created.center.x = self.center.x
        medium_rock_2_created.center.y = self.center.y
        medium_rock_2_created.velocity.dx = self.velocity.dx
        medium_rock_2_created.velocity.dy = self.velocity.dy - 2

        small_rock_created.center.x = self.center.x
        small_rock_created.center.y = self.center.y
        small_rock_created.velocity.dx = self.velocity.dx + 5
        small_rock_created.velocity.dy = self.velocity.dy

        return [medium_rock_1_created, medium_rock_2_created, small_rock_created, 2]
        #pass

    
    def wrap_screen(self, screen_width, screen_height):
        """This methods tests to see if a flying object in on the screen"""  
        super().wrap_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
        

class Medium_Rock(Big_Rock):
    """This class defines the medium rock attributes and methods"""

    def __init__(self):
        """This method overides the radius attribute"""
        super().__init__()
        self.radius = MEDIUM_ROCK_RADIUS
        self.drawing_path = "images/meteorGrey_med1.png"
        self.rotation_angle = MEDIUM_ROCK_SPIN

    def hit(self):
        """This function implements logic when the rock is hit by a bullet, breaks down rock by forming two new small rocks"""
        self.alive = False

        small_rock_created1 = Small_Rock()
        small_rock_created2 = Small_Rock()

        small_rock_created1.center.x = self.center.x
        small_rock_created1.center.y = self.center.y
        small_rock_created1.velocity.dx = self.velocity.dx + 1.5
        small_rock_created1.velocity.dy = self.velocity.dy + 1.5

        small_rock_created2.center.x = self.center.x
        small_rock_created2.center.y = self.center.y
        small_rock_created2.velocity.dx = -1.5
        small_rock_created2.velocity.dy = -1.5

        return [small_rock_created1, small_rock_created2, 4]


class Small_Rock(Big_Rock):
    """This class defines the small rock attributes and methods"""

    def __init__(self):
        """This method overides the radius attribute"""
        super().__init__()
        self.radius = SMALL_ROCK_RADIUS
        self.drawing_path = "images/meteorGrey_small1.png"
        self.rotation_angle = SMALL_ROCK_SPIN

    def hit(self):
        """This function implements logic when the rock is hit by a bullet, it ensures rock is destroyed"""
        self.alive = False
        return [6]


class Ship(Flying_Objects):
    """This is class defines a spaceship that can fire bullets"""
    def __init__(self):
        super().__init__()
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = SCREEN_HEIGHT / 2
        self.velocity.dx = SHIP_THRUST_AMOUNT
        self.velocity.dy = SHIP_THRUST_AMOUNT
        self.radius = SHIP_RADIUS
        self.speed = SHIP_THRUST_AMOUNT
        self.dethrust_ship = True
        self.rotation_angle = SHIP_TURN_AMOUNT
        self.drawing_path = "images/playerShip1_orange.png"
        self.alert_lives = 15
        #self.alive = True #this is not defined in requirements for bullet class, remove later.
        #self.lives = 1
        #self.angle = 0.0


    def advance(self):
        """This method moves a flying object on the screen"""
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    
    def rotate_right(self):
        """This method rotates the objects of this class"""
        self.angle += self.rotation_angle 

    def rotate_left(self):
        """This method rotates the ship to the left"""
        self.angle += self.rotation_angle * -1

    
    def draw(self):
        """This method draws an object on the screen, a string file path is passes in as an arguement to determen the png file to draw""" 
        super().draw() 

    
    def hit(self):
        """This methods return an int value when a hit is detected"""
        self.__init__()
        self.alert_lives += 10

    def alert_draw_function(self):
        """This functions draw an alert when the ship is hit."""
        
        if  self.alert_lives > 0:
            alert_text = "Ship Hit! Restarting...."
            start_x = 15
            start_y = SCREEN_HEIGHT - 40
            arcade.draw_text(alert_text, start_x=start_x, start_y=start_y, font_size=30, color=arcade.color.WHITE)
            self.alert_lives -= 1
        

    def wrap_screen(self, screen_width, screen_height):
        """This methods tests to see if a flying object in on the screen"""  
        super().wrap_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    def thrust(self):
        """This method moves the ship forward according to its angle"""
        
        self.dethrust_ship = True
        self.speed += SHIP_THRUST_AMOUNT
        self.velocity.dx = math.cos(math.radians(self.angle)) * (self.speed)
        self.velocity.dy = math.sin(math.radians(self.angle)) * (self.speed)
        #self.advance()

    def dethrust(self):
        """This function allows the ship to slow down when the up arrow key is released."""
        self.dethrust_ship = False
        self.velocity.dx = math.cos(math.radians(self.angle)) * (SHIP_THRUST_AMOUNT)
        self.velocity.dy = math.sin(math.radians(self.angle)) * (SHIP_THRUST_AMOUNT)
        self.speed = SHIP_THRUST_AMOUNT

class Bullet(Flying_Objects):
    """This class defines a bullet and inherits from the flying object class"""

    def __init__(self):
        """This method overides certain bullet attributes"""
        super().__init__()
        self.radius = BULLET_RADIUS
        self.lives = 60
        self.alive = True
        self.angle = 0.0
        self.drawing_path = "images/laserBlue01.png"

    
    def advance(self):
        """This method moves a flying object on the screen"""
        super().advance()


    def draw(self):
        """This method draws an object on the screen, a string file path is passes in as an arguement to determen the png file to draw"""   
        super().draw()

    def wrap_screen(self, screen_width, screen_height):
        """This methods tests to see if a flying object in on the screen"""  
        super().wrap_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    def die_in_sixty_frames(self):
        """This function ensures bullets are killd in 60 frames"""
        if self.lives > 0:
            self.lives -= 1
        else:
            self.alive = False

    def fire(self, angle):
        """this method fires a bullet according to the ship's angle which is passed in as an arguement"""
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
        self.advance()



class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.score = 0

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        
        self.rocks = []
        self.bullets = []

        for number in range(INITIAL_ROCK_COUNT):
            rock = Big_Rock()
            self.rocks.append(rock)

        self.ship = Ship()

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object

        for rock in self.rocks:
            rock.draw()

        for bullet in self.bullets:
            bullet.draw()

        self.ship.draw()

        self.ship.alert_draw_function()

        self.draw_score()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        #print(self.held_keys)
        if arcade.key.UP not in self.held_keys:
            if self.ship.dethrust_ship == True:
                self.ship.dethrust()

        # TODO: Tell everything to advance or move forward one step in time
        for rock in self.rocks:
            rock.advance()
            rock.rotate()
            rock.wrap_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        for bullet in self.bullets:
            bullet.advance()
            bullet.die_in_sixty_frames()
            bullet.wrap_screen(SCREEN_WIDTH,SCREEN_HEIGHT)

        self.ship.advance()
        self.ship.wrap_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
        #self.cleanup_zombies()
        self.check_collisions()
        self.check_ship_and_rocks_collisions()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = SCREEN_WIDTH - 120
        start_y = SCREEN_HEIGHT - 40
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=20, color=arcade.color.WHITE)


    def check_collisions(self):
        """
        Checks to see if bullets have hit rocks.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your rocks list "rocks"

        for bullet in self.bullets:
            for rock in self.rocks:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and rock.alive:
                    too_close = bullet.radius + rock.radius

                    if (abs(bullet.center.x - rock.center.x) < too_close and
                                abs(bullet.center.y - rock.center.y) < too_close):
                        # its a hit!
                        bullet.hit()
                        rocks_and_points_returned = rock.hit()
                        for x in rocks_and_points_returned:
                            if type(x) == Medium_Rock or type(x) == Small_Rock:
                                self.rocks.append(x)
                            elif type(x) == int:
                                self.score += x
                        #self.score += rock.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()


    def check_ship_and_rocks_collisions(self):
        """
        Checks to see if ship have hit rocks.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your rocks list "rocks"

        for rock in self.rocks:

            # Make sure they are both alive before checking for a collision
            if self.ship.alive and rock.alive:
                too_close = self.ship.radius + rock.radius

                if (abs(self.ship.center.x - rock.center.x) < too_close and
                            abs(self.ship.center.y - rock.center.y) < too_close):
                    # its a hit!
                    self.ship.hit()
                    self.score = 0
                    #self.score += rock.hit()

                    # We will wait to remove the dead objects until after we
                    # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()
        

        # TODO: Check for collisions

    def cleanup_zombies(self):
        """
        Removes any dead bullets or rocks from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for rock in self.rocks:
            if not rock.alive:
                self.rocks.remove(rock)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.rotate_right()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.rotate_left()

        if arcade.key.UP in self.held_keys:
            self.ship.thrust()

        if arcade.key.DOWN in self.held_keys:
            pass

        # Machine gun mode...
        if arcade.key.SPACE in self.held_keys:
            pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullet()
                bullet.angle = self.ship.angle
                bullet.center.x = self.ship.center.x
                bullet.center.y = self.ship.center.y
                bullet.fire(self.ship.angle)
                self.bullets.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
            
            

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()