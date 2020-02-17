"""
    the logitcal py for gui
"""
from PyQt5.QtCore import QCoreApplication
from ui_layout import Ui_MainWindow
import vocal_collection
from speech_recoginition import recognize
from play_audio import play
from tf_idf import text_match

WECOME = -1
BYEBYE = 6


class GUI(Ui_MainWindow):
    """
        the gui with logit
    """
    def __init__(self, MainWindow):
        super(GUI, self).__init__(MainWindow)
        self.recorder = vocal_collection.Recorder(save_path="record\\sample.wav")
        self.pushButton.clicked.connect(self.recording)
        self.pushButton_2.clicked.connect(self.responding)
        self.pushButton_3.clicked.connect(self.quit_play)
        self.pushButton_3.clicked.connect(QCoreApplication.instance().quit)
        self.play = play
        self.recognize = recognize
        self.text = ''
        self.play_path = 'output\\'
        self.record_path = "record\\sample.wav"
        self.mapping = {0: '取款', 1: '存款', 2: '转账', 3: '查询余额', 4: '修改密码', 5: '打印账单',8:'空表'}


    def recording(self):
        """

        :return:
        """
        self.recorder.start()
        print("--录音开始--")

    def responding(self):
        """

        :return:
        """
        print("--录音结束--")
        print("--开始匹配--")
        self.recorder.stop()
        recognized_text = self.recognize(self.record_path)
        print('%s' % recognized_text)
        if recognized_text == '':
            act_id = 8
        else:
            act_id = text_match(recognized_text)
        print("--匹配结束--")
        self.set_text(act_id)
        self.lineEdit.setText(self.text)
        self.play_action(act_id)


    def quit_play(self):
        """

        :return:
        """
        self.play_action(BYEBYE)

    def play_action(self, record_id=WECOME):
        """

        :param record_id:
        :return:
        """
        self.play(record_id, self.play_path)

    def set_text(self, act_id):
        """

        :param act_id:
        :return:
        """
        text1 = '您好, 已接通'
        text2 = '服务！'
        if act_id in [x for x in range(4)]:
            self.text = text1 + self.mapping[act_id] + text2
        elif act_id == -1:
            self.text = '欢迎使用自动取款机！'
        elif act_id == 5:
            self.text = '您好，正在打印账单！'
        elif act_id == 6:
            self.text = '感谢使用！'
        elif act_id == 7:
            self.text = '匹配不到您所描述的功能，请重新描述，或者转人工服务！'
        elif act_id == 8:
            self.text = '请读入语音！'
        else:
            self.text = 'error'
        print(self.text)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     MainWindow = QMainWindow()
#     ui = GUI(MainWindow)
#     MainWindow.show()
#     ui.play(WECOME)
#
#     sys.exit(app.exec_())

