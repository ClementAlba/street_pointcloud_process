import numpy
import pdal
import os
import json

with open("D:/calba/street_pointcloud_process/src/terrestre/seg_class_mobilier/config.json") as cfg:
    CONFIG = json.load(cfg)


def merge():
    pipeline = pdal.Reader.las(filename=CONFIG["output"] + "/*.las") | pdal.Filter.merge() | pdal.Filter.sample(
        radius=0.001) | pdal.Writer.las(filename="D:/data_dev/street_pointcloud_process/output/output.las",
                                        extra_dims="all", minor_version=4)
    pipeline.execute()


def add_OriginId():
    os.system("pdal-parallelizer process-pipelines -c "
              "D:/calba/street_pointcloud_process/src/terrestre/seg_class_mobilier/config.json -it dir -nw 3 -tpw 1")


def ground_above_ground_segmentation():
    os.system("pdal-parallelizer process-pipelines -c "
              "D:/calba/street_pointcloud_process/src/terrestre/seg_class_mobilier/config_output.json -it dir -nw 3 "
              "-tpw 1")


def above_ground_segmentation():
    os.system("D:/applications/CloudCompare_2_11/CloudCompare.exe -SILENT -AUTO_SAVE OFF -o "
              "D:/data_dev/street_pointcloud_process/output/output.las -DENSITY 0.3 -TYPE KNN -C_EXPORT_FMT LAS "
              "-SAVE_CLOUDS FILE D:/data_dev/street_pointcloud_process/output/output.las")

    os.system("pdal-parallelizer process-pipelines -c "
              "D:/calba/street_pointcloud_process/src/terrestre/seg_class_mobilier/config_sursol.json -it single -ts "
              "1000 1000 -nw 3 -tpw 1")


def mobile_objects_classification():
    os.system("pdal-parallelizer process-pipelines -c "
              "D:/calba/street_pointcloud_process/src/terrestre/seg_class_mobilier/config_obj_mobiles.json -it dir "
              "-nw 3 -tpw 1")


def calculate_scattering_anisotropy():
    os.system("pdal-parallelizer process-pipelines -c "
              "D:/calba/street_pointcloud_process/src/terrestre/seg_class_mobilier/config_anisotropy.json -it dir -nw"
              " 3 -tpw 1")


def above_ground_classification():
    os.system("pdal-parallelizer process-pipelines -c "
              "D:/calba/street_pointcloud_process/src/terrestre/seg_class_mobilier/config_class_sursol.json -it dir "
              "-nw 3 -tpw 1")


if __name__ == "__main__":
    # add_OriginId()
    # ground_above_ground_segmentation()
    # merge()
    # above_ground_segmentation()
    # mobile_objects_classification()
    # calculate_scattering_anisotropy()
    # above_ground_classification()
    merge()
