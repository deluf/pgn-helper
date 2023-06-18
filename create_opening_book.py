import os
import sys
import json


# Main menu
MIN_ELO = int(input(' Select the minimum elo of both players > '))
if (MIN_ELO < 0): exit('Elo can\'t be negative')

MAX_MOVES = int(input(' Select the maximum number of moves to pick from each player > '))
if (MAX_MOVES < 0): exit('The number of moves can\'t be negative')
# In any case the maximum number of moves won't exceed the number of moves in the first line of the match

JSON = {}
pgn_files = os.listdir('pgn/')


for index, filename in enumerate(pgn_files):

    pgn_file = open("PGN/" + filename, "r", encoding='utf-8', errors='ignore')
    lines = pgn_file.readlines()

    print(
        'Processing file {index:d} of {total:d}: {filename:s}'
        .format(
            index = index + 1,
            total = len(pgn_files),
            filename = filename
        )
    )

    for i in range (0, len(lines)):

        line = lines[i]


        # Line filtering
        if not line.startswith('[Event'):
            continue


        # Default white elo line number
        white_elo_line = i + 7
        # Confirm it by searching
        for j in range(i, len(lines)):
            if (lines[j].startswith('[WhiteElo')):
                white_elo_line = j
                break

        # Default black elo line number
        black_elo_line = i + 8
        # Confirm it by searching
        for j in range(i, len(lines)):
            if (lines[j].startswith('[BlackElo')):
                black_elo_line = j
                break


        # Elo filtering
        white_elo = lines[white_elo_line][11:15]
        black_elo = lines[black_elo_line][11:15]

        if (
            # White or black elo is missing
            len(white_elo) < 4 or
            len(black_elo) < 4 or

            # White or black elo is three digits (we olny care for high elos)
            white_elo[3] == '"' or
            black_elo[3] == '"' or

            int(white_elo) < MIN_ELO or
            int(black_elo) < MIN_ELO
        ):
            continue


        # Default match start line number
        match_start_line = i + 11
        # Confirm it by searching
        for j in range(i, len(lines)):
            if (lines[j].startswith('1.')):
                match_start_line = j
                break

        # Fetch the first line of moves of the match (excluding \n)
        move_line = lines[match_start_line][:-1].split(' ')

        # If the match ends early, let's say less than 10 moves, then skip it
        if (len(move_line) < 10):
            continue


        # Move filtering
        skip = False
        for j in range(0, len(move_line)):

            # Remove bad moves
            if len(move_line[j]) < 2:
                skip = True
                break

            # Remove move numbers (ex the 1. before 1.e4)
            if move_line[j][0].isdigit():
                move_line[j] = move_line[j][2:]

        if (skip):
            continue


        # Everything is ready to be put into the json file
        move_line = move_line[:MAX_MOVES * 2]

        for i in range(0, min(len(move_line), MAX_MOVES * 2)):

            pointer = JSON

            for j in range(0, i + 1):

                # If the move is already in the json file
                #  then increment its popularity (#)
                if move_line[j] in pointer:
                    pointer = pointer[move_line[j]]
                    pointer['#'] += 1

                # Else create a new entry with popularity 1
                else:
                    pointer[move_line[j]] = {
                        '#': 1
                    }
                    pointer = pointer[move_line[j]]


# Save json file
with open('opening_book.json', 'w') as outfile:
    json.dump(JSON, outfile)
