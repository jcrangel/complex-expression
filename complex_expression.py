"""
Complex expression evaluator. 

This program evaluate arithmetic expressions than could include complex numbers 

Julio C. Rangel

"""

import sys

DEBUG=False

class Stack:
	def __init__(self):
		self.array = []

	def empty(self):
		return len(self.array) == 0

	def pop(self):
		if not self.empty():
			return self.array.pop()
		else:

			return 'EOF'

	def push(self,data):
		self.array.append(data)

	def top(self):
		if not self.empty():
			return self.array[-1]
		else:
			return 'EOF'	



# Class to handle the complex expressions 	
class ComplexExpression: 
	
	# Constructor to initialize the class variables 
	def __init__(self, exp=''): 
		self.capacity = len(exp) 
		# This array is used a stack 
		# Precedence setting 
		self.level_precedence = {'n':3,'^':3,'*':2,'/':2,'-':1,'+':1 }
		self.exp = exp.replace(" ","") 
	

		#is not a number
	# def isOperand(self, c): 
	# 	return c.isalpha() or c.isdigit()
	def isOperator(self, ch): 
		return ch in '/*^+-'
	
	def isPartNumber(self,c):
		return c.isdigit() or c == '.'

	# Check if the precedence of operator is less than top of stack  
	def opPrecedenceIsLess(self, ch,stack): 
		try: 
			a = self.level_precedence[ch] 
			b = self.level_precedence[stack.top()] 
			return True if a <= b else False
		except KeyError: 
			return False
	def readWholeNumber(self, i_pos,exp):
		i = i_pos
		str_num =''
		# import pdb; pdb.set_trace()
		while i < len(exp) and (exp[i].isdigit() or exp[i] == '.' or exp[i]=='i'):
			str_num += exp[i]
			i += 1
		return i,str_num
	def isfloat(self,value):
		try:
			float(value)
			return True
		except ValueError:
			return False

	#check if value has the form ai		
	def isComplex(self,value): 
		try:
			return value[-1] == 'i'
		except IndexError:
			print('empty:',value)
			return False
	
	# check form [a,b]
	def isComplexVec(self,value):
		return value[0]=='['

	#get imaginary part from number ai
	def getIm(self,value):
		return value[:-1]

	#get the real and imaginary part from [re,im] or a, bi 
	def getReIm(self,a):
		if a[0] == '[':
			[re,im] = a[1:-1].split(',')
		elif self.isfloat(a):
			re,im = a,0
		elif self.isComplex(a):
			re,im = 0,self.getIm(a)

		return re,im
	#divide (a+bi)/(c+di)	
	def complexDiv(self,a,b,c,d):
		a,b,c,d = float(a),float(b),float(c),float(d)
		re = (a*c + b*d)/(c*c + d*d)
		im = (b*c - a*d)/(c*c + d*d)

		return re, im
	#return [a,b]	
	def makeComplexVec(self,a,b):
		return '['+str(a)+','+str(b)+']'

	# The main function that converts given infix expression 
	# to postfix expression 
	def infixToPostfix(self):
		exp = self.exp[:] 
		stack = Stack()
		output = []
		# Iterate over the expression for conversion
		import pdb; 
		i = 0
		while i < len(exp):
			# pdb.set_trace()
			ch = exp[i]
			# Letters
			# pdb.set_trace()
			if ch == 'i': 
				output.append('1i') 

			# Case -(a + b) -> 0 a b + - start expression,
			#Case "4*−2" - > 4 0 2 - * 
			#Case 2*(−x+y)    →   2 0 x - y + *
			# still using binary operator
			elif ch == '-' and (i == 0 or self.isOperator(exp[i-1]) or (exp[i-1] == '(')):
				stack.push('n')				
				# output.append('0')

			#Numbers
			elif ch.isdigit():
				# output.append(ch)
				i, whole_num = self.readWholeNumber(i,exp)
				output.append(whole_num)
				continue # i has been update 
			
			# If the character is an '(', push it to stack 
			elif ch == '(': 
				stack.push(ch) 

			# If ')', pop and output from the stack until and '(' is found 
			elif ch == ')': 
				while stack.top() != '(' and (not stack.empty()) : 
					output.append(stack.pop()) 
				if stack.top() != '(' and (not stack.empty()): 
					return -1
				else: 
					stack.pop() 

			# Operator found
			else: 
				while not stack.empty() and self.opPrecedenceIsLess(ch,stack): 
					output.append(stack.pop()) 
				stack.push(ch) 
			i += 1

		# pop all the operators
		while not stack.empty(): 
			output.append(stack.pop()) 
		
		return " ".join(output) 
	def evalBinaryExpression(self,a,b,op):
		import pdb
		res = ''
		# a b 
		# pdb.set_trace()
		if self.isfloat(a) and self.isfloat(b):
			to_eval = b + op + a
			res = str(eval(to_eval))
			if DEBUG: print(b,a,op,'=',res)
			return res
		elif op in '+-': ##addition cases
			# b ai op = [b,a]
			if self.isComplex(a) and self.isfloat(b):
				# pdb.set_trace()
				im = self.getIm(a)
				res = '['+b+','+str(eval(op+im))+']'
			# a bi + = [a,b]
			elif self.isComplex(b) and self.isfloat(a):
				im = self.getIm(b)
				res = '['+a+','+im+']'
			#case [re,im] b op = [re+b,im]
			elif self.isComplexVec(a) and self.isfloat(b):
				re,im = self.getReIm(a)
				res = '['+str(eval(b + op + re))+','+im+']'
			#case a [re,im] op = [a op re,im]
			elif self.isComplexVec(b) and self.isfloat(a):
				re,im = self.getReIm(b)
				res = '['+str(eval(re + op + a))+','+im+']'
			# case ai [re,im] op = [re,a + im]
			elif self.isComplex(a) and self.isComplexVec(b):
				im1 = self.getIm(a)
				re2,im2 = self.getReIm(b)
				res = '['+re2+','+str(eval(im1 + op + im2))+']'
			# case [re,im] ai op = [re,a + im]	
			elif self.isComplexVec(a) and self.isComplex(b):
				im1 = self.getIm(b)
				re2,im2 = self.getReIm(a)
				res = '['+re2+','+str(eval(im1 + op + im2))+']'
		elif op == '*':
			# pdb.set_trace()
			# ai b * = abi
			if self.isComplex(a) and self.isfloat(b):
				im = self.getIm(a)
				res = str(eval(im + op + b))+'i'
			# a bi * = abi
			elif self.isComplex(b) and self.isfloat(a):
				im = self.getIm(b)
				res = str(eval(im + op + a))+'i'
			#case [re,im] b * = [re*b,im*b]

			elif self.isComplexVec(a) and self.isfloat(b):
				re,im = self.getReIm(a)
				res = '['+str(eval(re + op + b))+','+str(eval(im + op + b))+']'
			#case a [re,im] * = [re*a,im*a]
			elif self.isComplexVec(b) and self.isfloat(a):
				re,im = self.getReIm(b)
				res = '['+str(eval(re + op + a))+','+str(eval(im + op + a))+']'
			#case [a,b] [c,d] *
			elif self.isComplexVec(a) and self.isComplexVec(b):
				re1,im1 = self.getReIm(a)
				re1,im1 = float(re1),float(im1)
				re2,im2 = self.getReIm(b)
				re2,im2 = float(re2),float(im2)
				res = '['+str(re1*re2 - im1*im2)+','+str(re1*im2 + im1*re2)+']'
		elif op == '/':

			re1,im1 = self.getReIm(b)
			re2,im2 = self.getReIm(a)
			re,im = self.complexDiv(re1,im1,re2,im2)
			res = self.makeComplexVec(re,im)

		else: 
			res = b +' '+ a +' ' +op
		if DEBUG: print(b,a,op,'=',res)
		return res
	def evalNegation(self,a,op):
		res =''
		if self.isfloat(a):
			res = str(-float(a))
		elif self.isComplexVec(a):
			re,im = self.getReIm(a)
			res = self.makeComplexVec(-float(re),-float(im))

		if DEBUG: print(a,op,'=',res)
		return res
	#Evaluate + - 
	def evaluate(self):
		import pdb
		exp = self.infixToPostfix() 
		stack = Stack()
		# pdb.set_trace()
		# Iterate over each token
		for token in exp.split(): 

			if self.isfloat(token):
				stack.push(token) 

			elif self.isComplex(token):
				stack.push(token) 
			
			#negation
			elif token == 'n':  
				a = stack.pop()
				res = self.evalNegation(a,token)
				stack.push(res)
				# stack.push(str(eval('-' + a))) 
			#binary operator
			else: 
				a = stack.pop() 
				b = stack.pop() 
				res = self.evalBinaryExpression(a,b,token)
				stack.push(res) 
			
		result = stack.pop() 
		return self.getReIm(result) 

