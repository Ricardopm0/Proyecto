import json # lo utilizamos para leer las Apis como json-
from urllib.request import urlopen #libreria que te permite llamar las APIS
from datetime import datetime #te permite usar estructuras de tiempo
from itertools import permutations # libreria necesaria para utilizar el numero vampiro
#########################CLASE EQUIPO#########################################
class Equipo:
    def __init__(self, id, nombre, codigo, grupo):
        self.id = id
        self.nombre = nombre
        self.codigo = codigo
        self.grupo = grupo

    def __str__(self):
        return f"{self.nombre} ({self.codigo}), Grupo: {self.grupo}"
    
class GestionEquipos:
    def __init__(self):
        self.equipos = []

    def agregar_equipo(self, equipo):
        self.equipos.append(equipo)

    def listar_equipos(self):
        return self.equipos

    def buscar_equipo_por_id(self, id):
        for equipo in self.equipos:
            if equipo.id == id:
                return equipo
        return None
###################################Clase Estadio##########################
class Estadio:
    def __init__(self, id, nombre, ubicacion,capacidad_f,capacidad_c):
        self.id = id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.capacidad_f= capacidad_f
        self.capacidad_c= capacidad_c

    def __str__(self):
        return f"{self.nombre}, Ubicación: {self.ubicacion} , Capacidad de : {self.capacidad_f}x{self.capacidad_c}"

class GestionEstadios:
    def __init__(self):
        self.estadios = []

    def agregar_estadio(self, estadio):
        self.estadios.append(estadio)

    def listar_estadios(self):
        return self.estadios

    def buscar_estadio_por_id(self, id):
        for estadio in self.estadios:
            if estadio.id == id:
                return estadio
        return None
##############################################################################
#############################Partidos###################################
class Partido:
    def __init__(self, id, equipo_local, equipo_visitante, fecha, estadio, grupo):
        self.id = id
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.fecha = datetime.strptime(fecha, "%Y-%m-%d")
        self.estadio = estadio
        self.grupo = grupo

    def __str__(self):
        return f"{self.equipo_local.nombre} vs {self.equipo_visitante.nombre} en {self.estadio.nombre} en la fecha {self.fecha.strftime('%Y-%m-%d')}. ID del partido: {self.id}"

class GestionPartidos:
    def __init__(self):
        self.partidos = []

    def agregar_partido(self, partido):
        self.partidos.append(partido)

    def listar_partidos(self):
        return self.partidos

    def buscar_partidos_por_pais(self, pais):
        return [partido for partido in self.partidos if partido.equipo_local.nombre == pais or partido.equipo_visitante.nombre == pais]

    def buscar_partidos_por_estadio(self, estadio_nombre):
        return [partido for partido in self.partidos if partido.estadio.nombre == estadio_nombre]

    def buscar_partidos_por_fecha(self, fecha):
        #es la estructura para que me guarde una fecha en el formato que esta en la api
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        return [partido for partido in self.partidos if partido.fecha.date() == fecha_obj.date()]
    
    
 ##############################################################################   
################################ Clase Cliente ###################################
class Cliente:
    def __init__(self, nombre, cedula, edad):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad
        self.entradas_compradas = []
        self.compras_restaurante = []

    def __str__(self):
        return f"Cliente: {self.nombre}, Cédula: {self.cedula}, Edad: {self.edad}"

    def agregar_entrada(self, entrada):
        self.entradas_compradas.append(entrada)

    def agregar_compra_restaurante(self, compra):
        self.compras_restaurante.append(compra)

    def es_vip(self):
        return any(entrada.tipo == 'VIP' for entrada in self.entradas_compradas)

    def es_menor_de_edad(self):
        return self.edad < 18

    def es_numero_vampiro(self,numero):
        numero_str = str(numero)
        longitud = len(numero_str)
        
        # Verificar que el número tenga un número par de dígitos
        if longitud % 2 != 0:
            return False
        
        mitad = longitud // 2
        permutaciones = set(permutations(numero_str))
        
        for perm in permutaciones:
            colmillo1 = int(''.join(perm[:mitad]))
            colmillo2 = int(''.join(perm[mitad:]))
            
            # Verificar que los colmillos no terminen ambos en cero
            if colmillo1 % 10 == 0 and colmillo2 % 10 == 0:
                continue
            
            # Verificar si multiplicar los colmillos da el número original
            if colmillo1 * colmillo2 == numero:
                return True
                
        return False
