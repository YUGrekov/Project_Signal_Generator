'''Заполнение таблицы разработки AI.'''
import re
import traceback
from model_new import AI
from model_new import Signals
from request_sql import RequestSQL
from general_functions import General_functions

T_SIGNALS = 'signals'


class AIParam():
    '''Общие параметры для аналогового сигнала по умолчанию.'''
    AnalogGroupId = 'Общестанционные'
    IsOilPressure = False
    IsPumpVibration = None
    IsEDVibration = None
    IsEDAmperage = None
    IsAuxPressure = None
    NumberUstMinAvar = 3
    NumberUstMinWarn = 2
    NumberUstMaxWarn = 2
    NumberUstMaxAvar = 3
    LoLim = 3900
    LoLimField = 4000
    LoLimEng = 0
    HiLimEng = 100
    HiLimField = 20000
    HiLim = 20100
    Histeresis = 0
    TimeFilter = 0
    Usts = [None, None, None, None, None, None,
            None, None, None, None, None, None]
    SigMask = '0000_0000_0000_0000'
    MsgMask = '0100_0000_0000_0001'
    CtrlMask = '0000_1111_0000_1111'
    Precision = 1
    DeltaT = 0.1
    PhysicEGU = 'мкА'


class AIParamVibr(AIParam):
    '''Параметры для аналогового сигнала вибрации.'''
    SetpointGroupId = 'Вибрации'
    EGU = 'мм/с'
    NumberUstMinWarn = 1
    NumberUstMaxWarn = 1
    LoLim = 3700
    HiLimEng = 30
    HiLim = 21600
    RuleName = 'Вибрации'

    def prepare(self):
        if 'насос' in self.name:
            AIParamVibr.AnalogGroupId = 'Вибрации насоса'
            AIParamVibr.IsPumpVibration = 1
            AIParamVibr.Usts = [None, None, None, 3, 7.1, 5.6,
                                8.9, 8.9, 7.1, 11.2, 11.2, 18]
            AIParamVibr.MsgMask = '0111_1111_0111_0001'
        else:
            AIParamVibr.AnalogGroupId = 'Вибрации ЭД'
            AIParamVibr.IsEDVibration = 1
            AIParamVibr.Usts = [None, None, None, 3, 7.1, 6,
                                None, 8.9, 7.1, None, 11.2, 18]
            AIParamVibr.MsgMask = '0111_0110_0111_0001'
        if 'вертик' in self.name:
            AIParamVibr.Sign = 'Xверт'
        elif 'горизонт' in self.name:
            AIParamVibr.Sign = 'Xгор'
        elif 'попереч' in self.name:
            AIParamVibr.Sign = 'Xпоп'
        else:
            AIParamVibr.Sign = 'X'
        AIParamVibr.SetpointGroupId = 'Вибрации ' + ('ПНА ' if 'ПНА' in self.name else 'МНА ') + self.tag[2:1]
        AIParamVibr.NumberNAorAux = self.tag[2:1]


class AIParamMoving(AIParam):
    """Параметры для аналогового сигнала осевого смещения."""
    AnalogGroupId = 'Осевые смещения'
    Sign = 'Xос'
    EGU = 'мм'
    IsEDVibration = 1
    NumberUstMinWarn = 1
    NumberUstMaxWarn = 1
    LoLim = 3700
    LoLimEng = -2.5
    HiLimEng = 2.5
    HiLim = 20640
    Usts = [None, None, None, -1, -0.5, None,
            None, 0.5, 1, None, None, None, None]
    MsgMask = '0111_0110_0111_0001'
    RuleName = 'Аналоги (макс1 = макс.уставка)'

    def prepare(self):
        AIParamMoving.SetpointGroupId = ('ПНА ' if 'ПНА' in self.name else 'МНА ') + self.tag[2:1]
        AIParamMoving.NumberNAorAux = self.tag[2:1]


class AIParamEDAmper(AIParam):
    """Параметры для аналогового сигнала силы тока."""
    AnalogGroupId = 'Сила тока'
    Sign = 'I'
    EGU = 'А'
    IsEDAmperage = 1
    HiLimEng = 600
    Usts = [None, None, None, None, 20, None,
            None, None, None, None, None, None, None]
    MsgMask = '0100_0000_0010_0001'
    Precision = 0
    DeltaT = 10
    RuleName = 'Аналоги (макс1 = макс.уставка)'

    def prepare(self):
        AIParamEDAmper.SetpointGroupId = ('ПНА ' if 'ПНА' in self.name else 'МНА ') + self.tag[2:1]
        AIParamEDAmper.NumberNAorAux = self.tag[2:1]


