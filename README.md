# primedice-simulator
A simulation to test different PrimeDice auto-bet settings.  The 
simulator outputs results in the form of graphs such as the one below.

![Sample Graph](/docs/primedice_example_graph.png)
  
***Dependencies:***

* matplotlib
* numpy 
* python 3  

PrimeDice is an online bitcoin gambling website in which you can choose
different values, such as your initial bet amount, the amount of "risk" 
you want to take, and the amount that you increase your bet after every
loss. The site then has an auto-bet setting where the computer will make
rolls over and over until either the user decides to stop or the user 
goes bankrupt.
  
Of course, the question every gambler wants the answer to is "What is 
the best gambling strategy?" So this program simulates several rounds 
with a given setting and records how long it takes for the player to go 
bankrupt each time. The output is then the average of those several 
simulations, and it gives a good idea of roughly how long you would 
have until you go bankrupt.
  
One interesting aspect to point out is that, as many millions of 
simulations I have run, the player has always gone bankrupt eventually. 
I think that says a thing or two about the nature of gambling.
