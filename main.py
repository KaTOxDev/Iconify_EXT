import sys
import os
import ctypes
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox
)
from PyQt6.QtGui import QIcon
import winreg

class IconAssigner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🖼️ File Icon Assigner Pro")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setGeometry(100, 100, 400, 250)

        layout = QVBoxLayout()

        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText("File extension (e.g. .kato)")
        layout.addWidget(QLabel("🧩 File Extension"))
        layout.addWidget(self.ext_input)

        self.icon_path = QLineEdit()
        self.icon_path.setPlaceholderText("Path to .ico file")
        layout.addWidget(QLabel("🎨 Icon File"))
        layout.addWidget(self.icon_path)

        browse_icon_btn = QPushButton("Browse Icon...")
        browse_icon_btn.clicked.connect(self.browse_icon)
        layout.addWidget(browse_icon_btn)

        self.app_path = QLineEdit()
        self.app_path.setPlaceholderText("Path to app to open this file type (optional)")
        layout.addWidget(QLabel("📦 Associated App (Optional)"))
        layout.addWidget(self.app_path)

        browse_app_btn = QPushButton("Browse App...")
        browse_app_btn.clicked.connect(self.browse_app)
        layout.addWidget(browse_app_btn)

        apply_btn = QPushButton("🔥 Apply Association")
        apply_btn.clicked.connect(self.apply_icon)
        layout.addWidget(apply_btn)

        restart_btn = QPushButton("♻️ Restart Explorer")
        restart_btn.clicked.connect(self.restart_explorer)
        layout.addWidget(restart_btn)

        self.setLayout(layout)

    def browse_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon", "", "Icons (*.ico)")
        if file_path:
            self.icon_path.setText(file_path)

    def browse_app(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select App", "", "Executables (*.exe)")
        if file_path:
            self.app_path.setText(file_path)

    def apply_icon(self):
        ext = self.ext_input.text().strip()
        icon = self.icon_path.text().strip()
        app = self.app_path.text().strip()

        if not ext.startswith(".") or not icon or not os.path.exists(icon):
            QMessageBox.critical(self, "Error", "Please enter valid extension and icon path.")
            return

        prog_id = f"{ext[1:].capitalize()}File"

        try:
            # Register extension
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ext) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, prog_id)

            # Set icon
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{prog_id}\\DefaultIcon") as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, icon)

            # Set app to open the file
            if app:
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{prog_id}\\shell\\open\\command") as key:
                    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{app}" "%1"')

            QMessageBox.information(self, "Success", "File association applied successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def restart_explorer(self):
        try:
            subprocess.run(["taskkill", "/F", "/IM", "explorer.exe"], shell=True)
            subprocess.run(["start", "explorer"], shell=True)
            QMessageBox.information(self, "Done", "Explorer restarted.")
        except Exception as e:
            QMessageBox.critical(self, "Oops!", str(e))


if __name__ == "__main__":
    # Admin check
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    app = QApplication(sys.argv)
    window = IconAssigner()
    window.show()
    sys.exit(app.exec())
