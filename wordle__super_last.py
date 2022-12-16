import sys
import random
import time
import sqlite3
from PyQt5.QtSql import *

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, i, j):
        super().__init__()

        self.stopwatch = time.time()

        self.setGeometry(300, 100, 570, 900)
        self.setWindowTitle('Wordle')
        self.i = i
        self.j = j
        self.names = [''] * i * j
        self.nowj = 0
        self.red = True


        f = open('words3.txt', 'r')
        self.lines = f.readlines()
        self.word = self.pickWord()

        fedu = QFont()
        fedu.setPointSize(25)
        fedu.setBold(True)
        fedu.setItalic(True)

        self.edu = QPushButton(self)
        self.edu.setText('Education')
        self.edu.move(160, 810)
        self.edu.resize(230, 50)
        self.edu.setFont(fedu)

        fontinp = QFont()
        fontinp.setPointSize(42)
        fontinp.setBold(True)
        fontinp.setCapitalization(True)

        self.inp = QLineEdit(self)
        self.inp.move(int((560 - 46 * self.i) / 2), 50 + self.j * 60)
        self.inp.resize(46 * self.i, 90)
        self.inp.setFont(fontinp)

        self.drawGrid()

        self.font = QFont()
        self.font.setPointSize(42)
        self.font.setBold(True)

        fontlet = QFont()
        fontlet.setPointSize(36)
        fontlet.setBold(True)
        fontlet.setCapitalization(True)

        self.letters1 = QLineEdit(self)
        self.letters1.setEnabled(False)
        self.letters1.move(10, 690)
        self.letters1.resize(530, 50)
        self.letters1.setText('ABCDEFGHIJKLM')
        self.letters1.setFont(fontlet)
        self.letters1.setAlignment(Qt.AlignHCenter)

        self.letters2 = QLineEdit(self)
        self.letters2.setEnabled(False)
        self.letters2.move(5, 740)
        self.letters2.resize(560, 50)
        self.letters2.setText('NOPQRSTUVWXYZ')
        self.letters2.setAlignment(Qt.AlignHCenter)
        self.letters2.setFont(fontlet)

        fontset = QFont()
        fontset.setPointSize(50)

        self.set = QPushButton(self)
        self.set.setText('\u2699')
        self.set.move(455, 797)
        self.set.resize(100, 103)
        self.set.setFont(fontset)

        self.reset = QPushButton(self)
        self.reset.setText('\u21BA')
        self.reset.move(78, 810)
        self.reset.resize(70, 70)
        self.reset.setFont(fontset)

        self.edu_screen = Education()
        self.set_screen = Settings(self.i, self.j, self)

        self.inp.textChanged.connect(self.check)
        self.edu.clicked.connect(self.education)
        self.set.clicked.connect(self.settings)
        self.reset.clicked.connect(self.clear)

    def check(self) -> None:


        txt = self.inp.text().lower()
        if len(txt) == self.i + 1:
            if not self.red:
                if txt[-1] == ' ':
                    self.putWord(txt.upper())
                    self.inp.setText('')
                    if self.nowj == self.j:
                        self.lw = LoseWindow(self, self.word[:-1], self.j, time.time() - self.stopwatch, time.ctime(int(time.time())))
                        self.lw.show()
                else:
                    self.inp.setText(txt[:-1])
            else:
                self.inp.setText(txt[:-1])

        if len(txt) == self.i:
            txt = txt + '\n'
            if txt not in self.lines:
                self.inp.setStyleSheet("background-color: red")
                self.red = True
            else:
                self.red = False
                self.inp.setStyleSheet("background-color: white")

        if len(txt) < self.i:
            self.red = False
            self.inp.setStyleSheet("background-color: white")

    def putWord(self, txt):
        colors = ['blue'] * self.i
        k = 0
        cw = self.word
        for i in txt:
            if i == cw[k]:
                colors[k] = 'green'
            elif i in cw:
                colors[k] = 'yellow'

            k += 1

        for i in range(self.i):
            c = self.nowj * self.i + i
            self.names[c].setText(txt[i])
            self.names[c].setFont(self.font)
            self.names[c].setAlignment(Qt.AlignCenter)
            self.names[c].setStyleSheet('background-color: ' + colors[i])

            if txt[i] <= 'M':
                let = self.letters1.text()
                if txt[i] in let:
                    ind = let.index(txt[i])
                    let = let[:ind] + let[ind+1:]
                    self.letters1.setText(let)
            else:
                let = self.letters2.text()
                if txt[i] in let:
                    ind = let.index(txt[i])
                    let = let[:ind] + let[ind+1:]
                    self.letters2.setText(let)
        self.nowj += 1

        if colors == ['green'] * self.i:
            self.win()

    def win(self):
        self.ww = WinWindow(self, self.word[:-1], self.nowj, self.j, time.time() - self.stopwatch, time.ctime(int(time.time())))
        self.ww.show()
        self.clear()

    def drawGrid(self):
        for j in range(self.j):
            for i in range(self.i):
                c = i + j * self.i
                self.names[c] = QLabel(self)
                self.names[c].move(int((560 - self.i * 60) / 2) + i * 60, 10 + j * 60)
                self.names[c].resize(57, 57)
                self.names[c].setStyleSheet("background-color: blue")

    def pickWord(self):
        return random.choice(list(filter(lambda x: len(x) == self.i + 1, self.lines))).upper()

    def clear(self):
        for j in range(self.j):
            for i in range(self.i):
                c = i + j * self.i
                self.names[c].setText('')
                self.names[c].setStyleSheet("background-color: blue")
        self.word = self.pickWord()
        self.nowj = 0
        self.stopwatch = time.time()
        self.inp.setEnabled(True)
        self.inp.setText('')
        self.letters1.setText('ABCDEFGHIJKLM')
        self.letters2.setText('NOPQRSTUVWXYZ')

    def education(self):
        self.edu_screen.show()
        #self.ww = WinWindow(self.word[:-1], self.nowj, self.j, time.time() - self.stopwatch, time.ctime(int(time.time())))
        #self.ww.show()

    def settings(self):
        self.set_screen.show()

    def restart(self):
        self.main_screen = MainWindow(self.set_screen.idi.value(), self.set_screen.idj.value())
        self.main_screen.show()
        self.close()


