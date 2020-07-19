"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# Ayesha Kemal (ak2235) and Kevin Huang (kqh3)
# December 4th, 2018
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
        _direction: The marching direction of the aliens [str, either 'Left' or 'Right']
        _alien_bolt_time: The amount of time between bolt firings [1 <= int <= BOLT_RATE]
        _alien_steps: A representation of the amount of time that has passed since the
                      last bolt firing. When this reaches _alien_bolt_time, an alien
                      fires [0 <= float or int <= _alien_bolt_time]
        _bolt_collided_with_alien: A bolt object that collided with an alien [Bolt Object]
        _bolt_collided_with_ship: A bolt object that collided with the ship [Bolt Object]
        _alien_collided: A list of the index positions of an alien that has collided with a ship
                         bolt, in the form of [row, column]
        _ship_stored: Stores the orginal ship object [Ship Object]
        _sound_pew: The sound that plays when the ship fires a bolt [Sound Object]
        _sound_blast: The sound that plays when an alien is destroyed [Sound Object]
        _sound_blast1: An alternative sound that plays when an alien is destroyed [Sound Object]
        _speed: The number of seconds between alien steps [0 < float <= 1]
        _score: The score the player has accumulated.
                Increases as the player kills aliens [Int or Float >= 0]
        _wave_number: The wave number the player is currently on.
                      Starts at 1 and increases by 1 as the player clears waves [Int >= 1]
        _boss_alien: a singular alien that appears in a wave.
                     [A 2D list of one Alien Object - Ex. [[Alien]] ]
        _sound_counter: Controls which sound file is played when an alien is killed
                        [int, either 0 or 1]
        _volume: Controls if sound is audible. If it is 0, the sound is muted.
                 If it is 1, the game plays sounds [int, either 0 or 1]


    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAliens(self):
        """
        Returns the value of the attribute _aliens
        """
        return self._aliens

    def setAliens(self, aliens):
        """
        Sets the attribute _aliens to aliens

        Parameter: aliens is the 2D list of aliens to be assigned
        Precondition: aliens is a 2D of aliens
        """
        self._aliens = aliens

    def setStoredAliens(self, aliens):
        """
        Sets the attribute _aliens_stored to aliens

        Parameter: aliens is the 2D list of aliens to be assigned
        Precondition: aliens is a 2D of aliens
        """
        self._aliens_stored = aliens

    def getStoredAliens(self):
        """
        Returns the value of the attribute _aliens_stored
        """
        return self._aliens_stored

    def getShip(self):
        """
        Returns the value of the attribute _ship
        """
        return self._ship

    def setShip(self,ship):
        """
        Sets the attribute _ship to ship

        Parameter: ship is a Ship Object to be assigned
        Precondition: ship is a Ship object
        """
        self._ship = ship

    def getDline(self):
        """
        Returns the value of the attribute _dline
        """
        return self._dline

    def setTime(self, time):
        """
        Sets the attribute _time to time

        Parameter: time is the value to be assigned
        Precondition: time is a int or float >= 0
        """
        self._time = time

    def getTime(self):
        """
        Returns the value of the attribute _time
        """
        return self._time

    def setLives(self, lives):
        """
        Sets the attribute _aliens to aliens

        Parameter: lives is the value to be assigned
        Precondition: lives is an int >= 0
        """
        self._lives = lives

    def getLives(self):
        """
        Returns the value of the attribute _lives
        """
        return self._lives

    def getStoredShip(self):
        """
        Returns the value of the attribute _ship_stored
        """
        return self._ship_stored

    def setStoredShip(self, ship):
        """
        Sets the attribute _ship_stored to ship

        Parameter: ship is the value to be assigned
        Precondition: ship is a Ship object
        """
        self._ship_stored = ship

    def getBolts(self):
        """
        Returns the value of the attribute _bolts
        """
        return self._bolts

    def setBolts(self, bolts):
        """
        Sets the attribute _bolts to bolts

        Parameter: bolts is value to be assigned
        Precondition: bolts is a list of bolts
        """
        self._bolts = bolts

    def getSound(self):
        """
        Returns the value of the attribute _sound
        """
        return self._sound

    def setSpeed(self, speed):
        """
        Sets the attribute _speed to speed

        Parameter: speed is the value to be assigned
        Precondition: speed is 0 < float <= 1
        """
        self._speed = speed

    def getSpeed(self):
        """
        Returns the value of the attribute _speed
        """
        return self._speed

    def getScore(self):
        """
        Returns the value of the attribute _score
        """
        return self._score

    def setScore(self, score):
        """
        Sets the attribute _score to score

        Parameter: score is the value to be assigned
        Precondition: score is an int >= 0
        """
        self._score = score

    def setWaveNumber(self, number):
        """
        Sets the attribute _wave_number to number

        Parameter: number is the value to be assigned
        Precondition: number is an int >= 0
        """
        self._wave_number = number

    def getWaveNumber(self):
        """
        Returns the value of the attribute _wave_number
        """
        return self._wave_number

    def getBossAlien(self):
        """
        Returns the value of the attribute _boss_alien
        """
        return self._boss_alien

    def setVolume(self, volume):
        """
        Sets the attribute _volume to volume

        Parameter: volume is the value to be assigned
        Precondition: volume is an int, either 0 or 1
        """
        self._volume = volume

    def getVolume(self):
        """
        Returns the value of the attribute _volume
        """
        return self._volume

    def setBossLives(self, lives):
        """
        Sets the attribute _boss_lives to lives

        Parameter: lives is value to be assigned
        Precondition: lives is an int >= 0
        """
        self._boss_lives = lives

    def getBossLives(self):
        """
        Returns the value of the attribute _boss_lives
        """
        return self._boss_lives

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializer for all the wave objects.

        Creates the ship objects, Alien objects, and Sound objects needed
        for the wave.
        """
        self._aliens = self.sort_aliens()
        self._ship = Ship(x = GAME_WIDTH / 2, y = SHIP_BOTTOM + SHIP_HEIGHT/2,
        width=SHIP_WIDTH, height = SHIP_HEIGHT, source = 'ship.png')
        self._ship_stored = self._ship
        self._dline = GPath(points = [0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE],
        linewidth = 2, linecolor = 'grey')
        self._time = 0
        self._direction = 'Right'
        self._bolts = []
        self._alien_bolt_time = 0
        self._alien_steps = None
        self._lives = SHIP_LIVES
        self._bolt_collided_with_ship = None
        self._bolt_collided_with_alien = None
        self._alien_collided = None
        self._sound_pew = Sound('pew1.wav')
        self._sound_blast = Sound('blast1.wav')
        self._sound_blast2 = Sound('blast2.wav')
        self._speed = ALIEN_SPEED
        self._score = 0
        self._score_stored = self._score
        self._wave_number = 1
        self._boss_alien = [[Alien(x = GAME_WIDTH /2 , y = GAME_HEIGHT / 2,
        width = ALIEN_WIDTH, height = ALIEN_HEIGHT, source = 'alien-strip4.png',
        format=(3,2))]]
        self._sound_counter = 0
        self._volume = 1
        self._boss_lives = 1

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input):
        """
        Animates the ship, aliens, and bolts in the wave.

        Parameter input: input is the user input that is required to control
        the ship, control the volume, and change the state
        Precondition: Must be an instance of GInput
        """
        if not self._ship is None:
            ds = 0
            if input.is_key_down('left'):
                ds = ds - SHIP_MOVEMENT/2
            if input.is_key_down('right'):
                ds = ds + SHIP_MOVEMENT/2
            new_ship_pos = self._ship.x + ds
            if new_ship_pos >= (SHIP_WIDTH/2) and new_ship_pos <= (GAME_WIDTH -
            SHIP_WIDTH/2):
                self._ship.setPosx(new_ship_pos)
            if input.is_key_down('spacebar'):
                self.draw_bolt_player()
        if (not self._aliens[0][0] is None) and (self._aliens[0][0].getSource() ==
        'alien-strip4.png'):
            self.move_boss_alien()
        else:
            self.move_aliens()
        self.delete_bolt()
        self.draw_bolt_alien()
        if self.is_player_bolt_in_list() == True:
            for _ in self._bolts:
                if _.getType() == 'player':
                    _.setPosy(_.getPosy() + BOLT_SPEED/2)
        if self.is_alien_bolt_in_list() == True:
            for _ in self._bolts:
                if _.getType() == 'alien':
                    _.setPosy(_.getPosy() - BOLT_SPEED/2)
        self.collision_detector()

    def draw(self,input,view):
        """
        Draws the wave objects to the view. This function draws the aliens,
        ships, bolts, defense lines needed to play the game.

        Parameter input: input is the user input that is required to control
        the ship, control the volume, and change the stateself.
        Precondition: Must be an instance of GInput.

        Parameter view: view is a reference to the window
        """
        for _ in self.getAliens():
            for x in _:
                if not x is None:
                    x.draw(view)
        if not self._ship is None:
            self._ship.draw(view)
        self.getDline().draw(view)
        if input.is_key_down('spacebar') or self.is_player_bolt_in_list() == True:
            for _ in self._bolts:
                if _.getType() == 'player':
                    _.draw(view)
        if self.is_alien_bolt_in_list() == True:
            for _ in self._bolts:
                if _.getType() == 'alien':
                    _.draw(view)
        self.update(input)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw_aliens(self):
        """
        Returns a 1D list of aliens to be drawn, representing all the aliens
        in a grid with rows and columns. The horizontal separation between aliens is
        ALIEN_H_SEP and the vertical separation is ALIEN_V_SEP. The rows start
        a distance ALIEN_CEILING from the top of the window and ALIEN_H_SEP from
        the left of the window.

        The returned list is the aliens starting from the bottom-left, then going right.
        When the end of the row is reached, it starts from the left of the row
         above the preceding row. This list will later be sorted by sort_aliens()
        """
        aliens = []
        START_HEIGHT = GAME_HEIGHT - ALIEN_CEILING - ALIEN_ROWS*(ALIEN_HEIGHT/2
        + ALIEN_V_SEP)-ALIEN_V_SEP - ALIEN_HEIGHT
        x_pos = ALIEN_H_SEP + ALIEN_WIDTH/2
        y_pos = START_HEIGHT
        counter_col = 1
        list_pos = 0
        while counter_col <= ALIEN_ROWS:
            counter_rows = 1
            while counter_rows <= ALIENS_IN_ROW:
                aliens.append(Alien(x = x_pos, y = y_pos, width = ALIEN_WIDTH,
                 height = ALIEN_HEIGHT, source = ALIEN_IMAGES[list_pos], format=(3,2)))
                counter_rows = counter_rows + 1
                x_pos = x_pos + ALIEN_H_SEP + ALIEN_WIDTH
            y_pos = y_pos + ALIEN_V_SEP + ALIEN_HEIGHT
            x_pos = ALIEN_H_SEP + ALIEN_WIDTH/2
            counter_col = counter_col + 1
            if  counter_col % 2 != 0:
                list_pos = list_pos + 1
                if list_pos >= len(ALIEN_IMAGES):
                    list_pos = 0
        return aliens

    def sort_aliens(self):
        """
        Returns a proper 2D (nested) list from the output of draw_aliens() in
        [column][row] form. i.e. Each element of the returned list is a list of
        all the alien objects in a row in order from left to right,
        beginning from the row closest to the ship.
        """
        aliens = self.draw_aliens()
        y = aliens[0].getPosy()
        counter = 0
        len_get = []
        while counter < len(aliens):
            if aliens[counter].getPosy() == y:
                len_get.append(aliens[counter])
                counter = counter + 1
            else:
                counter = len(aliens) + 1
        len_col = len(len_get)
        x = 0
        sorted_aliens = []
        while x < len(aliens):
            sorted_aliens.append(aliens[x : x + len_col])
            x = x + len_col
        return sorted_aliens

    def move_aliens(self):
        """
        Controls the movement logic of the aliens

        The aliens collectively march in one direction (initial direction is right).
        When the furthest alien reaches a distance ALIEN_H_SEP from the edge of the
        window, the aliens move down a distance ALIEN_V_WALK and then change direction
        The marching speed is determined by ALIEN_SPEED.

        Also updates the animation frame every time the aliens march.
        """
        if self._time > self._speed:
            if self._direction == 'Right':
                if (not self.furthest_alien() is None) and (self.furthest_alien()
                >= GAME_WIDTH - ALIEN_H_SEP*2.5):
                    for _ in self.getAliens():
                        for x in _:
                            if not x is None:
                                x.setPosy(x.getPosy() - ALIEN_V_WALK)
                                x.frame = (x.frame+1) % 2
                    self.change_direction()
                for _ in self.getAliens():
                    for x in _:
                        if not x is None:
                            x.setPosx(x.getPosx() + ALIEN_H_WALK)
                            x.frame = (x.frame+1) % 2
            if self._direction == 'Left':
                if (not self.furthest_alien() is None) and (self.furthest_alien()
                 <= ALIEN_H_SEP + ALIEN_H_SEP*1.5):
                    for _ in self.getAliens():
                        for x in _:
                            if not x is None:
                                x.setPosy(x.getPosy() - ALIEN_V_WALK)
                                x.setPosx(x.getPosx() + ALIEN_H_WALK)
                                x.frame = (x.frame+1) % 2
                    self.change_direction()
                for _ in self.getAliens():
                    for x in _:
                        if not x is None:
                            x.setPosx(x.getPosx() - ALIEN_H_WALK)
                            x.frame = (x.frame+1) % 2
            self._time = 0

    def furthest_alien(self):
        """
        Returns the x-Position of the right-most alien that is not None if _direction
        is 'Right' and the x-Position of the left-most alien that is not None
        if _direction is 'Left'
        """
        row = []
        for _ in self._aliens:
            for x in _ :
                if (x is None) == False:
                    if (x.getPosx() in row) == False:
                        row.append(x.getPosx())
        if row != []:
            if self._direction == 'Right':
                return max(row)
            if self._direction == 'Left':
                return min(row)

    def len_row(self):
        """
        Returns the length of the alien row, accounting for the alien width and
        horizontal separation between aliens.
        """
        return ALIENS_IN_ROW * ALIEN_WIDTH + (ALIENS_IN_ROW - 1)*ALIEN_H_SEP

    def change_direction(self):
        """
        Changes the marching direction of the aliens (the attribute _direction)
        to the opposite of what it currently is. (i.e. changes 'Left' to 'Right'
        and vice versa)
        """
        if self._direction == 'Right':
            self._direction = 'Left'
        elif self._direction == 'Left':
            self._direction = 'Right'

    def draw_bolt_player(self):
        """
        Adds a player bolt to the attribute _bolts if there is no player bolt already
        in bolts and if the ship is not None

        Also plays the pew sound if a player bolt is created.
        """
        if self.is_player_bolt_in_list() == False:
            if not self._ship is None:
                self._bolts.append(Bolt(self._ship.getPosx(), SHIP_BOTTOM, BOLT_WIDTH,
                 BOLT_HEIGHT, 'white', BOLT_SPEED, 'player'))
                if self._volume == 1:
                    self._sound_pew.play()

    def delete_bolt(self):
        """
        Removes the bolt objects in the attribute _bolts when they leave the game window.
        """
        for _ in self._bolts:
            if (self._bolts[self._bolts.index(_)].getPosy() >= GAME_HEIGHT and
            _.getType() == 'player'):
                self._bolts.remove(_)
        for _ in self._bolts:
            if (self._bolts[self._bolts.index(_)].getPosy() <= 0 and _.getType()
            == 'alien'):
                self._bolts.remove(_)

    def is_player_bolt_in_list(self):
        """
        Returns True if there is a player bolt in the attribute _bolts. False otherwise.
        """
        if self._bolts == []:
            return False
        else:
            for _ in self._bolts:
                if _.getType() == 'player':
                    return True
            return False

    def is_alien_bolt_in_list(self):
        """
        Returns True if there is an alien bolt in the attribute _bolts. False otherwise.
        """
        if self._bolts == []:
            return False
        else:
            for _ in self._bolts:
                if _.getType() == 'alien':
                    return True
            return False

    def draw_bolt_alien(self):
        """
        Draws the alien bolt from a proper location and at the proper time

        Time is determined by the constant BOLT_RATE, in which the number of steps
        the aliens march before firing is 1 <= steps <= BOLT_RATE

        The bolt is fired from an alien in a random column closest to the ship.
        """
        if self._alien_bolt_time == 0:
            self._alien_bolt_time = random.randint(1, BOLT_RATE)
        if self._alien_steps is None:
            self._alien_steps = 0
        if self._time == 0:
            self._alien_steps = self._alien_steps + .5
        if self._alien_steps == self._alien_bolt_time:
            picked = self.pick_alien()
            counter = 0
            while (picked is None) and (counter < 100):
                picked = self.pick_alien()
                counter = counter + 1
            if not picked is None:
                self._bolts.append(Bolt(picked.getPosx(), picked.getPosy() ,
                BOLT_WIDTH, BOLT_HEIGHT, 'white', -BOLT_SPEED, 'alien'))
                self._alien_bolt_time = random.randint(1, BOLT_RATE)
                self._alien_steps = 0

    def pick_alien(self):
        """
        Randomly selects a column of aliens and returns the first alien in that
        column that is not None. If all aliens in the column are None, it returns
        None.
        """
        col_num = random.randint(0, len(self._aliens[0]))
        picked_col = []
        for _ in self._aliens:
            picked_col.append(_[col_num - 1])
        for _ in picked_col:
            if not _ is None:
                return _

    def collides_ship(self):
        """
        Returns true when an alien bolt collides with the ship

        Also stores the bolt object in the attribute _bolt_collided_with_ship
        """
        for _ in self._bolts:
            if _.getType() == 'alien':
                if not self._ship is None:
                    if (self._ship.contains((_.getPosx(), _.getPosy())) or
                    self._ship.contains((_.getPosx() + BOLT_WIDTH, _.getPosy())) or
                    self._ship.contains((_.getPosx() , _.getPosy() + BOLT_HEIGHT)) or
                    self._ship.contains((_.getPosx() + BOLT_WIDTH, _.getPosy() +
                    BOLT_HEIGHT))):
                        self._bolt_collided_with_ship = _
                        return True

    def collides_alien(self):
        """
        Returns true when a player bolt collides with an alien

        Also stores the alien object in the attribute _alien_collided and the bolt
        in _bolt_collided_with_alien.
        """
        for _ in self._bolts:
            if _.getType() == 'player':
                for rows in self._aliens:
                    for aliens in rows:
                        if not aliens is None:
                            if (aliens.contains((_.getPosx(), _.getPosy())) or
                            aliens.contains((_.getPosx() + BOLT_WIDTH, _.getPosy())) or
                            aliens.contains((_.getPosx() , _.getPosy() + BOLT_HEIGHT)) or
                            aliens.contains((_.getPosx() + BOLT_WIDTH, _.getPosy() +
                            BOLT_HEIGHT))):
                                self._bolt_collided_with_alien = _
                                self._alien_collided = [self._aliens.index(rows),
                                self._aliens[self._aliens.index(rows)].index(aliens)]
                                return True

    def collision_detector(self):
        """
        Does everything that needs to be done when a collision is detected.

        If a ship collides with an alien bolt, the bolt is deleted and the ship becomes
        None.

        If an alien collides with a ship bolt, the bolt is deleted and the alien becomes
        None (normal type) or it loses a life (boss alien). Boss alien is destroyed
        if its lives become zero.

        In addition, the appropriate score value is added to self._score according
        to the type of alien collided, a blast sound is played, and self._speed decreases
        by a factor of .99 (the alien marching speed increases).
        """
        if self.collides_ship() == True:
            self._bolts.remove(self._bolt_collided_with_ship)
            self._ship = None
        if self.collides_alien() == True:
            if (self._aliens[self._alien_collided[0]][self._alien_collided[1]].getSource()
             == 'alien-strip1.png'):
                self._score = self._score + 10
            elif (self._aliens[self._alien_collided[0]][self._alien_collided[1]].getSource()
             == 'alien-strip2.png'):
                self._score = self._score + 20
            elif (self._aliens[self._alien_collided[0]][self._alien_collided[1]].getSource()
             == 'alien-strip3.png'):
                self._score = self._score + 30
            elif (self._aliens[self._alien_collided[0]][self._alien_collided[1]].getSource()
             == 'alien-strip4.png'):
                self._score = self._score + 40
            if self._sound_counter == 0 and self._volume == 1:
                self._sound_blast.play()
                self._aliens[self._alien_collided[0]][self._alien_collided[1]].frame = 2
                self._sound_counter = 1
            elif self._sound_counter == 1 and self._volume == 1:
                self._sound_blast2.play()
                self._aliens[self._alien_collided[0]][self._alien_collided[1]].frame = 3
                self._sound_counter = 0
            self._bolts.remove(self._bolt_collided_with_alien)
            if self._boss_lives == 1:
                self._aliens[self._alien_collided[0]][self._alien_collided[1]] = None
            else:
                self._boss_lives = self._boss_lives - 1
            self._speed = self._speed * .99

    def lose_a_life(self):
        """
        Decreases the number of SHIP_LIVES by one if the ship object is None and
        SHIP_LIVES > 0

        """
        if (self.getShip() is None) and self.getLives() > 0:

            self.setLives(self.getLives() - 1)

    def check_game_status(self):
        """
        Returns True if the number of SHIP_LIVES is 0.
        Returns False otherwise.
        """
        if self.getLives() == 0:
            return True
        else:
            return False

    def pos_aliens(self):
        """
        Returns True if the wave of aliens is below the DEFENSE_LINE.
        Returns False otherwise.
        """
        for _ in self.getAliens():
            for x in _:
                if not x is None:
                    if x.getPosy() - ALIEN_WIDTH/2 < DEFENSE_LINE:
                        return True
                    else:
                        return False

    def we_won(self):
        """
        Returns True if each alien in the wave is equal to None, indicating that
        the player has successfully completed the wave.

        Returns False if the wave of aliens has not been completed and there is
        at least one alien in the eave that is not equal to None.
        """
        for _ in self.getAliens():
            for x in _:
                if not x is None:
                    return False
        return True

    def game_over(self):
        """
        Returns True if each alien in the wave is equal to None, indicating that
        the player has successfully completed the wave.

        Returns False if the number of SHIP_LIVES is 0 OR if the wave of aliens
        is below the DEFENSE_LINE
        """
        #lost game
        if self.check_game_status() == True:
            return False
        #lost game
        if self.pos_aliens() == True:
            return False
        #won game
        if self.we_won() != False:
            return True

    def move_boss_alien(self):
        """
        Controls the movement logic of a boss alien. The boss alien moves
        pseudo-randomly in all four directions. If it approaches an edge
        of the window, it will move in the opposite direction.
        In addition, when the player shoots a bolt, there is a chance that
        the alien will move left or right to attempt to dodge it.
        """
        if self._time > self._speed:
            self.dodging()
            self.edge_movements()
            self.random_movements()

    def dodging(self):
        """
        Controls the dodging mechanism of the boss alien's movements.
        """
        x= self._aliens[0][0]
        for _ in self._bolts:
            if not x is None:
                if (not _ is None) and ((x.getPosx() - ALIEN_WIDTH/1.5) <=
                _.getPosx() <= (x.getPosx() + ALIEN_WIDTH/1.5)) and (_.getType()
                == 'player'):
                    y = random.randint(0,1)
                    if y == 0:
                        x.setPosx(x.getPosx() + ALIEN_H_WALK*1.5)
                        x.frame = (x.frame+1) % 2
                    elif y == 1:
                        x.setPosx(x.getPosx() - ALIEN_H_WALK*1.5)

    def edge_movements(self):
        """
        Prevents the boss alien from getting close to an edge of the window
        """
        x= self._aliens[0][0]
        if not x is None:
            if x.getPosx() >= GAME_WIDTH - ALIEN_H_SEP*4: # Right Edge
                x.setPosx(x.getPosx() - ALIEN_H_WALK*2)
                x.frame = (x.frame+1) % 2
            elif x.getPosx() <= ALIEN_H_SEP*4: #Left Edge
                x.setPosx(x.getPosx() + ALIEN_H_WALK*2)
                x.frame = (x.frame+1) % 2
            if  x.getPosy() <= DEFENSE_LINE + ALIEN_V_SEP*3: #Bottom Edge
                    x.setPosy(x.getPosy() + ALIEN_V_WALK*3)
                    x.frame = (x.frame+1) % 2
            elif x.getPosy() >= GAME_HEIGHT - ALIEN_V_SEP*4: #Top Edge
                x.setPosy(x.getPosy() - ALIEN_V_WALK*3)
                x.frame = (x.frame+1) % 2

    def random_movements(self):
        """
        Moves the boss alien pseudo-randomly in all four directions
        """
        x= self._aliens[0][0]
        z = random.randint(0,8)
        if z == 0:
            x.setPosy(x.getPosy() - ALIEN_V_WALK)
            x.frame = (x.frame+1) % 2
        elif z == 1 or z == 4:
            x.setPosy(x.getPosy() + ALIEN_V_WALK)
            x.frame = (x.frame+1) % 2
        elif z == 2 or z == 5 or z == 6:
            x.setPosx(x.getPosx() + ALIEN_H_WALK*1.5)
            x.frame = (x.frame+1) % 2
        elif z == 3 or z == 7 or z == 8:
            x.setPosx(x.getPosx() - ALIEN_H_WALK*1.5)
            x.frame = (x.frame+1) % 2
        self._time = 0


































    # HELPER METHODS FOR COLLISION DETECTION