######################################################################
######################Clase Entrada##################################
class Entrada:
    def __init__(self, tipo, partido, asiento):
        self.tipo = tipo
        self.partido = partido
        self.asiento = asiento
        self.precio_base = 35 if tipo == 'General' else 75
        #cree esto asi, porque con el id del partido que es unico, asociado a el asiento de ese partido es unico tambien
        #cree el id unico para cada entrada
        self.codigo = str(partido.id) +"/" +str(asiento[0])+"/"+str(asiento[1])
        self.usado = False

    def calcular_precio(self, cedula):
        descuento = 0
        if self.es_cedula_vampiro(cedula):
            descuento = self.precio_base * 0.5
        
        subtotal = self.precio_base - descuento
        iva = subtotal * 0.16
        total = subtotal + iva
        return subtotal, descuento, iva, total

    @staticmethod
    def es_cedula_vampiro(numero):
        numero_str = str(numero)
        longitud = len(numero_str)
        
        # Verificar que el número tenga un número par de dígitos
        if longitud % 2 != 0:
            return False
        
        mitad = longitud // 2
        permutaciones = set(permutations(numero_str))
        
        for perm in permutaciones:
            colmillo1 = int(''.join(perm[:mitad]))
            colmillo2 = int(''.join(perm[mitad:]))
            
            # Verificar que los colmillos no terminen ambos en cero
            if colmillo1 % 10 == 0 and colmillo2 % 10 == 0:
                continue
            
            # Verificar si multiplicar los colmillos da el número original
            if colmillo1 * colmillo2 == numero:
                return True
        return False

    def __str__(self):
        return f"Tipo: {self.tipo}, Partido: {self.partido}, Asiento: {self.asiento}"

class GestionEntradas:
    def __init__(self):
        self.entradas = []

    def vender_entrada(self,cliente, entrada):
        self.entradas.append([cliente, entrada])
        return entrada
    def buscar_entrada_id(self,codigo):
        for entradas in self.entradas:
            if entradas[1].codigo == codigo:
                return True
        return False
    def buscar_entrada(self,codigo):
        for entradas in self.entradas:
            if entradas[1].codigo == codigo:
                return entradas[1]
            
    def buscar_entrada_VIP(self,cedula):
        for entradas in self.entradas:
            if entradas[0].cedula == cedula:
                if entradas[1].tipo=="VIP":
                    return True
        return False
    def tener_entrada_VIP(self,cedula):
        for entradas in self.entradas:
            if entradas[0].cedula == cedula:
                if entradas[1].tipo=="VIP":
                    return entradas
    def listar_entradas(self):
        return self.entradas
#######################################################################################
################################# CLASE PRODUCTO######################################
class Producto:
    def __init__(self, nombre, clasificacion, tipo, precio,nombre_estadio,nombre_restaurante,cantidad):
        self.nombre = nombre
        self.clasificacion = clasificacion
        self.tipo = tipo
        self.precio = precio
        self.nombre_estadio=nombre_estadio
        self.nombre_restaurante=nombre_restaurante
        self.cantidad= cantidad

    def __str__(self):
        return f"{self.nombre} - {self.clasificacion} ({self.tipo}) - ${self.precio:.2f}, cantidad: {self.cantidad} restaurante: {self.nombre_restaurante}"
    
class GestionRestaurantes:
    def __init__(self):
        self.productos = []
    def anadir_producto(self,producto):
        self.productos.append(producto)
        return producto
    def buscar_restaurantes_por_estadio(self, estadio_nombre):
        return [producto for producto in self.productos if producto.nombre_estadio == estadio_nombre]
    def buscar_por_nombre(self, nombre):
        return [producto for producto in self.productos if nombre.lower() in producto.nombre.lower()]

    def buscar_por_tipo(self, clasificacion, tipo=None):
        if tipo:
            return [producto for producto in self.productos if producto.clasificacion == clasificacion and producto.tipo == tipo]
        return [producto for producto in self.productos if producto.clasificacion == clasificacion]

    def buscar_por_rango_precio(self, precio_min, precio_max):
        return [producto for producto in self.productos if precio_min <= producto.precio <= precio_max]
    
    
