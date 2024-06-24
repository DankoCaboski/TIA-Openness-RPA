from . import OpennessService, UDTService
import os

def create_standard_structure(myproject, device):
    block = OpennessService.create_group(device, "02_Blocos Standard Axis", None)
    import_standard_bk(myproject, device, block.Blocks, file_path_STD)

dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\dependence"
directory_path_STD = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\02_Blocos Standard Axis"

def list_files_in_directory(directory_path):
    try:
        # Lista todos os arquivos no diretório fornecido
        return [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
    except Exception as e:
        print(f"Error accessing directory {directory_path}: {e}")
        return []


file_path_STD = list_files_in_directory(directory_path_STD)

def import_standard_bk(myproject, device, group, directory_path):
    print('Importing comandos standard blocks')
    
    for bk_path in directory_path:  # Agora iterando sobre a lista de arquivos
        udtsa = UDTService.list_udt_from_bk(bk_path)
        for udt in udtsa:
            udt_path = dependencies + '\\' + udt + '.xml'             
            OpennessService.import_data_type(myproject, device, udt_path)
        OpennessService.import_block(group, bk_path)




