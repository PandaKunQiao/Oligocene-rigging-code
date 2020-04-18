# code by Fred Qiao @ SCAD
# select the controls that you want to mirror from first, then run the script
def mirrorCtrl():
	ctrlLs = cmds.ls(selection = True)
	for i in xrange(len(ctrlLs)):
		vertNum = cmds.getAttr(ctrlLs[i]+".degree") + cmds.getAttr(ctrlLs[i]+".spans") + 1
		for j in xrange(vertNum):
			crtFromPosition = cmds.xform(ctrlLs[i] + ".cv[" + str(j) + "]", query = True, ws = True, t = True)
			crtFromPosition[0] = -crtFromPosition[0]
			if ctrlLs[i][:2] == "Lf":
				mirrored = "Rt" + ctrlLs[i][2:]
			else:
				mirrored = "Lf" + ctrlLs[i][2:]
			cmds.xform(mirrored + ".cv[" + str(j) + "]", t = crtFromPosition, ws = True)
mirrorCtrl()