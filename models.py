from connect_settings import Connect
from peewee import PostgresqlDatabase
from peewee import Model
from peewee import CharField
from peewee import BooleanField
from peewee import IntegerField
from peewee import DoubleField
from playhouse.migrate import PostgresqlMigrator

connect = Connect()
db = PostgresqlDatabase(connect.database,
                        user=connect.user,
                        password=connect.password,
                        host=connect.host,
                        port=connect.port)

db_prj = PostgresqlDatabase(connect.database_msg,
                            user=connect.user_msg,
                            password=connect.password_msg,
                            host=connect.host_msg,
                            port=connect.port_msg)

migrator = PostgresqlMigrator(db)


class BaseModel(Model):
    class Meta:
        database = db
        order_by = id


class Signals(BaseModel):
    type_signal = CharField(null=True)
    uso = CharField(null=True)
    tag = CharField(null=True)
    description = CharField(null=True)
    schema = CharField(null=True)
    klk = CharField(null=True)
    contact = CharField(null=True)
    basket = IntegerField(null=True)
    module = IntegerField(null=True)
    channel = IntegerField(null=True)

    class Meta:
        table_name = 'signals'


class HardWare(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    uso = CharField(null=True)
    basket = IntegerField(null=True)
    powerLink_ID = CharField(null=True)
    Pic = CharField(null=True)
    type_0 = CharField(null=True)
    variable_0 = CharField(null=True)
    type_1 = CharField(null=True)
    variable_1 = CharField(null=True)
    type_2 = CharField(null=True)
    variable_2 = CharField(null=True)
    type_3 = CharField(null=True)
    variable_3 = CharField(null=True)
    type_4 = CharField(null=True)
    variable_4 = CharField(null=True)
    type_5 = CharField(null=True)
    variable_5 = CharField(null=True)
    type_6 = CharField(null=True)
    variable_6 = CharField(null=True)
    type_7 = CharField(null=True)
    variable_7 = CharField(null=True)
    type_8 = CharField(null=True)
    variable_8 = CharField(null=True)
    type_9 = CharField(null=True)
    variable_9 = CharField(null=True)
    type_10 = CharField(null=True)
    variable_10 = CharField(null=True)
    type_11 = CharField(null=True)
    variable_11 = CharField(null=True)
    type_12 = CharField(null=True)
    variable_12 = CharField(null=True)
    type_13 = CharField(null=True)
    variable_13 = CharField(null=True)
    type_14 = CharField(null=True)
    variable_14 = CharField(null=True)
    type_15 = CharField(null=True)
    variable_15 = CharField(null=True)
    type_16 = CharField(null=True)
    variable_16 = CharField(null=True)
    type_17 = CharField(null=True)
    variable_17 = CharField(null=True)
    type_18 = CharField(null=True)
    variable_18 = CharField(null=True)
    type_19 = CharField(null=True)
    variable_19 = CharField(null=True)
    type_20 = CharField(null=True)
    variable_20 = CharField(null=True)
    type_21 = CharField(null=True)
    variable_21 = CharField(null=True)
    type_22 = CharField(null=True)
    variable_22 = CharField(null=True)
    type_23 = CharField(null=True)
    variable_23 = CharField(null=True)
    type_24 = CharField(null=True)
    variable_24 = CharField(null=True)
    type_25 = CharField(null=True)
    variable_25 = CharField(null=True)
    type_26 = CharField(null=True)
    variable_26 = CharField(null=True)
    type_27 = CharField(null=True)
    variable_27 = CharField(null=True)
    type_28 = CharField(null=True)
    variable_28 = CharField(null=True)
    type_29 = CharField(null=True)
    variable_29 = CharField(null=True)
    type_30 = CharField(null=True)
    variable_30 = CharField(null=True)
    type_31 = CharField(null=True)
    variable_31 = CharField(null=True)
    type_32 = CharField(null=True)
    variable_32 = CharField(null=True)

    class Meta:
        table_name = 'hardware'


class AI(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    pValue = CharField(null=True)
    pHealth = CharField(null=True)
    AnalogGroupId = CharField(null=True)
    SetpointGroupId = CharField(null=True)
    Egu = CharField(null=True)
    sign_VU = CharField(null=True)
    IsOilPressure = BooleanField(null=True)
    number_NA_or_aux = IntegerField(null=True)
    IsPumpVibration = IntegerField(null=True)
    vibration_motor = IntegerField(null=True)
    current_motor = IntegerField(null=True)
    aux_outlet_pressure = IntegerField(null=True)
    number_ust_min_avar = IntegerField(null=True)
    number_ust_min_pred = IntegerField(null=True)
    number_ust_max_pred = IntegerField(null=True)
    number_ust_max_avar = IntegerField(null=True)
    LoLimField = DoubleField(null=True)
    HiLimField = DoubleField(null=True)
    LoLimEng = DoubleField(null=True)
    HiLimEng = DoubleField(null=True)
    LoLim = DoubleField(null=True)
    HiLim = DoubleField(null=True)
    Histeresis = DoubleField(null=True)
    TimeFilter = DoubleField(null=True)
    Min6 = DoubleField(null=True)
    Min5 = DoubleField(null=True)
    Min4 = DoubleField(null=True)
    Min3 = DoubleField(null=True)
    Min2 = DoubleField(null=True)
    Min1 = DoubleField(null=True)
    Max1 = DoubleField(null=True)
    Max2 = DoubleField(null=True)
    Max3 = DoubleField(null=True)
    Max4 = DoubleField(null=True)
    Max5 = DoubleField(null=True)
    Max6 = DoubleField(null=True)
    SigMask = CharField(null=True)
    MsgMask = CharField(null=True)
    CtrlMask = CharField(null=True)
    Precision = IntegerField(null=True)
    Pic = CharField(null=True)
    TrendingGroup = IntegerField(null=True)
    DeltaT = DoubleField(null=True)
    PhysicEgu = CharField(null=True)
    RuleName = CharField(null=True)
    fuse = CharField(null=True)
    uso = CharField(null=True)
    basket = IntegerField(null=True)
    module = IntegerField(null=True)
    channel = IntegerField(null=True)
    tag_eng = CharField(null=True)
    AlphaHMI = CharField(null=True)
    AlphaHMI_PIC1 = CharField(null=True)
    AlphaHMI_PIC1_Number_kont = CharField(null=True)
    AlphaHMI_PIC2 = CharField(null=True)
    AlphaHMI_PIC2_Number_kont = CharField(null=True)
    AlphaHMI_PIC3 = CharField(null=True)
    AlphaHMI_PIC3_Number_kont = CharField(null=True)
    AlphaHMI_PIC4 = CharField(null=True)
    AlphaHMI_PIC4_Number_kont = CharField(null=True)

    class Meta:
        table_name = 'ai'


class AO(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    pValue = CharField(null=True)
    pHealth = CharField(null=True)
    uso = CharField(null=True)
    basket = IntegerField(null=True)
    module = IntegerField(null=True)
    channel = IntegerField(null=True)
    tag_eng = CharField(null=True)

    class Meta:
        table_name = 'ao'


class DI(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    pValue = CharField(null=True)
    pHealth = CharField(null=True)
    Inv = IntegerField(null=True)
    ErrValue = IntegerField(null=True)
    priority_0 = IntegerField(null=True)
    priority_1 = IntegerField(null=True)
    Msg = IntegerField(null=True)
    isDI_NC = CharField(null=True)
    isAI_Warn = CharField(null=True)
    isAI_Avar = CharField(null=True)
    pNC_AI = CharField(null=True)
    TS_ID = CharField(null=True)
    isModuleNC = CharField(null=True)
    Pic = CharField(null=True)
    tabl_msg = CharField(null=True)
    group_diskrets = CharField(null=True)
    msg_priority_0 = IntegerField(null=True)
    sound_msg_0 = CharField(null=True)
    msg_priority_1 = IntegerField(null=True)
    sound_msg_1 = CharField(null=True)
    short_title = CharField(null=True)
    uso = CharField(null=True)
    basket = IntegerField(null=True)
    module = IntegerField(null=True)
    channel = IntegerField(null=True)
    tag_eng = CharField(null=True)
    AlphaHMI = CharField(null=True)
    AlphaHMI_PIC1 = CharField(null=True)
    AlphaHMI_PIC1_Number_kont = CharField(null=True)
    AlphaHMI_PIC2 = CharField(null=True)
    AlphaHMI_PIC2_Number_kont = CharField(null=True)
    AlphaHMI_PIC3 = CharField(null=True)
    AlphaHMI_PIC3_Number_kont = CharField(null=True)
    AlphaHMI_PIC4 = CharField(null=True)
    AlphaHMI_PIC4_Number_kont = CharField(null=True)

    class Meta:
        table_name = 'di'


class DO(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    pValue = CharField(null=True)
    pHealth = CharField(null=True)
    short_title = CharField(null=True)
    tabl_msg = CharField(null=True)
    uso = CharField(null=True)
    basket = IntegerField(null=True)
    module = IntegerField(null=True)
    channel = IntegerField(null=True)
    tag_eng = CharField(null=True)
    AlphaHMI = CharField(null=True)
    AlphaHMI_PIC1 = CharField(null=True)
    AlphaHMI_PIC1_Number_kont = CharField(null=True)
    AlphaHMI_PIC2 = CharField(null=True)
    AlphaHMI_PIC2_Number_kont = CharField(null=True)
    AlphaHMI_PIC3 = CharField(null=True)
    AlphaHMI_PIC3_Number_kont = CharField(null=True)
    AlphaHMI_PIC4 = CharField(null=True)
    AlphaHMI_PIC4_Number_kont = CharField(null=True)

    class Meta:
        table_name = 'do'


class RS(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    array_number_modul = IntegerField(null=True)
    pValue = CharField(null=True)
    pHealth = CharField(null=True)
    Pic = CharField(null=True)
    uso = CharField(null=True)
    basket = IntegerField(null=True)
    module = IntegerField(null=True)
    channel = IntegerField(null=True)

    class Meta:
        table_name = 'rs'


class USO(BaseModel):
    variable = CharField(null=True)
    name = CharField(null=True)
    temperature = CharField(null=True)
    door = CharField(null=True)
    signal_1 = CharField(null=True)
    signal_2 = CharField(null=True)
    signal_3 = CharField(null=True)
    signal_4 = CharField(null=True)
    signal_5 = CharField(null=True)
    signal_6 = CharField(null=True)
    signal_7 = CharField(null=True)
    signal_8 = CharField(null=True)
    signal_9 = CharField(null=True)
    signal_10 = CharField(null=True)
    signal_11 = CharField(null=True)
    signal_12 = CharField(null=True)
    signal_13 = CharField(null=True)
    signal_14 = CharField(null=True)
    signal_15 = CharField(null=True)
    signal_16 = CharField(null=True)
    signal_17 = CharField(null=True)
    signal_18 = CharField(null=True)
    signal_19 = CharField(null=True)
    signal_20 = CharField(null=True)
    signal_21 = CharField(null=True)
    signal_22 = CharField(null=True)
    signal_23 = CharField(null=True)
    signal_24 = CharField(null=True)
    signal_25 = CharField(null=True)
    signal_26 = CharField(null=True)
    signal_27 = CharField(null=True)
    signal_28 = CharField(null=True)
    signal_29 = CharField(null=True)
    signal_30 = CharField(null=True)
    signal_31 = CharField(null=True)
    signal_32 = CharField(null=True)

    class Meta:
        table_name = 'uso'


class KTPRP(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    Number_PZ = CharField(null=True)
    Type = CharField(null=True)
    Pic = CharField(null=True)
    number_list_VU = IntegerField(null=True)
    number_protect_VU = IntegerField(null=True)

    class Meta:
        table_name = 'ktprp'


class KTPR(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    avar_parameter = CharField(null=True)
    DisableMasking = IntegerField(null=True)
    auto_unlock_protection = IntegerField(null=True)
    shutdown_PNS_a_time_delay_up_5s_after_turning = IntegerField(null=True)
    bitmask_protection_group_membership = IntegerField(null=True)
    stop_type_NA = IntegerField(null=True)
    pump_station_stop_type = IntegerField(null=True)
    closing_gate_valves_at_the_inlet_NPS = IntegerField(null=True)
    closing_gate_valves_at_the_outlet_NPS = IntegerField(null=True)
    closing_gate_valves_between_PNS_and_MNS = IntegerField(null=True)
    closing_gate_valves_between_RP_and_PNS = IntegerField(null=True)
    closing_valves_inlet_and_outlet_MNS = IntegerField(null=True)
    closing_valves_inlet_and_outlet_PNS = IntegerField(null=True)
    closing_valves_inlet_and_outlet_MNA = IntegerField(null=True)
    closing_valves_inlet_and_outlet_PNA = IntegerField(null=True)
    closing_valves_inlet_RD = IntegerField(null=True)
    closing_valves_outlet_RD = IntegerField(null=True)
    closing_valves_inlet_SSVD = IntegerField(null=True)
    closing_valves_inlet_FGU = IntegerField(null=True)
    closing_secant_valve_connection_unit__oil_production_oil = IntegerField(null=True)
    closing_valves_inlet_RP = IntegerField(null=True)
    reserve_protect_14 = IntegerField(null=True)
    reserve_protect_15 = IntegerField(null=True)
    shutdown_oil_pumps = IntegerField(null=True)
    shutdown_oil_pumps_after_signal_stopped_NA = IntegerField(null=True)
    shutdown_circulating_water_pumps = IntegerField(null=True)
    shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_MNS = IntegerField(null=True)
    shutdown_pumps_pumping_out_from_tanks_collection_of_leaks_PNS = IntegerField(null=True)
    shutdown_pumps_pumping_out_from_tanks_SSVD = IntegerField(null=True)
    switching_off_the_electric_room_fans = IntegerField(null=True)
    shutdown_of_booster_fans_ED = IntegerField(null=True)
    shutdown_of_retaining_fans_of_the_electrical_room = IntegerField(null=True)
    shutdown_of_ED_air_compressors = IntegerField(null=True)
    shutdown_pumps_providing_oil = IntegerField(null=True)
    disabling_pumps_for_pumping_oil_oil_products_through_BIC = IntegerField(null=True)
    shutdown_domestic_and_drinking_water_pumps = IntegerField(null=True)
    shutdown_of_art_well_pumps = IntegerField(null=True)
    AVO_shutdown = IntegerField(null=True)
    shutdown_of_water_cooling_fans_circulating_water_supply_system = IntegerField(null=True)
    shutdown_exhaust_fans_of_the_pumping_room_of_the_MNS = IntegerField(null=True)
    shutdown_of_exhaust_fans_of_the_pumping_room_PNS = IntegerField(null=True)
    shutdown_of_exhaust_fans_in_the_centralized_oil_system_room = IntegerField(null=True)
    shutdown_of_exhaust_fans_oil_pit_in_the_electrical_room = IntegerField(null=True)
    shutdown_of_exhaust_fans_in_the_RD_room = IntegerField(null=True)
    shutdown_of_exhaust_fans_in_the_SSVD_room = IntegerField(null=True)
    shutdown_of_the_roof_fans_of_the_MNS_pump_room = IntegerField(null=True)
    shutdown_of_the_roof_fans_of_the_PNS_pump_room = IntegerField(null=True)
    switching_off_the_supply_fans_pumping_room_of_the_MNS = IntegerField(null=True)
    switching_off_the_supply_fans_pumping_room_of_the_PNS = IntegerField(null=True)
    switch_off_the_supply_fans_in_the_centralized_oil = IntegerField(null=True)
    switching_off_the_supply_fan_of_the_RD_room = IntegerField(null=True)
    switching_off_the_supply_fan_of_the_SSVD_room = IntegerField(null=True)
    switching_off_the_supply_fans_of_the_ED_air_compressor = IntegerField(null=True)
    switching_off_the_supply_fan_of_the_BIK_room = IntegerField(null=True)
    switching_off_the_supply_fan_of_the_SIKN_room = IntegerField(null=True)
    closing_the_air_valves_louvered_grilles_of_the_pump_room = IntegerField(null=True)
    closing_of_air_valves_louvered_grilles_of_the_compressor_room = IntegerField(null=True)
    shutdown_of_electric_oil_heaters = IntegerField(null=True)
    shutdown_of_the_electric_heaters_of_the_leakage_collection_MNS = IntegerField(null=True)
    shutdown_of_the_electric_heaters_of_the_leakage_collection_PNS = IntegerField(null=True)
    shutdown_of_electric_heaters_of_the_SIKN_leak_collection_tank = IntegerField(null=True)
    shutdown_of_air_coolers_of_the_locking_system_MNA = IntegerField(null=True)
    shutdown_of_air_coolers_of_the_locking_system_disc_NA = IntegerField(null=True)
    shutdown_of_the_external_cooling_circuit_ChRP_MNA = IntegerField(null=True)
    shutdown_of_the_external_cooling_circuit_ChRP_PNA = IntegerField(null=True)
    shutdown_of_locking_system_pumps = IntegerField(null=True)
    shutdown_of_pumps_for_pumping_oil_oil_products_through = IntegerField(null=True)
    shutdown_of_pumping_pumps_from_leakage_collection_tanks = IntegerField(null=True)
    shutdown_of_anticondensation_electric_heaters_ED = IntegerField(null=True)
    fire_protection = IntegerField(null=True)
    reserve_aux_15 = IntegerField(null=True)
    value_ust = IntegerField(null=True)
    Pic = CharField(null=True)
    group_ust = CharField(null=True)
    rule_map_ust = CharField(null=True)
    number_list_VU = IntegerField(null=True)
    number_protect_VU = IntegerField(null=True)

    class Meta:
        table_name = 'ktpr'


class KTPRA(BaseModel):
    id_num = IntegerField(null=True)
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    NA = CharField(null=True)
    avar_parameter = CharField(null=True)
    stop_type = IntegerField(null=True)
    AVR = IntegerField(null=True)
    close_valves = IntegerField(null=True)
    DisableMasking = IntegerField(null=True)
    value_ust = IntegerField(null=True)
    Pic = CharField(null=True)
    group_ust = CharField(null=True)
    rule_map_ust = CharField(null=True)
    number_list_VU = IntegerField(null=True)
    number_protect_VU = IntegerField(null=True)
    number_pump_VU = IntegerField(null=True)

    class Meta:
        table_name = 'ktpra'


class KTPRS(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    drawdown = CharField(null=True)
    reference_to_value = CharField(null=True)
    msg_priority_0 = IntegerField(null=True)
    msg_priority_1 = IntegerField(null=True)
    sound_msg_0 = CharField(null=True)
    sound_msg_1 = CharField(null=True)
    prohibition_issuing_msg = BooleanField(null=True)
    Pic = CharField(null=True)

    class Meta:
        table_name = 'ktprs'


class GMPNA(BaseModel):
    id_num = IntegerField(null=True)
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    name_for_Chrp_in_local_mode = CharField(null=True)
    NA = CharField(null=True)
    used_time_ust = BooleanField(null=True)
    value_ust = IntegerField(null=True)
    group_ust = CharField(null=True)
    rule_map_ust = CharField(null=True)
    number_list_VU = IntegerField(null=True)
    number_protect_VU = IntegerField(null=True)
    number_pump_VU = IntegerField(null=True)

    class Meta:
        table_name = 'gmpna'


class tmNA_UMPNA(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    unit = CharField(null=True)
    used = BooleanField(null=True)
    value_ust = IntegerField(null=True)
    value_real_ust = DoubleField(null=True)
    minimum = IntegerField(null=True)
    maximum = IntegerField(null=True)
    group_ust = CharField(null=True)
    rule_map_ust = CharField(null=True)

    class Meta:
        table_name = 'umpna_tm'


class tmNA_UMPNA_narab(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    unit = CharField(null=True)
    used = BooleanField(null=True)
    value_ust = IntegerField(null=True)
    minimum = IntegerField(null=True)
    maximum = IntegerField(null=True)
    group_ust = CharField(null=True)
    rule_map_ust = CharField(null=True)

    class Meta:
        table_name = 'umpna_narab_tm'


class UMPNA(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    vv_included = CharField(null=True)
    vv_double_included = CharField(null=True)
    vv_disabled = CharField(null=True)
    vv_double_disabled = CharField(null=True)
    current_greater_than_noload_setting = CharField(null=True)
    serviceability_of_circuits_of_inclusion_of_VV = CharField(null=True)
    serviceability_of_circuits_of_shutdown_of_VV = CharField(null=True)
    serviceability_of_circuits_of_shutdown_of_VV_double = CharField(null=True)
    stop_1 = CharField(null=True)
    stop_2 = CharField(null=True)
    stop_3 = CharField(null=True)
    stop_4 = CharField(null=True)
    monitoring_the_presence_of_voltage_in_the_control_current = CharField(null=True)
    voltage_presence_flag_in_the_ZRU_motor_cell = CharField(null=True)
    vv_trolley_rolled_out = CharField(null=True)
    remote_control_mode_of_the_RZiA_controller = CharField(null=True)
    availability_of_communication_with_the_RZiA_controller = CharField(null=True)
    the_state_of_the_causative_agent_of_ED = CharField(null=True)
    engine_prepurge_end_flag = CharField(null=True)
    flag_for_the_presence_of_safe_air_boost_pressure_in_the_en = CharField(null=True)
    flag_for_the_presence_of_safe_air_boost_pressure_in_the_ex = CharField(null=True)
    engine_purge_valve_closed_flag = CharField(null=True)
    oil_system_oil_temperature_flag_is_above_10_at_the_cooler_ou = CharField(null=True)
    flag_for_the_minimum_oil_level_in_the_oil_tank_for_an_indiv = CharField(null=True)
    flag_for_the_presence_of_the_minimum_level_of_the_barrier = CharField(null=True)
    generalized_flag_for_the_presence_of_barrier_fluid_pressure = CharField(null=True)
    command_to_turn_on_the_vv_only_for_UMPNA = CharField(null=True)
    command_to_turn_off_the_vv_output_1 = CharField(null=True)
    command_to_turn_off_the_vv_output_2 = CharField(null=True)
    NA_Chrp = CharField(null=True)
    type_NA_MNA = CharField(null=True)
    pump_type_NM = CharField(null=True)
    parametr_KTPRAS_1 = CharField(null=True)
    number_of_delay_scans_of_the_analysis_of_the_health_of_the = CharField(null=True)
    unit_number_of_the_auxiliary_system_start_up_oil_pump = CharField(null=True)
    NPS_number_1_or_2_which_the_AT_belongs = CharField(null=True)
    achr_protection_number_in_the_array_of_station_protections = CharField(null=True)
    saon_protection_number_in_the_array_of_station_protections = CharField(null=True)
    gmpna_49 = CharField(null=True)
    gmpna_50 = CharField(null=True)
    gmpna_51 = CharField(null=True)
    gmpna_52 = CharField(null=True)
    gmpna_53 = CharField(null=True)
    gmpna_54 = CharField(null=True)
    gmpna_55 = CharField(null=True)
    gmpna_56 = CharField(null=True)
    gmpna_57 = CharField(null=True)
    gmpna_58 = CharField(null=True)
    gmpna_59 = CharField(null=True)
    gmpna_60 = CharField(null=True)
    gmpna_61 = CharField(null=True)
    gmpna_62 = CharField(null=True)
    gmpna_63 = CharField(null=True)
    gmpna_64 = CharField(null=True)
    Pic = CharField(null=True)
    tabl_msg = CharField(null=True)
    replacement_uso_signal_vv_1 = CharField(null=True)
    replacement_uso_signal_vv_2 = CharField(null=True)

    class Meta:
        table_name = 'umpna'


class ZD(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    short_name = CharField(null=True)
    exists_interface = BooleanField(null=True)
    KVO = CharField(null=True)
    KVZ = CharField(null=True)
    MPO = CharField(null=True)
    MPZ = CharField(null=True)
    Dist = CharField(null=True)
    Mufta = CharField(null=True)
    Drive_failure = CharField(null=True)
    Open = CharField(null=True)
    Close = CharField(null=True)
    Stop = CharField(null=True)
    Opening_stop = CharField(null=True)
    Closeing_stop = CharField(null=True)
    KVO_i = CharField(null=True)
    KVZ_i = CharField(null=True)
    MPO_i = CharField(null=True)
    MPZ_i = CharField(null=True)
    Dist_i = CharField(null=True)
    Mufta_i = CharField(null=True)
    Drive_failure_i = CharField(null=True)
    Open_i = CharField(null=True)
    Close_i = CharField(null=True)
    Stop_i = CharField(null=True)
    Opening_stop_i = CharField(null=True)
    Closeing_stop_i = CharField(null=True)
    No_connection = CharField(null=True)
    Close_BRU = CharField(null=True)
    Stop_BRU = CharField(null=True)
    Voltage = CharField(null=True)
    Voltage_CHSU = CharField(null=True)
    Voltage_in_signaling_circuits = CharField(null=True)
    Serviceability_opening_circuits = CharField(null=True)
    Serviceability_closening_circuits = CharField(null=True)
    VMMO = CharField(null=True)
    VMMZ = CharField(null=True)
    Freeze_on_suspicious_change = CharField(null=True)
    Is_klapan = IntegerField(null=True)
    Opening_percent = CharField(null=True)
    Pic = CharField(null=True)
    Type_BUR_ZD = CharField(null=True)
    tabl_msg = CharField(null=True)
    AlphaHMI = CharField(null=True)
    AlphaHMI_PIC1 = CharField(null=True)
    AlphaHMI_PIC1_Number_kont = CharField(null=True)
    AlphaHMI_PIC2 = CharField(null=True)
    AlphaHMI_PIC2_Number_kont = CharField(null=True)
    AlphaHMI_PIC3 = CharField(null=True)
    AlphaHMI_PIC3_Number_kont = CharField(null=True)
    AlphaHMI_PIC4 = CharField(null=True)
    AlphaHMI_PIC4_Number_kont = CharField(null=True)

    class Meta:
        table_name = 'zd'


class ZD_tm(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    unit = CharField(null=True)
    used = BooleanField(null=True)
    value_ust = IntegerField(null=True)
    minimum = IntegerField(null=True)
    maximum = IntegerField(null=True)
    group_ust = CharField(null=True)
    rule_map_ust = CharField(null=True)

    class Meta:
        table_name = 'zd_tm'


class VS(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    short_name = CharField(null=True)
    group = IntegerField(null=True)
    number_in_group = IntegerField(null=True)
    MP = CharField(null=True)
    Pressure_is_True = CharField(null=True)
    Voltage = CharField(null=True)
    Voltage_Sch = CharField(null=True)
    Serviceability_of_circuits_of_inclusion = CharField(null=True)
    External_alarm = CharField(null=True)
    Pressure_sensor_defective = CharField(null=True)
    VKL = CharField(null=True)
    OTKL = CharField(null=True)
    Not_APV = IntegerField(null=True)
    Pic = CharField(null=True)
    tabl_msg = CharField(null=True)
    Is_klapana_interface_auxsystem = CharField(null=True)
    AlphaHMI = CharField(null=True)
    AlphaHMI_PIC1 = CharField(null=True)
    AlphaHMI_PIC1_Number_kont = CharField(null=True)
    AlphaHMI_PIC2 = CharField(null=True)
    AlphaHMI_PIC2_Number_kont = CharField(null=True)
    AlphaHMI_PIC3 = CharField(null=True)
    AlphaHMI_PIC3_Number_kont = CharField(null=True)
    AlphaHMI_PIC4 = CharField(null=True)
    AlphaHMI_PIC4_Number_kont = CharField(null=True)

    class Meta:
        table_name = 'vs'


class VS_tm(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    unit = CharField(null=True)
    used = BooleanField(null=True)
    value_ust = IntegerField(null=True)
    minimum = IntegerField(null=True)
    maximum = IntegerField(null=True)
    group_ust = CharField(null=True)
    rule_map_ust = CharField(null=True)

    class Meta:
        table_name = 'vs_tm'


class VSGRP(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    fire_or_watering = BooleanField(null=True)
    count_auxsys_in_group = IntegerField(null=True)
    WarnOff_flag_if_one_auxsystem_in_the_group_is_running = BooleanField(null=True)
    additional_steps_required = BooleanField(null=True)

    class Meta:
        table_name = 'vsgrp'


class VSGRP_tm(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    unit = CharField(null=True)
    used = BooleanField(null=True)
    value_ust = IntegerField(null=True)
    minimum = IntegerField(null=True)
    maximum = IntegerField(null=True)
    group_ust = CharField(null=True)
    rule_map_ust = CharField(null=True)

    class Meta:
        table_name = 'vsgrp_tm'


class UTS(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    short_name = CharField(null=True)
    location = CharField(null=True)
    VKL = CharField(null=True)
    Serviceability_of_circuits_of_inclusion = CharField(null=True)
    siren = IntegerField(null=True)
    Does_not_require_autoshutdown = CharField(null=True)
    Examination = CharField(null=True)
    Kvit = CharField(null=True)
    Pic = CharField(null=True)
    number_list_VU = IntegerField(null=True)
    order_number_for_VU = IntegerField(null=True)
    uso = CharField(null=True)
    basket = IntegerField(null=True)
    module = IntegerField(null=True)
    channel = IntegerField(null=True)

    class Meta:
        table_name = 'uts'


class UPTS(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    short_name = CharField(null=True)
    location = CharField(null=True)
    VKL = CharField(null=True)
    Serviceability_of_circuits_of_inclusion = CharField(null=True)
    siren = BooleanField(null=True)
    Does_not_require_autoshutdown = CharField(null=True)
    Examination = CharField(null=True)
    Kvit = CharField(null=True)
    Pic = CharField(null=True)
    number_list_VU = IntegerField(null=True)
    order_number_for_VU = IntegerField(null=True)
    uso = CharField(null=True)
    basket = IntegerField(null=True)
    module = IntegerField(null=True)
    channel = IntegerField(null=True)

    class Meta:
        table_name = 'upts'


class UTS_tm(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    unit = CharField(null=True)
    used = BooleanField(null=True)
    value_ust = IntegerField(null=True)
    minimum = IntegerField(null=True)
    maximum = IntegerField(null=True)
    group_ust = CharField(null=True)
    rule_map_ust = CharField(null=True)

    class Meta:
        table_name = 'uts_tm'


class VV(BaseModel):
    variable = CharField(null=True)
    name = CharField(null=True)
    VV_vkl = CharField(null=True)
    VV_otkl = CharField(null=True)
    Pic = CharField(null=True)

    class Meta:
        table_name = 'vv'


class PI(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    Type_PI = CharField(null=True)
    Fire_0 = CharField(null=True)
    Attention_1 = CharField(null=True)
    Fault_1_glass_pollution_broken_2 = CharField(null=True)
    Fault_2_fault_KZ_3 = CharField(null=True)
    Yes_connection_4 = CharField(null=True)
    Frequency_generator_failure_5 = CharField(null=True)
    Parameter_loading_error_6 = CharField(null=True)
    Communication_error_module_IPP_7 = CharField(null=True)
    Supply_voltage_fault_8 = CharField(null=True)
    Optics_contamination_9 = CharField(null=True)
    IK_channel_failure_10 = CharField(null=True)
    UF_channel_failure_11 = CharField(null=True)
    Loading_12 = CharField(null=True)
    Test_13 = CharField(null=True)
    Reserve_14 = CharField(null=True)
    Reset_Link = CharField(null=True)
    Reset_Request = CharField(null=True)
    Through_loop_number_for_interface = CharField(null=True)
    location = CharField(null=True)
    Pic = CharField(null=True)
    Normal = CharField(null=True)

    class Meta:
        table_name = 'pi'


class PT(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    nZDFoam_1 = IntegerField(null=True)
    nZDFoam_2 = IntegerField(null=True)
    nZDFoam_3 = IntegerField(null=True)
    nZDFoam_4 = IntegerField(null=True)
    nZDFoam_5 = IntegerField(null=True)
    nZDFoam_6 = IntegerField(null=True)
    nZDFoam_7 = IntegerField(null=True)
    nZDFoam_8 = IntegerField(null=True)
    nZDWater_1 = IntegerField(null=True)
    nZDWater_2 = IntegerField(null=True)
    nZDWater_3 = IntegerField(null=True)
    nZDWater_4 = IntegerField(null=True)
    nZDWater_5 = IntegerField(null=True)
    nZDWater_6 = IntegerField(null=True)
    nZDWater_7 = IntegerField(null=True)
    nZDWater_8 = IntegerField(null=True)
    pLmin_1 = CharField(null=True)
    pLmin_2 = CharField(null=True)
    pLmin_3 = CharField(null=True)
    pLmin_4 = CharField(null=True)
    pLmin_5 = CharField(null=True)
    pLmin_6 = CharField(null=True)
    pLmin_7 = CharField(null=True)
    pLmin_8 = CharField(null=True)
    number_UPTS_call_oper = IntegerField(null=True)
    max_number_launch_fire_algoritm = IntegerField(null=True)
    max_number_launch_watercooling_algoritm = IntegerField(null=True)

    class Meta:
        table_name = 'pt'


class PZ_tm(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    unit = CharField(null=True)
    used = BooleanField(null=True)
    value_ust = IntegerField(null=True)
    minimum = IntegerField(null=True)
    maximum = IntegerField(null=True)
    group_ust = CharField(null=True)
    rule_map_ust = CharField(null=True)

    class Meta:
        table_name = 'pz_tm'


class DPS(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    control = CharField(null=True)
    deblock = CharField(null=True)
    actuation = CharField(null=True)
    actuation_transmitter = CharField(null=True)
    malfunction = CharField(null=True)
    voltage = CharField(null=True)

    class Meta:
        table_name = 'dps'


class TM_DP(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    link_to_link_signal = CharField(null=True)
    link_to_timeout = CharField(null=True)
    Pic = CharField(null=True)

    class Meta:
        table_name = 'tm_dp'


class TM_TS(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    function_ASDU = CharField(null=True)
    addr_object = IntegerField(null=True)
    link_value = CharField(null=True)

    class Meta:
        table_name = 'tm_ts'


class TM_TI4(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    function_ASDU = CharField(null=True)
    addr_object = IntegerField(null=True)
    variable_value = CharField(null=True)
    variable_status = CharField(null=True)
    variable_Aiparam = CharField(null=True)

    class Meta:
        table_name = 'tm_ti4'


class TM_TI2(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    function_ASDU = CharField(null=True)
    addr_object = IntegerField(null=True)
    variable_value = CharField(null=True)
    variable_status = CharField(null=True)

    class Meta:
        table_name = 'tm_ti2'


class TM_TII(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    function_ASDU = CharField(null=True)
    addr_object = IntegerField(null=True)
    variable_value = CharField(null=True)
    variable_status = CharField(null=True)

    class Meta:
        table_name = 'tm_tii'


class TM_TU(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    function_ASDU = CharField(null=True)
    addr_object = IntegerField(null=True)
    variable_change = CharField(null=True)
    change_bit = IntegerField(null=True)
    descriptionTU = CharField(null=True)

    class Meta:
        table_name = 'tm_tu'


class TM_TR4(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    function_ASDU = CharField(null=True)
    addr_object = IntegerField(null=True)
    variable_change = CharField(null=True)
    descriptionTR4 = CharField(null=True)

    class Meta:
        table_name = 'tm_tr4'


class TM_TR2(BaseModel):
    variable = CharField(null=True)
    tag = CharField(null=True)
    name = CharField(null=True)
    function_ASDU = CharField(null=True)
    addr_object = IntegerField(null=True)
    variable_change = CharField(null=True)
    descriptionTR4 = CharField(null=True)

    class Meta:
        table_name = 'tm_tr2'