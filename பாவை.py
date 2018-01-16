#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# பாவை
# தமிழ் பாக்களை இயற்றுவதற்கு உதவுகிறது
#
# காப்புரிமை 2018, ஶ்ரீரமண ஶர்மா
# Copyright 2018, Shriramana Sharma
#
# பயனர் உரிமம்/User license: GNU GPL v3+
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


கடவுள்_வாழ்த்து = """\
வாக்குண்டாம் நல்ல மனமுண்டாம் மாமலராள்
நோக்குண்டாம் மேனி நுடங்காது - பூக்கொண்டு
துப்பார் திருமேனி தும்பிக்கை யான்பாதம்
தப்பாமல் சார்வார் தமக்கு.

பாலும் தெளிதேனும் பாகும் பருப்புமிவை
நாலும் கலந்துனக்கு நான்தருவேன் - கோலம்செய்
துங்கக் கரிமுகத்து தூமணியே நீஎனக்கு
சங்கத் தமிழ்மூன்றும் தா.

ஆழிமழைக் கண்ணா ஒன்றுநீ கைகரவேல்
ஆழியுள் புக்கு முகந்துகொடு ஆர்த்தேறி
ஊழி முதல்வன் உருவம்போல் மெய்கறுத்துப்
பாழியம் தோளுடையப் பற்பனாபன் கையில்
ஆழிபோல் மின்னி வலம்புரிபோல் நின்றதிர்ந்து
தாழாதே சார்ங்க முதைத்த சரமழைபோல்
வாழ உலகினில் பெய்திடாய் நாங்களும்
மார்கழி நீராட மகிழ்ந்தேலோர் எம்பாவாய்

முன்னிக் கடலைச் சுருக்கி எழுந்துடையான்
என்னத் திகழ்ந்தெம்மை ஆளுடையான் இட்டிடையின்
மின்னப் பொலிந்தெம் பிராட்டி திருவடிமேல்
பொன்னஞ் சிலம்பில் சிலம்பித் திருப்புருவம்
என்னச் சிலைகுலவி நந்தம்மை ஆளுடையாள்
தன்னிற் பரிவிலா எங்கோமான் அன்பர்க்கு
முன்னி யவன்நமக்கு முன்சுரக்கும் இன்னருளே
என்னப் பொழியாய் மழையேலோர் எம்பாவாய்.
"""


from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QSyntaxHighlighter
from PyQt5.QtWidgets import *

from யாப்பு import *
from பாவை_உதவி import *


முந்தைய_உள்ளீடு = None
ஏற்புடைய_தளைகள் = set()
தளைகளின்_சுருக்கமான_பெயர்கள் = dict(zip(தளைகள், ("இ வெ", "வெ வெ", "நே ஆ", "நி ஆ", "க", "ஒய வ", "ஒறா வ")))
சீரின்_முழு_வாய்ப்பாடு_காட்டவும் = False


def ஆய்வுகளை_உருவாக்கு(உள்ளீடு):

    global முந்தைய_உள்ளீடு
    if உள்ளீடு == முந்தைய_உள்ளீடு:
        return None
    if not உள்ளீடு.endswith("\n"):
        உள்ளீடு += "\n"
    முந்தைய_உள்ளீடு = உள்ளீடு

    global அலகிடப்பட்ட_பாக்கள், அடி_முழு_ஆய்வு, அடி_சுருக்க_ஆய்வு
    அலகிடப்பட்ட_பாக்கள் = பாக்கள்(உள்ளீடு)
    அடி_முழு_ஆய்வு = None
    அடி_சுருக்க_ஆய்வு = None
    அடி_ஆய்வு_உருவாக்கு()
    பா_மொத்த_ஆய்வு_உருவாக்கு()


தளைப்பெயர்_இல்லை = "?தளை?"
காசு_பிறப்பு_தேர்வு = {"தே·மா": "கா·சு", "புளி·மா": "பிறப்·பு"}
ஈற்றசைப்பெயர்_இல்லை = "?ஈற்றசை?"


