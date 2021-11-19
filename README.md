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


## 1. Description

In this project, we will use Adverserial AI to defeat the opponent at our newly-invented game, Trap!

Imagine the following scenario: you are a rebelling contestant and your opponent is one of the captors, whose identity is unknown! 
In order to find out who's standing behind Squid Game, you want to capture them *alive*! Likewise, they are interested in capturing you alive to find who's behind the rebellion. When you both realize your intentions are the same, you agree to make it into a mind game - and let the smarter player win. 
Your task in this game is thus twofold: Trap the opponent, and don't get trapped!

### 1.1 Organization
The game is organized as a two-player game on a 7x7 board space. Every turn, a player first **moves** and then **throws a trap** somewhere on the board. 

<img src="https://user-images.githubusercontent.com/55168908/142587004-8a5af0d4-6a1d-4bad-b5a3-cd21f51cab7b.png" height="400"/>


### 1.2 Movement

Each turn, a player can move one step in any possible direction, diagonals included (e.g., like King in chess), *so long as there is no trap placed in that cell and that it is within the borders of the grid*

no traps             |  with traps
:-------------------------:|:-------------------------:
![image](https://user-images.githubusercontent.com/55168908/142576384-3e3c6bec-9915-43ee-9b14-28c75e82ebc4.png)  |  ![image](https://user-images.githubusercontent.com/55168908/142577318-33321ee1-2afe-432f-ad75-967f89442ae7.png)


### 1.3 Throwing a Trap

Unlike movement, a trap can be thrown to *anywhere in the board*, with the exception of the opponents location - again, we want them alive! - and the player's location. Note that throwing a trap on top of another trap is possible but useless.

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


### 1.4 Game Over?

To win, you must "Trap" you opponent so that they could not possibly move in any direction, while you still can! Examples:

Example 1 (Win)             |  Example 2 (Loss)
:-------------------------:|:-------------------------:
![win1](https://user-images.githubusercontent.com/55168908/142578872-d27ef016-a3e7-427b-8e33-26f84b2172f0.png) | ![lose1](https://user-images.githubusercontent.com/55168908/142579019-c88b20a1-876e-427c-9f24-b79bbba5f9ff.png)


In example 1: the player can still move down or right, whereas the opponent has no valid moves.

In example 2: the player cannot move but the opponent still has a diagnoal move. 


## 2. What to Code

Two thoughtful actions are performed at each turn: One to maximize the chance of survival (moving), and the other to maximize the chance of winning the game (Trapping). So accordingly, we have two different Adversarial Search problems to compute at each turn!

### 2.1 The Search Algorithm
For **each** of the search problems, you will have to implement the ExpectiMinimax algorithm with Alpha-Beta Pruning!

### 2.2 Expecti--What Now?
Expectiminimax (indeed a mouthful) is a simple extension of the famous Minimax algorithm that we covered in class (Adversarial Search lecture)! 
The only difference is that in the expectiminimax, we introduce an intermediate **Chance Node** that accounts for chance and uncertainty. As we have previously established, throwing the trap is not always accurate, so we have to take into account potential consequences as we navigate the game. The modification is demonstrated in the comparison below:


Minimax             |  ExpectiMinimax
:-------------------------:|:-------------------------:
<img width="347" alt="minimax" src="https://user-images.githubusercontent.com/55168908/142590520-a3e29401-726a-4585-9579-c1dd47aee108.png">| <img width="431" alt="expecti" src="https://user-images.githubusercontent.com/55168908/142590403-aec560c3-1ede-4b49-81f4-57942bbbd990.png">

As you can see, you are now trying to maximize the opponents moves, given the *chance* of them happening. For example, if we are to throw a trap and want to maximize our chance of winning, our tree will have a chance node with value *p* as well as *n* nodes with values *(1-p)/n* (see equations in 1.3: Throwing a Trap).
The rest is the same! 

Note that the player is now maximizing their *Expected Utility* in every move (if that sounds not-necessarily-optimal to you, you aren't wrong!).

### Heuristics!

Since the Search Space here is HUGE! 

### Hmm that's a lot. Where Do We Start?

Fear not! Here's a very good recipe:

1. Start with implementing a simple minimax. Observe improvements.
2. Add Alpha-beta pruning. Observe improvements.
3. Extend minimax to Expectiminimax by introducing the Chance node

## Grading

The competition is designed so that **all groups will be able to get a good grade regardless of their placement in the competition**. We will test your code against players of three difficulty levels: Easy, Medium, and Hard (still very doable as long as you implement everything). 
* Grading & Logistics
* Q&A
* Resources

