# Teeko-AI-Player

## Description
A program that allows a user to play against my Teeko AI player.

## What is Teeko?
Teeko is a game played between two players, each of which with 4 red or black pieces, on a 5x5 board. At the start of the game, the player with black pieces always starts, and then each player takes turns placing their pieces until all pieces have been placed on the board - I will refer to this initial sequence of dropping pieces as the <b>drop phase</b>. The <b>goal</b> of the game is for <u>one player to get four pieces in a row either horizontally, vertically, diagonally, or in a 2x2 box</u> (in the example below, black wins). <u>this is underlined text in HTML or markdown, which accepts HTML</u>

<p align="center">
  <img src="https://github.com/peter-w-bryant/Teeko-AI-Player/blob/main/images/board.png?raw=true" alt="Sublime's custom image"/>
</p>

If after the <b>drop phase</b> neither player has won, each player continues taking turns by moving one piece to an adjacent space at a time. To be clear, by adjacent I mean that a player can move their piece either one space up, down, left right, or to any diagonoal such that the space they are moving to is not yet occupied.
