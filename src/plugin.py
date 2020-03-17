# -*- coding: utf-8 -*-
# by einfall, pclin & Sven_H for DreamOS

from Components.config import config, ConfigSelectionNumber, ConfigInteger, ConfigYesNo, ConfigIP, ConfigSelection, ConfigSubsection, NoSave, ConfigText
from Plugins.Plugin import PluginDescriptor
from os import system as os_system

from hyperioncontrol import _, hyperionStart, hyperioncontrol_version, send_CMD

config.plugins.hyperioncontrol = ConfigSubsection()
config.plugins.hyperioncontrol.saturationGain = NoSave(ConfigSelectionNumber(0,500,1,default = 100))
config.plugins.hyperioncontrol.valueGain = NoSave(ConfigSelectionNumber(0,500,1,default = 100))
config.plugins.hyperioncontrol.saturationLGain = NoSave(ConfigSelectionNumber(0,100,1,default = 100))
config.plugins.hyperioncontrol.luminanceGain = NoSave(ConfigSelectionNumber(0,100,1,default = 100))
config.plugins.hyperioncontrol.luminanceMinimum = NoSave(ConfigSelectionNumber(0,50,1,default = 0))
config.plugins.hyperioncontrol.gammaRed = NoSave(ConfigSelectionNumber(0,500,1,default = 250))
config.plugins.hyperioncontrol.gammaGreen = NoSave(ConfigSelectionNumber(0,500,1,default = 250))
config.plugins.hyperioncontrol.gammaBlue = NoSave(ConfigSelectionNumber(0,500,1,default = 250))
config.plugins.hyperioncontrol.thresholdRed = NoSave(ConfigSelectionNumber(0,100,1,default = 0))
config.plugins.hyperioncontrol.thresholdGreen = NoSave(ConfigSelectionNumber(0,100,1,default = 0))
config.plugins.hyperioncontrol.thresholdBlue = NoSave(ConfigSelectionNumber(0,100,1,default = 0))
config.plugins.hyperioncontrol.temperatureRed = NoSave(ConfigSelectionNumber(0,255,1,default = 255))
config.plugins.hyperioncontrol.temperatureGreen = NoSave(ConfigSelectionNumber(0,255,1,default = 255))
config.plugins.hyperioncontrol.temperatureBlue = NoSave(ConfigSelectionNumber(0,255,1,default = 255))
config.plugins.hyperioncontrol.redAdjustRed = NoSave(ConfigSelectionNumber(255,255,1,default = 255))
config.plugins.hyperioncontrol.redAdjustGreen = NoSave(ConfigSelectionNumber(0,255,1,default = 0))
config.plugins.hyperioncontrol.redAdjustBlue = NoSave(ConfigSelectionNumber(0,255,1,default = 0))
config.plugins.hyperioncontrol.greenAdjustRed = NoSave(ConfigSelectionNumber(0,255,1,default = 0))
config.plugins.hyperioncontrol.greenAdjustGreen = NoSave(ConfigSelectionNumber(255,255,1,default = 255))
config.plugins.hyperioncontrol.greenAdjustBlue = NoSave(ConfigSelectionNumber(0,255,1,default = 0))
config.plugins.hyperioncontrol.blueAdjustRed = NoSave(ConfigSelectionNumber(0,255,1,default = 0))
config.plugins.hyperioncontrol.blueAdjustGreen = NoSave(ConfigSelectionNumber(0,255,1,default = 0))
config.plugins.hyperioncontrol.blueAdjustBlue = NoSave(ConfigSelectionNumber(255,255,1,default = 255))
config.plugins.hyperioncontrol.whitelevelRed = NoSave(ConfigSelectionNumber(0,100,1,default = 100))
config.plugins.hyperioncontrol.whitelevelGreen = NoSave(ConfigSelectionNumber(0,100,1,default = 100))
config.plugins.hyperioncontrol.whitelevelBlue = NoSave(ConfigSelectionNumber(0,100,1,default = 100))
config.plugins.hyperioncontrol.blacklevelRed = NoSave(ConfigSelectionNumber(0,50,1,default = 0))
config.plugins.hyperioncontrol.blacklevelGreen = NoSave(ConfigSelectionNumber(0,50,1,default = 0))
config.plugins.hyperioncontrol.blacklevelBlue = NoSave(ConfigSelectionNumber(0,50,1,default = 0))
config.plugins.hyperioncontrol.bbdEnable = NoSave(ConfigYesNo(default = True))
config.plugins.hyperioncontrol.bbdThreshold = NoSave(ConfigSelectionNumber(1,20,1,default = 4))
config.plugins.hyperioncontrol.smoothingupdateFrequency = ConfigSelection(choices=[("1","1 Hz"),("5","5 Hz"),("10","10 Hz"),("15","15 Hz"),("20","20 Hz"),("25","25 Hz"),("30","30 Hz")], default = "20")
config.plugins.hyperioncontrol.framegrabberSize = NoSave(ConfigSelection(choices=[("160,160","160x160"),("320,320","320x320"),("384,216","384x216"),("640,640","640x640"),("720,576","720x576"),("720,720","720x720"),("1280,720","1280x720"),("1080,1080","1080x1080"),("1920,1080","1920x1080")], default = "160,160"))
config.plugins.hyperioncontrol.framegrabberFreq = NoSave(ConfigSelectionNumber(5,30,5,default = 10))
config.plugins.hyperioncontrol.webConfigEnable = NoSave(ConfigYesNo(default = True))
config.plugins.hyperioncontrol.webConfigPort   = NoSave(ConfigInteger(default = 8099, limits=(1, 65535) ))
config.plugins.hyperioncontrol.bootseqStart = NoSave(ConfigSelection(choices=[("color",_("Color")),("effect",_("Effect")),("off",_("off"))],default = "effect"))
config.plugins.hyperioncontrol.bootseqColor = NoSave(ConfigSelection(choices=[("#FFFFFF","")],default = "#FFFFFF"))
config.plugins.hyperioncontrol.bootseqEffect = NoSave(ConfigSelection(choices=[("Rainbow swirl fast","Rainbow swirl fast")],default = "Rainbow swirl fast"))
config.plugins.hyperioncontrol.bootseqDuration = NoSave(ConfigSelectionNumber(0,10000,500,default = 3000))
config.plugins.hyperioncontrol.onIdleAction = ConfigSelection(choices=[("color",_("Color")),("effect",_("Effect")),("nothing",_("nothing"))],default = "nothing")
config.plugins.hyperioncontrol.onIdleColor = ConfigText("#FFFFFF", False)
config.plugins.hyperioncontrol.onIdleEffect = ConfigText("Rainbow swirl fast", False)
config.plugins.hyperioncontrol.onIdlebackAction = ConfigSelection(choices=[("live",_("live mode")),("color",_("Color")),("effect",_("Effect")),("nothing",_("nothing"))],default = "nothing")
config.plugins.hyperioncontrol.onIdlebackColor = ConfigText("#FFFFFF", False)
config.plugins.hyperioncontrol.onIdlebackEffect = ConfigText("Rainbow swirl fast", False)

