from datetime import datetime

import random

class Empleado():
    Formato_fecha = "%d-%m-%Y"
    def __init__(self, id, nombre, nacionalidad, salario, fecha_nacimiento):
        self.id = id
        self.nombre = nombre
        self.nacionalidad = nacionalidad
        self.salario = salario
        self.fecha_nacimiento = fecha_nacimiento

class Piloto(Empleado):
    def __init__(self, id, nombre, nacionalidad, salario,fecha_nacimiento, score, num_auto):
        super().__init__(id, nombre, nacionalidad, salario,fecha_nacimiento )
        self.score = score
        self.num_auto = num_auto
        self.score_carrera = 0
        self.lesionado = False
        self.equipo = None
        self.puntaje_campeonato = 0
        self.abandono = False
        self.pilotos_abandonan = []

class PilotoReserva(Empleado):
    def __init__(self, id, nombre, fecha_nacimiento, nacionalidad, salario, score, num_auto, piloto_reemplazado=None):
        super().__init__(id, nombre, fecha_nacimiento, nacionalidad, salario)
        self.score = score
        self.num_auto = num_auto
        self.puntaje_campeonato = 0
        self.lesionado = False
        self.equipo = None
        self.piloto_reemplazado = piloto_reemplazado


class Mecanico(Empleado):
    def __init__(self, id, nombre, fecha_nacimiento, nacionalidad, salario, score):
        super().__init__(id, nombre, fecha_nacimiento, nacionalidad, salario)
        self.score = score
        self.equipo = None

class DirectorEquipo(Empleado):
    def __init__(self, id, nombre, fecha_nacimiento, nacionalidad, salario):
        super().__init__(id, nombre, fecha_nacimiento, nacionalidad, salario)
        self.equipo = None


class Auto:
    def __init__(self, modelo, año, score):
        self.modelo = modelo
        self.año = año
        self.score = score

class Equipo:
    def __init__(self, nombre, modelo_auto, pilotos_titulares, pilotos_reserva, mecanicos):
        self.nombre = nombre
        self.modelo_auto = modelo_auto
        self.pilotos_titulares = pilotos_titulares
        self.pilotos_reserva = pilotos_reserva
        self.mecanicos = mecanicos
        self.pilotos = pilotos_titulares   

def valida_opcion(minimo, maximo):
    while True:
        try:
            opcion = int(input(f"\nSeleccione una opcion ({minimo} - {maximo}): "))
            if minimo <= opcion <= maximo: return opcion
            else:
                print(f"Ingrese una opcion entre {minimo} y {maximo}.")
        except ValueError: 
            print("Ingrese un numero valido.")

def input_validado(mensaje, tipo):
    while True:
        valor = input(mensaje)
        try:
            if tipo == int: return int(valor)
            elif tipo == float: return float(valor)
            elif tipo == str and valor: return valor.strip()
            else:
                print("Valor invalido. Ingrese uno de nuevo.")
        except ValueError:
            print("Valor invalido. Ingrese uno de nuevo.")

def obtener_pilotos(self,empleados_totales):
    pilotostotales = []
    for empleado in empleados_totales:
        if isinstance(empleado, Piloto) or isinstance(empleado, PilotoReserva):
            pilotostotales.append(empleado)
    return pilotostotales

def convertir_enteros(autos):
    return [int(auto_num) for auto_num in autos if auto_num.strip().isdigit()]

def asignar_puntos(pilotos_en_carrera):
    puntos = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

    for piloto in pilotos_en_carrera:
        suma_score_mecanicos = sum(mecanico.score for mecanico in piloto.equipo.mecanicos)
        score_auto = piloto.equipo.modelo_auto.score
        score_piloto = piloto.score
        cantidad_errores_en_pits = piloto.errores_pits
        cantidad_penalidad_infringir_norma = piloto.penalidades
        piloto.score_final = suma_score_mecanicos + score_auto + score_piloto - 5 * cantidad_errores_en_pits - 8 * cantidad_penalidad_infringir_norma
   
    pilotos_en_carrera.sort(key=lambda piloto: piloto.score_final, reverse=True)
    for i, piloto in enumerate(pilotos_en_carrera):
        if i < len(puntos):
            piloto.puntos += puntos[i]
            print(f"{piloto.nombre} ha ganado {puntos[i]} puntos.")
            

def reiniciar_estado_pilotos(equipos_totales):
    for equipo in equipos_totales:
        for piloto in equipo.pilotos_titulares + equipo.pilotos_reserva:
            piloto.lesionado = False
            piloto.abandono = False
            piloto.score_carrera = 0
            piloto.score_final = 0
