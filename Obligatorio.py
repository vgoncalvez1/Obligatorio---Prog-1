from datatime import datatime
import random

#Simulacion de la carrera

class Employee():

    Formato_fecha = "%d-%m-%Y"
    

    def __init__(self, id, nombre, nacionalidad, salario, cargo, fecha_nacimiento, score ) -> None:
        self._id, self._nombre, self._fecha_nacimiento, self._nacionalidad = id, nombre, fecha_nacimiento, nacionalidad
        self._salario, self._cargo, self._score = salario, cargo, score
        try: datatime.strptime(fecha_nacimiento, self._formato_fecha)
        except ValueError: raise ValueError(f"La fecha {fecha_nacimiento} no tiene el formato correcto. Debe ser DD-MM-YYYY")

class pilot(Employee):
    def __init__(self, id, nombre, fecha_nacimiento, nacionalidad, salario, numero_auto, lesion=False, es_reserva = False) -> None:
        super().__init__(id, nombre, fecha_nacimiento, nacionalidad, salario, "Piloto de reserva" if es_reserva else "Piloto")
        self._lesionado, self._numero_auto, self._es_reserva = lesion, numero_auto, es_reserva

class Mechanic(Employee):
    def __init__(self, id, nombre, nacionalidad, salario, fecha_nacimiento, score) -> None:
        super().__init__(id, nombre, nacionalidad, salario, fecha_nacimiento, 'Mecanico')
        self._score = score

class Team_Manager(Employee):
    def __init__(self, id, nombre, fecha_nacimiento, nacionalidad, salario) -> None:
        super().__init__(id, nombre, fecha_nacimiento, nacionalidad, salario, 'Director de Equipo')

class Car:
    def __init__(self, modelo, año, score) -> None:
        self._modelo, self._año, self._socre = modelo, año, score
    
class Unforeseen:
    def __init__(self) -> None:
        self._lesion, self._abandono, self._error_pits, self._penalizacion = False, False, 0, 0

class Team:
    def __init__(self, nombre) -> None:
            self._nombre, self._empleados, self._auto = nombre, [], None

    @property
    def nombre(self):
        return self._nombre
    
    @property
    def pilotos(self):
        return[e for e in self._empleados if isinstance(e, pilot)]
    
    def agregar_empleado(self, empleado):
        if isinstance(empleado, pilot) and len(self._pilotos) >= 2:
            print("Ya hay dos pilotos en este equipo. No se pueden ingresar mas")
        else:
            self._empleados.append(empleado)

    def asignar_auto(self, auto):
        self._auto = auto

def obtener_datos_empleados():
    id, nombre, nacionalidad = int(input("\nIngrese ID: ", int)), input("Ingrese nombre: ", str), input("Ingrese nacionalidad: ", str)
    edad, fecha_nacimiento = int(input("Ingrese edad: ", int)), ""
    while True:
        fecha_nacimiento = input("Ingrese fecha de nacimiento (DD-MM-YYYY): ")
        try:
            datatime.strptime(fecha_nacimiento, Employee.Formato_fecha)
        except ValueError: 
            print(f"La fecha '{fecha_nacimiento}' no tiene el formato correcto.")
        else:
            break
    salario, score = input("Ingrese salario", float), input("Ingrese score", int)
    numero_auto, puntaje_campeonato = input("Ingrese numero de auto ", int), input("Ingrese puntaje campeonato: ", int)
    lesionado_input = ""
    while lesionado_input not in ["si", "no"]:
        lesionado_input = input("¿Esta lesionado? (Si/No): ").lower().strip()
    lesionado = lesionado_input == "si"
    return id, nombre, nacionalidad, edad, fecha_nacimiento, salario, score, numero_auto, puntaje_campeonato, lesionado

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

def generar_imprevistos_aleatorios():
    imprevisto = Unforeseen()
    if random.random() < 0.10: imprevisto._lesion = True
    if random.random() < 0.05: imprevisto._abandono = True
    imprevisto._error_pits, imprevisto._penalizacion = random.randint(0, 3), random.randint(0, 2)
    return imprevisto

def simular_carrera(autos, equipos):
    pilotos = [p for e in equipos for p in e._pilotos if p._lesion is False] or [p for e in equipos for p in e._pilotos]
    if not pilotos or not autos: print("No hay pilotos ni autos suficientes para simular la carrera."); return
    imprevistos_pilotos = {p._id: generar_imprevistos_aleatorios() for p in pilotos}
    print("\nSimulacion...\n")
    resultados = [(p._nombre, 0) if imprevistos_pilotos[p._id]._abandono else (p._nombre, 10 + autos[0]._score + p._score - 5 * imprevistos_pilotos[p._id]._error_pits - 8 * imprevistos_pilotos[p._id]._penalizacion) for p in pilotos]
    resultados.sort(key=lambda x: x[1], reverse=True)
    print("Resultados de la carrera: ")
    puntos = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    for i, (nombre, score) in enumerate(resultados, 1):
        if i <= len(puntos): print(f"{i}. {nombre} - Score: {score:.2f} - Puntos Obtenidos: {puntos[i-1]}")
        else:
            print(f"{i}. {nombre} -Score: {score:.2f}")

def ralizar_consultas(equipos):
    while True:
        pass
