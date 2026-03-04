"""
파일명: m_pathGUI.py
설명: Base Path, Exe Path, Resolution을 설정하는 다이얼로그
"""
import maya.cmds as cmds
import os

# ------------------------------------------------------------------------------
# [호환성 처리] Maya 버전에 따라 PySide2 또는 PySide6 로드
# ------------------------------------------------------------------------------
try:
    from PySide2 import QtWidgets, QtCore, QtGui
    def _run_dialog(dialog): return dialog.exec_() 
except ImportError:
    try:
        from PySide6 import QtWidgets, QtCore, QtGui
        def _run_dialog(dialog): return dialog.exec()
    except ImportError:
        cmds.error("PySide 라이브러리를 찾을 수 없습니다.")

# ------------------------------------------------------------------------------
# [커스텀 위젯] 2의 n제곱으로 움직이는 스핀박스
# ------------------------------------------------------------------------------
class PowerOfTwoSpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent=None):
        super(PowerOfTwoSpinBox, self).__init__(parent)
        # 기본적으로 텍스트를 직접 입력할 때도 유효성 검사를 하려면 추가 로직이 필요하지만,
        # 여기서는 버튼 동작(stepBy)에 집중합니다.

    def stepBy(self, steps):
        """
        화살표 버튼이나 휠을 굴렸을 때 호출되는 함수
        steps > 0: 증가 (Up)
        steps < 0: 감소 (Down)
        """
        current_val = self.value()
        
        if steps > 0:
            # 위로 누르면 2배씩 증가 (예: 64 -> 128)
            # steps가 1보다 클 때(휠 스크롤 등)도 대응하기 위해 2의 steps승 만큼 곱함
            new_val = current_val * (2 ** steps)
        else:
            # 아래로 누르면 2배씩 감소 (예: 128 -> 64)
            # 정수 나눗셈(//) 사용
            new_val = int(current_val / (2 ** abs(steps)))
        
        # 최소/최대값 범위 내에서 값 적용
        new_val = max(self.minimum(), min(new_val, self.maximum()))
        self.setValue(new_val)

# ------------------------------------------------------------------------------
# [UI 클래스]
# ------------------------------------------------------------------------------
class PathConfigDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PathConfigDialog, self).__init__(parent)
        self.setWindowTitle("Voxel Skinning Settings")
        self.resize(500, 250)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.result_base = None
        self.result_exe = None
        self.result_res = 64

        main_layout = QtWidgets.QVBoxLayout(self)

        # 1. Base Path
        grp_base = QtWidgets.QGroupBox("Scripts Folder (Base Path)")
        layout_base = QtWidgets.QHBoxLayout(grp_base)
        self.le_base = QtWidgets.QLineEdit()
        self.btn_base = QtWidgets.QPushButton("Browse...")
        self.btn_base.clicked.connect(self.browse_base_folder)
        layout_base.addWidget(self.le_base)
        layout_base.addWidget(self.btn_base)
        main_layout.addWidget(grp_base)

        # 2. EXE Path
        grp_exe = QtWidgets.QGroupBox("Voxel Solver Exe Path (.exe)")
        layout_exe = QtWidgets.QHBoxLayout(grp_exe)
        self.le_exe = QtWidgets.QLineEdit()
        self.btn_exe = QtWidgets.QPushButton("Browse...")
        self.btn_exe.clicked.connect(self.browse_exe_file)
        layout_exe.addWidget(self.le_exe)
        layout_exe.addWidget(self.btn_exe)
        main_layout.addWidget(grp_exe)

        # 3. Voxel Resolution (Power of 2)
        grp_res = QtWidgets.QGroupBox("Voxel Resolution (Power of 2)")
        layout_res = QtWidgets.QHBoxLayout(grp_res)

        # [수정됨] 커스텀 스핀박스 사용
        self.sb_res = PowerOfTwoSpinBox()
        self.sb_res.setRange(2, 4096)   # 최소 2, 최대 4096
        self.sb_res.setValue(64)        # 기본값
        self.sb_res.setFixedHeight(30)
        
        lbl_info = QtWidgets.QLabel("Values: 32, 64, 128, 256...")
        lbl_info.setStyleSheet("color: gray; font-size: 11px;")

        layout_res.addWidget(self.sb_res)
        layout_res.addWidget(lbl_info)
        main_layout.addWidget(grp_res)

        # 4. Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_run = QtWidgets.QPushButton("Run Voxel Skinning")
        self.btn_run.setFixedHeight(40)
        self.btn_run.setStyleSheet("background-color: #5D99C6; color: white; font-weight: bold;")
        self.btn_run.clicked.connect(self.accept_run)
        
        self.btn_cancel = QtWidgets.QPushButton("Cancel")
        self.btn_cancel.setFixedHeight(40)
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(self.btn_run)
        btn_layout.addWidget(self.btn_cancel)
        main_layout.addLayout(btn_layout)

        self.load_settings()

    def browse_base_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder", self.le_base.text())
        if folder: self.le_base.setText(folder)

    def browse_exe_file(self):
        res = QtWidgets.QFileDialog.getOpenFileName(self, "Select Exe", self.le_exe.text(), "Executable (*.exe)")
        filename = res[0] if isinstance(res, tuple) else res
        if filename: self.le_exe.setText(filename)

    def load_settings(self):
        if cmds.optionVar(exists="cgxr_base_path"):
            self.le_base.setText(cmds.optionVar(q="cgxr_base_path"))
        if cmds.optionVar(exists="cgxr_exe_path"):
            self.le_exe.setText(cmds.optionVar(q="cgxr_exe_path"))
        
        # 저장된 해상도 불러오기
        if cmds.optionVar(exists="cgxr_voxel_res"):
            saved_res = cmds.optionVar(q="cgxr_voxel_res")
            self.sb_res.setValue(int(saved_res))

    def accept_run(self):
        base_path = self.le_base.text().strip()
        exe_path = self.le_exe.text().strip()
        resolution = self.sb_res.value()

        if not os.path.isdir(base_path):
            cmds.warning("Invalid Scripts Folder Path!")
            return
        if not os.path.isfile(exe_path):
            cmds.warning("Invalid Exe File Path!")
            return

        # 설정 저장
        cmds.optionVar(stringValue=("cgxr_base_path", base_path))
        cmds.optionVar(stringValue=("cgxr_exe_path", exe_path))
        cmds.optionVar(intValue=("cgxr_voxel_res", resolution))

        self.result_base = base_path
        self.result_exe = exe_path
        self.result_res = resolution
        self.accept()

def show_dialog():
    dialog = PathConfigDialog()
    if _run_dialog(dialog):
        return dialog.result_base, dialog.result_exe, dialog.result_res
    else:
        return None, None, None