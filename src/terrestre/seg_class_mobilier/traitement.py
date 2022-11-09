import numpy
import pdal
import os
import json

with open("D:\calba\street_pointcloud_process\src\terrestre\seg_class_mobilier\files.json") as fls:
    FILES = json.load(fls)


with open("D:/calba/street_pointcloud_process/src/terrestre/seg_class_mobilier/config.json") as cfg:
    CONFIG = json.load(cfg)


def merge():
    pipeline = pdal.Reader.las(filename=CONFIG["output"] + "/*.las") | pdal.Filter.merge() | pdal.Filter.sample(
        radius=0.001) | pdal.Writer.las(filename=CONFIG['output'] + "/output.las",
                                        extra_dims="all", minor_version=4)
    pipeline.execute()


def add_OriginId():
    os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it dir -nw 3 -tpw 1")


def ground_above_ground_segmentation():
    CONFIG['input'] = CONFIG['output']
    CONFIG['pipeline'] = FILES['seg_sol_sursol']

    os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it dir -nw 3 -tpw 1")


def above_ground_segmentation():
    os.system("D:/applications/CloudCompare_2_11/CloudCompare.exe -SILENT -AUTO_SAVE OFF -o "
              + CONFIG['output'] + "/output.las -DENSITY 0.3 -TYPE KNN -C_EXPORT_FMT LAS "
              "-SAVE_CLOUDS FILE " + CONFIG['output'] + "/output.las")

    CONFIG['input'] = CONFIG['output'] + "/output.las"
    CONFIG['pipeline'] = FILES['seg_sursol']

    os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it single -ts 1000 1000 -nw 3 -tpw 1")


def mobile_objects_classification():
    CONFIG['input'] = CONFIG['output']
    CONFIG['pipeline'] = FILES['classification_objets_mobiles']

    os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it dir -nw 3 -tpw 1")


def calculate_scattering_anisotropy():
    CONFIG['pipeline'] = FILES['calcul_scattering_anisotropy']

    os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it dir -nw 3 -tpw 1")


def above_ground_classification():
    CONFIG['pipeline'] = FILES['classification_sursol']

    os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it dir -nw 3 -tpw 1")


if __name__ == "__main__":
    add_OriginId()
    ground_above_ground_segmentation()
    merge()
    above_ground_segmentation()
    mobile_objects_classification()
    calculate_scattering_anisotropy()
    above_ground_classification()
    merge()
