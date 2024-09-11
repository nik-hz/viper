# Proposal for viper programming language project for COMS 4115

## Team Members
- Angel Leyi Cui
- Nikolaus Holzer

## Work division
- Adding static types
- Adding brackets

## Weekly meeting
- Tuesday after class

## Introduction
The goal of the language is to improve on python by fix two issues that many people coming from languages like C and Java have with python. Dynamic typing and whitespace based syntax. We aim to achieve for python what Typescript does for Javascript. Viper should provide a python like experience, work with all python libraries, yet support static typing and use a bracket and semicolon based syntax structure.

We aim for our language to have a very flat learning curve for experienced python users; viper preserves the general user friendliness of python whilst adding features that many find useful in larger applications. To maintain the feel of python, viper is a superset of python so that all valid python code is also valid viper code allowing for easy integration into existing projects. 


## Motivation

## Language and compiler description
Viper is a superset of python. This means that similar to ts projects, viper projects can be compiled to python code. Viper is structured with the same data types as python but adds new syntax and static typing. We choose not to add new types to viper to maintain the python feel of the language.

Our compiler should support compiling viper to python, c or machine code directly. Since we want viper users to be able to use their favorite python libraries in their viper projects we propose two possible methods for this to work. One is to provide a type declaration file for the libraries being used, the other is to have the compiler fetch the dynamic types from the libraries themselves at compile time and use these to verify the viper code. Alternatively we may include a keyword in viper that allows us to ignore the type for library functions when they are used.


## Code example
This example demonstrates a recursive function that calculates the factorial of a number in Viper. 

``` python
# very similar syntax with only minimal changes
def int factorial(int n) {
    if (n == 0) {
        return 1;
    }
    return n * factorial(n - 1);
}

int n = 5;
print(f"factorial of {n} is {factorial(n)}")
```