#Aqui se inicializan las clases y guardan de manera global toda la info de sus respectivas clases
gestion_equipos = GestionEquipos()
gestion_estadios = GestionEstadios()
gestion_partidos = GestionPartidos()
gestion_entradas = GestionEntradas()
gestion_restaurante = GestionRestaurantes()


#se iniciliza desde antes de iniciar el programa
def registrar_informacion(api_url_partidos,api_url_equipos,api_url_estadios):
    #es el procediemiento para recibir las apis de la web
    response_estadios = urlopen(api_url_estadios)
    #en data_estadios, esta toda la informacion de la api
    data_estadios = json.loads(response_estadios.read())
    response_equipos = urlopen(api_url_equipos)
    data_equipos = json.loads(response_equipos.read())
    response_partidos = urlopen(api_url_partidos)
    data_partidos = json.loads(response_partidos.read())
    
    #se almacenan los equipos
    for equipo_data in data_equipos:
        equipo = Equipo(equipo_data["id"], equipo_data["name"], equipo_data["code"], equipo_data["group"])
        
        if not gestion_equipos.buscar_equipo_por_id(equipo.id):
            gestion_equipos.agregar_equipo(equipo)
    #se almacenan los estadios    
    for estadio_data in data_estadios:
        estadio= Estadio(estadio_data["id"], estadio_data["name"], estadio_data["city"], estadio_data["capacity"][0],estadio_data["capacity"][1])
        
        if not gestion_estadios.buscar_estadio_por_id(estadio.id):
           gestion_estadios.agregar_estadio(estadio)
        
    #se almacenan los partidos  
    for partido_data in data_partidos:
        equipo_local = gestion_equipos.buscar_equipo_por_id(partido_data["home"]["id"])
        equipo_visitante = gestion_equipos.buscar_equipo_por_id(partido_data["away"]["id"])
        
        estadio_partido = gestion_estadios.buscar_estadio_por_id(partido_data["stadium_id"])
        
        partido = Partido(partido_data["id"], equipo_local, equipo_visitante, partido_data["date"], estadio_partido, partido_data["group"])
        gestion_partidos.agregar_partido(partido)
    #se almacenan los restaurantes  
    for estadio in data_estadios:
        nombre_estadio = estadio["name"]
        for restaurante in estadio['restaurants']:
            nombre_restaurante=restaurante['name']
            for producto in restaurante['products']:
                nombre = producto['name']
                precio = float(producto['price']) * 1.16  # Añadir 16% de IVA
                cantidad= producto['stock']
                if producto['adicional'] in ['alcoholic', 'non-alcoholic']:
                    clasificacion = 'bebida'
                    tipo = producto['adicional']
                else:
                    clasificacion = 'alimento'
                    tipo = 'de empaque' if producto['adicional'] == 'package' else 'de preparación'
                
                prod = Producto(nombre, clasificacion, tipo, precio,nombre_estadio,nombre_restaurante,cantidad)
                gestion_restaurante.anadir_producto(prod)   
    
    return gestion_equipos, gestion_estadios,  gestion_partidos , gestion_restaurante
    