class WinWindow(QWidget):
    def __init__(self, mw, word, line, j, period, now_time):
        super().__init__()

        self.t = now_time
        self.line = line
        self.j = j
        self.word = word
        self.period = period
        self.mw = mw
        self.write_stats(now_time, word, line, int(period), len(word), j)

        self.setWindowTitle('Notification')
        self.setGeometry(300, 300, 500, 500)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_color)
        self.timer.start(1000)

        font_stat = QFont()
        font_stat.setPointSize(16)

        self.stats = QPushButton(self)
        self.stats.setText('My Statistics')
        self.stats.move(20, 450)
        self.stats.setFont(font_stat)
        self.stats.resize(self.stats.sizeHint())


        font_lbl = QFont()
        font_lbl.setPointSize(35)
        font_lbl.setBold(True)

        self.youwon = QLabel(self)
        self.youwon.setText('You Won!')
        self.youwon.setFont(font_lbl)
        self.youwon.move(50, 75)
        self.youwon.resize(400, 100)
        self.youwon.setAlignment(Qt.AlignCenter)

        self.tries = QLabel(self)   #проверить блок на параметры
        self.tries.setText("You guessed the word within %d tries" % line)
        self.tries.setFont(font_stat)
        self.tries.move(10, 250)
        self.tries.resize(470, 40)
        self.tries.setAlignment(Qt.AlignHCenter)

        self.tries2 = QLabel(self)
        if line < j / 2:
            self.tries2.setText("You've done really awesome")
        elif line == j:
            self.tries2.setText("You were close to defeat")
        else:
            self.tries2.setText("Not bad, not bad")
        self.tries2.setFont(font_stat)
        self.tries2.move(50, 200)
        self.tries2.resize(400, 30)
        self.tries2.setAlignment(Qt.AlignHCenter)

        self.period_lbl = QLabel(self)   #проверить блок на параметры
        self.period_lbl.setFont(font_stat)
        self.period_lbl.move(50, 300)
        self.period_lbl.resize(400, 30)
        self.period_lbl.setAlignment(Qt.AlignHCenter)
        self.period_lbl.setText("You've done it within %d seconds" % int(period))

        self.btn = QPushButton(self)
        self.btn.setText('Close')
        self.btn.setFont(font_stat)
        self.btn.move(400, 450)
        self.btn.resize(self.btn.sizeHint())

        self.btn.clicked.connect(self.close)
        self.stats.clicked.connect(self.stat)

        self.mw.clear()

    def write_stats(self, nt, w, ln, p, i, j):
        con = sqlite3.connect('statistics.sqlite')
        cur = con.cursor()
        cur.execute(
            "INSERT INTO stats (win, word, day, tries, period, field) VALUES('WIN', '%s', '%s', '%s', '%s secs', '%sx%s')" % (
            w, nt, ln, p, i, j))
        con.commit()
        con.close()

    def change_color(self):
        colors = ['cyan', 'darkCyan', 'red', 'darkRed', 'magenta', 'darkMagenta', 'green', 'darkGreen', 'yellow', 'darkYellow', 'blue', 'darkBlue']
        self.youwon.setStyleSheet('background-color: %s' % random.choice(colors))
        self.timer.start(1000)

    def stat(self):
        self.sw = Statistics()
        self.sw.show()


