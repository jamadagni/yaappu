# -*- coding: utf-8 -*-

# காப்புரிமை 2018, ஶ்ரீரமண ஶர்மா
# Copyright 2018, Shriramana Sharma
#
# Use and redistribution with or without modification is permitted without
# restrictions. THERE IS NO WARRANTY WHATSOEVER.


from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication


def உதவிப்பெட்டி_காட்டு(ஜன்னல், உதவிப்பெட்டி):
    இருக்குமிடம் = QApplication.desktop().availableGeometry()
    ஜன்னல்_உருவம் = ஜன்னல்.frameGeometry()
    அகலம் = உதவிப்பெட்டி.sizeHint().width()
    if இருக்குமிடம்.right() - ஜன்னல்_உருவம்.right() > அகலம்:  # வலது புறம் இடம் உள்ளது
        உதவிப்பெட்டி.move(ஜன்னல்_உருவம்.topRight())
    else:  # வலது புறம் இடம் இல்லை
        if ஜன்னல்_உருவம்.left() - இருக்குமிடம்.left() > அகலம்:  # இடது புறம் இடம் உள்ளது
            உதவிப்பெட்டி.move(ஜன்னல்_உருவம்.topLeft() - QPoint(அகலம், 0))
        else:  # இரு புறமும் இடம் இல்லை
            உதவிப்பெட்டி.move(ஜன்னல்_உருவம்.topRight() - QPoint(அகலம், 0))
    உதவிப்பெட்டி.show()
