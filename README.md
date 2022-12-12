# Lambda Calculus Interpreter

>Lambda calculus is a formal system in mathematical logic for expressing computation based on function abstraction and application using variable binding and substitution. - [Wikipedia](https://en.wikipedia.org/wiki/Lambda_calculus)



## Running the interpreter

#### <span>LambdaLexer.py</span>

- Rules to tokenize the input expression

#### <span>LambdaParser.py</span>

- Matches the input expression with the allowed expressions. Checks for syntax errors.

#### <span>main.py</span>

- Takes input from the command line
- Calculates free variables
- Calculates alpha equivalence and beta reduction
- Evaluates expression

Run <span>main.py</span> from terminal using 
```console
python main.py
```
