# AI Squid Game: Trap! (Fall 2021)

The final coding challenge for COMS W4701 - Artificial Intelligence, Columbia University.

Written by: Tom Cohen, 

Professor : Ansaf Salleb-Aouissi

## Outline (for internal use)

* Description and hyping of Game (Rules, ..)
* Coding (Minimax Algorithm, Alpha-Beta Pruning)
* Restrictions
* Logistics
* Grading
* Q&A
* Resources


## Description

In this project, we will use Adverserial AI to defeat the opponent at our newly-invented game, Trap!

Imagine the following scenario: you are a rebelling contestant and your opponent is one of the captors, whose identity is unknown! 
In order to find out who's standing behind Squid Game, you want to capture them *alive*! Likewise, they are interested in capturing you alive to find who's behind the rebellion. When you both realize your intentions are the same, you agree to make it into a mind game - and let the smarter player win. 
Your task in this game is thus twofold: Trap the opponent, and don't get trapped!

### Organization
The game is organized as a two-player game on a 7x7 board space. Every turn, a player first **moves** and then **throws a trap** somewhere on the board. 

![organization](https://user-images.githubusercontent.com/55168908/142587004-8a5af0d4-6a1d-4bad-b5a3-cd21f51cab7b.png | width = 100)


### Movement: 

Each turn, a player can move one step in any possible direction, diagonals included (e.g., like King in chess), *so long as there is no trap placed in that cell*

no traps             |  with traps
:-------------------------:|:-------------------------:
![image](https://user-images.githubusercontent.com/55168908/142576384-3e3c6bec-9915-43ee-9b14-28c75e82ebc4.png)  |  ![image](https://user-images.githubusercontent.com/55168908/142577318-33321ee1-2afe-432f-ad75-967f89442ae7.png)


### Throwing a Trap:

Unlike movement, a trap can be thrown to *anywhere in the board*. 

**However,** sadly, we are not on the olympic throwing team, and our aiming abilities deteriorate with distance, such that there is an increasing chance the trap will land on any of its neighboring cells. In fact, the chance *p* that it will land precisely on the cell we want is given as: 

![image](https://user-images.githubusercontent.com/55168908/142582036-d19b98ad-56e0-404a-8d07-cca66f4f54a7.png). 

![image](https://user-images.githubusercontent.com/55168908/142582525-4f5b2170-a177-4233-80c4-755542f69893.png)

The *n* surrounding cells divide the remainder equally between them, that is: 

![image](https://user-images.githubusercontent.com/55168908/142585339-93cddc84-ba13-4880-88b3-8070e772a46a.png)

![image](https://user-images.githubusercontent.com/55168908/142583267-3231710e-d3ad-40c6-8452-0f38da4e324c.png)



Example:

Target             |  Probabilities of trap placement
:-------------------------:|:-------------------------:
![trap1](https://user-images.githubusercontent.com/55168908/142584513-d4e70925-a2ad-436d-895c-e4cac90fbbcf.png)| ![trap2](https://user-images.githubusercontent.com/55168908/142584586-d40bca87-99e7-4b12-b761-2f3eb83190d5.png)




### Game Over?

To win, you must "Trap" you opponent so that they could not possibly move in any direction, while you still can! Examples:

Example 1 (Win)             |  Example 2 (Loss)
:-------------------------:|:-------------------------:
![win1](https://user-images.githubusercontent.com/55168908/142578872-d27ef016-a3e7-427b-8e33-26f84b2172f0.png) | ![lose1](https://user-images.githubusercontent.com/55168908/142579019-c88b20a1-876e-427c-9f24-b79bbba5f9ff.png)


In example 1: the player can still move down or right, whereas the opponent has no valid moves.

In example 2: the player cannot move but the opponent still has a diagnoal move. 


## What to Code

Two thoughtful actions are performed at each turn: One to maximize the chance of survival (moving), and the other to maximize the chance of winning the game (Trapping). So accordingly, we have two different Adversarial Search problems to compute at each turn!

### The Search Algorithm
For **each** of the search problems, you will have to implement an **Expecti-Minimax with Alpha-Beta Pruning** (if necessary, revisit our lecture on Adversarial Search).

### Expecti-What-Now?
Expectiminimax (indeed a mouthful) is a simple extension of the minimax algorithm! So think about how to implement minimax first. As we saw in the simple case of tic-tac-toe, it is useful to employ the minimax algorithm assuming the opponent is a perfect "minimizing" agent. In practice, an algorithm with the perfect opponent assumption deviates from reality when playing a sub-par opponent making silly moves, but still leads to the desired outcome of never losing. If the
deviation goes the other way, however, (a "maximax" opponent in which the opponent wants us to win), winning is obviously not guaranteed.



Minimax             |  ExpectiMinimax
:-------------------------:|:-------------------------:
![image](https://user-images.githubusercontent.com/55168908/142586538-292bed18-7ec9-437a-82fd-175d05ec8414.png)| ![image](https://user-images.githubusercontent.com/55168908/142586645-553af6e3-e420-4220-a241-56df3691c3b1.png)



