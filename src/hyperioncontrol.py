# -*- coding: utf-8 -*-
# by einfall, pclin & Sven_H for DreamOS

from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.MultiContent import MultiContentEntryText, MultiContentEntryTextAlphaBlend
from Components.Pixmap import Pixmap
from Components.FileList import FileList
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigText, ConfigSelection, ConfigSelectionNumber, ConfigSubsection, NoSave
from Tools.BoundFunction import boundFunction
from enigma import gFont, ePoint, eSize, getDesktop, ePixmap, eListboxPythonMultiContent, RT_HALIGN_CENTER, RT_VALIGN_CENTER, RT_WRAP, eListbox, eTimer, eConsoleAppContainer, eNetworkManager, eEnv
from skin import TemplatedListFonts, parseColor
from collections import OrderedDict
import subprocess, threading, os, json

sz_w = getDesktop(0).size().width()

hyperionremote_sh = "systemctl"
hyperioncontrol_version = "2.6"

json.encoder.FLOAT_REPR = lambda o: format(o, '.4f')

#== language-support ====================================
from Components.Language import language
from os import environ as os_environ, popen
import gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
lang = language.getLanguage()
os_environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("enigma2-plugins", resolveFilename(SCOPE_LANGUAGE))
gettext.bindtextdomain("HyperionControl", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/HyperionControl/locale"))

def _(txt):
	t = gettext.dgettext("HyperionControl", txt)
	if t == txt:
		t = gettext.gettext(txt)
	if t == txt:
		t = gettext.dgettext("enigma2-plugins", txt)
	return t
#== end language support ================================

class ColorNames():
	
	#english colornames
	itemslist_en = [(('Maroon', '#800000'),), (('Dark Red', '#8B0000'),), (('Brown', '#A52A2A'),), (('Firebrick', '#B22222'),), (('Crimson', '#DC143C'),), (('Red', '#FF0000'),), (('Tomato', '#FF6347'),), (('Coral', '#FF7F50'),), (('Indian Red', '#CD5C5C'),), (('Light Coral', '#F08080'),), (('Dark Salmon', '#E9967A'),), (('Salmon', '#FA8072'),), (('Light Salmon', '#FFA07A'),), (('Orange Red', '#FF4500'),), (('Dark Orange', '#FF8C00'),), (('Orange', '#FFA500'),), (('Gold', '#FFD700'),), (('Dark Golden Rod', '#B8860B'),), (('Golden Rod', '#DAA520'),), (('Pale Golden rod', '#EEE8AA'),), (('Dark Khaki', '#BDB76B'),), (('Khaki', '#F0E68C'),), (('Olive', '#808000'),), (('Yellow', '#FFFF00'),), (('Yellow Green', '#9ACD32'),), (('Dark Olive Green', '#556B2F'),), (('Olive Drab', '#6B8E23'),), (('Lawn Green', '#7CFC00'),), (('Chart Reuse', '#7FFF00'),), (('Green Yellow', '#ADFF2F'),), (('Dark Green', '#006400'),), (('Green', '#008000'),), (('Forest Green', '#228B22'),), (('Lime', '#00FF00'),), (('Lime Green', '#32CD32'),), (('Light Green', '#90EE90'),), (('Pale Green', '#98FB98'),), (('Dark Sea Green', '#8FBC8F'),), (('Medium Spring Green', '#00FA9A'),), (('Spring Green', '#00FF7F'),), (('Sea Green', '#2E8B57'),), (('Medium Aqua Marine', '#66CDAA'),), (('Medium Sea Green', '#3CB371'),), (('Light Sea Green', '#20B2AA'),), (('Dark Slate Gray', '#2F4F4F'),), (('Teal', '#008080'),), (('Dark Cyan', '#008B8B'),), (('Cyan', '#00FFFF'),), (('Light Cyan', '#E0FFFF'),), (('Dark Turquoise', '#00CED1'),), (('Turquoise', '#40E0D0'),), (('Medium Turquoise', '#48D1CC'),), (('Pale Turquoise', '#AFEEEE'),), (('Aqua Marine', '#7FFFD4'),), (('Powder Blue', '#B0E0E6'),), (('Cadet Blue', '#5F9EA0'),), (('Steel Blue', '#4682B4'),), (('Corn Flower Blue', '#6495ED'),), (('Deep Sky Blue', '#00BFFF'),), (('Dodger Blue', '#1E90FF'),), (('Light Blue', '#ADD8E6'),), (('Sky Blue', '#87CEEB'),), (('Light Sky Blue', '#87CEFA'),), (('Midnight Blue', '#191970'),), (('Navy', '#000080'),), (('Dark Blue', '#00008B'),), (('Medium Blue', '#0000CD'),), (('Blue', '#0000FF'),), (('Royal Blue', '#4169E1'),), (('Blue Violet', '#8A2BE2'),), (('Indigo', '#4B0082'),), (('Dark Slate Blue', '#483D8B'),), (('Slate Blue', '#6A5ACD'),), (('Medium Slate Blue', '#7B68EE'),), (('Medium Purple', '#9370DB'),), (('Dark Magenta', '#8B008B'),), (('Dark Violet', '#9400D3'),), (('Dark Orchid', '#9932CC'),), (('Medium Orchid', '#BA55D3'),), (('Purple', '#800080'),), (('Thistle', '#D8BFD8'),), (('Plum', '#DDA0DD'),), (('Violet', '#EE82EE'),), (('Magenta / Fuchsia', '#FF00FF'),), (('Orchid', '#DA70D6'),), (('Medium Violet Red', '#C71585'),), (('Pale Violet Red', '#DB7093'),), (('Deep Pink', '#FF1493'),), (('Hot Pink', '#FF69B4'),), (('Light Pink', '#FFB6C1'),), (('Pink', '#FFC0CB'),), (('Antique White', '#FAEBD7'),), (('Beige', '#F5F5DC'),), (('Bisque', '#FFE4C4'),), (('Blanched Almond', '#FFEBCD'),), (('Wheat', '#F5DEB3'),), (('Corn Silk', '#FFF8DC'),), (('Lemon Chiffon', '#FFFACD'),), (('Light Golden Rod Yellow', '#FAFAD2'),), (('Light Yellow', '#FFFFE0'),), (('Saddle Brown', '#8B4513'),), (('Sienna', '#A0522D'),), (('Chocolate', '#D2691E'),), (('Peru', '#CD853F'),), (('Sandy Brown', '#F4A460'),), (('Burly Wood', '#DEB887'),), (('Tan', '#D2B48C'),), (('Rosy Brown', '#BC8F8F'),), (('Moccasin', '#FFE4B5'),), (('Navajo White', '#FFDEAD'),), (('Peach Puff', '#FFDAB9'),), (('Misty Rose', '#FFE4E1'),), (('Lavender Blush', '#FFF0F5'),), (('Linen', '#FAF0E6'),), (('Old Lace', '#FDF5E6'),), (('Papaya Whip', '#FFEFD5'),), (('Sea Shell', '#FFF5EE'),), (('Mint Cream', '#F5FFFA'),), (('Slate Gray', '#708090'),), (('Light Slate Gray', '#778899'),), (('Light Steel Blue', '#B0C4DE'),), (('Lavender', '#E6E6FA'),), (('Floral White', '#FFFAF0'),), (('Alice Blue', '#F0F8FF'),), (('Ghost White', '#F8F8FF'),), (('Honeydew', '#F0FFF0'),), (('Ivory', '#FFFFF0'),), (('Azure', '#F0FFFF'),), (('Snow', '#FFFAFA'),), (('Dim Gray', '#696969'),), (('Gray', '#808080'),), (('Dark gray', '#A9A9A9'),), (('Silver', '#C0C0C0'),), (('Light Gray', '#D3D3D3'),), (('Gainsboro', '#DCDCDC'),), (('White Smoke', '#F5F5F5'),), (('White', '#FFFFFF'),)]
	
	#german colornames
	itemslist_de = [(('Kastanienbraun', '#800000'),), (('Dunkelrot', '#8B0000'),), (('Braun', '#A52A2A'),), (('Feuerrot', '#B22222'),), (('Purpur', '#DC143C'),), (('Rot', '#FF0000'),), (('Tomatenrot', '#FF6347'),), (('Korallrot', '#FF7F50'),), (('Indianerrot', '#CD5C5C'),), (('Helles Korallrot', '#F08080'),), (('Dunkles Lachsrosa', '#E9967A'),), (('Lachsrosa', '#FA8072'),), (('Helles Lachsrosa', '#FFA07A'),), (('Orangerot', '#FF4500'),), (('Dunkles Orangerot', '#FF8C00'),), (('Orangerot', '#FFA500'),), (('Gold', '#FFD700'),), (('Dunkle Goldrute', '#B8860B'),), (('Goldrute', '#DAA520'),), (('Blaß Goldrute', '#EEE8AA'),), (('Dunkler Erdton', '#BDB76B'),), (('Erdton', '#F0E68C'),), (('Olive', '#808000'),), (('Gelb', '#FFFF00'),), (('Gelbgrün', '#9ACD32'),), (('Dunkles Olivegrün', '#556B2F'),), (('Graugrün', '#6B8E23'),), (('Grasgrün', '#7CFC00'),), (('Chartreuse', '#7FFF00'),), (('Grüngelb', '#ADFF2F'),), (('Dunkelgrün', '#006400'),), (('Grün', '#008000'),), (('Waldgrün', '#228B22'),), (('Limone', '#00FF00'),), (('Limonengrün', '#32CD32'),), (('Hellgrün', '#90EE90'),), (('Blaßgrün', '#98FB98'),), (('Dunkel Seegrün', '#8FBC8F'),), (('Mittelfrühlingsgrün', '#00FA9A'),), (('Frühlingsgrün', '#00FF7F'),), (('Meergrün', '#2E8B57'),), (('Mittelaquamarinblau', '#66CDAA'),), (('Mittelseegrün', '#3CB371'),), (('Hellmeergrün', '#20B2AA'),), (('Dunkel Schiefergrau', '#2F4F4F'),), (('Blaugrün', '#008080'),), (('Dunkles Zyan', '#008B8B'),), (('Zyan', '#00FFFF'),), (('Helles Zyan', '#E0FFFF'),), (('Dunkeltürkis', '#00CED1'),), (('Türkis', '#40E0D0'),), (('Mitteltürkis', '#48D1CC'),), (('Blaßtürkis', '#AFEEEE'),), (('Aquamarin', '#7FFFD4'),), (('Pulverblau', '#B0E0E6'),), (('Kadettenblau', '#5F9EA0'),), (('Stahlblau', '#4682B4'),), (('Kornblumenblau', '#6495ED'),), (('Dunkelhimmelblau', '#00BFFF'),), (('Persenningblau', '#1E90FF'),), (('Hellblau', '#ADD8E6'),), (('Himmelblau', '#87CEEB'),), (('Hellhimmelblau', '#87CEFA'),), (('Mitternachtsblau', '#191970'),), (('Navy', '#000080'),), (('Dunkelblau', '#00008B'),), (('Mittelblau', '#0000CD'),), (('Blau', '#0000FF'),), (('Königsblau', '#4169E1'),), (('Blauviolett', '#8A2BE2'),), (('Indigoblau', '#4B0082'),), (('Dunkles Schieferblau', '#483D8B'),), (('Schlieferblau', '#6A5ACD'),), (('Mittelschieferblau', '#7B68EE'),), (('Mittellila', '#9370DB'),), (('Dunkelmagenta', '#8B008B'),), (('Dunkelviolett', '#9400D3'),), (('Dunkel Orchidee', '#9932CC'),), (('Mittelorchidee', '#BA55D3'),), (('Lila', '#800080'),), (('Distel', '#D8BFD8'),), (('Pflaume', '#DDA0DD'),), (('Violett', '#EE82EE'),), (('Magenta', '#FF00FF'),), (('Orchidee', '#DA70D6'),), (('Mittelviolettrot', '#C71585'),), (('Blaßviolettrot', '#DB7093'),), (('Dunkelrosa', '#FF1493'),), (('Knallrosa', '#FF69B4'),), (('Hellrosa', '#FFB6C1'),), (('Rosa', '#FFC0CB'),), (('Antikweiß', '#FAEBD7'),), (('Beige', '#F5F5DC'),), (('Bisquit', '#FFE4C4'),), (('Mandelweiß', '#FFEBCD'),), (('Weizen', '#F5DEB3'),), (('Kornseide', '#FFF8DC'),), (('Zitronenchiffon', '#FFFACD'),), (('Hellgoldrute Gelb', '#FAFAD2'),), (('Hellgelb', '#FFFFE0'),), (('Sattelbraun', '#8B4513'),), (('Sienna', '#A0522D'),), (('Schokolade', '#D2691E'),), (('Peru', '#CD853F'),), (('Sandbraun', '#F4A460'),), (('Burlywood', '#DEB887'),), (('Hautfarben', '#D2B48C'),), (('Rosigbraun', '#BC8F8F'),), (('Mokassin', '#FFE4B5'),), (('Navajo Weiß', '#FFDEAD'),), (('Pfirsich', '#FFDAB9'),), (('Blaßrose', '#FFE4E1'),), (('Lavendelhauch', '#FFF0F5'),), (('Leinen', '#FAF0E6'),), (('Alte Spitze', '#FDF5E6'),), (('Papaya Creme', '#FFEFD5'),), (('Muschelweiß', '#FFF5EE'),), (('Pfefferminzcreme', '#F5FFFA'),), (('Schiefergrau', '#708090'),), (('Hellschiefergrau', '#778899'),), (('Hellstahlblau', '#B0C4DE'),), (('Lavendel', '#E6E6FA'),), (('Blütenweiß', '#FFFAF0'),), (('Aliceblau', '#F0F8FF'),), (('Geisterweiß', '#F8F8FF'),), (('Honigtau', '#F0FFF0'),), (('Elfenbein', '#FFFFF0'),), (('Azur', '#F0FFFF'),), (('Schneeweiß', '#FFFAFA'),), (('Blaßgrau', '#696969'),), (('Grau', '#808080'),), (('Dunkelgrau', '#A9A9A9'),), (('Silber', '#C0C0C0'),), (('Hellgrau', '#D3D3D3'),), (('Gainsboro', '#DCDCDC'),), (('Rauch', '#F5F5F5'),), (('Weiß', '#FFFFFF'),)]
	
	#gradient
	itemsverlauf = [(('','#700000'),), (('','#800000'),), (('','#8D0000'),), (('','#990000'),), (('','#A60000'),), (('','#B30000'),), (('','#C00000'),), (('','#CC0000'),), (('','#D90000'),), (('','#E60000'),), (('','#F20000'),), (('','#FF0000'),), (('','#FF1010'),), (('','#FF2020'),), (('','#FF3030'),), (('','#FF3F3F'),), (('','#FF4F4F'),), (('','#FF5F5F'),), (('','#FF6F6F'),), (('','#FF7F7F'),), (('','#FF8F8F'),), (('','#FF9F9F'),), (('','#FFAFAF'),), (('','#FFBEBE'),), (('','#FFCECE'),), (('','#FFDEDE'),), (('','#FFEEEE'),), (('','#007000'),), (('','#008000'),), (('','#008D00'),), (('','#009900'),), (('','#00A600'),), (('','#00B300'),), (('','#00C000'),), (('','#00CC00'),), (('','#00D900'),), (('','#00E600'),), (('','#00F200'),), (('','#00FF00'),), (('','#10FF10'),), (('','#20FF20'),), (('','#30FF30'),), (('','#3FFF3F'),), (('','#4FFF4F'),), (('','#5FFF5F'),), (('','#6FFF6F'),), (('','#7FFF7F'),), (('','#8FFF8F'),), (('','#9FFF9F'),), (('','#AFFFAF'),), (('','#BEFFBE'),), (('','#CEFFCE'),), (('','#DEFFDE'),), (('','#EEFFEE'),), (('','#000070'),), (('','#000080'),), (('','#00008D'),), (('','#000099'),), (('','#0000A6'),), (('','#0000B3'),), (('','#0000C0'),), (('','#0000CC'),), (('','#0000D9'),), (('','#0000E6'),), (('','#0000F2'),), (('','#0000FF'),), (('','#1010FF'),), (('','#2020FF'),), (('','#3030FF'),), (('','#3F3FFF'),), (('','#4F4FFF'),), (('','#5F5FFF'),), (('','#6F6FFF'),), (('','#7F7FFF'),), (('','#8F8FFF'),), (('','#9F9FFF'),), (('','#AFAFFF'),), (('','#BEBEFF'),), (('','#CECEFF'),), (('','#DEDEFF'),), (('','#EEEEFF'),), (('','#9E9E00'),), (('','#ADAD00'),), (('','#B5B500'),), (('','#BDBD00'),), (('','#C6C600'),), (('','#CECE00'),), (('','#D6D600'),), (('','#DEDE00'),), (('','#E6E600'),), (('','#EFEF00'),), (('','#F7F700'),), (('','#FFFF00'),), (('','#FFFF10'),), (('','#FFFF20'),), (('','#FFFF30'),), (('','#FFFF3F'),), (('','#FFFF4F'),), (('','#FFFF5F'),), (('','#FFFF6F'),), (('','#FFFF7F'),), (('','#FFFF8F'),), (('','#FFFF9F'),), (('','#FFFFAF'),), (('','#FFFFBE'),), (('','#FFFFCE'),), (('','#FFFFDE'),), (('','#FFFFEE'),), (('','#009E9E'),), (('','#00ADAD'),), (('','#00B5B5'),), (('','#00BDBD'),), (('','#00C6C6'),), (('','#00CECE'),), (('','#00D6D6'),), (('','#00DEDE'),), (('','#00E6E6'),), (('','#00EFEF'),), (('','#00F7F7'),), (('','#00FFFF'),), (('','#10FFFF'),), (('','#20FFFF'),), (('','#30FFFF'),), (('','#3FFFFF'),), (('','#4FFFFF'),), (('','#5FFFFF'),), (('','#6FFFFF'),), (('','#7FFFFF'),), (('','#8FFFFF'),), (('','#9FFFFF'),), (('','#AFFFFF'),), (('','#BEFFFF'),), (('','#CEFFFF'),), (('','#DEFFFF'),), (('','#EEFFFF'),), (('','#4F004F'),), (('','#5E005E'),), (('','#6D006D'),), (('','#7C007C'),), (('','#8A008A'),), (('','#990099'),), (('','#A700A7'),), (('','#B600B6'),), (('','#C500C5'),), (('','#D300D3'),), (('','#E200E2'),), (('','#FF00FF'),), (('','#FF10FF'),), (('','#FF20FF'),), (('','#FF30FF'),), (('','#FF3FFF'),), (('','#FF4FFF'),), (('','#FF5FFF'),), (('','#FF6FFF'),), (('','#FF7FFF'),), (('','#FF8FFF'),), (('','#FF9FFF'),), (('','#FFAFFF'),), (('','#FFBEFF'),), (('','#FFCEFF'),), (('','#FFDEFF'),), (('','#FFEEFF'),), (('','#3F1F09'),), (('','#46220A'),), (('','#4D260B'),), (('','#53290C'),), (('','#5A2D0D'),), (('','#61300E'),), (('','#68330E'),), (('','#6F370F'),), (('','#753A10'),), (('','#7C3E11'),), (('','#834112'),), (('','#8B4513'),), (('','#924F1F'),), (('','#99592B'),), (('','#A16337'),), (('','#A86D42'),), (('','#AF774E'),), (('','#B6815A'),), (('','#BD8B66'),), (('','#C59472'),), (('','#CC9E7E'),), (('','#D3A88A'),), (('','#DAB296'),), (('','#E1BCA1'),), (('','#E9C6AD'),), (('','#F0D0B9'),), (('','#F7DAC5'),), (('','#C05000'),),  (('','#C65000'),),  (('','#CD5D00'),),  (('','#D66700'),),  (('','#E07100'),),  (('','#E08100'),), (('','#E09100'),), (('','#E39300'),), (('','#E69500'),), (('','#E99700'),), (('','#EC9900'),), (('','#F09B00'),), (('','#F39D00'),), (('','#F69F00'),), (('','#F9A100'),), (('','#FCA300'),), (('','#FFA500'),), (('','#FFAC14'),), (('','#FFB329'),), (('','#FFBB3D'),), (('','#FFC252'),), (('','#FFC966'),), (('','#FFD07A'),), (('','#FFD78F'),), (('','#FFDFA3'),), (('','#FFE6B8'),), (('','#FFEDCC'),), (('','#000000'),), (('','#111111'),), (('','#1B1B1B'),), (('','#242424'),), (('','#2E2E2E'),), (('','#373737'),), (('','#414141'),), (('','#4A4A4A'),), (('','#545454'),), (('','#5D5D5D'),), (('','#676767'),), (('','#707070'),), (('','#7A7A7A'),), (('','#838383'),), (('','#8D8D8D'),), (('','#969696'),), (('','#A0A0A0'),), (('','#A9A9A9'),), (('','#B3B3B3'),), (('','#BCBCBC'),), (('','#C6C6C6'),), (('','#CFCFCF'),), (('','#D9D9D9'),), (('','#E2E2E2'),), (('','#ECECEC'),), (('','#F5F5F5'),), (('','#FFFFFF'),)]
	
	def getGradientList(self):
		return self.itemsverlauf
	
	def getColorList(self):
		if lang == "de_DE":
			return self.itemslist_de
		else:
			return self.itemslist_en
	
	def getColorName(self, colorValue=""):
		if lang == "de_DE":
			colorList = self.itemslist_de
		else:
			colorList = self.itemslist_en
		
		for color in colorList:
			if color[0][1] == colorValue:
				return color[0][0]
		
		if colorValue == "#000000":
			return _("None")
		return colorValue


class hyperionControlColors(Screen):
	if sz_w == 1920:
		skin = """
		<screen name="hyperionControlColors" position="center,100" size="900,940" >
			<ePixmap pixmap="skin_default/buttons/red.png" position="20,860" scale="stretch" size="200,70" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="240,860" size="200,70" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="460,860"  size="200,70" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/blue.png" position="680,860" size="200,70" scale="stretch"/>
			<eLabel font="Regular;30" foregroundColor="white" name="" position="20,860" size="200,70" text="Exit" valign="center" halign="center" backgroundColor="#9f1313" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<widget source="key_yellow" render="Label" font="Regular;30" foregroundColor="white" position="460,860" size="200,70" valign="center" halign="center" backgroundColor="#a08500" shadowColor="black" shadowOffset="-2,-2" zPosition="1" transparent="1" />
			<widget source="key_blue" render="Label" font="Regular;30" foregroundColor="white" position="680,860" size="200,70" valign="center" halign="center" backgroundColor="#18188b" zPosition="1" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel name="" position="10,845" size="880,2" backgroundColor="grey" />
			<widget name="list" position="10,5" size="850,830" itemWidth="840" itemHeight="63" transparent="1" enableWrapAround="1" scrollbarMode="showOnDemand" />
		</screen>"""

	else:
		skin = """
		<screen name="hyperionControlColors" position="center,80" size="590,620" transparent="0">
			<ePixmap pixmap="skin_default/buttons/red.png" position="5,570" scale="stretch" size="140,40" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="150,570" size="140,40" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="295,570"  size="140,40" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/blue.png" position="440,570" size="140,40" scale="stretch"/>
			<eLabel font="Regular;22" foregroundColor="white" name="" position="5,570" size="140,40" text="Exit" valign="center" halign="center" backgroundColor="#9f1313" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<widget source="key_yellow" render="Label" font="Regular;22" foregroundColor="white" position="295,570" size="140,40" valign="center" halign="center" backgroundColor="#a08500" shadowColor="black" shadowOffset="-2,-2" zPosition="1" transparent="1" />
			<widget source="key_blue" render="Label" font="Regular;22" foregroundColor="white" position="440,570" size="140,40" valign="center" halign="center" backgroundColor="#18188b" zPosition="1" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel name="" position="5,560" size="580,2" backgroundColor="grey" />
			<widget name="list" position="10,3" size="575,550" itemWidth="565" itemHeight="45" transparent="1" enableWrapAround="1" scrollbarMode="showOnDemand" />
		</screen>"""
	
	def __init__(self, session, OnlyReturnColor=False):
		Screen.__init__(self, session)
		self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'MenuActions', 'SetupActions','ListboxActions'], {
		'cancel': self.key_exit,
		'ok'	: self.key_ok,
		'red'	: self.key_red,
		'green'	: self.key_green,
		'yellow': self.key_yellow,
		'blue'	: self.key_blue,
		'previousSection' : self.pageUp,
		'nextSection' : self.pageDown,
		'left' : self.moveLeft,
		'right': self.moveRight,
		})
		
		self.OnlyReturnColor = OnlyReturnColor

		tlf = TemplatedListFonts()
		
		self.ColorNames = ColorNames()
		self.litems = self.ColorNames.getColorList()
		self.ColorPage = "farbliste"
		
		if self.OnlyReturnColor:
			self["key_yellow"] = StaticText("")
			self["key_blue"] = StaticText("")
		else:
			self["key_yellow"] = StaticText(_("gradient"))
			self["key_blue"] = StaticText(_("Image Mode"))
				
		if sz_w == 1920:
			self.itemHeight = 63
			self.itemWidth = 840
			self.itemSize = 90
			self.margin = ePoint(10,10)
		else:
			self.itemHeight = 45
			self.itemWidth = 565
			self.itemSize = 60
			self.margin = ePoint(5,5)
		
		self.ml = MenuList(self.litems, mode=eListbox.layoutGrid, content=eListboxPythonMultiContent, itemSize=self.itemHeight, margin=ePoint(0,0), selectionZoom=1.1)
		self.ml.l.setFont(0, gFont(tlf.face(tlf.SMALL), tlf.size(tlf.SMALL)))
		self.ml.l.setFont(1, gFont(tlf.face(tlf.MEDIUM), tlf.size(tlf.MEDIUM)))
		self.ml.l.setBuildFunc(self.showList, True)
		self['list'] = self.ml
		
		self.onLayoutFinish.append(self.buildList)
		self.setTitle(_("Hyperion Control - Colors"))
		
	def buildList(self):
		self["list"].setList(self.litems)

	def moveLeft(self):
		if self.ColorPage == "farbverlauf":
			self["list"].instance.moveSelection(self["list"].instance.moveLeft)
		else:
			self.pageUp()

	def moveRight(self):
		if self.ColorPage == "farbverlauf":
			self["list"].instance.moveSelection(self["list"].instance.moveRight)
		else:
			self.pageDown()

	def pageUp(self):
		self["list"].pageUp()

	def pageDown(self):
		self["list"].pageDown()
		
	def showList(self, item, selected):
		(text, hcol) = item
		col = parseColor(hcol).argb()
		if selected:
			textcol = parseColor("#000000").argb()
			if col == textcol:
				textcol = parseColor("#FFFFFF").argb()
		else:
			textcol = parseColor("#FFFFFF").argb()
			color = [int(hcol[1:3],16), int(hcol[3:5],16),int(hcol[5:7],16) ]
			if (color[0]>191 and color[1]>181) or (color[1]>206 and color[2]>208):
				textcol = parseColor("#696969").argb()
		
		res = [item]
		
		try:
			if self.ColorPage == "farbverlauf":
				EntrySize = (self.itemSize,self.itemSize)
				if sz_w == 1920:
					pos = (7,7)
				else:
					pos = (5,5)
				if selected:
					pos = (0,0)
			elif self.ColorPage == "farbliste":
				if sz_w == 1920:
					margin = 5
					pos = (margin+15,margin)
					EntrySize = (self.itemWidth - margin*2 -25,self.itemHeight-margin*2)
				else:
					margin = 4
					pos = (margin+10,margin)
					EntrySize = (self.itemWidth - margin*2 -15,self.itemHeight-margin*2)
					
			if selected:
				res.append(MultiContentEntryTextAlphaBlend(pos=pos, size=EntrySize, font=1, text=text, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER|RT_WRAP, color=textcol, color_sel=textcol, backcolor=col, backcolor_sel=col))
			else:
				res.append(MultiContentEntryTextAlphaBlend(pos=pos, size=EntrySize, font=0, text=text, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER|RT_WRAP, color=textcol, color_sel=textcol, backcolor=col, backcolor_sel=col))
			return res
		
		except:
			import traceback
			traceback.print_exc()
			return None

	def key_red(self):
		self.key_exit()

	def key_green(self):
		pass
		
	def key_yellow(self):
		if self.OnlyReturnColor:
			return
		if self.ColorPage == "farbverlauf":
			self.ColorPage = "farbliste"
			self["key_yellow"].setText(_("gradient"))
			#self["list"].instance.setMode(eListbox.layoutVertical)
			self["list"].instance.setItemHeight(self.itemHeight)
			self["list"].instance.setItemWidth(self.itemWidth)
			self["list"].instance.setMargin(ePoint(0,0))
			self.litems = self.ColorNames.getColorList()
		else:
			self.ColorPage = "farbverlauf"
			self["key_yellow"].setText(_("color list"))
			#self["list"].instance.setMode(eListbox.layoutGrid)
			self["list"].instance.setItemHeight(self.itemSize)
			self["list"].instance.setItemWidth(self.itemSize)
			self["list"].instance.setMargin(self.margin)
			self.litems = self.ColorNames.getGradientList()
			
		index = self["list"].getSelectionIndex()
		self["list"].moveToIndex(0)
		self.buildList()
		self["list"].moveToIndex(index)

	def key_blue(self):
		if self.OnlyReturnColor:
			return
		try:
			if config.plugins.hyperioncontrol.lastpicpath.value:
				path = config.plugins.hyperioncontrol.lastpicpath.value
			else:
				path = "/"
			self.session.openWithCallback(self.selectPictureCallback, HyperionControlPictureBrowser, path)
		except:
			import traceback
			traceback.print_exc()

	def selectPictureCallback(self, retvalue):
		if retvalue:
			cmd = "hyperion-remote --clearall && hyperion-remote -i " + retvalue
			print "[HyperionControl] cmd", cmd
			command = Command(cmd)
			command.run(timeout=3)
			print "[HyperionControl] cmd_out:", command.out

	def key_ok(self):
		exist = self['list'].getCurrent()
		if exist == None:
			return
		print "=== index ok", self["list"].getSelectionIndex()
		(name, color) = self['list'].getCurrent()[0]
		print name, color
		
		if self.OnlyReturnColor:
			self.close((name,color))
			return
		cmd = "-c '%s'" % color
		send_CMD(cmd)

	def key_exit(self):
		self.close()
		

