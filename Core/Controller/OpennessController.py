from Services import OpennessService
from . import RobotController
from . import MesaGiratoriaController
from . import StandardAxisController
from Controller import LanguageController
import traceback
from System.IO import FileInfo # type: ignore
from System import String # type: ignore
import tkinter as tk

RPA_status = "Idle"
hardwareList = []
redes = []
hardwareListRemota = []
myproject = None

def create_project(project_path, project_name, hardware, rb_blocks_value, mg_blocks_value, selec_blocks_value):
    
    try:
        
        global RPA_status
        RPA_status = 'Starting TIA UI'
        print(RPA_status)
        
        mytia = OpennessService.open_tia_ui()

        #Creating new project
        RPA_status = 'Creating project'
        print(RPA_status)
        
        global myproject
        myproject = OpennessService.create_project(mytia, project_path, project_name)
        LanguageController.add_language(myproject, "pt-BR")
        if hardware != None and myproject != None:
            addHardware(hardware)
            wire_profinet()
            redes.append(create_IO_System())
            connect_IO_System(hardware, redes)
            addIORemota(hardware)
            import_libraries(mytia)
            myproject.Save()
        
        for device in hardware:    
            deviceName = device["Name"]
            deviceType = device["HardwareType"]
            if deviceType == "CONTROLLERS":
                device = OpennessService.get_device_by_name(myproject, deviceName)
                OpennessService.create_group(device, "01_Sistema", None)

                StandardAxisController.create_standard_structure(myproject, device)

                OpennessService.create_group(device, "03_Blocos Operacionais", None)
                OpennessService.create_group(device, "04_Safety", None)

                if rb_blocks_value > 0 : 
                    for device in hardware:
                        deviceName = device["Name"]
                        device = OpennessService.get_device_by_name(myproject, deviceName)
                        RobotController.create_robot_structure(myproject, device, "nome_robo", "abb")
                        
                        # tipo = 'robo'
                        # import_block = OpennessService.verify_and_import(myproject, deviceName, r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\db_falhas.xml", repetitions= rb_blocks_value, tipo = tipo)
                        # print(import_block)

                if mg_blocks_value > 0:
                    for device in hardware:
                        deviceName = device["Name"]
                        device = OpennessService.get_device_by_name(myproject, deviceName)
                        MesaGiratoriaController.create_mesa_structure(myproject, device, "Mesa Giratória", "", mg_blocks_value)
        
        # if selec_blocks_value > 0:
        #     for device in hardware:
        #         deviceName = device["Name"]
        #         import_block = OpennessService.verify_and_import(myproject, deviceName, dir_block, repetitions=mg_blocks_value, tipo= '')
        #         print(import_block)

        myproject.Save()
        redes.clear()
        RPA_status = 'Project created successfully!'
        print(RPA_status)
        
        return True

    except Exception as e:
        RPA_status = f'Error: {e}'
        print(RPA_status)
        return False
    
 
def addHardware(hardware):
    deviceName = ''
    deviceMlfb = ''

    plc_count = 0
    for device in hardware:
        deviceName = device["Name"]
        deviceMlfb = device["Mlfb"]
        deviceType = device["HardwareType"]
        deviceVersion = device["Firm_Version"]
        Start_Adress = device ["Start_Adress"]
        
        if deviceType == "CONTROLLERS":
            plc_count += 1
        hardwareList.append(OpennessService.addHardware(deviceType, deviceName, deviceMlfb, myproject,deviceVersion, plc_count, Start_Adress))

def addIORemota(hardware):
    deviceName = ''
    deviceMlfb = ''

    remot_count = 0
    for device in hardware:
        deviceName = device["Name"]
        deviceMlfb = device["Mlfb"]
        deviceType = device["HardwareType"]
        deviceVersion = device["Firm_Version"]
        Start_Adress = device ["Start_Adress"]
        
        if deviceType == "REMOTAS":
            remot_count += 1
        if remot_count > 0:
            hardwareListRemota.append(OpennessService.addIORemota(deviceType, deviceName, deviceMlfb, myproject,deviceVersion, Start_Adress, remot_count ))
    
