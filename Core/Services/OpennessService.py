import signal
import clr
from System.IO import DirectoryInfo, FileInfo  # type: ignore
from System import Int32, String # type: ignore
clr.AddReference('System.Collections')
from System.Collections.Generic import List # type: ignore
from repositories import UserConfig
from Controller import LanguageController
from . import UDTService
import re


def add_DLL(tia_Version):
    try:
        tuple = UserConfig.getDllPath(tia_Version)
        if tuple is None:
            print(f"Não foi possível obter o caminho da DLL para a versão {tia_Version}.")
            return False
        
        project_dll = r'' + tuple[0]
        clr.AddReference(project_dll)
        
        global tia, hwf, comp

        import Siemens.Engineering as tia # type: ignore
        import Siemens.Engineering.HW.Features as hwf # type: ignore
        import Siemens.Engineering.Compiler as comp # type: ignore
        return True

    except Exception as e:
        print("Error adding DLL reference: ", e)
        return False
    
def open_tia_ui():
    # Create an instance of Tia Portal
    return tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)

def create_project(tia_instance, project_dir, project_name):
    try:
        proj_dir_info = get_directory_info(project_dir+"\\"+project_name)
        if not proj_dir_info.Exists:
            return tia_instance.Projects.Create(proj_dir_info, project_name)
        else:
            return "Project already exists"
    except Exception as e:
        print('Error creating project: ', e)

def compilate_item(to_compile):
    try:
        RPA_status = "Compiling..."
        print(RPA_status)
        compiler_result = get_service(comp.ICompilable, to_compile).Compile()
        
        enumerable_attributes = get_attibutes(["State"], compiler_result)
        state = enumerable_attributes[0]
        print("State: ", state)
        
        if state == "Success":
            RPA_status = "Compilation successful!"
            print(RPA_status)
            return True
        else:
            RPA_status = "Compilation failed!"
            print(RPA_status)
            return False
            # get_compilation_error_description(compiler_result.Messages)
            
    except Exception as e:
        print('Error compiling device:', e)
        
# def get_compilation_error_description(messages):
#     description = ""
#     while description == "":
#         print(messages.GetType())
#         next_resulte = messages[0]
#         description = get_attibutes(["Description"], next_resulte)
#         messages = next_resulte.Messages
#         print("Looping")
#     raise Exception(description)
        
def get_attibutes(attribute_names, item):
    cs_attribute_names = List[str]()
    for i in attribute_names:
        cs_attribute_names.Add(i)
    return item.GetAttributes(cs_attribute_names)
    
def get_all_devices(myproject):
    try:
        devices = []
        for device in myproject.Devices:
            devices.append(device)
        return devices
    except Exception as e:
        print('Error getting all devices:', e)
        
def get_device_by_index(myproject, index):
    cpu_list = get_all_devices(myproject)
    cpu = cpu_list[index]
    return cpu 

def get_device_by_name(myproject, device_name):
    return next((d for d in myproject.Devices if d.Name == device_name), None)
         
def configurePath(path):
    return path.replace("/", "\\")

def get_directory_info(path):
    project_dir = configurePath(path)
    return DirectoryInfo(project_dir)

def get_file_info(path):
    path = configurePath(path)
    return FileInfo(path)

def open_project(project_path):
    file_info = get_file_info(project_path)
    
    if not file_info.Exists:
        print("Project file not found:", project_path)
        return None
    mytia = open_tia_ui()
    return mytia.Projects.OpenWithUpgrade(file_info)

