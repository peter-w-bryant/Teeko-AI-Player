# Teeko-AI-Player

## Description
A program that allows a user to play against my Teeko AI player.

## What is Teeko?
Teeko is a game played between two players, each of which with 4 red or black pieces, on a 5x5 board. At the start of the game, the player with black pieces always starts, and then each player takes turns placing their pieces until all pieces have been placed on the board - I will refer to this initial sequence of dropping pieces as the <b>drop phase</b>. The <b>goal</b> of the game is for one player to get four pieces in a row either horizontally, vertically, diagonally, or in a 2x2 box (in the example below, black wins).

<p align="center">
  <img src="https://github.com/peter-w-bryant/Teeko-AI-Player/blob/main/images/board.png?raw=true" alt="Sublime's custom image"/>
</p>

If after the <b>drop phase</b> neither player has won, each player continues taking turns by moving one piece to an adjacent space at a time. To be clear, by adjacent I mean that a player can move their piece either one space up, down, left, right, or to any diagonal such that the space they are moving to is not yet occupied. It should be mentioned that my program does not support the ability to wrap around the board, meaning if your piece was on the bottom right corner of the board and you tried to move the piece to the right, it would be marked as an invalid move instead of moving all the way to the bottom left corner.

## Functions

There are several functions defined in this program that ensure that the Teeko game remains valid (i.e. all rules are followed). I have ommited these functions from this write-up, and have instead opted to just describe the functions that allow my AI player to make decisions about where to move their pieces.

My <b>make_move(self, state)</b> contains all the logic that allows my AI player to choose their move. This function can be broken down into the following components:

<ol> 
  <li>Generates a subtree of depth <i>d</i> under the current state.</li>
  <li>Uses a heuristic scoring function to evaluate the "leaves" at depth <i>d</i>, and propagates these scores back up to the current state.</li>
  <li>Selects and returns the best possible next move using the <b>minimax</b> algorithm.</li>
</ol>

### Helper Functions

The following helper functions are implemented and called in the <b>make_move(self, state)</b> function:

<ul>
  <li><b>succ(self, state)</b></li>
  <li><b>game_value(self, state)</b></li>
  <li><b>heuristic_game_value(self, state)</b></li>
</ul>
