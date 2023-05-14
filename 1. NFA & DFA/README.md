# NFA & DFA implementation in Python

  Python algorithm that get as input a NFA / DFA and a list of strings and determines if the string is accepted or not. If the string is accepted every path that reaches a final state will be displayed.
  
## How to read the input
The algorithm uses 2 input files, one for the automata and one for the strings.

## The *automata input file* has the following layout:

n (number of states)

sigma (alphabet)

index of the initial state

list of the final states

state1 symbol state2 (this represents the delta function, from state1 with symbol we get to state2)

## The *string input file* has the following layout:

Every string on its own line, and they are inside a set of **" "**

**""** represents λ(lambda), the empty string

## Example of input files

***automata input***

``` python
6
a b
0
5
0 a 1
0 a 2
1 a 3
1 b 1
1 a 4
2 b 1
3 a 5
4 b 3
4 b 5
```

***strings input***

``` python
"abbbaa"
"aaaa"
"aaa"
"abab"
""
```

## Example of output

``` python
String abbbaa is accepted by automata
Roads: 
0 1 1 1 1 3 5
0 2 1 1 1 3 5

String aaaa is not accepted by automata

String aaa is accepted by automata
Roads: 
0 1 3 5

String abab is accepted by automata
Roads: 
0 1 1 4 5
0 2 1 4 5

String λ is not accepted by automata
```
