import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
from datetime import datetime

class MIT_gen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置应用图标
        self.setWindowIcon(QIcon('icons/licence.svg'))

        # 设置主窗口属性
        self.setWindowTitle('MIT_gen')

        layout = QVBoxLayout()

        # 创建名字输入框
        self.name_input = QLineEdit(self)
        layout.addWidget(QLabel('你的名字:', self))
        layout.addWidget(self.name_input)

        # 创建邮箱地址输入框
        self.email_input = QLineEdit(self)
        layout.addWidget(QLabel('邮箱地址:', self))
        layout.addWidget(self.email_input)

        # 创建文本编辑框
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        # 创建生成按钮
        generate_button = QPushButton('生成MIT许可证', self)
        generate_button.clicked.connect(self.generate_license)
        layout.addWidget(generate_button)

        # 设置布局
        self.setLayout(layout)

        self.setWindowTitle('MIT许可证生成器')
        self.setGeometry(100, 100, 600, 400)

    def generate_license(self):
        # 获取用户输入
        current_year = datetime.now().year
        author_name = self.name_input.text()
        email_address = self.email_input.text()

        # 生成MIT许可证文本
        license_text = self.MIT_gen(current_year, author_name, email_address)

        # 在文本编辑框中显示生成的许可证
        self.text_edit.setPlainText(license_text)

    def MIT_gen(self, current_year, author_name, email_address):
        license_text = f"""MIT License
Copyright (c) {current_year}, {author_name}({email_address})
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject
to the following conditions:
The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
(MIT license, http://www.opensource.org/licenses/mit-license.html)
"""

        return license_text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MIT_gen()
    window.show()
    sys.exit(app.exec_())