def அடி_ஆய்வு_உருவாக்கு():
    
    global அடி_முழு_ஆய்வு, அடி_சுருக்க_ஆய்வு
    if சீரின்_முழு_வாய்ப்பாடு_காட்டவும்:
        if அடி_முழு_ஆய்வு:  # ஏற்கெனவே உள்ளது
            return
    else:
        if அடி_சுருக்க_ஆய்வு:  # ஏற்கெனவே உள்ளது
            return

    அடி_ஆய்வு = []
    for பா in அலகிடப்பட்ட_பாக்கள்:
        if not பா:  # தமிழ் இல்லாத வரியாக இருக்கும்
            அடி_ஆய்வு.append("")
            continue
        for அடி in பா:
            அடி_ஆய்வு_வரி = [அடி.நீளப்பெயர், ":"]
            சேர்க்க = அடி_ஆய்வு_வரி.append
            பா_முதற்சீர் = பா[0][0]
            பா_இறுதிச்சீர் = பா[-1][-1]
            for சீர் in அடி:
                if not சீர்:  # தவறாக உள்ளிடப்பட்ட தமிழெழுத்துக்கள் (உயிர்க்குறிகள் முதலிய) வெற்றுச்சீராக கொள்ளப்படலாம்
                    continue
                if சீரின்_முழு_வாய்ப்பாடு_காட்டவும்:
                    if சீர்.வாய்ப்பாடு:
                        if சீர் is பா_இறுதிச்சீர் and சீர்.வாய்ப்பாடு in காசு_பிறப்பு_தேர்வு and சீர்[-1].மொழி[-1] == "ு":
                            சேர்க்க(காசு_பிறப்பு_தேர்வு[சீர்.வாய்ப்பாடு])
                        else:
                            சேர்க்க(சீர்.வாய்ப்பாடு)
                    else:
                        சேர்க்க(சீர்.அசைப்பெயர்கள்)
                else:
                    if சீர் is not பா_முதற்சீர்:
                        சேர்க்க(சீர்[0].பெயர்)
                    if len(சீர்) != 1:
                        சேர்க்க("…")
                    if சீர் is not பா_இறுதிச்சீர்:
                        சேர்க்க(சீர்.ஈற்றசைப்பெயர் if சீர்.ஈற்றசைப்பெயர் else ஈற்றசைப்பெயர்_இல்லை)
                if சீர் is not பா_இறுதிச்சீர்:
                    சேர்க்க("{" + (தளைகளின்_சுருக்கமான_பெயர்கள்[சீர்.தளை] if சீர்.தளை else தளைப்பெயர்_இல்லை) + "}")
            அடி_ஆய்வு.append(" ".join(அடி_ஆய்வு_வரி))
        அடி_ஆய்வு.append("")
    அடி_ஆய்வு = "\n".join(அடி_ஆய்வு)
    if சீரின்_முழு_வாய்ப்பாடு_காட்டவும்:
        அடி_முழு_ஆய்வு = அடி_ஆய்வு
    else:
        அடி_சுருக்க_ஆய்வு = அடி_ஆய்வு


def பா_மொத்த_ஆய்வு_உருவாக்கு():
    global பா_மொத்த_ஆய்வு
    பா_மொத்த_ஆய்வு = []
    for பா in அலகிடப்பட்ட_பாக்கள்:
        if not பா:  # தமிழ் இல்லாத வரியாக இருக்கும்
            continue
        பா_மொத்த_ஆய்வு.append(
            "“{} … {}” : அடிகள் {} : {}\n".format(பா[0][0].மொழி, பா[-1][-1].மொழி, len(பா), பா.தளை_விவரம்()))
    பா_மொத்த_ஆய்வு = "\n".join(பா_மொத்த_ஆய்வு)