#to get consolen-output with timeout-function
class Command(object):
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None

	def run(self, timeout):
		def target():
			self.process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			(self.out,self.err) = self.process.communicate()

		thread = threading.Thread(target=target)
		thread.start()
		self.timeout=False

		thread.join(float(timeout))
		if thread.is_alive():
			self.process.terminate()
			self.timeout=True
			self.process = None
			thread = None
			return
#=============================================

class ConfigListHC(ConfigList):
	def __init__(self, list, session = None):
		ConfigList.__init__(self, list, session = session)
	
	def jumpToPreviousSection(self):
		index = self.getCurrentIndex() - 1
		index = self.getCurrentIndex() - 1
		maxlen = len(self._ConfigList__list)
		while index >= 0 and maxlen > 0:
			index -= 1
			#fix jump to PreviousSection on empty lines in ConfigList
			if index in self._headers and self.list[index] != ("",):
				if index + 1 < maxlen:
					self.setCurrentIndex(index + 1)
					return
				else:
					self.setCurrentIndex(index - 1)
					return
		self.pageUp()

#=========================================================================

class hyperionControlSetup(Screen, ConfigListScreen):
	if sz_w == 1920:
		skin = """
		<screen name="hyperionControlSetup" position="center,100" size="900,950" >
			<ePixmap pixmap="skin_default/buttons/red.png" position="20,870" scale="stretch" size="200,70" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="240,870" size="200,70" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="460,870"  size="200,70" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/blue.png" position="680,870" size="200,70" scale="stretch"/>
			<eLabel name="" position="10,850" size="880,2" backgroundColor="grey" />
			<eLabel font="Regular;30" foregroundColor="white" name="" position="20,870" size="200,70" text="Exit" valign="center" halign="center" backgroundColor="#9f1313" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel font="Regular;30" foregroundColor="white" name="" position="240,870" size="200,70" text="Save" valign="center" halign="center" backgroundColor="#1f771f" transparent="1" shadowColor="black" shadowOffset="-2,-2" />
			<widget source="key_yellow" render="Label" font="Regular;30" foregroundColor="white" position="460,870" size="200,70" valign="center" halign="center" backgroundColor="#a08500" shadowColor="black" shadowOffset="-2,-2" zPosition="1" transparent="1" />
			<widget source="key_blue" render="Label" font="Regular;30" foregroundColor="white" position="680,870" size="200,70" valign="center" halign="center" backgroundColor="#18188b" zPosition="1" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<widget name="config" seperation="100" position="10,10" size="880,820" enableWrapAround="1" scrollbarMode="showOnDemand" />
		</screen>"""
	else:
		skin = """
		<screen name="hyperionControlSetup" position="center,80" size="590,620">
			<ePixmap pixmap="skin_default/buttons/red.png" position="5,570" scale="stretch" size="140,40" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="150,570" size="140,40" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="295,570"  size="140,40" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/blue.png" position="440,570" size="140,40" scale="stretch"/>
			<eLabel font="Regular;22" foregroundColor="white" name="" position="5,570" size="140,40" text="Exit" valign="center" halign="center" backgroundColor="#9f1313" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel font="Regular;22" foregroundColor="white" name="" position="150,570" size="140,40" text="Save" valign="center" halign="center" backgroundColor="#1f771f" transparent="1" shadowColor="black" shadowOffset="-2,-2" />
			<widget source="key_yellow" render="Label" font="Regular;22" foregroundColor="white" position="295,570" size="140,40" valign="center" halign="center" backgroundColor="#a08500" shadowColor="black" shadowOffset="-2,-2" zPosition="1" transparent="1" />
			<widget source="key_blue" render="Label" font="Regular;22" foregroundColor="white" position="440,570" size="140,40" valign="center" halign="center" backgroundColor="#18188b" zPosition="1" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel name="" position="5,560" size="580,2" backgroundColor="grey" />
			<widget name="config" position="10,10" seperation="100" size="570,545" enableWrapAround="1" scrollbarMode="showOnDemand" />
		</screen>"""
		
	def __init__(self, session):
		Screen.__init__(self, session)
		self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'MenuActions','InfobarEPGActions'], {
		'cancel': self.key_exit,
		'red'	: self.key_red,
		'green'	: self.key_green,
		'yellow': self.key_yellow,
		'blue'	: self.key_blue,
		'menu'	: self.menu,
		'showEventInfo': self.info,
		#'ok': self.key_ok,
		})
		
		self["key_yellow"] = StaticText()
		self["key_blue"] = StaticText(_("Options"))
		self.setupPage = "transform"
		
		self.list = []
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changed)
		self["config"] = ConfigListHC(self.list, session = session)
		self.setTitle(_("Hyperion Control - Setup"))
		self["key_yellow"].setText(_("Device/LED"))
		self.onShown.append(self.readData)
		self.lastLEDcountTxt = None
		self.ColorNames = ColorNames()
		
		#reload ConfigText to ConfigSelection for Idle-Color and Idle-Effects
		color = config.plugins.hyperioncontrol.onIdleColor.value
		colorName = self.ColorNames.getColorName(color)
		config.plugins.hyperioncontrol.onIdleColor = ConfigSelection(choices = [(color,colorName)], default = color)
		color = config.plugins.hyperioncontrol.onIdlebackColor.value
		colorName = self.ColorNames.getColorName(color)
		config.plugins.hyperioncontrol.onIdlebackColor = ConfigSelection(choices = [(color,colorName)], default = color)
		value = config.plugins.hyperioncontrol.onIdleEffect.value
		config.plugins.hyperioncontrol.onIdleEffect = ConfigSelection(choices = [(value,value)], default = value)
		value = config.plugins.hyperioncontrol.onIdlebackEffect.value
		config.plugins.hyperioncontrol.onIdlebackEffect = ConfigSelection(choices = [(value,value)], default = value)
	
	def readData(self):
		self.onShown.remove(self.readData)
		self.readValuesFromConfig()
		readValuesFromRemote(self)
		self.buildConfig()
	
	def saveJson(self):
		try:
			# hsv
			self.jsonConfig['color']['transform'][0]['hsv']['saturationGain'] = int(config.plugins.hyperioncontrol.saturationGain.value) / 100.0
			self.jsonConfig['color']['transform'][0]['hsv']['valueGain'] = int(config.plugins.hyperioncontrol.valueGain.value) / 100.0
			
			# hsl
			self.jsonConfig['color']['transform'][0]['hsl']={}
			self.jsonConfig['color']['transform'][0]['hsl']['saturationLGain'] = int(config.plugins.hyperioncontrol.saturationLGain.value) / 100.0
			self.jsonConfig['color']['transform'][0]['hsl']['luminanceGain'] = int(config.plugins.hyperioncontrol.luminanceGain.value) / 100.0
			self.jsonConfig['color']['transform'][0]['hsl']['luminanceMinimum'] = int(config.plugins.hyperioncontrol.luminanceMinimum.value) / 100.0
			
			# red
			self.jsonConfig['color']['transform'][0]['red']['gamma'] = int(config.plugins.hyperioncontrol.gammaRed.value) / 100.0
			self.jsonConfig['color']['transform'][0]['red']['threshold'] = int(config.plugins.hyperioncontrol.thresholdRed.value) / 100.0
			
			#set as new key
			self.jsonConfig['color']['temperature'] = [{}]
			self.jsonConfig['color']['temperature'][0]['id'] = "default"
			self.jsonConfig['color']['temperature'][0]['leds'] = "*"
			self.jsonConfig['color']['temperature'][0]['correctionValues'] = {}
			
			self.jsonConfig['color']['temperature'][0]['correctionValues']['red'] = int(config.plugins.hyperioncontrol.temperatureRed.value)
			
			#set as new key
			self.jsonConfig['color']['channelAdjustment'] = [{}]
			self.jsonConfig['color']['channelAdjustment'][0]['id'] = "default"
			self.jsonConfig['color']['channelAdjustment'][0]['leds'] = "*"
			self.jsonConfig['color']['channelAdjustment'][0]['pureRed'] = {}
			self.jsonConfig['color']['channelAdjustment'][0]['pureGreen'] = {}
			self.jsonConfig['color']['channelAdjustment'][0]['pureBlue'] = {}
			
			self.jsonConfig['color']['channelAdjustment'][0]['pureRed']['redChannel'] = int(config.plugins.hyperioncontrol.redAdjustRed.value)
			self.jsonConfig['color']['channelAdjustment'][0]['pureGreen']['redChannel'] = int(config.plugins.hyperioncontrol.greenAdjustRed.value)
			self.jsonConfig['color']['channelAdjustment'][0]['pureBlue']['redChannel'] = int(config.plugins.hyperioncontrol.blueAdjustRed.value)
			self.jsonConfig['color']['transform'][0]['red']['whitelevel'] = int(config.plugins.hyperioncontrol.whitelevelRed.value) / 100.0
			self.jsonConfig['color']['transform'][0]['red']['blacklevel'] = int(config.plugins.hyperioncontrol.blacklevelRed.value) / 100.0
			
			# green
			self.jsonConfig['color']['transform'][0]['green']['gamma'] = int(config.plugins.hyperioncontrol.gammaGreen.value) / 100.0
			self.jsonConfig['color']['transform'][0]['green']['threshold'] = int(config.plugins.hyperioncontrol.thresholdGreen.value) / 100.0
			self.jsonConfig['color']['temperature'][0]['correctionValues']['green'] = int(config.plugins.hyperioncontrol.temperatureGreen.value) 
			self.jsonConfig['color']['channelAdjustment'][0]['pureRed']['greenChannel'] = int(config.plugins.hyperioncontrol.redAdjustGreen.value)
			self.jsonConfig['color']['channelAdjustment'][0]['pureGreen']['greenChannel'] = int(config.plugins.hyperioncontrol.greenAdjustGreen.value)
			self.jsonConfig['color']['channelAdjustment'][0]['pureBlue']['greenChannel'] = int(config.plugins.hyperioncontrol.blueAdjustGreen.value)
			self.jsonConfig['color']['transform'][0]['green']['whitelevel'] = int(config.plugins.hyperioncontrol.whitelevelGreen.value) / 100.0
			self.jsonConfig['color']['transform'][0]['green']['blacklevel'] = int(config.plugins.hyperioncontrol.blacklevelGreen.value) / 100.0
			
			# blue
			self.jsonConfig['color']['transform'][0]['blue']['gamma'] = int(config.plugins.hyperioncontrol.gammaBlue.value) / 100.0
			self.jsonConfig['color']['transform'][0]['blue']['threshold'] = int(config.plugins.hyperioncontrol.thresholdBlue.value) / 100.0
			self.jsonConfig['color']['temperature'][0]['correctionValues']['blue'] = int(config.plugins.hyperioncontrol.temperatureBlue.value)
			self.jsonConfig['color']['channelAdjustment'][0]['pureRed']['blueChannel'] = int(config.plugins.hyperioncontrol.redAdjustBlue.value)
			self.jsonConfig['color']['channelAdjustment'][0]['pureGreen']['blueChannel'] = int(config.plugins.hyperioncontrol.greenAdjustBlue.value)
			self.jsonConfig['color']['channelAdjustment'][0]['pureBlue']['blueChannel'] = int(config.plugins.hyperioncontrol.blueAdjustBlue.value)
			self.jsonConfig['color']['transform'][0]['blue']['whitelevel'] = int(config.plugins.hyperioncontrol.whitelevelBlue.value) / 100.0
			self.jsonConfig['color']['transform'][0]['blue']['blacklevel'] = int(config.plugins.hyperioncontrol.blacklevelBlue.value) / 100.0
			
			#Framegrabber
			self.jsonConfig['framegrabber']['width'] = int(str(config.plugins.hyperioncontrol.framegrabberSize.value).split(",")[0])
			self.jsonConfig['framegrabber']['height'] = int(str(config.plugins.hyperioncontrol.framegrabberSize.value).split(",")[1])
			self.jsonConfig['framegrabber']['frequency_Hz'] = int(config.plugins.hyperioncontrol.framegrabberFreq.value) * 1.0
			
			#Smoothing
			self.jsonConfig['color']['smoothing']['updateFrequency'] = int(config.plugins.hyperioncontrol.smoothingupdateFrequency.value) * 1.0
			
			#BlackborderDetector
			self.jsonConfig['blackborderdetector']['enable'] = config.plugins.hyperioncontrol.bbdEnable.value
			self.jsonConfig['blackborderdetector']['threshold'] = int(config.plugins.hyperioncontrol.bbdThreshold.value) / 100.0
			
			#webif
			self.jsonConfig['webConfig']['enable'] = config.plugins.hyperioncontrol.webConfigEnable.value
			self.jsonConfig['webConfig']['port'] = int(config.plugins.hyperioncontrol.webConfigPort.value)
			
			#bootsequence
			if config.plugins.hyperioncontrol.bootseqStart.value == "off":
				self.jsonConfig['bootsequence']['effect'] = ""
				self.jsonConfig['bootsequence']['color'] = [0,0,0]
			elif config.plugins.hyperioncontrol.bootseqStart.value == "effect":
				self.jsonConfig['bootsequence']['effect'] = config.plugins.hyperioncontrol.bootseqEffect.value
				self.jsonConfig['bootsequence']['color'] = [0,0,0]
			else:
				self.jsonConfig['bootsequence']['effect'] = str("")
				color = config.plugins.hyperioncontrol.bootseqColor.value
				self.jsonConfig['bootsequence']['color'] = [int(color[1:3],16), int(color[3:5],16),int(color[5:7],16) ]
			self.jsonConfig['bootsequence']['duration_ms'] = int(config.plugins.hyperioncontrol.bootseqDuration.value)
			
			# device
			self.jsonConfig['device']['type'] = str(config.plugins.hyperioncontrol.deviceType.value)
			self.jsonConfig['device']['name'] = str(config.plugins.hyperioncontrol.configName.value)
			if config.plugins.hyperioncontrol.deviceType.value in ("sedu","adalight","AdalightApa102","atmo","karate"):
				self.jsonConfig['device']['output'] = str(config.plugins.hyperioncontrol.outputTYPE.value)
				self.jsonConfig['device']['delayafterconnect'] = int(config.plugins.hyperioncontrol.delayafterconnect.value)
			else:
				if config.plugins.hyperioncontrol.deviceType.value in ("philipshue","philipshueentertainment"):
					self.jsonConfig['device']['output'] = ".".join(["%d" % d for d in config.plugins.hyperioncontrol.outputIP.value])
				elif config.plugins.hyperioncontrol.deviceType.value == "udpraw":
					self.jsonConfig['device']['output'] = ".".join(["%d" % d for d in config.plugins.hyperioncontrol.outputIP.value]) + ":19446"
			if config.plugins.hyperioncontrol.deviceType.value == "philipshue":
				self.jsonConfig['device']['username'] = str(config.plugins.hyperioncontrol.phe_username.value)
				self.jsonConfig['device']['lightIds'] = [int(s) for s in config.plugins.hyperioncontrol.phe_lightIds.value.split(',')]
				self.jsonConfig['device']['switchOffOnBlack'] = str(config.plugins.hyperioncontrol.phe_switchOffOnBlack.value)
			if config.plugins.hyperioncontrol.deviceType.value == "philipshueentertainment":
				self.jsonConfig['device']['username'] = str(config.plugins.hyperioncontrol.phe_username.value)
				self.jsonConfig['device']['clientkey'] = str(config.plugins.hyperioncontrol.phe_clientkey.value)
				self.jsonConfig['device']['lightIds'] = [int(s) for s in config.plugins.hyperioncontrol.phe_lightIds.value.split(',')]
				self.jsonConfig['device']['groupId'] = int(config.plugins.hyperioncontrol.phe_groupId.value)
				self.jsonConfig['device']['switchOffOnBlack'] = str(config.plugins.hyperioncontrol.phe_switchOffOnBlack.value)
			if config.plugins.hyperioncontrol.deviceType.value == "philipshueentertainment":
				self.jsonConfig['device']['colorOrder'] = str(config.plugins.hyperioncontrol.colorOrder.value)
			else:
				self.jsonConfig['device']['colorOrder'] = str(config.plugins.hyperioncontrol.colorOrder.value)
				self.jsonConfig['device']['rate'] = int(config.plugins.hyperioncontrol.baudrate.value)
			
			#LED-Config
			if config.plugins.hyperioncontrol.ledBegin.value != "0":
				LEDconfig = self.createNewLEDConfig()
				if LEDconfig:
					self.jsonConfig['leds'] = LEDconfig
				else:
					self.session.open(MessageBox,_("Error when generating the LED config!"), MessageBox.TYPE_INFO,timeout=5)
			
			#aml-Service
			self.writeAmlService()
			
			config_file_path ="/etc/hyperion/hyperion.config.json"
			
			if os.path.exists(config_file_path): 
				#write values in config.json
				with open(config_file_path, "w") as write_file:
					json.dump(self.jsonConfig, write_file, ensure_ascii=False, indent=4)
				#daemon reload und services neu starten
				cmd = "systemctl daemon-reload && systemctl restart hyperion && systemctl restart hyperionaml"
				os.system(cmd)
				self.session.openWithCallback(self.saveJsonMessageCallback, MessageBox,_("The settings were saved in '/etc/hyperion/hyperion.config.json'.\n\nHyperion and Hyperionaml were restarted."), MessageBox.TYPE_INFO,timeout=10)
			else:
				self.session.open(MessageBox,_("File '/etc/hyperion/hyperion.config.json' not found!"), MessageBox.TYPE_INFO,timeout=5)
			
			self.saveAll() #save all config-values which don't use NoSave()
			config.plugins.hyperioncontrol.save()
			
			
		
		except:
			import traceback, sys
			traceback.print_exc()
			exc_type, exc_value, exc_traceback = sys.exc_info()
			error = "\n".join(traceback.format_exception_only(exc_type, exc_value))
			self.session.open(MessageBox,_("When saving the 'hyperion.config.json' an error has occurred!\n\nError:\n%s") % error, MessageBox.TYPE_INFO,timeout=5)

	def saveJsonMessageCallback(self, ret=None):
		#check installed packages for device-type
		if config.plugins.hyperioncontrol.deviceType.value in ("sedu","adalight","AdalightApa102","atmo","karate"):
			command = Command("apt list --installed kernel-module-usbserial kernel-module-ch341 kernel-module-ftdi-sio")
			command.run(timeout=5)
		
			#read real settings from hyperion-remote -l
			if command.timeout or command.process.returncode != 0:
				print "[HyperionControl] timeout/error on check packages"
			else:
				cmdValue = command.out.strip().split("\n")
				if len(cmdValue)<4:
					self.session.openWithCallback(self.installPackages, MessageBox,_("You need more kernel-moduls for the selected device-type:\n  - kernel-module-usbserial\n  - kernel-module-ch341\n  - kernel-module-ftdi-sio\n\nDo you want to install this needed modules?"), MessageBox.TYPE_YESNO)

	def installPackages(self, ret=None):
		if ret:
			self.session.openWithCallback(self.installPackagesCallback, Console,_("HyperionControl - install needed modules"),["apt-get -y --assume-yes install kernel-module-usbserial kernel-module-ch341 kernel-module-ftdi-sio","modprobe usbserial","modprobe ch341","modprobe ftdi-sio","systemctl restart hyperion && systemctl restart hyperionaml"])
		
	def installPackagesCallback(self, ret=None):
		self.session.open(MessageBox,_("Needed modules was installed and loaded.\n\nHyperion and Hyperionaml were restarted."), MessageBox.TYPE_INFO)
	
	def writeAmlService(self):
		
		script_txt = "[Unit]\n"
		script_txt += "Description=Hyperionaml Systemd service\n"
		script_txt += "Wants=enigma2.service\n"
		script_txt += "Wants=hyperion.service\n"
		script_txt += "[Service]\n"
		script_txt += "Type=simple\n"
		script_txt += "User=root\n"
		script_txt += "Group=root\n"
		script_txt += "UMask=007\n"
		
		width = int(str(config.plugins.hyperioncontrol.framegrabberSize.value).split(",")[0])
		height = int(str(config.plugins.hyperioncontrol.framegrabberSize.value).split(",")[1])
		freq = config.plugins.hyperioncontrol.framegrabberFreq.value
		script_txt += "ExecStart=/usr/bin/hyperion-aml -f %s --width %s --height %s\n" % (freq, width, height)
		
		script_txt += "ExecReload=/bin/kill -HUP $MAINPID\n"
		script_txt += "Restart=on-failure\n"
		script_txt += "TimeoutStopSec=10\n"
		script_txt += "[Install]\n"
		script_txt += "WantedBy=multi-user.target\n"
		
		amlservice_file = open("/lib/systemd/system/hyperionaml.service", "w+")
		amlservice_file.write(script_txt)
		amlservice_file.close()
		os.chmod("/lib/systemd/system/hyperionaml.service",0644)

	def getNewFixScanValue(self, ledNr, changeNumber, changes, currentPosition):
		#print "== scanValue", ledNr, changes
		hPicDeep = int(config.plugins.hyperioncontrol.hPicDeep.value) / 100.0
		vPicDeep = int(config.plugins.hyperioncontrol.vPicDeep.value) / 100.0
		
		hPicDist = self.hPicDist
		vPicDist = self.vPicDist
		#print "== position, changeLED, ledNr, ledIndex", currentPosition, changes[changeNumber], ledNr, ledNr-1
		
		#if ledNr == 1:
		#	print "== start position '%s' on ledNr '%s', index '%s'" % (currentPosition, ledNr, ledNr-1)
		
		#reset scan_min-Values after change position
		if changeNumber >0 and ledNr == changes[changeNumber-1]+1:
			#print "== new position '%s' on ledNr '%s', index '%s'" % (currentPosition, ledNr, ledNr-1)
			if currentPosition == "bottom":
				if config.plugins.hyperioncontrol.ledDirection.value == "1": #UZ
					self.hscan_min = 1.0000 - vPicDist
				elif config.plugins.hyperioncontrol.ledDirection.value == "2": #GUZ
					self.hscan_min = 0.0000 - self.h_diff + vPicDist
			
			elif currentPosition == "top":
				if config.plugins.hyperioncontrol.ledDirection.value == "1": #UZ
					self.hscan_min = 0.0000 - self.h_diff + vPicDist
				elif config.plugins.hyperioncontrol.ledDirection.value == "2": #GUZ
					self.hscan_min = 1.0000 - vPicDist
			
			elif currentPosition == "right":
				if config.plugins.hyperioncontrol.ledDirection.value == "1": #UZ
					self.vscan_min = 0.0000 - self.vr_diff + hPicDist
				elif config.plugins.hyperioncontrol.ledDirection.value == "2": #GUZ
					self.vscan_min = 1.0000 - hPicDist
			
			elif currentPosition == "left":
				if config.plugins.hyperioncontrol.ledDirection.value == "1": #UZ
					self.vscan_min = 1.0000 -hPicDist
				elif config.plugins.hyperioncontrol.ledDirection.value == "2": #GUZ
					self.vscan_min = 0.0000 - self.vl_diff + hPicDist
		
		#set scan-Values on Corner LED
		if changeNumber < 4 and ledNr == changes[changeNumber]:
			if currentPosition == "bottom":
				if config.plugins.hyperioncontrol.ledDirection.value == "1" and config.plugins.hyperioncontrol.ledCornerBottomLeft.value: #UZ
					#print "== corner led BottomLeft", ledNr, ledNr-1
					return (0.0000 + vPicDist, vPicDeep + vPicDist, 1.0000-hPicDeep - hPicDist, 1.0000 - hPicDist) #fix value for corner led BottomLeft
				elif config.plugins.hyperioncontrol.ledDirection.value == "2" and config.plugins.hyperioncontrol.ledCornerBottomRight.value: #GUZ
					#print "== corner led BottomRight", ledNr, ledNr-1
					return (1.0000 - vPicDeep - vPicDist, 1.0000 - vPicDist, 1.0000 - hPicDeep - hPicDist,1.0000 - hPicDist) #fix value for corner led BottomRight
			elif currentPosition == "top":
				if config.plugins.hyperioncontrol.ledDirection.value == "1" and config.plugins.hyperioncontrol.ledCornerTopRight.value: #UZ
					#print "== corner led TopRight", ledNr, ledNr-1
					return (1.0000-vPicDeep - vPicDist, 1.0000 - vPicDist, 0.0000 + hPicDist, hPicDeep + hPicDist) #fix value for corner led TopRight
				elif config.plugins.hyperioncontrol.ledDirection.value == "2" and config.plugins.hyperioncontrol.ledCornerTopLeft.value: #GUZ
					#print "== corner led TopLeft", ledNr, ledNr-1
					return (0.0000 + vPicDist, vPicDeep + vPicDist, 0.0000 + hPicDist, hPicDeep + hPicDist) #fix value for corner LED TopLeft
			elif currentPosition == "right":
				if config.plugins.hyperioncontrol.ledDirection.value == "1" and config.plugins.hyperioncontrol.ledCornerBottomRight.value: #UZ
					#print "== corner led BottomRight", ledNr, ledNr-1
					return (1.0000-vPicDeep - vPicDist, 1.0000 - vPicDist, 1.0000-hPicDeep - hPicDist,1.0000 - hPicDist) #fix value for corner led BottomRight
				elif config.plugins.hyperioncontrol.ledDirection.value == "2" and config.plugins.hyperioncontrol.ledCornerTopRight.value: #GUZ
					#print "== corner led TopRight", ledNr, ledNr-1
					return (1.0000-vPicDeep - vPicDist, 1.0000 - vPicDist, 0.0000 + hPicDist, hPicDeep + hPicDist) #fix value for corner led TopRight
			elif currentPosition == "left":
				#UZ
				if config.plugins.hyperioncontrol.ledDirection.value == "1" and config.plugins.hyperioncontrol.ledCornerTopLeft.value:
					#print "== corner led TopLeft", ledNr, ledNr-1
					return (0.0000 + vPicDist, vPicDeep + vPicDist, 0.0000 + hPicDist, hPicDeep + hPicDist) #fix value for corner LED TopLeft
				#GUZ
				elif config.plugins.hyperioncontrol.ledDirection.value == "2" and config.plugins.hyperioncontrol.ledCornerBottomLeft.value:
					#print "== corner led BottomLeft", ledNr, ledNr-1
					return (0.0000 + vPicDist, vPicDeep + vPicDist, 1.0000 - hPicDeep - hPicDist, 1.0000 - hPicDist) #fix value for corner led BottomLeft
		
		#jump hscan_min on LED-gap
		if self.gap > 0 and ledNr == self.gapLED:
			if config.plugins.hyperioncontrol.ledDirection.value == "1": #UZ
				self.hscan_min = self.hscan_min - (self.h_diff * self.gap)
			elif config.plugins.hyperioncontrol.ledDirection.value == "2": #GUZ
				self.hscan_min = self.hscan_min + (self.h_diff * self.gap)
		
		#Overlap in %
		overlap_h_diff  = self.h_diff  / 100 / 2 * int(config.plugins.hyperioncontrol.PicOverlap.value)
		overlap_vr_diff = self.vr_diff / 100 / 2 * int(config.plugins.hyperioncontrol.PicOverlap.value)
		overlap_vl_diff = self.vl_diff / 100 / 2 * int(config.plugins.hyperioncontrol.PicOverlap.value)
		
		#set scanValues 
		if currentPosition == "bottom":
			if config.plugins.hyperioncontrol.ledDirection.value == "1": #UZ
				self.hscan_min = self.hscan_min - self.h_diff
			elif config.plugins.hyperioncontrol.ledDirection.value == "2": #GUZ
				self.hscan_min = self.hscan_min + self.h_diff
			self.hscan_max = self.hscan_min + self.h_diff
			hscan_min = self.hscan_min - overlap_h_diff
			hscan_max = self.hscan_max + overlap_h_diff
			return (hscan_min, hscan_max, 1.000 - hPicDeep - hPicDist, 1.0000 - hPicDist) #vscan bottom fix
		
		elif currentPosition == "top":
			if config.plugins.hyperioncontrol.ledDirection.value == "1": #UZ
				self.hscan_min = self.hscan_min + self.h_diff
			elif config.plugins.hyperioncontrol.ledDirection.value == "2": #GUZ
				self.hscan_min = self.hscan_min - self.h_diff
			self.hscan_max = self.hscan_min + self.h_diff
			hscan_min = self.hscan_min - overlap_h_diff
			hscan_max = self.hscan_max + overlap_h_diff
			return (hscan_min, hscan_max, 0.0000 + hPicDist, hPicDeep + hPicDist) #vscan top fix
		
		elif currentPosition == "left":
			if config.plugins.hyperioncontrol.ledDirection.value == "1": #UZ
				self.vscan_min = self.vscan_min - self.vl_diff 
			elif config.plugins.hyperioncontrol.ledDirection.value == "2": #GUZ
				self.vscan_min = self.vscan_min + self.vl_diff
			self.vscan_max = self.vscan_min + self.vl_diff
			vscan_min = self.vscan_min - overlap_vl_diff
			vscan_max = self.vscan_max + overlap_vl_diff
			return (0.0000 + vPicDist, vPicDeep + vPicDist, vscan_min, vscan_max) #hscan left fix
		
		elif currentPosition == "right":
			if config.plugins.hyperioncontrol.ledDirection.value == "1": #UZ
				self.vscan_min = self.vscan_min + self.vr_diff
			elif config.plugins.hyperioncontrol.ledDirection.value == "2": #GUZ
				self.vscan_min = self.vscan_min - self.vr_diff
			self.vscan_max = self.vscan_min + self.vr_diff
			vscan_min = self.vscan_min - overlap_vr_diff
			vscan_max = self.vscan_max + overlap_vr_diff
			return (1.0000 - vPicDeep - vPicDist, 1.0000 - vPicDist, vscan_min, vscan_max) #hscan right fix
	
	def createNewLEDConfig(self):
		try:
			led_top   = int(config.plugins.hyperioncontrol.ledTop.value)
			led_right = int(config.plugins.hyperioncontrol.ledRight.value)
			led_left  = int(config.plugins.hyperioncontrol.ledLeft.value)
			self.gap  = int(config.plugins.hyperioncontrol.ledBottomGap.value)
			
			#count corner LEDs
			ledCornerTopLeft = 1 if config.plugins.hyperioncontrol.ledCornerTopLeft.value else 0
			ledCornerTopRight = 1 if config.plugins.hyperioncontrol.ledCornerTopRight.value else 0
			ledCornerBottomLeft = 1 if config.plugins.hyperioncontrol.ledCornerBottomLeft.value else 0
			ledCornerBottomRight = 1 if config.plugins.hyperioncontrol.ledCornerBottomRight.value else 0
			
			led_count = led_top*2 + led_right + led_left - self.gap + ledCornerTopLeft + ledCornerTopRight + ledCornerBottomLeft + ledCornerBottomRight
			#print "=== led-count", led_count
			
			#image area - distance
			self.hPicDist = int(config.plugins.hyperioncontrol.hPicDist.value) / 100.0
			self.vPicDist = int(config.plugins.hyperioncontrol.vPicDist.value) / 100.0
			
			self.h_diff  = (1.0 - 2 * self.vPicDist) / led_top if led_top else 0
			self.vr_diff = (1.0 - 2 * self.hPicDist) / led_right
			self.vl_diff = (1.0 - 2 * self.hPicDist) / led_left
			
			self.hscan_min = 0
			self.hscan_max = 0
			self.vscan_min = 0
			self.vscan_max = 0
			
			self.gapLED = 0
			
			#ledBegin "unten Mitte"
			if config.plugins.hyperioncontrol.ledBegin.value == "1":
				if config.plugins.hyperioncontrol.ledDirection.value == "1": # UZ
					change0 = (led_top // 2) - (self.gap // 2) + ledCornerBottomLeft
					change1 = change0 + led_left + ledCornerTopLeft
					change2 = change1 + led_top + ledCornerTopRight
					change3 = change2 + led_right + ledCornerBottomRight
					positions = ["bottom","left","top","right","bottom"]
					self.hscan_min = 0.5000 - (self.h_diff * (self.gap // 2)) # UZ = unten mitte nach links
					self.gapLED = 0
				else: #GUZ
					change0 = (led_top // 2) - (self.gap // 2) + ledCornerBottomRight
					change1 = change0 + led_right + ledCornerTopRight
					change2 = change1 + led_top + ledCornerTopLeft
					change3 = change2 + led_left + ledCornerBottomLeft
					positions = ["bottom","right","top","left","bottom"]
					self.hscan_min = 0.5000 - self.h_diff + (self.h_diff * (self.gap // 2)) # GUZ = unten mitte nach rechts
					self.gapLED = 0
				changes = [change0,change1,change2,change3]
			
			#ledBegin "rechts unten"
			if config.plugins.hyperioncontrol.ledBegin.value == "2":
				if config.plugins.hyperioncontrol.ledDirection.value == "1": # UZ
					change0 = led_top - self.gap + ledCornerBottomLeft
					change1 = change0 + led_left + ledCornerTopLeft
					change2 = change1 + led_top + ledCornerTopRight
					change3 = change2 + led_right + ledCornerBottomRight
					self.hscan_min = 1.0000 - self.vPicDist # UZ = unten von rechts nach links
					positions = ["bottom","left","top","right"]
					if self.gap:
						self.gapLED = (led_top // 2) - (self.gap // 2) + 1
				else: #GUZ
					change0 = led_right + ledCornerTopRight
					change1 = change0 + led_top + ledCornerTopLeft
					change2 = change1 + led_left + ledCornerBottomLeft
					change3 = change2 + led_top - self.gap + ledCornerBottomRight
					positions = ["right","top","left","bottom"]
					self.vscan_min = 1.0000 - self.hPicDist # GUZ = rechte Seite nach oben
					if self.gap:
						self.gapLED = change2 + (led_top // 2) - (self.gap // 2) + 1
				changes = [change0,change1,change2,change3]
			
			#ledBegin "rechts oben"
			if config.plugins.hyperioncontrol.ledBegin.value == "3":
				if config.plugins.hyperioncontrol.ledDirection.value == "1": # UZ
					change0 = led_right + ledCornerBottomRight
					change1 = change0 + led_top - self.gap + ledCornerBottomLeft
					change2 = change1 + led_left + ledCornerTopLeft
					change3 = change2 + led_top + ledCornerTopRight
					self.vscan_min = 0.0000 - self.vr_diff + self.hPicDist # UZ = rechts von oben nach unten
					positions = ["right", "bottom","left","top"]
					if self.gap:
						self.gapLED = change0 + (led_top // 2) - (self.gap // 2) + 1
				else: #GUZ
					change0 = led_top + ledCornerTopLeft
					change1 = change0 + led_left + ledCornerBottomLeft
					change2 = change1 + led_top - self.gap + ledCornerBottomRight
					change3 = change2 + led_right + ledCornerTopRight
					positions = ["top","left","bottom","right"]
					self.hscan_min = 1.0000 - self.vPicDist # GUZ = oben von rechts nach links
					if self.gap:
						self.gapLED = change1 + (led_top // 2) - (self.gap // 2) + 1
				changes = [change0,change1,change2,change3]
			
			#ledBegin "links oben"
			if config.plugins.hyperioncontrol.ledBegin.value == "4":
				if config.plugins.hyperioncontrol.ledDirection.value == "1": # UZ
					change0 = led_top + ledCornerTopRight
					change1 = change0 + led_right + ledCornerBottomRight
					change2 = change1 + led_top - self.gap + ledCornerBottomLeft
					change3 = change2 + led_left + ledCornerTopLeft
					self.hscan_min = 0.0000 - self.h_diff + self.vPicDist # UZ = oben von links nach rechts
					positions = ["top", "right", "bottom","left"]
					if self.gap:
						self.gapLED = change1 + (led_top // 2) - (self.gap // 2) + 1
				else: #GUZ
					change0 = led_left + ledCornerBottomLeft
					change1 = change0 + led_top - self.gap + ledCornerBottomRight
					change2 = change1 + led_right + ledCornerTopRight
					change3 = change2 + led_top + ledCornerTopLeft
					positions = ["left","bottom","right","top"]
					self.vscan_min = 0.0000 - self.vl_diff + self.hPicDist # GUZ = links von oben nach unten
					if self.gap:
						self.gapLED = change0 + (led_top // 2) - (self.gap // 2) + 1
				changes = [change0,change1,change2,change3]
			
			#ledBegin "links unten"
			if config.plugins.hyperioncontrol.ledBegin.value == "5":
				if config.plugins.hyperioncontrol.ledDirection.value == "1": # UZ
					change0 = led_left + ledCornerTopLeft
					change1 = change0 + led_top + ledCornerTopRight
					change2 = change1 + led_right + ledCornerBottomRight
					change3 = change2 + led_top - self.gap + ledCornerBottomLeft
					self.vscan_min = 1.000 - self.hPicDist # UZ = links von unten nach oben
					positions = ["left","top", "right", "bottom"]
					if self.gap:
						self.gapLED = change2 + (led_top // 2) - (self.gap // 2) + 1
				else: #GUZ
					change0 = led_top - self.gap + ledCornerBottomRight
					change1 = change0 + led_right + ledCornerTopRight
					change2 = change1 + led_top + ledCornerTopLeft
					change3 = change2 + led_left + ledCornerBottomLeft
					positions = ["bottom","right","top","left"]
					self.hscan_min = 0.0000 - self.h_diff + self.vPicDist # GUZ = unten von links nach rechts
					if self.gap:
						self.gapLED = (led_top // 2) - (self.gap // 2) + 1
				changes = [change0,change1,change2,change3]
				
			#print "=== changes, positions, gapLED", changes, positions, self.gapLED
			leds = []
			for i in range(1,led_count+1):
				position = 0
				for x in changes:
					if i<= x:
						break
					position +=1
				changeNumber = position
				
				(hscan_min, hscan_max, vscan_min, vscan_max) = self.getNewFixScanValue(i,changeNumber,changes,positions[position])
				
				#if use overlap cut to min/max
				if hscan_min < 0.0000: hscan_min = 0.0000
				if hscan_min > 1.0000: hscan_min = 1.0000
				if hscan_max < 0.0000: hscan_max = 0.0000
				if hscan_max > 1.0000: hscan_max = 1.0000
				if vscan_min < 0.0000: vscan_min = 0.0000
				if vscan_min > 1.0000: vscan_min = 1.0000
				if vscan_max < 0.0000: vscan_max = 0.0000
				if vscan_max > 1.0000: vscan_max = 1.0000
				
				led = OrderedDict()
				led['index'] = int(i-1)
				led['hscan'] = {'minimum': abs(hscan_min), 'maximum': abs(hscan_max)}
				led['vscan'] = {'minimum': abs(vscan_min), 'maximum': abs(vscan_max)}
				leds.append(led)
				#print "=== led dict", led
				
				#print "index: ", i-1
				#print '"hscan" : { "minimum" : %s, "maximum" : %s },' % (format(round(hscan_min,4),".4f"), format(round(hscan_max,4),".4f"))
				#print '"vscan" : { "minimum" : %s, "maximum" : %s }' % (format(round(vscan_min,4),".4f"), format(round(vscan_max,4),".4f"))
				#print "------------------------------------------------"
			#print "=== leds", leds
			return leds

		except:
			import traceback
			traceback.print_exc()
			return None

	def importJsonBak(self, retval):
		try:
			if not retval:
				return
			
			#read values from config.json.bak
			if not self.jsonConfig:
				self.session.open(MessageBox,_("There are no data in '/etc/hyperion/hyperion.config.json'!\n\nAn import is therefore not possible."), MessageBox.TYPE_INFO,timeout=5)
				return
			
			self.jsonConfigBak= ""
			config_file_path ="/etc/hyperion/hyperion.config.json.bak"
			if os.path.exists(config_file_path): 
				#json.bak einlesen
				valuesFromConfig = open(config_file_path).read()
				lines = valuesFromConfig.split("\n")
				newlines=[]
				for line in lines:
					cleanline = line.replace("\t","")
					if not cleanline.rstrip().startswith("//") and cleanline.strip() != "":
						newlines.append(line)
				valuesFromConfig = "\n".join(newlines)
				self.jsonConfigBak = json.loads(valuesFromConfig, object_pairs_hook=OrderedDict)
				
				#alle Hauptkeys aus json.bak in json übernehmen
				for (k, v) in self.jsonConfigBak.items():
					#print "===", k
					key = str(k)
					if key in self.jsonConfig:
						self.jsonConfig[key] = self.jsonConfigBak[key]
				
				#reload configs from jsonConfigBak
				# hsv
				setConfigValueFromJson(config.plugins.hyperioncontrol.saturationGain, self.jsonConfigBak, ['color','transform',0,'hsv','saturationGain'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.valueGain, self.jsonConfigBak, ['color','transform',0,'hsv','valueGain'],100)
				# hsl
				setConfigValueFromJson(config.plugins.hyperioncontrol.saturationLGain, self.jsonConfigBak, ['color','transform',0,'hsl','saturationLGain'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.luminanceGain, self.jsonConfigBak, ['color','transform',0,'hsl','luminanceGain'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.luminanceMinimum, self.jsonConfigBak, ['color','transform',0,'hsl','luminanceMinimum'],100)
				# red
				setConfigValueFromJson(config.plugins.hyperioncontrol.gammaRed, self.jsonConfigBak, ['color','transform',0,'red','gamma'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.thresholdRed, self.jsonConfigBak, ['color','transform',0,'red','threshold'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.temperatureRed, self.jsonConfigBak, ['color','temperature',0,'correctionValues','red'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.redAdjustRed, self.jsonConfigBak, ['color','channelAdjustment',0,'pureRed','redChannel'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.greenAdjustRed, self.jsonConfigBak, ['color','channelAdjustment',0,'pureGreen','redChannel'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.blueAdjustRed, self.jsonConfigBak, ['color','channelAdjustment',0,'pureBlue','redChannel'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.whitelevelRed, self.jsonConfigBak, ['color','transform',0,'red','whitelevel'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.blacklevelRed, self.jsonConfigBak, ['color','transform',0,'red','blacklevel'],100)
				
				# green
				setConfigValueFromJson(config.plugins.hyperioncontrol.gammaGreen, self.jsonConfigBak, ['color','transform',0,'green','gamma'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.thresholdGreen, self.jsonConfigBak, ['color','transform',0,'green','threshold'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.temperatureGreen, self.jsonConfigBak, ['color','temperature',0,'correctionValues','green'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.redAdjustGreen, self.jsonConfigBak, ['color','channelAdjustment',0,'pureRed','greenChannel'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.greenAdjustGreen, self.jsonConfigBak, ['color','channelAdjustment',0,'pureGreen','greenChannel'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.blueAdjustGreen, self.jsonConfigBak, ['color','channelAdjustment',0,'pureBlue','greenChannel'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.whitelevelGreen, self.jsonConfigBak, ['color','transform',0,'green','whitelevel'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.blacklevelGreen, self.jsonConfigBak, ['color','transform',0,'green','blacklevel'],100)
				
				# blue
				setConfigValueFromJson(config.plugins.hyperioncontrol.gammaBlue, self.jsonConfigBak, ['color','transform',0,'blue','gamma'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.thresholdBlue, self.jsonConfigBak, ['color','transform',0,'blue','threshold'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.temperatureBlue, self.jsonConfigBak, ['color','temperature',0,'correctionValues','blue'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.redAdjustBlue, self.jsonConfigBak, ['color','channelAdjustment',0,'pureRed','blueChannel'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.greenAdjustBlue, self.jsonConfigBak, ['color','channelAdjustment',0,'pureGreen','blueChannel'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.blueAdjustBlue, self.jsonConfigBak, ['color','channelAdjustment',0,'pureBlue','blueChannel'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.whitelevelBlue, self.jsonConfigBak, ['color','transform',0,'blue','whitelevel'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.blacklevelBlue, self.jsonConfigBak, ['color','transform',0,'blue','blacklevel'],100)
				
				# device
				setConfigValueFromJson(config.plugins.hyperioncontrol.deviceType, self.jsonConfigBak, ['device','type'])
				setConfigValueFromJson(config.plugins.hyperioncontrol.configName, self.jsonConfigBak, ['device','name'])
				if config.plugins.hyperioncontrol.deviceType.value in ("udpraw","philipshue","philipshueentertainment"):
					outputIP = setConfigValueFromJson(config.plugins.hyperioncontrol.outputIP, self.jsonConfigBak, ['device','output'], onlyReturnValue=True)
					outputIP = outputIP.replace(":19446","").split(".")
					outputIP = [int(d) for d in outputIP]
					config.plugins.hyperioncontrol.outputIP.value = outputIP
				setConfigValueFromJson(config.plugins.hyperioncontrol.colorOrder, self.jsonConfigBak, ['device','colorOrder'])
				if config.plugins.hyperioncontrol.deviceType.value == "philipshue":
					setConfigValueFromJson(config.plugins.hyperioncontrol.phe_username, self.jsonConfigBak, ['device','username'])
					lightIDs = setConfigValueFromJson(config.plugins.hyperioncontrol.phe_lightIds, self.jsonConfigBak, ['device','lightIds'], onlyReturnValue=True)
				if config.plugins.hyperioncontrol.deviceType.value == "philipshueentertainment":
					setConfigValueFromJson(config.plugins.hyperioncontrol.phe_username, self.jsonConfigBak, ['device','username'])
					setConfigValueFromJson(config.plugins.hyperioncontrol.phe_clientkey, self.jsonConfigBak, ['device','clientkey'])
					lightIDs = setConfigValueFromJson(config.plugins.hyperioncontrol.phe_lightIds, self.jsonConfigBak, ['device','lightIds'], onlyReturnValue=True)
					config.plugins.hyperioncontrol.phe_lightIds.value = ', '.join(map(str, lightIDs))
					setConfigValueFromJson(config.plugins.hyperioncontrol.phe_groupId, self.jsonConfigBak, ['device','groupId'])
					setConfigValueFromJson(config.plugins.hyperioncontrol.delayafterconnect, self.jsonConfigBak, ['device','delayafterconnect'])
				if config.plugins.hyperioncontrol.deviceType.value in ("philipshue","philipshueentertainment"):
					self.jsonConfig['device']['switchOffOnBlack'] = str(config.plugins.hyperioncontrol.phe_switchOffOnBlack.value)
				else:
					setConfigValueFromJson(config.plugins.hyperioncontrol.baudrate, self.jsonConfigBak, ['device','rate'],calculate=1)

				#outputType
				if config.plugins.hyperioncontrol.deviceType.value in ("sedu","adalight","AdalightApa102","atmo","karate"):
					setConfigValueFromJson(config.plugins.hyperioncontrol.outputTYPE, self.jsonConfigBak, ['device','output'])

				#Framegrabber
				width = setConfigValueFromJson(None, self.jsonConfigBak, ['framegrabber','width'],None,True,"160")
				height = setConfigValueFromJson(None, self.jsonConfigBak, ['framegrabber','height'],None,True,"160")
				config.plugins.hyperioncontrol.framegrabberSize.value = str(width) + "," + str(height)
				setConfigValueFromJson(config.plugins.hyperioncontrol.framegrabberFreq, self.jsonConfigBak, ['framegrabber','frequency_Hz'],1)
				
				#Smoothing
				setConfigValueFromJson(config.plugins.hyperioncontrol.smoothingupdateFrequency, self.jsonConfigBak, ['smoothing','updateFrequency'],1)

				#BlackborderDetector(not in remote only in json)
				bbdEnable = setConfigValueFromJson(config.plugins.hyperioncontrol.bbdEnable, self.jsonConfigBak, ['blackborderdetector','enable'],calculate=None,onlyReturnValue=True)
				if str(bbdEnable).lower() == "true":
					config.plugins.hyperioncontrol.bbdEnable.value = True
				else:
					config.plugins.hyperioncontrol.bbdEnable.value = False
				setConfigValueFromJson(config.plugins.hyperioncontrol.bbdThreshold, self.jsonConfigBak, ['blackborderdetector','threshold'],calculate=100)
				
				#webif
				webConfigEnable = setConfigValueFromJson(config.plugins.hyperioncontrol.webConfigEnable, self.jsonConfigBak, ['webConfig','enable'],calculate=None,onlyReturnValue=True)
				if str(webConfigEnable).lower() == "true":
					config.plugins.hyperioncontrol.webConfigEnable.value = True
				else:
					config.plugins.hyperioncontrol.webConfigEnable.value = False
				setConfigValueFromJson(config.plugins.hyperioncontrol.webConfigPort, self.jsonConfigBak, ['webConfig','port'],calculate=1)
				
				#bootsequence
				effect = setConfigValueFromJson(config.plugins.hyperioncontrol.bootseqEffect, self.jsonConfigBak, ['bootsequence','effect'],calculate=None,onlyReturnValue=True)
				color = setConfigValueFromJson(config.plugins.hyperioncontrol.bootseqColor, self.jsonConfigBak, ['bootsequence','color'],calculate=None,onlyReturnValue=True)
				if effect:
					config.plugins.hyperioncontrol.bootseqStart.value = "effect"
					config.plugins.hyperioncontrol.bootseqEffect.choices.choices = [(effect,effect)]
					config.plugins.hyperioncontrol.bootseqEffect.value = str(effect)
				else:
					if color == [0,0,0]:
						config.plugins.hyperioncontrol.bootseqStart.value = "off"
					else:
						config.plugins.hyperioncontrol.bootseqStart.value = "color"
					effect = config.plugins.hyperioncontrol.bootseqEffect.default
					config.plugins.hyperioncontrol.bootseqEffect.choices.choices = [(effect,effect)]
					config.plugins.hyperioncontrol.bootseqEffect.value = str(effect)
				
				if color:
					color = "#" + '{:02x}'.format(color[0]).upper() + '{:02x}'.format(color[1]).upper() + '{:02x}'.format(color[2]).upper()
					colorName = self.ColorNames.getColorName(color)
					config.plugins.hyperioncontrol.bootseqColor.choices.choices = [(color,colorName)]
					config.plugins.hyperioncontrol.bootseqColor.value = str(color)
				setConfigValueFromJson(config.plugins.hyperioncontrol.bootseqDuration, self.jsonConfigBak, ['bootsequence','duration_ms'],calculate=1)
				
				self.jsonConfigBak= ""
				
				#reload ConfigList with new values
				self.buildConfig()
				self.session.open(MessageBox,_("The import from the file '/etc/hyperion/hyperion.config.json.bak' has been successfully completed."), MessageBox.TYPE_INFO,timeout=5)
			
			else:
				self.session.open(MessageBox,_("Import failed!\n\nFile '/etc/hyperion/hyperion.config.json.bak' not found!"), MessageBox.TYPE_INFO,timeout=5)

		except:
			import traceback
			traceback.print_exc()
			self.session.open(MessageBox,_("Error importing the 'hyperion.config.json.bak'!"), MessageBox.TYPE_INFO,timeout=5)
			self.jsonConfigBak= ""

	def readValuesFromConfig(self):
		
		try:
			#read values from config.json
			self.jsonConfig = ""
			config_file_path ="/etc/hyperion/hyperion.config.json"
			if os.path.exists(config_file_path): 
				valuesFromConfig = open(config_file_path).read()
				lines = valuesFromConfig.split("\n")
				newlines=[]
				for line in lines:
					cleanline = line.replace("\t","")
					if not cleanline.rstrip().startswith("//") and cleanline.strip() != "":
						newlines.append(line)
				valuesFromConfig = "\n".join(newlines)
				self.jsonConfig = json.loads(valuesFromConfig, object_pairs_hook=OrderedDict)
				
				#Framegrabber(not in remote only in json)
				config.plugins.hyperioncontrol.framegrabberSize.value = str(self.jsonConfig['framegrabber']['width']) + "," + str(self.jsonConfig['framegrabber']['height'])
				config.plugins.hyperioncontrol.framegrabberFreq.value = str(int(self.jsonConfig['framegrabber']['frequency_Hz']))
				#BlackborderDetector(not in remote only in json)
				bbdenabled = self.jsonConfig['blackborderdetector']['enable']
				if str(bbdenabled).lower() == "true":
					config.plugins.hyperioncontrol.bbdEnable.value = True
				else:
					config.plugins.hyperioncontrol.bbdEnable.value = False
				config.plugins.hyperioncontrol.bbdThreshold.value = str(int(float(self.jsonConfig['blackborderdetector']['threshold']) * 100))
				
				#webif
				webConfigEnabled = self.jsonConfig['webConfig']['enable']
				if str(webConfigEnabled).lower() == "true":
					config.plugins.hyperioncontrol.webConfigEnable.value = True
				else:
					config.plugins.hyperioncontrol.webConfigEnable.value = False
				config.plugins.hyperioncontrol.webConfigPort.value = int(self.jsonConfig['webConfig']['port'])
				
				#bootsequence
				effect = self.jsonConfig['bootsequence']['effect']
				color = self.jsonConfig['bootsequence']['color']
				if effect:
					config.plugins.hyperioncontrol.bootseqStart.value = "effect"
					config.plugins.hyperioncontrol.bootseqEffect.choices.choices = [(effect,effect)]
					config.plugins.hyperioncontrol.bootseqEffect.value = str(effect)
				else:
					if color == [0,0,0]:
						config.plugins.hyperioncontrol.bootseqStart.value = "off"
					else:
						config.plugins.hyperioncontrol.bootseqStart.value = "color"
					effect = config.plugins.hyperioncontrol.bootseqEffect.default
					config.plugins.hyperioncontrol.bootseqEffect.choices.choices = [(effect,effect)]
					config.plugins.hyperioncontrol.bootseqEffect.value = str(effect)
				if color:
					color = "#" + '{:02x}'.format(color[0]).upper() + '{:02x}'.format(color[1]).upper() + '{:02x}'.format(color[2]).upper()
					colorName = self.ColorNames.getColorName(color)
					config.plugins.hyperioncontrol.bootseqColor.choices.choices = [(color,colorName)]
					config.plugins.hyperioncontrol.bootseqColor.value = str(color)
				config.plugins.hyperioncontrol.bootseqDuration.value = str(self.jsonConfig['bootsequence']['duration_ms'])
				
		except:
			import traceback, sys
			traceback.print_exc()
			exc_type, exc_value, exc_traceback = sys.exc_info()
			error = "\n".join(traceback.format_exception_only(exc_type, exc_value))
			self.session.open(MessageBox,_("Error loading the '/etc/hyperion/hyperion.config.json'!\n\nError:\n%s") % error, MessageBox.TYPE_INFO,timeout=5)

	def buildConfig(self):
		
		self.list = []
		if self.setupPage == "transform":
			self.list.append(getConfigListEntry(_("HSV (0-500, default=100)"), ))
			self.list.append(getConfigListEntry(_("Saturation Gain"), NoSave(config.plugins.hyperioncontrol.saturationGain)))
			self.list.append(getConfigListEntry(_("Value Gain"), NoSave(config.plugins.hyperioncontrol.valueGain)))
			self.list.append(getConfigListEntry("", )) 
			
			self.list.append(getConfigListEntry(_("HSL"), ))
			self.list.append(getConfigListEntry(_("SaturationL Gain (0-100, default=100)"), NoSave(config.plugins.hyperioncontrol.saturationLGain)))
			self.list.append(getConfigListEntry(_("Luminance Gain (0-100, default=100)"), NoSave(config.plugins.hyperioncontrol.luminanceGain)))
			self.list.append(getConfigListEntry(_("Luminance Minimum (0-50, default=0)"), NoSave(config.plugins.hyperioncontrol.luminanceMinimum)))
			self.list.append(getConfigListEntry("", ))
			
			self.list.append(getConfigListEntry(_("Gamma (0-500, default=250)"), )) 
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.gammaRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.gammaGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.gammaBlue)) )
			self.list.append(getConfigListEntry("", ))
					
			self.list.append(getConfigListEntry(_("Threshold (0-100, default=0)"), )) 
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.thresholdRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.thresholdGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.thresholdBlue)) )
			self.list.append(getConfigListEntry("", ))
					
			self.list.append(getConfigListEntry(_("Temperature (0-255, default=255)"), )) 
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.temperatureRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.temperatureGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.temperatureBlue)) )
			self.list.append(getConfigListEntry("", ))
			
			self.list.append(getConfigListEntry(_("Red Adjust (0-255, default=255, 0, 0)"), ))
			self.list.append(getConfigListEntry(_("red (fix)"), NoSave(config.plugins.hyperioncontrol.redAdjustRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.redAdjustGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.redAdjustBlue)) )
			self.list.append(getConfigListEntry("", ))
			
			self.list.append(getConfigListEntry(_("Green Adjust (0-255, default=0, 255, 0)"), ))
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.greenAdjustRed)) )
			self.list.append(getConfigListEntry(_("green (fix)"), NoSave(config.plugins.hyperioncontrol.greenAdjustGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.greenAdjustBlue)) )
			self.list.append(getConfigListEntry("", ))
			
			self.list.append(getConfigListEntry(_("Blue Adjust (0-255, default=0, 0, 255)"), ))
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.blueAdjustRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.blueAdjustGreen)) )
			self.list.append(getConfigListEntry(_("blue (fix)"), NoSave(config.plugins.hyperioncontrol.blueAdjustBlue)) )
			self.list.append(getConfigListEntry("", ))
			
			self.list.append(getConfigListEntry(_("Whitelevel (0-100, default=100)"), )) 
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.whitelevelRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.whitelevelGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.whitelevelBlue)) )
			self.list.append(getConfigListEntry("", ))
			
			self.list.append(getConfigListEntry(_("Blacklevel (0-50, default=0)"), )) 
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.blacklevelRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.blacklevelGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.blacklevelBlue)) )
			self.list.append(getConfigListEntry("", ))
			
			self.list.append(getConfigListEntry(_("Framegrabber"), ))
			self.list.append(getConfigListEntry(_("Size (default=160x160)"), NoSave(config.plugins.hyperioncontrol.framegrabberSize)) )
			self.list.append(getConfigListEntry(_("Frequency in Hz (10-25, default=10)"), NoSave(config.plugins.hyperioncontrol.framegrabberFreq)) )
			self.list.append(getConfigListEntry("", ))
			
			self.list.append(getConfigListEntry(_("BlackBorderDetection"), ))
			self.list.append(getConfigListEntry(_("enabled"), NoSave(config.plugins.hyperioncontrol.bbdEnable)) )
			self.list.append(getConfigListEntry(_("threshold (1-20, default=4)"), NoSave(config.plugins.hyperioncontrol.bbdThreshold)) )
			self.list.append(getConfigListEntry("", ))
			
			self.list.append(getConfigListEntry(_("Webif"), ))
			self.webConfigIndex = self.list.index((_("Webif"), ))
			self.list.append(getConfigListEntry(_("enabled"), NoSave(config.plugins.hyperioncontrol.webConfigEnable)) )
			self.list.append(getConfigListEntry(_("port (default=8099)"), NoSave(config.plugins.hyperioncontrol.webConfigPort)) )
			self.list.append(getConfigListEntry("", ))
			self.writeWepifIP()
			
			self.list.append(getConfigListEntry(_("Bootsequence"), ))
			self.list.append(getConfigListEntry(_("start with"), NoSave(config.plugins.hyperioncontrol.bootseqStart)) )
			if config.plugins.hyperioncontrol.bootseqStart.value != "off":
				if config.plugins.hyperioncontrol.bootseqStart.value == "effect":
					self.list.append(getConfigListEntry(_("... select start effect (with ok key)"), NoSave(config.plugins.hyperioncontrol.bootseqEffect)) )
				else:
					self.list.append(getConfigListEntry(_("... select start color (with ok key)"), NoSave(config.plugins.hyperioncontrol.bootseqColor)) )
				self.list.append(getConfigListEntry(_("duration in ms"), NoSave(config.plugins.hyperioncontrol.bootseqDuration)) )
			self.list.append(getConfigListEntry("", ))
			
			self.list.append(getConfigListEntry(_("Idle actions"), ))
			self.list.append(getConfigListEntry(_("on Idle action"), config.plugins.hyperioncontrol.onIdleAction) )
			if config.plugins.hyperioncontrol.onIdleAction.value != "nothing":
				if config.plugins.hyperioncontrol.onIdleAction.value == "effect":
					self.list.append(getConfigListEntry(_("... select idle effect (with ok key)"), config.plugins.hyperioncontrol.onIdleEffect) )
				else:
					self.list.append(getConfigListEntry(_("... select idle color (with ok key)"), config.plugins.hyperioncontrol.onIdleColor) )
			self.list.append(getConfigListEntry(_("leave Idle action"), config.plugins.hyperioncontrol.onIdlebackAction) )
			if config.plugins.hyperioncontrol.onIdlebackAction.value != "nothing":
				if config.plugins.hyperioncontrol.onIdlebackAction.value == "effect":
					self.list.append(getConfigListEntry(_("... select start effect (with ok key)"), config.plugins.hyperioncontrol.onIdlebackEffect) )
				elif config.plugins.hyperioncontrol.onIdlebackAction.value == "color":
					self.list.append(getConfigListEntry(_("... select start color (with ok key)"), config.plugins.hyperioncontrol.onIdlebackColor) )
			
		elif self.setupPage == "device":
			self.list.append(getConfigListEntry(_("Device-Setup"), ))
			self.list.append(getConfigListEntry(_("Device-Typ"), config.plugins.hyperioncontrol.deviceType))
			self.list.append(getConfigListEntry(_("Config-Name"), config.plugins.hyperioncontrol.configName))
			if config.plugins.hyperioncontrol.deviceType.value == "udpraw":
				self.list.append(getConfigListEntry(_("Device-IP (fix port: 19446)"), config.plugins.hyperioncontrol.outputIP))
			elif config.plugins.hyperioncontrol.deviceType.value in ("philipshue","philipshueentertainment"):
				self.list.append(getConfigListEntry(_("Device-IP"), config.plugins.hyperioncontrol.outputIP))
			if config.plugins.hyperioncontrol.deviceType.value in ("sedu","adalight","AdalightApa102","atmo","karate"):
				self.list.append(getConfigListEntry(_("Output"), config.plugins.hyperioncontrol.outputTYPE))
				self.list.append(getConfigListEntry(_("delayafterconnect (0-20, default=0)"), config.plugins.hyperioncontrol.delayafterconnect))
			if config.plugins.hyperioncontrol.deviceType.value == "philipshue":
				self.list.append(getConfigListEntry(_("UserName"), config.plugins.hyperioncontrol.phe_username))
				self.list.append(getConfigListEntry(_("LightIDs"), config.plugins.hyperioncontrol.phe_lightIds))
				self.list.append(getConfigListEntry(_("Switch Off On Black"), config.plugins.hyperioncontrol.phe_switchOffOnBlack))
			if config.plugins.hyperioncontrol.deviceType.value == "philipshueentertainment":
				self.list.append(getConfigListEntry(_("UserName"), config.plugins.hyperioncontrol.phe_username))
				self.list.append(getConfigListEntry(_("ClientKey"), config.plugins.hyperioncontrol.phe_clientkey))
				self.list.append(getConfigListEntry(_("LightIDs"), config.plugins.hyperioncontrol.phe_lightIds))
				self.list.append(getConfigListEntry(_("GroupID"), config.plugins.hyperioncontrol.phe_groupId))
				self.list.append(getConfigListEntry(_("Switch Off On Black"), config.plugins.hyperioncontrol.phe_switchOffOnBlack))
			if config.plugins.hyperioncontrol.deviceType.value in ("philipshue","philipshueentertainment"):
				self.list.append(getConfigListEntry(_("colorOrder"), config.plugins.hyperioncontrol.colorOrder))
			else:
				self.list.append(getConfigListEntry(_("colorOrder"), config.plugins.hyperioncontrol.colorOrder))
				self.list.append(getConfigListEntry(_("Baudrate"), config.plugins.hyperioncontrol.baudrate))
			
			self.list.append(getConfigListEntry("", ))
			self.list.append(getConfigListEntry(_("LED-Setup"), ))
			self.ledSetupIndex = self.list.index((_("LED-Setup"), ))
			self.list.append(getConfigListEntry(_("LED begin"), config.plugins.hyperioncontrol.ledBegin))
			if config.plugins.hyperioncontrol.ledBegin.value != "0":
				self.list.append(getConfigListEntry(_("LED direction"), config.plugins.hyperioncontrol.ledDirection))
				self.list.append(getConfigListEntry(_("Number of LEDs top"), config.plugins.hyperioncontrol.ledTop))
				self.list.append(getConfigListEntry(_("Number of LEDs right"), config.plugins.hyperioncontrol.ledRight))
				self.list.append(getConfigListEntry(_("Number of LEDs left"), config.plugins.hyperioncontrol.ledLeft))
				self.list.append(getConfigListEntry(_("Number of LEDs gap bottom"), config.plugins.hyperioncontrol.ledBottomGap))
				self.list.append(getConfigListEntry(_("Corner LED left top"), config.plugins.hyperioncontrol.ledCornerTopLeft))
				self.list.append(getConfigListEntry(_("Corner LED right top"), config.plugins.hyperioncontrol.ledCornerTopRight))
				self.list.append(getConfigListEntry(_("Corner LED left bottom"), config.plugins.hyperioncontrol.ledCornerBottomLeft))
				self.list.append(getConfigListEntry(_("Corner LED right bottom"), config.plugins.hyperioncontrol.ledCornerBottomRight))
				
				self.list.append(getConfigListEntry("", ))
				self.list.append(getConfigListEntry(_("LED-Image Area"), ))
				self.list.append(getConfigListEntry(_("horizontal depth (default=8%)"), config.plugins.hyperioncontrol.hPicDeep))
				self.list.append(getConfigListEntry(_("vertical depth (default=5%)"), config.plugins.hyperioncontrol.vPicDeep))
				self.list.append(getConfigListEntry(_("horizontal distance (default=0%)"), config.plugins.hyperioncontrol.hPicDist))
				self.list.append(getConfigListEntry(_("vertical distance (default=0%)"), config.plugins.hyperioncontrol.vPicDist))
				self.list.append(getConfigListEntry(_("overlap (default=0%)"), config.plugins.hyperioncontrol.PicOverlap))
				self.writeLedCount()
				
				self.list.append(getConfigListEntry("", ))
				self.list.append(getConfigListEntry(_("Smoothing"), ))
				self.list.append(getConfigListEntry(_("Update Frequency (default=20 Hz)"), config.plugins.hyperioncontrol.smoothingupdateFrequency))
		
		self["config"].list = self.list
		self["config"].l.setList(self.list) 
	
	def getConfigName(self, subsection, configelement):
		for item in subsection.dict():
			conf = subsection.__getattr__(item)
			if conf == configelement:
				return item

	def writeWepifIP(self):
		if config.plugins.hyperioncontrol.webConfigEnable.value:
			ipA = self.getCurrentIP()
			ipA = "http://" + ipA + ":%s" % int(config.plugins.hyperioncontrol.webConfigPort.value)
			self.list[self.webConfigIndex] = ((_("Webif") + "  (%s)" % ipA,))
			self["config"].l.invalidateEntry(self.webConfigIndex)
		else:
			self.list[self.webConfigIndex] = ((_("Webif"),))
			self["config"].l.invalidateEntry(self.webConfigIndex)
		
	def writeLedCount(self):
		led_top   = int(config.plugins.hyperioncontrol.ledTop.value)
		led_right = int(config.plugins.hyperioncontrol.ledRight.value)
		led_left  = int(config.plugins.hyperioncontrol.ledLeft.value)
		led_gap  = int(config.plugins.hyperioncontrol.ledBottomGap.value)
		led_count = led_top*2 + led_right + led_left - led_gap
		for ledCornerConfig in (config.plugins.hyperioncontrol.ledCornerTopLeft,config.plugins.hyperioncontrol.ledCornerTopRight,config.plugins.hyperioncontrol.ledCornerBottomLeft,config.plugins.hyperioncontrol.ledCornerBottomRight):
			if ledCornerConfig.value:
				led_count += 1
		self.list[self.ledSetupIndex] = ((_("LED-Setup (Number of LEDs: %s)") % led_count,))
		self["config"].l.invalidateEntry(self.ledSetupIndex)
	
	def changed(self):
		current = self["config"].getCurrent()
		configName = self.getConfigName(config.plugins.hyperioncontrol, current[1])
		#print "[HyperionControl] - change:", configName
		
		if configName in ("deviceType", "ledBegin", "bootseqStart","onIdleAction","onIdlebackAction"):
			#set to default baudrate for devices
			if configName == "deviceType" and current[1].value == "sedu":
				config.plugins.hyperioncontrol.baudrate.value = "500000"
			elif configName == "deviceType" and current[1].value == "karate":
				config.plugins.hyperioncontrol.baudrate.value = "57600"
			elif configName == "deviceType" and current[1].value == "adalight":
				config.plugins.hyperioncontrol.baudrate.value = "115200"
			elif configName == "deviceType" and current[1].value == "AdalightApa102":
				config.plugins.hyperioncontrol.baudrate.value = "115200"
			elif configName == "deviceType" and current[1].value == "atmo":
				config.plugins.hyperioncontrol.baudrate.value = "38400"
			elif configName == "deviceType":
				config.plugins.hyperioncontrol.baudrate.value = "200000"
			self.buildConfig()
			return
		
		if configName.startswith("led"):
			self.writeLedCount()
		
		if configName.startswith("webConfig"):
			self.writeWepifIP()
		
		cmd = ""
		if configName == "saturationGain":
			value = int(config.plugins.hyperioncontrol.saturationGain.value) / 100.0
			cmd = "-s %s" % value
		elif configName == "valueGain":
			value = int(config.plugins.hyperioncontrol.valueGain.value) / 100.0
			cmd = "-v %s" % value
		elif configName == "saturationLGain":
			value = int(config.plugins.hyperioncontrol.saturationLGain.value) / 100.0
			cmd = "-u %s" % value
		elif configName == "luminanceGain":
			value = int(config.plugins.hyperioncontrol.luminanceGain.value) / 100.0
			cmd = "-m %s" % value
		elif configName == "luminanceMinimum":
			value = int(config.plugins.hyperioncontrol.luminanceMinimum.value) / 100.0
			cmd = "-n %s" % value
		elif configName.startswith("gamma"):
			Red = int(config.plugins.hyperioncontrol.gammaRed.value) / 100.0
			Green = int(config.plugins.hyperioncontrol.gammaGreen.value) / 100.0
			Blue = int(config.plugins.hyperioncontrol.gammaBlue.value) / 100.0
			cmd = "-g '%s %s %s'" % (Red, Green, Blue)
		elif configName.startswith("threshold"):
			Red = int(config.plugins.hyperioncontrol.thresholdRed.value) / 100.0
			Green = int(config.plugins.hyperioncontrol.thresholdGreen.value) / 100.0
			Blue = int(config.plugins.hyperioncontrol.thresholdBlue.value) / 100.0
			cmd = "-t '%s %s %s'" % (Red, Green, Blue)
		elif configName.startswith("temperature"):
			Red = int(config.plugins.hyperioncontrol.temperatureRed.value)
			Green = int(config.plugins.hyperioncontrol.temperatureGreen.value)
			Blue = int(config.plugins.hyperioncontrol.temperatureBlue.value)
			cmd = "-Z '%s %s %s'" % (Red, Green, Blue)
		elif configName.startswith("redAdjust"):
			Red = int(config.plugins.hyperioncontrol.redAdjustRed.value)
			Green = int(config.plugins.hyperioncontrol.redAdjustGreen.value)
			Blue = int(config.plugins.hyperioncontrol.redAdjustBlue.value)
			cmd = "-R '%s %s %s'" % (Red, Green, Blue)
		elif configName.startswith("greenAdjust"):
			Red = int(config.plugins.hyperioncontrol.greenAdjustRed.value)
			Green = int(config.plugins.hyperioncontrol.greenAdjustGreen.value)
			Blue = int(config.plugins.hyperioncontrol.greenAdjustBlue.value)
			cmd = "-G '%s %s %s'" % (Red, Green, Blue)
		elif configName.startswith("blueAdjust"):
			Red = int(config.plugins.hyperioncontrol.blueAdjustRed.value)
			Green = int(config.plugins.hyperioncontrol.blueAdjustGreen.value)
			Blue = int(config.plugins.hyperioncontrol.blueAdjustBlue.value)
			cmd = "-B '%s %s %s'" % (Red, Green, Blue)
		elif configName.startswith("whitelevel"):
			Red = int(config.plugins.hyperioncontrol.whitelevelRed.value) / 100.0
			Green = int(config.plugins.hyperioncontrol.whitelevelGreen.value) / 100.0
			Blue = int(config.plugins.hyperioncontrol.whitelevelBlue.value) / 100.0
			cmd = "-w '%s %s %s'" % (Red, Green, Blue)
		elif configName.startswith("blacklevel"):
			Red = int(config.plugins.hyperioncontrol.blacklevelRed.value) / 100.0
			Green = int(config.plugins.hyperioncontrol.blacklevelGreen.value) / 100.0
			Blue = int(config.plugins.hyperioncontrol.blacklevelBlue.value) / 100.0
			cmd = "-b '%s %s %s'" % (Red, Green, Blue)
			
		if cmd:
			send_CMD(cmd)

	def menu(self):
		list = []
		list.append((_("import complete config from hyperion.config.json.bak"), "importCompleteConfig"))
		list.append((_("import LED-config from hyperion.config.json.ledimport"), "importLEDConfig"))
		list.append((_("save current config-file as hyperion.config.json.bak"), "saveAsBak"))
		list.append((_("show content of current hyperion.config.json"), "showConfig"))
		self.session.openWithCallback(
			self.menuCallback,
			ChoiceBox, 
			title = _("Hyperion Control - Setup-Options"),
			list = list,
		)

	def menuCallback(self, ret):
		ret = ret and ret[1]
		if ret:
			if ret == "importCompleteConfig":
				message_txt = _("Should import all data from existing 'hyperion.config.json.bak'?\n\nAll setup values will be overwritten with the data from the 'hyperion.config.json.bak'!\n\nThe read values can then be changed via the green button saved in the current 'hyperion.config.json'.")
				self.session.openWithCallback(self.importJsonBak, MessageBox, message_txt, MessageBox.TYPE_YESNO,default=False)
			elif ret == "importLEDConfig":
				if config.plugins.hyperioncontrol.ledBegin.value != "0":
					self.session.open(MessageBox, _("The LED config import is only possible with the option 'LED start: no'!"), MessageBox.TYPE_INFO)
					return
				else:
					self.session.openWithCallback(self.importLEDConfig, MessageBox,_("Should the LED config data import from exist 'hyperion.config.json.ledimport' ?\n\nAll LED values are taken with the data from the 'hyperion.config.json.ledimport' overwritten!\n\nThe read-in values can then be saved via the green button in the current 'hyperion.config.json'."), MessageBox.TYPE_YESNO,default=False)
			elif ret == "saveAsBak":
				config_bakfile_path ="/etc/hyperion/hyperion.config.json.bak"
				message_txt = _("Should the current config file be backed up as 'hyperion.config.json.bak'?")
				if os.path.exists(config_bakfile_path):
					message_txt += _("\n\nThe already existing 'hyperion.config.json.bak' will be overwritten!")
				self.session.openWithCallback(self.saveConfigAsBak, MessageBox, message_txt, MessageBox.TYPE_YESNO,default=False)
			elif ret == "showConfig":
				config_file_path ="/etc/hyperion/hyperion.config.json"
				self.session.open(Console,_("Hyperion config file"),["cat %s" % config_file_path])

	def saveConfigAsBak(self, ret):
		if ret:
			config_file_path ="/etc/hyperion/hyperion.config.json"
			config_bakfile_path ="/etc/hyperion/hyperion.config.json.bak"
			if os.path.exists(config_file_path):
				os.system('cp %s %s' % (config_file_path, config_bakfile_path))
				print "[HyperionControl] configfile saved as .bak"
				self.session.open(MessageBox,_("The current config file was successful saved as '/etc/hyperion/hyperion.config.json.bak'."), MessageBox.TYPE_INFO,timeout=5)
			else:
				self.session.open(MessageBox,_("Backup as .bak failed!\n\nFile '/etc/hyperion/hyperion.config.json' not found!"), MessageBox.TYPE_INFO,timeout=5)
	
	def importLEDConfig(self, ret):
		if not ret:
			return
		try:
			if not self.jsonConfig:
				self.session.open(MessageBox,_("There are no data from '/etc/hyperion/hyperion.config.json'!\n\nAn import is therefore not possible."), MessageBox.TYPE_INFO,timeout=5)
				return
			
			self.jsonConfigImport= ""
			config_file_path ="/etc/hyperion/hyperion.config.json.ledimport"
			if os.path.exists(config_file_path): 
				#json.bak einlesen
				valuesFromConfig = open(config_file_path).read()
				lines = valuesFromConfig.split("\n")
				newlines=[]
				for line in lines:
					cleanline = line.replace("\t","").lstrip()
					if not cleanline.rstrip().startswith("//") and cleanline.strip() != "":
						newlines.append(line)
				valuesFromConfig = "\n".join(newlines)
				print "=== config", valuesFromConfig
				self.jsonConfigImport = json.loads(valuesFromConfig, object_pairs_hook=OrderedDict)
				
				#LED-key aus import json in json übernehmen
				if "leds" in self.jsonConfigImport:
					self.jsonConfig["leds"] = self.jsonConfigImport["leds"]
					#print "=== LED-Config-Import erfolgreich"
					self.session.open(MessageBox,_("The LED Config import was completed successfully.\n\nWhen saving via the green button, the acquired LED information can be saved in the current config."), MessageBox.TYPE_INFO,timeout=10)
				else:
					self.session.open(MessageBox,_("The LED config import failed. No LED config could be found in the import file!"), MessageBox.TYPE_INFO,timeout=5)
				self.jsonConfigImport= ""
			else:
				self.session.open(MessageBox,_("Import failed!\n\nFile '/etc/hyperion/hyperion.config.json.ledimport' not found!"), MessageBox.TYPE_INFO,timeout=5)
				
		except:
			import traceback, sys
			traceback.print_exc()
			exc_type, exc_value, exc_traceback = sys.exc_info()
			error = "\n".join(traceback.format_exception_only(exc_type, exc_value))
			self.session.open(MessageBox,_("Error when importing the LED config!\n\nError:\n%s") % error, MessageBox.TYPE_INFO,timeout=5)
			self.jsonConfigImport= ""

	def info(self):
		current = self["config"].getCurrent()
		configName = self.getConfigName(config.plugins.hyperioncontrol, current[1])
		
		message_txt = ""
		if configName in ("ledBegin", "ledDirection", "hPicDeep", "vPicDeep", "vPicDist", "hPicDist"):
			self.session.open(HyperionControlInfoScreen,configName)
			return
		elif configName in ("saturationGain","saturationLGain"):
			message_txt = _("Saturation describes the relationship between color and gray content. It is expressed in percentages between 0% (gray) and 100% (fully saturated color).")
		elif configName in ("valueGain","luminanceGain"):
			message_txt = _("With the brightness you adjust the brightness of the LED's.")
		elif configName == "luminanceMinimum":
			message_txt = _("With 'Luminance Minimum' you can  regulate the minimum brightness of the LEDs.")
		elif configName.startswith("whitelevel"):
			message_txt = _("Whitelevel\n\nThe led strips channels dont have always the same perceived amount of color, that's why when we see a white image the leds are a bit reddish, greenish or bluish. To correct that behaviour, we need to limit the output or one or two channels so we perceive a perfect white.\n\nChange the 'Red', 'Green', 'Blue' values until your 'led white' fits your 'TV white'.\n\nHINT: Don't adjust the brightness of your leds with this setting!")
		elif configName.startswith("gamma"):
			message_txt = _("Gamma correction\nEach gamma channel must be set so that the 'gray' of the LEDs does not look greenish/reddish/bluish.\nThis should be checked with each test image (calibration via Ok button in the setup option).")
		elif configName.startswith("threshold"):
			message_txt = _("With this setting you delete the color information of the smallest values - so they are interpreted as black. If you, for example, set 'red' to a threshold of 10, all red values below are interpreted as black.")
		elif configName.startswith("temperature"):
			message_txt = _("The 'temperature' changes the perception of all colors, either they are 'warmer' or 'colder'. With certain combinations you can set the Kelvin values for the color temperature as with LED lamps.\n\nExamples:\nDirect sunlight = 6,000K = 255, 255, 255\nCandle light = 1,900K = 255, 147, 41\nHalogen light = 3,200K = 255, 241, 224")
		elif "Adjust" in configName:
			message_txt = _("Color correction\n\nIn this case, each color channel must be adjusted to match the color TV output in order to correct any color casts in the LEDs.\nThis should be checked with the test images (calibration via the Ok button for the respective setup option).")
		elif configName.startswith("blacklevel"):
			message_txt = _("The black level determines how bright the LEDs are in black. This can be checked via the test pattern (calibration via the OK key in the setup option).")
		elif configName.startswith("framegrabber"):
			message_txt = _("The video grabber image size specifies the width and height of the image which is sent to Hyperion and evaluated.\nThe frequency indicates the rhythm at which the pictures are sent (e.g., 10Hz = 10 frames per second).\nA larger image and a higher frequency results in a higher CPU load on the Dreambox.")
		elif configName.startswith("bbd"):
			message_txt = _("With this option, the black border detection can be activated and adjusted. Black frames are ignored (as with some movies) and the image areas after that are used for the color definition of the LEDs.\n\nhint: If the LEDs do not show anything on black border when the black border detection is activated, the threshold value may be too low. If the threshold is set too high, even dark areas of the image in movies can be classified as black borders.")
		elif configName.startswith("webConfig"):
			ipA = self.getCurrentIP()
			ipA = "http://" + ipA + ":%s" % int(config.plugins.hyperioncontrol.webConfigPort.value)
			message_txt = _("Webif\n\nMany settings from the plugin (such as transform, colors and effects) can also be changed in the hyperion web interface via browser access.\n\nCall in the web browser via:\n\n%s") % ipA
		elif configName.startswith("bootseq"):
			message_txt = _("Bootsequence\n\nWith this options you can setup the bootsequence. Youn can set a color or an effect on boot hyperion (with 'off' you can deactivate this function). You can also set the duration of the bootsequence (0 ms = endless).\nOn 'off' hyperion start directly in live mode.")
		elif configName == "deviceType":
			message_txt = _("Device-Type\n\nHere you can select the used device type.\n\nIf you use a device via USB (Adalight, Adalight-APA102, Sedulight, Karatelight, Atmolight), you need additional kernel modules:\napt-get install kernel-module-ch341\napt-get install kernel-module-usbserial")
		elif configName == "configName":
			message_txt = _("Can be chosen freely.")
		elif configName == "outputIP":
			message_txt = _("IP Adress of Wemos ESP or HueBridge.")
		elif configName == "phe_username":
			message_txt = _("Generating your username. Visit developers.meethue.com and follow the Getting Started Guide step bystep.\nOnce you establish your connection with the bridge, you will have a 32 characters uniqueusername.")
		elif configName == "phe_clientkey":
			message_txt = _("Open web interface for developers (API debugging) on the bridge: http: // <IP of the bridge> /debug/clip.html.\nCreate a new user here. Devicetype: myapplication hyperionHue, generateclientkey: true \nThe answer is the trust name and the client key.")
		elif configName == "phe_lightIds":
			message_txt = _("In PhilipsHue App you can see your Lights.\nMake a note of ordering of the Lights next to the lamp icons in Lights section.\nThis is your LightsIDs.")
		elif configName == "phe_groupId":
			message_txt = _("Identify entertainment area. \n / api / <user name from step 1> / groups / <number of entertainment area>")
		elif configName == "phe_switchOffOnBlack":
			message_txt = _("Not all colrs can be displayed by the Philips Hue devices and black will result in abluish, dark color.\nTherefore, you can let Hyperion switch off your lights when the light should be black:")
		elif configName == "baudrate":
			message_txt = _("Baudrate\n\nThe baudrate is preset with a default value for each device type. In rare cases, however, this value can deviate. If no result is visible, the baud rate must be selected differently.\n\nIf no default baudrate is required, this can be freely selected.\nThe baudrate then depends on the set videograbber frequency (FPS) and the number of LEDs used. An LED requires 24 bits + 8 bits for Control. If, for example, we have installed 100 LEDs, you need 32 * 100 bits per second, which is then multiplied by the set frequency.\n\nWith 10 FPS this would be 32 * 100 * 10 = 32,000 bits.\nA baud rate of 32,000 would thus be sufficient to control all LEDs.")
		elif configName == "colorOrder":
			message_txt = _("If the colors are not displayed correctly. Red e.g. Is blue, you can change the color order here.")
		elif configName == "outputTYPE":
			message_txt = _("Output\n\nDepending on the device type used, the appropriate output must be selected.\n\nIf you are not sure, check the description of your device.\n\nIf you don't find any information then you have to find out by trying.")
		elif configName == "smoothingupdateFrequency":
			message_txt = _("Update Frequency\n\nThe setting is used to smooth the LED data in order to reduce the flickering of the LEDs, the higher the value the higher the smoothing.\n\nValues up to 30 Hz are possible for APA102 and LPD8806\n\nWith other LED stripes, this must be tested yourself\n\nProblems can possibly arise if the value is selected too high.")
		
		if message_txt:
			self.session.open(MessageBox, message_txt, MessageBox.TYPE_INFO, windowTitle="Hyperion Control Info")

	def getHostname(self):
		if os.path.exists(eEnv.resolve("${sysconfdir}/hostname")):
			fp = open(eEnv.resolve("${sysconfdir}/hostname"), 'r')
			hostname = fp.readline().replace("\n","")
			fp.close()
			return hostname
		else:
			return "unknown hostname"
	
	def getCurrentIP(self):
		ipA = self.getHostname()
		if ipA != "unknown hostname":
			return ipA
		services = eNetworkManager.getInstance().getServices()
		ipA = _("IP_of_the_box")
		for service in services:
			ip = self.getServiceIP(service)
			name = service.name()
			if ip != None:
				ipA = "%s" % ip
		return ipA

	def getServiceIP(self, service):
		ip = None
		if service.state() == eNetworkManager.STATE_ONLINE:
			ipv4 = service.ipv4()
			ip = ipv4.get("Address", "0.0.0.0")
			if ip == "0.0.0.0":
				ipv6 = self._service.ipv6()
				ip6 = ipv6.get("Address", "::")
				if ip6 != "::":
					ip = ip6
		return ip

	def keyOK(self):
		current = self["config"].getCurrent()
		configName = self.getConfigName(config.plugins.hyperioncontrol, current[1])
		
		if configName.startswith(("gamma","whitelevel","blacklevel","redAdjust","greenAdjust","blueAdjust", "temperature")):
			self.session.open(HyperionControlColorSetup, configName, current[0])
		elif configName in ("bootseqColor", "onIdleColor", "onIdlebackColor"):
			self.session.openWithCallback(boundFunction(self.colorCallback,current[1]), hyperionControlColors, True)
		elif configName in ("bootseqEffect", "onIdleEffect", "onIdlebackEffect"):
			self.session.openWithCallback(boundFunction(self.effectsCallback,current[1]), hyperionControlEffects, True)

	def colorCallback(self, configObj=None, retvalue=False):
		if retvalue and configObj:
			configObj.choices.choices = [(retvalue[1],retvalue[0])]
			configObj.value = str(retvalue[1])

	def effectsCallback(self, configObj=None, retvalue=False):
		if retvalue:
			configObj.choices.choices = [(retvalue,retvalue)]
			configObj.value = str(retvalue)

	def key_red(self):
		config.plugins.hyperioncontrol.save()
		self.close()

	def key_green(self):
		self.saveJson()
		
	def key_yellow(self):
		if self.setupPage == "transform":
			self.setupPage = "device"
			self["key_yellow"].setText(_("Transform"))
		else:
			self.setupPage = "transform"
			self["key_yellow"].setText(_("Device/LED"))
		self.buildConfig()
	
	def key_blue(self):
		self.menu()
	
	def key_exit(self):
		self.saveAll() #save all config-values which don't use NoSave()
		config.plugins.hyperioncontrol.save()
		self.close(self.session, "exit")


class hyperionControlSystem(Screen):
	if sz_w == 1920:
		skin = """
		<screen name="hyperionControlSystem" position="center,200" size="900,800" >
			<ePixmap pixmap="skin_default/buttons/red.png" position="20,720" scale="stretch" size="200,70" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="240,720" size="200,70" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="460,720"  size="200,70" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/blue.png" position="680,720" size="200,70" scale="stretch"/>
			<eLabel font="Regular;30" foregroundColor="white" name="" position="20,720" size="200,70" text="Exit" valign="center" halign="center" backgroundColor="#9f1313" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel font="Regular;30" foregroundColor="white" name="" position="680,720" size="200,70" text="About" valign="center" halign="center" backgroundColor="#18188b" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel name="" position="10,700" size="880,2" backgroundColor="grey" />
			<widget name="list" position="10,10" size="880,680" itemWidth="880" itemHeight="60" enableWrapAround="1" scrollbarMode="showOnDemand" />
		</screen>"""
	else:
		skin = """
		<screen name="hyperionControlSystem" position="center,80" size="590,620" >
			<ePixmap pixmap="skin_default/buttons/red.png" position="5,570" scale="stretch" size="140,40" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="150,570" size="140,40" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="295,570"  size="140,40" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/blue.png" position="440,570" size="140,40" scale="stretch"/>
			<eLabel font="Regular;22" foregroundColor="white" name="" position="5,570" size="140,40" text="Exit" valign="center" halign="center" backgroundColor="#9f1313" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel font="Regular;22" foregroundColor="white" name="" position="440,570" size="140,40" text="About" valign="center" halign="center" backgroundColor="#18188b" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel name="" position="5,560" size="580,2" backgroundColor="grey" />
			<widget name="list" position="10,10" size="575,540" itemWidth="575" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		
		self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'MenuActions','SetupActions'], {
		'cancel': self.key_exit,
		'ok'	: self.key_ok,
		'red'	: self.key_red,
		'green'	: self.key_green,
		'yellow': self.key_yellow,
		'blue'	: self.key_blue,
		'previousSection' : self.pageUp,
		'nextSection' : self.pageDown,
		'left'	: self.pageUp,
		'right'	: self.pageDown,
		})

		self.litems = []
		tlf = TemplatedListFonts()
		self.ml = MenuList(self.litems, mode=eListbox.layoutGrid, content=eListboxPythonMultiContent, margin=ePoint(0,0), selectionZoom=1.3)
		self.ml.l.setFont(0, gFont(tlf.face(tlf.BIG), tlf.size(tlf.BIG)))
		self['list'] = self.ml	
		self.onLayoutFinish.append(self.buildList)
		self.setTitle(_("Hyperion Control - SystemCTL"))

	def buildList(self):
		self.ml.l.setBuildFunc(self.showList, True)
		self.litems = []
		self.litems.append(((_("start hyperionaml"), "start"),))
		self.litems.append(((_("stop hyperionaml"), "stop"),))
		self.litems.append(((_("restart hyperionaml"), "restart"),))
		self.litems.append(((_("status hyperionaml"), "status"),))
		self.litems.append(((_("start hyperion"), "start_1"),))
		self.litems.append(((_("stop hyperion"), "stop_1"),))
		self.litems.append(((_("restart hyperion"), "restart_1"),))
		self.litems.append(((_("status hyperion"), "status_1"),))
		self.litems.append(((_("disable hyperion"), "disable_1"),))
		self.litems.append(((_("enable autostart"), "enable"),))
		self.litems.append(((_("disable autostart"), "disable"),))
		self.litems.append(((_("status autostart"), "status_2"),))
		self["list"].setList(self.litems)

	def showList(self, item, selected):
		res = [item]
		(name, cmd) = item
		if sz_w == 1920:
			res.append(MultiContentEntryText(pos=(0,0), size=(880,60), font=0, text=name, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
		else:
			res.append(MultiContentEntryText(pos=(0,0), size=(575,40), font=0, text=name, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
		return res

	def pageUp(self):
		self["list"].pageUp()

	def pageDown(self):
		self["list"].pageDown()

	def key_red(self):
		self.close()

	def key_green(self):
		pass

	def key_yellow(self):
		pass

	def key_blue(self):
		about(self)

	def key_exit(self):
		self.close(self.session, "exit")

	def key_ok(self):
		exist = self['list'].getCurrent()
		if exist == None:
			return
		(name, returnValue) = self['list'].getCurrent()[0]
		if returnValue == "start":
			self.session.open(Console,_("start hyperionaml"),["%s start hyperionaml" % hyperionremote_sh])
		elif returnValue == "stop":
			self.session.open(Console,_("stop hyperionaml"),["%s stop hyperionaml" % hyperionremote_sh])
		elif returnValue == "restart":
			self.session.open(Console,_("restart hyperionaml"),["%s restart hyperionaml" % hyperionremote_sh])
		elif returnValue == "status":
			self.session.open(Console,_("status hyperionaml"),["%s status hyperionaml" % hyperionremote_sh])
		if returnValue == "start_1":
			self.session.open(Console,_("start hyperion"),["%s start hyperion" % hyperionremote_sh])
		elif returnValue == "stop_1":
			self.session.open(Console,_("stop hyperion"),["%s stop hyperion" % hyperionremote_sh])
		elif returnValue == "restart_1":
			self.session.open(Console,_("restart hyperion"),["%s restart hyperion" % hyperionremote_sh])
		elif returnValue == "status_1":
			self.session.open(Console,_("status hyperion"),["%s status hyperion" % hyperionremote_sh])
		elif returnValue == "disable_1":
			self.session.open(Console,_("disable hyperion"),["%s disable hyperion" % hyperionremote_sh])
		elif returnValue == "enable":
			self.session.open(Console,_("enable systemd-hyperionaml.timer"),["%s enable systemd-hyperionaml.timer" % hyperionremote_sh])
		elif returnValue == "disable":
			self.session.open(Console,_("disable systemd-hyperionaml.timer"),["%s disable systemd-hyperionaml.timer" % hyperionremote_sh])
		elif returnValue == "status_2":
			self.session.open(Console,_("status systemd-hyperionaml.timer"),["%s status systemd-hyperionaml.timer" % hyperionremote_sh])

class hyperionControlEffects(Screen):
	if sz_w == 1920:
		skin = """
		<screen name="hyperionControlEffects" position="center,200" size="900,800" >
			<ePixmap pixmap="skin_default/buttons/red.png" position="20,720" scale="stretch" size="200,70" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="240,720" size="200,70" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="460,720"  size="200,70" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/blue.png" position="680,720" size="200,70" scale="stretch"/>
			<eLabel font="Regular;30" foregroundColor="white" name="" position="20,720" size="200,70" text="Exit" valign="center" halign="center" backgroundColor="#9f1313" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel name="" position="10,700" size="880,2" backgroundColor="grey" />
			<widget name="list" position="10,10" size="880,680" itemWidth="880" itemHeight="60" enableWrapAround="1" scrollbarMode="showOnDemand" />
		</screen>"""
	else:
		skin = """
		<screen name="hyperionControlEffects" position="center,80" size="590,620" >
			<ePixmap pixmap="skin_default/buttons/red.png" position="5,570" scale="stretch" size="140,40" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="150,570" size="140,40" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="295,570"  size="140,40" scale="stretch"/>
			<ePixmap pixmap="skin_default/buttons/blue.png" position="440,570" size="140,40" scale="stretch"/>
			<eLabel font="Regular;22" foregroundColor="white" name="" position="5,570" size="140,40" text="Exit" valign="center" halign="center" backgroundColor="#9f1313" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<eLabel name="" position="5,560" size="580,2" backgroundColor="grey" />
			<widget name="list" position="10,10" size="575,540" itemWidth="575" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" />
		</screen>"""
		
	def __init__(self, session, OnlyReturnEffect=False):
		Screen.__init__(self, session)
		self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'MenuActions', 'SetupActions',], {
		'cancel': self.key_exit,
		'ok'	: self.key_ok,
		'red'	: self.key_red,
		'green'	: self.key_green,
		'yellow': self.key_yellow,
		'blue'	: self.key_blue,
		'previousSection' : self.pageUp,
		'nextSection' : self.pageDown,
		'left'	: self.pageUp,
		'right'	: self.pageDown,
		})
		self.setTitle(_("Hyperion Control - Effects"))
		self.OnlyReturnEffect = OnlyReturnEffect
		
		tlf = TemplatedListFonts()
		self.litems = [('Blue mood blobs',), ('Cinema brighten lights',), ('Cinema dim lights',), ('Cold mood blobs',), ('Color traces',), ('Full color mood blobs',), ('Green mood blobs',), ('Knight rider',), ('Police Lights Single',), ('Police Lights Solid',), ('Rainbow mood',), ('Rainbow swirl',), ('Rainbow swirl fast',), ('Random',), ('Red mood blobs',), ('Running dots',), ('Snake',), ('Sparks',), ('Sparks Color',), ('Strobe Raspbmc',), ('Strobe blue',), ('Strobe white',), ('Warm mood blobs',), ('X-Mas',), ('UDP listener',), ('UDP multicast listener',), ('System Shutdown',)]
		self.ml = MenuList(self.litems, mode=eListbox.layoutGrid, content=eListboxPythonMultiContent, margin=ePoint(0,0), selectionZoom=1.2)
		self.ml.l.setFont(0, gFont(tlf.face(tlf.BIG), tlf.size(tlf.BIG)))
		self['list'] = self.ml

		self.onLayoutFinish.append(self.buildList)

	def buildList(self):
		self.ml.l.setBuildFunc(self.showList, True)
		self["list"].setList(self.litems)

	def showList(self, item, selected):
		res = [item]
		if sz_w == 1920:
			res.append(MultiContentEntryText(pos=(0,0), size=(880,60), font=0, text=item, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
		else:
			res.append(MultiContentEntryText(pos=(0,0), size=(575,40), font=0, text=item, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
		return res

	def pageUp(self):
		self["list"].pageUp()

	def pageDown(self):
		self["list"].pageDown()

	def key_red(self):
		self.close()

	def key_green(self):
		pass
		
	def key_yellow(self):
		pass
		
	def key_blue(self):
		pass

	def key_ok(self):
		exist = self['list'].getCurrent()
		if exist == None:
			return
		effect = self['list'].getCurrent()[0]
		print effect
		if self.OnlyReturnEffect:
			self.close(effect)
			return
		cmd = "--effect '%s'" % effect
		send_CMD(cmd)

	def key_exit(self):
		self.close()


class hyperionStart(Screen):
	if sz_w == 1920:
		skin = """
		<screen name="hyperionStart" position="center,center" size="900,650">
			<eLabel font="Regular;42" foregroundColor="white" name="" position="0,20" size="900,110" text="Hyperion Control" valign="center" halign="center" transparent="1" />
			<widget name="logo" position="70,160" size="270,270" />
			<widget name="status" position="410,160" size="460,270" font="Regular;23" foregroundColor="black" backgroundColor="white" />
			<eLabel name="" position="10,550" size="880,2" backgroundColor="grey" />
			<ePixmap pixmap="skin_default/buttons/red.png" position="10,560" size="210,70" scale="stretch" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="230,560" size="210,70" scale="stretch" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="450,560" size="210,70" scale="stretch" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="670,560" size="210,70" scale="stretch" />
			<widget source="key_red" render="Label" backgroundColor="#9f1313" font="Regular;30" halign="center" position="10,560"  size="210,70" foregroundColor="white" shadowColor="black" shadowOffset="-2,-2" transparent="1" valign="center" zPosition="1" />
			<widget source="key_green" render="Label" backgroundColor="#1f771f" font="Regular;30" halign="center" position="230,560" size="210,70" foregroundColor="white" shadowColor="black" shadowOffset="-2,-2"  transparent="1" valign="center" zPosition="1" />
			<widget source="key_yellow" render="Label" font="Regular;30" foregroundColor="white" position="450,560" size="210,70" valign="center" halign="center" backgroundColor="#a08500" shadowColor="black" shadowOffset="-2,-2" zPosition="1" transparent="1" />
			<widget source="key_blue" render="Label"  font="Regular;30" foregroundColor="white" position="670,560" size="210,70" valign="center" halign="center" zPosition="1" backgroundColor="#18188b" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<widget name="version" font="Regular;30" position="15,500" size="400,40" />
			<ePixmap pixmap="skin_default/buttons/key_menu.png" position="785,490" size="90,45" scale="stretch" />
		</screen>"""
	else:
		skin = """
		<screen name="hyperionStart" position="center,center" size="600,500">
			<eLabel font="Regular;32" foregroundColor="white" name="" position="0,20" size="600,98" text="Hyperion Control" valign="center" halign="center" transparent="1" />
			<widget name="logo" position="30,150" size="200,200" />
			<widget name="status" position="280,150" size="300,200" font="Regular;16" foregroundColor="black" backgroundColor="white" />
			<eLabel name="" position="5,440" size="590,2" backgroundColor="grey" />
			<ePixmap pixmap="skin_default/buttons/red.png" position="5,450" size="145,40" scale="stretch" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="155,450" size="145,40" scale="stretch" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="305,450" size="145,40" scale="stretch" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="455,450" size="145,40" scale="stretch" />
			<widget source="key_red" render="Label" backgroundColor="#9f1313" font="Regular;22" halign="center" position="5,450"  size="145,40" foregroundColor="white" shadowColor="black" shadowOffset="-2,-2" transparent="1" valign="center" zPosition="1" />
			<widget source="key_green" render="Label" position="155,450" size="145,40" zPosition="1" font="Regular;22" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-2,-2"/>
			<widget source="key_yellow" render="Label" font="Regular;22" foregroundColor="white" position="305,450" size="145,40" valign="center" halign="center" backgroundColor="#a08500" shadowColor="black" shadowOffset="-2,-2" zPosition="1" transparent="1" />
			<widget source="key_blue" render="Label" font="Regular;22" foregroundColor="white" position="455,450" size="145,40" valign="center" halign="center" backgroundColor="#18188b" zPosition="1" shadowColor="black" shadowOffset="-2,-2" transparent="1" />
			<widget name="version" font="Regular;22" position="15,400" size="300,25" />
			<ePixmap pixmap="skin_default/buttons/key_menu.png" position="497,395" size="72,36" />
		</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["logo"] = Pixmap()
		self["version"] = Label(_("Version") + " " + hyperioncontrol_version)
		self["status"] = Label(_("state:"))
		self["key_red"] = StaticText(_("Colors"))
		self["key_green"] = StaticText(_("Effects"))
		self["key_yellow"] = StaticText(_("Setup"))
		self["key_blue"] = StaticText(_("Live Mode"))
		
		self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'MenuActions','InfobarEPGActions'], 
		{
			'cancel': self.close,
			'red'	: self.key_red,
			'green'	: self.key_green,
			'yellow': self.key_yellow,
			'blue'	: self.key_blue,
			'menu': self.menu,
			'showEventInfo': self.about,
		})
		
		self.onLayoutFinish.append(self.layoutFinished)
		self.onShown.append(self.refreshStatus)
		self.runfirst = True

	def refreshStatus(self):
		status_txt = "\n  " + _("state:") + "   " + _("CPU") + "  %s\n\n"
		print "[HyperionControl] refresh status"
		
		#hyperion-status
		command = Command("systemctl status hyperion")
		command.run(timeout=3)
		cmd_out= command.out
		if "Active: active" in cmd_out:
			status_txt += "  Hyperion: %s\n" % _("active")
		else:
			status_txt += "  Hyperion: %s\n" % _("inactive")
		
		#hyperionaml-status
		command = Command("systemctl status hyperionaml")
		command.run(timeout=3)
		cmd_out= command.out
		aml_active = False
		if "Active: active" in cmd_out:
			status_txt += "  Hyperionaml: %s\n" % _("active")
			aml_active = True
		else:
			status_txt += "  Hyperionaml: %s\n" % _("inactive")
		
		#get fps and size from framegrabber
		fg_fps = "10"
		fg_size_w = "160"
		fg_size_h = "160"
		pos1 = cmd_out.find("hyperion-aml -f ")
		if pos1>0:
			pos2 = cmd_out.find("\n",pos1 + 5)
			if pos2>0:
				row_txt_list = cmd_out[pos1:pos2].split(" ")
				if len(row_txt_list) > 1 and row_txt_list[1]== "-f":
					fg_fps =  row_txt_list[2]
				if len(row_txt_list) > 3 and row_txt_list[3]== "--width" :
					fg_size_w =  row_txt_list[4]
				if len(row_txt_list) > 5 and row_txt_list[5]== "--height":
					fg_size_h =  row_txt_list[6]
		
		fg_size = "%sx%s" % (fg_size_w, fg_size_h)
		
		#systemd-hyperionaml.timer
		command = Command("systemctl status systemd-hyperionaml.timer")
		command.run(timeout=3)
		cmd_out= command.out
		if "enabled;" in cmd_out:
			status_txt += "  Autostart: %s\n\n" % _("active")
		else:
			status_txt += "  Autostart: %s\n\n" % _("inactive")
		
		#Modus
		self.jsonRemote = readValuesFromRemote(self, self.runfirst, False)
		self.runfirst=False
		if self.jsonRemote:
			if self.jsonRemote["activeEffects"] != []:
				status_txt += "  " + _("Mode: ") + _("Effects") + "\n\n"
			elif self.jsonRemote["activeLedColor"] != []:
				status_txt += "  " + _("Mode: ") + _("Colors") + "\n\n"
			else:
				status_txt += "  " + _("Mode: ") + _("Live Mode") + " " + _("or") + " " + _("Image Mode") + "\n\n"
		
		if aml_active:
			status_txt += "  " + _("Framegrabber") + ": " + fg_size + " " + _("FPS") +" " + fg_fps + "\n"
		
		#use for CPU-usage
		self.lastTotal = 0
		self.lastIdle = 0
		cpu_value = self.getCPU()
		self.status_txt = status_txt
		self["status"].setText(self.status_txt % cpu_value)
		
		#CPU-refresh-Timer
		self.cpuTimer = eTimer()
		self.cpuTimer_conn = self.cpuTimer.timeout.connect(self.refreshCPU)
		self.cpuTimer.start(1000)
	
	def refreshCPU(self):
		try:
			cpu_value = self.getCPU()
			self["status"].setText(self.status_txt % cpu_value)
		except:
			import traceback, sys
			traceback.print_exc()
	
	def getCPU(self):
		try:
			if os.path.isfile("/proc/stat"):
				fields = [float(column) for column in os.popen("cat /proc/stat").readline().strip().split()[1:]]
				idle, total = fields[3], fields[0]+fields[1]+fields[2]+fields[3]
				idle_delta, total_delta = idle - self.lastIdle, total - self.lastTotal
				self.lastIdle, self.lastTotal = idle, total
				utilisation = 100.0 * (1.0 - idle_delta / total_delta)
				return format(round(utilisation,2),"0.1f") + "%"
			else:
				return "No info"
		
		except:
			import traceback, sys
			traceback.print_exc()
			return "No info"
	
	def layoutFinished(self):
		self["logo"].instance.setPixmapFromFile("/usr/lib/enigma2/python/Plugins/Extensions/HyperionControl/hyperion_logo.png")
		self.setTitle(_("Hyperion Control"))

	def about(self):
		about(self)

	def key_red(self):
		self.session.open(hyperionControlColors)

	def key_green(self):
		self.session.open(hyperionControlEffects)
		
	def key_yellow(self):
		self.session.open(hyperionControlSetup)

	def key_blue(self):
		if self["key_blue"].getText():
			send_CMD('--clearall')
			self.session.open(MessageBox,_("The Live Mode has been activated."), MessageBox.TYPE_INFO,timeout=5)
	
	def menu(self):
		self.session.open(hyperionControlSystem)

class HyperionControlPictureBrowser(Screen):
	if sz_w == 1920:
		skin = """
		<screen name="HyperionControlPictureBrowser" position="center,170" size="1500,740" title="Hyperion Control Picture Browser">
			<ePixmap pixmap="Default-FHD/skin_default/buttons/red.svg" position="10,5" size="300,70" />
			<ePixmap pixmap="Default-FHD/skin_default/buttons/green.svg" position="310,5" size="300,70" />
			<widget backgroundColor="#9f1313" font="Regular;30" halign="center" position="10,5" render="Label" foregroundColor="white" shadowColor="black" shadowOffset="-2,-2" size="300,70" source="key_red" transparent="1" valign="center" zPosition="1" />
			<widget backgroundColor="#1f771f" font="Regular;30" halign="center" position="310,5" render="Label" foregroundColor="white" shadowColor="black" shadowOffset="-2,-2" size="300,70" source="key_green" transparent="1" valign="center" zPosition="1" />
			<eLabel backgroundColor="grey" position="10,80" size="900,1" />
			<eLabel backgroundColor="grey" position="920,5" size="1,725" />
			<widget name="picpreview" position="960,90" size="500,500" />
			<widget enableWrapAround="1" name="filelist" position="10,90" scrollbarMode="showOnDemand" size="900,630" />
		</screen>"""
	else:
		skin = """
		<screen name="HyperionControlPictureBrowser" position="center,120" size="920,430" title="Hyperion Control Picture Browser">
			<ePixmap pixmap="skin_default/buttons/red.png" position="10,5" size="200,40"/>
			<ePixmap pixmap="skin_default/buttons/green.png" position="210,5" size="200,40"/>
			<widget source="key_red" render="Label" position="10,5" size="200,40" zPosition="1" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-2,-2"/>
			<widget source="key_green" render="Label" position="210,5" size="200,40" zPosition="1" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-2,-2"/>
			<eLabel position="10,50" size="590,1" backgroundColor="grey"/>
			<eLabel position="610,5" size="1,420" backgroundColor="grey"/>
			<widget name="picpreview" position="620,80" size="290,290" />
			<widget name="filelist" position="10,60" size="590,360" enableWrapAround="1" scrollbarMode="showOnDemand"/>
		</screen>"""

	def __init__(self, session, current_path=None):
		Screen.__init__(self, session)
		if current_path:
			currDir = current_path
			if not os.path.exists(currDir):
				currDir = "/"
		else:
			currDir = None #start with mountpoints-list

		self.filelist = FileList(currDir, matchingPattern="(?i)^.*\.(jpg|png)")
		self["filelist"] = self.filelist
		self["picpreview"] = Pixmap()
		self["filelist"].onSelectionChanged.append(self.selectionChanged)
		
		self["FilelistActions"] = ActionMap(["SetupActions"],
			{
				"save": self.ok,
				"ok": self.ok,
				"cancel": self.exit
			})
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		
		self.ThumbTimer = eTimer()
		self.ThumbTimer_conn = self.ThumbTimer.timeout.connect(self.showThumb)
		
		self.onShown.append(self.setWindowTitle)

	def setWindowTitle(self):
		self.setTitle(_("Hyperion Control Picture Browser"))

	def ok(self):
		if self["filelist"].canDescent(): # isDir
			self["filelist"].descent()
		else:
			file_name = self["filelist"].getFilename()
			path = self["filelist"].getCurrentDirectory()
			self.exit(path + file_name)

	def showThumb(self):
		if not self["filelist"].canDescent():
			file_name = self["filelist"].getFilename()
			path = self["filelist"].getCurrentDirectory()
			#print "== picname", path + file_name
			self["picpreview"].instance.setPixmapFromFile(path + file_name)
			self["picpreview"].show()

	def selectionChanged(self):
		if self["picpreview"] is None:
			return
		
		if not self["filelist"].canDescent():
			self.ThumbTimer.start(400, True)
		else:
			self["picpreview"].hide()

	def exit(self, retvalue=None):
		self.ThumbTimer.stop()
		self.ThumbTimer_conn = None
		if self.filelist.getCurrentDirectory() is None:
			config.plugins.hyperioncontrol.lastpicpath.value = "/"
		else:
			config.plugins.hyperioncontrol.lastpicpath.value = self["filelist"].getCurrentDirectory()
		config.plugins.hyperioncontrol.save()
		
		self["picpreview"] = None
		self.close(retvalue)

class HyperionControlInfoScreen(Screen):
	
	IS_DIALOG = True
	
	if sz_w == 1920:
		skin = """
		<screen name="HyperionControlInfoScreen" position="center,150" size="1400,840">
			<widget name="infopicture" position="50,50" size="1300,740"/>
			<widget name="infotext" position="50,50" size="800,300"/>
		</screen>"""
	else:
		skin = """
		<screen name="HyperionControlInfoScreen" position="center,120" size="920,530">
			<widget name="infopicture" position="20,20" size="880,500"/>
			<widget name="infotext" position="50,50" size="800,300"/>
		</screen>"""

	def __init__(self, session, info_txt=""):
		Screen.__init__(self, session)
		
		self["infopicture"] = Pixmap()
		self["infotext"] = Label()
		self.info_txt = info_txt
		
		self["infopicture"].hide()
		self["infotext"].hide()
		
		self["FilelistActions"] = ActionMap(["SetupActions"],
			{
				"ok": self.ok,
				"cancel": self.exit
			})
		
		self.onShown.append(self.setWindowTitle)

	def setWindowTitle(self):
		self.setTitle(_("Hyperion Control Info"))
		
		path = "/usr/lib/enigma2/python/Plugins/Extensions/HyperionControl/pictures/"
		if self.info_txt in ("hPicDeep", "vPicDeep"):
			filename = "image_area_depth_de.jpg"
		
		elif self.info_txt in ("ledBegin", "ledDirection"):
			filename = "image_area_begin_de.jpg"
		
		elif self.info_txt in ("vPicDist", "hPicDist"):
			filename = "image_area_distance_de.jpg"
		
		self["infopicture"].instance.setPixmapFromFile(path + filename)
		self["infopicture"].show()
		

	def ok(self):
		self.close()

	def exit(self):
		self.close()


class HyperionControlColorSetup(Screen, ConfigListScreen):
	
	if sz_w == 1920:
		skin = """
		<screen transparent="0" position="0,0" size="1920,1080" backgroundColor="#00FFFFFF" flags="wfNoBorder">
			<widget name="config" seperation="100" foregroundColor="#000000" backgroundColor="#FFFFFF" transparent="0" backgroundColorSelected="#004176b6" position="center,center" size="450,200" enableWrapAround="1" scrollbarMode="showOnDemand" />
			<widget name="pixmap" position="0,0" size="1920,1080" zPosition="-1" />
			<widget name="infotext" position="center,800" size="1920,100" font="Regular;30" foregroundColor="#000000" halign="center" transparent="1" />
		</screen>"""
	else:
		skin = """
		<screen position="0,0" size=" 1280,720" backgroundColor="#00FFFFFF" flags="wfNoBorder">
			<widget name="config" seperation="100" foregroundColor="#000000" backgroundColor="#FFFFFF" transparent="0" backgroundColorSelected="#004176b6" position="center,center" size="300,130" enableWrapAround="1" scrollbarMode="showOnDemand" />
			<widget name="pixmap" position="0,0" size="1280,720" zPosition="-1" />
			<widget name="infotext" position="center,550" size="1280,100" font="Regular;22" foregroundColor="#000000" halign="center" transparent="1" />
		</screen>"""

	def __init__(self, session, configName="", configText=""):
		Screen.__init__(self, session)
		
		self.configName = configName
		self.configText = configText
		
		#disable osd_alpha (GUI Transparenz)
		self.osd = config.av.osd_alpha.value
		config.av.osd_alpha.value = 255
		self["pixmap"] = Pixmap()
		self["pixmap"].hide()
		self["infotext"] = Label(_("change backgroundcolor with 'ok' key and close with 'exit' key"))
		
		self.list = []
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changed)
		self["config"] = ConfigListHC(self.list, session = session)
		self.buildConfig()
		
		self["FilelistActions"] = ActionMap(["SetupActions","ColorActions"],
			{
				"ok":     self.keyOK,
				"cancel": self.exit,
			})
		
		if self.configName.startswith("whitelevel"):
			title = _("whitelevel")
			self["infotext"].setText(_("close with 'exit' key"))
		elif self.configName.startswith("blacklevel"):
			title = _("blacklevel")
			self["infotext"].setText(_("close with 'exit' key"))
		elif self.configName.startswith("redAdjust"):
			title = _("redAdjust")
		elif self.configName.startswith("greenAdjust"):
			title = _("greenAdjust")
		elif self.configName.startswith("blueAdjust"):
			title = _("blueAdjust")
		elif self.configName.startswith("gamma"):
			title = _("gamma")
		elif self.configName.startswith("temperature"):
			title = _("temperature")
		self.setTitle(title)
		
		self.onShown.append(self.setWindowTitle)

	def setWindowTitle(self):
		self.ColorIndex = 0
		if self.configName.startswith("whitelevel"):
			self.Colors = ("#FFFFFF",)
		if self.configName.startswith("blacklevel"):
			self.Colors = ("#000000",)
			self["infotext"].instance.setForegroundColor (parseColor("#FFFFFF"))
		elif self.configName.startswith("redAdjust"):
			self.Colors = ("#FF0000", "#FF00FF", "#FFFF00")
		elif self.configName.startswith("greenAdjust"):
			self.Colors = ("#00FF00", "#00FFFF", "#FFFF00")
		elif self.configName.startswith("blueAdjust"):
			self.Colors = ("#0000FF", "#00FFFF", "#FF00FF")
		elif self.configName.startswith("temperatureRed"):
			self.Colors = ("#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#00FFFF", "#FF00FF", "#FFFF00")
		elif self.configName.startswith("temperatureGreen"):
			self.Colors = ("#FFFFFF", "#00FF00", "#FF0000", "#0000FF", "#00FFFF", "#FF00FF", "#FFFF00")
		elif self.configName.startswith("temperatureBlue"):
			self.Colors = ("#FFFFFF", "#0000FF", "#FF0000", "#00FF00", "#00FFFF", "#FF00FF", "#FFFF00")
		elif self.configName.startswith("gamma"):
			self.Colors = ("#3F3F3F", "#7F7F7F", "#BFBFBF", "#000000")
		
		color = self.Colors[self.ColorIndex]
		self.instance.setBackgroundColor(parseColor(color))
		self["infotext"].instance.setBackgroundColor (parseColor(color))
		self["config"].instance.setBackgroundColor(parseColor("#7F7F7F"))
		
		cmd = "-c '%s'" % color
		send_CMD(cmd)
		
		#set selected config from setup-screen
		index = 0
		for configentry in self.list:
			if configentry[0] == self.configText:
				break
			index += 1
		self["config"].setCurrentIndex(index)
		

	def buildConfig(self):
		
		self.list = []
		if self.configName.startswith("whitelevel"):
			self.list.append(getConfigListEntry(_("Whitelevel (0-100, default=100)"), )) 
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.whitelevelRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.whitelevelGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.whitelevelBlue)) )
		elif self.configName.startswith("blacklevel"):
			self.list.append(getConfigListEntry(_("Blacklevel (0-50, default=0)"), )) 
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.blacklevelRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.blacklevelGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.blacklevelBlue)) )
		elif self.configName.startswith("temperature"):
			self.list.append(getConfigListEntry(_("temperature"), )) 
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.temperatureRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.temperatureGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.temperatureBlue)) )
		elif self.configName.startswith("redAdjust"):
			self.list.append(getConfigListEntry(_("Red Adjust (0-255, default=255, 0, 0)"), ))
			self.list.append(getConfigListEntry(_("red (fix)"), NoSave(config.plugins.hyperioncontrol.redAdjustRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.redAdjustGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.redAdjustBlue)) )
		elif self.configName.startswith("greenAdjust"):
			self.list.append(getConfigListEntry(_("Green Adjust (0-255, default=0, 255, 0)"), ))
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.greenAdjustRed)) )
			self.list.append(getConfigListEntry(_("green (fix)"), NoSave(config.plugins.hyperioncontrol.greenAdjustGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.greenAdjustBlue)) )
		elif self.configName.startswith("blueAdjust"):
			self.list.append(getConfigListEntry(_("Blue Adjust (0-255, default=0, 0, 255)"), ))
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.blueAdjustRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.blueAdjustGreen)) )
			self.list.append(getConfigListEntry(_("blue (fix)"), NoSave(config.plugins.hyperioncontrol.blueAdjustBlue)) )
		elif self.configName.startswith("gamma"):
			self.list.append(getConfigListEntry(_("Gamma (0-500, default=250)"), )) 
			self.list.append(getConfigListEntry(_("red"), NoSave(config.plugins.hyperioncontrol.gammaRed)) )
			self.list.append(getConfigListEntry(_("green"), NoSave(config.plugins.hyperioncontrol.gammaGreen)) )
			self.list.append(getConfigListEntry(_("blue"), NoSave(config.plugins.hyperioncontrol.gammaBlue)) )
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def changed(self):
		current = self["config"].getCurrent()
		print "[HyperionControl] - change:", self.configName
		
		cmd = ""
		if self.configName.startswith("whitelevel"):
			Red = int(config.plugins.hyperioncontrol.whitelevelRed.value) / 100.0
			Green = int(config.plugins.hyperioncontrol.whitelevelGreen.value) / 100.0
			Blue = int(config.plugins.hyperioncontrol.whitelevelBlue.value) / 100.0
			cmd = "-w '%s %s %s'" % (Red, Green, Blue)
		elif self.configName.startswith("temperature"):
			Red = int(config.plugins.hyperioncontrol.temperatureRed.value)
			Green = int(config.plugins.hyperioncontrol.temperatureGreen.value)
			Blue = int(config.plugins.hyperioncontrol.temperatureBlue.value)
			cmd = "-Z '%s %s %s'" % (Red, Green, Blue)
		elif self.configName.startswith("redAdjust"):
			Red = int(config.plugins.hyperioncontrol.redAdjustRed.value)
			Green = int(config.plugins.hyperioncontrol.redAdjustGreen.value)
			Blue = int(config.plugins.hyperioncontrol.redAdjustBlue.value)
			cmd = "-R '%s %s %s'" % (Red, Green, Blue)
		elif self.configName.startswith("greenAdjust"):
			Red = int(config.plugins.hyperioncontrol.greenAdjustRed.value)
			Green = int(config.plugins.hyperioncontrol.greenAdjustGreen.value)
			Blue = int(config.plugins.hyperioncontrol.greenAdjustBlue.value)
			cmd = "-G '%s %s %s'" % (Red, Green, Blue)
		elif self.configName.startswith("blueAdjust"):
			Red = int(config.plugins.hyperioncontrol.blueAdjustRed.value)
			Green = int(config.plugins.hyperioncontrol.blueAdjustGreen.value)
			Blue = int(config.plugins.hyperioncontrol.blueAdjustBlue.value)
			cmd = "-B '%s %s %s'" % (Red, Green, Blue)
		elif self.configName.startswith("gamma"):
			Red = int(config.plugins.hyperioncontrol.gammaRed.value) / 100.0
			Green = int(config.plugins.hyperioncontrol.gammaGreen.value) / 100.0
			Blue = int(config.plugins.hyperioncontrol.gammaBlue.value) / 100.0
			cmd = "-g '%s %s %s'" % (Red, Green, Blue)
		elif self.configName.startswith("blacklevel"):
			Red = int(config.plugins.hyperioncontrol.blacklevelRed.value) / 100.0
			Green = int(config.plugins.hyperioncontrol.blacklevelGreen.value) / 100.0
			Blue = int(config.plugins.hyperioncontrol.blacklevelBlue.value) / 100.0
			cmd = "-b '%s %s %s'" % (Red, Green, Blue)
		
		if cmd:
			send_CMD(cmd)
	
	def keyOK(self):
		#switch colors for gamma-settings
		if self.configName.startswith(("gamma", "redAdjust", "greenAdjust", "blueAdjust","temperature")):
			self.ColorIndex += 1
			if not self.configName.startswith("temperature") and self.ColorIndex in (4,5):
				if self.ColorIndex == 4: direction = ePixmap.GRADIENT_HORIZONTAL
				if self.ColorIndex == 5: direction = ePixmap.GRADIENT_VERTICAL
				color  = "#000000"
				color1 = "#000000"
				color2 = "#FFFFFF"
			elif not self.configName.startswith("temperature") and self.ColorIndex in (6,7):
				if self.ColorIndex == 6: direction = ePixmap.GRADIENT_HORIZONTAL
				if self.ColorIndex == 7: direction = ePixmap.GRADIENT_VERTICAL
				color  = "#000000"
				color2 = "#000000"
				color1 = "#FFFFFF"
			
			if self.configName.startswith("temperature"):
				if self.ColorIndex > 6: self.ColorIndex = 0
			elif not self.configName.startswith("gamma"):
				if self.ColorIndex > 2: self.ColorIndex = 0
			elif self.ColorIndex > 7:
				self.ColorIndex = 0
			
			if self.configName.startswith("temperature"):
				color = self.Colors[self.ColorIndex]
				self.instance.setBackgroundColor(parseColor(color))
				self["infotext"].instance.setBackgroundColor (parseColor(color))
				cmd = "-c '%s'" % color
				send_CMD(cmd)
			
			#if first 4 normal colors
			elif self.ColorIndex < 4:
				self["pixmap"].hide()
				color = self.Colors[self.ColorIndex]
				if color in ("#FF000000","#000000"):
					self["infotext"].instance.setForegroundColor(parseColor("#FFFFFF"))
				else:
					self["infotext"].instance.setForegroundColor(parseColor("#000000"))
				self.instance.setBackgroundColor(parseColor(color))
				self["infotext"].instance.setBackgroundColor (parseColor(color))
				cmd = "-c '%s'" % color
				send_CMD(cmd)
			
			#if 4 gradient pixmap colors
			else:
				self.instance.setBackgroundColor(parseColor(color))
				self["infotext"].instance.setBackgroundColor (parseColor(color))
				self["pixmap"].instance.setGradient(parseColor(color1), parseColor(color2), direction)
				self["pixmap"].show()
				self["infotext"].hide()
				self["config"].hide()
				
				self.container = eConsoleAppContainer()
				width = int(str(config.plugins.hyperioncontrol.framegrabberSize.value).split(",")[0])
				height = int(str(config.plugins.hyperioncontrol.framegrabberSize.value).split(",")[1])
				cmd = 'dreamboxctl screenshot -f /tmp/HyperionOSD.jpg -iw %s -ih %s && hyperion-remote -i /tmp/HyperionOSD.jpg' % (width, height)
				self.container_appClosed_conn = self.container.appClosed.connect(self.eConsoleFinished)
				self.container.execute(cmd)
			self.instance.invalidate()

	def eConsoleFinished(self, status):
		self["infotext"].show()
		self["config"].show()
		
	def exit(self):
		#reenable osd_alpha (GUI Transparenz)
		config.av.osd_alpha.value = self.osd
		self.close()