def addHardware(deviceType, deviceName, deviceMlfb, myproject,FirmVersion,plc_count,Start_Adress):
    try:
        if deviceType == "CONTROLLERS":
            print('Creating CPU: ', deviceName)
            config_Plc = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
            deviceCPU = myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
            count = myproject.Devices.Count
            Count = count - 1
            Device = myproject.Devices[Count]
            networkIterface = get_network_interface_CPU(Device)
            Node = networkIterface.Nodes[0]
            address = Node.SetAttribute("Address", String(Start_Adress))
            return deviceCPU
            
        elif deviceType == "IHM":
            print("Creating IHM: ", deviceName)
            config_Hmi = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
            deviceIHM = myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)
            count = myproject.Devices.Count
            Count = count - 1
            Device = myproject.Devices[Count]
            networkIterface = get_network_interface_IHM(Device)
            Node = networkIterface.Nodes[0]
            address = Node.SetAttribute("Address", String(Start_Adress))
            return deviceIHM

        elif deviceType == "DI" or deviceType == "DO":
            print('Creating IO Node: ', deviceName)
            confing_IOnode = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
            plcRef = plc_count - 1
            Devices = myproject.Devices[plcRef]
            typeName = Devices.GetAttribute("TypeName")
            if typeName == "ET 200SP-Station":
                countFINAL = Devices.DeviceItems.Count
                count = countFINAL - 1 
            elif typeName == "ET 200S station":
                countFINAL = Devices.DeviceItems.Count
                count = countFINAL + 2
            else:
                count = Devices.DeviceItems.Count
            DeviceItemAssociation = Devices.GetAttribute("Items")
            if DeviceItemAssociation[0].CanPlugNew(confing_IOnode, deviceName, count):
                IONode = DeviceItemAssociation[0].PlugNew(confing_IOnode, deviceName, count)
                if typeName == "ET 200SP-Station":
                    Start_Adress_int = int(Start_Adress)
                    addressController = Devices.DeviceItems[countFINAL].DeviceItems[0].Addresses[0]
                    StartAddress = addressController.SetAttribute("StartAddress", Int32(Start_Adress_int))
                    GETStartAddress = addressController.GetAttribute("StartAddress")
                elif typeName == "ET 200S station":
                    addressController = Devices.DeviceItems[countFINAL].DeviceItems[0].Addresses[0]
                    Start_Adress_int = int(Start_Adress)
                    StartAddress = addressController.SetAttribute("StartAddress", Int32(Start_Adress_int))
                    GETStartAddress = addressController.GetAttribute("StartAddress")
                else:
                    addressController = Devices.DeviceItems[count].DeviceItems[0].Addresses[0]
                    Start_Adress_int = int(Start_Adress)
                    StartAddress = addressController.SetAttribute("StartAddress", Int32(Start_Adress_int))
                    GETStartAddress = addressController.GetAttribute("StartAddress")
                    print("Address Start: " , GETStartAddress )
                return IONode
            
            
    except Exception as e:
        RPA_status = 'Unknown hardware type: ', deviceType
        print(RPA_status)
        RPA_status = 'Error creating hardware: ', e
        print(RPA_status)
        
def GetAllProfinetInterfaces(myproject):
    RPA_status = 'Getting PROFINET interfaces'
    print(RPA_status)
    try:
        network_ports = []
        for device in myproject.Devices:            
            if (not is_gsd(device)):
                hardware_type = getHardwareType(device)
                
                if (hardware_type == "CPU"):
                    get_types(device)
                    network_interface_cpu = get_network_interface_CPU(device)
                    network_ports.append(network_interface_cpu)
                    
                elif (hardware_type == "IHM"):
                    network_interface_ihm = get_network_interface_IHM(device)
                    network_ports.append(network_interface_ihm)
                    
            else:
                RPA_status = 'Device' + str(device.GetAttribute("Name")) + ' is GSD: '
                print(RPA_status)
                
        return network_ports

    except Exception as e:
        RPA_status = 'Error getting PROFINET interfaces: ', e
        print(RPA_status)
        
def getCompositionPosition(deviceComposition):
    return deviceComposition.DeviceItems

def get_service(tipo, parent):
    try:
        network_interface_type = tipo
        getServiceMethod = parent.GetType().GetMethod("GetService").MakeGenericMethod(network_interface_type)
        return getServiceMethod.Invoke(parent, None)
    except Exception as e:
        RPA_status = 'Error getting service: ', e
        print(RPA_status)
        
def get_software(parent):
    try:
        parent = parent.DeviceItems[1]
        software_container = get_service(hwf.SoftwareContainer, parent)
        if not software_container:
            raise Exception("No SoftwareContainer found for device.")
        else:
            plc_software = software_container.Software
            if not plc_software:
                raise Exception("No CONTROLLERS software found for device.")
            return software_container.Software
        
    except Exception as e:
        RPA_status = 'Error getting software container: ', e
        print(RPA_status)
        print("Name: ", str(parent.GetAttribute("Name")))
        print("Type: ", parent.GetType())
        
