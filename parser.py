import functions
attrib_declaration_keywords = ["loc"]
attribute_objects = ["CHECKPOINT", "ENEMY", "BORDER", "RECT"]

def remove_comments(line):
	#remove comments tabs and spaces
	line = line.split('#', 1)[0]
	line = line.replace('\t', "")
	line = line.replace(' ', "")
	return line

def replace_variables(variables, line):
	# replaces all variables in the line with their actual value
	for var in variables:
		line = line.replace(var, str(variables[var]))
	return line	

def string_to_int_tuple(string):
	string = string.replace('(', "")
	string = string.replace(')', "")
	string = string.split(',')
	return tuple([eval(x) for x in string])


# takes in a line list broken into [attrib/declare, value]
# adds a variable to the variable dictionary or returns attribute
def handle_declarations(variables, line, current_object): 
	# if the line contains an equal sign it must be declaring an attribute
	# for an object or declaring a variable
	# line[0] holds the attribute or declaration
	# line[1] holds the value be declared or assigned	
	if line[0] in attrib_declaration_keywords:
		#make the string tuples to int tuples
		if '(' in line[1]:
			current_tuple = line[1]	
			#convert to int tuple to pass attributes
			current_object.append(string_to_int_tuple(current_tuple))	
			#just append attribute as int 	
		else:
			current_object.append(int(line[1]))	
	#if it is a declaration add it variables dict
	else:
		variables[line[0]] = eval(line[1])

# splits the line into a list of parameters
def parse_parameters(line):
	# remove () from the function call
	line = line[1:-1]
	parameters = []
	isTuple = False
	current_parameter = ""
	for char in line:
		if char == '(':
			isTuple = True
		elif char == ')':
			isTuple = False
		if char == ',' and not isTuple:
			parameters.append(string_to_int_tuple(current_parameter))
			current_parameter = ""
			continue
		current_parameter += char


	current_parameter = string_to_int_tuple(current_parameter)
	parameters.append(current_parameter)
	
	return parameters
		
			
# searches for functions in the level files and calculates their results
def check_functions(attributes, current_object, line):
	for func in functions.attr_functions:
		if func in line:
			# remove the name of the function from line
			line = line.replace(func, "")
			parameters = parse_parameters(line)
			
			# pass the list of parameters to the function
			function = functions.attr_functions[func]
			# get the results of the function and append them to the list
			result = function(parameters)

			if type(result) is list:
				attributes.append(current_object)
				for res in result:
					attributes.append(res)
			else:
				current_object.append(result)

			break
 
					
def parse_block(block):
	#contains the variables in our level file
	variables = {}
	#removes the comments 
	lines = block.split("\n")
	attributes = []
	current_object = []
	for index, line in enumerate(lines):
		line = remove_comments(line)
		line = replace_variables(variables, line)
		#check for assigment or declaration	
		if '=' in line: 
			declaration = line.split('=')
			handle_declarations(variables, declaration, current_object)
	
		#add the attributes
		if line in attribute_objects:
			current_object.append(line)
		#FIX THIS LINE
		if line == "SUB":
			attributes.append(current_object)
			current_object = []
		check_functions(attributes, current_object, line)
	attributes.append(current_object)
	return attributes	


