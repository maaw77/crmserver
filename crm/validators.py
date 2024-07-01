from pydantic import BaseModel, ValidationError, field_validator
import datetime


# Defining classes to validate input data.
class DateActionValidator(BaseModel):
    date_action: datetime.date


class GsmTableValidator(BaseModel):
    """Priem"""
    dt_receiving: datetime.date | str  # Data priemki
    dt_crch: datetime.date | str  # Data sozdaniya ili posledney pravki
    site: str  # Uchastok
    income_kg: float   # Prinyato v kg
    operator: str  # Operator
    provider: str  # Postavshik
    contractor: str  # Perevozshik
    license_plate: str   # GOS nomer
    status: str  # Zagruzgen
    been_changed: bool   # table_color = '#f7fcc5' = True

    @field_validator('dt_crch', 'dt_receiving')
    @classmethod
    def check_valid_date(cls, in_date: datetime.date) -> str:
        if in_date == datetime.date.min:
            return ''
        return str(in_date)


class TankTableValidator(BaseModel):
    """Vidacha v ATZ"""
    dt_giveout: datetime.date | str   # Data vidachi
    dt_crch: datetime.date | str  # Data sozdaniya ili posledney pravki
    site: str   # Uchastok
    onboard_num:  str   # Bortovoi nomer
    dest_site: str   # Uchastok naznacheniya
    given_kg: float # Vidano v kg
    status: str  # Zagruzgen
    been_changed: bool  # table_color = '#f7fcc5' = True

    @field_validator('dt_crch', 'dt_giveout')
    @classmethod
    def check_valid_date(cls, in_date: datetime.date) -> str:
        if in_date == datetime.date.min:
            return ''
        return str(in_date)


class SheetTableValidator(BaseModel):
    """Vidacha  iz ATZ"""
    dt_giveout: datetime.date | str   # Data vidachi
    dt_crch: datetime.date | str  # Data sozdaniya ili posledney pravki
    site: str  # Uchastok
    atz: str  # ATZ
    give_site: str   # Uchastok vidachi
    given_litres: float   # Vidano v litres
    given_kg: float  # Vidano v kg
    status: str  # Zagruzgen
    been_changed: bool   # table_color = '#f7fcc5' = True

    @field_validator('dt_crch', 'dt_giveout')
    @classmethod
    def check_valid_date(cls, in_date: datetime.date) -> str:
        if in_date == datetime.date.min:
            return ''
        return str(in_date)


class AZSTableValidator(BaseModel):
    """Vidacha  iz TRK"""
    dt_giveout: datetime.date | str  # Data vidachi
    dt_crch: datetime.date | str  # Data sozdaniya ili posledney pravki
    site: str  # Uchastok
    storekeeper: str  # FIO kladovchika
    counter_azs_bd: float  # Shetchik nachalo dnya
    counter_azs_ed: float  # Shetchik konec dnya
    given_litres: float  # Vidano v litres za sutki
    given_kg: float  # Vidano v kg za sutki
    status: str  # Zagruzgen
    been_changed: bool  # table_color = '#f7fcc5' = True

    @field_validator('dt_crch', 'dt_giveout')
    @classmethod
    def check_valid_date(cls, in_date: datetime.date) -> str:
        if in_date == datetime.date.min:
            return ''
        return str(in_date)


class ExchangeTableValidator(BaseModel):
    """Obmen megdu rezervuarami"""
    dt_change: datetime.date | str  # Data obmena
    dt_crch: datetime.date | str  # Data sozdaniya ili posledney pravki
    site: str  # Uchastok
    operator: str  # Operator
    tanker_in: str  # Ishodniy rezervuar
    tanker_out: str  # Konechniy rezervuar
    litres: float  # Obyom topliva
    been_changed: bool  # table_color = '#f7fcc5' = True
    status: str  # Zagruzgen

    @field_validator('dt_crch', 'dt_change')
    @classmethod
    def check_valid_date(cls, in_date: datetime.date) -> str:
        if in_date == datetime.date.min:
            return ''
        return str(in_date)


