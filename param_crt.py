import os
from iccr import Collision
import pandas as pd

def create_params(file_name, param_template, output_path, ic_path):
    dirName = "params_temp"
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")
    save_param = os.path.join(dirName, file_name)
    op_path_template = "__output__path__"
    ic_path_template = "__ic__path__"
    with open(param_template, 'r', encoding='utf-8') as param:
        content = param.read()
    with open(save_param, 'w', encoding='utf-8') as file:
        new_content = content.replace(op_path_template, output_path)
        new_content = new_content.replace(ic_path_template, ic_path)
        file.write(new_content)
        file.close()
        param.close()

def create_ics(data_csv_file, galaxy_file1, galaxy_file2):
    """
    usar ICCR como biblioteca ou como subprocesso ?
    usar open_coord_csv para pegar as coordenadas do arquivo do queorbita
    """
    dirName = "ics_temp"
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")

    data_ic = data_csv_file
    _collision = Collision(galaxy_file1, galaxy_file2)
    _collision.create_file()
    _collision.initial_condition_file(pericenter=0, orbit=data_ic)

def open_coord_csv(csv_file):
    pd.open_csv(csv_file)
    #pegar dados do csv
    # cubo [[galaxy1_coords, galaxy2_coords, galaxy1_vels, galaxy2_vels],[..],...]
    return  #retorna array com todas [coord, vel]

def make_chain(csv_file, galaxy_file1, galaxy_file2):
    for data in open_coord_csv(csv_file):
        create_ics(data, galaxy_file1, galaxy_file2)
        create_params(...)

    return None
create_params("teste", "param_template.txt", "../teste", "../ic_teste")
