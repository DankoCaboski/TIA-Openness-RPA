from . import OpennessService, UDTService
import os
 
def create_mesa_structure(myproject, device, mesa_name, mesa_type):

    group_name = mesa_name + '_group' 
    mesa_group = OpennessService.create_group(device, group_name, "03_Blocos Operacionais")

    cmd_name = 'Comando Mesa'
    cmd_name_group = OpennessService.create_group(device, cmd_name, group_name)

    mesaA_name = 'Mesa A'
    mesa_groupA = OpennessService.create_group(device, mesaA_name, group_name)

    produto1_mesa_A_name = 'Produto 1'
    produto1_mesa_A = OpennessService.create_group(device, produto1_mesa_A_name, mesaA_name)

    import_mesa_bk(myproject, device, cmd_name_group.Blocks, mesa_type, file_paths_CMD)
    import_mesa_A(myproject, device, mesa_groupA.Blocks, mesa_type, file_paths_A)
    import_mesa_A_prod(myproject, device, produto1_mesa_A.Blocks, mesa_type, file_paths_A_prod1)

dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\dependence"
directory_path_CMD = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\move_table"
directory_path_A = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\move_table\Lado A"
directory_path_A_prod1 = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\move_table\Lado A\Produto 1"

def list_files_in_directory(directory_path):
    try:
        # Lista todos os arquivos no diretório fornecido
        return [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
    except Exception as e:
        print(f"Error accessing directory {directory_path}: {e}")
        return []


file_paths_CMD = list_files_in_directory(directory_path_CMD)
file_paths_A = list_files_in_directory(directory_path_A)
file_paths_A_prod1 = list_files_in_directory(directory_path_A_prod1)

def import_mesa_bk(myproject, device, mesa_group, mesa_type: str, file_paths_CMD):
    mesa_type = mesa_type.upper()
    if mesa_type == '':
        print('Importing comandos mesa blocks')
        for bk_path in file_paths_CMD:  # Agora iterando sobre a lista de arquivos
            udtsa = UDTService.list_udt_from_bk(bk_path)
            for udt in udtsa:
                udt_path = dependencies + '\\' + udt + '.xml'             
                OpennessService.import_data_type(myproject, device, udt_path)
            OpennessService.import_block(mesa_group, bk_path)
    elif mesa_type == 'FANUC':
        print('Importing FANUC mesa blocks')
        for bk_path in file_paths_CMD:  # Usando a lista de arquivos para FANUC também
            print(f'Importing block from {bk_path}')
            OpennessService.import_data_type(myproject, device, udt_path)
        OpennessService.import_block(mesa_group, bk_path)

def import_mesa_A(myproject, device, mesa_group, mesa_type: str, file_paths):
    mesa_type = mesa_type.upper()
    if mesa_type == '':
        print('Importing mesa A blocks')
        for bk_path in file_paths:  # Agora iterando sobre a lista de arquivos
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

def import_mesa_A_prod(myproject, device, mesa_group, mesa_type: str, file_paths):
    mesa_type = mesa_type.upper()
    if mesa_type == '':
        print('Importing mesa A produto blocks')
        
        for bk_path in file_paths:  # Agora iterando sobre a lista de arquivos
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

