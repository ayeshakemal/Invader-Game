"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

# Ayesha Kemal (ak2235) and Kevin Huang (kqh3)
# December 4th, 2018
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.


    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _lastkeys: the number of keys pressed in the previous frame
                   [int >= 0]
    """

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state = STATE_INACTIVE
        self._game = None
        self._text = GLabel(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=GAME_WIDTH,
        height=GAME_HEIGHT, font_name = 'Arcade')
        self._text.text = "Press 'S' to Start. Press 'Y' to toggle Volume"
        self._text.font_size = 30
        self._text.halign = 'center'
        self._text.valign = 'middle'
        self._text.bold = True
        self._text.linecolor = [0.0,1.0,0.0,1.0]
        self._text.fillcolor = 'black'
        self._lastkeys = 0
        self._wave = Wave()

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        current_keys = self.input.key_count
        if self.input.is_key_down('y') and current_keys > 0 and self._lastkeys == 0:
            if self._wave.getVolume() == 1:
                self._wave.setVolume(0)
            elif self._wave.getVolume() == 0:
                self._wave.setVolume(1)
        if (self.input.is_key_down('s') and current_keys > 0 and
        self._lastkeys == 0 and self._state == STATE_INACTIVE):
            self._state = STATE_NEWWAVE
            self._text = None
        if self._state == STATE_NEWWAVE:
            self._state = STATE_ACTIVE
        self._wave.setTime(self._wave.getTime() + dt)
        if self._state == STATE_PAUSED:
            if self.input.is_key_down('s') and current_keys > 0 and self._lastkeys == 0:
                self._state = STATE_CONTINUE
                self._wave.setShip(self._wave.getStoredShip())
                self._state = STATE_ACTIVE
                self._text = None
        self.state_is_complete()

    def state_is_complete(self):
        """
        Updates the state if the state is STATE_COMPLETE
        """
        current_keys = self.input.key_count
        if self._state == STATE_COMPLETE:
            if self.input.is_key_down('s') and current_keys > 0 and self._lastkeys == 0:
                if self._wave.game_over() == True:
                    lives = self._wave.getLives()
                    speed = self._wave.getSpeed()
                    score = self._wave.getScore()
                    number = self._wave.getWaveNumber()
                    self._wave = Wave()
                    self._state = STATE_NEWWAVE
                    self._text = None
                    self._wave.setSpeed(speed*.95)
                    self._wave.setLives(lives)
                    self._wave.setScore(score)
                    self._wave.setWaveNumber(number + 1)
                    if self._wave.getWaveNumber() % 2 == 0:
                        self._wave.setAliens(self._wave.getBossAlien())
                        self._wave.setBossLives(BOSS_LIVES)
                else:
                    self.start()
        self._lastkeys = current_keys

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        if self._state == STATE_INACTIVE:
            self._text.draw(self.view)
        if self._state == STATE_NEWWAVE:
            self._wave.draw(self.input, self.view)
            self._wave.update(self.input)
        self.game_is_active()
        if self._state == STATE_CONTINUE:
            self._wave.draw(self.input, self.view)
            self._wave.update(self.input)
        if (self._wave.getShip() is None) and self._state == STATE_ACTIVE:
            self._wave.lose_a_life()
            self._state = STATE_PAUSED
        self.game_is_paused()
        self.game_is_done()

    def game_is_active(self):
        """
        Draws the active screen displaying the player score, the ship lives,
        and the current wave when the player is in STATE_ACTIVE.

        The active screen displays "Lives: __" , "Wave: __", and "Score: __"
        """
        if self._state == STATE_ACTIVE:
            self._text = GLabel(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=GAME_WIDTH,
            height=GAME_HEIGHT, font_name = 'Arcade')
            self._text.fillcolor = 'black'
            if self._wave.getWaveNumber() % 2 == 0:
                self._text.text = ("Lives: "  + str(self._wave.getLives()) + '   '
                + 'Boss Lives: ' + str(self._wave.getBossLives()) + '   ' 'Score: '
                + str(self._wave.getScore()))
            else:
                self._text.text = ("Lives: "  + str(self._wave.getLives()) + '      '
                + 'Wave: ' + str(self._wave.getWaveNumber()) + '      ' 'Score: ' +
                 str(self._wave.getScore()))
            self._text.font_size = 40
            self._text.halign = 'left'
            self._text.valign = 'top'
            self._text.bold = True
            self._text.linecolor = [0.0,1.0,0.0,1.0]
            self._text.draw(self.view)
            self._wave.draw(self.input, self.view)
            self._wave.update(self.input)

    def game_is_paused(self):
        """
        Draws the paused screen displaying how many lives the ship has left when
        tbe player reaches STATE_PAUSED.

        The paused screen displays "Lives Remaining: __ . Press 'S' to Continue"

        """
        if self._state == STATE_PAUSED:
            if self._wave.check_game_status() == False:
                self._wave.setBolts([])
                self._text = GLabel(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=GAME_WIDTH,
                height=GAME_HEIGHT, font_name = 'Arcade')
                self._text.text = ("Lives Remaining: "  + str(self._wave.getLives())+
                 " Press 'S' to Continue")
                self._text.font_size = 40
                self._text.halign = 'center'
                self._text.valign = 'middle'
                self._text.bold = True
                self._text.linecolor = [0.0,1.0,0.0,1.0]
                self._text.fillcolor = 'black'
                self._text.draw(self.view)
                self._wave.update(self.input)

    def game_is_done(self):
        """
        Draws the next wave screen or losing screen after the player reaches STATE_COMPLETE.

        The next wave screen displays 'Wave cleared. Press 'S' to begin next Wave'
        and the losing screen displays 'Game Over! Score: '
        """
        if self._wave.game_over() == False and self._state != STATE_INACTIVE:
            self._wave.setBolts([])
            self._state = STATE_COMPLETE
            self._text = GLabel(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=GAME_WIDTH,
            height=GAME_HEIGHT, font_name = 'Arcade')
            self._text.text = "Game Over! Score: " + str(self._wave.getScore())
            self._text.font_size = 40
            self._text.halign = 'center'
            self._text.valign = 'middle'
            self._text.bold = True
            self._text.linecolor = [0.0,1.0,0.0,1.0]
            self._text.fillcolor = 'black'
            self._text.draw(self.view)
            self._wave.update(self.input)
        if self._wave.game_over() == True and self._state != STATE_INACTIVE:
            self._wave.setBolts([])
            self._state = STATE_COMPLETE
            self._text = GLabel(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=GAME_WIDTH,
            height=GAME_HEIGHT, font_name = 'Arcade')
            self._text.text = "Wave cleared. Press 'S' to begin next Wave"
            self._text.font_size = 35
            self._text.halign = 'center'
            self._text.valign = 'middle'
            self._text.bold = True
            self._text.linecolor = [0.0,1.0,0.0,1.0]
            self._text.fillcolor = 'black'
            self._text.draw(self.view)
            self._wave.update(self.input)
