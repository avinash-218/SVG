import json
import xml.etree.ElementTree as ET
import os
import shutil

input_dir = 'Jsons'
output_dir = 'SVGs'

if(os.path.exists(output_dir)):
    shutil.rmtree(output_dir)
os.mkdir(output_dir)

def create_svg(data, output_file_path):
    svg_root = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width='1920', height='1080')   #create root svg

    for fur in data['model']['furnitures']: # create bbox for furnitures
        bbox = fur['bounding_box_points']
        width = str((bbox['finalX'] - bbox['initialX'])/2.0)
        height = str((bbox['finalY'] - bbox['initialY'])/2.0)
        
        ET.SubElement(svg_root, "rect", x=str(fur['centre_x']), y=str(-fur['centre_y']), width=width, height=height, id=fur['object_id'], **{"class": fur['category_type']})

    for wall in data['model']['structure']: #create polygon for walls
        vertices = wall['vertices']
        polygon_points = " ".join([f"{coord['x_coord']},{coord['y_coord']}" for coord in vertices])
        ET.SubElement(svg_root, "polygon", points=polygon_points, fill="orange", id=wall['object_id'], **{"class": "wall"})

    tree = ET.ElementTree(svg_root)

    with open(output_file_path, "wb") as f:
        tree.write(f)

for file in os.listdir(input_dir):
    input_file_path = os.path.join(input_dir, file)
    output_file_path = os.path.join(output_dir, file.split('.')[0] + '.svg')

    with open(input_file_path, 'r') as file:
        data = json.load(file)

    create_svg(data, output_file_path)