# DFA minimization in Python

  Python algorithm that get as input a DFA and minimizes it.
  
## The *input file* has the following layout:

list of states

sigma (alphabet)

index of the initial state

list of the final states

state1 symbol state2 (this represents the delta function, from state1 with symbol we get to state2)

## Example of input

``` python
q0 q1 q2 q3 q4 q5
0 1
q0
q5
q0 0 q1
q0 1 q2
q1 0 q0
q1 1 q3
q2 0 q5
q2 1 q4
q3 0 q5
q3 1 q4
q4 0 q4
q4 1 q4
q5 0 q5
q5 1 q4
```

## Example of output

``` python
The minimized automata is: 

States: q0q1, q2q3, q5
Sigma: 0, 1
Initial state: q0q1
Final states: q5
Delta (transition function):
q0q1  --- 0 --->  q0q1
q0q1  --- 1 --->  q2q3
q2q3  --- 0 --->  q5
  q5  --- 0 --->  q5
```