class அசை_உறுப்பு_காட்டுவோன்(QSyntaxHighlighter):

    def __init__(தான், தாய், பாவை):
        super().__init__(தாய்)
        தான்.பாவை = பாவை

    def highlightBlock(தான், உள்ளீட்டு_வரி):
        ஆய்வுகளை_உருவாக்கு(தான்.பாவை.உள்ளீட்டுப்பெட்டி.toPlainText())
        உள்ளீட்டு_வரி += "\n"
        for பா in அலகிடப்பட்ட_பாக்கள்:
            if not பா:
                continue
            for அடி in பா:
                if அடி.உள்ளீட்டு_வரி != உள்ளீட்டு_வரி:
                    continue
                for சீர்_எண், சீர் in enumerate(அடி):
                    for அசை_எண், அசை in enumerate(சீர்):
                        if சீர்_எண் > 15 or அசை_எண் > 3:
                            பூச்சு = வண்ணம்_தவறு
                        else:
                            பூச்சு = வண்ணங்கள்_அசைகள்[அசை.பெயர்][அசை_எண்]
                        தான்.setFormat(அசை.தொடக்கம், அசை.முடிவு - அசை.தொடக்கம், பூச்சு)


class அடி_ஆய்வு_உறுப்பு_காட்டுவோன்(QSyntaxHighlighter):

    def __init__(தான், தாய்):
        super().__init__(தாய்)

    import re
    தளை_வடிவம் = re.compile("\{([^}]+)\}")

    def highlightBlock(தான், உள்ளீட்டு_வரி):
        try:
            தான்.setFormat(0, உள்ளீட்டு_வரி.index(":") + 1, வண்ணம்_ஆய்வு_சிறப்பு)
            தான்.setFormat(உள்ளீட்டு_வரி.index("?ஈற்றசை?"), 8, வண்ணம்_தவறு)
        except ValueError:
            pass
        for ஒப்பு in தான்.தளை_வடிவம்.finditer(உள்ளீட்டு_வரி):
            தான்.setFormat(ஒப்பு.start(), ஒப்பு.end() - ஒப்பு.start(), வண்ணம்_ஆய்வு_சிறப்பு if ஒப்பு.group(1) in ஏற்புடைய_தளைகள் else வண்ணம்_தவறு)


class பா_மொத்த_ஆய்வு_உறுப்பு_காட்டுவோன்(QSyntaxHighlighter):

    def __init__(தான், தாய்):
        super().__init__(தாய்)

    import re
    எண்_வடிவம் = re.compile("“.*”|[\d\.]+%?")

    def highlightBlock(தான், உள்ளீட்டு_வரி):
        for ஒப்பு in தான்.எண்_வடிவம்.finditer(உள்ளீட்டு_வரி):
            தான்.setFormat(ஒப்பு.start(), ஒப்பு.end() - ஒப்பு.start(), வண்ணம்_ஆய்வு_சிறப்பு)


