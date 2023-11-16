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




