import maya.cmds as cmds
import subprocess
import os
import sys
import importlib

# ==============================================================================
# [설정] 스크립트 경로 자동 감지 및 모듈 로드
# ==============================================================================
SCRIPT_DIR = os.path.dirname(__file__) if '__file__' in locals() else "C:/Users/user/Desktop/boyun/maya/cgxr/scripts"
SCRIPT_DIR = SCRIPT_DIR.replace("\\", "/")

if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

# 필요한 모듈 import
import m_extractData
import m_xmlDeformer
import m_pathGUI 
import m_skinApply # [NEW] 방금 만든 적용 모듈

# 수정 사항 즉시 반영을 위해 reload
importlib.reload(m_extractData)
importlib.reload(m_xmlDeformer)
importlib.reload(m_pathGUI)
importlib.reload(m_skinApply)

# ==============================================================================
# [Main] 전체 실행 함수
# ==============================================================================
def run_voxel_skinning_pipeline():
    print("\n" + "="*50)
    print("   [Start] Voxel Skinning Automation")
    print("="*50)

    # 1. 대상 메쉬 확인
    selection = cmds.ls(selection=True)
    if not selection:
        cmds.error("대상이 될 메쉬를 선택해주세요! (Please select a target mesh)")
        return
    target_mesh = selection[0]
    print(f">> Target Mesh: '{target_mesh}'")

    # 2. 경로 설정 (GUI)
    base_path, exe_path, res = m_pathGUI.show_dialog()
    
    if base_path is None or exe_path is None:
        print(">> Cancelled by User.")
        return 
    
    # 파일 경로 자동 생성
    hierarchy_file = os.path.join(base_path, "skeleton_hierarchy.txt")
    transform_file = os.path.join(base_path, "skeleton_transforms.txt")
    obj_file       = os.path.join(base_path, "character_mesh.obj")
    output_csv     = os.path.join(base_path, "VertexWeight.csv")
    output_xml     = "VoxelWeights.xml"
    xml_full_path  = os.path.join(base_path, output_xml)

    # [Step 1] Export
    print("\n>> [Step 1] Exporting Data...")
    try:
        ordered_joints = m_extractData.run_export(hierarchy_file, transform_file, obj_file, target_mesh)
    except Exception as e:
        cmds.error(f"Export Failed: {e}")
        return

    # [Step 2] Run C++
    print("\n>> [Step 2] Running C++ Solver...")
    if not os.path.exists(exe_path):
        cmds.error(f"Exe not found: {exe_path}")
        return
    
    args = [exe_path, str(res), hierarchy_file, transform_file, obj_file, output_csv]
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    try:
        subprocess.run(args, capture_output=True, text=True, startupinfo=si)
        print("   - Solver Finished.")
    except Exception as e:
        cmds.error(f"Solver Error: {e}")
        return

    # [Step 3] Convert XML
    print("\n>> [Step 3] Converting CSV to XML...")
    try:
        m_xmlDeformer.run_conversion(output_csv, xml_full_path, ordered_joints, target_mesh)
    except Exception as e:
        cmds.error(f"XML Convert Error: {e}")
        return

    # [Step 4] Auto Apply (모듈 호출)
    try:
        m_skinApply.import_weights_auto_safe(xml_full_path, target_mesh)
    except Exception as e:
        cmds.error(f"Applying Weights Failed: {e}")
        return
    
    print("\n" + "="*50)
    print(f"   [Success] All Done! ({target_mesh})")
    print("="*50)

if __name__ == "__main__":
    run_voxel_skinning_pipeline()