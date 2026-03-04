import csv
from collections import defaultdict
import xml.etree.ElementTree as ET
import maya.cmds as cmds
import maya.api.OpenMaya as om

# -----------------------------------------------------------------------------
# 내부 헬퍼 함수들 
# -----------------------------------------------------------------------------

def get_skin_cluster(mesh, joints_list):
    """메쉬에서 스킨 클러스터 노드를 찾습니다."""
    history = cmds.listHistory(mesh)
    skin_clusters = cmds.ls(history, type="skinCluster")
    if skin_clusters:
        return skin_clusters[0]
    else:
        # 스킨이 아예 없으면 새로 생성
        print("   - No skinCluster found. Creating new one...")
        cmds.select(joints_list, r=True)
        cmds.select(mesh, add=True)
        # 기본 옵션으로 생성 (Closest joint, Linear skinning)
        target_skin = cmds.skinCluster(tsb=True, bm=0, sm=0, nw=1, n="VoxelSkinCluster")[0]
    return target_skin

def get_vertex_positions(mesh_name):
    """OpenMaya를 이용해 버텍스 월드 좌표를 가져옵니다."""
    sel_list = om.MSelectionList()
    sel_list.add(mesh_name)
    dag_path = sel_list.getDagPath(0)
    mfn_mesh = om.MFnMesh(dag_path)
    return mfn_mesh.getPoints(om.MSpace.kWorld)

def indent(elem, level=0):
    """XML 파일의 들여쓰기(Indent)를 맞춰주는 함수입니다."""
    i = "\n" + level * "  " 
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i

# -----------------------------------------------------------------------------
# 메인 변환 함수 (외부에서 호출 가능하도록 수정됨)
# -----------------------------------------------------------------------------

def run_conversion(csv_path, xml_output_path, joints_list, target_mesh_name=None):
    """
    Args:
        csv_path (str): 입력 CSV 파일 경로
        xml_output_path (str): 출력 XML 파일 경로
        target_mesh_name (str): 대상 메쉬 이름 (None일 경우 현재 선택된 메쉬 사용)
    """
    
    # 1. CSV 파일 읽기 (기존 로직 유지)
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    
    weights_data = rows[:] 
    joint_weights = defaultdict(list)
    
    for row in weights_data:
        # 빈 줄이거나 데이터가 부족한 경우 건너뛰기 (안전장치)
        if not row: continue
            
        vert_index = int(row[0])
        weights = list(map(float, row[1:]))
        total = sum(weights)
        
        # Zero division 방지 및 정규화 로직 유지
        for i, w in enumerate(row[1:]):
            weight = float(w) / total if total > 0 else 0.0
            if weight > 0.0:  # Only include non-zero weights
                joint_weights[i].append((vert_index, weight))

    # 2. 메시 선택 확인 (함수 인자로 받거나, 선택된 것 사용)
    if target_mesh_name:
        mesh = target_mesh_name
    else:
        selection = cmds.ls(selection=True)
        if not selection:
            cmds.error("스킨 메시를 먼저 선택하세요.")
        mesh = selection[0]

    # 3. 스킨 클러스터 찾기
    skin_cluster = get_skin_cluster(mesh, joints_list)
    if not skin_cluster:
        cmds.error(f"{mesh}에 스킨 클러스터가 없습니다.")

    # 4. 조인트 리스트 추출
    joint_list = cmds.skinCluster(skin_cluster, q=True, inf=True)

    # 5. 쉐이프 이름 추출
    shape_nodes = cmds.listRelatives(mesh, shapes=True)
    if not shape_nodes:
        cmds.error(f"{mesh}에 쉐이프 노드가 없습니다.")
    shape_node = shape_nodes[0]

    # 6. XML 구조 만들기
    root = ET.Element("deformerWeight")

    header = ET.SubElement(root, "headerInfo")
    # fileName 속성은 현재 저장하려는 파일 경로로 업데이트
    header.set("fileName", xml_output_path) 
    header.set("worldMatrix", "1.000000 0.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 0.000000 1.000000")

    # Vertex 좌표 가져오기
    vertex_positions = get_vertex_positions(mesh)

    # <shape> 태그 추가
    shape_elem = ET.SubElement(root, "shape")
    shape_elem.set("name", shape_node)
    shape_elem.set("group", "0")
    shape_elem.set("stride", "3")
    shape_elem.set("size", str(len(vertex_positions)))
    shape_elem.set("max", str(len(vertex_positions) - 1))

    for idx, pt in enumerate(vertex_positions):
        pt_elem = ET.SubElement(shape_elem, "point")
        pt_elem.set("index", str(idx))
        pt_elem.set("value", f"{pt.x:.6f} {pt.y:.6f} {pt.z:.6f}")

    # <weights> 태크 추가
    layer = 0
    for j, p in joint_weights.items():
        # 인덱스 범위 체크
        if j >= len(joint_list):
            print(f"[WARNING] CSV의 조인트 인덱스({j})가 Maya 스킨 클러스터의 조인트 개수({len(joint_list)})를 초과했습니다. 무시합니다.")
            continue
            
        w_elem = ET.SubElement(root, "weights")
        w_elem.set("deformer", skin_cluster)
        w_elem.set("source", joint_list[j])
        w_elem.set("shape", shape_node)
        w_elem.set("layer", str(layer))
        w_elem.set("defaultValue", "0.000")
        w_elem.set("size", str(len(p)))
        
        if p:
            max_index = max(i for i, _ in p)
            w_elem.set("max", str(max_index))
        else:
            w_elem.set("max", "0")

        for index, value in p:
            point = ET.SubElement(w_elem, "point")
            point.set("index", str(index))
            point.set("value", f"{value:.3f}")
        layer += 1

    # XML 저장
    indent(root)
    tree = ET.ElementTree(root)
    tree.write(xml_output_path, encoding='utf-8', xml_declaration=True)

    print(f"XML 저장 완료: {xml_output_path}")