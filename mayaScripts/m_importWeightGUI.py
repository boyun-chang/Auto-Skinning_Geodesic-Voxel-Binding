"""
파일명: m_importWeightGUI.py
설명: XML 경로를 복사하고 마야의 Import Deformer Weights 옵션 창을 띄우는 모듈
"""
import maya.cmds as cmds
import maya.mel as mel
import os

def open_import_options_gui(xml_path, target_mesh):
    print("\n>> [Step 4] Opening Import GUI...")

    # 1. 플러그인 로드 확인
    if not cmds.pluginInfo('deformerWeights', q=True, loaded=True):
        try:
            cmds.loadPlugin('deformerWeights')
        except:
            pass 

    # 2. 메쉬 선택 (창이 떴을 때 적용 대상을 확실히 하기 위함)
    if cmds.objExists(target_mesh):
        cmds.select(target_mesh, r=True)
        print(f"   - Selected mesh: {target_mesh}")
    else:
        cmds.warning(f"Mesh '{target_mesh}' not found. Please select it manually.")

    # 3. XML 파일 경로 클립보드 복사 (Ctrl+V 편의 기능)
    #    (윈도우 경로인 역슬래시 \로 바꿔야 탐색기에서 잘 인식됨)
    clean_path = xml_path.replace("/", "\\")
    os.system(f'echo {clean_path}| clip') 
    print(f"   - XML Path copied to clipboard! (Press Ctrl+V in the filename field)")
    print(f"   - File: {clean_path}")

    # 4. Maya GUI 창 실행
    try:
        # 올바른 명령어: ImportDeformerWeightsOptions
        mel.eval("ImportDeformerWeightsOptions")
        print("   - GUI Window Opened. Please set options and click 'Import'.")
    except Exception as e:
        print(f"   [Warning] Standard command failed. Trying fallback...")
        try:
            # 강제로 UI 스크립트 로드 시도
            mel.eval("source \"performDeformerWeightsImport.mel\"")
            mel.eval("ImportDeformerWeightsOptions")
        except Exception as e2:
            cmds.error(f"GUI 창을 여는 데 실패했습니다: {e2}")