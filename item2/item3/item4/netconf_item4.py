import xml.dom.minidom
from ncclient import manager

HOST = "192.168.56.104"
PORT = 830
USER = "cisco"
PASS = "cisco123!"

print("Iniciando conexión NETCONF con el router CSR1000v...")

try:
    m = manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False
    )
    print("Conexión NETCONF establecida con éxito!\n")

    nuevo_hostname = "Candia-Oyanedel"
    
    netconf_hostname = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>{nuevo_hostname}</hostname>
        </native>
    </config>
    """
    
    print(f"Modificando el hostname del dispositivo a '{nuevo_hostname}'...")
    respuesta_hostname = m.edit_config(target="running", config=netconf_hostname)
    print("Respuesta del Router:")
    print(xml.dom.minidom.parseString(respuesta_hostname.xml).toprettyxml())

    netconf_loopback = """
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <Loopback>
                    <name>111</name>
                    <description>Loopback 111 - Creada mediante NETCONF en Examen</description>
                    <ip>
                        <address>
                            <primary>
                                <address>111.111.111.111</address>
                                <mask>255.255.255.255</mask>
                            </primary>
                        </address>
                    </ip>
                </Loopback>
            </interface>
        </native>
    </config>
    """
    
    print("Creando la interfaz Loopback 111 con IP 111.111.111.111/32...")
    respuesta_loopback = m.edit_config(target="running", config=netconf_loopback)
    print("Respuesta del Router:")
    print(xml.dom.minidom.parseString(respuesta_loopback.xml).toprettyxml())

    print("Todas las configuraciones requeridas fueron aplicadas correctamente!")
    
    m.close_session()

except Exception as e:
    print(f"Ocurrió un error durante la ejecución: {e}")
