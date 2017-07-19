'''Defines some additional spice for theia.'''

#Provides:
#   gbeamInit

import sys
import os
import string
import random
import curses

def gbeamInit(menu):
    "Pick in the menu."
    if '--magazzu' in menu:
        magazzu()
    elif '--hang' in menu:
        hang()
    elif '--schiaccia' in menu:
        pong()


# hang function
def hang():
    """The whole hangman game, from welcome to exit."""

    # game data
    wordList = [
    'feeling',
    'sculptor',
    'wonderful',
    'sweetest',
    'hedgerow',
    'hacking',
    'the',
    'art',
    'of',
    'exploitation',
    'python',
    'press',
    'starch',
    'inside',
    'descriptor',
    'overflow',
    'privilege',
    'replace',
    'interferometry',
    'merger',
    'coalescence',
    'gravitation',
    'computing',
    'width',
    'master',
    'slave',
    'difference',
    'flag',
    'c'
    ]

    maxTries = 8
    scoreFile = 'scores'
    newFileString = """# High scores for the hangman game.
    # Have this file in the current directory from which you're playing
    # to have access to the high scores.\n"""

    def listScores():
        """List all the names and scores listed in the high scores file."""
        # Check for scores file
        if not os.path.isfile(scoreFile): # no scores file
            print "There is no high scores file, would you like to create one?",
            ans = raw_input()
            if ans == '' or ans[0] == 'y' or ans[0] == 'Y': # create scores file
                print "Creating scores file."
                newf = open(scoreFile, 'w')
                newf.write(newFileString)
                newf.close()
            else:
                print "Aborting file creation, exiting program."
                raise SystemExit("Exit for refusal of scores file creation.")

        # Print scores
        toPrint = noComment(scoreFile)

        if len(toPrint) == 0:   # no scores yet
            print "There are no scores registered yet."
        else:
            print "Here are the registered players and their scores:\n" + toPrint

    def askName():
        """Get name of player and corresponding score if any."""
        # Get name
        print "What is your name?",
        name = raw_input()
        while True:
            if name == ''  or ' ' in name or name[0] not in string.letters:
                print "%r is not a valid name, " % name,
                print "the name must start with a letter and contain no spaces."
                name = raw_input()
            else:
                break

        # Get score
        print "Looking up your score..."
        allStr = noComment(scoreFile) # string with all names and scores

        if name not in allStr:  # no score for this name
            print "You have no score registered yet! Assigning you a score of 0..."
            return (name, 0, False)
        else:
            # find score as the string between the name and the end of file/\n
            beg = allStr.find(name, 0) + len(name) + 1
            if allStr.find('\n', beg) != -1:
                end = allStr.find('\n', beg)
            else:
                end = len(allStr) -1
        return (name, int(allStr[beg:end]), True)

    def updateScore(name, oldscore, newscore):
        """Update the score of a registered player on the scores file."""
        print "\nUpdating scores file..."
        allStr = noComment(scoreFile) # containing all the non-commented lines

        # replace "name oldscore" by "name newscore" in allStr
        olds = "%s %d" % (name, oldscore)
        news = "%s %d" % (name, newscore)
        allStr = allStr.replace(olds, news, 1)

        # write to file
        with open(scoreFile, 'w') as sf:
            sf.write(newFileString)
            sf.write(allStr)

        print "Wrote your new score to scores file."

    def addScore(name, score):
        """Add a non-registered player and his new score to the scores file."""
        print "\nUpdating scores file..."
        with open(scoreFile, 'a') as sf:
            sf.write("%s %d\n" % (name,score))

        print "Wrote your new score to the scores file."

    def noComment(fileName, exclude = '#'):
        """Return string of all the non-commented lines of the file.

        This raises an IOError if the file is not found.

        """
        allStr = "" # string with all names and scores
        if not os.path.isfile(fileName):
            raise IOError("%r file not found while extracting non-comment lines.")
        else:
            with open(fileName, 'r') as sf:
                for line in sf: # populate string with names and scores
                    if not exclude in line:
                        allStr = allStr + line

        return allStr

    welcome = """
        Welcome to the hangman game.
        Learn your vocabulary and have fun, right from the command line!

        Copyright (C) 2017 R. Duque
        License: GNU GPLv3 <http://gnu.org/licenses/gpl.html>
        This is free software: you are free to change and redistribute it.
        There is NO WARRANTY, to the extent permitted by law.
        For more information, please see the README file.
        """

    goodbye = "\nSee you later!"

    rightLetter = "Congrats, %r is one of the letters of the word!"

    wrongLetter = "Sorry, %r didn't work"

    wholeWord = "Nice! You guessed the whole word %r!"

    def askExit():
        """Ask whether to exit the program or not."""
        print "Would you like to continue playing?",
        ans = raw_input()
        if ans =='' or ans[0] == 'y' or ans[0] == 'Y':
            print "\nGreat! New word please!"
            return False
        else:
            return True

    showTries = "You still have %d tries left."

    scoreLine = "Your current score is %d points."

    wins = "\nBravo! You guessed the word %r in %d tries!"

    loss = "Sorry buddy you have not more tries left, the word was %r."

    def chooseLetter(guessed):
        print "Go ahead, guess a letter or a word!",
        ans = raw_input()

        while True:
            if ans == '' or not set(ans).issubset(set(string.letters)):
                print "%r is not valid input, type in just letters." % ans ,
                ans = raw_input()
                continue

            if ans in guessed:
                print "\nYou already tried %r! Pick another one." % ans ,
                print "These are your previous tries: ",
                for i in guessed:
                    print "%r, " % i,

                ans = raw_input()
                continue

            else:
                break

        return ans

    def printState(word, found):
        """Prints the word with only the found letters."""
        toPrint = ''
        for i in word:
            if i in found:
                toPrint = toPrint + i
            else:
                toPrint = toPrint + '*'

        print "\nHere's the word so far: %s" % toPrint

    rules = """
        This is hangman! I'm going to pick a word and you're going to have %d tries
        to guess the letters in the word. You can also try to guess the entire
        word. Along the way I'll show you the letters you've already tried and the
        letters you've already guessed in the word.
        """ % maxTries

    # welcome
    print welcome
    try:
        listScores()
        # user can exit if he does not create score file in listScores()
    except SystemExit:
        print goodbye
        sys.exit(1)
    # initialize player info: hasName == True if name is registered in scores
    # oldscore = score before game, newscore = score during and after game
    (name, oldscore, hasName) = askName()
    newscore = oldscore
    print rules
    print scoreLine % newscore

    # enter the sequence of games
    while True:
        # choose word for game and initialize tries
        word = random.choice(wordList)
        guessed = set()
        found = set()
        toFind = set(word)
        triesLeft = maxTries
        tries = 0

        # play the actual game with this word
        while triesLeft > 0 and not toFind.issubset(found):
            printState(word, found)
            print showTries % triesLeft
            answer = chooseLetter(guessed)
            guessed.add(answer)
            tries = tries + 1

            if answer == word:
                # found whole word
                found.add(answer)
                print wholeWord % word
                triesLeft = triesLeft - 1
                break

            if answer in word:
                # found one letter of the word
                found.add(answer)
                print rightLetter % answer
            else:
                triesLeft = triesLeft - 1
                print wrongLetter % answer

        # determine how much to add to the score (if any)
        if toFind.issubset(found) or word in found:
            print wins % (word, tries)
            toAdd = len(word) + triesLeft
        else:
            print loss % word
            toAdd = 0

        # update in-game score
        newscore = newscore + toAdd
        print scoreLine % newscore

        if askExit():
            # write new score to file and quit
            if hasName:
                # add score to entry in scores file
                updateScore(name, oldscore, newscore)
            else:
                #append name and score to scores file
                addScore(name, newscore)

            # exit
            print goodbye
            sys.exit(0)

