import sys
sys.coinit_flags = 2
import os
import pywinauto
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import re
from repositories import UserConfig, MlfbManagement
from Controller.OpennessController import open_project, export_data_type, export_block
from Services.OpennessService import add_DLL, configurePath
import os
import Controller.OpennessController as OpennessController

favico_path = "./Assets/favico.ico"
if not os.path.exists(favico_path):
    favico_path = "favico.ico"
    print("File exists")

# Criando a janela principal
root = tk.Tk()
root.geometry("800x500")
root.iconbitmap(favico_path)
root.title("RPA Tia Openness")

# Variavel no nome do projeto
project_name_var=tk.StringVar()
quant_rb_import=tk.IntVar()
quant_gp_import=tk.IntVar()
dt_to_export = tk.StringVar()
bk_to_export = tk.StringVar()

############### FUNCTIONS ################
def CreateProject():
    project_name = project_name_var.get()
    global selected_version, project_dir
    if not UserConfig.CheckDll(selected_version):
        label_status_projeto.config(text="Erro: Dll não configurada para esta versão do TIA")
        return
    
    if not validate_all_device_names():
        label_status_projeto.config(text="Erro: Há nomes de dispositivos duplicados. Por favor, verifique.")
        return
    
    if project_name and project_dir: 
        devices = []
        for linha in InfoHardware:
            devices.append({"HardwareType": linha["combobox"].get(), "Mlfb":linha["mlfb"].get(),"Firm_Version":linha["firm_version"].get(), "Name": linha["entry"].get(), "Start_Adress": linha["Start_Adress"].get()})   
        label_status_projeto.config(text="Criando projeto...")
        status_criacao = OpennessController.create_project(project_dir, project_name, devices, rb_blocks_value, mg_blocks_value,selec_blocks_value)
        if status_criacao:
            label_status_projeto.config(text="Projeto criado com sucesso!")
        else:
            label_status_projeto.config(text="Falha ao criar projeto")
        
    else:
        label_status_projeto.config(text="Erro: Nome do projeto ou diretório não informados")
        
def opn_project():
    project_path = open_file_dialog()
    if project_path != None and project_path != '':
        open_project(project_path)
    else:
        label_status_projeto.config(text="Erro: Projeto não selecionado")

def open_directory_project_dialog():
    global project_dir
    project_dir = filedialog.askdirectory()

def open_directory_dialog():
    return filedialog.askdirectory()
    
def open_file_dialog():
    return filedialog.askopenfilename()

# def open_file_xml_dialog():
#     global dir_block
#     dir_block_config = filedialog.askopenfilename()
#     dir_block = configurePath(dir_block_config)
#     print(dir_block)
#     return dir_block

def validate_all_device_names():
    names_seen = {}
    all_names_valid = True
    for info in InfoHardware:
        device_name = info["entry"].get()
        device_type = info["combobox"].get()

        # Permitir device_name vazio se o device_type for 'IO_Node'
        if device_type == "DI" and device_type == "DO" and not device_name:
            continue
        
        # Checa por nomes duplicados
        if device_name in names_seen and device_type != "DI" and device_type != "DO":
            messagebox.showerror("Erro", f"O nome do dispositivo '{device_name}' já existe. Por favor, escolha um nome diferente.")
            info["entry"].set('')  # Limpa o campo de entrada duplicado
            all_names_valid = False
        else:
            names_seen[device_name] = None  # Armazena que o nome foi visto

    return all_names_valid


    