config.plugins.hyperioncontrol.deviceType = ConfigSelection(choices=[("udpraw","UDPRaw"),("sedu","Sedulight"),("adalight","Adalight"),("AdalightApa102","Adalight-APA102"),("karate","Karatelight"),("atmo","Atmolight"),("philipshue","PhilipsHue"),("philipshueentertainment","PhilipsHueEntertainment")], default = "udpraw")
config.plugins.hyperioncontrol.configName = ConfigText("HyperionConfig", False)
config.plugins.hyperioncontrol.phe_username = ConfigText("username", False)
config.plugins.hyperioncontrol.phe_clientkey = ConfigText("clientkey", False)
config.plugins.hyperioncontrol.phe_lightIds = ConfigText("lightIds", False)
config.plugins.hyperioncontrol.phe_groupId = ConfigText("groupId", False)
config.plugins.hyperioncontrol.phe_switchOffOnBlack = NoSave(ConfigYesNo(default = True))
config.plugins.hyperioncontrol.outputIP = ConfigIP(default = [192, 168, 178, 24])
config.plugins.hyperioncontrol.outputTYPE = ConfigSelection(choices=[("/dev/ttyUSB0","/dev/ttyUSB0"), ("/dev/ttyACM0","/dev/ttyACM0"), ("/dev/ttyAMA0","/dev/ttyAMA0"), ("/dev/ttyS0","/dev/ttyS0"), ("/dev/null","/dev/null"),], default = "/dev/ttyUSB0")
config.plugins.hyperioncontrol.delayafterconnect = ConfigSelectionNumber(0,20,1,default = 0)
config.plugins.hyperioncontrol.colorOrder = ConfigSelection(choices=[("rgb","RGB"), ("bgr","BGR"), ("rbg","RBG"), ("brg","BRG"), ("grb","GRB"), ("gbr","GBR")], default = "rgb")
config.plugins.hyperioncontrol.baudrate = ConfigSelection(choices=[("38400","38.400"), ("50000","50.000"), ("57600","57.600"), ("100000","100.000"),("115200","115.200"), ("150000","150.000"), ("200000","200.000"), ("250000","250.000"), ("460800","460.800"), ("500000","500.000"), ("800000","800.000"), ("1000000","1.000.000")], default = "200000")
config.plugins.hyperioncontrol.protocol = ConfigSelection(choices=[("0","0"), ("2","2"), ("3","3")], default = "0")
config.plugins.hyperioncontrol.lastpicpath = ConfigText("/", False)
config.plugins.hyperioncontrol.ledDirection = ConfigSelection(choices=[("1",_("clockwise")), ("2",_("counterclockwise"))], default = "1")
config.plugins.hyperioncontrol.ledBegin = ConfigSelection(choices=[("0",_("none")),("1",_("bottom middle")), ("2",_("right bottom")), ("3",_("right top")), ("4",_("left top")), ("5",_("left bottom"))], default = "0")
config.plugins.hyperioncontrol.ledTop = ConfigSelectionNumber(0,300,1,default = 0)
config.plugins.hyperioncontrol.ledRight = ConfigSelectionNumber(0,200,1,default = 0)
config.plugins.hyperioncontrol.ledLeft = ConfigSelectionNumber(0,200,1,default = 0)
config.plugins.hyperioncontrol.ledBottomGap = ConfigSelectionNumber(0,100,1,default = 0)
config.plugins.hyperioncontrol.ledCornerTopLeft = ConfigYesNo(default = False)
config.plugins.hyperioncontrol.ledCornerTopRight = ConfigYesNo(default = False)
config.plugins.hyperioncontrol.ledCornerBottomLeft = ConfigYesNo(default = False)
config.plugins.hyperioncontrol.ledCornerBottomRight = ConfigYesNo(default = False)
config.plugins.hyperioncontrol.hPicDeep = ConfigSelectionNumber(1,99,1,default = 8)
config.plugins.hyperioncontrol.vPicDeep = ConfigSelectionNumber(1,99,1,default = 5)
config.plugins.hyperioncontrol.hPicDist = ConfigSelectionNumber(0,50,1,default = 0)
config.plugins.hyperioncontrol.vPicDist = ConfigSelectionNumber(0,50,1,default = 0)
config.plugins.hyperioncontrol.PicOverlap = ConfigSelectionNumber(0,100,1,default = 0)