def comprar_entradas():
    
    # Datos del cliente
    nombre = input("Ingrese su nombre: ")
    cedula = input("Ingrese su cédula: ")
    edad = int(input("Ingrese su edad: "))
    cliente = Cliente(nombre, cedula, edad)
    print("Partidos disponibles:")
    for partido in gestion_partidos.listar_partidos():
        print(partido)
    # Selección del partido
    partido_id = input("Ingrese el ID del partido que desea comprar: ")
    partido_seleccionado = None
    #buscamos el id en nuestro partidos
    for partido in gestion_partidos.listar_partidos():
        if partido.id == partido_id:
            partido_seleccionado = partido
            break
    #si no hay lo mandamos de nuevo al menu
    if not partido_seleccionado:
        print("Partido no encontrado.")
        menu()
    # Tipo de entrada
    tipo_entrada = input("Ingrese el tipo de entrada (General/VIP): ")
    print("Este estadio posee una cantidad de "+str(partido_seleccionado.estadio.capacidad_f)+" filas y "+str(partido_seleccionado.estadio.capacidad_c)+" de columnas.\n")
    
    disponible=True
    while disponible:
        fila=int(input("Seleccione la fila: "))
        if fila>partido_seleccionado.estadio.capacidad_f:
            print("debe escoger un asiento de fila valido")
            continue
        columna=int(input("Seleccione la columna: "))
        if columna>partido_seleccionado.estadio.capacidad_c:
            print("debe escoger un asiento de columna valido")
            continue
        if gestion_entradas.buscar_entrada_id(partido_seleccionado.id+"/"+str(fila)+"/"+str(columna)):
            print("Este asiento ya esta vendido, seleccione otro")
        else:
            disponible=False
    # Cálculo de precio
    entrada=Entrada(tipo_entrada,partido_seleccionado,(fila, columna))
    subtotal, descuento, iva, total = entrada.calcular_precio(cliente.cedula)

    # Mostrar resumen de compra
    print("\nResumen de la compra:")
    print(f"Asiento: fila {fila}, columna {columna}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Descuento: ${descuento:.2f}")
    print(f"IVA: ${iva:.2f}")
    print(f"Total: ${total:.2f}")

    confirmar = input("¿Desea proceder al pago? (si/no): ")
    if confirmar.lower() == 'si':
        # Venta de entrada
        entradafinal= gestion_entradas.vender_entrada(cliente, entrada)
        cliente.agregar_entrada(entrada)
        print("Pago exitoso. ¡Disfrute el partido!\n")
        print("Su codigo unico sera: "+ entrada.codigo+"\n")
        print("No lo pierda, ya que lo necesitará para entrar.\n")
    else:
        print("Compra cancelada.")
    menu()


def verificar_entradas():
    codigo_buscar=input("Por Favor indique el número de boleto para poder ingresar: \n")
    if gestion_entradas.buscar_entrada_id(codigo_buscar):
        entrada=gestion_entradas.buscar_entrada(codigo_buscar)
        if not(entrada.usado):
            print("su boleto se encontro en la base de datos y no se ha usado, puede pasar")
            entrada.usado=True
        else:
           print("su boleto se encontro en la base de datos y se ha usado, usted NO puede pasar") 
    else:
        print("Su boleto no fue encontrado, No puede pasar")
    menu()
    
def NumeroPerfecto(num):
	suma = 0
	for i in range(1,num):
		if (num % (i) == 0):
			suma += (i)
	if num == suma:
		return True
	else:
		return False 


def comprar_restaurante():
    cedula=input("Indique su número de cedula: ")
    compras=[]
    comprando=True
    conseguido=False
    if gestion_entradas.buscar_entrada_VIP(str(cedula)):
        entrada = gestion_entradas.tener_entrada_VIP(str(cedula))
        print("bienvenido a los restaurantes de "+ str(entrada[1].partido.estadio.nombre))
        #se imprime todos los porductos y restaurantes que hay en ese estadio
        for restaurante in gestion_restaurante.buscar_restaurantes_por_estadio(entrada[1].partido.estadio.nombre):
            print(restaurante)
        #simulacion de un carrito de compras
            
        while comprando:
            pedir=input("Coloque el nombre del producto que quiera añadir al carrito: \n")
            for restaurante in gestion_restaurante.buscar_restaurantes_por_estadio(entrada[1].partido.estadio.nombre):
                if restaurante.nombre==pedir:
                    conseguido=True
                    if entrada[0].edad <18 and restaurante.tipo=="alcoholic":
                        print("No puedes comprar bebidas alcoholicas, selecciona otro producto")
                    else:
                        cant=int(input("¿Cuántas quieres comprar? hay disponibles: " + str(restaurante.cantidad)+"\n"))
                        if cant> int(restaurante.cantidad):
                            print("No hay la cantidad solicitada")
                        else:
                            compras.append([restaurante,cant])
                            restaurante.cantidad= int(restaurante.cantidad) - cant
            if not(conseguido):
                print("producto no conseguido por favor asegurese de escribir bien el nombre")
            if len(compras)==0:
                pass
            else:
                seguir=input("¿Quiere seguir comprando? si/no: \n")
                if seguir=="no":
                    comprando=False
        print("Lista de cosas para llevar: \n")
        subtotal=0
        descuento=0
        for listaCosas in compras:
            # print(listaCosas[0].nombre+ "lleva " + str(listaCosas[1])+ " productos,costo unitario : "+ str(listaCosas[0].precio))
            print(f"{listaCosas[0].nombre} lleva:{listaCosas[1]} productos,costo unitario : ${listaCosas[0].precio:.2f}")
            subtotal=subtotal+ listaCosas[0].precio*int(listaCosas[1])
        print(f"Subtotal:$ {subtotal:.2f}")
        if NumeroPerfecto(int(cedula)):
            descuento=subtotal*0.15
            print(f"Descuento:$ {descuento:.2f}")
        else:
            print("Descuento: $0.00")
        total= subtotal-descuento
        print(f"TOTAL:$ {total:.2f}")
        decision=input("¿Desea Procesar la compra ? si/no: \n") 
        if decision=="si":
            print("SU COMPRA HA SIDO EXITOSA!!")
        else:
            print("Su compra no fue procesada, regresará al menu")
        menu()
    else:
        print("Usted no tiene ninguna entrada VIP que le permita usar los Restaurantes")
        menu()
