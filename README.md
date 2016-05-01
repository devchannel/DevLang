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
    + `|int|x` Declaration of a variable (`x`), which is an integer.
    + `|int|f => |int|x ->` Declaration of a function (`f`). `f` returns an integer, which is specified in `|int|f`, and takes one parameter (`x`) which is an integer as well (`|int|x`). A `->` will always be followed by a block of code.
- **First class functions.** Functions can be used in a similar way as other data types. They can be passed as arguments to other functions and functions can be returned from functions.
    + `(|int| => |int| |int|)g => (|int|h => |int| |int|) ->` A function(`g`) that requires a function, that requires integers as arguments andFINISH 
