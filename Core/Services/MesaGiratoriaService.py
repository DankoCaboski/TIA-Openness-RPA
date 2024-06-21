from . import OpennessService, UDTService
import os
from Controller import LanguageController

def create_mesa_structure(myproject, device, mesa_name, mesa_type):
    group_name = mesa_name + '_group' 
    mesa_group = OpennessService.create_group(device, group_name, None)
    import_mesa_bk(myproject, device, mesa_group.Blocks, mesa_type, file_paths)

directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\move_table"

def list_files_in_directory(directory_path):
    try:
        # Lista todos os arquivos no diretório fornecido
        return [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
    except Exception as e:
        print(f"Error accessing directory {directory_path}: {e}")
        return []


file_paths = list_files_in_directory(directory_path)
print(file_paths)

def import_mesa_bk(myproject, device, mesa_group, mesa_type: str, file_paths):
    mesa_type = mesa_type.upper()
    if mesa_type == 'ABB':
        print('Importing ABB mesa blocks')
        dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\robots\bk_dp"
        LanguageController.add_language(myproject, "pt-BR")
        for bk_path in file_paths:  # Agora iterando sobre a lista de arquivos
            print(f'Importing block from {bk_path}')
            udtsa = UDTService.list_udt_from_bk(bk_path)
            for udt in udtsa:
                udt_path = dependencies + '\\' + udt + '.xml'             
                OpennessService.import_data_type(myproject, device, udt_path)
            OpennessService.import_block(mesa_group, bk_path)
    elif mesa_type == 'FANUC':
        print('Importing FANUC mesa blocks')
        for bk_path in file_paths:  # Usando a lista de arquivos para FANUC também
            print(f'Importing block from {bk_path}')
            OpennessService.import_data_type(myproject, device, udt_path)
        OpennessService.import_block(mesa_group, bk_path)
            