class AIParamNC(AIParam):
    """Параметры для аналогового сигнала с контролем целостности."""
    AnalogGroupId = 'Сигнализаторы'
    SetpointGroupId = 'Сигналы с контролем цепи'
    Sign = None
    EGU = 'мА'
    LoLimEng = 4
    HiLimEng = 20
    MsgMask = '0000_0000_0000_0000'
    RuleName = 'Сигналы с контролем цепи'


class AIParamGAS(AIParam):
    """Параметры для аналогового сигнала загазованности."""
    AnalogGroupId = 'Загазованность'
    SetpointGroupId = 'Загазованность'
    Sign = 'Газ'
    EGU = '%'
    LoLim = 3700
    HiLim = 20800
    Usts = [None, None, None, None, None, None,
            None, 10, 30, None, None, None]
    MsgMask = '0100_0110_0000_0001'
    RuleName = 'Загазованность'


class AIParamTemp(AIParam):
    """Параметры для аналогового сигнала температуры."""
    AnalogGroupId = 'Температуры'
    Sign = 'T'
    EGU = '°C'
    Histeresis = 0.5
    DeltaT = 0.5
    RuleName = 'Аналоги (макс1 = макс.уставка)'

    def prepare(self):
        if 'CSC' in self.tag:
            typeTemp = 1
        elif re.search(r'шкаф.+приборн', self.name):
            typeTemp = 2
        elif 'НА' in self.name:
            typeTemp = 3
        elif re.search(r'температур.+масл', self.name):
            typeTemp = 4
        else:
            typeTemp = 7
        match typeTemp:
            case 1:
                AIParamTemp.SetpointGroupId = 'Температура воздуха'
                AIParamTemp.LoLimEng = -20
                AIParamTemp.HiLimEng = 80
                AIParamTemp.Usts = [None, None, None, None, 5, None,
                                    None, 35, None, None, None, None]
                AIParamTemp.MsgMask = '0100_0010_0010_0001'
            case 2:
                AIParamTemp.SetpointGroupId = 'Температура воздуха'
                AIParamTemp.LoLimEng = -50
                AIParamTemp.HiLimEng = 100
                AIParamTemp.Usts = [None, None, None, None, None, 5,
                                    None, None, None, None, None, None]
                AIParamTemp.MsgMask = '0100_0000_0100_0001'
            case 3:
                AIParamTemp.AnalogGroupId = 'Температура двигателя'
                AIParamTemp.SetpointGroupId = ('ПНА ' if 'ПНА' in self.name else 'МНА ') + self.tag[2:1]
                AIParamTemp.LoLimEng = -50
                AIParamTemp.HiLimEng = 150

                if 'статор' in self.name:
                    AIParamTemp.Usts = [None, None, None, None, None, None,
                                        50, 110, 120, None, None, None]
                    AIParamTemp.MsgMask = '0100_0111_0000_0001'
                elif 'подшипн' in self.name:
                    AIParamTemp.Usts = [None, None, None, None, None, None,
                                        None, 65, 75, None, None, None]
                    AIParamTemp.MsgMask = '0100_0110_0000_0001'
                else:
                    AIParamTemp.Usts = [None, None, None, None, None, None,
                                        None, 50, 60, None, None, None]
                    AIParamTemp.MsgMask = '0100_0110_0000_0001'

                AIParamTemp.RuleName = 'Аналоги (макс1 = повышенная)'
            case 4:
                AIParamTemp.AnalogGroupId = 'Температура масла'
                AIParamTemp.SetpointGroupId = 'Общестанционные'
                AIParamTemp.LoLimEng = -50
                AIParamTemp.HiLimEng = 100
                AIParamTemp.RuleName = 'Аналоги (макс1 = повышенная)'
            case 7:
                AIParamTemp.SetpointGroupId = 'Общестанционные'
                AIParamTemp.LoLimEng = -50
                AIParamTemp.HiLimEng = 100
                AIParamTemp.MsgMask = '0100_0000_0000_0001'
            case _:
                AIParamTemp.SetpointGroupId = 'Заполни вручную!'


