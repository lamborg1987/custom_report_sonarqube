import zipfile
import os
import shutil
from getcredentials import getstm


def compress():
    """compress all reports"""
    directories = ["BUG", "VULNERABILITY", "CODE_SMELL"]
    csv_file = "full-report_" + getstm() + ".csv"

    zip_file_name = "ALL_reports_" + getstm() + ".zip"

    with zipfile.ZipFile(zip_file_name, "w") as zip_file:
        for directory in directories:
            for root, dirs, files in os.walk(directory):
                print(dirs)
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=directory)
                    zip_file.write(file_path, arcname=arcname)

        zip_file.write(csv_file)

    print(f'File comprees "{zip_file_name}"')

    for directory in directories:
        shutil.rmtree(directory)

    for file in [csv_file]:
        os.remove(file)
