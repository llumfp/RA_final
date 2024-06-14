import csv
import xml.etree.ElementTree as ET

def main(xml_file,csv_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find all Conf elements
    conf_elements = root.findall(".//Conf")

    # Open CSV file for writing
    with open(csv_file, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write components to CSV file
        for conf in conf_elements:
            components = conf.text.strip().replace("[", "").replace("]", "").replace("'", "").split()
            components_str = ', '.join(components[:6])
            csvwriter.writerow(components_str.split(', ')[:6])

xml_file = 'taskfile_tampconfig_chess_1_simple.xml'
csv_file = 'taskfile_tampconfig_chess_1_simple.csv'

main(xml_file,csv_file)