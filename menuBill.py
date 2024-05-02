from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color,grey_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient, VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

path, _ = os.path.split(os.path.abspath(__file__))

#Procesos de las Opciones del Menu Facturacion
#CLIENTE
class CrudClients(ICrud):
    def create(self):
        validar = Valida()
        
        while True:
            borrarPantalla()
            print('\033c', end='')
            gotoxy(2,1);print(cyan_color+"█"*90)
            gotoxy(2,2);print(cyan_color+"██"+" "*34+"INGRESO DE CLIENTE"+" "*34+"██")
            
            #****************************************************
            #Verificación de DNI
            gotoxy(5,4);print("dni: ")
            dni=validar.cedula("Error: debe contener 10 dígitos",23,4)
            json_file = JsonFile(path+'/archivos/clients.json')
            client = json_file.find("dni",dni)
            if client:
                gotoxy(35,6);print("Cliente ya existente")
                time.sleep(1)
            else: 
                break
            
        #****************************************************
        gotoxy(5,5);print("Nombre: ")
        first_name=validar.solo_letras("Error: Solo letras",23,5)
        gotoxy(5,6);print("Apellido:")
        last_name=validar.solo_letras("Error: Solo letras",23,6)
        
        #****************************************************
        gotoxy(5,7);type_client = str(input("El cliente es VIP? (s/n): ")).lower()
        if type_client =="s":
            vip=VipClient(first_name,last_name,dni)
            save = VipClient.getJson(vip)
        else:
            gotoxy(5,8);discount = input("Aplica al descuento el cliente? (s/n): ").lower()
            if discount == "s" : discount=True
            else:discount=False
            regular = RegularClient(first_name,last_name,dni, discount)
            save = RegularClient.getJson(regular)
            
        gotoxy(15,10);print(green_color+"Está seguro de grabar el cliente? (s/n): ")
        gotoxy(58,10);procesar = input().lower()
        if procesar == "s":
            json_file = JsonFile(path+'/archivos/clients.json')
            invoices = json_file.read()
            invoices.append(save)
            json_file = JsonFile(path+'/archivos/clients.json')
            json_file.save(invoices)
            gotoxy(15,11);print("😊 cliente guardado satisfactoriamente 😊"+reset_color)
            gotoxy(4,15);input("Presione una tecla para continuar...") 
            
        else:
            gotoxy(20,10);print("🤣 No pudo registrar al cliente 🤣"+reset_color)    
        time.sleep(1)
        
    def update(self):
        validar = Valida()
        
        print('\033c', end='')
        gotoxy(2,1);print(yellow_color+"█"*90)
        gotoxy(2,2);print("██"+" "*30+"ACTUALIZACIÓN DE CLIENTES"+" "*31+"██")
        
        #*********************************************************
        json_file = JsonFile(path+'/archivos/clients.json')
        gotoxy(2,2);clients = json_file.read()
        gotoxy(4,5);dni = print("Ingrese el dni del cliente a actualizar: ")
        dni=validar.cedula("Error: debe contener 10 dígitos",50,5)
        client_update = None
        for client in clients:
            if client["dni"] == dni:
                client_update = client
                break
        
        #*********************************************************
        if client_update:
            #Verificar que las claves existan 
            if "nombre" in client_update:
                gotoxy(4,6);print("Nombre:", client_update["nombre"])
            if "apellido" in client_update:
                gotoxy(4,7);print("Apellido:", client_update["apellido"])
            if "valor" in client_update:
                gotoxy(4,8);print("Valor:", str(client_update["valor"]))
    
            #*********************************************************
            #Solicitar la nueva información 
            gotoxy(4,9); print("Ingrese el nuevo nombre (enter si no desea actualizar): ")
            nuevo_nombre=validar.solo_letras("Error: Solo letras",65,9)
            gotoxy(4,10); print("Ingrese el nuevo apellido (enter si no desea actualizar): ")
            nuevo_apellido=validar.solo_letras("Error: Solo letras",65,10)
            gotoxy(4,11); print("Ingrese el nuevo valor (enter si no desea actualizar): ")
            nuevo_valor = validar.solo_decimales("Error: Solo números",65,11)

            #*********************************************************
            #Actualizar la información del cliente 
            if nuevo_nombre:
                client_update["nombre"] = nuevo_nombre
            if nuevo_apellido:
                client_update["apellido"] = nuevo_apellido
            if nuevo_valor:
                client_update["valor"] = float(nuevo_valor)

            #*********************************************************
            #Guardar los cambios en el archivo JSON 
            json_file.save(clients)
            gotoxy(4,13);print(green_color+"cliente actualizado exitosamente.")
            
        else:
            print(red_color+"No se encontró ningún cliente con el dni proporcionado."+reset_color)

        gotoxy(4,12);print(yellow_color+"*"*90+reset_color)
        gotoxy(8,14);input("Presione Enter para continuar...")
         
    def delete(self):
        validar = Valida()
        
        print('\033c', end='')
        gotoxy(2,1);print(red_color+"█"*90)
        gotoxy(2,2);print("██"+" "*30+"ELIMINACIÓN DE CLIENTE"+" "*34+"██"+reset_color)
        
        #*********************************************************
        json_file = JsonFile(path+'/archivos/clients.json')
        gotoxy(2,2);json_file.read()
        gotoxy(4,5);dni = print("Ingrese el dni del cliente a eliminar: ")
        dni=validar.cedula("Error: debe contener 10 dígitos",50,5)
        client = json_file.find('dni',dni)
            
        #*********************************************************
        #Se muestra por pantalla los datos del cliente
        if client:
            gotoxy(4,6);print(purple_color + "DATOS DEL CLIENTE:" + reset_color)
            gotoxy(15,7);headers = "DNI".ljust(15) + "NOMBRE".ljust(20) + "APELLIDO".ljust(20) + "VALOR".ljust(15)
            gotoxy(10,8);print(purple_color + "-" * len(headers) + reset_color)
            gotoxy(15,9);print(headers)
            gotoxy(10,10);print(purple_color + "-" * len(headers) + reset_color)
            
            #*********************************************************
            for find in client:
                client_info = find['dni'].ljust(15) + find['nombre'].ljust(20) + find['apellido'].ljust(20) + str(find['valor']).ljust(15)
                gotoxy(15,11);print(client_info)
                gotoxy(10,12);print(purple_color + "-" * len(headers) + reset_color)
            
            #*********************************************************
            gotoxy(4,13);print(red_color+"Está seguro de eliminar el cliente? (s/n): ")
            procesar=validar.solo_letras("Error: Solo letras",50,13).lower()
            if procesar == "s": 
                delete = json_file.delete('dni',dni)
                
                if delete:
                    gotoxy(20,15);print("😊 Cliente eliminado 😊"+reset_color)
                    
            elif procesar == "n":
                gotoxy(20,15);print("❗El cliente no será eliminado❗"+reset_color) 
                   
            else:
                gotoxy(20,15);print("❗No es válido su ingreso❗"+reset_color) 
                
            gotoxy(4,17);input("Presione una tecla para continuar...")    
            time.sleep(2)
        else:
            gotoxy(35,6);print("Cliente no existente")
            time.sleep(1)
    
    def consult(self):
        
        print('\033c', end='')
        gotoxy(2,1);print(yellow_color + "█"*90)
        gotoxy(2,2);print("██" + " " * 32 + "Consulta de Clientes" + " " * 34 + "██")

        #*********************************************************
        #Mostrar lista de clientes
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()
        
        #*********************************************************
        gotoxy(37,4);print("Lista de Clientes" + reset_color)
        gotoxy(15,6);print("-" * 60)
        gotoxy(15,7);print("DNI".ljust(15) + "NOMBRE".ljust(20) + "APELLIDO".ljust(20) + "VALOR".ljust(15))
        gotoxy(15,8);print("-" * 60)

        row = 10
        for client in clients:
            gotoxy(15,row);print(client['dni'].ljust(15) + client['nombre'].ljust(20) + client['apellido'].ljust(20) + str(client['valor']).ljust(15))
            row += 1

        #*********************************************************
        #Solicitar DNI del cliente 
        gotoxy(8,row+5);print("Ingrese DNI del Cliente: ", end='')
        validar = Valida()
        client_dni = validar.cedula("Cédula no identificada", 37, row+5)

        #*********************************************************
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.find("dni", client_dni)
        if clients:
            gotoxy(15,row+7);print(purple_color + "DNI".ljust(15) + "NOMBRE".ljust(20) + "APELLIDO".ljust(20) + "VALOR".ljust(15))
            gotoxy(15,row+8);print("-" * 60)

            #*********************************************************
            #Detalles del cliente
            for client in clients:
                gotoxy(15,row+9);print(client['dni'].ljust(15) + client['nombre'].ljust(20) + client['apellido'].ljust(20) + str(client['valor']).ljust(15) + reset_color)
            gotoxy(30,row+12);print("😊 Gracias por consultar 😊")
        else:
            gotoxy(2,row+7);print(red_color+"😓 El cliente con el DNI proporcionado no se encuentra 😓" + reset_color)

        #*********************************************************
        gotoxy(2,row+10);print(purple_color + "█" * 90 + reset_color)
        gotoxy(3,row+13);input("Presione una tecla para continuar...") 
        