class AIParamPres(AIParam):
    """Параметры для аналогового сигнала давления."""
    AnalogGroupId = 'Давления'
    Sign = 'P'
    RuleName = 'Аналоги (макс1 = макс.уставка)'

    def prepare(self):
        if 'НА' in self.name:
            if 'нефти' in self.name:
                typePress = 1
            elif 'масла' in self.name:
                typePress = 2
        elif re.search(r'авлени.+выход.+насос', self.name):
            typePress = 3
        else:
            if re.search(r'на прием.+точка', self.name):
                typePress = 4
            elif re.search(r'в коллектор.+точка', self.name):
                typePress = 5
            elif re.search(r'на выход.+точка', self.name):
                typePress = 6
            else:
                typePress = 7
        match typePress:
            # Давления нефти МНА
            case 1:
                AIParamPres.SetpointGroupId = ('ПНА ' if 'ПНА' in self.name else 'МНА ') + self.tag[2:1]
                AIParamPres.EGU = 'МПа'
                AIParamPres.IsOilPressure = 1
                if self.tag[2:1] == 1:
                    AIParamPres.HiLimEng = 6
                else:
                    AIParamPres.HiLimEng = 10
                AIParamPres.Precision = 2
                AIParamPres.Histeresis = 0.5
                AIParamPres.DeltaT = 0.003
            # Давления масла МНА
            case 2:
                AIParamPres.SetpointGroupId = ('ПНА ' if 'ПНА' in self.name else 'МНА ') + self.tag[2:1]
                AIParamPres.EGU = 'кПа'
                AIParamPres.HiLimEng = 400
                AIParamPres.Usts = [None, None, None, 25, None, None,
                                    None, None, None, None, None, None]
                AIParamPres.MsgMask = '0100_0000_0001_0001'
                AIParamPres.Precision = 0
                AIParamPres.Histeresis = 0
                AIParamPres.DeltaT = 3
            # Давления вспомсистем
            case 3:
                AIParamPres.SetpointGroupId = 'Вспомсистемы'
                AIParamPres.EGU = 'МПа'
                if 'масл' not in self.name:
                    AIParamPres.IsOilPressure = 1
                AIParamPres.IsAuxPressure = 1
                AIParamPres.Precision = 2
                AIParamPres.MsgMask = '0100_0000_0010_0001'
                AIParamPres.RuleName = 'Аналоги (макс1 = повышенная)'
            # Давления на приеме МНС
            case 4:
                AIParamPres.AnalogGroupId = 'Давления вход МНС'
                AIParamPres.SetpointGroupId = 'Общестанционные'
                AIParamPres.EGU = 'МПа'
                AIParamPres.IsOilPressure = 1
                AIParamPres.HiLimEng = 6
                AIParamPres.Usts = [None, None, None, 0.41, 0.44, None,
                                    None, None, None, None, None, None]
                AIParamPres.MsgMask = '0100_0000_0011_0001'
                AIParamPres.Precision = 3
                AIParamPres.DeltaT = 0.003
            # Давления в коллекторе МНС
            case 5:
                AIParamPres.AnalogGroupId = 'Давления выход МНС'
                AIParamPres.SetpointGroupId = 'Общестанционные'
                AIParamPres.EGU = 'МПа'
                AIParamPres.IsOilPressure = 1
                AIParamPres.HiLimEng = 10
                AIParamPres.Usts = [None, None, None, None, None, None,
                                    4.9, 6.59, 6.85, None, None, None]
                AIParamPres.MsgMask = '0100_0111_0000_0001'
                AIParamPres.Precision = 3
                AIParamPres.DeltaT = 0.003
            # Давления на выходе НПС
            case 6:
                AIParamPres.AnalogGroupId = 'Давления выход НПС'
                AIParamPres.SetpointGroupId = 'Общестанционные'
                AIParamPres.EGU = 'МПа'
                AIParamPres.IsOilPressure = 1
                AIParamPres.HiLimEng = 10
                AIParamPres.Usts = [None, None, None, None, None, None,
                                    None, 4.94, 5.11, None, None, None]
                AIParamPres.MsgMask = '0100_0110_0000_0001'
                AIParamPres.Precision = 3
                AIParamPres.DeltaT = 0.003
            # Остальные давления
            case 7:
                AIParamPres.SetpointGroupId = 'Общестанционные'
                AIParamPres.EGU = 'МПа'
                AIParamPres.IsOilPressure = 1
                AIParamPres.Precision = 2
            case _:
                AIParamPres.SetpointGroupId = 'Заполни вручную!'


