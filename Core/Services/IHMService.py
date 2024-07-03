from . import OpennessService
from . import UDTService
import os
dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\dependence"

def create_IHM_structure(myproject, device):
    o1Sistemas =  '01_Sistemas'
    system_group = OpennessService.create_folder(device, o1Sistemas, None).Screens
    group_name_celula =  '01.2_Célula'
    Celula_group = OpennessService.create_folder(device, group_name_celula, o1Sistemas).Screens
    group_name_prod_temp =  '1.2.1Produção e Tempo de Ciclo'
    prod_group = OpennessService.create_folder(device, group_name_prod_temp, group_name_celula).Screens
    group_name_alarm =  '01.3_Alarmes'
    alarm_group = OpennessService.create_folder(device, group_name_alarm, o1Sistemas).Screens
    import_template(device)
    import_Screens(system_group, 'sistema')
    import_Screens(prod_group, 'prod')
    import_Screens(alarm_group, 'alarm')

def import_Screens(group, screen_type):
    screen_paths = {
        'sistema': r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Screens\01_Sistema",
        'prod': r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Screens\Produção e tempo ciclo",
        'alarm': r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Screens\Alarm"
    }
    
    if screen_type in screen_paths:
        Screen_bk_path = screen_paths[screen_type]
        arquivos_xml = [f for f in os.listdir(Screen_bk_path) if f.endswith('.xml')]
        for arquivo in arquivos_xml:
            arquivo_caminho_completo = OpennessService.get_file_info(os.path.join(Screen_bk_path, arquivo))
            import_options = OpennessService.tia.ImportOptions.Override
            group.Import(arquivo_caminho_completo, import_options)
    else:
        raise ValueError(f"Tipo de tela '{screen_type}' não é válido. Use 'sistema', 'prod' ou 'alarm'.")

def import_template(device):
    template = device.ScreenTemplateFolder.ScreenTemplates
    Screen_bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Template"
    arquivos_xml = [f for f in os.listdir(Screen_bk_path) if f.endswith('.xml')]
    for arquivo in arquivos_xml:
        arquivo_caminho_completo = OpennessService.get_file_info(os.path.join(Screen_bk_path, arquivo))
        import_options = OpennessService.tia.ImportOptions.Override
        importTemplate = template.Import(arquivo_caminho_completo, import_options)

    