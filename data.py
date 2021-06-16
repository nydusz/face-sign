import codecs
import csv
import glob
import os
import re


def get_Write_file_infos():
    file_infos_list = []
    os.chdir(r"D:/Project/face-recognition/face_dataset")
    for file_name in glob.glob("*.jpg"):
        file_name = file_name.split('.')[0]
        file_infos_list.append(file_name)
    return file_infos_list


def write_csv(file_infos_list):
    with open('D:/Project/face-recognition/wf.csv', "w", newline='', encoding='utf-8-sig') as csv_file:
        headers = ['姓名']
        wt = csv.DictWriter(csv_file, fieldnames=headers)
        wt.writeheader()
        writer = csv.writer(csv_file)
        for row in file_infos_list:
            if row != '':
                writer.writerow([row])


def main():
    file_infos_list = get_Write_file_infos()
    write_csv(file_infos_list)


if __name__ == '__main__':
    main()