class பாவை_ஜன்னல்(QWidget):

    def __init__(தான்):

        super().__init__()
        தான்.setWindowTitle("பாவை – அறிய, இயற்ற")

        # உள்ளீடு

        பெ = தான்.உள்ளீட்டுப்பெட்டி = QPlainTextEdit()
        பெ.setPlaceholderText("பாவை இங்கு உள்ளிடுக")
        பெ.setLineWrapMode(QPlainTextEdit.NoWrap)
        பெ.textChanged.connect(lambda: தான்.உள்ளீட்டைக்_கையாள்())
        தான்.அசை_உறுப்பு_காட்டுவோன் = அசை_உறுப்பு_காட்டுவோன்(பெ.document(), தான்)

        ஒ = தான்.உள்ளீட்டு_ஒட்டி = QLabel("உள்ளீடு (&I):")
        ஒ.setBuddy(பெ)

        உ = தான்.உள்ளீட்டு_உறுப்புகள் = QWidget()
        அ = QVBoxLayout()
        அ.addWidget(ஒ)
        அ.addWidget(பெ)
        உ.setLayout(அ)

        # அடி ஆய்வு

        பெ = தான்.அடி_ஆய்வுப்பெட்டி = QPlainTextEdit()
        பெ.setReadOnly(True)
        பெ.setLineWrapMode(QPlainTextEdit.NoWrap)
        தான்.அடி_ஆய்வு_உறுப்பு_காட்டுவோன் = அடி_ஆய்வு_உறுப்பு_காட்டுவோன்(பெ.document())

        ஒ = தான்.அடி_ஆய்வு_ஒட்டி = QLabel("அடி ஆய்வு (&A):")
        ஒ.setBuddy(பெ)
        
        அ = தான்.சீரின்_முழு_வாய்ப்பாடு_தேர்வு_அழுத்துவான் = QCheckBox("சீரின் முழு வாய்ப்பாடைக் காட்டு (&F)")
        அ.toggled.connect(lambda: தான்.சீரின்_முழு_வாய்ப்பாடு_காட்டுவது())

        உ = தான்.அடி_ஆய்வு_உறுப்புகள் = QWidget()
        அ1 = QHBoxLayout()
        அ1.addWidget(ஒ)
        அ1.addWidget(அ)
        அ2 = QVBoxLayout()
        அ2.addLayout(அ1)
        அ2.addWidget(பெ)
        உ.setLayout(அ2)

        # உள்ளீட்டையும் அடி ஆய்வையும் உடைத்துக் காட்ட

        உ = தான்.உள்ளீடு_அடி_ஆய்வு_உடைப்பான் = QSplitter()
        உ.addWidget(தான்.உள்ளீட்டு_உறுப்புகள்)
        உ.addWidget(தான்.அடி_ஆய்வு_உறுப்புகள்)
        உ.setChildrenCollapsible(False)

        # பா மொத்த ஆய்வு

        பெ = தான்.பா_மொத்த_ஆய்வுப்பெட்டி = QPlainTextEdit()
        பெ.setReadOnly(True)
        தான்.பா_மொத்த_ஆய்வு_உறுப்பு_காட்டுவோன் = பா_மொத்த_ஆய்வு_உறுப்பு_காட்டுவோன்(பெ.document())

        ஒ = தான்.பா_ஆய்வு_ஒட்டி = QLabel("பா ஆய்வு (&P):")
        ஒ.setBuddy(பெ)

        உ = தான்.பா_மொத்த_ஆய்வு_உறுப்புகள் = QWidget()
        அ = QVBoxLayout()
        அ.addWidget(ஒ)
        அ.addWidget(பெ)
        உ.setLayout(அ)

        # உள்ளீட்டையும் அடி ஆய்வையும் உடைத்துக் காட்ட

        உ = தான்.உள்ளீடு_அடி_ஆய்வு_பா_மொத்த_ஆய்வு_உடைப்பான் = QSplitter(Qt.Vertical)
        உ.addWidget(தான்.உள்ளீடு_அடி_ஆய்வு_உடைப்பான்)
        உ.addWidget(தான்.பா_மொத்த_ஆய்வு_உறுப்புகள்)
        உ.setChildrenCollapsible(False)

        # உள்ளீட்டுப் பெட்டி, ஆய்வுப் பெட்டிகள் இவற்றுள் சறுக்குவான்களை ஒருங்கிணைக்க

        for சுருள்_பெயர் in "verticalScrollBar", "horizontalScrollBar":
            சறுக்குவான்கள்_சார்பிடம்_ஒருங்கிணைக்க(*(getattr(பெ, சுருள்_பெயர்)() for பெ in \
                                                    (தான்.உள்ளீட்டுப்பெட்டி, தான்.அடி_ஆய்வுப்பெட்டி, தான்.பா_மொத்த_ஆய்வுப்பெட்டி)))

        # உதவி அழுத்துவான்கள்

        அ = தான்.உள்ளீட்டை_நீக்குதல்_அழுத்துவான் = QPushButton("உள்ளீட்டை நீக்குக (&C)")
        அ.clicked.connect(lambda: தான்.உள்ளீட்டை_நீக்கு())

        அ = தான்.தளைகள்_தேர்வு_அழுத்துவான் = QPushButton("ஏற்புடைய தளைகள்… (&T)")
        அ.clicked.connect(lambda: தான்.தளைகள்_தேர்வு_காட்டு())

        அமை = தான்.அழுத்துவான்கள்_அமைப்பு = QHBoxLayout()
        அமை.addWidget(தான்.உள்ளீட்டை_நீக்குதல்_அழுத்துவான்)
        அமை.addWidget(தான்.தளைகள்_தேர்வு_அழுத்துவான்)

        # ஏற்புடைய தளைகளைத் தேர்வு செய்ய

        def செயல்படுத்துவான்(அழுத்துவான்):  # தளை தேர்வு செய்ய/நீக்க ஏற்படும் அறிக்கைகளுக்குத் தகுந்த செயலை உருவாக்குகிறது
            def செயல்(தேர்வு):
                (ஏற்புடைய_தளைகள்.add if தேர்வு else ஏற்புடைய_தளைகள்.remove)(தளைகளின்_சுருக்கமான_பெயர்கள்[அழுத்துவான்.text()])
            return செயல்

        தான்.தளைகள்_தேர்வு_அழுத்துவான்கள் = [QCheckBox(தளை) for தளை in தளைகள்]
        அமை = தான்.தளைகள்_பெட்டி_அமைப்பு = QVBoxLayout()
        for அ in தான்.தளைகள்_தேர்வு_அழுத்துவான்கள்:
            அ.toggled.connect(செயல்படுத்துவான்(அ))
            அ.toggled.connect(lambda: தான்.அடி_ஆய்வு_உறுப்பு_காட்டுவோன்.rehighlight())
            அமை.addWidget(அ)

        பெ = தான்.தளைகள்_தேர்வு_பெட்டி = QWidget(தான்)  # தான் என்பது முக்கியம் ஏனெனில் இதனைத் தனக்குள் அமைப்பில் உட்படுத்தவில்லை
        பெ.setWindowFlags(Qt.Dialog)  # தனியாகக் காட்டுவதற்கு
        பெ.setWindowTitle("தளைகள்")
        பெ.setLayout(அமை)

        # வண்ணத்திட்டம் தேர்வு செய்ய

        தான்.வண்ணத்திட்டம்_ஒட்டி = QLabel("வண்ணத்திட்டம்")

        அ = தான்.வண்ணத்திட்டம்_வெண்மை_அழுத்துவான் = QRadioButton("வெண்மை (&L)")
        அ.clicked.connect(lambda: தான்.வண்ணத்திட்டம்_அமை("வெண்மை"))
        அ.click()

        அ = தான்.வண்ணத்திட்டம்_கறுமை_அழுத்துவான் = QRadioButton("கறுமை (&D)")
        அ.clicked.connect(lambda: தான்.வண்ணத்திட்டம்_அமை("கறுமை"))

        அ = தான்.பற்றி_அழுத்துவான் = QPushButton("பாவை பற்றி… (&X)")
        அ.clicked.connect(lambda: தான்.பற்றி())

        அமை = தான்.வண்ணத்திட்ட_அமைப்பு = QHBoxLayout()
        அமை.addWidget(தான்.வண்ணத்திட்டம்_ஒட்டி)
        அமை.addWidget(தான்.வண்ணத்திட்டம்_வெண்மை_அழுத்துவான்)
        அமை.addWidget(தான்.வண்ணத்திட்டம்_கறுமை_அழுத்துவான்)
        அமை.addWidget(தான்.பற்றி_அழுத்துவான்)

        # ஒட்டு மொத்த அமைப்பு

        அமை = தான்.நீள்_அமைப்பு = QVBoxLayout()
        அமை.addWidget(தான்.உள்ளீடு_அடி_ஆய்வு_பா_மொத்த_ஆய்வு_உடைப்பான்)
        அமை.addLayout(தான்.அழுத்துவான்கள்_அமைப்பு)
        அமை.addLayout(தான்.வண்ணத்திட்ட_அமைப்பு)
        தான்.setLayout(அமை)

        தான்.அமைப்புகள்_பதிவெடு()

    def closeEvent(தான், நிகழ்வு):
        if தான்.உள்ளீட்டை_நீக்கலாமா("வெளியேறுவதா"):
            தான்.அமைப்புகள்_பதிவிடு()
        else:
            நிகழ்வு.ignore()

    def அமைப்புகள்_பதிவிடு(தான்):
        அமை = QSettings("ஶ்ரீரமண ஶர்மா", "பாவை")
        அமை.setValue("கடவுள் வாழ்த்து காட்டியாயிற்று", True)
        அமை.setValue("சீரின் முழு வாய்ப்பாடைக் காட்டு", தான்.சீரின்_முழு_வாய்ப்பாடு_தேர்வு_அழுத்துவான்.isChecked())
        அமை.setValue("வண்ணத்திட்டம்", "வெண்மை" if தான்.வண்ணத்திட்டம்_வெண்மை_அழுத்துவான்.isChecked() else "கறுமை")
        அமை.beginGroup("ஏற்புடைய தளைகள்")
        for அ in தான்.தளைகள்_தேர்வு_அழுத்துவான்கள்:
            அமை.setValue(அ.text(), அ.isChecked())
        அமை.endGroup()

    def அமைப்புகள்_பதிவெடு(தான்):
        அமை = QSettings("ஶ்ரீரமண ஶர்மா", "பாவை")
        if not அமை.value("கடவுள் வாழ்த்து காட்டியாயிற்று", defaultValue = False, type = bool):
            தான்.உள்ளீட்டுப்பெட்டி.setPlainText(கடவுள்_வாழ்த்து)
        தான்.சீரின்_முழு_வாய்ப்பாடு_தேர்வு_அழுத்துவான்.setChecked(அமை.value("சீரின் முழு வாய்ப்பாடைக் காட்டு", defaultValue = False, type = bool))
        வண்ணத்திட்டம் = அமை.value("வண்ணத்திட்டம்", defaultValue = "வெண்மை")
        if வண்ணத்திட்டம் == "வெண்மை":
            தான்.வண்ணத்திட்டம்_வெண்மை_அழுத்துவான்.click()  # clicked அறிக்கையினால் தான் வண்ணத்திட்டத்தை அமல்படுத்துவதால் setChecked போதாது
        else:
            தான்.வண்ணத்திட்டம்_கறுமை_அழுத்துவான்.click()
        அமை.beginGroup("ஏற்புடைய தளைகள்")
        for அ in தான்.தளைகள்_தேர்வு_அழுத்துவான்கள்:
            அ.setChecked(அமை.value(அ.text(), defaultValue = True, type = bool))
        அமை.endGroup()

    def பற்றி(தான்):
        QMessageBox.about(தான், "பாவை",
                "பாக்களை அறிய/இயற்ற உதவும்பொருட்டு உருவாக்கப்பட்டது<br>"
                "‘<b>பாவை</b>’ என்ற இந்த மென்பொருள்.<br><br>"
                "<b>காப்புரிமை</b>: <a href=\"mailto:jamadagni@gmail.com\">ஶ்ரீரமண ஶர்மா</a>, 2018<br>"
                "<b>உரிமம்</b>: <a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\">GPL v3+</a><br><br>"
                "<b>மேலும் பார்க்க</b>: நண்பர் வினோத் ராஜனின் வலைத்தள செயலி <a href=\"http://avalokitam.com\">அவலோகிதம்</a>")

    def உள்ளீட்டைக்_கையாள்(தான்):
        ஆய்வுகளை_உருவாக்கு(தான்.உள்ளீட்டுப்பெட்டி.toPlainText())
        தான்.அடி_ஆய்வு_காட்டு()
        தான்.பா_மொத்த_ஆய்வுப்பெட்டி.setPlainText(பா_மொத்த_ஆய்வு)

    def உள்ளீட்டை_நீக்கலாமா(தான், கேள்வி):
        if தான்.உள்ளீட்டுப்பெட்டி.toPlainText() in ("", கடவுள்_வாழ்த்து):
            return True
        else:
            return QMessageBox.warning(தான், "பாவை: {}?".format(கேள்வி),
                                   "தாங்கள் உள்ளீட்டை நகலிட்டுக்கொள்ள விரும்பலாம்.\n{}?".format(கேள்வி),
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes

    def உள்ளீட்டை_நீக்கு(தான்):
        if தான்.உள்ளீட்டை_நீக்கலாமா("உள்ளீட்டை நீக்கவா"):
            தான்.உள்ளீட்டுப்பெட்டி.clear()
            தான்.உள்ளீட்டுப்பெட்டி.setFocus()

    def அடி_ஆய்வு_காட்டு(தான்):
        உள்ளீட்டு_இடம் = தான்.உள்ளீட்டுப்பெட்டி.verticalScrollBar().value()
        தான்.அடி_ஆய்வுப்பெட்டி.setPlainText(அடி_முழு_ஆய்வு if சீரின்_முழு_வாய்ப்பாடு_காட்டவும் else அடி_சுருக்க_ஆய்வு)
        தான்.அடி_ஆய்வுப்பெட்டி.verticalScrollBar().setValue(உள்ளீட்டு_இடம்)  # அடி ஆய்வுப்பெட்டியில் உள்ளீட்டின் அளவே வரிகள் இருப்பதால் இது சரியாகிறது

    def சீரின்_முழு_வாய்ப்பாடு_காட்டுவது(தான்):
        global சீரின்_முழு_வாய்ப்பாடு_காட்டவும்
        சீரின்_முழு_வாய்ப்பாடு_காட்டவும் = தான்.சீரின்_முழு_வாய்ப்பாடு_தேர்வு_அழுத்துவான்.isChecked()
        அடி_ஆய்வு_உருவாக்கு()
        தான்.அடி_ஆய்வு_காட்டு()

    def தளைகள்_தேர்வு_காட்டு(தான்):
        உதவிப்பெட்டி_காட்டு(தான், தான்.தளைகள்_தேர்வு_பெட்டி)

    def வண்ணத்திட்டம்_அமை(தான், பெயர்):

        global வண்ணங்கள்_அசைகள், வண்ணம்_ஆய்வு_சிறப்பு, வண்ணம்_தவறு
        வ = வண்ணத்திட்டங்கள்_உறுப்பு_காட்டுவோனுக்கு[பெயர்]
        வண்ணங்கள்_அசைகள் = வ["சீரின் அசைகள்"]
        வண்ணம்_ஆய்வு_சிறப்பு = வ["ஆய்வு சிறப்பு"]
        வண்ணம்_தவறு = வ["தவறு"]

        பி = வ["பின்னணி"]
        தான்.உள்ளீட்டுப்பெட்டி.setStyleSheet("QPlainTextEdit {{ color: {}; background: {} }}".format(வ["தமிழ் அல்லாதது"], பி))
        தான்.அடி_ஆய்வுப்பெட்டி.setStyleSheet("QPlainTextEdit {{ color: {}; background: {} }}".format(வ["ஆய்வு"], பி))
        தான்.பா_மொத்த_ஆய்வுப்பெட்டி.setStyleSheet("QPlainTextEdit {{ color: {}; background: {} }}".format(வ["ஆய்வு"], பி))
        தான்.அசை_உறுப்பு_காட்டுவோன்.rehighlight()
        தான்.அடி_ஆய்வு_உறுப்பு_காட்டுவோன்.rehighlight()


செயலி = QApplication([])
ஜன்னல் = பாவை_ஜன்னல்()
ஜன்னல்.show()
செயலி.exec_()
