# Ganit (गणित)
Ganit(गणित) means calculation in Sanskrit. As the name suggests, this is a calculation utility. This is a parser library implemented in python. The library takes as argument an expression, either infix or postfix and evaluates the expression and returns the result. It supports all major mathematical functions.

The evaluator can take variable as argument. Evaluation of expression like `x^2 + y^3` is possible with this library. It can also take expression as variable. Or in other words, nested expression like `cos(x^2+y^2)^2 + sin(x^2+y^2)^2` is also possible. Or even evaluation of nested expression like `cos(y); y = sin(theta); theta=acos(sin(x)); x = 45` is possible, it actually evaluates `cos(sin(acos(sin(45))))` in this case. It starts from the innermost expression and gradually evaluates the outermost.

Apart from evaluating the expression, parser can return prescanned expression. A prescanned expression is the one which converts an expression and changing multiple occurences of +/-. e.g. `-2` will be converted to `0-2` and `--2` to `0+2` or `---2` to `-2` and so on. Similar changes occur for multiple occurences of `+` as well.

The parser can also return the postfix expression of a given infix expression. e.g. `2 * 4` will be returned as `2 4 *`.

## Usage
### Download Source Code
The source code can be downloaded and the parser can be called directly in program.
```python
# import the library and the main parser module
from ganit.parser import Parser
# Create an object of the parser
p = Parser()
print(p.prescan("2 * 4")) # It will print '2*4'
print(p.convert("2 * 4")) # It will print '2 4 *'
# Evaluate the expression
print(p.evaluate("2*4")) # It will print '8'
```
### pip install --> Planned
Incomplete, need to complete

## Evaluation
The library can be used for 3 different tasks -
* Prescanning of Expression
* Conversion of Infix to Postfix
* Evaluation of Infix/Postfix expression

The library gives 5 predefined variables -
* e - Euler's Number
* pi - π
* tau - τ, the circle constant equal to 2*π, the ratio of a circle’s circumference to its radius.
* True - boolean True value to work with logic expressions
* False - boolean False value to work with logic expressions
### Prescanning of Expression
In infix expression, if expression is not properly embraced, finding the difference between negation and subtraction is difficult during infix to postfix conversion. So, before processing an infix notation, the library checks for occurence and minu/plus signs and tries to find what purpose the sign is used for.
Below are some examples -
* '-2' is changed to '0-2'
* '--2' is changed to '0+2'
* '---2' is changed to '0-2'
* '(-2)' is changed to '(0-2)'
* '4*-7' is changed to '4*(0-7)'
Similar logic is also applied for multiple occurences of '+'. Please check the 'Test' section for more details.

The argument of prescan is the expression to be evaluated. A 'dict' object can also be passed as argument, which has a key "exp".

This method does not check for validity of the expression. e.g. If you pass an expression with a variable and the variable is not passed, the method still succeeds and returns a changed expression.
```python
from ganit.parser import Parser
p = Parser()
print(p.prescan("2 * 4")) # It will print '2*4'
d = {"exp": "2 * x"}
print(p.prescan(d)) # It will print "2*x"
print(p.prescan(2)) # It will print "2"
print(p.prescan(3.14)) # It will print "3.14"
```

### Conversion of Infix to Postfix
Before evaluating any expression, parser converts any infix notation to postfix notation, thus making the processing easier.

The convert method has 2 arguments -
1. The required exp argument, which can be either a 'str' or a 'dict' object containing "exp" and "variables" as keys or an 'int' or 'float' object.
1. If the first argument is 'str', a 'dict' object with all the variables as keys can be passed to it. If the first object is 'dict' object, the second argument is ignored.

This method checks the validity of the passed expression.

