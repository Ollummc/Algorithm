from enum import Enum
class FacilityEnum (Enum):
    AC = "Acut-Care"
    LTC = "Long-Term_Care"
    AS = "Ambulant_Service"
    PC = "Pediatrics_Care"
    PSYC = "Psychiatric_Care"

class AreaHours (Enum):
    AC = 400
    LTC = 400
    AS = 400
    PC = 120
    PSYC = 120