def wire_profinet():
    global RPA_status
    
    ProfinetInterfaces = OpennessService.GetAllProfinetInterfaces(myproject)
    RPA_status = "Nº de interfaces PROFINET :" + str(len(ProfinetInterfaces))
    print(RPA_status)
    
    if len(ProfinetInterfaces) > 1:
        mysubnet = OpennessService.SetSubnetName(myproject)
        for port in ProfinetInterfaces:
            node = port.Nodes[0]
            OpennessService.ConnectToSubnet(node, mysubnet)
        
        RPA_status = "Rede PROFINET configurada com sucesso!"
        print(RPA_status)
        
    else:
        RPA_status = "Número de interfaces PROFINET menor que 2"
        print(RPA_status)

def create_IO_System():
    Device = myproject.Devices[0]
    count = myproject.UngroupedDevicesGroup.Devices.Count
    if count >= 1:
        networkIterface = OpennessService.get_network_interface_CPU(Device)
        redeIO = networkIterface.IoControllers[0]
        nomerede = "PROFINET IO-System"
        rede = redeIO.CreateIoSystem(nomerede)
        RPA_status = "Rede IO Criada"
        print(RPA_status)
        return rede
    

def connect_IO_System(hardware, redes):
    for rede in redes:  # Loop para cada rede na lista de redes
        for device in hardware:
            deviceType = device["HardwareType"]
            if deviceType == "REMOTAS":
                Devices = myproject.UngroupedDevicesGroup.Devices  # Referenciando a lista de dispositivos
                for i, Device in enumerate(Devices):
                    networkInterface = OpennessService.get_network_interface_REMOTAS(Device)
                    Io_System = networkInterface.IoConnectors[0]
                    if Io_System.GetAttribute("ConnectedToIoSystem") == "" or Io_System.GetAttribute("ConnectedToIoSystem") == None:  # Verifica se o Io_System não está conectado
                        connect = Io_System.ConnectToIoSystem(rede)  # Usando a rede atual do loop externo  
def open_project(project_path):
    global RPA_status
    RPA_status = 'Opening project'
    print(RPA_status)
    try:
        global myproject
        myproject = OpennessService.open_project(project_path)
        # device = OpennessService.get_device_by_index(myproject, 0)
        # OpennessService.create_group(device, 'E', 'G')
        RPA_status = 'Project opened successfully!'
        print(RPA_status)
        
    except Exception as e:
        RPA_status = f'Error opening project: {e}\n{traceback.format_exc()}'
        print(RPA_status)
        return

def export_block(device, block_name : str, block_path : str):
    try:
        if device == None:
            device = OpennessService.get_device_by_index(myproject, 0)
            
        status = OpennessService.export_block(device, block_name, block_path)
        if status:
            RPA_status = 'Block exported successfully!'
            print(RPA_status)
        else:
            RPA_status = 'Error exporting block'
            print(RPA_status)
            
    except Exception as e:
        RPA_status = 'Error exporting block: ', e
        print('Error exporting block: ', e)
        return
    
def export_data_type(device, data_type_name : str, data_type_path : str):
    global RPA_status
    RPA_status = 'Exporting data type'
    print(RPA_status)
    
    try:
        if device == None:
            device = OpennessService.get_device_by_index(myproject, 0)
        
        if not OpennessService.is_gsd(device):
            result = OpennessService.export_data_type(device, data_type_name, data_type_path)
            if result:
                RPA_status = 'Data type exported successfully!'
                print(RPA_status)
            else:
                RPA_status = 'Error exporting data type'
                print(RPA_status)
                
    except Exception as e:
        RPA_status = 'Error exporting data type while in controller: ', e
        print(RPA_status)
        return
def import_libraries(mytia):
    biblioteca = OpennessService.get_file_info(r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Library")
    OpenGlobalLibrary = mytia.GlobalLibraries.Open(biblioteca, OpennessService.tia.OpenMode.ReadWrite)
    enumLibrary =  OpenGlobalLibrary.TypeFolder.Folders
    projectLib = myproject.ProjectLibrary
    for folder in enumLibrary:
        # Verifica se 'Types' não está vazio antes de tentar acessar um índice
        try:
            updateLibrary = folder.Types[0].UpdateLibrary(projectLib)
            nameFolderEnum = OpennessService.get_attibutes(["Name"], folder)
            nameFolder = nameFolderEnum[0]
            print('update library:', nameFolder)
        except IndexError:
            # Ocorre se não houver itens em Types
            print('Erro: Não há tipos disponíveis em', folder)
        except Exception as e:
            # Captura outras exceções que podem ocorrer no processo
            print('Erro ao atualizar a biblioteca:', e)
    CloseGlobalLibrary = mytia.GlobalLibraries[0].Close()
    print("Close Library:", CloseGlobalLibrary)