```python
from ganit.parser import Parser
p = Parser()
# Convert only numeric or predefined variables like e, pi and tau
print(p.convert("2 * 4")) # It will print '2 4 *'
d = {"exp": "2*x", "variables": {"x":2}}
print(p.convert(d)) # It will print '2 x *'
print(p.convert(d, {"y": 2})) # It will print '2 x *'
d = {"exp": "2*x", "variables": {"y":2}}
print(p.convert(d)) # It will throw error as the variable 'x' is not passed as variable
print(p.convert(d, {"x": 2})) # It will also throw an error, as the first object is of type dict, so second argument is ignored.
print(p.convert("2*x", {"x": 2})) # It will print '2 x *'
print(p.convert(2)) # It will print '2'
print(p.convert(2, {"x": 2})) # It will print '2'. The second argument is ignored.
print(p.convert("2 * pi")) # It will print '2 pi *'
```

### Evaluation of Infix/Postfix expression
The actual evaluation happens here.

The evaluate method has 3 arguments -
1. The required exp argument, which can be either a 'str' or a 'dict' object containing "exp", "variables", "convert" as keys or an 'int' or 'float' object.
1. The second argument is a bool value. This determines if the expression needs to be first converted to a postfix nontation or not. If an postfix notation is passed, this variable can be passed as False. The default value is True. If the first argument is of type 'dict', this value is ignored, even if passed.
1. If the first argument is 'str', a 'dict' object with all the variables as keys can be passed to it. If the first object is 'dict' object, this argument is ignored.

This method checks the validity of the passed expression first, then proceeds with evaluation. If postfix notation is wrong, it does not perform any calculations.

Evaluation can be done in nested fashion. So, an expression can contain a variable which in turn is another expression and the pattern go infinitely. Evaluation can also be done for a postfix notation.

```python
from ganit.parser import Parser
p = Parser()
print(p.evaluate("2 * 4")) # It will print '8'
print(p.evaluate("2 * x")) # It will throw error
print(p.evaluate("2 * x", {"x": 2})) # It will print 4
print(p.evaluate("2 x *", False, {"x": 2})) # It will print 4
# Nested Expression
d = {"exp": "2 * x", "variables": { "x": {"exp": "2*y", "variables": {"y": 3}} }}
p.evaluate(d) # it will print '12'
# Nested postfix expression
d = {"exp": "2 * x", "variables": { "x": {"exp": "2 y *", "convert": False, "variables": {"y": 3}} }}
p.evaluate(d) # it will also print '12'
```

## Suppported functions
### Arithmatic expressions
1. `+` : Addition. Takes two operands. Having precedence 2.
1. `-` : Subtraction. Takes two operands. Having precedence 2.
1. `*` : Multiplication.Takes two operands. Having precedence 3.
1. `/` : Division.Takes two operands. Having precedence 3.
1. `%` : Modulus.Takes two operands. Having precedence 3.
1. `^` : Power.Takes two operands. Having precedence 4.
### Algebric Expression
1. `abs` : This is a function and takes only a parameter. It returns the absolute value of the parameter passed.
Incomplete --> Please check the Test Section for a complete understanding of supported functionality.
### Trigonometric
Incomplete --> Please check the Test Section for a complete understanding of supported functionality.
### Logical expressions
1. `? :` : Ternary expression, this works pretty much like `if else` statement. If there is no need of an `else` statement, the `:` operation can be removed. But the `:` operation can only be used with `?`. So, any expression containing `:` but not containing `?` will throw an error. The use of this expression is as follows -
```
<Condition>?<Statement to be evaluated if condition is True>:<Statement to be evaluated if condition is False>
```
Or, you can remove the else part by removing :
```
<Condition>?<Statement to be evaluated if condition is True>
```
But the following will cause an error.
```
:<Statement>
```
1. `>`: Greater than. Takes two arguments. Having a lower precedence than Addition/Subtraction
1. `<`: Less than. Takes two arguments. Having a lower precedence than Addition/Subtraction
### Matrix Manipulation
Planned feature to be added in future
### Calculus
Planned feature to be added in future

## Todo
- [ ] Need to create pip package
- [ ] Need to complete the documentation of supported functions
- [ ] Need to add support for Matrix Manipulation
- [ ] Need to add support for vector mathematics
- [ ] Need to add support for calculus
- [ ] Need to make an AST which can make it portable to any language.
- [ ] Need to write the AST and Ganit can be used on that platform (shell script, .net script (dll), Java, JavaScript etc.)
- [ ] May be port this library to npm, maven etc.

