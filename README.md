# Imatari-Automata
Trying to automate algorithm generation from any source data set to any goal data set

# what is this project?

This a personal project, this idea of automated reasoning has been polluting my mind for a few month now and not finding any problem solver anywhere has been quite a bummer.

So in order to keep my curiosity from overflowing, I am going to try and make my own, anyone is welcome to contribute, this is a research (in the purest meaning) project.

Starting from the basics, we are going to try to find a way to let the machine determine the best way to code an algorithm to solve problems.

We won't use any context limitations, nor any difficulty gfor now, we are at the process of generating working functions.

Then we will try to analyze those functions and the data transformations associated with each operation

Then we will try to find any relation between operation parameter data and the operation resulting data in order to later guide the process of generating code with whole new learned informations

Then we will try to add new concepts like context switching to the algorithm generator.


## The basics

First concepts:

- An algorithm is a sequence of operations on data, which take one or more data structures and results in one or more data structures.
- An operation is any finite process manipulating one or more data structure and resulting in one or more data structures.
- A data structure is a data container containing a specific type of data or data structure, and have its own properties and operations on itself.
- A data is a value of a specified type, it's own properties and operations on itself are determined by it's type.
- A type is either the representation of a specific data structure and its content type, or a specific known data type. It also inherits specific properties and operations on any data of this type.

## Current state

We have successfully parsed a whole lot of python libraries and and python itself for functions and their annotations, fact is, most of those functions are NOT annotated and as such, automated type check should be used to determine their input and output data types.

Sadly we have come to a conclusion which is, if we can totally describe a problem, and its solution , then we can already describe the algorithm to our problem. Automating this process of description will necessitate either using randomness and some kind of optimisation algorithm to check the fit of such generated algorithms. Or an AI system able to visualize and translate data property manipulations into source code and check those results.
