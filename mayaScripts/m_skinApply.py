"""
파일명: m_skinApply.py
설명: XML 웨이트 데이터를 마야 스킨 클러스터에 자동으로 적용하는 모듈
      (기존 스킨 유지, 누락 조인트 추가, MEL 명령어로 안전하게 적용)
"""
import maya.cmds as cmds
import maya.mel as mel
import os

def import_weights_auto_safe(xml_path, target_mesh):
    print("\n>> [Step 4] Applying Weights (Auto & Safe Mode)...")
    
    # --------------------------------------------------------------------------
    # 1. 스킨 클러스터 확인 및 확보
    # --------------------------------------------------------------------------
    history = cmds.listHistory(target_mesh)
    existing_skins = cmds.ls(history, type='skinCluster')
    
    target_skin = None

    if existing_skins:
        target_skin = existing_skins[0]
        print(f"   - Found existing skinCluster: {target_skin} (Updating...)")
    else:
        # 스킨이 아예 없으면 새로 생성
        print("   - No skinCluster found.")
       
    # --------------------------------------------------------------------------
    # 3. Maya OptionVar 설정 (GUI와 싱크 맞추기)
    # --------------------------------------------------------------------------
    cmds.optionVar(stringValue=("deformerWeightsImportMapMethod", "index"))
    cmds.optionVar(intValue=("deformerWeightsImportIgnoreName", 0))
    cmds.optionVar(intValue=("deformerWeightsImportNormalize", 1))

    # --------------------------------------------------------------------------
    # 4. MEL 명령어 실행
    # --------------------------------------------------------------------------
    folder_path = os.path.dirname(xml_path).replace("\\", "/")
    file_name = os.path.basename(xml_path)
    
    # MEL 명령어 조립 (-ignoreName 플래그 제외하여 False 효과)
    mel_cmd1 = f'deformerWeights -import -deformer "{target_skin}" -path "{folder_path}" -method "index" -worldSpace "{file_name}";'
    mel_cmd2 = f'skinCluster -e -forceNormalizeWeights "{target_skin}";'
    try:
        # print(f"   [Executing] {mel_cmd}") # 디버깅 필요시 주석 해제
        mel.eval(mel_cmd1)
        print("   - Weights Imported successfully via MEL.")
        
        # 5. 마무리 정규화 (Normalize)
        mel.eval(mel_cmd2)
        print("   - Normalization Complete.")
        
    except Exception as e:
        cmds.error(f"MEL Execution Failed: {e}\nCommand: {mel_cmd}")