def get_network_interface_CPU(deviceComposition):
    cpu = getCompositionPosition(deviceComposition)[1].DeviceItems
    for option in cpu:
        optionName = option.GetAttribute("Name")
        if optionName == "PROFINET interface_1":
            return get_service(hwf.NetworkInterface, option)
            
def get_network_interface_IHM(deviceComposition):
    hmi = getCompositionPosition(deviceComposition)[2].DeviceItems
    for option in hmi:
        optionName = option.GetAttribute("Name")
        if optionName == "PROFINET Interface_1":
            return get_service(hwf.NetworkInterface, option)
        
def is_gsd(device):
    try:
        if device.GetAttribute("IsGsd") == True:
            return True
        return False
    
    except Exception as e:
        RPA_status = 'Error checking GSD: ', e
        print(RPA_status)
        
def is_cpu(device):
    try:
        device_item = device[1]
        if str(device_item.GetAttribute("Classification")) == "CPU":
            return True
        return False
    
    except Exception as e:
        RPA_status = 'Error checking CPU: ', e
        print(RPA_status)

def is_hmi(device):
    try:
        device_item = device[0]
        type_identifier = str(device_item.GetAttribute("TypeIdentifier"))
        
        if (type_identifier.__contains__("OrderNumber:6AV")):
            return True
        return False
    
    except Exception as e:
        RPA_status = 'Error checking IHM: ', e
        print(RPA_status)
def is_IO(device):
    try:
        device_item = device[0]
        type_identifier = str(device_item.GetAttribute("TypeIdentifier"))
        
        if (type_identifier.__contains__("OrderNumber:6ES7")):
            return True
        return False
    
    except Exception as e:
        RPA_status = 'Error checking IO: ', e
        print(RPA_status)
        
def getHardwareType(device):
    try:
        device_item_impl = getCompositionPosition(device)
        if (is_cpu(device_item_impl)):
            return "CPU"
        elif (is_hmi(device_item_impl)):
            return "IHM"
        elif (is_IO(device_item_impl)):
            return "IO Node"
            
    except Exception as e:
        RPA_status = 'Error getting hardware type: ', e
        print(RPA_status)

def ConnectToSubnet(node, subnet):
    try:
        RPA_status = 'Connecting to subnet'
        node.ConnectToSubnet(subnet)
    except Exception as e:
        RPA_status = 'Error connecting to subnet: ', e
        print(RPA_status)
        
def SetSubnetName(myproject):
    RPA_status = 'Setting subnet name'
    print(RPA_status)
    return myproject.Subnets.Create("System:Subnet.Ethernet", "NewSubnet")


def recursive_folder_search(groups, group_name):
    
    try:
        found = groups.Find(group_name)
        if found:
            return found
        
        for group in groups.GetEnumerator():
            found = recursive_folder_search(group.Groups, group_name)
            if found:
                return found
    except Exception as e:
        print('Error searching group:', e)


def create_group(device, group_name, parent_group):
    try:
        plc_software = get_software(device)
        groups = plc_software.BlockGroup.Groups
        if not parent_group:
            return groups.Create(group_name)
        else:
            return recursive_folder_search(groups, parent_group).Groups.Create(group_name)
            
    except Exception as e:
        print('Error creating group:', e)


def import_data_type(myproject, cpu, data_type_path):
    try:
        udts_dependentes = UDTService.list_udt_from_bk(data_type_path)
        for udt in udts_dependentes:
            udt_path = data_type_path.rsplit(".xml", 1)[0] + "\\" + udt + ".xml"
            import_data_type(myproject, cpu, udt_path) 
        
        types = get_types(cpu)
        if type(data_type_path) == str:
            data_type_path = get_file_info(data_type_path)
        import_options = tia.ImportOptions.Override
        types.Import(data_type_path, import_options)
        
    except Exception as e:
        if str(e).__contains__("culture"):
            LanguageController.add_language(myproject, "pt-BR")
            import_data_type(myproject, cpu, data_type_path)
            
        else:
            print('Error importing data type from: ', data_type_path)
            print('Error message: ', e)
   
    