#PRODUCTOS
class CrudProducts(ICrud):
    
    def create(self):
        validar = Valida()
        
        while True:
            validar = Valida()
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"█"*90)
            gotoxy(2,2);print("██"+" "*34+"Registro de Producto"+" "*32+"██"+reset_color)
            
            #*********************************************************
            #Obtener datos del nuevo producto
            gotoxy(4,4); print(grey_color+"Ingrese el nombre del producto: ")
            name=validar.solo_letras("Error: Solo letras",45,4)
            
            json_file = JsonFile(path+'/archivos/products.json')
            product = json_file.find("descripcion",name)
            if product:
                gotoxy(35,6);print("Producto existente")
                time.sleep(1)
            else: 
                break
        
        #*********************************************************
        gotoxy(4,5); print("Ingrese el precio del producto: ")
        price=validar.solo_decimales("Error: Solo números",45,5)
            
        gotoxy(4,6); print("Ingrese el stock inicial del producto: ")
        stock=validar.solo_numeros("Error: Solo enteros",45,6)

        #*********************************************************
        #Se genera un ID único para el nuevo producto
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        if products:
            last_id = max(product["id"] for product in products)
            new_id = last_id + 1
        else:
            new_id = 1
        
        #*********************************************************
        #Crear instancia de la clase Product con los datos ingresados
        new_product = Product(new_id, name, price, stock)
        
        #*********************************************************
        #Guardar el nuevo producto en el archivo JSON de productos
        products.append(new_product.getJson())
        json_file.save(products)
        
        #*********************************************************
        gotoxy(2,8);print(green_color+"██"+" "*40+" "*46+"██")
        gotoxy(2,9);print("█"*90+reset_color)
        gotoxy(27,11);print(grey_color+"✅ Producto registrado exitosamente con ID:", new_id)
        gotoxy(4,13);input(reset_color+"Presione Enter para continuar...")
    
    
    def update(self):
        validar = Valida()
        
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,3);print(" "*30+"Actualización de Producto"+" "*30+reset_color)
        
        #*********************************************************
        json_file = JsonFile(path+'/archivos/products.json')
        invoices1 = json_file.read()
        
        #*********************************************************
        #Impresión de los productos
        ancho_consola = 80
        gotoxy(6,4);print("Productos:")
        print("-" * ancho_consola)
        print(f"{'ID'.center(10)}{'Descripción'.center(20)}{'Precio'.center(15)}{'Stock'.center(10)}")
        print("-" * ancho_consola)

        for product in invoices1:
            print(f"{str(product['id']).center(10)}{product['descripcion'].center(20)}{str(product['precio']).center(15)}{str(product['stock']).center(10)}")
        
        #*********************************************************
        product_id = int(input("⭐ Ingrese el ID del producto que desea actualizar: "))
        borrarPantalla()
        
        #*********************************************************
        #Busca el producto en el archivo JSON de productos
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        product_to_update = None
        for product in products:
            if product["id"] == product_id:
                product_to_update = product
                break
        
        #*********************************************************
        #Verificar que las claves existan 
        if product_to_update:
            if "descripcion" in product_to_update:
                print("Producto:", product_to_update["descripcion"])
            if "precio" in product_to_update:
                print("Precio:", product_to_update["precio"])
            if "stock" in product_to_update:
                print("Stock:", product_to_update["stock"])

            #*********************************************************
            #Solicitar nueva información 
            gotoxy(2,5);print(cyan_color+"*"*90+reset_color)
            gotoxy(4,6); print("Ingrese el nuevo nombre del producto (ENTER si no desea actualizar): ")
            nuevo_nombre=validar.solo_letras("Error: Solo letras",80,6)
            
            gotoxy(4,7); print("Ingrese el nuevo precio del producto (ENTER si no desea actualizar): ")
            nuevo_precio=validar.solo_decimales("Error: Solo números",80,7)
                
            gotoxy(4,8); print("Ingrese el nuevo stock del producto (ENTER si no desea actualizar): ")
            nuevo_stock=validar.solo_numeros("Error: Solo enteros",80,8)

            #*********************************************************
            #Actualizar la información del producto 
            if nuevo_nombre:
                product_to_update["descripcion"] = nuevo_nombre
            if nuevo_precio:
                product_to_update["precio"] = float(nuevo_precio)
            if nuevo_stock:
                product_to_update["stock"] = int(nuevo_stock)

            #*********************************************************
            #Guardar los cambios en el archivo JSON 
            json_file.save(products)
            gotoxy(2,10);print(cyan_color+"*"*90+reset_color)
            gotoxy(30,12);print(green_color+"✅ Producto actualizado exitosamente."+reset_color)
            
        else:
            gotoxy(25,4);print(red_color+"❌ No se encontró ningún producto con el ID proporcionado ❌"+reset_color)
            time.sleep(2)

        gotoxy(8,14);input("Presione Enter para continuar...")
    
    def delete(self):
        
        print('\033c', end='')
        gotoxy(2,1);print(red_color+"█"*90)
        gotoxy(2,3);print(" "*30+"Eliminación de Producto"+" "*30+reset_color)
        
        #*********************************************************
        json_file = JsonFile(path+'/archivos/products.json')
        invoices1 = json_file.read()
        
        #*********************************************************
        #Impresión de los productos
        ancho_consola = 80
        gotoxy(2,4);print("Productos:")
        print("-" * ancho_consola)
        print(f"{'ID'.center(10)}{'Descripción'.center(20)}{'Precio'.center(15)}{'Stock'.center(10)}")
        print("-" * ancho_consola)

        #*********************************************************
        #Se muestran los detalles del producto
        for product in invoices1:
            print(f"{str(product['id']).center(10)}{product['descripcion'].center(20)}{str(product['precio']).center(15)}{str(product['stock']).center(10)}")
            
        product_id = input(" ⭐ Ingrese el ID del producto que desea eliminar: ")
        time.sleep(1)
        borrarPantalla()
        
        #*********************************************************
        #Se busca el producto en el archivo JSON
        if product_id.isdigit():
            invoices1 = json_file.delete("id",int(product_id))
            gotoxy(30,3);print(red_color+invoices1+reset_color)
            gotoxy(6,5);input("Presione una tecla para continuar...") 

        else:
            gotoxy(30,3);print(red_color+"❗El ID no es válido❗"+reset_color)  
            gotoxy(15,5);print(blue_color+"No ingresó el id correspondiente.... inténtelo mas tarde..."+reset_color) 
            gotoxy(6,8);input("Presione una tecla para continuar...")  
    
    def consult(self):
        
        print('\033c', end='')
        gotoxy(2,1);print(yellow_color+"█"*90)
        gotoxy(2,2);print("██"+" "*32+"Consulta de Producto"+" "*34+"██")

        #*********************************************************
        #Mostrar lista de productos
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        
        #*********************************************************
        gotoxy(37,4);print(grey_color+"Lista de Productos" + reset_color)
        gotoxy(15,6);print("-" * 60)
        gotoxy(15,7);print("ID".ljust(10) + "DESCRIPCIÓN".ljust(25) + "PRECIO".ljust(15) + "STOCK".ljust(10))
        gotoxy(15,8);print("-" * 60)
        total_precio = 0
        total_stock = 0
        row = 9
        
        for product in products:
            gotoxy(15,row);print(str(product['id']).ljust(10) + product['descripcion'].ljust(25) + f"{product['precio']:.2f}".ljust(15) + str(product['stock']).ljust(10))
            total_precio += product['precio']
            total_stock += int(product['stock']) 
            row += 1

        #*********************************************************
        #Mostrar la suma total de precio y stock
        gotoxy(15,row+2);print(f"Total del Precio: {total_precio:.2f}".ljust(40))
        gotoxy(15,row+3);print(f"Total del Stock: {total_stock}".ljust(40))

        #*********************************************************
        #Solicitar ID del producto
        gotoxy(8,row+5);print("Ingrese ID del Producto: ", end='')
        validar = Valida()
        product_id = validar.solo_numeros("Solo numeros", 37, row+5)
        borrarPantalla()
        
        #*********************************************************
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.find("id", int(product_id))
        if products:
            gotoxy(15,row+7);print(purple_color+"ID".ljust(10) + "DESCRIPCIÓN".ljust(25) + "PRECIO".ljust(15) + "STOCK".ljust(10))
            gotoxy(15,row+8);print("-" * 60)

            #*********************************************************
            #Detalles del producto
            for product in products:
                gotoxy(15,row+9);print(str(product['id']).ljust(10) + product['descripcion'].ljust(25) + f"{product['precio']:.2f}".ljust(15) + str(product['stock']).ljust(10)+reset_color)
            gotoxy(30,row+12);print("😊 Gracias por consultar 😊")
            
        else:
            gotoxy(2,row+7);print(red_color + "😓 El producto con el ID proporcionado no se encuentra 😓" + reset_color)

        #*********************************************************
        gotoxy(2,row+10);print(grey_color + "█" * 90 + reset_color)
        gotoxy(3,row+13);input("Presione una tecla para continuar...")
    

