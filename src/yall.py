class t:
	def __init__(self, regex, special={}):
		self.regex = regex
		self.special = special

	def __setitem__(self, item, value):
		self.special[item] = value


class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __str__(self):
		return f'Token({self.type}, {self.value!r})'

	def __repr__(self):
		return f'Token({self.type}, {self.value!r})'


def token(regex):
	def wrapper(func):
		func.regex = regex
		return func

	return wrapper


class Tokenizer:
	def tokenize(self, string):
		import re

		ret = []
		rest = string
		members = list(self.__class__.__dict__.keys())
		tokens = [i for i in members if i.isupper()]

		while rest:
			matched = False

			for token in tokens:
				regex = eval('self.' + token)

				if type(regex) == t:
					match = re.match(regex.regex, rest)
				elif callable(regex) and hasattr(regex, 'regex'):
					if regex.regex == '':
						raise Warning('Regexes in the \'token\' decorator can\'t be empty!')
					else:
						match = re.match(regex.regex, rest)
				else:
					raise Warning(
						'Tokens must be functions decorated with the \'token\' decorator or instances of the \'t\' class!'
					)

				if match:
					if type(regex) == t:
						res = match[0]
					else:
						try:
							res = regex(match)
						except TypeError:
							raise Warning('Tokens must have 2 arguments, including \'self\'!')

					if res is not None:
						if type(regex) == t and res in regex.special:
							ret.append(Token(regex.special[res], res))
						else:
							ret.append(Token(token, res))
					else:
						ret.append(Token(token, match[0]))

					rest = rest[len(match[0]):]
					matched = True
					continue
			try:
				match = re.match(self.ignore, rest)
				if match:
					rest = rest[len(match[0]):]
					matched = True

			except AttributeError:
				pass

			if not matched:
				try:
					print(self.error(rest))
					rest = rest[1:]
				except AttributeError:
					print(f'Illegal token[s]: {rest}')
					rest = rest[1:]

		return ret