class AIParamDeltaPres(AIParam):
    """Параметры для аналогового сигнала перепада давления."""
    AnalogGroupId = 'Перепад давления'
    Sign = 'dP'
    RuleName = 'Аналоги (макс1 = макс.уставка)'

    def prepare(self):
        if re.search(r'авлени.+вентил', self.name):
            typePress = 1
        else:
            typePress = 2
        match typePress:
            # Перепад давления вспомсистем
            case 1:
                AIParamDeltaPres.SetpointGroupId = 'Вспомсистемы'
                AIParamDeltaPres.EGU = 'кПа'
                AIParamDeltaPres.IsAuxPressure = 1
                AIParamDeltaPres.Precision = 2
                AIParamDeltaPres.MsgMask = '0100_0000_0010_0001'
            # Остальные перепады давления
            case 2:
                AIParamDeltaPres.SetpointGroupId = 'Общестанционные'
                if 'маслофильт' in self.name:
                    AIParamDeltaPres.EGU = 'кПа'
                else:
                    AIParamDeltaPres.EGU = 'МПа'
                    AIParamDeltaPres.IsOilPressure = 1
            case _:
                AIParamDeltaPres.SetpointGroupId = 'Заполни вручную!'


class AIParamLevel(AIParam):
    """Параметры для аналогового сигнала уровня."""
    AnalogGroupId = 'Уровни'
    SetpointGroupId = 'Уровни'
    Sign = 'L'
    EGU = 'мм'
    Histeresis = 5
    DeltaT = 1
    RuleName = 'Аналоги (макс1 = макс.уставка)'


class BaseCls():
    typeAnalog = {'температур': AIParamTemp,
                  'вибрац': AIParamVibr,
                  'Уровень': AIParamLevel,
                  'давлен': AIParamPres,
                  'перепад': AIParamDeltaPres,
                  'сила тока': AIParamEDAmper,
                  'загазован': AIParamGAS,
                  'пожар': AIParamNC,
                  'аварийн': AIParamNC,
                  'затопл': AIParamNC,
                  'осев': AIParamMoving
                  }


class Analogs():
    '''Заполнение таблицы AI.'''
    def __init__(self):
        # self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def check_table(self):
        '''Проверяем таблицу signals на наличие и заполненость.'''
        result = self.request.check_table(T_SIGNALS)
        if not result:
            print('''SQL. AI. Таблица signals отсутсвует или не заполнена''')
            # self.logsTextEdit.logs_msg('''SQL. AI. Таблица
            #                            signals отсутсвует
            #                            или не заполнена''', 2)
            return False
        return True

    def check_signal(self, signal) -> bool:
        '''Проверка сигнала на существование в таблице AI.
        По УСО, корзине, модулю и каналу.'''
        uso = signal.uso
        basket = signal.basket
        module = signal.module
        channel = signal.channel
        coinc = self.request.select_orm(AI,
                                        (AI.uso == uso) &
                                        (AI.basket == basket) &
                                        (AI.module == module) &
                                        (AI.channel == channel),
                                        AI.basket)
        return bool(coinc)

    def ai(self):
        '''Заполнение таблицы.'''
        try:
            # Проверяем таблицу signals
            if not self.check_table():
                raise

            data = self.request.select_orm(Signals,
                                           (Signals.type_signal.contains('AI')) |
                                           (Signals.schema.contains('AI')),
                                           Signals.description)
            for signal in data:
                exist = self.check_signal(signal)

                if exist:
                    print(signal.description)
                else:
                    print('не существует')

            print('SQL. AI. Таблица заполнена')
            # self.logsTextEdit.logs_msg('''SQL. AI.
            #                            Таблица заполнена''', 1)
        except Exception:
            print({traceback.format_exc()})
            # self.logsTextEdit.logs_msg(f'''SQL. AI. Ошибка
            #                            {traceback.format_exc()}''', 2)


a = Analogs()
a.ai()
