# fish auto rigger for Project Olegoscen at SCA
# Fred Qiao @ SCAD
# Apr 2020
# qiaozhehao951115@gmail.com

import maya.cmds as cmds
from functools import partial
import string
# function to add the expression for auto swimming automatically
def addAutoRotate(origExpression, componentHolder, component, numHolder, ctrlNum):
	for i in xrange(ctrlNum):
		crtString = origExpression
		crtString = string.replace(crtString, componentHolder, component)
		crtString = string.replace(crtString, numHolder, str(i+1))
		cmds.expression(string = crtString, object = crtString, name = component + "_auto_" + str(i+1) + "_exp")


def addShaper(shaperCtrl, component, jntNum):
	# add length control
	for i in xrange(jntNum):
		attrName = "section_" + str(i+1) + "_length"
		cmds.addAttr(shaperCtrl, attributeType = "double", 
				longName = "section_" + str(i+1) + "_length", defaultValue = 0)
		cmds.setAttr(shaperCtrl + "." + attrName, lock = False, channelBox = True)
		cmds.setAttr(shaperCtrl + "." + attrName , keyable = True)
		cmds.connectAttr(shaperCtrl + "." + attrName, component + "_" + str(i+1) + "_ctrl_auto.translateX")

# set rgb
def setRGBColor(ctrl, color = (1,1,1)):
    
    rgb = ("R","G","B")
    
    cmds.setAttr(ctrl + ".overrideEnabled",1)
    cmds.setAttr(ctrl + ".overrideRGBColors",1)
    
    for channel, color in zip(rgb, color):
        
        cmds.setAttr(ctrl + ".overrideColor%s" %channel, color)