def AddHardware():
    global NHardware, CPU_list, IO_List
    
    if NHardware == 0:
        # Cabeçalhos das colunas
        headers = ["Type of Device", "Article Number", "Version", "Name", "Address"]
        for idx, header in enumerate(headers):
            label = ttk.Label(screen_frames[4], text=header)
            label.grid(row=0, column=idx, padx=5, pady=5)

    tupla_Input = {"combobox": tk.StringVar(root), "mlfb": tk.StringVar(root), "firm_version": tk.StringVar(root), "entry": tk.StringVar(root), "Start_Adress": tk.StringVar(root)}
    
    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    # Combobox 1º coluna - Tipo de Hardware
    combobox = ttk.Combobox(screen_frames[4], textvariable=tupla_Input["combobox"], values=opcoes_Hardware)
    combobox.grid(row=NHardware + 1, column=0, padx=5)
    
    # MLFB - Combobox 2º coluna       
    mlfb_combobox = ttk.Combobox(screen_frames[4], textvariable=tupla_Input["mlfb"])
    mlfb_combobox.grid(row=NHardware + 1, column=1, padx=5)

    def validate_address_input(P):
        if tupla_Input["combobox"].get() == "CONTROLLERS" or "IHM" :
            return re.match(r'^\d{0,3}(\.\d{0,3}){0,3}(\.\d{0,2})?$', P) is not None
        
        elif tupla_Input["combobox"].get() == "DI" or "DO":
            return re.match(r'^\d{0,5}?$', P) is not None
        else:
            return P.isdigit()

    validate_command = (root.register(validate_address_input), '%P')
    
    def update_mlfb_combobox(*args):
        selected_option = tupla_Input["combobox"].get()
        
        if selected_option == "CONTROLLERS":
            valueSource = mlfb_List[0]
            tupla_Input["Start_Adress"].set("192.168.0.01")
        elif selected_option == "IHM":
            valueSource = mlfb_List[1]
            tupla_Input["Start_Adress"].set("192.168.0.01")
        elif selected_option == "DI" or selected_option == "DO":
            valueSource = mlfb_List[2 if selected_option == "DI" else 3]
            tupla_Input["Start_Adress"].set("0")
            special_entry.grid()
        else:
            valueSource = []

        mlfb_combobox['values'] = valueSource
    #Função para atualizar a versão do componente para a ultima
    def update_firmware_versions_ui(*args):
        selected_mlfb = tupla_Input["mlfb"].get()
        firmware_versions = firm_versions.get(selected_mlfb, [])
        firm_version_combobox['values'] = firmware_versions
        if firmware_versions:
            firm_version_combobox.set(firmware_versions[-1])

    tupla_Input["combobox"].trace_add('write', update_mlfb_combobox)
    tupla_Input["mlfb"].trace_add('write', update_firmware_versions_ui)
    
    # FirmVersion - Combobox 3º coluna
    firm_version_combobox = ttk.Combobox(screen_frames[4], textvariable=tupla_Input["firm_version"], values=[])
    firm_version_combobox.grid(row=NHardware + 1, column=2, padx=5)
    
    # Entry - Nome do Hardware 4º coluna
    entry = ttk.Entry(screen_frames[4], textvariable=tupla_Input["entry"])
    entry.grid(row=NHardware + 1, column=3, padx=5)
    entry.bind('<Return>', focus_next_widget)

    # Entry Especial - Só aparece para DI
    special_entry = ttk.Entry(screen_frames[4], textvariable=tupla_Input["Start_Adress"],validate='key', validatecommand=validate_command)
    special_entry.grid(row=NHardware + 1, column=4, padx=5)
    special_entry.bind('<Return>', focus_next_widget)

    NHardware += 1
    
    InfoHardware.append(tupla_Input)




def update_status(status):
    global screen_instance
    if screen_instance:
        global RAP_status_Tela
        if not status:
            if RAP_status_Tela != OpennessController.RPA_status:
                RAP_status_Tela = OpennessController.RPA_status
        else:
            RAP_status_Tela = status
            
def setDllPath(dll_matrix):
    for dll in dll_matrix:
        tia_Version = dll["Tia_Version"]
        path = dll["Path"]
        UserConfig.saveDll(tia_Version, path)
    
def slice_tupla(string):
    if len(string) >= 2:
        return string[2:-3]
    else:
        return string
        
