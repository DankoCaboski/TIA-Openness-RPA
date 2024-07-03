from . import OpennessService
from . import UDTService
import os
dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\dependence"

def create_IHM_structure(myproject, device):
    group_name =  '01_Sistemas'
    system_group = OpennessService.create_folder(device, group_name, None).Screens
    import_template(device)
    import_Screen_bk(system_group)

def import_Screen_bk(system_group):
    Screen_bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Screens"
    arquivos_xml = [f for f in os.listdir(Screen_bk_path) if f.endswith('.xml')]
    for arquivo in arquivos_xml:
        arquivo_caminho_completo = OpennessService.get_file_info(os.path.join(Screen_bk_path, arquivo))
        import_options = OpennessService.tia.ImportOptions.Override
        ScreensSystem = system_group.Import(arquivo_caminho_completo, import_options)
       

def import_template(device):
    template = device.ScreenTemplateFolder.ScreenTemplates
    Screen_bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Template"
    arquivos_xml = [f for f in os.listdir(Screen_bk_path) if f.endswith('.xml')]
    for arquivo in arquivos_xml:
        arquivo_caminho_completo = OpennessService.get_file_info(os.path.join(Screen_bk_path, arquivo))
        import_options = OpennessService.tia.ImportOptions.Override
        importTemplate = template.Import(arquivo_caminho_completo, import_options)

    