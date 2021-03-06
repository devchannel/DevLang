##Under construction:

This document is incomplete, the most up to date version can be viewed [here](https://docs.google.com/document/d/1Wgv1mFhS7QLXeMiKywPW4d4QxSMqi6jdzJfKoCRohWg/edit?usp=sharing).


#DevLang

DevLang is a pure functional programming language written in Python created by the DevChannel slack team with the goal of implementing a full fledged compiler. In contrast to functional programming languages such as Haskell, DevLang code is written in an imperative style while keeping the foundations of a functional programming language.

##Language Specification

###Data types:

####Support for:

* Char
* 32-bit Integer
* 64-bit Integer
* String
* Float
* Boolean

###Features:

- **Statically typed.** All functions, parameters and variable declarations require to be annotated with types.
    + `//` is used for comments.
    + `|int|x` Declaration of a variable (`x`), which is an integer.
    + `|int|f => |int|x ->` Declaration of a function (`f`). `f` returns an integer, which is specified in `|int|f`, and takes one parameter (`x`) which is an integer as well (`|int|x`). A `->` will always be followed by a block of code.
- **First class functions.** Functions can be used in a similar way as other data types. They can be passed as arguments to other functions and functions can be returned from functions.
    + `(|int| => |int| |int|)g => (|int|h => |int| |int|) ->` A function(`g`) that requires a function (`h`) - that requires integers as arguments and returns an integer - as an argument and returns a function of the type integer.
- **Record types.** Our construct for grouping data.

        Person : {
            |string|name = "John"; //Default value
            |int|age = 20;
        };


        //Can be used like this:

        Person "John1" 19;
        Person _ 19; //Underscore means to use the default value
        Person _ _;

        |Person|p = Person "John1" 19;
        |p| == |Person|; //You can ask what the type of a variable is by using |var|
- **Immutable.** There is no changing of state. All variables are declared as constant.

        |int|x = 5;
        x = 7 //A new variable named *x* is declared. It is, however, referred to as 'x' and therefore shadows the former declaration of *x*


        //These are equivalent, but in the former declaration we infer the type of *x*:

        |int|x = 5
        |int|x = 7

- **Looping.** While a given for any imperative programming language, that does not have to be the case for a functional programming language. We allow for both *for* and *while* loops.


## Contributing
First off, a warning. This code has been said to cause PTSD and major headaches. Make sure to have some water and painkillers nearby while reading. 

Currently, we target only LLVM, being able to target other languages would be nice. We hope to target C in the future, and any help upon that would be appreciated.

The code is also written by us amateur compiler developers, and it's pretty bad. Help on improving it, removing redundant code, making it readable, and anything like that would also be appreciated. Just submit an issue, and ask to work on it. 
