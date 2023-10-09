import models as m
import psycopg2 as postgres
from psycopg2 import Error
from peewee import PostgresqlDatabase

MNS_LIST = [m.AI, m.AIFuse, m.AIgrp, m.AO, m.Buf, m.BufR, m.DI, m.DO, m.DPS,
            m.GMPNA, m.HardWare, m.HMINA, m.HMIREAL, m.HMIUDINT, m.HMIVS,
            m.HMIWORD, m.HMIZD, m.KTPR, m.KTPRA, m.KTPRS, m.Msg, m.MsgCat,
            m.MsgOthers, m.Net, m.NPS, m.PIC, m.PrjTM, m.RS, m.RSData, m.RSReq,
            m.Signals, m.SPGrp, m.SPRules, m.SS, m.SSData, m.TM_DP, m.TM_TI2,
            m.TM_TI4, m.TM_TII, m.TM_TR2, m.TM_TR4, m.TM_TS, m.TM_TU,
            m.TrendsGrp, m.UMPNA, m.tmNA_UMPNA_narab, m.tmNA_UMPNA, m.USO,
            m.UTS, m.UTS_tm, m.VS, m.VS_tm, m.VSGRP, m.VSGRP_tm, m.VV,
            m.ZD, m.ZD_tm, m.ZDType]

PT_LIST = [m.AI, m.AIFuse, m.AIgrp, m.BD, m.BDGRP, m.Buf, m.BufR, m.DI, m.DO,
           m.HardWare, m.HMIREAL, m.HMIUDINT, m.HMIVS, m.HMIWORD, m.HMIZD,
           m.KTPRP, m.KTPRS, m.Msg, m.MsgCat, m.MsgOthers, m.Net, m.PI, m.PIC,
           m.PrjTM, m.PT, m.PZ, m.PZ_tm, m.RS, m.RSData, m.RSReq, m.Signals,
           m.SPGrp, m.SPRules, m.SS, m.SSData, m.TrendsGrp, m.USO, m.UPTS,
           m.UTS_tm, m.VS, m.VS_tm, m.VSGRP, m.VSGRP_tm, m.ZD, m.ZD_tm,
           m.ZDType]


class NewDB():
    '''Создание новой БД SQL с таблицами под определённую систему.'''
    def __init__(self):
        self.link = postgres.connect(dbname="postgres",
                                     user=m.connect.user,
                                     password=m.connect.password,
                                     host=m.connect.host)

    def create_new_base(self, type_system: str):
        """Создание подключения с PostgresSQL.
        Создание новой БД. Название БД из файла init_conf.cfg

        Args:
            type_system (str): Тип системы(МНС, ПТ, САР, РП)
        """
        cursor = self.link.cursor()
        self.link.autocommit = True

        sql = f'CREATE DATABASE {m.connect.database}'
        try:
            cursor.execute(sql)
        except (Exception, Error) as error:
            print(error)

        cursor.close()
        self.link.close()

        self.create_new_tabl(type_system)

    def create_new_tabl(self, type_system: str):
        '''Создание таблиц в новой БД.'''
        db = PostgresqlDatabase(m.connect.database,
                                user=m.connect.user,
                                password=m.connect.password,
                                host=m.connect.host,
                                port=m.connect.port)
        with db:
            type_list = MNS_LIST if type_system == 'MNS' else PT_LIST
            db.create_tables(type_list)