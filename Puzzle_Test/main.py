# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from puzzle import Puzzle

photo = 'image.png'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    puzzle = Puzzle(photo)

    puzzle.show('shuffled')