############### VARIABLES ################
NHardware = 0
InfoHardware = []
RAP_status_Tela = "Idle"
screen_instance = False
screen_frames = []
opcoes_Hardware = ["CONTROLLERS", "IHM", "DI", "DO"]
firm_versions = {}
selected_version = None
mlfb_Plc = []
mlfb_ihm = []
mlfb_DI = []
mlfb_DO = []
rb_blocks_value = 0
mg_blocks_value = 0
selec_blocks_value = 0
CPU_list = []
IO_List = []
mlfb_List=[mlfb_Plc, mlfb_ihm, mlfb_DI, mlfb_DO]

############### SCREEN ################
def main_screen():
    global screen_frames, firm_versions
    
    global screen_instance
    if not screen_instance:
        screen_instance = True
        update_status("Idle")
        
        i=0
        IHM = 0 
        IO = 0
        for type in opcoes_Hardware:
            for ii in MlfbManagement.getMlfbByHwType(type):
                mlfb_List[i].append(slice_tupla(str(ii)))
            i += 1

        for type in opcoes_Hardware:
            for item in MlfbManagement.getMlfbIHMByHwType(type):
                mlfb_List[IHM].append(slice_tupla(str(item)))
            IHM += 1
            
        for type in opcoes_Hardware:
            for item in MlfbManagement.getMlfbIOByHwType(type):
                mlfb_List[IO].append(slice_tupla(str(item)))
            IO += 1

        #atualiza lista de versão
        firm_versions.clear()  # Limpa o dicionário para evitar dados obsoletos

        for hw_type in opcoes_Hardware:
            firmware_data = MlfbManagement.getMlfbByVersion(hw_type)
            for mlfb, version in firmware_data:
                if mlfb not in firm_versions:
                    firm_versions[mlfb] = []
                firm_versions[mlfb].append(version)
            
        
        #Frame for user configuration 
        user_config = ttk.Frame(root)
        screen_frames.append(user_config)
        
        # Button Configurações
        BtnUserSettings = tk.Button(user_config, text="...", command=user_config_screen)
        BtnUserSettings.pack(padx=5, pady=5, anchor='w')
        screen_frames.append(BtnUserSettings)
        
        user_config.pack(padx=5, pady=5, anchor='w')
        
        proj_config_frame = ttk.Frame(root)
        screen_frames.append(proj_config_frame)
        
        # Project name
        ProjectName = tk.Label(proj_config_frame, text="Nome do projeto: ")
        ProjectName.grid(row=0, column=0, padx=5, pady=5)

        entrada1 = tk.Entry(proj_config_frame, textvariable = project_name_var)
        entrada1.grid(row=0, column=1, padx=5, pady=5)

        # Path
        btn_open_dialog = tk.Button(proj_config_frame, text="Selecionar diretório", command=open_directory_project_dialog)
        btn_open_dialog.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Button para criar
        criarBtn = tk.Button(proj_config_frame, text="Criar projeto", command=CreateProject)
        criarBtn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Button para abrir projeto
        openBtn = tk.Button(proj_config_frame, text="Abrir projeto", command=opn_project)
        openBtn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        # Button para importar bloco
        exportBkBtn = tk.Button(proj_config_frame, text="Import blocos", command=import_blocks_screen)
        exportBkBtn.grid(row=4, column=0, padx=5, pady=5)
        
        # Button para exportar bloco
        exportBkBtn = tk.Button(proj_config_frame, text="Exprtar blocos", command=exportar_blocks_screen)
        exportBkBtn.grid(row=4, column=1, padx=5, pady=5)

        # Button para exportar udt
        exportDtBtn = tk.Button(proj_config_frame, text="Export Data Type", command=export_data_type_screen)
        exportDtBtn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        proj_config_frame.pack()

        # Button para adicionar uma nova linha
        botao_adicionar_linha = tk.Button(root, text="Adicionar hardware", command=AddHardware)
        botao_adicionar_linha.pack(pady=10)
        screen_frames.append(botao_adicionar_linha)

        hardwareConfig = ttk.Frame(root)
        hardwareConfig.pack(padx=5, pady=5)
        screen_frames.append(hardwareConfig)
        
        global RAP_status_Tela
        global label_status_projeto
        label_status_projeto = tk.Label(root, text="Status: " + RAP_status_Tela)
        label_status_projeto.pack(padx=5, pady=5)

        # Carregar a imagem
        load_image(root, r"./logo.png")

        root.mainloop()
