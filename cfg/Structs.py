from abc import ABC, abstractmethod
from enum import Enum

class GrandesAlianzas(Enum):
    ORDEN = "Orden"
    DESTRUCCION = "Destrucción"
    MUERTE = "Muerte"
    CAOS = "Caos"

class Facciones(Enum):
    
    #Orden - 8
    CITIES = "Cities of Sigmar"
    DAUGHTERS = "Daughters of Khaine"
    FYRESLAYERS = "Fyreslayers"
    IDONETH = "Idoneth Deepkin"
    KHARADRON = "Kharadron Overlords"
    LUMINETH = "Lumineth Realm-lords"
    SERAPHON = "Seraphon"
    STORMCAST = "Stormcast Eternals"
    SYLVANETH = "Sylvaneth"
    
    #Muerte - 4
    FLESH = "Flesh-eater Courts"
    NIGHTHAUNT = "Nighthaunt"
    OSSIARCH = "Ossiarch Bonereapers"
    SOULBLIGHT = "Soulblight Gravelords"
    
    #Caos - 7
    KHORNE = "Blades of Khorne"
    TZEENTCH = "Disciples of Tzeentch"
    SLAANESH = "Hedonites of Slaanesh"
    NURGLE = "Maggotkin of Nurgle"
    SKAVEN = "Skaven"
    SLAVES = "Slaves to Darkness"
    BEASTS = "Beasts of Chaos"
    
    #Destrucción - 5
    GOBLINS = "Gloomspite Gitz"
    OGOR = "Ogor Mawtribes"
    ORRUK = "Orruk Warclans"
    SONS = "Sons of Behemat"
    
    #Scenery - 1
    SCENOGRAPHY = "Escenografía"
    
class Tipo_WH(Enum):
    MINIATURA = "Miniatura"
    REGIMIENTO = "Regimiento"
    BANDA = "Banda"

class Warhammer(ABC):
    @abstractmethod
    def __init__(self,nombre,faccion):
        super().__init__()
        self.nombre = nombre
        self.faccion = Facciones(faccion)

# Miniatura es una sola figura (por ejemplo, heroes, monstruos, etc)
class Miniatura(Warhammer):
    def __init__(self):
        super().__init__()

# Regimiento es grupo de miniaturas iguales (por ejemplo, 10 goblins nocturnos) 
class Regimiento(Warhammer):
    def __init__(self, cantidad):
        super().__init__()
        self.cantidad = cantidad

# Banda es grupo de miniaturas diferentes (por ejemplo, Underworlds, Morgheim, etc)
class Banda(Warhammer):
    def __init__(self, cantidad, nombres):
        super().__init__()
        self.cantidad = cantidad
        self.nombres = nombres #Lista de todos los nombres 
        
class Environment(Warhammer):
    def __init__(self):
        super().__init()