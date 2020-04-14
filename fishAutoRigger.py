# fish auto rigger for Project Olegoscene UI
# Fred Qiao SCAD
# Apr 2020
# qiaozhehao951115@gmai.com

import maya.cmds as cmds
from functools import partial
# generic component
class genericComponent(object):


	def __init__(self, compName, side, secNum):
		self.compName = compName
		self.side = side
		self.secNum = secNum
		self.buildSuf  = "_build"

		self.buildLs = []
		for i in xrange(secNum):
			self.buildLs += [self.compName + "_" +  str(i+1) + self.buildSuf]
		self.buildTransRotLs = [((0, 0, 0), (180, 90, 0))]
		for i in xrange(secNum-1):
			self.buildTransRotLs += [((1, 0, 0), (0, 0, 0))]

	def setTransRotLs(self, jntLs, attrLs):
		for i in xrange(len(jntLs)):
			cmds.setAttr(jntLs[i] + ".translate", attrLs[i][0][0], attrLs[i][0][1], attrLs[i][0][2], type = "double3")
			cmds.setAttr(jntLs[i] + ".jointOrient", attrLs[i][1][0], attrLs[i][1][1], attrLs[i][1][2], type = "double3")
			cmds.setAttr(jntLs[i] + ".rotate", 0,0,0, type = "double3")
			cmds.setAttr(jntLs[i] + ".scale", 1,1,1, type = "double3")

	def getTransRotLs(self, jntLs):
		rstLs = []
		for i in xrange(len(jntLs)):
			crtAttrLs = []
			crtAttrLs += [cmds.getAttr(jntLs[i] + ".translate")[0]]
			crtAttrLs += [cmds.getAttr(jntLs[i] + ".jointOrient")[0]]
			rstLs += [crtAttrLs]
		return rstLs


	def createJointChain(self, nameLs, transRotLs):
		prevJnt = None
		for i in xrange(len(nameLs)):
			cmds.select(clear = True)
			crtJnt = cmds.joint(name = nameLs[i])
			cmds.select(clear = True)
			if prevJnt != None:
				cmds.parent(crtJnt, prevJnt)
			prevJnt = crtJnt
		self.setTransRotLs(nameLs, transRotLs)

	def build(self):
		cmds.select(clear = True)
		self.createJointChain(self.buildLs, self.buildTransRotLs)


	def final(self):
		for i in xrange(len())







def genericBuildButtonWrapper(nameField, numField, *args):
	compName = cmds.textField(nameField, q = True, text = True)
	secNum = int(cmds.textField(numField, q = True, text = True))
	genericComp = genericComponent(compName, None, secNum)
	genericComp.build()
	return None


def genericFinalButtonWrapper(nameField, numField, *args):
	compName = cmds.textField(nameField, q = True, text = True)
	secNum = int(cmds.textField(numField, q = True, text = True))
	genericComp = genericComponent(compName, None, secNum)
	genericComponent.final()
	return None

def genericMirrorButtonWrapper(*args):
	return None

def genericConnectButtonWrapper(*args):
	return None








# UI

# UI helper functions
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

def main():
	WINDOWNAME = "Oligocene Fish Auto Rigger"
	WIDTH = 180
	HEIGHT = 380
	BORDERWIDTH = 5
	ROWSPACE = 5
	SEPAHEIGHT = 10
	SUBWINODWWIDTH = 385
	SUBWINDOWHEIGHT = 340
	mainWindow = cmds.window(menuBar = True, title = WINDOWNAME, 
		widthHeight = (WIDTH+5, HEIGHT), sizeable = False)
	cmds.columnLayout(columnWidth = WIDTH - BORDERWIDTH*2, 
		columnOffset = ("left", BORDERWIDTH), rowSpacing = ROWSPACE)

	cmds.text(label = "Oligocene Fish Auto Rigger v1.0", font = "boldLabelFont", height = 30)

	cmds.text(label = "- Placer", font = "boldLabelFont")
	buildingButtonLs = insertButtonSet(1, 1, 30, WIDTH-BORDERWIDTH*2, 
		["Final"], colorLs =  [(0.6, 0.6, 0.6)])
	# addButtonCmds(buildingButtonLs, [
	# 	partial(finalButtonWrapper, None, None, None, "placer")
	# 	])

	cmds.text(label = "- Head", font = "boldLabelFont")
	buildingButtonLs = insertButtonSet(1, 3, 30, WIDTH/3.0-BORDERWIDTH/3.0*2, 
		["Build", "Final", "Connect"], colorLs = [(0.7, 0.7, 0.7), (0.6, 0.6, 0.6), (0.35, 0.35, 0.35)])
	# addButtonCmds(buildingButtonLs, [
	# 	partial(buildButtonWrapper, None, None, None, "spine"),
	# 	partial(finalButtonWrapper, None, None, None, "spine"),
	# 	partial(rebuildButtonWrapper, None, None, None, "spine")])	

	cmds.text(label = "- Generic Component", font = "boldLabelFont")
	cmds.rowColumnLayout(numberOfColumns = 2, 
		columnWidth = [(1, 0.5*(WIDTH-BORDERWIDTH*2)), 
			(2, 0.5*(WIDTH-BORDERWIDTH*2))],
		columnAttach = [(1, "left", 0), (2, "left", 0)])
	nameTextLs = [cmds.text(label = "Name")]
	nameTextFieldLs = [cmds.textField(annotation = "Type in the name of component")]
	cmds.setParent("..")
	cmds.rowColumnLayout(numberOfColumns = 2, 
		columnWidth = [(1, 0.7*(WIDTH-BORDERWIDTH*2)), 
			(2, 0.3*(WIDTH-BORDERWIDTH*2))],
		columnAttach = [(1, "left", 0), (2, "left", 0)])
	numTextLs = [cmds.text(label = "Section Number")]
	numTextFieldLs = [cmds.textField(annotation = "Type in the name of component")]
	cmds.setParent("..")
	
	buildingButtonLs = insertButtonSet(2, 2, 30, WIDTH/2.0-BORDERWIDTH/2.0*2, 
		["Build", "Final", "Mirror", "Connect"], colorLs = [(0.7, 0.7, 0.7), (0.6, 0.6, 0.6), (0.5, 0.5, 0.5), (0.35, 0.35, 0.35)])
	addButtonCmds(buildingButtonLs, [
	 	partial(genericBuildButtonWrapper, nameTextFieldLs[0], numTextFieldLs[0]),
	 	partial(genericFinalButtonWrapper),
	 	partial(genericMirrorButtonWrapper),
	 	partial(genericConnectButtonWrapper),
	 	])	
	



	hierarchyButtonLs = insertButtonSet(1, 1, 30, WIDTH-BORDERWIDTH*2, 
		["Sort Hierarchy"], colorLs = [(0.2, 0.2, 0.2)])
	# addButtonCmds(hierarchyButtonLs, [
	# 	partial(hierarchyButtonWrapper)])

	setButtonLs = insertButtonSet(1, 1, 30, WIDTH-BORDERWIDTH*2, 
		["Create Bind Set"], colorLs = [(0.2, 0.2, 0.2)])
	# addButtonCmds(setButtonLs, [
	# 	partial(bindSetButtonWrapper)])





	cmds.showWindow(mainWindow)
main()