## Test
The following tests were performed on the parser. As and when new functions are added, this list gets bigger.

Sl. No. | Original Exprression | Variables| Prescanned exprression | Postfix exprression | Postfix Result
------- | -------------------- | -------- | -----------------------| ------------------- | --------------
1 | - | No Variable | "Expresssion Error: ends with an operator - '-'" | "Expresssion Error: ends with an operator - '-'" | "Expresssion Error: ends with an operator - '-'"
2 | -2 | No Variable | -2 | -2 | -2
3 | -9*-4 | No Variable | 0-9*(0-4) | 0 9 0 4 - * -  | 36
4 | -2--7 | No Variable | 0-2+7 | 0 2 - 7 +  | 5
5 | 2+-7 | No Variable | 2+(0-7) | 2 0 7 - +  | -5
6 | -(2*7*-7)-8 | No Variable | 0-(2*7*(0-7))-8 | 0 2 7 * 0 7 - * - 8 -  | 90
7 | -(2*7*-7)*-8 | No Variable | 0-(2*7*(0-7))*(0-8) | 0 2 7 * 0 7 - *  0 8 - * -  | -784
8 | -(2*7*-7)*(-8) | No Variable | 0-(2*7*(0-7))*(0-8) | 0 2 7 * 0 7 - *  0 8 - * -  | -784
9 | -(2*7*-7)*cos(-8) | No Variable | 0-(2*7*(0-7))*cos(0-8) | 0 2 7 * 0 7 - * 0 8 - cos * -  | -14.259003313244127
10 | -(2*7*(-7))*cos(-8) | No Variable | 0-(2*7*(0-7))*cos(0-8) | 0 2 7 * 0 7 - * 0 8 - cos * -  | -14.259003313244127
11 | -(2*7*(-7))*atan(-8) | No Variable | 0-(2*7*(0-7))*atan(0-8) | 0 2 7 * 0 7 - * 0 8 - atan * -  | -141.75125056031723
12 | -(2 + 7) | No Variable | 0-(2+7) | 0 2 7 + -  | -9
13 | 4 * -8 | No Variable | 4*(0-8) | 4 0 8 - *  | -32
14 |  4*  - 8  | No Variable | 4*(0-8) | 4 0 8 - *  | -32
15 |  2 *(-4 +8) | No Variable | 2*(0-4+8) | 2 0 4 - 8 + *  | 8
16 | 1-4 | No Variable | 1-4 | 1 4 -  | -3
17 | 1 - 4  | No Variable | 1-4 | 1 4 -  | -3
18 |  4*8 - 2 | No Variable | 4*8-2 | 4 8 * 2 -  | 30
19 |  4 -  +2 | No Variable | 4-2 | 4 2 -  | 2
20 |  4 +  -2 | No Variable | 4+(0-2) | 4 0 2 - +  | 2
21 | +++++ | No Variable |  | 'Invalid Expression: ' | 'Invalid Expression: '
22 | ------ | No Variable | "Expresssion Error: ends with an operator - '------'" | "Expresssion Error: ends with an operator - '------'" | "Expresssion Error: ends with an operator - '------'"
23 | + | No Variable |  | 'Invalid Expression: ' | 'Invalid Expression: '
24 | +2 | No Variable | +2 | +2 | +2
25 | +9*+4 | No Variable | 9*4 | 9 4 *  | 36
26 | +2-+7 | No Variable | 2-7 | 2 7 -  | -5
27 | 2++7 | No Variable | 2+7 | 2 7 +  | 9
28 | +(2*7*+7)+8 | No Variable | (2*7*7)+8 |  2 7 * 7 * 8 +  | 106
29 | +(2*7*+7)*+8 | No Variable | (2*7*7)*8 |  2 7 * 7 * 8 *  | 784
30 | +(2*7*+7)*(+8) | No Variable | (2*7*7)*(8) |  2 7 * 7 *  8 *  | 784
31 | +(2*7*+7)*cos(+8) | No Variable | (2*7*7)*cos(8) |  2 7 * 7 * 8 cos *  | -14.259003313244127
32 | +(2*7*(+7))*cos(+8) | No Variable | (2*7*(7))*cos(8) |  2 7 * 7 * 8 cos *  | -14.259003313244127
33 | +(2*7*(+7))*atan(+8) | No Variable | (2*7*(7))*atan(8) |  2 7 * 7 * 8 atan *  | 141.75125056031723
34 | +(2 + 7) | No Variable | (2+7) |  2 7 +   | 9
35 | 4 * +8 | No Variable | 4*8 | 4 8 *  | 32
36 |  4*  + 8  | No Variable | 4*8 | 4 8 *  | 32
37 |  2 *(+4 +8) | No Variable | 2*(4+8) | 2 4 8 + *  | 24
38 | 1+4 | No Variable | 1+4 | 1 4 +  | 5
39 | 1 + 4  | No Variable | 1+4 | 1 4 +  | 5
40 |  4*8 + 2 | No Variable | 4*8+2 | 4 8 * 2 +  | 34
41 |  4 +  +2 | No Variable | 4+2 | 4 2 +  | 6
42 | 4+log(5) | No Variable | 4+log(5) | 4 5 log +  | 4.698970004336019
43 |  | No Variable |  | 'Invalid Expression: ' | 'Invalid Expression: '
44 | 2+3-4/5*9 | No Variable | 2+3-4/5*9 | 2 3 + 4 5 / 9 * -  | -2.2
45 | 2+3*log(9)- | No Variable | "Expresssion Error: ends with an operator - '2+3*log(9)-'" | "Expresssion Error: ends with an operator - '2+3*log(9)-'" | "Expresssion Error: ends with an operator - '2+3*log(9)-'"
46 | 2*x-t*y | {'x': 1, 't': 1} | 2*x-t*y | 'Invalid input y' | 'Invalid input y'
47 | 2*x-t*y | {'x': 1, 't': 1, 'y': 1} | 2*x-t*y | 2 x * t y * -  | 1
48 | 2*4-3 | No Variable | 2*4-3 | 2 4 * 3 -  | 5
49 | cos(5) | No Variable | cos(5) | 5 cos  | 0.28366218546322625
50 | 2.445*4-3.9*log(5, 10) | No Variable | 2.445*4-3.9*log(5,10) | 2.445 4 * 3.9 5 10  log * -  | 'Invalid Postfix Notation: Stack not 1'
51 | 2*4-3*log(5, 10) | No Variable | 2*4-3*log(5,10) | 2 4 * 3 5 10  log * -  | 'Invalid Postfix Notation: Stack not 1'
52 | ((((ln(1)+2)*3)-cos((sqrt(4)+5)))+(sqrt(ln((6*4)))+4)) | No Variable | ((((ln(1)+2)*3)-cos((sqrt(4)+5)))+(sqrt(ln((6*4)))+4)) |   1 ln 2 + 3 *  4 sqrt 5 +  cos -  6 4 *  ln sqrt 4 + +   | 11.028807433280551
53 | 2*3-2*8*5/2%3*abs(-4) | No Variable | 2*3-2*8*5/2%3*abs(0-4) | 2 3 * 2 8 * 5 * 2 / 3 % 0 4 - abs * -  | 2
54 | 2*3-2*8*5/2%3*abs(-4)*ceil(2) | No Variable | 2*3-2*8*5/2%3*abs(0-4)*ceil(2) | 2 3 * 2 8 * 5 * 2 / 3 % 0 4 - abs * 2 ceil * -  | -2
55 | 2*3-2*8*5/2%3*abs(-4)*ceil(2)*factorial(2) | No Variable | 2*3-2*8*5/2%3*abs(0-4)*ceil(2)*factorial(2) | 2 3 * 2 8 * 5 * 2 / 3 % 0 4 - abs * 2 ceil * 2 factorial * -  | -10
56 | factorial(2)*2*3-2*8*5/2%3*abs(-4)*ceil(2) | No Variable | factorial(2)*2*3-2*8*5/2%3*abs(0-4)*ceil(2) | 2 factorial 2 * 3 * 2 8 * 5 * 2 / 3 % 0 4 - abs * 2 ceil * -  | 4
57 | 2*3-2*8*5/2%3*abs(-4)*ceil(2.8)*factorial(2) | No Variable | 2*3-2*8*5/2%3*abs(0-4)*ceil(2.8)*factorial(2) | 2 3 * 2 8 * 5 * 2 / 3 % 0 4 - abs * 2.8 ceil * 2 factorial * -  | -18
58 | 2*3-2*8*5/2%3*abs(-4)*ceil(2.8)*factorial(2)*gcd(5,15) | No Variable | 2*3-2*8*5/2%3*abs(0-4)*ceil(2.8)*factorial(2)*gcd(5,15) | 2 3 * 2 8 * 5 * 2 / 3 % 0 4 - abs * 2.8 ceil * 2 factorial * 5 15  gcd * -  | -114
59 | 2*3-2*8*5/2%3*abs(-4)*ceil(2.8)*factorial(2)*gcd(5.2,15) | No Variable | 2*3-2*8*5/2%3*abs(0-4)*ceil(2.8)*factorial(2)*gcd(5.2,15) | 2 3 * 2 8 * 5 * 2 / 3 % 0 4 - abs * 2.8 ceil * 2 factorial * 5.2 15  gcd * -  | 'Value Error: 15.0 , 5.2. GCD can only be determined for integers.'
60 | 2*3-2*8*5/2%3*abs(-4)*ceil(2.8)*factorial(1.2)*gcd(5,15) | No Variable | 2*3-2*8*5/2%3*abs(0-4)*ceil(2.8)*factorial(1.2)*gcd(5,15) | 2 3 * 2 8 * 5 * 2 / 3 % 0 4 - abs * 2.8 ceil * 1.2 factorial * 5 15  gcd * -  | 'Value Error: 1.2. Factorial calculation can only be done for integers.'
61 | 2*3-2*8*5/2*exp(2) | No Variable | 2*3-2*8*5/2*exp(2) | 2 3 * 2 8 * 5 * 2 / 2 exp * -  | -289.56224395722603
62 | 2*pow(2,3) | No Variable | 2*pow(2,3) | 2 2 3  pow *  | 16
63 | 2*pow(2,3)*sqrt(4) | No Variable | 2*pow(2,3)*sqrt(4) | 2 2 3  pow * 4 sqrt *  | 32
64 | 2*pow(2,3)*log(1000) | No Variable | 2*pow(2,3)*log(1000) | 2 2 3  pow * 1000 log *  | 48
65 | 2*pow(2,3)*log2(16) | No Variable | 2*pow(2,3)*log2(16) | 2 2 3  pow * 16 log2 *  | 64
66 | 2*pow(2,3)*Log(16, 2) | No Variable | 2*pow(2,3)*Log(16,2) | 2 2 3  pow * 16 2  Log *  | 64
67 | 2*pow(2,3)*ln(e^2) | No Variable | 2*pow(2,3)*ln(e^2) | 2 2 3  pow * e 2 ^ ln *  | 32
68 | -(2*7*-7)*sin(-8) | No Variable | 0-(2*7*(0-7))*sin(0-8) | 0 2 7 * 0 7 - * 0 8 - sin * -  | -96.95710816909141
69 | -(2*7*-7)*tan(-8) | No Variable | 0-(2*7*(0-7))*tan(0-8) | 0 2 7 * 0 7 - * 0 8 - tan * -  | 666.3717226115972
70 | -(2*7*-7)*sinh(-8) | No Variable | 0-(2*7*(0-7))*sinh(0-8) | 0 2 7 * 0 7 - * 0 8 - sinh * -  | -146066.92492737592
71 | -(2*7*-7)*cosh(-8) | No Variable | 0-(2*7*(0-7))*cosh(0-8) | 0 2 7 * 0 7 - * 0 8 - cosh * -  | 146066.95780271344
72 | -(2*7*-7)*tanh(-8) | No Variable | 0-(2*7*(0-7))*tanh(0-8) | 0 2 7 * 0 7 - * 0 8 - tanh * -  | -97.99997794310823
73 | -(2*7*-7)*atan(-8) | No Variable | 0-(2*7*(0-7))*atan(0-8) | 0 2 7 * 0 7 - * 0 8 - atan * -  | -141.75125056031723
74 | -(2*7*-7)*asin(-8) | No Variable | 0-(2*7*(0-7))*asin(0-8) | 0 2 7 * 0 7 - * 0 8 - asin * -  | math domain error
75 | -(2*7*-7)*acos(-8) | No Variable | 0-(2*7*(0-7))*acos(0-8) | 0 2 7 * 0 7 - * 0 8 - acos * -  | math domain error
76 | -(2*7*-7)*asin(-.8) | No Variable | 0-(2*7*(0-7))*asin(0-.8) | 0 2 7 * 0 7 - * 0 .8 - asin * -  | -90.874931364158
77 | -(2*7*-7)*acos(-.8) | No Variable | 0-(2*7*(0-7))*acos(0-.8) | 0 2 7 * 0 7 - * 0 .8 - acos * -  | 244.81297139005787
78 | -(2*7*-7)*atanh(-8) | No Variable | 0-(2*7*(0-7))*atanh(0-8) | 0 2 7 * 0 7 - * 0 8 - atanh * -  | math domain error
79 | -(2*7*-7)*asinh(-8) | No Variable | 0-(2*7*(0-7))*asinh(0-8) | 0 2 7 * 0 7 - * 0 8 - asinh * -  | -272.09428351092436
80 | -(2*7*-7)*acosh(-8) | No Variable | 0-(2*7*(0-7))*acosh(0-8) | 0 2 7 * 0 7 - * 0 8 - acosh * -  | math domain error
81 | hypot(4,3) | No Variable | hypot(4,3) | 4 3  hypot  | 5
82 | deg(pi/3) | No Variable | deg(pi/3) | pi 3 / deg  | 59.99999999999999
83 | rad(60) | No Variable | rad(60) | 60 rad  | 1.0471975511965976
84 | t y * | {'x': 1, 't': 1, 'y': 1} | "Expresssion Error: ends with an operator - 'ty*'" | "Expresssion Error: ends with an operator - 'ty*'" | 1
85 | t y * | {'x': 1, 'y': 1} | "Expresssion Error: ends with an operator - 'ty*'" | "Expresssion Error: ends with an operator - 'ty*'" | 'Unknown Symbol in expression: t'
86 | 3 t y * | {'t': 1, 'y': 1} | "Expresssion Error: ends with an operator - '3ty*'" | "Expresssion Error: ends with an operator - '3ty*'" | 'Invalid Postfix Notation: Stack not 1'
87 |  y     * | {'t': 1, 'y': 1} | "Expresssion Error: ends with an operator - 'y*'" | "Expresssion Error: ends with an operator - 'y*'" | 'Invalid Postfix Notation: Causes Stack Underflow -  y     *'
88 | -2 | No Variable | -2 | -2 | -2
89 | --2 | No Variable | 0+2 | 0 2 +  | 2
90 | ---2 | No Variable | 0-2 | 0 2 -  | -2
91 | ----2 | No Variable | 0+2 | 0 2 +  | 2
92 | -----2 | No Variable | 0-2 | 0 2 -  | -2
93 | ++2 | No Variable | 2 | 2 | 2
94 | +++2 | No Variable | 2 | 2 | 2
95 | ++++2 | No Variable | 2 | 2 | 2
96 | --++2 | No Variable | 0+2 | 0 2 +  | 2
97 | ++-2 | No Variable | (0-2) |  0 2 -   | -2
98 | ++++----2 | No Variable | (0+2) |  0 2 +   | 2
99 | ++++-----2 | No Variable | (0-2) |  0 2 -   | -2
100 | -(2*7*-7)*cos(---8) | No Variable | 0-(2*7*(0-7))*cos(0-8) | 0 2 7 * 0 7 - * 0 8 - cos * -  | -14.259003313244127
101 | -(2*7*-7)*cos(----8) | No Variable | 0-(2*7*(0-7))*cos(0+8) | 0 2 7 * 0 7 - * 0 8 + cos * -  | -14.259003313244127
102 | -(2*7*--7)*cos(--8) | No Variable | 0-(2*7*(0+7))*cos(0+8) | 0 2 7 * 0 7 + * 0 8 + cos * -  | 14.259003313244127
103 | -(2*7*---7)*cos(---8) | No Variable | 0-(2*7*(0-7))*cos(0-8) | 0 2 7 * 0 7 - * 0 8 - cos * -  | -14.259003313244127
104 | -(2*7*----7)*cos(----8) | No Variable | 0-(2*7*(0+7))*cos(0+8) | 0 2 7 * 0 7 + * 0 8 + cos * -  | 14.259003313244127
105 | -(2*7*-----7)*cos(----8) | No Variable | 0-(2*7*(0-7))*cos(0+8) | 0 2 7 * 0 7 - * 0 8 + cos * -  | -14.259003313244127
106 | sin(cos(45)) | No Variable | sin(cos(45)) | 45 cos sin  | 0.5014916033198201
107 | deg(asin(cos(45))) | No Variable | deg(asin(cos(45))) | 45 cos asin deg  | 31.68992191129556
108 | deg(asin(cos(rad(45)))) | No Variable | deg(asin(cos(rad(45)))) | 45 rad cos asin deg  | 45.00000000000001
109 | deg(acos(cos(rad(hypot(4, 3))))) | No Variable | deg(acos(cos(rad(hypot(4,3))))) | 4 3  hypot rad cos acos deg  | 4.999999999999992
110 | deg(acos(cos(rad(hypot(4, 3)))))+ y     *x^t | {'x': 4, 't': 16, 'y': 9} | deg(acos(cos(rad(hypot(4,3)))))+y*x^t | 4 3  hypot rad cos acos deg y x t ^ * +  | 38654705669
111 | atan(deg(acos(cos(rad(hypot(4, 3)))))+ y     *x^t) | {'x': 4, 't': 16, 'y': 9} | atan(deg(acos(cos(rad(hypot(4,3)))))+y*x^t) | 4 3  hypot rad cos acos deg y x t ^ * + atan  | 1.5707963267690266
112 | atan(deg(acos(cos(rad(hypot(4, 3)))))+ y     *x^t) | {'x': '2*4 - 3', 't': 16, 'y': 9} | atan(deg(acos(cos(rad(hypot(4,3)))))+y*x^t) | 4 3  hypot rad cos acos deg y x t ^ * + atan  | 1.5707963267941685
113 | hypot(x^2*4, y*t) | {'x': '2*4 - 3', 't': 6, 'y': '5*0.6'} | hypot(x^2*4,y*t) | x 2 ^ 4 * y t *  hypot  | 101.6070863670443
114 | hypot(x^2*4, y*t) | {'x': '2*m - 3', 't': 6, 'y': '5*0.6'} | hypot(x^2*4,y*t) | x 2 ^ 4 * y t *  hypot  | 'Invalid input m'
115 | hypot(x+y*t,x*y) | {'x': '6', 't': 6, 'y': '5*0.6'} | hypot(x+y*t,x*y) | x y t * + x y *  hypot  | 30
116 | hypot(x+y*t,x*y) | {'x': '4', 't': 6, 'y': '5*0.6'} | hypot(x+y*t,x*y) | x y t * + x y *  hypot  | 25.059928172283335
117 | hypot(x+y*t,x*y) | {'x': '5*5', 't': 6, 'y': {'variables': {'a': 9, 'b': 10}, 'exp': 'a + b'}} | hypot(x+y*t,x*y) | x y t * + x y *  hypot  | 494.92019558712695
118 | x | {'x': {'variables': {'x': '2*4 - 3', 't': 16, 'y': 9}, 'exp': 'atan(deg(acos(cos(rad(hypot(4, 3)))))+ y     *x^t)', 'convert': True}} | x | x  | 1.5707963267941685
119 | x*y + z^2 | {'x': 2, 'y': {'variables': {'x': {'variables': {'y': 1}, 'exp': '2*y'}, 'y': {'variables': {'x': {'variables': {'theta': {'variables': {'y': {'variables': {'x': {'variables': {'x': '2*4 - 3', 't': 16, 'y': 9}, 'exp': 'atan(deg(acos(cos(rad(hypot(4, 3)))))+ y     *x^t)', 'convert': True}}, 'exp': 'x'}, 'z': 'e'}, 'exp': 'log(9*y) - 2*cos(z)+ln(e^2)'}}, 'exp': '(sin(theta))^2 + (cos(theta))^2'}}, 'exp': '2*x'}}, 'exp': 'x + y'}, 'z': '5*0.5'} | x*y+z^2 | x y * z 2 ^ +  | 14.25
120 | x | {'x': {'variables': {'y': {'variables': {'z': 3}, 'exp': 'z'}}, 'exp': 'y'}} | x | x  | 3
121 | 14.25 | No Variable | 14.25 | 14.25 | 14.25
122 | 14 | No Variable | 14 | 14 | 14
123 | x + y | {'x': {'variables': {'y': {'exp': 23}}, 'exp': 'y'}, 'y': {'exp': 25}} | x+y | x y +  | 48
124 | cos(x^2 + y^2)^2 + sin(x^2 + y^2)^2 | {'x': 30, 'y': 20} | cos(x^2+y^2)^2+sin(x^2+y^2)^2 | x 2 ^ y 2 ^ + cos 2 ^ x 2 ^ y 2 ^ + sin 2 ^ +  | 1
125 | cos(y) | {'y': {'exp': 'sin(theta)', 'variables': {'theta': {'exp': 'acos(sin(x))', 'variables': {'x': 45}}}}} | cos(y) | y cos  | 0.8651625117859165
126 | 2*4-3<5*2+4?4:3 | No Variable | 2*4-3<5*2+4?4:3 | 2 4 * 3 - 5 2 * 4 + < 4 ? 3 :  | 4
127 | True?4:5 | No Variable | True?4:5 | True 4 ? 5 :  | 4
128 | False?4:5 | No Variable | False?4:5 | False 4 ? 5 :  | 5
129 | 2*4?4:5 | No Variable | 2*4?4:5 | 2 4 * 4 ? 5 :  | '?: only works for boolean condition'
130 | {'variables': {'theta': 30}, 'exp': 'sin(theta)^2+cos(theta)^2<0'} | {'theta': 30} | sin(theta)^2+cos(theta)^2<0 | theta sin 2 ^ theta cos 2 ^ + 0 <  | False
131 | 2*4-3<5*2+4?4*4^2:2*4-5*3 | No Variable | 2*4-3<5*2+4?4*4^2:2*4-5*3 | 2 4 * 3 - 5 2 * 4 + < 4 4 2 ^ * ? 2 4 * 5 3 * - :  | 64
132 | 2*4-3<5*2+4?4*4^2 | No Variable | 2*4-3<5*2+4?4*4^2 | 2 4 * 3 - 5 2 * 4 + < 4 4 2 ^ * ?  | 64
133 | :4*2+5 | No Variable | :4*2+5 |  4 2 * 5 + :  | 'Invalid Postfix Notation: Causes Stack Underflow -  4 2 * 5 + : '
134 | 4*3:4*2+5 | No Variable | 4*3:4*2+5 | 4 3 * 4 2 * 5 + :  | ': only works with ? operator'