def set_version(usr_config_screen, version_select):
    global selected_version 
    selected_version = version_select
    
    if add_DLL(selected_version):
        print(f"Versão {selected_version} configurada com sucesso.")
        usr_config_screen.destroy()
    else:
        print(f"Falha ao configurar a versão {selected_version}.")
    return selected_version

def user_config_screen():
    usr_config_screen = tk.Toplevel(root)
    usr_config_screen.title("Configurações do usuário")
    usr_config_screen.geometry("540x360")
    
    usr_config_screen.transient(root)
    usr_config_screen.grab_set()
    
    nova_label = tk.Label(usr_config_screen, text="Aqui você pode configurar suas preferências")
    nova_label.pack()
    
    dll_config_frame = ttk.Frame(usr_config_screen)
    
    InstructionsDllPath = tk.Label(dll_config_frame, text="Selecione a versão do TIA Portal:")
    InstructionsDllPath.grid(row=0, column=0, padx=5, pady=5)

    dll_matrix = []
    
    def setDllTuple(Tia_Version):
        info_dll = {"Tia_Version": Tia_Version, "Path": open_file_dialog()}
        dll_matrix.append(info_dll)
    
    # Tia V15.1
    Btn151 = tk.Button(dll_config_frame, command=lambda: set_version(usr_config_screen, 151), width=10, text="Tia V15.1")
    Btn151.grid(row=1, column=0, padx=5, pady=5)    
    
    # Tia V16
    Btn16 = tk.Button(dll_config_frame, command=lambda: set_version(usr_config_screen, 16), width=10, text="Tia V16")
    Btn16.grid(row=2, column=0, padx=5, pady=5)
    
    # Tia V17
    Btn17 = tk.Button(dll_config_frame, command=lambda: set_version(usr_config_screen, 17), width=10, text="Tia V17")
    Btn17.grid(row=3, column=0, padx=5, pady=5,)
    
    dll_config_frame.pack(padx=5, pady=5)
    
    
    fechar_botao = tk.Button(usr_config_screen, text="Fechar", command=usr_config_screen.destroy)
    fechar_botao.pack()
    # Carregar a imagem
    load_image(usr_config_screen, r"./logo.PNG")
    
def export_data_type_screen():
    data_type_config_screen = tk.Toplevel(root)
    data_type_config_screen.title("Configurações do usuário")
    data_type_config_screen.geometry("540x360")
    
    data_type_config_screen.transient(root)
    data_type_config_screen.grab_set()
    
    frame_dt = tk.Frame(data_type_config_screen)
    frame_dt.pack(pady=10)
    
    InstructionBlocks = tk.Label(frame_dt, text="Nome do data type que deseja exportar?")
    InstructionBlocks.grid(row=0, column=0, padx=5, pady=5,)
    
    nome_dt = tk.Entry(frame_dt, textvariable=dt_to_export)
    nome_dt.grid(row=0, column=1, padx=5, pady=5)
    
    export_dt = tk.Button(frame_dt, text="Exportar", command=call_export_dt)
    export_dt.grid(row=1, column=1, columnspan=2 ,padx=5, pady=5)
    
def call_export_dt():
    dt_name = dt_to_export.get()
    export_data_type(None, dt_name, open_directory_dialog())

def call_export_bk():
    bk_name = bk_to_export.get()
    export_block(None, bk_name, open_directory_dialog())  


def import_blocks_screen():
    global rb_blocks_value, mg_blocks_value
    
    # Criando a janela
    import_config_frame = tk.Toplevel(root)
    import_config_frame.title("Configurações dos blocos")
    import_config_frame.geometry("600x360")

    import_config_frame.transient(root)
    import_config_frame.grab_set()
    
    # Label informativo
    nova_label = tk.Label(import_config_frame, text="Aqui você pode selecionar os blocos que deseja importar")
    nova_label.pack(pady=10)
    
    # Frame para os blocos
    frame_blocks = tk.Frame(import_config_frame)
    frame_blocks.pack(pady=10)

    # Adicione os elementos ao frame_blocks
    add_elements_to_frame(frame_blocks)

    # Botão para salvar configurações e fechar a janela
    save_btn = tk.Button(import_config_frame, text="Salvar Configurações", command=lambda: save_config(entrada1rb, entrada2gp, import_config_frame))
    save_btn.pack(pady=20)
    

