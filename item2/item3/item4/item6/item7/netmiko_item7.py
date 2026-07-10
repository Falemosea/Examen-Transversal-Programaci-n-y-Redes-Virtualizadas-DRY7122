from netmiko import ConnectHandler


dispositivo = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.104',
    'username': 'cisco',
    'password': 'cisco123!',
    'port': 22,
}


comandos_configuracion = [
    'ipv6 unicast-routing',
    

    'router ospf 1',
    'router-id 1.1.1.1',
    'passive-interface default',
    'no passive-interface GigabitEthernet1',
    'network 0.0.0.0 255.255.255.255 area 0',
    'exit',
    

    'ipv6 router ospf 1',
    'router-id 1.1.1.1',
    'passive-interface default',
    'no passive-interface GigabitEthernet1',
    'exit'
]

def ejecutar_script():
    print("Iniciando conexión SSH con Netmiko al router...")
    try:

        conexion = ConnectHandler(**dispositivo)
        print("Conexión exitosa. Aplicando configuraciones OSPF...\n")
        

        salida_config = conexion.send_config_set(comandos_configuracion)
        print("--- Resultado de la configuración ---")
        print(salida_config)
        print("\n")
        

        print("--- Demostración OSPF (show running-config | section ospf) ---")
        salida_ospf = conexion.send_command('show running-config | section ospf')
        print(salida_ospf)
        print("\n")
        

        print("--- Información de Interfaces (IPv4 e IPv6) ---")
        salida_int_ipv4 = conexion.send_command('show ip interface brief')
        salida_int_ipv6 = conexion.send_command('show ipv6 interface brief')
        print("IPv4:")
        print(salida_int_ipv4)
        print("\nIPv6:")
        print(salida_int_ipv6)
        print("\n")
        

        print("--- Versión del Sistema (show version) ---")

        salida_version = conexion.send_command('show version')
        print('\n'.join(salida_version.split('\n')[:15])) 
        print("... [Salida truncada para visualización] ...")
        print("\n")


        print("--- Running Config (show running-config) ---")
        salida_run = conexion.send_command('show running-config')
        

        with open("running_config_item7.txt", "w") as archivo:
            archivo.write(salida_run)
        print("El running-config se ha guardado exitosamente en el archivo 'running_config_item7.txt'.\n")


        conexion.disconnect()
        print("Proceso finalizado y conexión cerrada.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    ejecutar_script()
