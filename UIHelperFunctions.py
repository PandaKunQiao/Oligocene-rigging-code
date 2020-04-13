# UI helper functions
# By Fred Qiao Apr 2020
# adding a set of buttons
# return the list of button labels
def insertButtonSet(rowNum, colNum, buttonHeight, buttonWidth, labelLs, 
	msgLs = None, colorLs = None):
	# create row attachLs
	rowAttachLs = []
	columnAttachLs = []
	colSpacingLs = []
	rowSpacing = [(1, 0)]

	buttonLs = []

	# no color choice is specified
	if colorLs == None:
		colorLs = []
		for i in xrange(rowNum*colNum):
			colorLs += [[0.35, 0.35, 0.35]]
	for i in xrange(colNum):
		rowAttachLs += [(i+1, "top", 0)]
		columnAttachLs += [(i+1, "left", 0)]
		colSpacingLs += [(i+1, 0)]
	cmds.rowColumnLayout(numberOfColumns = colNum, columnSpacing = colSpacingLs, 
		columnAttach = columnAttachLs)
	for i in xrange(rowNum*colNum):
		if msgLs != None:
			crtMsg = msgLs[i]
			if crtMsg != None:
				crtButton = cmds.button(label = labelLs[i], width = buttonWidth, 
					height = buttonHeight, annotation = crtMsg, 
					backgroundColor = colorLs[i])
			else:
				crtButton = cmds.button(label = labelLs[i], width = buttonWidth, 
					height = buttonHeight, backgroundColor = colorLs[i])
		else:
			crtButton = cmds.button(label = labelLs[i], width = buttonWidth, 
				height = buttonHeight, backgroundColor = colorLs[i])
		buttonLs += [crtButton]
	cmds.setParent("..")
	return buttonLs	

def addButtonCmds(buttonLs, cmdsLs):
	for i in xrange(len(buttonLs)):
		crtButton = buttonLs[i]
		crtCmd = cmdsLs[i]
		cmds.button(crtButton, edit = True, command = cmdsLs[i])