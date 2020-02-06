

# Complex expression evaluator

This program evaluates arithmetic expressions than could include complex numbers.

## Usage:

    $python complex_expression.py "(25+3i)*(6+6i)"
    Re: 132.0
    Im: 168.0

Accepts pure real number expression with (+,-,*,/):
 
"(1+2)*(3+4)"
 
"(1+(4+5+2)-3)+(6+8)"

"(1+(4+5+2)-3)/(-6+8)"

"1-(6+8)"

"-6+8"

"-(6+8)"

"-(-6+8)-(-4+3)"

"4*-2"
 
Or in combination with complex numbers:

"(-5+23+5+3i+2)*(2+4+2i+2*4i)*2"

"(-5+23+5+3i+2)*(2+4+2i+4i)/(4i+3+2i)"

"(25+3i)*(6+6i)"

"13/2i"

"2i/13"

"(-3 + 3i) /( 8 - 2i)"

"(-3 + 3i) /( -8 - 2i)"

"1 /( 1 + 2i)"

"-   ( -  3 - 3i )"

## How it works
The program first transforms the infix expression to postfix :
"-(-6+8)-(-4+ 3)" ->
"6 n 8 + n 4 n 3 + -"
where 'n' indicates a negation.  After that, the postfix expression is evaluated using a stack.  
To handle the complex number, it transforms the complex number to vectors : 'a+bi' -> '[a,b]' , then [a,b] is handled as a single token. 




Julio C. Rangel

