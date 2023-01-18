import pdal
import os
import json
from pdal_parallelizer import process_pipelines as process

N_WORKERS = 7
TIMEOUT = 500

with open("D:/calba/street_pointcloud_process/src/terrestre/seg_class_mobilier/files.json") as fls:
    FILES = json.load(fls)

with open(FILES['config'], 'r') as cfg:
    CONFIG = json.load(cfg)


def write_json(data):
    with open(FILES['config'], 'w') as cfg:
        json.dump(data, cfg)


def merge():
    print("\n ====== MERGING ====== \n")

    pipeline = pdal.Reader.las(filename=CONFIG["output"] + "/*.las") | pdal.Filter.merge() | pdal.Writer.las(filename=CONFIG['output'] + "/output.las",
                                        extra_dims="all", minor_version=4)
    pipeline.execute()


def add_OriginId():
    print("\n ====== ADDING ORIGIN_ID DIMENSION ====== \n")

    process(config=FILES['config'], timeout=TIMEOUT, input_type="single", tile_size=(20, 20), n_workers=N_WORKERS)

    # os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it dir -nw 5 -tpw 1")


def ground_above_ground_segmentation():
    print("\n ====== GROUND - ABOVE GROUND SEGMENTATION ====== \n")

    CONFIG['input'] = CONFIG['output']
    CONFIG['pipeline'] = FILES['seg_sol_sursol']

    write_json(CONFIG)

    process(config=FILES['config'], timeout=TIMEOUT, input_type="dir", n_workers=N_WORKERS)

    # os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it dir -nw 5 -tpw 1")


def above_ground_segmentation():
    print("\n ====== ABOVE GROUND SEGMENTATION ====== \n")

    os.system("D:/applications/CloudCompare_2_11/CloudCompare.exe -SILENT -AUTO_SAVE OFF -o -GLOBAL_SHIFT AUTO "
              + CONFIG['output'] + "/output.las -DENSITY 0.3 -TYPE KNN -C_EXPORT_FMT LAS "
                                   "-SAVE_CLOUDS FILE " + CONFIG['output'] + "/output.las")

    CONFIG['input'] = CONFIG['output'] + "/output.las"
    CONFIG['pipeline'] = FILES['seg_sursol']

    write_json(CONFIG)

    for f in os.listdir(CONFIG['output']):
        if f != "output.las":
            os.remove(os.path.join(CONFIG['output'], f))

    process(config=FILES['config'], timeout=TIMEOUT, input_type="single", tile_size=(20, 20), n_workers=N_WORKERS)

    # os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it single -ts 20 20 -nw 5 -tpw 1")

    os.remove(os.path.join(CONFIG['output'], 'output.las'))


def mobile_objects_classification():
    print("\n ====== MOBILE OBJECTS CLASSIFICATION ====== \n")

    CONFIG['input'] = CONFIG['output']
    CONFIG['pipeline'] = FILES['classification_objets_mobiles']

    write_json(CONFIG)

    process(config=FILES['config'], timeout=TIMEOUT, input_type="dir", n_workers=N_WORKERS)

    # os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it dir -nw 5 -tpw 1")


def calculate_scattering_anisotropy():
    print("\n ====== SCATTERING ANISOTROPY CALCULATION ====== \n")

    CONFIG['input'] = CONFIG['output']
    CONFIG['pipeline'] = FILES['calcul_scattering_anisotropy']

    write_json(CONFIG)

    process(config=FILES['config'], timeout=TIMEOUT, input_type="dir", n_workers=N_WORKERS)

    # os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it dir -nw 5 -tpw 1")


def above_ground_classification():
    print("\n ====== ABOVE GROUND CLASSIFICATION ====== \n")

    CONFIG['pipeline'] = FILES['classification_sursol']

    write_json(CONFIG)

    process(config=FILES['config'], timeout=TIMEOUT, input_type="dir", n_workers=N_WORKERS)

    # os.system("pdal-parallelizer process-pipelines -c " + FILES['config'] + " -it dir -nw 5 -tpw 1")


if __name__ == "__main__":
    add_OriginId()
    ground_above_ground_segmentation()
    merge()
    above_ground_segmentation()
    mobile_objects_classification()
    calculate_scattering_anisotropy()
    above_ground_classification()
    merge()