class CrudSales(ICrud):
    def create(self):
        validar = Valida()
        
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        
        #*********************************************************
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        
        #*********************************************************
        dni=validar.cedula("Error: debe contener 10 dígitos",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        
        #*********************************************************
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        
        #*********************************************************
        #Detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            
            #*********************************************************
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
                
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        
        #*********************************************************
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
            
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)    
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(yellow_color+"█"*90)
        gotoxy(2,2);print(yellow_color+"██"+" "*34+"Consulta de Venta"+" "*35+"██")
        
        #*********************************************************
        json_file = JsonFile(path+'/archivos/invoices.json')
        gotoxy(2,2);invoices = json_file.read()
        
        #*********************************************************
        #Mostrar las facturas
        gotoxy(42,3);print(purple_color+"Facturas"+reset_color)
        gotoxy(9,5);print(f"{'ID'.ljust(10)}{'Fecha'.ljust(20)}{'Cliente'.ljust(30)}{'Total'.rjust(10)}")
        gotoxy(7,6);print("-" * 80)
        f = 7
        for fac in invoices:
            id_str = str(fac['factura']).ljust(10)
            fecha_str = fac['Fecha'].ljust(20)
            cliente_str = fac['cliente'].ljust(30)
            total_str = f"{fac['total']:.2f}".rjust(10) 
            gotoxy(9, f);print(f"{id_str}{fecha_str}{cliente_str}{total_str}")
            f += 1
        
        #*********************************************************
        gotoxy(7, 12);invoice = input("Ingrese el ID: ")
        borrarPantalla()
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            
            #*********************************************************
            gotoxy(30,1);print(blue_color+f"IMPRESIÓN DE LA FACTURA")
            gotoxy(2,2);print(purple_color+"*"*90+reset_color)
            for fac in invoices:
                gotoxy(5,4);print(f"Factura#: {fac['factura']} {''*3} Fecha:{fac['Fecha']}")
                gotoxy(5,6);print(f"Comprador: {fac['cliente']}")
                gotoxy(66,4);print(f"Subtotal: {fac['subtotal']}")
                gotoxy(66,5);print(f"Decuento: {fac['descuento']}")
                gotoxy(66,6);print(f"Iva     : {fac['iva']}")
                gotoxy(66,7);print(f"Total   : {fac['total']}")
                
                #*********************************************************
                gotoxy(2,9);print(purple_color+"*"*90+reset_color+reset_color) 
                gotoxy(5,10);print(blue_color) 
                gotoxy(12,10);print("ARTÍCULO") 
                gotoxy(24,10);print("PRECIO") 
                gotoxy(38,10);print("CANTIDAD") 
                gotoxy(48,10);print("SUBTOTAL") 
                gotoxy(58,10);print(reset_color) 
                
                #*********************************************************
                d=11
                for det in fac['detalle']:
                    gotoxy(12,d);print(det['poducto']) 
                    gotoxy(24,d);print(det['precio']) 
                    gotoxy(38,d);print(det['cantidad']) 
                    gotoxy(48,d);print(det['precio']*det['cantidad']) 
                    d+=1
                    
                gotoxy(58,d);print(reset_color)
                
            x=input("presione una tecla para continuar...")    
        else:    
            gotoxy(30,3);print(red_color+"Debe de ingresar un ID válido. regresando..... 😓")
            time.sleep(2)
            
    def update(self):
        validar = Valida()
        
        print('\033c', end='')
        gotoxy(2,1);print(grey_color+"█"*90)
        gotoxy(2,2);print("██"+" "*31+"Modificación de Factura"+" "*32+"██"+reset_color)
        
        #*********************************************************
        json_file = JsonFile(path+'/archivos/invoices.json')
        gotoxy(2,2);invoices = json_file.read()
        
        #*********************************************************
        #Mostrar las facturas
        gotoxy(9,6);print(f"{'ID'.ljust(10)}{'Fecha'.ljust(20)}{'Cliente'.ljust(30)}{'Total'.rjust(10)}")
        gotoxy(7,7);print("-" * 80)
        f = 8
        for fac in invoices:
            id_str = str(fac['factura']).ljust(10)
            fecha_str = fac['Fecha'].ljust(20)
            cliente_str = fac['cliente'].ljust(30)
            total_str = f"{fac['total']:.2f}".rjust(10) 
            gotoxy(9, f);print(f"{id_str}{fecha_str}{cliente_str}{total_str}")
            f += 1
        
        #*********************************************************
        gotoxy(6,4);print(purple_color+"Ingrese el ID de la factura a actualizar: "+reset_color)
        gotoxy(2,4);invoice_number = validar.solo_numeros("Error: Solo Numeros",48,4)
        borrarPantalla()
        
        #*********************************************************
        #Se busca el número de la factura
        if str(invoice_number).isdigit(): 
            invoice_number = int(invoice_number)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            invoice_found = False
            for invoice in invoices:
                if invoice["factura"] == invoice_number:
                    invoice_found = True

                    #*********************************************************
                    gotoxy(2,1);print(purple_color+"█"*90)
                    gotoxy(2,2);print("██"+" "*85+" "+"██")
                    gotoxy(2,3);print("██"+" "*30+f"IMPRESIÓN DE LA FACTURA #{invoice_number}"+" "*30+"██")
                    gotoxy(5,5);print("*" * 84+reset_color) 

                    #*********************************************************
                    #Se define la longitud máxima de las etiquetas para alinear los valores
                    max_label_length = max(len(key) for key in invoice if key != 'detalle') + 1  

                    for key, value in invoice.items():
                        if key == 'detalle':
                            print(f"{key.title()}:") 
                            for i, detalle in enumerate(value, start=1):
                                print(f"Detalle {i}:")
                                for d_key, d_value in detalle.items():
                                    print(f"{' ' * 4}{d_key.title().ljust(max_label_length - 4)}: {d_value}")
                        else:
                            print(f"{key.title().ljust(max_label_length)}: {value}")

                    #*********************************************************
                    #Mostrar el menú de opciones
                    print(purple_color+"*" * 30+reset_color)  
                    x=input("presione una tecla para continuar...")
                    borrarPantalla() 
                    print('\033c', end='')
                    gotoxy(2,1);print(yellow_color+"█"*90)
                    gotoxy(2,2);print("██"+" "*30+"MODIFICACIÓN DE FACTURA"+" "*33+"██"+reset_color) 
                    gotoxy(32,4);print("💻 ¿Qué desea modificar?💻")
                    gotoxy(5,6);print("1. Fecha")
                    gotoxy(5,7);print("2. Cliente")
                    gotoxy(5,8);print("3. Subtotal")
                    gotoxy(5,9);print("4. Descuento")
                    gotoxy(5,10);print("5. Iva")
                    gotoxy(5,11);print("6. Total")
                    gotoxy(5,12);print(red_color+"7. Salir 🚶"+reset_color)
                    
                    #*********************************************************
                    gotoxy(5,14);print('Seleccione una opción:',end="")
                    gotoxy(5,14);opcion = validar.solo_numeros("Error: Solo numeros",28, 14)
                    
                    if str(opcion) == '1':
                        print(green_color)
                        gotoxy(5,16);print("Ingrese la nueva fecha (YYYY-MM-DD): ") 
                        gotoxy(5,16);nueva_fecha = validar.solo_fecha("Error: eso no es una fecha",43,16)
                        invoice["Fecha"] = nueva_fecha
                        
                    elif str(opcion) == '2':
                        print(green_color)
                        gotoxy(5,16);print("Ingrese el nombre del cliente: ")
                        gotoxy(5,16);nuevo_cliente = validar.solo_letras("Error: Solo letras",35,16).lower().capitalize()
                        if nuevo_cliente:
                            nuevo_cliente = nuevo_cliente.capitalize()
                            invoice["cliente"] = nuevo_cliente
                        else:
                            gotoxy(5,17);print(red_color+"No se ingresó un nuevo nombre. Manteniendo el cliente actual..."+reset_color)
                        
                    elif str(opcion) == '3':
                        print(green_color)
                        gotoxy(5,16);print("Ingrese el nuevo subtotal: ")
                        gotoxy(5,16);nuevo_subtotal = validar.solo_decimales("Error: Solo numeros",32,16) 
                        if nuevo_subtotal:
                            nuevo_subtotal = nuevo_subtotal
                            invoice["subtotal"] = float(nuevo_subtotal)
                        else:
                            gotoxy(5,17);print(red_color+"No se ingresó un nuevo subtotal. Manteniendo el subtotal actual..."+reset_color)
                        
                    elif str(opcion) == '4':
                        print(green_color)
                        gotoxy(5,16);print("Ingrese el nuevo descuento: ")
                        gotoxy(5,16);nuevo_descuento = validar.solo_decimales("Error: Solo numeros",34,16) 
                        if nuevo_descuento:
                            nuevo_descuento = nuevo_descuento
                            invoice["descuento"] = float(nuevo_descuento)
                        else:
                            gotoxy(5,17);print(red_color+"No se ingresó un nuevo descuento. Manteniendo el descuento actual..."+reset_color)
                        
                    elif str(opcion) == '5':
                        print(green_color)
                        gotoxy(5,16);print("Ingrese el nuevo IVA: ")
                        gotoxy(5,16);nuevo_iva = validar.solo_decimales("Error: Solo numeros",29,16) 
                        if nuevo_iva:
                            nuevo_iva = nuevo_iva
                            invoice["iva"] = float(nuevo_iva)
                        else:
                            gotoxy(5,17);print(red_color+"No se ingresó un nuevo iva. Manteniendo el iva actual..."+reset_color)
                        
                        
                    elif str(opcion) == '6':
                        print(green_color)
                        gotoxy(5,16);print("Ingrese el nuevo total: ")
                        gotoxy(5,16);nuevo_total = validar.solo_decimales("Error: Solo numeros",32,16)
                        if nuevo_total:
                            nuevo_total = nuevo_total
                            invoice["total"] = float(nuevo_total)
                        else:
                            gotoxy(5,17);print(red_color+"No se ingresó un nuevo total. Manteniendo el total actual..."+reset_color)
                        
                    elif str(opcion) == '7':
                        gotoxy(28,17);print(red_color+"⚠️ Operación de modificación cancelada ⚠️"+reset_color)
                        break
                    
                    else:
                        gotoxy(36,17);print(red_color+"🚫 Opción no válida 🚫"+reset_color)
                        break
                    
                    #*********************************************************
                    json_file.save(invoices)
                    gotoxy(32,18);print(cyan_color+"😄 Factura actualizada exitosamente 😄"+reset_color)
                    break

            if not invoice_found:
                gotoxy(32,10);print(cyan_color+f"😣 No se encontró la factura con el número {invoice_number} 😣"+reset_color)
                
        gotoxy(5,21);input("Presione una tecla para continuar...")
        
    def delete(self):
        print('\033c', end='')
        gotoxy(2,1);print(red_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"ELIMINAR FACTURA"+" "*36+"██")
        
        #*********************************************************
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices1 = json_file.read()
        gotoxy(42,3);print(grey_color+"Facturas"+reset_color)
        gotoxy(9,5);print(f"{'ID'.ljust(10)}{'Fecha'.ljust(20)}{'Cliente'.ljust(30)}{'Total'.rjust(10)}")
        gotoxy(7,6);print("-" * 80)

        #*********************************************************
        #Se muestran todas las facturas
        f = 7
        for fac in invoices1:
            id_str = str(fac['factura']).ljust(10)
            fecha_str = fac['Fecha'].ljust(20)
            cliente_str = fac['cliente'].ljust(30)
            total_str = f"{fac['total']:.2f}".rjust(10) 
            gotoxy(9, f);print(f"{id_str}{fecha_str}{cliente_str}{total_str}")
            f += 1
        print(reset_color)
        
        #*********************************************************
        invoice= input(grey_color+"\t Ingrese el número de la factura a eliminar: "+reset_color)
        if invoice.isdigit():
            invoices = json_file.delete("factura",int(invoice))
            print(red_color+"\n"+"\t"+"\t"+invoices+reset_color)
            time.sleep(1)
            
        else: 
            if invoice.isalpha():
                print(yellow_color+"\n"+"\t"+"\t"+"⚠️Tiene que ingresar un número entero⚠️"+reset_color)
                time.sleep(1)

