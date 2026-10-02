# styles/scrollbar.py

SCROLLBAR = """

/* =========================================================
   SCROLLBAR VERTICAL
========================================================= */

QScrollBar:vertical {
    background: #111111;
    width: 16px;
    border-radius: 8px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 #0078ff,
        stop:1 #00bfff
    );

    min-height: 45px;
    border-radius: 8px;
}

QScrollBar::handle:vertical:hover {
    background: #33aaff;
}

QScrollBar::handle:vertical:pressed {
    background: #005ed1;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    border: none;
    background: none;
    height: 0px;
}

QScrollBar::up-arrow:vertical,
QScrollBar::down-arrow:vertical {
    background: none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}


/* =========================================================
   SCROLLBAR HORIZONTAL
========================================================= */

QScrollBar:horizontal {
    background: #111111;
    height: 16px;
    border-radius: 8px;
    margin: 4px;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 #00bfff,
        stop:1 #0078ff
    );

    min-width: 45px;
    border-radius: 8px;
}

QScrollBar::handle:horizontal:hover {
    background: #33ccff;
}

QScrollBar::handle:horizontal:pressed {
    background: #0099ff;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
    width: 0px;
}

QScrollBar::left-arrow:horizontal,
QScrollBar::right-arrow:horizontal {
    background: none;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: transparent;
}

"""