def onLeaveStandby():
	print "[HyperionControl] comes back from standby (idle)"
	#set mode to live-mode on come back from Standby (Idle)
	if config.plugins.hyperioncontrol.onIdlebackAction.value == "color":
		cmd = "-c '%s'" % config.plugins.hyperioncontrol.onIdlebackColor.value
		send_CMD(cmd)
	elif config.plugins.hyperioncontrol.onIdlebackAction.value == "effect":
		cmd = "--effect '%s'" % config.plugins.hyperioncontrol.onIdlebackEffect.value
		send_CMD(cmd)
	elif config.plugins.hyperioncontrol.onIdlebackAction.value == "live":
		send_CMD('--clearall')

def onStandby(configElement):
	print "[HyperionControl] go to standby (idle)..."
	from Screens.Standby import inStandby
	inStandby.onClose.append(onLeaveStandby)
	#set mode on standby (idle)
	if config.plugins.hyperioncontrol.onIdleAction.value == "color":
		cmd = "-c '%s'" % config.plugins.hyperioncontrol.onIdleColor.value
		send_CMD(cmd)
	elif config.plugins.hyperioncontrol.onIdleAction.value == "effect":
		cmd = "--effect '%s'" % config.plugins.hyperioncontrol.onIdleEffect.value
		send_CMD(cmd)

def sessionstart(reason, **kwargs):
	if kwargs.has_key("session") and reason == 0:
		print "[HyperionControl] sessionstart"
		config.misc.standbyCounter.addNotifier(onStandby, initial_call = False)

def autostart(reason, **kwargs):
	if reason == 0:
		print "[HyperionControl] start"
		#if hyperionaml is active restart hyperionaml service on start e2
		os_system("systemctl -q is-active hyperionaml  && systemctl restart hyperionaml") 
	if reason == 1:
		print "[HyperionControl] shutdown"
		#stop hyperion service on shutdown (led's off)
		os_system("systemctl stop hyperion")

def main(session, **kwargs):
	session.open(hyperionStart)

def Plugins(path,**kwargs):
	name = _("Hyperion Control")
	description = _("Control Your LEDs (v%s)") % hyperioncontrol_version
	descriptors = []
	descriptors.append( PluginDescriptor(name = name, where = PluginDescriptor.WHERE_SESSIONSTART, fnc=sessionstart) )
	descriptors.append( PluginDescriptor(name = name, where = PluginDescriptor.WHERE_AUTOSTART, fnc=autostart) )
	descriptors.append( PluginDescriptor(name = name, description = description, where = PluginDescriptor.WHERE_PLUGINMENU,icon="hyperioncontrol.png", fnc = main) )
	descriptors.append( PluginDescriptor(name=name, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main) )
	return descriptors
	
