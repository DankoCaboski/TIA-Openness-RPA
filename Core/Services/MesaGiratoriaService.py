from . import OpennessService, UDTService
import os

# Definição de diretórios de dependências e caminhos para os diretórios dos blocos
dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\dependence"
directory_path_CMD = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\move_table"

# Diretórios para os lados A, B, C e D
directory_path_A = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\move_table\Lado A"
directory_path_B = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\move_table\Lado B"
directory_path_C = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\move_table\Lado C"
directory_path_D = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\move_table\Lado D"

# Função principal para criar a estrutura das mesas baseada no valor de mg_blocks_value
def create_mesa_structure(myproject, device, mesa_name, mesa_type, mg_blocks_value):
    group_name = mesa_name + '_group'
    mesa_group = OpennessService.create_group(device, group_name, "03_Blocos Operacionais")

    cmd_name = 'Comando Mesa'
    cmd_name_group = OpennessService.create_group(device, cmd_name, group_name)
    import_mesa_bk(myproject, device, cmd_name_group.Blocks, mesa_type, file_paths_CMD)

    mesas = {
        1: ('Mesa A', directory_path_A, list_files_in_directory(directory_path_A), import_mesa),
        2: ('Mesa B', directory_path_B, list_files_in_directory(directory_path_B), import_mesa),
        3: ('Mesa C', directory_path_C, list_files_in_directory(directory_path_C), import_mesa),
        4: ('Mesa D', directory_path_D, list_files_in_directory(directory_path_D), import_mesa)
    }

    for i in range(1, mg_blocks_value + 1):
        if i in mesas:
            mesa_name, directory_path, file_paths, import_function = mesas[i]
            mesa_group = OpennessService.create_group(device, mesa_name, group_name)
            import_function(myproject, device, mesa_group.Blocks, mesa_type, file_paths)

# Função para listar arquivos nos diretórios especificados
def list_files_in_directory(directory_path):
    try:
        return [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
    except Exception as e:
        print(f"Error accessing directory {directory_path}: {e}")
        return []

# Funções de importação para blocos de comando e mesas
def import_mesa_bk(myproject, device, mesa_group, mesa_type: str, file_paths):
    for bk_path in file_paths:
        udtsa = UDTService.list_udt_from_bk(bk_path)
        for udt in udtsa:
            udt_path = dependencies + '\\' + udt + '.xml'
            OpennessService.import_data_type(myproject, device, udt_path)
        OpennessService.import_block(mesa_group, bk_path)

def import_mesa(myproject, device, mesa_group, mesa_type: str, file_paths):
    mesa_type = mesa_type.upper()
    for bk_path in file_paths:
        udtsa = UDTService.list_udt_from_bk(bk_path)
        for udt in udtsa:
            udt_path = dependencies + '\\' + udt + '.xml'
            OpennessService.import_data_type(myproject, device, udt_path)
        OpennessService.import_block(mesa_group, bk_path)

# Lista de caminhos para arquivos de blocos
file_paths_CMD = list_files_in_directory(directory_path_CMD)
