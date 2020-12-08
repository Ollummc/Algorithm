from enum import Enum
class FacilityEnum (Enum):
    AC = "Acut-Care"
    LTC = "Long-Term_Care"
    AS = "Ambulant_Service"
    PC = "Pediatrics_Care"
    PSYC = "Psychiatric_Care"

class AreaHours (Enum):
    AC = 2#6#400
    LTC = 2#6#400
    AS = 2#6#400
    PC = 2#2#120
    PSYC =2 #2#120
class InternalAssignments (Enum):
    ORI = "Orientation-Phase"
    ELE1 = "Elective 1"
    ELE2 = "Elective 2"
    SPEC = "Specialization"