def about(self):
		title="HyperionControl version %s \nplugin by\neinfall, pclin & Sven_H" % hyperioncontrol_version
		self.session.open(MessageBox,("%s") % (title),  MessageBox.TYPE_INFO)

def send_CMD(cmd):
	raw = "hyperion-remote %s" % cmd
	print "[HyperionControl] SEND CMD TO Hyperion Remote: %s" % raw
	os.system(raw)

def setConfigValueFromJson(config, jsonData, jsonKey, calculate=None, onlyReturnValue=False, default=None):
	try:
		for item in jsonKey:
			jsonData = jsonData[item]
		if calculate:
			jsonData = int(jsonData * calculate)
		if onlyReturnValue:
			print "[HyperionControl] return value", item, jsonData
			return jsonData
		else:
			config.value = str(jsonData)
			print "[HyperionControl] set value to", item, str(jsonData)
	except (KeyError, TypeError, IndexError):
		if onlyReturnValue:
			#print "[HyperionControl] error on item - return default", item, config.default
			if default:
				return default
			else:
				return config.default
		else:
			config.value = config.default
			#print "[HyperionControl] error on item - set default", item, config.default

def readValuesFromRemote(self, showMessage=True, setConfig=True):
	print "[HyperionControl] readValuesFromRemote"
	try:
		command = Command("hyperion-remote -l")
		command.run(timeout=5)
		
		#read real settings from hyperion-remote -l
		if command.timeout:
			print "[HyperionControl] timeout on readValuesFromRemote"
			if showMessage:
				self.session.open(MessageBox,_("Timeout on load remote-Data!\n\n"), MessageBox.TYPE_INFO,timeout=5)
			return None
		elif command.process.returncode != 0:
			print "[HyperionControl] error on readValuesFromRemote:", str(command.process.returncode), str(command.err)
			if showMessage:
				self.session.open(MessageBox,_("Error on load remote-Data!\n\nError:\n%s") % str(command.err), MessageBox.TYPE_INFO,timeout=5)
			return None
		
		valuesFromRemote = command.out
		
		pos = valuesFromRemote.find("Server info:")
		if pos:
			valuesFromRemote = valuesFromRemote[pos+12:]
			jsonRemote = json.loads(valuesFromRemote)
			if setConfig:
				setConfigValueFromJson(config.plugins.hyperioncontrol.saturationGain, jsonRemote, ['transform',0,'saturationGain'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.valueGain, jsonRemote, ['transform',0,'valueGain'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.saturationLGain, jsonRemote, ['transform',0,'saturationLGain'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.luminanceGain, jsonRemote, ['transform',0,'luminanceGain'],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.luminanceMinimum, jsonRemote, ['transform',0,'luminanceMinimum'],100)
				
				setConfigValueFromJson(config.plugins.hyperioncontrol.gammaRed, jsonRemote, ['transform',0,'gamma',0],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.gammaGreen, jsonRemote, ['transform',0,'gamma',1],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.gammaBlue, jsonRemote, ['transform',0,'gamma',2],100)
				
				setConfigValueFromJson(config.plugins.hyperioncontrol.thresholdRed, jsonRemote, ['transform',0,'threshold',0],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.thresholdGreen, jsonRemote, ['transform',0,'threshold',1],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.thresholdBlue, jsonRemote, ['transform',0,'threshold',2],100)
				
				setConfigValueFromJson(config.plugins.hyperioncontrol.redAdjustRed, jsonRemote, ['adjustment',0,'redAdjust',0])
				setConfigValueFromJson(config.plugins.hyperioncontrol.redAdjustGreen, jsonRemote, ['adjustment',0,'redAdjust',1])
				setConfigValueFromJson(config.plugins.hyperioncontrol.redAdjustBlue, jsonRemote, ['adjustment',0,'redAdjust',2])
				setConfigValueFromJson(config.plugins.hyperioncontrol.greenAdjustRed, jsonRemote, ['adjustment',0,'greenAdjust',0])
				setConfigValueFromJson(config.plugins.hyperioncontrol.greenAdjustGreen, jsonRemote, ['adjustment',0,'greenAdjust',1])
				setConfigValueFromJson(config.plugins.hyperioncontrol.greenAdjustBlue, jsonRemote, ['adjustment',0,'greenAdjust',2])
				setConfigValueFromJson(config.plugins.hyperioncontrol.blueAdjustRed, jsonRemote, ['adjustment',0,'blueAdjust',0])
				setConfigValueFromJson(config.plugins.hyperioncontrol.blueAdjustGreen, jsonRemote, ['adjustment',0,'blueAdjust',1])
				setConfigValueFromJson(config.plugins.hyperioncontrol.blueAdjustBlue, jsonRemote, ['adjustment',0,'blueAdjust',2])
				setConfigValueFromJson(config.plugins.hyperioncontrol.temperatureRed, jsonRemote, ['temperature',0,'correctionValues',0])
				setConfigValueFromJson(config.plugins.hyperioncontrol.temperatureGreen, jsonRemote, ['temperature',0,'correctionValues',1])
				setConfigValueFromJson(config.plugins.hyperioncontrol.temperatureBlue, jsonRemote, ['temperature',0,'correctionValues',2])
				
				setConfigValueFromJson(config.plugins.hyperioncontrol.blacklevelRed, jsonRemote, ['transform',0,'blacklevel',0],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.blacklevelGreen, jsonRemote, ['transform',0,'blacklevel',1],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.blacklevelBlue, jsonRemote, ['transform',0,'blacklevel',2],100)
				
				setConfigValueFromJson(config.plugins.hyperioncontrol.whitelevelRed, jsonRemote, ['transform',0,'whitelevel',0],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.whitelevelGreen, jsonRemote, ['transform',0,'whitelevel',1],100)
				setConfigValueFromJson(config.plugins.hyperioncontrol.whitelevelBlue, jsonRemote, ['transform',0,'whitelevel',2],100)
			
			return jsonRemote

	except:
		import traceback, sys
		traceback.print_exc()
		exc_type, exc_value, exc_traceback = sys.exc_info()
		if showMessage:
			error = "\n".join(traceback.format_exception_only(exc_type, exc_value))
			self.session.open(MessageBox,_("Error on load remote-Data!\n\nError:\n%s") % error, MessageBox.TYPE_INFO,timeout=10)
		return None

