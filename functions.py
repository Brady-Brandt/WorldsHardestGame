# logic for our predefined functions in our level files
BORDERW = 5


# takes in dimensions of rectangle and calcs the borders
def calc_borders(params):
	rect = params[0]
	x = rect[0]
	y = rect[1]
	w = rect[2]
	h = rect[3]
	left_border = (x-BORDERW, y-BORDERW, BORDERW, h+BORDERW)
	top_border = (x-BORDERW, y-BORDERW, w+BORDERW,BORDERW)
	right_border = (w+x, y-BORDERW, BORDERW, h+BORDERW*2)
	bottom_border = (x-BORDERW, y+h, w+BORDERW, BORDERW) # get it into proper parsing format
	left_border = ["BORDER", left_border]
	top_border = ["BORDER", top_border]
	right_border = ["BORDER", right_border]
	bottom_border = ["BORDER", bottom_border]

	result = [left_border, top_border, right_border, bottom_border]    
	# second optional parameter will only put a border around the inputted sides
	# left = 1
	# top = 2
	# right = 3
	# bottom = 4	
	if len(params) > 1:
		borders = []
		for border in params[1]:
			borders.append(result[border - 1])

		# fills in the space normally used for border with a white
		# background color	
		if len(params) == 3:
			for i in params[2]:
				rect = result[i-1]
				rect[0] = "RECT"
				borders.append(rect)	
		return borders

		

	return result

# takes in rectangle dimensions and returns the location of the middle
def calc_middle(params):
	rect = params[0]
	x = rect[0]
	y = rect[1]
	w = rect[2]
	h = rect[3]
	
	result = ((w / 2) + x, (h / 2) + y)	
	return result
	
# takes in two 4 element tuples specifying a custom border
# the tuples specify one line
# (x,y,w,h) 
def custom_border(params):
	border_one = ["BORDER", params[0]]
	border_two = ["BORDER", params[1]]
	return [border_one, border_two]



# contains functions built in to our level files
attr_functions = {
	"CALC_BORDERS": calc_borders,
	"CALC_MIDDLE": calc_middle,
	"CUSTOM_BORDER": custom_border,
}	