#######################################Estadisticas##############################
class Estadisticas:
    def __init__(self,gestion_partidos, gestion_entradas, gestion_restaurantes):
        self.gestion_entradas = gestion_entradas
        self.gestion_restaurantes = gestion_restaurantes
        self.gestion_partidos = gestion_partidos
    def promedio_gasto_vip(self):
        total_gasto = 0
        total_vips = 0

        for entrada_info in self.gestion_entradas.entradas:
            cliente, entrada = entrada_info
            if entrada.tipo == 'VIP':
                total_vips += 1
                total_gasto += entrada.precio_base  # Precio del ticket
                for compra in cliente.compras_restaurante:
                    total_gasto += compra.precio * compra.cantidad

        if total_vips == 0:
            return 0
        return total_gasto / total_vips

    def asistencia_partidos(self):
        partidos_info = []

        for partido in self.gestion_partidos.partidos:
            boletos_vendidos = sum(1 for entrada_info in self.gestion_entradas.entradas if entrada_info[1].partido.id == partido.id)
            personas_asistieron = sum(1 for entrada_info  in self.gestion_entradas.entradas if entrada_info[1].partido.id == partido.id and entrada_info[1].usado)
            asistencia_venta_ratio = personas_asistieron / boletos_vendidos if boletos_vendidos > 0 else 0

            partidos_info.append({
                'nombre_partido': f"{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}",
                'estadio': partido.estadio.nombre,
                'boletos_vendidos': boletos_vendidos,
                'personas_asistieron': personas_asistieron,
                'asistencia_venta_ratio': asistencia_venta_ratio
            })

        partidos_info.sort(key=lambda x: x['asistencia_venta_ratio'], reverse=True)
        return partidos_info

    def partido_mayor_asistencia(self):
        max_asistencia = 0
        partido_mayor_asistencia = None

        for partido in self.gestion_partidos.partidos:
            personas_asistieron = sum(1 for entrada_info in self.gestion_entradas.entradas if entrada_info[1].partido.id == partido.id and entrada_info[1].usado)
            if personas_asistieron > max_asistencia:
                max_asistencia = personas_asistieron
                partido_mayor_asistencia = partido

        return partido_mayor_asistencia, max_asistencia

    def partido_mayor_boletos_vendidos(self):
        max_boletos_vendidos = 0
        partido_mayor_boletos_vendidos = None

        for partido in self.gestion_partidos.partidos:
            boletos_vendidos = sum(1 for entrada_info in self.gestion_entradas.entradas if entrada_info[1].partido.id == partido.id)
            if boletos_vendidos > max_boletos_vendidos:
                max_boletos_vendidos = boletos_vendidos
                partido_mayor_boletos_vendidos = partido

        return partido_mayor_boletos_vendidos, max_boletos_vendidos

    def top_productos_vendidos(self):
        producto_ventas = {}

        for producto in self.gestion_restaurantes.productos:
            ventas = producto.cantidad
            if producto.nombre not in producto_ventas:
                producto_ventas[producto.nombre] = 0
            producto_ventas[producto.nombre] += ventas

        top_3_productos = sorted(producto_ventas.items(), key=lambda x: x[1], reverse=True)[:3]
        return top_3_productos

    def top_clientes(self):
        cliente_boletos = {}

        for entrada_info in self.gestion_entradas.entradas:
            cliente = entrada_info[0]
            if cliente.cedula not in cliente_boletos:
                cliente_boletos[cliente.cedula] = 0
            cliente_boletos[cliente.cedula] += 1

        top_3_clientes = sorted(cliente_boletos.items(), key=lambda x: x[1], reverse=True)[:3]
        return top_3_clientes       
    