def exportar_blocks_screen():
    data_type_config_screen = tk.Toplevel(root)
    data_type_config_screen.title("Exprtar blocos")
    data_type_config_screen.geometry("600x360")
    
    data_type_config_screen.transient(root)
    data_type_config_screen.grab_set()
    
    frame_dt = tk.Frame(data_type_config_screen)
    frame_dt.pack(pady=10)
    
    InstructionBlocks = tk.Label(frame_dt, text="Nome do bloco que deseja exportar?")
    InstructionBlocks.grid(row=0, column=0, padx=5, pady=5,)
    
    nome_dt = tk.Entry(frame_dt, textvariable=bk_to_export)
    nome_dt.grid(row=0, column=1, padx=5, pady=5)
    
    export_dt = tk.Button(frame_dt, text="Exportar", command=call_export_bk)
    export_dt.grid(row=1, column=1, columnspan=2 ,padx=5, pady=5)
    

def add_elements_to_frame(frame):
    global entrada1rb, entrada2gp, entrada3
    
    # Bloco do robô
    InstructionBlocks = tk.Label(frame, text="Quantidade de blocos do robô deseja importar?")
    InstructionBlocks.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    entrada1rb = tk.Entry(frame)
    entrada1rb.insert(0, rb_blocks_value)  # Inserir o valor armazenado
    entrada1rb.grid(row=0, column=1, padx=2, pady=2)


    # Bloco do grampo
    InstructionBlocks1 = tk.Label(frame, text="Quantidade de mesas giratórias deseja importar?")
    InstructionBlocks1.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    entrada2gp = tk.Entry(frame)
    entrada2gp.insert(0, mg_blocks_value)  # Inserir o valor armazenado
    entrada2gp.grid(row=1, column=1, padx=2, pady=2)

    # Bloco do selecionado 
    InstructionBlocks2 = tk.Label(frame, text="Quantidade de blocos do grampo deseja importar?")
    InstructionBlocks2.grid(row=2, column=0, padx=5, pady=5, sticky='w')

    entrada3 = tk.Entry(frame)
    entrada3.insert(0, selec_blocks_value)  # Inserir o valor armazenado
    entrada3.grid(row=2, column=1, padx=2, pady=2)

def save_config(entrada1rb, entrada2gp, window):
    global rb_blocks_value, mg_blocks_value, selec_blocks_value
    
    # Atualizar as variáveis globais com os valores atuais
    rb_blocks_value = int(entrada1rb.get())
    mg_blocks_value = int(entrada2gp.get())
    selec_blocks_value = int(entrada3.get())
    
    # Aqui você pode salvar esses dados em um arquivo, banco de dados, etc.
    with open("config_blocos.txt", "w") as file:
        file.write(f"Robô - Quantidade: {rb_blocks_value}\n")
        file.write(f"Grampo - Quantidade: {mg_blocks_value}\n")

    print("Configurações salvas com sucesso!")
    
    # Fecha a janela
    window.destroy()



def load_image(window, image_path):
    # Carregar a imagem
    img = Image.open(image_path)
    img = img.resize((125, 100))  # Redimensionar a imagem conforme necessário
    img = ImageTk.PhotoImage(img)
        
    # Exibir a imagem
    label_image = tk.Label(window, image=img)
    label_image.image = img  # Mantém uma referência para evitar a coleta de lixo
    label_image.place(x=window.winfo_width() - img.width(), y=0)

    # Atualizar a posição da imagem quando a largura da janela mudar
    def update_image_position(event):
        label_image.place(x=window.winfo_width() - img.width(), y=0)

    window.bind("<Configure>", update_image_position)
        
############### RENDER ################
main_screen()