class LoseWindow(QWidget):
    def __init__(self, mw, word, j, period, now_time):
        super(LoseWindow, self).__init__()

        self.setWindowTitle('Notification')
        self.setGeometry(300, 300, 500, 500)
        self.write_stats(now_time, word, 'MAX', int(period), len(word), j)

        font_stat = QFont()
        font_stat.setPointSize(16)

        self.stats = QPushButton(self)
        self.stats.setText('My Statistics')
        self.stats.move(20, 450)
        self.stats.setFont(font_stat)
        self.stats.resize(self.stats.sizeHint())

        font_lbl = QFont()
        font_lbl.setPointSize(35)
        font_lbl.setBold(True)

        self.youlost = QLabel(self)
        self.youlost.setText('You Lost :(')
        self.youlost.setFont(font_lbl)
        self.youlost.move(50, 75)
        self.youlost.resize(400, 100)
        self.youlost.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setPointSize(25)
        font.setBold(True)

        self.period_lbl = QLabel(self)
        self.period_lbl.setFont(font_stat)
        self.period_lbl.move(50, 300)
        self.period_lbl.resize(400, 30)
        self.period_lbl.setAlignment(Qt.AlignHCenter)
        self.period_lbl.setText("It took %d seconds" % int(period))

        self.btn = QPushButton(self)
        self.btn.setText('Close')
        self.btn.setFont(font_stat)
        self.btn.move(400, 450)
        self.btn.resize(self.btn.sizeHint())

        self.lbl = QLabel(self)
        self.lbl.setFont(font)
        self.lbl.move(50, 185)
        self.lbl.resize(400, 70)
        self.lbl.setAlignment(Qt.AlignHCenter)
        self.lbl.setText("The word was %s" % word)

        self.btn.clicked.connect(self.close)
        self.stats.clicked.connect(self.stat)

        self.mw = mw
        self.mw.clear()

    def write_stats(self, nt, w, ln, p, i, j):
        con = sqlite3.connect('statistics.sqlite')
        cur = con.cursor()
        cur.execute(
            "INSERT INTO stats (win, word, day, tries, period, field) VALUES('LOSE', '%s', '%s', '%s', '%s secs', '%sx%s')" % (
            w, nt, ln, p, i, j))
        con.commit()
        con.close()
        
    def stat(self):
        self.sw = Statistics()
        self.sw.show()