#*********************************************************
#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()  
    print('\033c', end='')
    
    #*********************************************************
    menu_main = Menu("MENÚ FACTURACIÓN:",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    
    if opc == "1":
        opc1 = ''
        
        while opc1 !='5':
            borrarPantalla()  
            
            #*********************************************************
            #Muestra el menú de CLIENTES
            clients = CrudClients()
            menu_clients = Menu("Menu Clientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            
            #*********************************************************
            if opc1 == "1":
                clients.create()
                
            elif opc1 == "2":
                clients.update()
            
            elif opc1 == "3":
                clients.delete()
            
            elif opc1 == "4":
                clients.consult()
                
            elif opc1 == "5":
                pass
            print("Regresando al menu Clientes...")
    
    #*********************************************************           
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()
            
            #*********************************************************
            #Muestra el menú de PRODUCTOS
            products = CrudProducts()   
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            
            #*********************************************************
            if opc2 == "1":
                products.create()
                
            elif opc2 == "2":
                products.update()
            
            elif opc2 == "3":
                products.delete()
            
            elif opc2 == "4":
                products.consult()
    
    #*********************************************************       
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            
            #*********************************************************
            #Muestra el menú de VENTAS
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            
            #*********************************************************
            if opc3 == "1":
                sales.create()
                
            elif opc3 == "2":
                sales.consult()
            
            elif opc3 == "3":
                sales.update()
                
            elif opc3 == "4":
                sales.delete()
                time.sleep(2)
    
    #*********************************************************
    print("Regresando al menu Principal...")
    # time.sleep(2)            

#*********************************************************
borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()