class RemainsTableValidator(BaseModel):
    """Snyatie ostatkov"""
    dt_inspection: datetime.date | str  # Data obmena
    site: str  # Uchastok
    inspector: str   # FIO proveryayshego
    tanker_num: str  # Nomer emkosti
    remains_kg: float  # Ostatki (kg)
    fuel_mark: str  # Marka topliva
    status: str  # Zagruzgen

    @field_validator('dt_inspection')
    @classmethod
    def check_valid_date(cls, in_date: datetime.date) -> str:
        if in_date == datetime.date.min:
            return ''
        return str(in_date)


if __name__ == '__main__':
    print(DateActionValidator(date_action='2025-04-01'))
    in_data = {'dt_receiving': datetime.date(2024, 5, 1),
               'dt_crch': datetime.date(1, 1, 1),
               'been_changed': False, 'site': 'АНДАТ', 'income_kg': 27379.80078125,
               'operator': 'КУЗЬМИНА', 'provider': 'ООО "ТК-ЛЕГИОН"',
               'contractor': 'ООО "ТК ЛЕГИОН"', 'license_plate': 'Х837РК',
               'status': 'Загружен'}
    print(GsmTableValidator(**in_data))

    in_data = {'dt_giveout': datetime.date(2024, 5, 1),
               'dt_crch': datetime.date(1, 1, 1), 'been_changed': False, 'site': 'МАГЫЗЫ',
               'onboard_num': '90260 (C445KP124) НЕФАЗ 66062', 'dest_site': 'УСТЬ-ВЕСЕЛЫЙ ',
               'given_kg': 4772.7998046875, 'status': 'Загружен'}
    print(TankTableValidator(**in_data))

    in_data = {'dt_giveout': datetime.date(2024, 5, 1),
               'dt_crch': datetime.date(1, 1, 1),
               'been_changed': False, 'site': 'ИЛЬИНСКИЙ-ПЕТРОПАВЛОВСКИЙ', 'atz': 'АТЗ - 22139 (H370PH124) ',
               'give_site': 'ИЛЬИНСКИЙ-ПЕТРОПАВЛОВСКИЙ', 'given_litres': 149.0, 'given_kg': 125.9000015258789,
               'status': 'Загружен'}
    print(SheetTableValidator(**in_data))

    in_data = {'dt_giveout': datetime.date(2024, 5, 1),
               'dt_crch': datetime.date(2024, 5, 17),
               'been_changed': False, 'site': 'ГОРЕЛАЯ',
               'storekeeper': 'ЗЫЛЬ Е.С.', 'counter_azs_bd': 0.0, 'counter_azs_ed': 62.0,
               'given_litres': 62.0, 'given_kg': 47.599998474121094, 'status': 'Загружен'}
    print(AZSTableValidator(**in_data))

    in_data = {'dt_change': datetime.date(2024, 5, 1),
                'dt_crch': datetime.date(1, 1, 1),
                'been_changed': False, 'site': 'ИЛЬИНСКИЙ СЕВЕРО-ЕНИСЕЙСКИЙ',
                'operator': 'ЗВЕЙНИК А.В.',
                'tanker_in': 'АТЗ - 90085 (C003РУ55) ', 'tanker_out': 'Емкость №2 (ДТ ЛЕТНЕЕ)',
                'litres': 1660.0, 'status': 'Загружен'}
    print(ExchangeTableValidator(**in_data))

    in_data = {'dt_inspection': datetime.date(2024, 5, 1),
               'site': 'НАДЕЖДА', 'inspector': 'КОРОБЕЙНИКОВ', 'tanker_num': 'ЕВРОКУБ БЕНЗИН (100007) ',
               'remains_kg': 0.0, 'fuel_mark': 'АИ-92', 'status': 'Загружен'}
    print(RemainsTableValidator(**in_data))