def imprimir_mejores_pagados(empleados_totales):
    pilotos_titulares = [empleado for empleado in empleados_totales if isinstance(empleado, Piloto)]
    pilotos_reserva = [empleado for empleado in empleados_totales if isinstance(empleado, PilotoReserva)]

    todos_los_pilotos = pilotos_titulares + pilotos_reserva

    if len(todos_los_pilotos) < 5:
        print("No hay suficientes pilotos para mostrar los 5 mejores pagados.")
        return

    mejores_pagados = sorted(todos_los_pilotos, key=lambda piloto: piloto.salario, reverse=True)[:5]

    print("\nLos 5 pilotos mejor pagados son:")
    for i, piloto in enumerate(mejores_pagados, start=1):
        print(f"{i}. {piloto.nombre} - Salario: {piloto.salario}")

def imprimir_top_score(empleados_totales):
    pilotos_titulares = [empleado for empleado in empleados_totales if isinstance(empleado, Piloto)]
    pilotos_reserva = [empleado for empleado in empleados_totales if isinstance(empleado, PilotoReserva)]

    todos_los_pilotos = pilotos_titulares + pilotos_reserva

    if len(todos_los_pilotos) < 3:
        print("No hay suficientes pilotos para mostrar el top 3 de mayor score.")
        return

    top_score = sorted(todos_los_pilotos, key=lambda piloto: piloto.score, reverse=True)[:3]

    print("\nEl top 3 de pilotos con mayor score es:")
    for i, piloto in enumerate(top_score, start=1):
        print(f"{i}. {piloto.nombre} - Score: {piloto.score}")

def ordenar_participantes(equipos):
     return sorted([participante for equipo in equipos for participante in equipo.obtener_pilotos() if isinstance(participante, (Piloto, PilotoReserva))], key=lambda participante: participante.score_final, reverse=True)


def simular_carrera(equipos_totales,autos_totales):
        lesionados = input("Ingrese numero de auto  los pilotos lesionados (separados por coma): ").split(',')
        abandonos = input("Ingrese numero auto los pilotos que abandonan (separados por coma): ").split(',')
        errores_pits = input("Ingrese numero de auto los pilotos que cometen error en pits (separados por coma): ").split(',')
        penalizaciones = input("Ingrese numero de auto  los pilotos que reciben penalidad por infringir una norma(separados por coma): ").split(',')

        lesionados = convertir_enteros(lesionados)
        abandonos = convertir_enteros(abandonos)
        errores_pits = convertir_enteros(errores_pits)
        penalizaciones = convertir_enteros(penalizaciones)

        for piloto in obtener_pilotos(equipos_totales):
            if piloto.numero_auto in lesionados:
                piloto.lesionado = True
            if piloto.numero_auto in abandonos:
                piloto.abandono = True 
            if piloto.lesionado or piloto.abandono:
                piloto.score_final = 0

        pilotos_en_carrera = [piloto for piloto in obtener_pilotos(equipos_totales) if not piloto.abandono and not piloto.lesionado]

        asignar_puntos(pilotos_en_carrera)

        reiniciar_estado_pilotos(obtener_pilotos(equipos_totales))
        
        print("\nResultados de la carrera:")
        for i, participante in enumerate(pilotos_carrera):
            print(f"{i + 1}. {participante.nombre} ({participante.score_final})")

        print("\nPuntos asignados:")
        for i, (posicion, nombre, puntos_ganados) in enumerate(puntos_asignados(participantes_ordenados[:10])):
            print(f"{posicion}. {nombre} ({puntos_ganados})")


def realizar_consultas(equipos_totales,empleados_totales):
    while True:
        print("\nSeleccione una opcion.")
        print("1. Top 10 pilotos con mas puntos en el campeonato.")
        print("2. Resumen campeonato de constructores (equipos).")
        print("3. Top 5 pilotos mejor pagados.")
        print("4. Top 3 pilotos mas habilidosos.")
        print("5. Retornar jefes de equipo.")
        print("6. Volver al menu principal.")
        opcion = valida_opcion(1, 6)
        if opcion == 1:    
            imprimir_top_score(empleados_totales)
        if opcion == 2:
            print("opcion 2")
        if opcion == 3:
            imprimir_mejores_pagados(empleados_totales)
        if opcion == 4:
            print("opcion 4")
        if opcion == 5:
            print("opcion 5")
        if opcion == 6:
            return

