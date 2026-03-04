import sys
import os
import importlib

# 1. 스크립트 파일들이 있는 폴더 경로
script_path = "C:/Users/user/Desktop/boyun/maya/cgxr/scripts"

# 2. 마야에게 경로 알려주기 (등록 안 되어 있으면 추가)
if script_path not in sys.path:
    sys.path.append(script_path)

# 3. 메인 모듈 불러오기 
# (파일 이름이 RunVoxelSkinning_Final.py 라고 가정)
import RunAutoSkinning as tool_module

# 4. 코드를 수정했을 때 마야를 껐다 켜지 않아도 반영되도록 Reload
importlib.reload(tool_module)

# 5. 실행 함수 호출
tool_module.run_voxel_skinning_pipeline()