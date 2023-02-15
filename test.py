import sys
import tkinter as tk
import winreg
from tkinter import messagebox
import winsound
import wmi

# Cria a janela
root = tk.Tk()
root.geometry("400x100")
root.title('Processor Temperature')
fonte = ("Arial", 24, "bold")


# Cria o label para exibir a temperatura
label_temp = tk.Label(root, text="Temperatura: -- ºC", font=fonte)
label_temp.pack(pady=10)

root.resizable(False, False)

# Cria o label para exibir a temperatura
#label_temp = tk.Label(root, text="Temperatura: -- ºC")
#label_temp.pack(pady=10)

# Função para atualizar a temperatura
def update_temp():
    # Conecta ao namespace 'root\WMI'
    w = wmi.WMI(namespace="root\\WMI")

    # Obtem as informações de temperatura do processador
    temperature_info = w.MSAcpi_ThermalZoneTemperature()[0]

    #Calcula a temperatura em graus Celcius
    temperature_celsius = (temperature_info.CurrentTemperature - 2732) / 10.0

    # Atualiza o label com a temperatura
    label_temp.config(text=f"Temperatura: {temperature_celsius:.0f} ºC")

    # Verifica se a temperatura ultrapassou um limite e emite um alerta se necessário
    if temperature_celsius > 80:
        root.attributes('-topmost', 1)
        tk.messagebox.showwarning("Alerta de temperatura", f"A temperatura do processador atingiu {temperature_celsius:.2f} ºC!")
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        root.attributes('-topmost', 0)

    #Agenda a próxima atualização da temperatura em 5 segundos
    root.after(5000, update_temp)

#Inicia a atualização da temperatura
update_temp()

# Adiciona um menu de configurações
menu = tk.Menu(root)
root.config(menu=menu)
config_menu = tk.Menu(menu)
menu.add_cascade(label="Configurações", menu=config_menu)

# Adiciona a opção para iniciar com o Windows
def toggle_startup():
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS)
    if startup_var.get():
        winreg.SetValueEx(reg_key, "Monitor de Temperatura do Processador", 0, winreg.REG_SZ, f'"{sys.executable}" "{__file__}"')
    else:
        try:
            winreg.DeleteValue(reg_key, "Monitor de Temperatura do Processador")
        except FileNotFoundError:
            pass

startup_var = tk.BooleanVar()
config_menu.add_checkbutton(label="Iniciar com o Windows", variable=startup_var, command=toggle_startup)

# Inicia o loop da janela
root.mainloop()