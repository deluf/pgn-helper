# PGN Mentor downloader


## About
PGN Mentor downloader is a collection of python scripts to easily download and process pgn files hosted on  <a href="https://www.pgnmentor.com/files.html">PGN Mentor</a>.

### Fetch files
With the <a href="fetch_files.py">fetch_files.py</a> script you can easily bulk-download all the pgn files from one of the three  categories in which the website organizes them: by player, by opening, or by event.

### Create opening book
Once downloaded, you can process the pgn files as you want; for example, the <a href="create_opening_book.py">create_opening_book.py</a> script creates a json file which represents the tree of all the first  <em>n</em> moves played in every match of each pgn file by players which elo is greater than <em>x</em>, where <em>n</em> and <em>x</em> are parameters of the script.

For instance, here is how a json opening book generated with 2500+ players and 2 moves by the script looks like (# is the popularity of the move, that is the number of times the move has been played):
```
{
  "e4": {
    "#": 478088,
    "e5": {
      "#": 118698,
      "Nf3": {
        "#": 74146,
        "Nf6": {
          "#": 4778
        },
        "Nc6": {
          "#": 31850
        },
        "d6": {
          "#": 445
        }
      },
    ...
    }
  ...
  }
...
}
```
Remember that you can, and should, minify the json file to save some space!


I also made a few opening books, each one with 2500+ players but different number of moves, so that you can directly download them.

## Setup
The only dependency is beautifulsoup4: ```pip install beautifulsoup4```
