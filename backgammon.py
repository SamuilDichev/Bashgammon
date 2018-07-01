from board import Board
import random
import re
import sys

# todo: jail rolls
# todo: can't split dice rolls
# todo: make sure the "done" thing works
exitTerms = ("quit", "exit", "bye", "q")


def main():
  b = Board()
  # ntro = open('readme.txt', 'r')

  SIDE = True  # True if X, false if O
  # for line in intro:
  #   print(line)
  print("What do you want to play? Type 'pc' for Player vs. Computer or 'pp' for Player vs. Player")

  line = input()
  # if line == 'pc':
  #   print("I haven't done this yet!")
  # else:
  while (line not in exitTerms and (b.xFree < 15 or b.oFree < 15)):
    print(b)
    turnComplete = False
    (roll1, roll2, total) = roll()

    if SIDE:
      print("X, what do you want to do?")
    else:
      print("O, what do you want to do?")

    while (not turnComplete and line not in exitTerms and total > 0):
      line = input()
      position, steps = parseMove(line)

      # Done with move
      if (position == 100 and steps == 100):
        total = 0
        break

      jailFreed = False
      jailCase = False

      if ((SIDE and b.xJail > 0) or (not SIDE and b.oJail > 0)):
        jailCase = True

      if (steps != roll1 and steps != roll2 and steps != total and not jailCase):
        print("You didn't roll that!")
        continue

      # If X turn and in JAIL
      position = position
      if (steps == 0 and SIDE and b.xJail > 0):
        tempSteps = 25 - position
        if (tempSteps != roll1 and tempSteps != roll2):
          print("You didn't roll that!")
          continue
        else:
          jailFreed = True

      # If O turn and in JAIL
      elif (steps == 0 and not SIDE and b.oJail > 0):
        tempSteps = position
        if (tempSteps != roll1 and tempSteps != roll2):
          print("You didn't roll that!")
          continue
        else:
          jailFreed = True

      if (position < 1 or position > 24 or steps < 0):
        print("That move is not allowed.  Please try again.")
        continue

      move, response = b.makeMove(position - 1, SIDE, steps)
      print(response)

      if (move and jailFreed):
        steps = tempSteps
      if move:
        total = total - steps
        print(b)
        print("You have " + str(total) + " steps left.")
    SIDE = not SIDE  # TODO: Include error management


def roll():
  roll1 = random.randint(1, 6)
  roll2 = random.randint(1, 6)
  total = roll1 + roll2
  if (roll1 == roll2):
    total *= 2

  print("You rolled a " + str(roll1) + " and a " + str(roll2) + " giving you a total of " + str(total) + " moves.")
  return roll1, roll2, total


def parseMove(input):
  if input in ['d', 'f', 'done', 'finish']:
    return (100, 100)
  if input in exitTerms:
    exit(0)

  (position, steps) = re.split('[,\s]', input)
  return (int(position), int(steps))


if __name__ == "__main__":
  main()