class Statistics(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Statistics')
        self.setGeometry(300, 300, 700, 700)

        font_stat = QFont()
        font_stat.setPointSize(16)

        self.btn = QPushButton(self)
        self.btn.setText('Close')
        self.btn.setFont(font_stat)
        self.btn.move(600, 650)
        self.btn.resize(self.btn.sizeHint())

        self.btn.clicked.connect(self.close)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('statistics.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('stats')
        model.select()

        self.table = QTableView(self)
        self.table.setModel(model)
        self.table.move(10, 10)
        self.table.resize(690, 580)

        self.btn2 = QPushButton(self)
        self.btn2.setText('Delete All')
        self.btn2.setFont(font_stat)
        self.btn2.move(10, 650)
        self.btn2.resize(self.btn2.sizeHint())

        self.btn2.clicked.connect(self.delete_all)

        db.close()

    def delete_all(self):
        con = sqlite3.connect('statistics.sqlite')
        cur = con.cursor()
        cur.execute("DELETE from stats")
        con.commit()
        con.close()

class Education(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Education')
        self.setGeometry(300, 300, 500, 500)

        font_fin = QFont()
        font_fin.setPointSize(16)
        font_fin.setBold(True)

        self.fin = QPushButton(self)
        self.fin.setText('Finish')
        self.fin.move(400, 10)
        self.fin.setFont(font_fin)
        self.fin.resize(self.fin.sizeHint())

        self.fin.clicked.connect(self.close)

        self.ru = QPushButton(self)
        self.ru.setText('Rules')
        self.ru.move(10, 10)
        self.ru.setFont(font_fin)
        self.rul()
        self.ru.resize(self.ru.sizeHint())

        self.mak = QPushButton(self)
        self.mak.setText('Im already \n'
                         'tired of these \n'
                         'games, I want \n'
                         'to have a snack')
        self.mak.move(100, 90)
        self.mak.resize(300, 300)
        self.mak.setFont(font_fin)
        self.makdag()

    def rul(self):
        self.ru.clicked.connect(self.papa2)

    def papa2(self):
        self.w2 = Rules()
        self.w2.show()

    def makdag(self):
        self.mak.clicked.connect(self.papa3)

    def papa3(self):
        self.w4 = Example()
        self.w4.show()


class Rules(QWidget):
    def __init__(self):
        super(Rules, self).__init__()
        self.setWindowTitle('Rules')
        self.setGeometry(300, 300, 720, 470)

        font = QFont()
        font.setPointSize(15)
        font.setItalic(True)

        self.lbl2 = QLabel(self)
        self.lbl2.setText(
            "Oh my God, didn't you understand anything \n"
            'from the words of my great creator? \n'
            'The interface is intuitive... In general,\n'
            ' if in short, then you have to enter words \n'
            'with the number of letters, \n'
            'as in the line of blue squares. \n'
            'the letter is blue - it is not in the word, \n'
            'yellow - there is, but in another place, green - \n'
            'you guessed both the letter and the place. \n'
            'And yes, donations for this creation can \n'
            "be translated by Nikita Sergeevich's phone number.\n"
            "If something goes wrong, here's our tg: @wordle_Bot572_bot'")
        self.lbl2.setFont(font)
        self.lbl2.move(10, 10)
        self.lbl2.resize(self.lbl2.sizeHint())

        font_close = QFont()
        font_close.setPointSize(16)

        self.btn = QPushButton(self)
        self.btn.setText('Close')
        self.btn.setFont(font_close)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(625, 410)

        self.btn.clicked.connect(self.close)

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        x1 = 10

        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('Order in McDonalds')

        self.check1 = QCheckBox(self)
        self.check1.setText('Cheeseburger')
        self.check1.move(x1, 0)

        self.check2 = QCheckBox(self)
        self.check2.setText('Hamburg')
        self.check2.move(x1, 25)

        self.check3 = QCheckBox(self)
        self.check3.setText('Coca-cola')
        self.check3.move(x1, 50)

        self.check4 = QCheckBox(self)
        self.check4.setText('Nuggets')
        self.check4.move(x1, 75)

        self.button = QPushButton('Order', self)
        self.button.move(x1, 120)
        self.button.resize(self.button.sizeHint())

        self.urorder = QPlainTextEdit(self)
        self.urorder.move(x1, 150)
        self.urorder.resize(200, 200)
        self.urorder.setEnabled(False)

        self.button.clicked.connect(self.order)

    def order(self):
        self.urorder.clear()
        ret = 'Your order: \n\n'

        if self.check1.isChecked():
            ret += 'Cheeseburger\n'
        if self.check2.isChecked():
            ret += 'Hamburger\n'
        if self.check3.isChecked():
            ret += 'Coca-cola\n'
        if self.check4.isChecked():
            ret += 'Nuggets\n'

        self.urorder.insertPlainText(ret)


class Settings(QWidget):
    def __init__(self, i, j, mw):
        super().__init__()

        self.applied = False

        self.setWindowTitle('Settings')
        self.setGeometry(300, 300, 500, 500)

        self.i = i
        self.j = j
        self.mw = mw

        fontfin = QFont()
        fontfin.setPointSize(16)
        fontfin.setBold(True)

        self.apply_btn = QPushButton(self)
        self.apply_btn.setText('Apply')
        self.apply_btn.move(400, 450)
        self.apply_btn.setFont(fontfin)
        self.apply_btn.resize(self.apply_btn.sizeHint())

        self.cancel_btn = QPushButton(self)
        self.cancel_btn.setText('Cancel')
        self.cancel_btn.move(15, 450)
        self.cancel_btn.setFont(fontfin)
        self.cancel_btn.resize(self.cancel_btn.sizeHint())

        self.au_btn = QPushButton(self)
        self.au_btn.setText('About us')
        self.au_btn.move(200, 450)
        self.au_btn.setFont(fontfin)
        self.mama()
        self.au_btn.resize(self.au_btn.sizeHint())

        self.re_btn = QPushButton(self)   ##добавить весь кусок в обновление
        self.re_btn.setText('Registration')
        self.re_btn.move(175, 400)
        self.re_btn.setFont(fontfin)
        self.rega()
        self.re_btn.resize(self.re_btn.sizeHint())

        self.re1_btn = QPushButton(self)  ##добавить весь кусок в обновление
        self.re1_btn.setText('Statistics')
        self.re1_btn.move(175, 350)
        self.re1_btn.setFont(fontfin)
        self.stat()
        self.re1_btn.resize(self.re1_btn.sizeHint())

        self.idi = QSpinBox(self)
        self.idi.move(350, 53)
        self.idi.setMaximum(9)
        self.idi.setMinimum(2)
        self.idi.setValue(self.i)

        font_id = QFont()
        font_id.setPointSize(20)
        font_id.setItalic(True)

        self.text_idi = QLabel(self)
        self.text_idi.setText('Length of the word')
        self.text_idi.move(60, 50)
        self.text_idi.setFont(font_id)
        self.text_idi.resize(self.text_idi.sizeHint())

        self.idj = QSpinBox(self)
        self.idj.move(350, 103)
        self.idj.setMaximum(9)
        self.idj.setMinimum(2)
        self.idj.setValue(self.j)

        self.text_idj = QLabel(self)
        self.text_idj.setText('Amount of tries')
        self.text_idj.move(60, 100)
        self.text_idj.setFont(font_id)
        self.text_idj.resize(self.text_idi.sizeHint())

        self.sca = SettingsCheckApply(self)

        self.f = True

        self.apply_btn.clicked.connect(self.apply)
        self.cancel_btn.clicked.connect(self.close)

    def apply(self):
        if self.mw.nowj and self.f:
            self.check_apply()
            return
        self.applied = True
        self.mw.restart()
        self.close()

    def check_apply(self):
        self.sca.show()

    def mama(self):
        self.au_btn.clicked.connect(self.papa1)

    def papa1(self):
        self.w2 = AboutUs()
        self.w2.show()

    def rega(self):                              #добавить 2 последние функции
        self.re_btn.clicked.connect(self.rega2)

    def rega2(self):
        self.w3 = Registr()
        self.w3.show()

    def stat(self):
        self.re1_btn.clicked.connect(self.stat1)

    def stat1(self):
        self.sw = Statistics()
        self.sw.show()

class AboutUs(QWidget):
    def __init__(self):
        super(AboutUs, self).__init__()
        self.setWindowTitle('About_us')

        font = QFont()
        font.setPointSize(15)
        font.setItalic(True)

        self.lbl1 = QLabel(self)
        self.lbl1.setText(
            'Our games have been on the market since 2007,\n'
            ' we are a company responsible for our actions \n'
            'and words, thank you for choosing us \n'
            "(we hope its not because your PC won't run\n"
            ' anything else). Our TG channel: @wordle_Bot572_bot')
        self.lbl1.setFont(font)
        self.lbl1.move(100, 10)
        self.lbl1.resize(self.lbl1.sizeHint())

class Registr(QWidget):     #добавить весь класс
    def __init__(self):

        super(Registr, self).__init__()
        self.setWindowTitle('Registration')
        self.setGeometry(300, 300, 350, 160)

        self.number1 = QLabel(self)
        self.number1.setText('Your name:')
        self.number1.move(10, 20)

        self.input1 = QLineEdit(self)
        self.input1.move(90, 20)

        self.number2 = QLabel(self)
        self.number2.setText('Your surname:')
        self.number2.move(10, 55)

        self.input1 = QLineEdit(self)
        self.input1.move(110, 55)

        self.number2 = QLabel(self)
        self.number2.setText('Your age:')
        self.number2.move(10, 90)

        self.input1 = QLineEdit(self)
        self.input1.move(90, 90)

        self.number2 = QLabel(self)
        self.number2.setText('Your email:')
        self.number2.move(10, 125)

        self.input1 = QLineEdit(self)
        self.input1.move(95, 125)

        self.sa_btn = QPushButton(self)
        self.sa_btn.setText('save')
        self.sa_btn.move(245, 120)
        self.save1()
        self.sa_btn.resize(self.sa_btn.sizeHint())

    def save1(self):
        self.sa_btn.clicked.connect(self.save2)

    def save2(self):
        self.w4 = Saveting()
        self.w4.show()


class Saveting(QWidget):       #добавить вес класс
    def __init__(self):
        super(Saveting, self).__init__()
        self.setWindowTitle('Save inforation(no)')

        font = QFont()
        font.setPointSize(15)
        font.setItalic(True)

        self.lbl5 = QLabel(self)
        self.lbl5.setText(
            'Are you serious? Did you think we would \n'
            'save such a useless information? Registered \n'
            ' - take a pie from the shelf')
        self.lbl5.setFont(font)
        self.lbl5.move(100, 10)
        self.lbl5.resize(self.lbl5.sizeHint())

class SettingsCheckApply(QWidget):
    def __init__(self, sw):
        super().__init__()

        self.setWindowTitle('Warning')
        self.setGeometry(300, 300, 450, 300)

        self.sw = sw

        font = QFont()
        font.setPointSize(15)
        font.setItalic(True)

        self.lbl = QPlainTextEdit(self)
        self.lbl.setPlainText('If you press APPLY button, your progress will be deleted permanently and you will be given another word')
        self.lbl.setFont(font)
        self.lbl.move(100, 10)
        self.lbl.resize(self.lbl.sizeHint())

        font_btn = QFont()
        font_btn.setPointSize(20)

        self.apply_btn = QPushButton(self)
        self.apply_btn.setText('Apply anyways')
        self.apply_btn.move(210, 250)
        self.apply_btn.resize(220, 40)
        self.apply_btn.setFont(font_btn)

        self.cancel_btn = QPushButton(self)
        self.cancel_btn.setText('Cancel')
        self.cancel_btn.move(10, 250)
        self.cancel_btn.resize(200, 40)
        self.cancel_btn.setFont(font_btn)

        self.apply_btn.clicked.connect(self.apply)
        self.cancel_btn.clicked.connect(self.close)

    def apply(self):
        self.sw.f = False
        self.sw.close()
        self.close()
        self.sw.apply()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(5, 6)
    ex.show()
    sys.exit(app.exec())
