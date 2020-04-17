# Code by Fred Qiao at SCAD
# Apr.2020
# code as part of the auto fish rigger component
import maya.cmds as cmds

def addShaper(component, jntNum):
	shaperCtrl = cmds.duplicate("sample_shaper_ctrl", name = component + "_shaper_ctrl")[0]
	# # add attribute to scale in Y
	# cmds.addAttr(shaperCtrl, attributeType = "double", 
	# 			longName = "y_width", defaultValue = 1, min = 0.001)
	# cmds.setAttr(shaperCtrl + ".y_width", lock = False, channelBox = True)
	# cmds.setAttr(shaperCtrl + ".y_width", keyable = True)
	# cmds.connectAttr(shaperCtrl + ".y_width", component + "_1_ctrl_auto.scaleY")


	# # add attribute to scale in Z
	# cmds.addAttr(shaperCtrl, attributeType = "double", 
	# 			longName = "z_width", defaultValue = 1, min = 0.001)
	# cmds.setAttr(shaperCtrl + ".z_width", lock = False, channelBox = True)
	# cmds.setAttr(shaperCtrl + ".z_width", keyable = True)
	# cmds.connectAttr(shaperCtrl + ".z_width", component + "_1_ctrl_auto.scaleZ")

	# add length control
	for i in xrange(jntNum):
		attrName = "section_" + str(i+1) + "_length"
		cmds.addAttr(shaperCtrl, attributeType = "double", 
				longName = "section_" + str(i+1) + "_length", defaultValue = 0)
		cmds.setAttr(shaperCtrl + "." + attrName, lock = False, channelBox = True)
		cmds.setAttr(shaperCtrl + "." + attrName , keyable = True)
		cmds.connectAttr(shaperCtrl + "." + attrName, component + "_" + str(i+1) + "_ctrl_auto.translateX")
		
addShaper("spine", 5)
addShaper("Lf_bottom_front_fin", 2)
addShaper("Lf_pectoralFin", 4)
addShaper("bottom_back_fin", 3)
addShaper("top_front_fin", 3)
addShaper("Rt_pectoralFin", 4)
addShaper("Rt_bottom_front_fin", 2)
addShaper("top_back_fin", 3)
addShaper("top_tail", 3)
addShaper("bottom_tail", 3)
