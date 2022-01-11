import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm


def convert_all_xml_path():
    os.chdir(os.path.join(os.getcwd(), 'Project3_final', 'group1_8'))
    os.makedirs("Annotations/update_path", exist_ok=True)
    xml_path = os.path.join(os.getcwd(), 'Annotations')
    for xml_file in tqdm(glob.glob(xml_path + '/*.xml')):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        path = root.find('path')
        img_new_path = os.path.join(
            os.getcwd(), 'Images', xml_file[-17:-4] + '.jpg',)
        path.text = img_new_path
        tree.write(f'Annotations/update_path/{xml_file[-17:]}')


def test1():
    os.chdir(os.path.join(os.getcwd(), 'Project3_final', 'Touch_Ground'))
    os.makedirs("update_path", exist_ok=True)
    xml_file = os.path.join(os.getcwd(), 'group01_00389.xml')
    print(xml_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    path = root.find('path')
    path.text = 'abscd'
    tree.write('update_path/group01_00389.xml')


if __name__ == '__main__':
    convert_all_xml_path()