def export_data_type(device, data_type_name : str, data_type_path : str):
    try:
        types = get_types(device)
        data_type_path = data_type_path + "\\" + data_type_name + ".xml"
        data_type_path = get_file_info(data_type_path)
        
        data_type = types.Find(str(data_type_name))
        
        if data_type is not None:
            attempts = 0
            while data_type.GetAttribute("IsConsistent") == False:
                result = compilate_item(data_type) != "Success"
                if result == "Success":
                    break
                attempts += 1
                if attempts > 3:
                    raise Exception("Error compiling data type")
        
            data_type.Export(data_type_path, tia.ExportOptions.WithDefaults)
            RPA_status = 'Data type exported successfully!'
            print(RPA_status)
            return True
        
        else:
            RPA_status = 'Data type not found'
            print(RPA_status)
            return False
            
    except Exception as e:
        print('Error exporting data type while in service:', e)
  
# Função para importar os blocos de código para o software CONTROLLERS
def import_block(object, file_path):
    try:
        import_options = tia.ImportOptions.Override
        xml_file_info = get_file_info(file_path)
        
        if str(object.GetType()) == "Siemens.Engineering.HW.DeviceImpl":
            object = object.DeviceItems[1]
            print(f"Importing block to CPU: {object}")
            plc_software = get_software(object)
            plc_software.BlockGroup.Blocks.Import(xml_file_info, import_options)
            
        elif str(object.GetType()) == "Siemens.Engineering.SW.Blocks.PlcBlockComposition":
            print(f"Importing block to group: {object}")
            object.Import(xml_file_info, import_options)
            
        return True
    
    except Exception as e:
        print('Error importing block:', e)
        return False
    
def export_block(device, block_name : str, block_path : str):
    global RPA_status
    try:
        RPA_status = 'Exporting block'
        print(RPA_status)
        
        block_path = get_file_info(block_path + "\\" + block_name + ".xml")
        
        plc_software = get_software(device)
        myblock = plc_software.BlockGroup.Blocks.Find(block_name)
    
        attempts = 0
        while myblock.GetAttribute("IsConsistent") == False:
            result = compilate_item(myblock) != "Success"
            if result == "Success":
                break
            attempts += 1
            if attempts > 3:
                raise Exception("Error compiling data type")
        
        myblock.Export(block_path, tia.ExportOptions.WithDefaults)
        
    except Exception as e:
        RPA_status = 'Error exporting block: ', e
        print(RPA_status)
        return

# Função para alterar o nome e número no XML
def editar_tags_xml(arquivo, novo_nome, novo_numero):
    with open(arquivo, 'r', encoding='utf-8') as file:
        conteudo = file.read()

    # Substituir o texto nas tags <Name> e <Number>
    conteudo = re.sub(r'(?<=<Name>)[^<]+(?=</Name>)', novo_nome, conteudo)
    conteudo = re.sub(r'(?<=<Number>)[^<]+(?=</Number>)', str(novo_numero), conteudo)
    
    with open(arquivo, 'w', encoding='utf-8') as file:
        file.write(conteudo)

def verify_and_import(myproject, device_name, file_path, repetitions=0, tipo='' ):
    try:
        
        device = get_device_by_name(myproject, device_name)
        
        if not device:
            print(f"Device {device_name} not found in the project.")
            return

        # Extrair nome e número base do XML
        if tipo == 'robo':
            nome_base = "0070_robo"
            numero_base = 70
        else:
            nome_base = "0080_Grampo"
            numero_base = 80

        if not nome_base or not numero_base:
            print("Failed to extract base name or number from XML.")
            return

        # Executar a primeira importação
        import_block(device, file_path)

        # Executar importações adicionais conforme necessário
        for i in range(repetitions):
            print(f"Repetition {i+1} of {repetitions}")

            # Modificar o XML com novos valores de nome e número
            novo_nome = f"{int(nome_base.split('_')[0]) + i + 1:04d}_{nome_base.split('_')[1]}"
            novo_numero = numero_base + i + 1
            
            # Chamar a função para modificar o XML
            editar_tags_xml(file_path, novo_nome, novo_numero)

            # Realizar a importação após modificar o XML
            import_block(device, file_path)

    except Exception as e:
        print('Error verifying or importing file:', e)
        
def get_types(cpu):
    plc_software = get_software(cpu)
    type_group = plc_software.TypeGroup
    return type_group.Types 