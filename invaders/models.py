"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object. So technically Bolt, which has a velocity,
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you
add new features to your game, such as power-ups.  If you are unsure about whether to
make a new class or not, please ask on Piazza.

# Ayesha Kemal (ak2235) and Kevin Huang (kqh3)
# December 4th, 2018
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getPosx(self):
        """
        RETURNS the x position of the ship object.
        """
        return self.x

    def setPosx(self, x):
        """
        SETS the x position of the ship object to the value x.

        Parameter x: The x value to be assigned.
        Precondition: x must be an int or float
        """
        self.x = x

    def __init__(self, x, y, width, height, source):
        """
        Initializes a new ship object.

        Parameter x: The x positon of the ship object.
        Precondition: X must be an int or float.

        Parameter y: The y positon of the ship object.
        Precondition: Y must be an int or float.

        Parameter width: The width of the ship object.
        Precondition: Width must be an int or float.

        Parameter height: The height of the ship object.
        Precondition: Height must be an int or float.

        Parameter source: The source file for the ship object image.
        Precondition: Source must be a string refering to a valid file.
        """
        super().__init__(x=x,y=y,width=width,height=height,source=source,)


class Alien(GSprite):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    def getPosx(self):
        """
        RETURNS the x position of the alien object.
        """
        return self.x

    def setPosx(self, x):
        """
        SETS the x position of the alien object to the value x.

        Parameter x: The x value to be assigned.
        Precondition: x must be an int or float
        """
        self.x = x

    def getPosy(self):
        """
        RETURNS the y position of the alien object.
        """
        return self.y

    def setPosy(self, y):
        """
        SETS the y position of the alien object to the value y.

        Parameter y: The y value to be assigned.
        Precondition: y must be an int or float
        """
        self.y = y

    def getSource(self):
        """
        RETURNS the source of the alien object.
        """
        return self.source

    def __init__(self, x, y, width, height, source, format):
        """
        Initializes a new alien object.

        Parameter x: The x positon of the alien object.
        Precondition: X must be an int or float.

        Parameter y: The y positon of the alien object.
        Precondition: Y must be an int or float.

        Parameter width: The width of the alien object.
        Precondition: Width must be an int or float.

        Parameter height: The height of the alien object.
        Precondition: Height must be an int or float.

        Parameter source: The source file for the alien object image.
        Precondition: Source must be a string refering to a valid file.

        Parameter format: Format is the grid of animation frames.
        Precondition: Format must be a tuple of two ints or floats.
        """
        super().__init__(x=x,y=y,width=width,height=height,source=source,
        format=format)


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need getters for
    them.  However, it is possible to write this assignment with no setters for the
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.

    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a
    helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
        _type: [The type of the bolt; either 'player' or 'alien']

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setPosx(self, x):
        """
        SETS the x position of the bolt object to the value x.

        Parameter x: The x value to be assigned.
        Precondition: x must be an int or float
        """
        self.x = x

    def getPosx(self):
        """
        RETURNS the x position of the bolt object.
        """
        return self.x

    def setPosy(self, y):
        """
        SETS the y position of the bolt object to the value x.

        Parameter y: The y value to be assigned.
        Precondition: y must be an int or float
        """
        self.y = y

    def getPosy(self):
        """
        RETURNS the y position of the bolt object.
        """
        return self.y

    def getSpeed(self):
        """
        RETURNS the velocity/speed of the bolt object.
        """
        return self._velocity

    def setSpeed(self, speed):
        """
        SETS the veocity of the bolt object to the value speed.

        Parameter speed: The speed value to be assigned.
        Precondition: Speed must be an int or float
        """
        self._velocity = speed

    def getType(self):
        """
        RETURNS the type of bolt object either 'player' or 'alien'.
        """
        return self._type

    def setType(self, type):
        """
        SETS the type of the bolt to the given value type.

        Parameter type: The type value to be assigned.
        Precondition: Type must be a valid string.
        """
        self._type = type

    def __init__(self, x, y, width, height, fillcolor, velocity, type):
        """
        Initializes a new bolt object.

        Parameter x: The x positon of the bolt object.
        Precondition: X must be an int or float.

        Parameter y: The y positon of the bolt object.
        Precondition: Y must be an int or float.

        Parameter width: The width of the bolt object.
        Precondition: Width must be an int or float.

        Parameter height: The height of the bolt object.
        Precondition: Height must be an int or float.

        Parameter fillcolor: The bolt object's fill color
        Precondition: Must be a 4-element list of floats between 0 and 1
        (representing r, g, b, and a)

        Parameter velocity: The velocity of the bolt object.
        Precondition: Velocity must be an int or float

        Parameter type: The type of bolt either 'player' or 'alien'
        Precondition: Type must be a valid string.
        """
        super().__init__(x=x,y=y,width=width,height=height,fillcolor=fillcolor)
        self._velocity = velocity
        self._type = type