#Aquí se inicializa todo
#urls de cada api, la de restaurantes es la misma que de los estadios
api_url_partidos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"
api_url_equipos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json"
api_url_estadios=  "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"
gestion_equipo,gestion_estadio, gestion_partidos,gestion_restaurante = registrar_informacion(api_url_partidos,api_url_equipos,api_url_estadios)
estadisticas = Estadisticas(gestion_partidos,gestion_entradas, gestion_restaurante)

#Definimos el menu principal que se encargará de 
def menu():
    #Imprimimos el menú   
    print("\n\nBienvenido a este mundo de la Eurocopa 2024\n")
    print("MENÚ:\n")
    print("1- Buscar todos los partidos de una fecha")
    print("2- Buscar todos los partidos de un estadio")
    print("3- Buscar todos los partidos de un País")
    print("4- Vender Entrada")
    print("5- Verificar entradas al estadio")
    print("6- Comprar en el Restaurante")
    print("7- Ver estadísticas")
    opcion= int(input("Seleccione una opción: \n"))
    if opcion==1:
        fecha= input("Seleccione una fecha en el formato YYYY-MM-DD: \n")
        print("\n-------Todos los partidos de la fecha "+fecha+"-------\n")
        for fecha_buscar in gestion_partidos.buscar_partidos_por_fecha(fecha):
            print(fecha_buscar)
        print("--------------")
        #esta llamada es recursiva
        menu()
    elif opcion==2:
        nombre_estadio= input("Seleccione el nombre del estadio: \n")
        print("\n-------Todos los partidos del estadio " +nombre_estadio+"-------\n")
        for estadio_buscar in gestion_partidos.buscar_partidos_por_estadio(nombre_estadio):
            print(estadio_buscar)
        print("--------------")
        menu()
    elif opcion==3:
        nombre_pais= input("Seleccione el país que quiera conocer sus partidos: \n")
        print("\n-------Todos los partidos del país "+nombre_pais+"-------\n")
        for pais_buscar in gestion_partidos.buscar_partidos_por_pais(nombre_pais):
            print(pais_buscar)
        print("--------------")
        menu()
    elif opcion==4:
        comprar_entradas()
    elif opcion==5:
        verificar_entradas()
    elif opcion==6:
        comprar_restaurante()
    elif opcion == 7:
        print("\n-------Estadísticas-------\n")
        print("1- Promedio de gasto de un cliente VIP en un partido (ticket + restaurante)")
        print("2- Tabla con la asistencia a los partidos de mejor a peor")
        print("3- Partido con mayor asistencia")
        print("4- Partido con mayor boletos vendidos")
        print("5- Top 3 productos más vendidos en el restaurante")
        print("6- Top 3 de clientes (clientes que más compraron boletos)")

        opcion_estadistica = int(input("Seleccione una opción de estadísticas: \n"))
        if opcion_estadistica == 1:
            print(f"Promedio de gasto de un cliente VIP: ${estadisticas.promedio_gasto_vip():.2f}")
        elif opcion_estadistica == 2:
            print("Asistencia a los partidos de mejor a peor:")
            for partido in estadisticas.asistencia_partidos():
                print(partido)
        elif opcion_estadistica == 3:
            partido, asistencia = estadisticas.partido_mayor_asistencia()
            print(f"Partido con mayor asistencia: {partido} con {asistencia} asistentes")
        elif opcion_estadistica == 4:
            partido, boletos_vendidos = estadisticas.partido_mayor_boletos_vendidos()
            print(f"Partido con mayor boletos vendidos: {partido} con {boletos_vendidos} boletos vendidos")
        elif opcion_estadistica == 5:
            print("Top 3 productos más vendidos en el restaurante:")
            for producto in estadisticas.top_productos_vendidos():
                print(producto)
        elif opcion_estadistica == 6:
            print("Top 3 de clientes (clientes que más compraron boletos):")
            for cliente in estadisticas.top_clientes():
                print(cliente)
        else:
            print("Opción incorrecta")
        menu()
    else:
        print("Opción incorrecta")
        menu()
        
#Damos inicio al programa    
menu()