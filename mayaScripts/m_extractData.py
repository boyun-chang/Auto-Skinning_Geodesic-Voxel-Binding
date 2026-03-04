"""
설명: 마야 씬에서 스켈레톤 정보와 메쉬를 추출하여 파일로 저장하는 모듈
"""
import maya.cmds as cmds
import maya.api.OpenMaya as om

def get_sorted_joints_hierarchy():
    """아웃라이너 순서대로 정렬된 조인트 리스트 반환"""
    all_joints = cmds.ls(type='joint', long=True)
    if not all_joints: return []
    
    # 최상위 루트 찾기
    roots = [j for j in all_joints if not cmds.listRelatives(j, parent=True, type='joint')]
    
    ordered_joints = []
    def traverse(node):
        ordered_joints.append(node)
        children = cmds.listRelatives(node, children=True, type='joint', fullPath=True) or []
        for child in children: traverse(child)
        
    for root in roots: traverse(root)
    return ordered_joints

def export_hierarchy(filename, joints_list):
    """[Index] [ParentIndex] [Name] 형식으로 저장"""
    joint_to_index = {name: i for i, name in enumerate(joints_list)}
    
    with open(filename, 'w') as f:
        for i, joint in enumerate(joints_list):
            parent = cmds.listRelatives(joint, parent=True, type='joint', fullPath=True)
            p_idx = joint_to_index[parent[0]] if (parent and parent[0] in joint_to_index) else -1
            short_name = joint.split('|')[-1]
            f.write(f"{i} {p_idx} {short_name}\n")
    print(f">> Saved Hierarchy: {filename}")

def export_transforms(filename, joints_list):
    """[Name] [Position] 형식으로 저장"""
    with open(filename, 'w') as f:
        for joint in joints_list:
            mat = cmds.xform(joint, q=True, ws=True, m=True)
            pos = om.MTransformationMatrix(om.MMatrix(mat)).translation(om.MSpace.kWorld)
            short_name = joint.split('|')[-1]
            f.write(f"{short_name} {pos}\n")
    print(f">> Saved Transforms: {filename}")

def export_obj(filename, target_mesh):
    """지정된 메쉬를 OBJ로 깨끗하게 내보내기"""
    if not cmds.pluginInfo('objExport', q=True, loaded=True):
        cmds.loadPlugin('objExport')
        
    if not cmds.objExists(target_mesh):
        cmds.error(f"Mesh '{target_mesh}' not found!")
        return False
        
    # 현재 선택 백업
    sel = cmds.ls(sl=True)
    
    cmds.select(target_mesh, r=True)
    # 옵션: 그룹X, 재질X, 노멀O, 스무딩O
    options = "groups=0;ptgroups=0;materials=0;smoothing=1;normals=1"
    cmds.file(filename, force=True, options=options, type="OBJexport", pr=True, es=True)
    
    # 선택 복구
    if sel: cmds.select(sel, r=True)
    else: cmds.select(cl=True)
    
    print(f">> Saved OBJ: {filename}")
    return True

def run_export(hierarchy_path, transform_path, obj_path, target_mesh):
    """전체 추출 과정 실행 함수"""
    ordered_joints = get_sorted_joints_hierarchy()
    
    export_hierarchy(hierarchy_path, ordered_joints)
    export_transforms(transform_path, ordered_joints)
    success = export_obj(obj_path, target_mesh)
    
    return ordered_joints if success else None