# magazzu function
def magazzu():
    sys.exit(0)

# pong function
def pong():
    HEIGHT = 20
    WIDTH = 60
    TIMEOUT = 50

    class player(object):
        def __init__(self, name, body, keyup, keydown, side):
            self.name = name
            self.hit_score = 0
            self.keyup = keyup
            self.keydown = keydown
            self.body = body
            self.side = side
            if side == 'left':
                self.bounce = [[coord[0], coord[1]+1] for coord in self.body]
            if side == 'right':
                self.bounce = [[coord[0], coord[1]-1] for coord in self.body]
            for part in self.body:
                win.addch(part[0], part[1], '|')

        @property
        def score(self):
            return ' {}: {} '.format(self.name, self.hit_score)

        def make_a_point(self):
            self.hit_score += 1

        def update_bounce(self):
            if self.side == 'left':
                self.bounce = [[coord[0], coord[1]+1] for coord in self.body]
            if self.side == 'right':
                self.bounce = [[coord[0], coord[1]-1] for coord in self.body]
            for part in self.body:
                win.addch(part[0], part[1], '|')

        def go_up(self):
            win.addch(self.body[-1][0], self.body[-1][1], ' ')
            del self.body[-1]
            self.body.insert(0, [self.body[0][0]-1, self.body[-1][1]])
            self.update_bounce()
            win.addch(self.body[0][0], self.body[0][1], '|')

        def go_down(self):
            win.addch(self.body[0][0], self.body[0][1], ' ')
            del self.body[0]
            self.body.insert(len(self.body), [self.body[-1][0]+1, self.body[-1][1]])
            self.update_bounce()
            win.addch(self.body[-1][0], self.body[-1][1], '|')

    class ball(object):
        def __init__(self, dir=-1, coef=0):
            self.position = [HEIGHT/2, WIDTH/2]
            self.dir = dir
            self.coef = coef
            win.addch(self.position[0], self.position[1], 'o')

        def bounce(self, where):
            #control if len(player)%2 = 0 or 1
            if where == 0:
                self.coef -= 1
            elif where == 2:
                self.coef += 1
            self.dir *= -1

        def bounce_segment(self):
            self.coef *= -1

        def reset(self, position=[HEIGHT/2, WIDTH/2], dir=-1, coef=0):
            self.position = position
            self.dir = dir
            self.coef = coef
    print('---------------------------')
    print('Welcome to PONG multiplayer')
    print('---------------------------')
    name1 = raw_input('player left name: ')
    print('Do not use the following key(s): ESC, SPACE, p, n')
    keyup1 = ord('{}'.format(raw_input('{} key up: '.format(name1))))
    keydown1 = ord('{}'.format(raw_input('{} key down: '.format(name1))))

    name2 = raw_input('player right name: ')
    print('Do not use the following key(s): ESC, SPACE, p, n')
    keyup2 = ord('{}'.format(raw_input('{} key up: '.format(name2))))
    keydown2 = ord('{}'.format(raw_input('{} key down: '.format(name2))))

    curses.initscr()
    win = curses.newwin(HEIGHT, WIDTH, 0, 0) #y,x coordiates
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)
    win.timeout(TIMEOUT)

    #name1 = 'player1'
    score1 = 0
    body1 = [[HEIGHT/2-1, 1], [HEIGHT/2, 1], [HEIGHT/2+1, 1]]
    player1 = player(name1, body1, keyup1, keydown1, 'left')

    score2 = 0
    body2 = [[HEIGHT/2-1,WIDTH-2], [HEIGHT/2,WIDTH-2], [HEIGHT/2+1,WIDTH-2]]
    player2 = player(name2, body2, keyup2, keydown2, 'right')

    ball = ball()

    score_max = 3
    new_round_message = 'press SPACE bar for another round'
    new_round_message_erase = '                                 '
    end_message = '  THE END\n  - ESC to quit\n  - n bar for another game'
    key = 0
    point = False

    while key != 27: # While Esc key is not pressed
        win.border(0)
        win.addstr(0, 3, ' {}'.format(player1.score))
        win.addstr(0, WIDTH/2 - 4, ' PONG ')
        win.addstr(0, WIDTH-15, '{}'.format(player2.score))
        win.addstr(HEIGHT-1, WIDTH/2-12, ' ESC (quit), p (pause) ')

        event = win.getch()
        key = event

        if player1.hit_score == score_max-1:
            winer = player1
            looser = player2
            winer_message = '{} has defeated {} {}-{}'.format(winer.name, looser.name,
                                                    winer.hit_score+1, looser.hit_score)
        elif player2.hit_score == score_max-1:
            winer = player2
            looser = player1
            winer_message = '{} has defeated {} {}-{}'.format(winer.name, looser.name,
                                                    winer.hit_score+1, looser.hit_score)

    # pause mode
        prevKey = key
        event = win.getch()
        key = key if event == -1 else event

        if key == ord('p'):
            key = -1
            while key != ord('p'):
                key = win.getch()
            key = prevKey
            continue

    # move the players
        if key == player1.keyup:
            if player1.body[0][0] == 1 :
                continue
            else:
                player1.go_up()
        if key == player1.keydown:
            if player1.body[2][0] == HEIGHT-2 :
                continue
            else:
                player1.go_down()
        if key == player2.keyup:
            if player2.body[0][0] == 1 :
                continue
            else:
                player2.go_up()
        if key == player2.keydown:
            if player2.body[2][0] == HEIGHT-2 :
                continue
            else:
                player2.go_down()

    # move the ball
        if ball.position in player1.bounce:
            ball.bounce(player1.bounce.index(ball.position))
        elif ball.position in player2.bounce:
            ball.bounce(player2.bounce.index(ball.position))
        elif ball.position[0] == 1 or ball.position[0] == HEIGHT-2:
            ball.bounce_segment()

        if ball.position[1] == WIDTH-2 and ball.position not in player2.body:
            if player1.hit_score < score_max -1:
                win.addstr(3, 10, new_round_message)
            else:
                win.addstr(3, 10, end_message)
                win.addstr(7, 3, winer_message)

            player1.make_a_point()
            old = [ball.position[0], ball.position[1]]
            ball.reset()
            point = True

        elif ball.position[1] == 1 and ball.position not in player1.body:
            if player2.hit_score < score_max -1:
                win.addstr(3, 10, new_round_message)
            else:
                win.addstr(3, 10, end_message)
                win.addstr(7, 3, winer_message)

            player2.make_a_point()
            old = [ball.position[0], ball.position[1]]
            ball.reset()
            point = True

        if point:
            if key == ord(' '):
                win.addch(old[0], old[1], ' ')
                win.addstr(3,10, new_round_message_erase)
                point = False
            elif key == ord('n'):
                win.addch(old[0], old[1], ' ')
                win.addstr(3, 2, '                       ')
                win.addstr(4, 2, '                       ')
                win.addstr(5, 2, '                         ')
                win.addstr(7, 2, '                                         ')
                player1.hit_score = 0
                player2.hit_score = 0
                point = False
            else:
                continue
        else:
            win.addch(ball.position[0], ball.position[1], ' ')
            ball.position = [ball.position[0]+ball.coef, ball.position[1]+ball.dir]
            if ball.position[0] < 1 :
                ball.position[0] = 1
            elif ball.position[0] > HEIGHT-2:
                ball.position[0] = HEIGHT-2
            win.addch(ball.position[0], ball.position[1], 'o')

    curses.endwin()
    print('---------------------------')
    print('End game')
    print(winer_message)
    sys.exit(0)
