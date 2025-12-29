import os
import pandas as pd

def create_params(file_name, output_path, ic_path):
    dirName = "params_temp"
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")
    save_param = os.path.join(dirName, file_name)
    op_path_template = "__output__path__"
    ic_path_template = "__ic__path__"
    with open("param_template.txt", 'r', encoding='utf-8') as param:
        content = param.read()
    with open(save_param, 'w', encoding='utf-8') as file:
        new_content = content.replace(op_path_template, output_path)
        new_content = new_content.replace(ic_path_template, ic_path)
        file.write(new_content)
        file.close()
        param.close()

def create_config():
    dirName = "config_temp"
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")

    j = 0
    try:
        for i in sorted(os.listdir('orbits_temp/')):
            fname = i
            if fname != '.ipynb_checkpoints':
                orb = pd.read_csv(f'orbits_temp/{fname}', sep="\t")
                data_initial = orb.loc[0]
                config_template = "config_template.ini"
                file_name = f"config_{j}.ini"
                save_configs = os.path.join(dirName, file_name)
                data = [data_initial.x_kepl, data_initial.y_kepl, data_initial.z_kepl,
                        data_initial.Vx_kepl, data_initial.Vy_kepl, data_initial.Vz_kepl] #dados do queorbita
                replacements = {"__g1cx__":data[0] , "__g1cy__":data[1],"__g1cz__":data[2],
                                "__g1vx__":data[3], "__g1vy__":data[4],"__g1vz__":data[5]}

                with open(config_template, 'r', encoding='utf-8') as param:
                    content = param.read()
                with open(save_configs, 'w', encoding='utf-8') as file:
                    for template_data_, data_ in replacements.items():
                        content = content.replace(template_data_, str(data_))
                    file.write(content)
                    file.close()
                    param.close()
                j += 1
    except Exception as e:
        print(f"Drop orbits_temp directory in the directory: {e}")
    return 0

def run_iccr():
    dirName = "ic"
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")
    counter_name=0
    try:
        for configs_ in sorted(os.listdir('config_temp/')):
            fname = configs_
            if fname != '.ipynb_checkpoints':
                os.system(f'collision config_temp/{fname}')
                os.rename("collision_file.hdf5", f"collision_orb_{counter_name}.hdf5")
                os.system(f"cp collision_orb_{counter_name}.hdf5 ic/")
                os.system(f"rm collision_orb_{counter_name}.hdf5")
                create_params(f"param_{counter_name}.txt", f"../outputs/collision_orb_{counter_name}/",f"ic/collision_orb_{counter_name}")
            counter_name += 1
    except Exception as e:
        print(f"Verify ICCR code: {e}")
    return 0
create_config()
run_iccr()