def main():
    empleados_totales = []
    autos_totales = []
    equipos_totales=[]
    while True:
        print("1. Alta de empleado.")
        print("2. Alta de auto.")
        print("3. Alta de equipo.")
        print("4. Simular carrera.")
        print("5. Realizar consultas.")
        print("6. Finalizar programa.")
        opcion = valida_opcion(1, 6)

        if opcion == 1:
            try:
                id = int(input("Ingrese cedula: "))
                nombre = input("Ingrese nombre: ")
                fecha_nacimiento = input("Ingrese fecha de nacimiento (DD-MM-YYYY): ")
                datetime.strptime(fecha_nacimiento, Empleado.Formato_fecha)
                nacionalidad = input("Ingrese nacionalidad: ")
                salario = float(input("Ingrese salario: "))
                tipo_empleado = input("\nSeleccione el tipo de empleado (Piloto/Piloto Reserva/Mecanico/Director) o 'Salir' para volver al menu principal: ").lower()
                if tipo_empleado not in ["piloto","piloto reserva","mecanico", "director", "salir"]:
                    print("Tipo de empleado invalido.")
                if tipo_empleado == "salir":break

                if tipo_empleado == "piloto":
                    print("Ingrese score (1-99): ")
                    score = valida_opcion(1, 99)
                    num_auto = int(input("Ingrese numero de auto: "))
                    piloto = Piloto(id,nombre,nacionalidad,salario,fecha_nacimiento,score,num_auto)

                    empleados_totales.append(piloto)

                if tipo_empleado == 'piloto reserva':
                    print("Ingrese score (1-99): ")
                    score = valida_opcion(1, 99)
                    num_auto = int(input("Ingrese número de auto: "))
                    pilotodereserva = PilotoReserva(id, nombre, fecha_nacimiento,salario,nacionalidad, score, num_auto)
                    empleados_totales.append(pilotodereserva)

                if tipo_empleado == "mecanico":
                    print("Ingrese score (1-99): ")
                    score = valida_opcion(1, 99)
                    mecanico = Mecanico(id, nombre, fecha_nacimiento, nacionalidad, salario, score)
                    empleados_totales.append(mecanico)

                if tipo_empleado == "director":
                    dir_equipo= DirectorEquipo(id, nombre, fecha_nacimiento, nacionalidad, salario)
                    empleados_totales.append(dir_equipo)
            except ValueError:
                print(f"Error datos invalidos")
                
        if opcion == 2:
             modelo = input("Ingrese modelo de auto: ")
             score = input_validado("Ingrese score: ", int)
             año = input("Ingrese año del auto")
             auto=Auto(modelo,año,score)
             autos_totales.append(auto)
             print(f"Auto modelo: {modelo} del año {año} con un score de:{score} ha sido ingresado correctamente.")

             
        if opcion == 3:#nombre, modelo_auto, pilotos_titulares, pilotos_reserva, mecanicos
            nombre = input("Ingrese nombre del equipo:")

            pilotos_disponibles = [piloto for piloto in empleados_totales if isinstance(piloto, Piloto) and piloto.equipo is None]
            pilotos_disponibles = sorted(pilotos_disponibles, key=lambda piloto: piloto.score, reverse=True)
            
            pilotosres_disponibles = [piloto for piloto in empleados_totales if isinstance(piloto, PilotoReserva) and piloto.equipo is None]
            pilotosres_disponibles = sorted(pilotosres_disponibles, key=lambda piloto: piloto.score, reverse=True)
            
            mecanicos_disponibles = [mecanico for mecanico in empleados_totales if isinstance(mecanico, Mecanico) and mecanico.equipo is None]
            mecanicos_disponibles = sorted(mecanicos_disponibles, key=lambda mecanico: mecanico.score, reverse=True)

            dir_disponible = [director for director in empleados_totales if isinstance(director,DirectorEquipo) and director.equipo is None]

            if len(pilotos_disponibles) < 2:
                print("No hay 2 pilotos disponibles.")
                break
            else:
                print("Pilotos disponibles para asignar al equipo:")
                for index, piloto in enumerate(pilotos_disponibles, start=1):
                    print(f"{index}. {piloto.nombre} - Score: {piloto.score} ID {piloto.id}")

            piloto_seleccionados = []

            for x in range(2): 
                while True:
                    try:
                        id_titular = int(input("Ingrese el ID del piloto titular: "))
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
                        continue

                    piloto_seleccionado = None
                    for piloto in pilotos_disponibles:
                        if piloto.id == id_titular:
                            piloto_seleccionado = piloto
                            break

                    if piloto_seleccionado:
                        piloto_seleccionados.append(piloto_seleccionado)
                        pilotos_disponibles.remove(piloto_seleccionado)  
                        break
                    else:
                        print("ID de piloto no válido. Intente nuevamente.")
            
            
            if len(pilotosres_disponibles) < 1:
                print("No hay pilotos de reserva disponibles.")
            else:
                print("Pilotos de reserva disponibles para asignar al equipo:")
                for index, piloto in enumerate(pilotosres_disponibles, start=1):
                    print(f"{index}. {piloto.nombre} - Score: {piloto.score} ID {piloto.id}")

            reserva_seleccionados = []
            while True:
                try:
                    id_reserva = int(input("Ingrese el ID del piloto de reserva: "))
                except ValueError:
                    print("Por favor, ingrese un número válido.")
                    continue

                res_seleccionado = None
                for reserva in pilotosres_disponibles:
                    if reserva.id == id_reserva:
                        res_seleccionado = reserva
                        break

                if res_seleccionado:
                        reserva_seleccionados.append(res_seleccionado)
                        pilotosres_disponibles.remove(res_seleccionado)  
                        break 
                else:
                    print("ID de piloto no válido. Intente nuevamente.")
                
                reserva = PilotoReserva(
                    id=reserva_seleccionados.id,
                    nombre=reserva_seleccionados.nombre,
                    fecha_nacimiento=reserva_seleccionados.fecha_nacimiento,
                    nacionalidad=reserva_seleccionados.nacionalidad,
                    salario=reserva_seleccionados.salario,
                    score=reserva_seleccionados.score,
                    num_auto=reserva_seleccionados.num_auto,
                    piloto_reemplazado=reserva_seleccionados
                    )
            mecanico_seleccionados = []
            if len(mecanicos_disponibles)<8:
                    print("No hay mecanicos disponibles.")
            else:
                print("Mecanicos disponibles para asignar al equipo:")
                for index, piloto in enumerate(mecanicos_disponibles, start=1):
                    print(f"{index}. {piloto.nombre} - Score: {piloto.score} ID {piloto.id}")
            for i in range(8):
                while True:
                    try:
                        id_mecanico= int(input("Ingrese el ID del mecanico: "))
                    except ValueError:
                        print("Por favor, ingrese un numero valido.")
                        continue
                    mecanico_seleccionado= None
                    for mecanico in mecanicos_disponibles:
                        if mecanico.id == id_mecanico:
                            mecanico_seleccionado = mecanico
                            break
                    if mecanico_seleccionado:
                        mecanico_seleccionados.append(mecanico_seleccionado)
                        mecanicos_disponibles.remove(mecanico_seleccionado)
                        break
                    else:
                        print("Id de mecanico no valida.Intente Nuevamente")

            director_seleccionados = []

            if len(dir_disponible)<1:
                print("No hay directores de equipo disponibles.")
            else:
                print("Directores disponibles para asignar al equipo:")
                for index, piloto in enumerate(dir_disponible, start=1):
                    print(f"{index}. {piloto.nombre} - ID {piloto.id}")
            while True:
                try:
                    id_director= int(input("Ingrese el ID del director: "))
                except ValueError:
                    print("Por favor, ingrese un numero valido.")
                    continue
                director_seleccionado= None
                for director in dir_disponible:
                    if director.id == id_director:
                        director_seleccionado = director
                        break
                if director_seleccionado:
                    director_seleccionados.append(director_seleccionado)
                    dir_disponible.remove(director_seleccionado)
                    break
                else:
                    print("Id de director no valida.Intente Nuevamente")
            autos_disp = [auto for auto in autos_totales]
            if not autos_disp:
                print("No hay autos disponibles.")
                break
            else:
                print("\nAutos disponibles:")
                for i, auto in enumerate(autos_disp, 1):
                    print(f"{i}. {auto.modelo} - Año: {auto.año}")

                while True:
                    try:
                        indice_auto = int(input("Seleccione el número del auto: "))
                        auto_seleccionado = autos_disp[indice_auto - 1]
                        break
                    except (ValueError, IndexError):
                        print("Número de auto no válido. Intente nuevamente.")

            equipo = Equipo(nombre, auto_seleccionado, piloto_seleccionados, reserva_seleccionados, mecanico_seleccionados)
            equipos_totales.append(equipo)
            print("Equipo creado correctamente")

        if opcion == 4:
            simular_carrera(equipos_totales,autos_totales)
        if opcion == 5:
            realizar_consultas(equipos_totales, empleados_totales)
        if opcion == 6:
            exit()


if __name__ == "__main__":
    main()