# placer component
class placer(object):

	def createCtrl(self, pointLs, shapeType, ctrlName, degree):
		if shapeType == "circle":
			ctrl = cmds.circle(name = ctrlName)[0]
			for i in xrange(len(pointLs)):
				cmds.xform(ctrl+".cv[" + str(i) + "]", worldSpace = True, translation = pointLs[i])
			return ctrl
		else:
			ctrl = cmds.curve(point = pointLs, name = ctrlName, degree = degree)
			return ctrl

	def __init__(self):

		self.buildLs = ["cog_build", "cog_tip_build"]
		self.globalCtrl = "global_ctrl"
		self.orientCtrl = "move_ctrl"
		self.charCtrl = "char_ctrl"
		self.autoCtrl = "auto_ctrl"
		self.cogCtrl = "cog_ctrl"
		self.CTRLname = "placer_CTRL_GRP"

		self.refSuf = "_ref"
		self.globalCtrlShapeLs = [[[5.083185932272879, 3.1125536907144174e-16, -5.083185932272883], [4.4018156430227595e-16, 4.4018156430227595e-16, -7.188710485484426], [-5.083185932272879, 3.1125536907144174e-16, -5.083185932272877], [-7.188710485484427, 2.2819090023669337e-32, -3.726640209986566e-16], [-5.083185932272879, -3.112553690714418e-16, 5.083185932272879], [-7.200980459151989e-16, -4.401815643022763e-16, 7.188710485484433], [5.083185932272879, -3.1125536907144174e-16, 5.083185932272877], [7.188710485484427, -6.0027404505551e-32, 9.803219107312316e-16], [7.188710485484427, -6.0027404505551e-32, 9.803219107312316e-16], [7.188710485484427, -6.0027404505551e-32, 9.803219107312316e-16], [7.188710485484427, -6.0027404505551e-32, 9.803219107312316e-16]]]
		self.orientCtrlShapeLs = [[[1.9702477141469998, 0.0001239829303505055, -2.027355718809554], [2.9892245381664666, 2.9872845047256933e-05, -0.5895418874976464], [4.483839791800435, 1.9571847529992282e-05, -0.5895418874976464], [4.483839791800435, 1.9571847529992282e-05, -0.5895418874976464], [4.483839791800435, 1.9571847529992282e-05, -2.009426378449913], [4.483839791800435, 1.9571847529992282e-05, -2.009426378449913], [5.9784550454344, 0.0, 0.0], [5.9784550454344, 0.0, 0.0], [4.483839791800435, 1.9571847529992282e-05, 2.009426378449913], [4.483839791800435, 1.9571847529992282e-05, 2.009426378449913], [4.483839791800435, 1.9571847529992282e-05, 0.5895418874976464], [4.483839791800435, 1.9571847529992282e-05, 0.5895418874976464], [2.9892245381664666, 2.9872845047256933e-05, 0.5895418874976464], [1.9702477141469998, 0.0001239829303505055, 2.027355718809554], [1.9702477141469998, 0.0001239829303505055, 2.027355718809554], [0.5729352503162067, 2.9872845047256933e-05, 2.9892245381664666], [0.5729352503162067, 1.9571847529992282e-05, 4.483839791800435], [0.5729352503162067, 1.9571847529992282e-05, 4.483839791800435], [2.009426378449913, 1.9571847529992282e-05, 4.483839791800435], [2.009426378449913, 1.9571847529992282e-05, 4.483839791800435], [0.0, 0.0, 5.9784550454344], [0.0, 0.0, 5.9784550454344], [-2.009426378449913, 1.9571847529992282e-05, 4.483839791800435], [-2.009426378449913, 1.9571847529992282e-05, 4.483839791800435], [-0.5729352503162067, 1.9571847529992282e-05, 4.483839791800435], [-0.5729352503162067, 1.9571847529992282e-05, 4.483839791800435], [-0.5729352503162067, 2.9872845047256933e-05, 2.9892245381664666], [-1.9702477141469998, 0.0001239829303505055, 2.027355718809554], [-1.9702477141469998, 0.0001239829303505055, 2.027355718809554], [-2.9892245381664666, 2.9872845047256933e-05, 0.5895418874976464], [-4.483839791800435, 1.9571847529992282e-05, 0.5895418874976464], [-4.483839791800435, 1.9571847529992282e-05, 0.5895418874976464], [-4.483839791800435, 1.9571847529992282e-05, 2.009426378449913], [-4.483839791800435, 1.9571847529992282e-05, 2.009426378449913], [-5.9784550454344, 0.0, 0.0], [-5.9784550454344, 0.0, 0.0], [-4.483839791800435, 1.9571847529992282e-05, -2.009426378449913], [-4.483839791800435, 1.9571847529992282e-05, -2.009426378449913], [-4.483839791800435, 1.9571847529992282e-05, -0.5895418874976464], [-4.483839791800435, 1.9571847529992282e-05, -0.5895418874976464], [-2.9892245381664666, 2.9872845047256933e-05, -0.5895418874976464], [-1.9702477141469998, 0.0001239829303505055, -2.027355718809554], [-1.9702477141469998, 0.0001239829303505055, -2.027355718809554], [-0.5729352503162067, 2.9872845047256933e-05, -2.9892245381664666], [-0.5729352503162067, 1.9571847529992282e-05, -4.483839791800435], [-0.5729352503162067, 1.9571847529992282e-05, -4.483839791800435], [-2.009426378449913, 1.9571847529992282e-05, -4.483839791800435], [-2.009426378449913, 1.9571847529992282e-05, -4.483839791800435], [0.0, 0.0, -5.9784550454344], [0.0, 0.0, -5.9784550454344], [2.009426378449913, 1.9571847529992282e-05, -4.483839791800435], [2.009426378449913, 1.9571847529992282e-05, -4.483839791800435], [0.5729352503162067, 1.9571847529992282e-05, -4.483839791800435], [0.5729352503162067, 1.9571847529992282e-05, -4.483839791800435], [0.5729352503162067, 2.9872845047256933e-05, -2.9892245381664666], [1.9702477141469998, 0.0001239829303505055, -2.027355718809554]]]
		self.autoCtrlShapeLs = [[[-1.5157345533370972, 0.1755240112543106, 0.0], [-1.5016640424728394, 0.12693294882774353, 0.0], [-1.4836187362670898, 0.0848207026720047, 0.0], [-1.4615988731384277, 0.04918726533651352, 0.0], [-1.4356040954589844, 0.02003263123333454, 0.0], [-1.4056346416473389, -0.002643194515258074, 0.0], [-1.3716905117034912, -0.018840212374925613, 0.0], [-1.3337715864181519, -0.02855842374265194, 0.0], [-1.2918778657913208, -0.031797826290130615, 0.0], [-1.2414783239364624, -0.029254000633955002, 0.0], [-1.1933046579360962, -0.02162252366542816, 0.0], [-1.1473567485809326, -0.008903391659259796, 0.0], [-1.1036347150802612, 0.008903391659259796, 0.0], [-1.1214416027069092, 0.14754192531108856, 0.0], [-1.1697742938995361, 0.14245426654815674, 0.0], [-1.2007771730422974, 0.14581291377544403, 0.0], [-1.2276463508605957, 0.1558888554573059, 0.0], [-1.2503817081451416, 0.17268207669258118, 0.0], [-1.2689834833145142, 0.19619259238243103, 0.0], [-1.2834514379501343, 0.22642040252685547, 0.0], [-1.293785810470581, 0.2633655071258545, 0.0], [-1.2999863624572754, 0.3070279061794281, 0.0], [-1.3020532131195068, 0.3574075698852539, 0.0], [-1.3020532131195068, 0.983188807964325, 0.0], [-1.3088897466659546, 1.0854586362838745, 0.0], [-1.3293993473052979, 1.1734988689422607, 0.0], [-1.3635820150375366, 1.2473095655441284, 0.0], [-1.411437749862671, 1.3068907260894775, 0.0], [-1.4736820459365845, 1.3527988195419312, 0.0], [-1.551030158996582, 1.3855903148651123, 0.0], [-1.6434823274612427, 1.405265212059021, 0.0], [-1.7510385513305664, 1.4118235111236572, 0.0], [-1.864795207977295, 1.4053845405578613, 0.0], [-1.9822087287902832, 1.386067271232605, 0.0], [-2.103278875350952, 1.3538720607757568, 0.0], [-2.228005886077881, 1.3087985515594482, 0.0], [-2.228005886077881, 1.101476788520813, 0.0], [-2.115123748779297, 1.1548970937728882, 0.0], [-2.006693124771118, 1.193054437637329, 0.0], [-1.9027141332626343, 1.2159489393234253, 0.0], [-1.8031870126724243, 1.2235803604125977, 0.0], [-1.7444603443145752, 1.2198243141174316, 0.0], [-1.6935639381408691, 1.2085559368133545, 0.0], [-1.6504977941513062, 1.1897753477096558, 0.0], [-1.6152617931365967, 1.1634825468063354, 0.0], [-1.5878560543060303, 1.129677414894104, 0.0], [-1.5682804584503174, 1.0883601903915405, 0.0], [-1.5565351247787476, 1.039530634880066, 0.0], [-1.5526200532913208, 0.983188807964325, 0.0], [-1.5526200532913208, 0.8165681958198547, 0.0], [-1.6111280918121338, 0.8165681958198547, 0.0], [-1.6975685358047485, 0.8146702647209167, 0.0], [-1.7788218259811401, 0.8089764714241028, 0.0], [-1.8548882007598877, 0.7994868159294128, 0.0], [-1.9257675409317017, 0.7862012982368469, 0.0], [-1.991459846496582, 0.769119918346405, 0.0], [-2.0519652366638184, 0.7482426166534424, 0.0], [-2.107283592224121, 0.7235695123672485, 0.0], [-2.157414674758911, 0.6951004862785339, 0.0], [-2.20198130607605, 0.6630939841270447, 0.0], [-2.2406058311462402, 0.6278083324432373, 0.0], [-2.2732880115509033, 0.5892435312271118, 0.0], [-2.300028085708618, 0.5473995804786682, 0.0], [-2.3208258152008057, 0.5022764801979065, 0.0], [-2.335681200027466, 0.45387423038482666, 0.0], [-2.344594717025757, 0.4021928310394287, 0.0], [-2.3475656509399414, 0.34723228216171265, 0.0], [-2.3404908180236816, 0.26873138546943665, 0.0], [-2.319265604019165, 0.19730551540851593, 0.0], [-2.28389048576355, 0.1329546719789505, 0.0], [-2.234365463256836, 0.07567883282899857, 0.0], [-2.1741085052490234, 0.028657792136073112, 0.0], [-2.1065382957458496, -0.004928663372993469, 0.0], [-2.0316543579101562, -0.025080537423491478, 0.0], [-1.9494569301605225, -0.031797826290130615, 0.0], [-1.897050142288208, -0.02855842374265194, 0.0], [-1.8441267013549805, -0.018840212374925613, 0.0], [-1.7906864881515503, -0.002643194515258074, 0.0], [-1.7367295026779175, 0.02003263123333454, 0.0], [-1.6822558641433716, 0.04918726533651352, 0.0], [-1.627265453338623, 0.0848207026720047, 0.0], [-1.627265453338623, 0.0848207026720047, 0.0], [-1.627265453338623, 0.0848207026720047, 0.0]], [[-0.07657212764024734, 0.0, 0.0], [0.17399483919143677, 0.0, 0.0], [0.17399483919143677, 1.3812975883483887, 0.0], [-0.07657212764024734, 1.3812975883483887, 0.0], [-0.07657212764024734, 0.4858708083629608, 0.0], [-0.12784594297409058, 0.4152200222015381, 0.0], [-0.17991489171981812, 0.35398930311203003, 0.0], [-0.23277896642684937, 0.3021787405014038, 0.0], [-0.2864376902580261, 0.25978824496269226, 0.0], [-0.3408915400505066, 0.22681787610054016, 0.0], [-0.39614027738571167, 0.20326761901378632, 0.0], [-0.45218390226364136, 0.18913745880126953, 0.0], [-0.5090225338935852, 0.1844273954629898, 0.0], [-0.558030903339386, 0.1885213702917099, 0.0], [-0.5994872450828552, 0.20080327987670898, 0.0], [-0.6333916783332825, 0.22127313911914825, 0.0], [-0.6597442030906677, 0.24993093311786652, 0.0], [-0.6794986128807068, 0.28828704357147217, 0.0], [-0.693608820438385, 0.3378519117832184, 0.0], [-0.7020750641822815, 0.39862552285194397, 0.0], [-0.7048971056938171, 0.47060784697532654, 0.0], [-0.7048971056938171, 1.3812975883483887, 0.0], [-0.9554639458656311, 1.3812975883483887, 0.0], [-0.9554639458656311, 0.3892054259777069, 0.0], [-0.9487864375114441, 0.2975084185600281, 0.0], [-0.9287537932395935, 0.21574826538562775, 0.0], [-0.8953661322593689, 0.14392492175102234, 0.0], [-0.8486233353614807, 0.08203839510679245, 0.0], [-0.7905922532081604, 0.032235048711299896, 0.0], [-0.723339855670929, -0.0033387718722224236, 0.0], [-0.6468660235404968, -0.024683063849806786, 0.0], [-0.5611708760261536, -0.031797826290130615, 0.0], [-0.4912753701210022, -0.027246763929724693, 0.0], [-0.42404288053512573, -0.01359357126057148, 0.0], [-0.35947340726852417, 0.009161748923361301, 0.0], [-0.29756683111190796, 0.041019197553396225, 0.0], [-0.2383236289024353, 0.08197877556085587, 0.0], [-0.181743323802948, 0.13204048573970795, 0.0], [-0.12782615423202515, 0.19120430946350098, 0.0], [-0.07657212764024734, 0.25947028398513794, 0.0], [-0.07657212764024734, 0.25947028398513794, 0.0], [-0.07657212764024734, 0.25947028398513794, 0.0]], [[1.1388194561004639, 0.0, 0.0], [1.1388194561004639, 0.1729801893234253, 0.0], [1.072998046875, 0.16057902574539185, 0.0], [1.0179877281188965, 0.15644530951976776, 0.0], [0.9631364941596985, 0.16067840158939362, 0.0], [0.9155986905097961, 0.17337766289710999, 0.0], [0.8753746151924133, 0.19454307854175568, 0.0], [0.8424637913703918, 0.22417467832565308, 0.0], [0.8168664574623108, 0.262272447347641, 0.0], [0.7985828518867493, 0.3088364005088806, 0.0], [0.7876124978065491, 0.36386650800704956, 0.0], [0.7839558720588684, 0.4273627996444702, 0.0], [0.7839558720588684, 1.193054437637329, 0.0], [1.145179033279419, 1.193054437637329, 0.0], [1.145179033279419, 1.3812975883483887, 0.0], [0.7839558720588684, 1.3812975883483887, 0.0], [0.7839558720588684, 1.6560308933258057, 0.0], [0.5333889126777649, 1.6318645477294922, 0.0], [0.5333889126777649, 1.3812975883483887, 0.0], [0.36040884256362915, 1.3812975883483887, 0.0], [0.36040884256362915, 1.193054437637329, 0.0], [0.5333889126777649, 1.193054437637329, 0.0], [0.5333889126777649, 0.38157394528388977, 0.0], [0.5400665402412415, 0.2895987033843994, 0.0], [0.560099184513092, 0.20827576518058777, 0.0], [0.5934868454933167, 0.13760510087013245, 0.0], [0.6402295231819153, 0.07758670300245285, 0.0], [0.6988967061042786, 0.029730968177318573, 0.0], [0.7680569291114807, -0.004451695829629898, 0.0], [0.8477104306221008, -0.02496129460632801, 0.0], [0.9378572106361389, -0.031797826290130615, 0.0], [1.0307068824768066, -0.02384837158024311, 0.0], [1.0307068824768066, -0.02384837158024311, 0.0], [1.0307068824768066, -0.02384837158024311, 0.0]], [[1.9507288932800293, -0.031797826290130615, 0.0], [2.0247483253479004, -0.028757160529494286, 0.0], [2.0948128700256348, -0.019635159522294998, 0.0], [2.1609225273132324, -0.004431822337210178, 0.0], [2.2230772972106934, 0.01685284823179245, 0.0], [2.2812771797180176, 0.04421885311603546, 0.0], [2.335522174835205, 0.07766619324684143, 0.0], [2.385812282562256, 0.11719486862421036, 0.0], [2.432147979736328, 0.16280487179756165, 0.0], [2.473733425140381, 0.21362178027629852, 0.0], [2.5097742080688477, 0.26877114176750183, 0.0], [2.5402703285217285, 0.3282529413700104, 0.0], [2.5652217864990234, 0.39206722378730774, 0.0], [2.5846285820007324, 0.46021392941474915, 0.0], [2.5984902381896973, 0.532693088054657, 0.0], [2.606807231903076, 0.609504759311676, 0.0], [2.609579563140869, 0.6906487941741943, 0.0], [2.606807231903076, 0.7717829346656799, 0.0], [2.5984902381896973, 0.8485648036003113, 0.0], [2.5846285820007324, 0.9209942817687988, 0.0], [2.5652217864990234, 0.9890714287757874, 0.0], [2.5402703285217285, 1.0527962446212769, 0.0], [2.5097742080688477, 1.112168788909912, 0.0], [2.473733425140381, 1.1671890020370483, 0.0], [2.432147979736328, 1.217856764793396, 0.0], [2.385812282562256, 1.2633177042007446, 0.0], [2.335522174835205, 1.3027172088623047, 0.0], [2.2812771797180176, 1.3360552787780762, 0.0], [2.2230772972106934, 1.363331913948059, 0.0], [2.1609225273132324, 1.3845469951629639, 0.0], [2.0948128700256348, 1.39970064163208, 0.0], [2.0247483253479004, 1.4087928533554077, 0.0], [1.9507288932800293, 1.4118235111236572, 0.0], [1.8767094612121582, 1.4087928533554077, 0.0], [1.8066449165344238, 1.39970064163208, 0.0], [1.7405352592468262, 1.3845469951629639, 0.0], [1.6783804893493652, 1.363331913948059, 0.0], [1.620180606842041, 1.3360552787780762, 0.0], [1.5659351348876953, 1.3027172088623047, 0.0], [1.5156450271606445, 1.2633177042007446, 0.0], [1.4693095684051514, 1.217856764793396, 0.0], [1.4277241230010986, 1.1671890020370483, 0.0], [1.3916833400726318, 1.112168788909912, 0.0], [1.361187219619751, 1.0527962446212769, 0.0], [1.336235761642456, 0.9890714287757874, 0.0], [1.3168292045593262, 0.9209942817687988, 0.0], [1.3029673099517822, 0.8485648036003113, 0.0], [1.2946500778198242, 0.7717829346656799, 0.0], [1.2918777465820312, 0.6906487941741943, 0.0], [1.2946500778198242, 0.609504759311676, 0.0], [1.3029673099517822, 0.532693088054657, 0.0], [1.3168292045593262, 0.46021392941474915, 0.0], [1.336235761642456, 0.39206722378730774, 0.0], [1.361187219619751, 0.3282529413700104, 0.0], [1.3916833400726318, 0.26877114176750183, 0.0], [1.4277241230010986, 0.21362178027629852, 0.0], [1.4693095684051514, 0.16280487179756165, 0.0], [1.5156450271606445, 0.11719486862421036, 0.0], [1.5659351348876953, 0.07766619324684143, 0.0], [1.620180606842041, 0.04421885311603546, 0.0], [1.6783804893493652, 0.01685284823179245, 0.0], [1.7405352592468262, -0.004431822337210178, 0.0], [1.8066449165344238, -0.019635159522294998, 0.0], [1.8767094612121582, -0.028757160529494286, 0.0], [1.8767094612121582, -0.028757160529494286, 0.0], [1.8767094612121582, -0.028757160529494286, 0.0]], [[-1.5526200532913208, 0.31161871552467346, 0.0], [-1.6364073753356934, 0.25096434354782104, 0.0], [-1.7186046838760376, 0.20763981342315674, 0.0], [-1.7992122173309326, 0.18164509534835815, 0.0], [-1.838919758796692, 0.1751464158296585, 0.0], [-1.8782298564910889, 0.1729801893234253, 0.0], [-1.9222698211669922, 0.17687541246414185, 0.0], [-1.962812066078186, 0.1885611116886139, 0.0], [-1.9998564720153809, 0.20803728699684143, 0.0], [-2.033403158187866, 0.23530392348766327, 0.0], [-2.0612263679504395, 0.2682146728038788, 0.0], [-2.0810999870300293, 0.30462318658828735, 0.0], [-2.093024253845215, 0.3445294499397278, 0.0], [-2.096998929977417, 0.38793349266052246, 0.0], [-2.095001459121704, 0.4192543625831604, 0.0], [-2.0890097618103027, 0.44898533821105957, 0.0], [-2.065042018890381, 0.5036776065826416, 0.0], [-2.0250959396362305, 0.5520102977752686, 0.0], [-1.9691716432571411, 0.5939834117889404, 0.0], [-1.9002100229263306, 0.6279276013374329, 0.0], [-1.821152687072754, 0.6521734595298767, 0.0], [-1.7319995164871216, 0.6667209267616272, 0.0], [-1.6327506303787231, 0.6715701222419739, 0.0], [-1.5526200532913208, 0.6690263152122498, 0.0], [-1.5526200532913208, 0.6690263152122498, 0.0], [-1.5526200532913208, 0.6690263152122498, 0.0]], [[1.9500927925109863, 0.15644530951976776, 0.0], [1.9047441482543945, 0.15863141417503357, 0.0], [1.862034797668457, 0.1651897132396698, 0.0], [1.8219642639160156, 0.17612022161483765, 0.0], [1.7845330238342285, 0.19142292439937592, 0.0], [1.7497410774230957, 0.2110978215932846, 0.0], [1.717587947845459, 0.2351449429988861, 0.0], [1.6611995697021484, 0.2963557541370392, 0.0], [1.616478443145752, 0.37346547842025757, 0.0], [1.5845346450805664, 0.4648842513561249, 0.0], [1.5653681755065918, 0.5706120133399963, 0.0], [1.5589795112609863, 0.6906487941741943, 0.0], [1.5653681755065918, 0.8106458783149719, 0.0], [1.5845346450805664, 0.9162544012069702, 0.0], [1.616478443145752, 1.007474422454834, 0.0], [1.6611995697021484, 1.0843058824539185, 0.0], [1.717587947845459, 1.1452385187149048, 0.0], [1.7497410774230957, 1.1691763401031494, 0.0], [1.7845330238342285, 1.188761830329895, 0.0], [1.8219642639160156, 1.2039949893951416, 0.0], [1.862034797668457, 1.2148756980895996, 0.0], [1.9047441482543945, 1.2214041948318481, 0.0], [1.9500927925109863, 1.2235803604125977, 0.0], [1.9954514503479004, 1.2214041948318481, 0.0], [2.0381908416748047, 1.2148756980895996, 0.0], [2.078310966491699, 1.2039949893951416, 0.0], [2.115811824798584, 1.188761830329895, 0.0], [2.150693416595459, 1.1691763401031494, 0.0], [2.182955265045166, 1.1452385187149048, 0.0], [2.239622116088867, 1.0843058824539185, 0.0], [2.2846217155456543, 1.007474422454834, 0.0], [2.3167638778686523, 0.9162544012069702, 0.0], [2.3360495567321777, 0.8106458783149719, 0.0], [2.342477798461914, 0.6906487941741943, 0.0], [2.3360495567321777, 0.5706120133399963, 0.0], [2.3167638778686523, 0.4648842513561249, 0.0], [2.2846217155456543, 0.37346547842025757, 0.0], [2.239622116088867, 0.2963557541370392, 0.0], [2.182955265045166, 0.2351449429988861, 0.0], [2.150693416595459, 0.2110978215932846, 0.0], [2.115811824798584, 0.19142292439937592, 0.0], [2.078310966491699, 0.17612022161483765, 0.0], [2.0381908416748047, 0.1651897132396698, 0.0], [1.9954514503479004, 0.15863141417503357, 0.0], [1.9954514503479004, 0.15863141417503357, 0.0], [1.9954514503479004, 0.15863141417503357, 0.0]]]
		self.cogCtrlShapeLs = [[[-0.15508276221968603, 0.8802444753680065, 0.8256615948314078], [0.15508276221968603, 0.8802444753680065, 0.8256615948314078], [0.15508276221968603, 0.8802444753680065, -0.8256615948314078], [-0.15508276221968603, 0.8802444753680065, -0.8256615948314078], [-0.15508276221968603, 0.8802444753680065, 0.8256615948314078], [-0.15508276221968603, -0.8802444753680065, 0.8256615948314078], [-0.15508276221968603, -0.8802444753680065, -0.8256615948314078], [0.15508276221968603, -0.8802444753680065, -0.8256615948314078], [0.15508276221968603, -0.8802444753680065, 0.8256615948314078], [-0.15508276221968603, -0.8802444753680065, 0.8256615948314078], [0.15508276221968603, -0.8802444753680065, 0.8256615948314078], [0.15508276221968603, 0.8802444753680065, 0.8256615948314078], [0.15508276221968603, 0.8802444753680065, -0.8256615948314078], [0.15508276221968603, -0.8802444753680065, -0.8256615948314078], [-0.15508276221968603, -0.8802444753680065, -0.8256615948314078], [-0.15508276221968603, 0.8802444753680065, -0.8256615948314078], [-0.15508276221968603, 0.8802444753680065, -0.8256615948314078]]]
		# seal the character
		for i in xrange(len(self.autoCtrlShapeLs)):
			self.autoCtrlShapeLs[i] += [self.autoCtrlShapeLs[i][0]]
		self.outCtrl = self.cogCtrl
		self.buildTransRotLs = [((0, 0, 0), (180, 90, 0)), ((1, 0, 0), (0, 0, 0))]

	def setTransRotLs(self, jntLs, attrLs):
		for i in xrange(len(jntLs)):
			cmds.setAttr(jntLs[i] + ".translate", attrLs[i][0][0], attrLs[i][0][1], attrLs[i][0][2], type = "double3")
			cmds.setAttr(jntLs[i] + ".jointOrient", attrLs[i][1][0], attrLs[i][1][1], attrLs[i][1][2], type = "double3")
			cmds.setAttr(jntLs[i] + ".rotate", 0,0,0, type = "double3")
			cmds.setAttr(jntLs[i] + ".scale", 1,1,1, type = "double3")

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

	def getTransRotLs(self, jntLs):
		rstLs = []
		for i in xrange(len(jntLs)):
			crtAttrLs = []
			crtAttrLs += [cmds.getAttr(jntLs[i] + ".translate")[0]]
			crtAttrLs += [cmds.getAttr(jntLs[i] + ".jointOrient")[0]]
			rstLs += [crtAttrLs]
		return rstLs

	def build(self):
		self.createJointChain(self.buildLs, self.buildTransRotLs)


	def finish(self):
		self.createCtrl(self.globalCtrlShapeLs[0], "circle", self.globalCtrl, 3)
		self.createCtrl(self.orientCtrlShapeLs[0], "curve", self.orientCtrl, 3)
		setRGBColor(self.globalCtrl, (0, 0.85, 1))
		setRGBColor(self.orientCtrl, (0, 1, 0))
		globalRef = cmds.createNode("transform", name = self.globalCtrl + self.refSuf)
		orientRef = cmds.createNode("transform", name = self.orientCtrl + self.refSuf)
		cmds.parent(self.globalCtrl, globalRef)
		cmds.parent(self.orientCtrl, orientRef)
		cmds.parent(orientRef, self.globalCtrl)
		cmds.createNode("transform", name = self.CTRLname)
		cmds.parent(globalRef, self.CTRLname)
		cmds.createNode("transform", name = self.autoCtrl)
		autoRef = cmds.createNode("transform", name = self.autoCtrl + "_ref")
		cmds.parent(self.autoCtrl, autoRef)
		for i in xrange(len(self.autoCtrlShapeLs)):
			autoTemp = self.createCtrl(self.autoCtrlShapeLs[i], "curve", "autoTemp_" + str(i), 1)
			autoShape = cmds.listRelatives(autoTemp, children = True, shapes = True)[0]
			cmds.parent(autoShape, self.autoCtrl, r = True, s = True)
			cmds.delete(autoTemp)
		cmds.addAttr(self.autoCtrl, longName = "time", attributeType = "double")
		cmds.setAttr(self.autoCtrl + ".time", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".time", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "master_blend", min = 0, max = 1, attributeType = "double")
		cmds.setAttr(self.autoCtrl + ".master_blend", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_blend", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "master_delay", attributeType = "double")
		cmds.setAttr(self.autoCtrl + ".master_delay", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_delay", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "master_amp", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".master_amp", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_amp", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "master_speed", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".master_speed", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_speed", keyable = True)
		setRGBColor(self.autoCtrl, (0, 0.5, 1))
		cmds.parent(autoRef, self.orientCtrl)

		cogPos = cmds.xform(self.buildLs[0], q = True, ws = True, m = True)
		self.createCtrl(self.cogCtrlShapeLs[0], "curve", self.cogCtrl, 1)
		cogRef = cmds.createNode("transform", name = self.cogCtrl + self.refSuf)
		cmds.parent(self.cogCtrl, cogRef)
		cmds.xform(cogRef, m = cogPos, ws = True)
		cmds.parent(cogRef, self.orientCtrl)
		setRGBColor(cogCtrl, (1, 0.5, 0))
		cmds.delete(self.buildLs)



class genericComponent(object):


	def __init__(self, compName, secNum):
		self.compName = compName
		
		if  self.compName[:3] == "Lf_":
			self.side = "Lf"
		elif self.compName[:3] == "Rt_":
			self.side = "Rt"
		else:
			self.side = "M"

		self.secNum = secNum
		self.buildJntNum = secNum + 1
		self.buildSuf  = "_build"
		self.bnSuf = "_jnt"
		self.ctrlSuf ="_ctrl"
		self.autoSuf = "_auto"
		self.refSuf = "_ref"
		self.shaperSuf = "_shaper"
		self.CTRLname = self.compName + "_CTRL_GRP"
		self.RIGname = self.compName + "_RIG_GRP"

		self.buildLs = []
		for i in xrange(self.buildJntNum):
			self.buildLs += [self.compName + "_" +  str(i+1) + self.buildSuf]
		self.buildTransRotLs = [((0, 0, 0), (180, 90, 0))]
		for i in xrange(self.buildJntNum-1):
			self.buildTransRotLs += [((1, 0, 0), (0, 0, 0))]

		self.bnLs = []
		for  i in xrange(secNum):
			self.bnLs += [self.compName + "_" + str(i+1) + self.bnSuf]
		self.ctrlShape = [[4.7982373409884725e-17, 0.7836116248912246, -0.7836116248912245], [4.155062684684256e-33, 1.1081941875543877, -6.785732323110912e-17], [-4.7982373409884725e-17, 0.7836116248912244, 0.7836116248912245], [-6.785732323110915e-17, 5.74489823752483e-17, 1.1081941875543881], [-4.7982373409884725e-17, -0.7836116248912245, 0.7836116248912245], [-6.797314477808589e-33, -1.1081941875543884, 1.1100856969603225e-16], [4.7982373409884725e-17, -0.7836116248912244, -0.7836116248912245], [6.785732323110915e-17, -1.511240500779959e-16, -1.1081941875543881], [6.785732323110915e-17, -1.511240500779959e-16, -1.1081941875543881], [6.785732323110915e-17, -1.511240500779959e-16, -1.1081941875543881], [6.785732323110915e-17, -1.511240500779959e-16, -1.1081941875543881], [6.785732323110915e-17, -1.511240500779959e-16, -1.1081941875543881]]
		self.ctrlShapeLs = []
		for i in xrange(secNum):
			self.ctrlShapeLs += [self.ctrlShape]
		self.fkCtrlLs = []
		for i in xrange(secNum):
			self.fkCtrlLs += [self.compName + "_" + str(i+1) + self.ctrlSuf]

		self.autoCtrl = self.compName + self.autoSuf + self.ctrlSuf
		self.autoShape = [[0.0, 0.4072525915310115, 0.0], [0.0, 0.27150172768734115, -0.27150172768734115], [0.0, 0.0, -0.4072525915310115], [0.0, -0.27150172768734115, -0.27150172768734115], [0.0, -0.4072525915310115, 0.0], [0.0, -0.27150172768734115, 0.27150172768734115], [0.0, 0.0, 0.4072525915310115], [0.0, 0.27150172768734115, 0.27150172768734115], [0.0, 0.4072525915310115, 0.0], [0.27150172768734115, 0.27150172768734115, 0.0], [0.4072525915310115, 0.0, 0.0], [0.27150172768734115, -0.27150172768734115, 0.0], [0.0, -0.4072525915310115, 0.0], [-0.27150172768734115, -0.27150172768734115, 0.0], [-0.4072525915310115, 0.0, 0.0], [-0.27150172768734115, 0.27150172768734115, 0.0], [0.0, 0.4072525915310115, 0.0], [0.0, 0.4072525915310115, 0.0]]
		self.masterString = "float $blend = auto_ctrl.master_blend * COMPONENT_auto_ctrl.master_blend;\nfloat $freq = auto_ctrl.master_speed * COMPONENT_auto_ctrl.master_speed * COMPONENT_auto_ctrl.section_NUM_speed/12;\nfloat $delay = auto_ctrl.master_delay + COMPONENT_auto_ctrl.master_delay + COMPONENT_auto_ctrl.section_NUM_delay;\nfloat $amp = auto_ctrl.master_amp * COMPONENT_auto_ctrl.master_amp*5 *COMPONENT_auto_ctrl.section_NUM_amp;\nCOMPONENT_NUM_ctrl_auto.rotateY = sin((auto_ctrl.time * $freq) + $delay) * $amp * $blend;"

		self.shaperCtrl = self.compName + self.shaperSuf + self.ctrlSuf
		self.shaperShape = [[0.0, 0.12305783963900688, -0.12305783963900688], [0.0, 0.12305783963900688, -0.24611567927801375], [-6.831082346392785e-17, -0.12305783963900688, -0.24611567927801375], [-3.415541173196392e-17, -0.12305783963900688, -0.12305783963900688], [-8.197298815671341e-17, -0.24611567927801375, -0.12305783963900688], [-3.415541173196392e-17, -0.24611567927801375, 0.12305783963900688], [0.0, -0.12305783963900688, 0.12305783963900688], [0.0, -0.12305783963900688, 0.24611567927801375], [6.831082346392785e-17, 0.12305783963900688, 0.24611567927801375], [3.415541173196392e-17, 0.12305783963900688, 0.12305783963900688], [8.197298815671341e-17, 0.24611567927801375, 0.12305783963900688], [3.415541173196392e-17, 0.24611567927801375, -0.12305783963900688], [0.0, 0.12305783963900688, -0.12305783963900688], [0.0, 0.12305783963900688, -0.12305783963900688], [0.0, 0.12305783963900688, -0.12305783963900688]]
	


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

	def createCtrl(self, pointLs, shapeType, ctrlName):
		if shapeType == "circle":
			ctrl = cmds.circle(name = ctrlName)[0]
			for i in xrange(len(pointLs)):
				cmds.xform(ctrl+".cv[" + str(i) + "]", worldSpace = True, translation = pointLs[i])
			return ctrl
		else:
			ctrl = cmds.curve(point = pointLs, name = ctrlName, degree = 1)
			return ctrl

	def getFkCtrlTrans(self):
		rst = []
		for i in xrange(len(self.buildLs)):
			m = cmds.xform(self.buildLs[i], query = True, matrix = True, worldSpace = True)
			if self.side == "Rt":
				print "noooo"
				cmds.select(clear = True)
				temp = cmds.createNode("transform")
				cmds.xform(temp, matrix = m, worldSpace = True)
				cmds.setAttr(temp + ".rotateX", -cmds.getAttr(temp + ".rotateX"))
				cmds.setAttr(temp + ".rotateY", -cmds.getAttr(temp + ".rotateY"))
				cmds.setAttr(temp + ".rotateZ", 180+cmds.getAttr(temp + ".rotateZ"))
				cmds.setAttr(temp+".scaleZ", -1)
				m = cmds.xform(temp, worldSpace = True, matrix = True, query = True)
				cmds.delete(temp)
			rst += [m]
		return rst

	def build(self):
		cmds.select(clear = True)
		self.createJointChain(self.buildLs, self.buildTransRotLs)


	def finish(self):
		# create bind chain
		tarnsLs = self.getTransRotLs(self.buildLs)

		# create ctrl chain
		self.createJointChain(self.bnLs, tarnsLs)
		fkTransLs = self.getFkCtrlTrans()
		for i in xrange(self.secNum):
			cmds.select(clear = True)
			crtCtrl = self.createCtrl(self.ctrlShape, "circle", self.fkCtrlLs[i])
			crtAuto = cmds.createNode("transform", name = self.fkCtrlLs[i] + "_auto")
			cmds.select(clear = True)
			crtRef = cmds.createNode("transform", name = self.fkCtrlLs[i] + "_ref")
			cmds.select(clear = True)
			cmds.parent(crtCtrl, crtAuto)
			cmds.parent(crtAuto, crtRef)
			cmds.xform(crtRef, matrix = fkTransLs[i], ws = True)
			if (i != 0):
				cmds.parent(crtRef, self.fkCtrlLs[i-1])
			setRGBColor(crtCtrl, (1, 1, 0))

		# create auto ctrl
		self.createCtrl(self.autoShape, "curve", self.autoCtrl)
		autoRef = cmds.createNode("transform", name = self.autoCtrl + "_ref")
		cmds.parent(self.autoCtrl, autoRef)
		cmds.xform(autoRef, matrix = fkTransLs[0], ws = True)
		cmds.parent(autoRef, self.fkCtrlLs[0])
		setRGBColor(self.autoCtrl, (0, 0.5, 1))
		

		# create master attributes
		cmds.addAttr(self.autoCtrl, longName = "master_blend", min = 0, max = 1, attributeType = "double", defaultValue = 0)
		cmds.setAttr(self.autoCtrl + ".master_blend", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_blend", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "master_delay", attributeType = "double", defaultValue = 0)
		cmds.setAttr(self.autoCtrl + ".master_delay", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_delay", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "master_amp", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".master_amp", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_amp", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "master_speed", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".master_speed", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_speed", keyable = True)

		# createshaper ctrl
		self.createCtrl(self.shaperShape, "curve", self.shaperCtrl)
		shaperRef = cmds.createNode("transform", name = self.shaperCtrl + "_ref")
		cmds.parent(self.shaperCtrl, shaperRef)
		cmds.xform(shaperRef, matrix = fkTransLs[0], ws = True)
		cmds.parent(shaperRef, self.fkCtrlLs[0])
		addShaper(self.shaperCtrl, self.compName, self.secNum)
		setRGBColor(self.shaperCtrl, (1, 0.5, 0.5))

		for i in xrange(self.secNum):
			attrName = "section_" + str(i+1)
			cmds.addAttr(self.autoCtrl, attributeType = "enum", 
					longName = attrName, enumName = "_________")
			cmds.setAttr(self.autoCtrl + "." + attrName, lock = True, channelBox = True)
			cmds.setAttr(self.autoCtrl + "." + attrName , keyable = False)
			delayAttrName = "section_" + str(i+1) + "_delay"
			cmds.addAttr(self.autoCtrl, longName = delayAttrName, attributeType = "double", defaultValue = i)
			cmds.setAttr(self.autoCtrl + "." + delayAttrName , lock = False, channelBox = True)
			cmds.setAttr(self.autoCtrl + "." + delayAttrName, keyable = True)

			ampAttrName = "section_" + str(i+1) + "_amp"
			cmds.addAttr(self.autoCtrl, longName = ampAttrName, attributeType = "double", defaultValue = (i+1) * 0.1)
			cmds.setAttr(self.autoCtrl + "." + ampAttrName , lock = False, channelBox = True)
			cmds.setAttr(self.autoCtrl + "." + ampAttrName, keyable = True)

			speedAttrName = "section_" + str(i+1) + "_speed"
			cmds.addAttr(self.autoCtrl, longName = speedAttrName, attributeType = "double", defaultValue = 1)
			cmds.setAttr(self.autoCtrl + "." + speedAttrName , lock = False, channelBox = True)
			cmds.setAttr(self.autoCtrl + "." + speedAttrName, keyable = True)

		addAutoRotate(self.masterString, "COMPONENT", self.compName, "NUM", self.secNum)

		cmds.select(clear = True)
		ctrlGrp = cmds.createNode("transform", name = self.CTRLname)
		cmds.parent(self.fkCtrlLs[0] + self.refSuf, ctrlGrp)
		cmds.select(clear = True)
		rigGrp = cmds.joint(name = self.RIGname)
		cmds.parent(self.bnLs[0], rigGrp)

		# add parent and scale constraint
		for i in xrange(self.secNum):
			cmds.parentConstraint(self.fkCtrlLs[i], self.bnLs[i], mo = True)
			cmds.scaleConstraint(self.fkCtrlLs[i], self.bnLs[i], mo = True)

		cmds.delete(self.buildLs)

	def rebuild(self):
		transRotLs = self.getTransRotLs(self.bnLs)
		transRotLs += [((0, 0, 0), (0, 0, 0))]
		self.createJointChain(self.buildLs, transRotLs)

def mirrorGeneric(compName, secNum):
	comp = genericComponent(compName, secNum)
	comp.rebuild()
	side = compName[:2]
	if side == "Lf":
		crtMirror = cmds.mirrorJoint(comp.buildLs[0], mirrorYZ = True, mirrorBehavior = True, searchReplace = ["Lf", "Rt"])[0]
		crt = genericComponent("Rt" + compName[2:], secNum)
		crt.finish()
	else:
		crtMirror = cmds.mirrorJoint(comp.buildLs[0], mirrorYZ = True, mirrorBehavior = True, searchReplace = ["Rt", "Lf"])[0]
		crt = genericComponent("Lf" + compName[2:], secNum)
		crt.finish()
	cmds.delete(comp.buildLs)




class head(object):

	def getTransRotLs(self, jntLs):
		rstLs = []
		for i in xrange(len(jntLs)):
			crtAttrLs = []
			crtAttrLs += [cmds.getAttr(jntLs[i] + ".translate")[0]]
			crtAttrLs += [cmds.getAttr(jntLs[i] + ".jointOrient")[0]]
			rstLs += [crtAttrLs]
		return rstLs

	def setTransRotLs(self, jntLs, attrLs):
		for i in xrange(len(jntLs)):
			cmds.setAttr(jntLs[i] + ".translate", attrLs[i][0][0], attrLs[i][0][1], attrLs[i][0][2], type = "double3")
			cmds.setAttr(jntLs[i] + ".jointOrient", attrLs[i][1][0], attrLs[i][1][1], attrLs[i][1][2], type = "double3")
			cmds.setAttr(jntLs[i] + ".rotate", 0,0,0, type = "double3")
			cmds.setAttr(jntLs[i] + ".scale", 1,1,1, type = "double3")

	def createCtrl(self, pointLs, shapeType, ctrlName):
		if shapeType == "circle":
			ctrl = cmds.circle(name = ctrlName)[0]
			for i in xrange(len(pointLs)):
				cmds.xform(ctrl+".cv[" + str(i) + "]", worldSpace = True, translation = pointLs[i])
			return ctrl
		else:
			ctrl = cmds.curve(point = pointLs, name = ctrlName, degree = 1)
			return ctrl

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
	def __init__(self):
		self.compName = "head"
		self.buildSuf = "_build"
		self.secNum = 2
		self.buildJntNum = self.secNum + 1
		self.jawPrefixLs = ["jaw_upper", "jaw_lower"]
		self.tipPrefix = "_tip"
		self.gillPrefixLs = ["Lf_gill"]
		self.rtGillPrefixLs = ["Rt_grill"]
		self.jawBuildLs = []
		self.jawTipBuildLs = []
		self.bnSuf = "_jnt"
		self.ctrlSuf = "_ctrl"
		self.refSuf = "_ref"
		self.autoSuf = "_auto"
		self.shaperSuf = "_shaper"
		self.CTRLname = self.compName + "_CTRL_GRP"
		self.RIGname = self.compName + "_RIG_GRP"


		for i in xrange(len(self.jawPrefixLs)):
			self.jawBuildLs += [self.jawPrefixLs[i] + self.buildSuf]
			self.jawTipBuildLs += [self.jawPrefixLs[i] + self.tipPrefix + self.buildSuf]
		

		self.gillBuildLs = []
		self.gillTipBuildLs = []
		for i in xrange(len(self.gillPrefixLs)):
			self.gillBuildLs +=[self.gillPrefixLs[i] + self.buildSuf]
			self.gillTipBuildLs += [self.gillPrefixLs[i] + self.tipPrefix + self.buildSuf] 
		self.headBuildLs = []
		for i in xrange(self.buildJntNum):
			self.headBuildLs += [self.compName + "_" + str(i+1) + self.buildSuf]

		self.headBuildTransRotLs = [((0, 0, 0), (0, -90, 0))]
		for i in xrange(self.buildJntNum-1):
			self.headBuildTransRotLs += [((1, 0, 0), (0, 0, 0))]

		self.jawBuildTransRotLs = [((0.401, 0, 0), (0, 0, 30)), ((0.401, -0.132, 0), (0, 0, 0))]
		self.gillBuildTransRotLs = [((0.339, 0, -0.384), (0, 160, 0))]

		self.jawBnLs = []
		self.jawCtrlLs = []
		for i in xrange(len(self.jawPrefixLs)):
			self.jawBnLs += [self.jawPrefixLs[i] + self.bnSuf]
			self.jawCtrlLs += [self.jawPrefixLs[i] + self.ctrlSuf]
		self.gillBnLs = [self.gillPrefixLs[0] + self.bnSuf]
		self.gillCtrlLs = [self.gillPrefixLs[0] + self.ctrlSuf]
		self.rtGillCtrlLs = [self.rtGillPrefixLs[0] + self.ctrlSuf]

		self.headCtrlLs = []
		self.headBnLs = []
		for i in xrange(self.secNum):
			self.headBnLs += [self.compName + "_" + str(i+1) + self.bnSuf]
			self.headCtrlLs += [self.compName + "_" + str(i+1) + self.ctrlSuf]

		self.headCtrlShapeLs = [[[0.24424134321270735, -0.7694195822328146, 0.4568777859683162], [0.24593941651044599, 0.6484609783471149, 0.4568777859683162], [0.24593941651044599, 0.6484609783471149, -0.4568777859683162], [0.24424134321270735, -0.7694195822328146, -0.4568777859683162], [0.24424134321270735, -0.7694195822328146, 0.4568777859683162], [0.24424134321270735, -0.7694195822328146, 0.4568777859683162]], [[0.07994014468667704, -0.6942101581939167, 0.38605220750935804], [0.08163821798441567, 0.5850750471603137, 0.38605220750935804], [0.08163821798441567, 0.5850750471603137, -0.38605220750935804], [0.07994014468667704, -0.6942101581939167, -0.38605220750935804], [0.07994014468667704, -0.6942101581939167, 0.38605220750935804], [0.07994014468667704, -0.6942101581939167, 0.38605220750935804]]]
		self.gillCtrlShapeLs = [[[0.34429350829745364, 0.2586236197253903, 0.08052508552033154], [0.30539567654255984, -0.2586236197253903, 0.10792686908613491], [0.1726396991601099, -0.46826454325832273, -0.0805250855203319], [0.2115375309150037, 0.46826454325832273, -0.10792686908613533], [0.34429350829745364, 0.2586236197253903, 0.08052508552033154], [0.34429350829745364, 0.2586236197253903, 0.08052508552033154]]]
		self.jawCtrlShapeLs = [[[0.20496979762658663, 0.2654861937040582, 0.16209816510443523], [0.44299483007210216, -0.02000690318290629, 0.061384585555537684], [0.44299483007210216, -0.02000690318290629, -0.061384585555537684], [0.20496979762658663, 0.2654861937040582, -0.16209816510443523], [0.20496979762658663, 0.2654861937040582, 0.16209816510443523], [0.06091989319150838, 0.03859841125016042, 0.332128410460509], [0.06091989319150838, 0.03859841125016042, -0.332128410460509], [0.38823565275532884, -0.1509141026092611, -0.061384585555537684], [0.38823565275532884, -0.1509141026092611, 0.061384585555537684], [0.06091989319150838, 0.03859841125016042, 0.332128410460509], [0.38823565275532884, -0.1509141026092611, 0.061384585555537684], [0.44299483007210216, -0.02000690318290629, 0.061384585555537684], [0.44299483007210216, -0.02000690318290629, -0.061384585555537684], [0.38823565275532884, -0.1509141026092611, -0.061384585555537684], [0.06091989319150838, 0.03859841125016042, -0.332128410460509], [0.20496979762658663, 0.2654861937040582, -0.16209816510443523], [0.20496979762658663, 0.2654861937040582, -0.16209816510443523]], [[0.11070407270799235, 0.05519623612088831, 0.2692413437693746], [0.39968962152361254, -0.14041670365469985, 0.08300142208316369], [0.39968962152361254, -0.14041670365469985, -0.08300142208316369], [0.11070407270799235, 0.05519623612088831, -0.2692413437693746], [0.11070407270799235, 0.05519623612088831, 0.2692413437693746], [-0.09093821350321367, -0.17627421192253245, 0.13808872934931407], [-0.09093821350321367, -0.17627421192253245, -0.13808872934931407], [0.3239809676169649, -0.20959853180748478, -0.08300142208316369], [0.3239809676169649, -0.20959853180748478, 0.08300142208316369], [-0.09093821350321367, -0.17627421192253245, 0.13808872934931407], [0.3239809676169649, -0.20959853180748478, 0.08300142208316369], [0.39968962152361254, -0.14041670365469985, 0.08300142208316369], [0.39968962152361254, -0.14041670365469985, -0.08300142208316369], [0.3239809676169649, -0.20959853180748478, -0.08300142208316369], [-0.09093821350321367, -0.17627421192253245, -0.13808872934931407], [0.11070407270799235, 0.05519623612088831, -0.2692413437693746], [0.11070407270799235, 0.05519623612088831, -0.2692413437693746]]]


		self.autoCtrl = self.compName + self.autoSuf + self.ctrlSuf
		self.autoShape = [[0.0, 0.4072525915310115, 0.0], [0.0, 0.27150172768734115, -0.27150172768734115], [0.0, 0.0, -0.4072525915310115], [0.0, -0.27150172768734115, -0.27150172768734115], [0.0, -0.4072525915310115, 0.0], [0.0, -0.27150172768734115, 0.27150172768734115], [0.0, 0.0, 0.4072525915310115], [0.0, 0.27150172768734115, 0.27150172768734115], [0.0, 0.4072525915310115, 0.0], [0.27150172768734115, 0.27150172768734115, 0.0], [0.4072525915310115, 0.0, 0.0], [0.27150172768734115, -0.27150172768734115, 0.0], [0.0, -0.4072525915310115, 0.0], [-0.27150172768734115, -0.27150172768734115, 0.0], [-0.4072525915310115, 0.0, 0.0], [-0.27150172768734115, 0.27150172768734115, 0.0], [0.0, 0.4072525915310115, 0.0], [0.0, 0.4072525915310115, 0.0]]
		self.masterString = "float $blend = auto_ctrl.master_blend * COMPONENT_auto_ctrl.master_blend;\nfloat $freq = auto_ctrl.master_speed * COMPONENT_auto_ctrl.master_speed * COMPONENT_auto_ctrl.section_NUM_speed/12;\nfloat $delay = auto_ctrl.master_delay + COMPONENT_auto_ctrl.master_delay + COMPONENT_auto_ctrl.section_NUM_delay;\nfloat $amp = auto_ctrl.master_amp * COMPONENT_auto_ctrl.master_amp*5 *COMPONENT_auto_ctrl.section_NUM_amp;\nCOMPONENT_NUM_ctrl_auto.rotateY = sin((auto_ctrl.time * $freq) + $delay) * $amp * $blend;"

		self.shaperCtrl = self.compName + self.shaperSuf + self.ctrlSuf
		self.shaperShape = [[0.0, 0.12305783963900688, -0.12305783963900688], [0.0, 0.12305783963900688, -0.24611567927801375], [-6.831082346392785e-17, -0.12305783963900688, -0.24611567927801375], [-3.415541173196392e-17, -0.12305783963900688, -0.12305783963900688], [-8.197298815671341e-17, -0.24611567927801375, -0.12305783963900688], [-3.415541173196392e-17, -0.24611567927801375, 0.12305783963900688], [0.0, -0.12305783963900688, 0.12305783963900688], [0.0, -0.12305783963900688, 0.24611567927801375], [6.831082346392785e-17, 0.12305783963900688, 0.24611567927801375], [3.415541173196392e-17, 0.12305783963900688, 0.12305783963900688], [8.197298815671341e-17, 0.24611567927801375, 0.12305783963900688], [3.415541173196392e-17, 0.24611567927801375, -0.12305783963900688], [0.0, 0.12305783963900688, -0.12305783963900688], [0.0, 0.12305783963900688, -0.12305783963900688], [0.0, 0.12305783963900688, -0.12305783963900688]]
	



	def build(self):
		cmds.select(clear = True)
		for i in xrange(self.buildJntNum):
			cmds.joint(name = self.headBuildLs[i])
		self.setTransRotLs(self.headBuildLs, self.headBuildTransRotLs)

		cmds.select(clear = True)
		for i in xrange(len(self.jawBuildLs)):
			cmds.joint(name = self.jawBuildLs[i])
			cmds.joint(name = self.jawTipBuildLs[i])
			cmds.setAttr(self.jawTipBuildLs[i] + ".translate", 1, 0, 0, type = "double3")
		cmds.parent(self.jawBuildLs, self.headBuildLs[1])
		self.setTransRotLs(self.jawBuildLs, self.jawBuildTransRotLs)

		cmds.select(clear = True)
		cmds.joint(name = self.gillBuildLs[0])
		cmds.joint(name = self.gillTipBuildLs[0])
		cmds.setAttr(self.gillTipBuildLs[0] + ".translate", 1, 0, 0, type = "double3")
		cmds.parent(self.gillBuildLs[0], self.headBuildLs[0])
		self.setTransRotLs(self.gillBuildLs, self.gillBuildTransRotLs)


	def finish(self):
		
		self.headBnTransRotLs = self.getTransRotLs(self.headBuildLs)[:-1]
		self.createJointChain(self.headBnLs, self.headBnTransRotLs)
		
		self.jawBnTransRotLs = self.getTransRotLs(self.jawBuildLs)
		for i in xrange(len(self.jawBnLs)):
			cmds.select(clear = True)
			cmds.joint(name = self.jawBnLs[i])
			cmds.parent(self.jawBnLs[i], self.headBnLs[-1])
		self.setTransRotLs(self.jawBnLs, self.jawBnTransRotLs)

		self.gillBnTransRotLs = self.getTransRotLs(self.gillBuildLs)
		cmds.select(clear = True)
		cmds.joint(name = self.gillBnLs[0])
		cmds.parent(self.gillBnLs[0], self.headBnLs[0])
		self.setTransRotLs(self.gillBnLs, self.gillBnTransRotLs)

		self.rtGillBnLs = cmds.mirrorJoint(self.gillBnLs[0], mirrorYZ = True, mirrorBehavior = True, searchReplace = ["Lf", "Rt"])

		headRootCtrlMat = ()
		# create fk ctrl
		for i in xrange(self.secNum):
			crtCtrl = self.createCtrl(self.headCtrlShapeLs[i], "curve", self.headCtrlLs[i])
			cmds.select(clear = True)
			crtAuto = cmds.createNode("transform", name = self.headCtrlLs[i] + "_auto")
			cmds.select(clear = True)
			crtRef = cmds.createNode("transform", name = self.headCtrlLs[i] + "_ref")
			cmds.parent(crtCtrl, crtAuto)
			cmds.parent(crtAuto, crtRef)
			crtMat = cmds.xform(self.headBnLs[i], q= True, m = True, ws = True)
			if i == 0:
				headRootCtrlMat = crtMat
			if i != 0:
				cmds.parent(crtRef, self.headCtrlLs[i-1])
			cmds.xform(crtRef, m = crtMat, ws = True)

		# create gill ctrl
		self.createCtrl(self.gillCtrlShapeLs[0], "curve", self.gillCtrlLs[0])
		cmds.select(clear = True)
		gillAuto = cmds.createNode("transform", name = self.gillCtrlLs[0] + "_auto")
		cmds.select(clear = True)
		gillRef = cmds.createNode("transform", name = self.gillCtrlLs[0] + self.refSuf)
		cmds.parent(self.gillCtrlLs[0], gillAuto)
		cmds.parent(gillAuto, gillRef)
		gillMatrix = cmds.xform(self.gillBnLs[0], q = True, m = True, ws = True)
		cmds.xform(gillRef, m = gillMatrix, ws = True)
		cmds.parent(gillRef, self.headCtrlLs[0])
		
		cmds.select(clear = True)
		temp = cmds.createNode("transform")
		rtTempMatrix = cmds.xform(self.rtGillBnLs[0], m = True, ws = True, q = True)
		cmds.xform(temp, matrix = rtTempMatrix, worldSpace = True)
		cmds.setAttr(temp + ".rotateX", -cmds.getAttr(temp + ".rotateX"))
		cmds.setAttr(temp + ".rotateY", -cmds.getAttr(temp + ".rotateY"))
		cmds.setAttr(temp + ".rotateZ", 180+cmds.getAttr(temp + ".rotateZ"))
		cmds.setAttr(temp+".scaleZ", -1)
		rtGillMatrix = cmds.xform(temp, worldSpace = True, matrix = True, query = True)
		cmds.delete(temp)

		self.createCtrl(self.gillCtrlShapeLs[0], "curve", self.rtGillCtrlLs[0])
		cmds.select(clear = True)
		rtGillAuto = cmds.createNode("transform", name = self.rtGillCtrlLs[0] + "_auto")
		cmds.select(clear = True)
		rtGillRef = cmds.createNode("transform", name = self.rtGillCtrlLs[0] + self.refSuf)
		cmds.parent(self.rtGillCtrlLs[0], rtGillAuto)
		cmds.parent(rtGillAuto, rtGillRef)
		cmds.xform(rtGillRef, m = rtGillMatrix, ws = True)
		cmds.parent(rtGillRef, self.headCtrlLs[0])

		for i in xrange(len(self.jawCtrlLs)):
			self.createCtrl(self.jawCtrlShapeLs[i], "curve", self.jawCtrlLs[i])
			cmds.select(clear = True)
			crtAuto = cmds.createNode("transform", name = self.jawCtrlLs[i] + "_auto")
			cmds.select(clear = True)
			crtRef = cmds.createNode("transform", name = self.jawCtrlLs[i] + self.refSuf)
			cmds.select(clear = True)
			cmds.parent(self.jawCtrlLs[i], crtAuto)
			cmds.parent(crtAuto, crtRef)
			cmds.parent(crtRef, self.headCtrlLs[-1])
			crtMatrix = cmds.xform(self.jawBnLs[i], q = True, ws = True, m = True)
			cmds.xform(crtRef, ws = True, m = crtMatrix)

		# create auto ctrl
		self.createCtrl(self.autoShape, "curve", self.autoCtrl)
		autoRef = cmds.createNode("transform", name = self.autoCtrl + "_ref")
		cmds.parent(self.autoCtrl, autoRef)
		cmds.xform(autoRef, matrix = headRootCtrlMat, ws = True)
		cmds.parent(autoRef, self.headCtrlLs[0])
		setRGBColor(self.autoCtrl, (0, 0.5, 1))
		

		# create master attributes
		cmds.addAttr(self.autoCtrl, longName = "master_blend", min = 0, max = 1, attributeType = "double", defaultValue = 0)
		cmds.setAttr(self.autoCtrl + ".master_blend", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_blend", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "master_delay", attributeType = "double", defaultValue = 0)
		cmds.setAttr(self.autoCtrl + ".master_delay", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_delay", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "master_amp", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".master_amp", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_amp", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "master_speed", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".master_speed", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".master_speed", keyable = True)

		# create gill attributes
		cmds.addAttr(self.autoCtrl, attributeType = "enum", 
					longName = "Lf_gill", enumName = "_________")
		cmds.setAttr(self.autoCtrl + ".Lf_gill", lock = True, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".Lf_gill" , keyable = False)
		cmds.addAttr(self.autoCtrl, longName = "Lf_gill_delay", attributeType = "double", defaultValue = 0)
		cmds.setAttr(self.autoCtrl + ".Lf_gill_delay", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".Lf_gill_delay", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "Lf_gill_amp", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".Lf_gill_amp", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".Lf_gill_amp", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "Lf_gill_speed", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".Lf_gill_speed", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".Lf_gill_speed", keyable = True)

		cmds.addAttr(self.autoCtrl, attributeType = "enum", 
					longName = "Rt_gill", enumName = "_________")
		cmds.setAttr(self.autoCtrl + ".Rt_gill", lock = True, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".Rt_gill" , keyable = False)
		cmds.addAttr(self.autoCtrl, longName = "Rt_gill_delay", attributeType = "double", defaultValue = 0)
		cmds.setAttr(self.autoCtrl + ".Rt_gill_delay", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".Rt_gill_delay", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "Rt_gill_amp", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".Rt_gill_amp", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".Rt_gill_amp", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "Rt_gill_speed", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".Rt_gill_speed", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".Rt_gill_speed", keyable = True) 


		# add jaw attributes
		cmds.addAttr(self.autoCtrl, attributeType = "enum", 
					longName = "upper_jaw", enumName = "_________")
		cmds.setAttr(self.autoCtrl + ".upper_jaw", lock = True, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".upper_jaw" , keyable = False)
		cmds.addAttr(self.autoCtrl, longName = "upper_jaw_delay", attributeType = "double", defaultValue = 0)
		cmds.setAttr(self.autoCtrl + ".upper_jaw_delay", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".upper_jaw_delay", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "upper_jaw_amp", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".upper_jaw_amp", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".upper_jaw_amp", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "upper_jaw_speed", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".upper_jaw_speed", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".upper_jaw_speed", keyable = True)

		cmds.addAttr(self.autoCtrl, attributeType = "enum", 
					longName = "lower_jaw", enumName = "_________")
		cmds.setAttr(self.autoCtrl + ".lower_jaw", lock = True, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".lower_jaw" , keyable = False)
		cmds.addAttr(self.autoCtrl, longName = "lower_jaw_delay", attributeType = "double", defaultValue = 0)
		cmds.setAttr(self.autoCtrl + ".lower_jaw_delay", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".lower_jaw_delay", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "lower_jaw_amp", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".lower_jaw_amp", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".lower_jaw_amp", keyable = True)
		cmds.addAttr(self.autoCtrl, longName = "lower_jaw_speed", attributeType = "double", defaultValue = 1)
		cmds.setAttr(self.autoCtrl + ".lower_jaw_speed", lock = False, channelBox = True)
		cmds.setAttr(self.autoCtrl + ".lower_jaw_speed", keyable = True)

		# connect to auto control

		# 
		cmds.select(clear = True)
		ctrlGrp = cmds.createNode("transform", name = self.CTRLname)
		cmds.parent(self.headCtrlLs[0] + self.refSuf, ctrlGrp)
		cmds.select(clear = True)
		rigGrp = cmds.joint(name = self.RIGname)
		cmds.parent(self.headBnLs[0], rigGrp)

		# add parent and scale constraint
		for i in xrange(self.secNum):
			cmds.parentConstraint(self.headCtrlLs[i], self.headBnLs[i], mo = True)
			cmds.scaleConstraint(self.headCtrlLs[i], self.headBnLs[i], mo = True)
		cmds.parentConstraint(self.gillCtrlLs[0], self.gillBnLs[0], mo = True)
		cmds.scaleConstraint(self.gillCtrlLs[0], self.gillBnLs[0], mo = True)
		cmds.parentConstraint(self.rtGillCtrlLs[0], self.rtGillBnLs[0], mo = True)
		cmds.scaleConstraint(self.rtGillCtrlLs[0], self.rtGillBnLs[0], mo = True)
		for i in xrange(len(self.jawCtrlLs)):
			cmds.parentConstraint(self.jawCtrlLs[i], self.jawBnLs[i], mo = True)
			cmds.scaleConstraint(self.jawCtrlLs[i], self.jawBnLs[i], mo = True)
		cmds.delete(self.jawBuildLs)
		cmds.delete(self.gillBuildLs)
		cmds.delete(self.headBuildLs)

# headComp = head()
# headComp.build()
# headComp.finish()





def placerBuildButtonWrapper(*args):
	placerComp = placer()
	placerComp.build()

def placerFinalButtonWrapper(*args):
	placerComp = placer()
	placerComp.finish()



def genericBuildButtonWrapper(nameField, numField, *args):
	compName = cmds.textField(nameField, q = True, text = True)
	secNum = int(cmds.textField(numField, q = True, text = True))
	genericComp = genericComponent(compName, secNum)
	genericComp.build()
	return None


def genericFinalButtonWrapper(nameField, numField, *args):
	compName = cmds.textField(nameField, q = True, text = True)
	secNum = int(cmds.textField(numField, q = True, text = True))
	genericComp = genericComponent(compName, secNum)
	genericComp.finish()
	return None

def genericMirrorButtonWrapper(nameField, numField, *args):
	compName = cmds.textField(nameField, q = True, text = True)
	secNum = int(cmds.textField(numField, q = True, text = True))
	mirrorGeneric(compName, secNum)
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
	buildingButtonLs = insertButtonSet(1, 2, 30, (WIDTH-BORDERWIDTH*2)*0.5, 
		["Build", "Final"], colorLs =  [(0.7, 0.7, 0.7),(0.6, 0.6, 0.6)])
	addButtonCmds(buildingButtonLs, [
		partial(placerBuildButtonWrapper),
		partial(placerFinalButtonWrapper)
		])

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
	 	partial(genericFinalButtonWrapper, nameTextFieldLs[0], numTextFieldLs[0]),
	 	partial(genericMirrorButtonWrapper, nameTextFieldLs[0], numTextFieldLs[0]),
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