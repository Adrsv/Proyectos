def menu():
    print('1. Agregar')
    print('2. Mostrar')
    print('3. Modificar')
    print('4. Buscar')
    print('5. Eliminar')
    print('6. Salir')
    
    option = 0
    while option != 6:
        option = int(input('Ingrese una opcion: '))
        
        if option == 1:
            agregar()
        if option == 2:
            mostrar()
        if option == 3:
            modificar()
        if option == 4:
            buscar()
        if option == 5:
            eliminar()
        if option == 6:
            break
    
def verificar_producto(producto):
    with open('stock.txt', 'r') as file:
        for line in file:
            if producto in line:
                return True
    return False

#Funcion agregar, opcion 1
def agregar():
    #Inicia el loop
    while True:
        #Entrada de datos del producto
        producto = input('Ingrese el nombre del producto, para finalizar escriba "fin": ').lower().strip() #lower(poner en minusculas) strip(quitar los espacios al inicio y final)
        #Si el usuario ingresa 'fin' se termina el loop
        if producto.lower() == 'fin':
            break
        #Verificacion del producto en el stock
        if verificar_producto(producto):
            print(f'El producto {producto} ya existe')
        else:
            #Si no existe, se ingresa la cantidad del producto equivalente
            cantidad = int(input('Ingrese la cantidad: '))
            #Abre el archivo stock.txt con el modo de escritura al final 'a' y agrega el producto con su cantidad
            with open('stock.txt', 'a') as file:
                file.write(f'{producto} : {cantidad}\n')
            print('Producto agregado')

#Funcion mostrar, opcion 2
def mostrar():
    with open('stock.txt', 'r') as file:
        for line in file:
            print(line.strip())

#Funcion modificar, opcion 3
def modificar():
    #Se ingresa el nombre del producto a modificar
    producto = input('Ingrese el producto a modificar: ').lower().strip()
    #Se verifica si no esta en el stock
    if not verificar_producto(producto):
        print(f'El producto {producto} no existe en el stock')
    else:
        #Si esta, se ponen los nuevos valores
        producto_nuevo = input('Ingrese el nombre del producto: ').lower().strip()
        cantidad_nueva = int(input('Ingrese la cantidad del producto: '))
        #Se abre el archivo de texto en modo lectura 'r'
        with open('stock.txt', 'r') as file:
            lines = file.readlines()
        #Se abre el archivo de texto en modo escritura 'w'
        with open('stock.txt', 'w') as file:
            for line in lines:
                if producto in line:
                    #Se verifica si la variable no esta vacia
                    if producto_nuevo != '':
                        file.write(f'{producto_nuevo} : {cantidad_nueva}\n')
                    else:
                        #Si esta vacia, se coloca el nombre original, pero se puede cambiar el valor de la cantidad
                        file.write(f'{producto} : {cantidad_nueva}\n')
                else:
                    file.write(line)

#Funcion buscar, opcion 4
def buscar():
    encontrado = False
    #Se ingresa el nombre del producto a buscar
    producto_buscado = input('Ingrese el producto a buscar: ').lower().strip() 
    #Se verifica que el producto buscado no este en el stock
    if not verificar_producto(producto_buscado):
        print(f'El producto {producto_buscado} no existe en el stock')
    else:
        #Si el producto se encuentra en el stock, se abre el archivo de texto en modo lectura 'r'
        with open('stock.txt', 'r') as file:
            #Se recorre linea por linea del archivo 
            for line in file:
                producto, cantidad = line.strip().split(':')
                #Si el producto del stock coincide con el buscado, se muestra en pantalla y la variable encontrado pasa a valer True finalizando el loop
                if producto.strip() == producto_buscado:
                    print(f'Producto encontrado: {producto} - Cantidad: {cantidad}')
                    encontrado = True
                    break
        #Si la variable encontrado sigue siendo False, se muestra el siguiente mensaje
        if not encontrado:
            print(f'El producto {producto_buscado} no se encuentra en el stock')

#Funcion eliminar, opcion 5
def eliminar():
    #Ingresa el nombre del producto a eliminar
    producto = input('Ingrese el nombre del producto a eliminar: ').lower().strip()
    #Se verifica si no existe el producto ingresado en el stock
    if not verificar_producto(producto):
        print(f'El producto {producto} no existe en el stock')
    #De existir el producto, se elimina del stock
    else:
        #Se abre el archivo en modo lectura 'r' para verificar que este el producto
        with open('stock.txt', 'r') as file:
            lines = file.readlines()
        #Se abre el archivo en modo de escritura 'w' para reemplazar el espacio eliminado con los productos de las siguientes lineas
        with open('stock.txt', 'w') as file:
            for line in lines:
                if producto not in line:
                    file.write(line)
        print(f'El producto {producto} ah sido eliminado')
        
menu() #Inicia el programa principal