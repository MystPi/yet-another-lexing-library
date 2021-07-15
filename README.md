# Yet Another Lexing Library
YALL is yet another lexing library for Python, designed for brevity and simplicity. No dependencies required!

## Example
```py
from yall import *

class CalcLexer(Tokenizer):
	# Tokens must be instances of the 't' class or functions decorated with the 'token' decorator.
	PLUS   = t(r'\+')
	MINUS  = t(r'-')
	TIMES  = t(r'\*')
	DIVIDE = t(r'/')
	POW    = t(r'\^')
	EQ     = t(r'=')
	LPAREN = t(r'\(')
	RPAREN = t(r'\)')
	
	# You can provide special tokens in a dictionary or by indexing:
	NAME = t(r'[a-zA-Z_][a-zA-Z0-9_]*', {
		'sin': 'SIN',
		'cos': 'COS',
		'tan': 'TAN'
	})
	
	NAME['asin'] = 'ASIN'
	NAME['acos'] = 'ACOS'
	NAME['atan'] = 'ATAN'
	
	# You can process tokens with functions:
	@token(r'\-?\d*\.\d+')
	def FLOAT(self, s):
		return float(s[0])
		
	@token(r'\-?\d+')
	def INT(self, s):
		return int(s[0])
	
	# To ignore specific characters, just include an 'ignore' variable:
	ignore = r' '
	
	# To ignore spaces AND newlines you would use this regex:
	# ignore = r' |\n'


lexer = CalcLexer()
test = 'x = 2.5 * (5 + 7) + sin 1'
for token in lexer.tokenize(test):
	print(token)
```