exp = sys.argv[1]
# print(exp,"=")
expression = ComplexExpression(exp)
expression.infixToPostfix()
re, im = expression.evaluate()
print('Re:',re,'\nIm:',im)

# exp = "a+b*(c^d-e)^(f+g*h)-i"
# obj = ComplexExpression(exp) 
# print(obj.infixToPostfix()) 

# exp = "(a+i)*(2+i)"
# exp = "(1+2)*(3+4)"
# exp ="(1+(4+5+2)-3)+(6+8)"
# exp ="(1+(4+5+2)-3)/(-6+8)"
# exp = "1-(6+8)"
# exp = "-6+8"
# exp = "-(6+8)"
# exp = "-(-6+8)-(-4+3)"
# exp = "4*-2"
# exp = "(-5+23+5+3i+2)*(2+4+2i+2*4i)*2"
# exp ='(-5+23+5+3i+2)*(2+4+2i+4i)/(4i+3+2i)'
# exp = '(25+3i)*(6+6i)'
# exp = '13/2i'
# exp = '2i/13'
# exp = '(-3 + 3i) /( 8 - 2i)'
# exp = '(-3 + 3i) /( -8 - 2i)'
# exp = '1 /( 1 + 2i)'
# # exp = '-   ( -  3 - 3i )'
# print(exp)
# expression = ComplexExpression(exp)
# print(expression.infixToPostfix())
# print(expression.evaluate())
# print("----------")


