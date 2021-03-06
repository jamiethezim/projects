#!/Users/jamiezimmerman/anaconda/bin/python

#TODO This shebang path MUST be changed before execution
# 1. bash$ which python
# 2. copy the pathname to the first line of this file with proper #!

#-----------------------------------------------------------------------#

#Written by Jamie Zimmerman 3/29/2017
#Backwards compatible for Python 2.6.6 deployment on RHEL server


#Usage: ./check2.py -c [bash command] -o [math operator] -a [amount to operate by]
#Example: ./check2.py -c 'echo SNMP - OK - -98 total power 25 KW' -o '/' -a 10

import argparse
from operator import mul, truediv
#import subprocess
import sys
import re

def check(command, OP, amount):
	ops = {'*': mul, '/': truediv}
	res = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
	#res = "SNMP WARNING - UPS batter Voltage *423*"
	li = re.split("[= ]+", res) #splits by multiple delimiters: =, <space> 
	destarred = False #boolean keeps track of a word having **
	for i in range(len(li)):
		try:
			if li[i].startswith('*') and li[i].endswith('*'):
				li[i] = li[i].strip('*')
				destarred = True
			
			new_value = calculate(float(li[i]), ops[OP], amount)
			
			if destarred:
				li[i] = "*{0:.1f}*".format(new_value)
				destarred = False
			else:
				li[i] = "{0:.1f}".format(new_value)
		except ValueError:
			pass
	# reg ex split function destroys the equals sign critical to the string
	# equal sign necessary on very last number only if there was a bar in the bash command
	if '|' in command:
		i = find(li)
		sub = " ".join(li[0:i]) #join the first section of the string
		sub += "=" #include the lost #
		while i < len(li):
			sub += li[i] #add the rest of the list items
			i += 1
		return sub
	else:
		return " ".join(li)

#----------------------------------------------------------#

#helper function gets the input string - i.e. the result of the bash command piped into this python program
def get_command():
	command = sys.stdin.read().strip()
	return command 


#helper function to calculate new value
def calculate(inp, op, out):
	'''
	inp -> float/int
	op -> mathematical function from operator library
	out -> float/int
	'''
	return op(inp, out)

#helper function finds index of last instance of a number in a list
def find(lis):
	for j in range(len(lis)-1, -1, -1):
		try:
			dummy = float(lis[j])
			return j
		except ValueError:
			pass
	return None


#----------------------------------------------------------#
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='SNMP get string process')
	#parser.add_argument('-c', "--command", type=str, required=True, help='command to run')
	parser.add_argument('-o', "--operation", type=str, required=True, help='operation to perform, ie: "/" to divide or "*" to multiply')
	parser.add_argument('-a', "--amount", type=int, required=True, help='int(amount) to divide/multiply by')
	
	args = parser.parse_args()

	#command = args.command
	operation = args.operation
	amount = args.amount

	res = check(command, operation, amount)
	print(res)
