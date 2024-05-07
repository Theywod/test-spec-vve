#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Created with Corsair v1.0.4

Control/status register map.
"""


class _RegSampl_num:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.SAMPL_NUM_ADDR)
        return (rdata >> self._rmap.SAMPL_NUM_VAL_POS) & self._rmap.SAMPL_NUM_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.SAMPL_NUM_ADDR)
        rdata = rdata & (~(self._rmap.SAMPL_NUM_VAL_MSK << self._rmap.SAMPL_NUM_VAL_POS))
        rdata = rdata | (val << self._rmap.SAMPL_NUM_VAL_POS)
        self._rmap._if.write(self._rmap.SAMPL_NUM_ADDR, rdata)


class _RegArea0_start:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.AREA0_START_ADDR)
        return (rdata >> self._rmap.AREA0_START_VAL_POS) & self._rmap.AREA0_START_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.AREA0_START_ADDR)
        rdata = rdata & (~(self._rmap.AREA0_START_VAL_MSK << self._rmap.AREA0_START_VAL_POS))
        rdata = rdata | (val << self._rmap.AREA0_START_VAL_POS)
        self._rmap._if.write(self._rmap.AREA0_START_ADDR, rdata)


class _RegArea1_start:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.AREA1_START_ADDR)
        return (rdata >> self._rmap.AREA1_START_VAL_POS) & self._rmap.AREA1_START_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.AREA1_START_ADDR)
        rdata = rdata & (~(self._rmap.AREA1_START_VAL_MSK << self._rmap.AREA1_START_VAL_POS))
        rdata = rdata | (val << self._rmap.AREA1_START_VAL_POS)
        self._rmap._if.write(self._rmap.AREA1_START_ADDR, rdata)


class _RegArea2_start:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.AREA2_START_ADDR)
        return (rdata >> self._rmap.AREA2_START_VAL_POS) & self._rmap.AREA2_START_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.AREA2_START_ADDR)
        rdata = rdata & (~(self._rmap.AREA2_START_VAL_MSK << self._rmap.AREA2_START_VAL_POS))
        rdata = rdata | (val << self._rmap.AREA2_START_VAL_POS)
        self._rmap._if.write(self._rmap.AREA2_START_ADDR, rdata)


class _RegArea0_end:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.AREA0_END_ADDR)
        return (rdata >> self._rmap.AREA0_END_VAL_POS) & self._rmap.AREA0_END_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.AREA0_END_ADDR)
        rdata = rdata & (~(self._rmap.AREA0_END_VAL_MSK << self._rmap.AREA0_END_VAL_POS))
        rdata = rdata | (val << self._rmap.AREA0_END_VAL_POS)
        self._rmap._if.write(self._rmap.AREA0_END_ADDR, rdata)


class _RegArea1_end:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.AREA1_END_ADDR)
        return (rdata >> self._rmap.AREA1_END_VAL_POS) & self._rmap.AREA1_END_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.AREA1_END_ADDR)
        rdata = rdata & (~(self._rmap.AREA1_END_VAL_MSK << self._rmap.AREA1_END_VAL_POS))
        rdata = rdata | (val << self._rmap.AREA1_END_VAL_POS)
        self._rmap._if.write(self._rmap.AREA1_END_ADDR, rdata)


class _RegArea2_end:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.AREA2_END_ADDR)
        return (rdata >> self._rmap.AREA2_END_VAL_POS) & self._rmap.AREA2_END_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.AREA2_END_ADDR)
        rdata = rdata & (~(self._rmap.AREA2_END_VAL_MSK << self._rmap.AREA2_END_VAL_POS))
        rdata = rdata | (val << self._rmap.AREA2_END_VAL_POS)
        self._rmap._if.write(self._rmap.AREA2_END_ADDR, rdata)


class _RegBuf_ctrl:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def spec_req(self):
        """Флаг запроса спектра"""
        return 0

    @spec_req.setter
    def spec_req(self, val):
        rdata = self._rmap._if.read(self._rmap.BUF_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.BUF_CTRL_SPEC_REQ_MSK << self._rmap.BUF_CTRL_SPEC_REQ_POS))
        rdata = rdata | (val << self._rmap.BUF_CTRL_SPEC_REQ_POS)
        self._rmap._if.write(self._rmap.BUF_CTRL_ADDR, rdata)

    @property
    def area_req(self):
        """Флаг запроса трех интегралов в заданных бинах спектра"""
        return 0

    @area_req.setter
    def area_req(self, val):
        rdata = self._rmap._if.read(self._rmap.BUF_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.BUF_CTRL_AREA_REQ_MSK << self._rmap.BUF_CTRL_AREA_REQ_POS))
        rdata = rdata | (val << self._rmap.BUF_CTRL_AREA_REQ_POS)
        self._rmap._if.write(self._rmap.BUF_CTRL_ADDR, rdata)


class _RegAcc_start:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.ACC_START_ADDR)
        return (rdata >> self._rmap.ACC_START_VAL_POS) & self._rmap.ACC_START_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.ACC_START_ADDR)
        rdata = rdata & (~(self._rmap.ACC_START_VAL_MSK << self._rmap.ACC_START_VAL_POS))
        rdata = rdata | (val << self._rmap.ACC_START_VAL_POS)
        self._rmap._if.write(self._rmap.ACC_START_ADDR, rdata)


class _RegAcc_stop:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.ACC_STOP_ADDR)
        return (rdata >> self._rmap.ACC_STOP_VAL_POS) & self._rmap.ACC_STOP_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.ACC_STOP_ADDR)
        rdata = rdata & (~(self._rmap.ACC_STOP_VAL_MSK << self._rmap.ACC_STOP_VAL_POS))
        rdata = rdata | (val << self._rmap.ACC_STOP_VAL_POS)
        self._rmap._if.write(self._rmap.ACC_STOP_ADDR, rdata)


class _RegAdc_th:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.ADC_TH_ADDR)
        return (rdata >> self._rmap.ADC_TH_VAL_POS) & self._rmap.ADC_TH_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.ADC_TH_ADDR)
        rdata = rdata & (~(self._rmap.ADC_TH_VAL_MSK << self._rmap.ADC_TH_VAL_POS))
        rdata = rdata | (val << self._rmap.ADC_TH_VAL_POS)
        self._rmap._if.write(self._rmap.ADC_TH_ADDR, rdata)


class _RegAdc_filter:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def window_size(self):
        """Размер окна фильтра по степени двойки (2^window_size)"""
        rdata = self._rmap._if.read(self._rmap.ADC_FILTER_ADDR)
        return (rdata >> self._rmap.ADC_FILTER_WINDOW_SIZE_POS) & self._rmap.ADC_FILTER_WINDOW_SIZE_MSK

    @window_size.setter
    def window_size(self, val):
        rdata = self._rmap._if.read(self._rmap.ADC_FILTER_ADDR)
        rdata = rdata & (~(self._rmap.ADC_FILTER_WINDOW_SIZE_MSK << self._rmap.ADC_FILTER_WINDOW_SIZE_POS))
        rdata = rdata | (val << self._rmap.ADC_FILTER_WINDOW_SIZE_POS)
        self._rmap._if.write(self._rmap.ADC_FILTER_ADDR, rdata)

    @property
    def bypass(self):
        """Bypass"""
        rdata = self._rmap._if.read(self._rmap.ADC_FILTER_ADDR)
        return (rdata >> self._rmap.ADC_FILTER_BYPASS_POS) & self._rmap.ADC_FILTER_BYPASS_MSK

    @bypass.setter
    def bypass(self, val):
        rdata = self._rmap._if.read(self._rmap.ADC_FILTER_ADDR)
        rdata = rdata & (~(self._rmap.ADC_FILTER_BYPASS_MSK << self._rmap.ADC_FILTER_BYPASS_POS))
        rdata = rdata | (val << self._rmap.ADC_FILTER_BYPASS_POS)
        self._rmap._if.write(self._rmap.ADC_FILTER_ADDR, rdata)


class _RegBline_ctrl:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def averagings(self):
        """Количество усреднений при расчете baseline, по степени двойки (2^averagings)"""
        rdata = self._rmap._if.read(self._rmap.BLINE_CTRL_ADDR)
        return (rdata >> self._rmap.BLINE_CTRL_AVERAGINGS_POS) & self._rmap.BLINE_CTRL_AVERAGINGS_MSK

    @averagings.setter
    def averagings(self, val):
        rdata = self._rmap._if.read(self._rmap.BLINE_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.BLINE_CTRL_AVERAGINGS_MSK << self._rmap.BLINE_CTRL_AVERAGINGS_POS))
        rdata = rdata | (val << self._rmap.BLINE_CTRL_AVERAGINGS_POS)
        self._rmap._if.write(self._rmap.BLINE_CTRL_ADDR, rdata)

    @property
    def auto_baseline(self):
        """Включить автоматический расчет"""
        rdata = self._rmap._if.read(self._rmap.BLINE_CTRL_ADDR)
        return (rdata >> self._rmap.BLINE_CTRL_AUTO_BASELINE_POS) & self._rmap.BLINE_CTRL_AUTO_BASELINE_MSK

    @auto_baseline.setter
    def auto_baseline(self, val):
        rdata = self._rmap._if.read(self._rmap.BLINE_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.BLINE_CTRL_AUTO_BASELINE_MSK << self._rmap.BLINE_CTRL_AUTO_BASELINE_POS))
        rdata = rdata | (val << self._rmap.BLINE_CTRL_AUTO_BASELINE_POS)
        self._rmap._if.write(self._rmap.BLINE_CTRL_ADDR, rdata)


class _RegBline_manual:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.BLINE_MANUAL_ADDR)
        return (rdata >> self._rmap.BLINE_MANUAL_VAL_POS) & self._rmap.BLINE_MANUAL_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.BLINE_MANUAL_ADDR)
        rdata = rdata & (~(self._rmap.BLINE_MANUAL_VAL_MSK << self._rmap.BLINE_MANUAL_VAL_POS))
        rdata = rdata | (val << self._rmap.BLINE_MANUAL_VAL_POS)
        self._rmap._if.write(self._rmap.BLINE_MANUAL_ADDR, rdata)


class _RegBline_acc:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.BLINE_ACC_ADDR)
        return (rdata >> self._rmap.BLINE_ACC_VAL_POS) & self._rmap.BLINE_ACC_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.BLINE_ACC_ADDR)
        rdata = rdata & (~(self._rmap.BLINE_ACC_VAL_MSK << self._rmap.BLINE_ACC_VAL_POS))
        rdata = rdata | (val << self._rmap.BLINE_ACC_VAL_POS)
        self._rmap._if.write(self._rmap.BLINE_ACC_ADDR, rdata)


class _RegBline_trend_delay:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.BLINE_TREND_DELAY_ADDR)
        return (rdata >> self._rmap.BLINE_TREND_DELAY_VAL_POS) & self._rmap.BLINE_TREND_DELAY_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.BLINE_TREND_DELAY_ADDR)
        rdata = rdata & (~(self._rmap.BLINE_TREND_DELAY_VAL_MSK << self._rmap.BLINE_TREND_DELAY_VAL_POS))
        rdata = rdata | (val << self._rmap.BLINE_TREND_DELAY_VAL_POS)
        self._rmap._if.write(self._rmap.BLINE_TREND_DELAY_ADDR, rdata)


class _RegBline_actual:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.BLINE_ACTUAL_ADDR)
        return (rdata >> self._rmap.BLINE_ACTUAL_VAL_POS) & self._rmap.BLINE_ACTUAL_VAL_MSK


class _RegGate_ctrl:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def hysteresis_en(self):
        """Включить hysteresis снятия гейта на уровне threshold/2"""
        rdata = self._rmap._if.read(self._rmap.GATE_CTRL_ADDR)
        return (rdata >> self._rmap.GATE_CTRL_HYSTERESIS_EN_POS) & self._rmap.GATE_CTRL_HYSTERESIS_EN_MSK

    @hysteresis_en.setter
    def hysteresis_en(self, val):
        rdata = self._rmap._if.read(self._rmap.GATE_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.GATE_CTRL_HYSTERESIS_EN_MSK << self._rmap.GATE_CTRL_HYSTERESIS_EN_POS))
        rdata = rdata | (val << self._rmap.GATE_CTRL_HYSTERESIS_EN_POS)
        self._rmap._if.write(self._rmap.GATE_CTRL_ADDR, rdata)

    @property
    def pileup_reject(self):
        """Отбрасывать gates, где есть pileup"""
        rdata = self._rmap._if.read(self._rmap.GATE_CTRL_ADDR)
        return (rdata >> self._rmap.GATE_CTRL_PILEUP_REJECT_POS) & self._rmap.GATE_CTRL_PILEUP_REJECT_MSK

    @pileup_reject.setter
    def pileup_reject(self, val):
        rdata = self._rmap._if.read(self._rmap.GATE_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.GATE_CTRL_PILEUP_REJECT_MSK << self._rmap.GATE_CTRL_PILEUP_REJECT_POS))
        rdata = rdata | (val << self._rmap.GATE_CTRL_PILEUP_REJECT_POS)
        self._rmap._if.write(self._rmap.GATE_CTRL_ADDR, rdata)

    @property
    def pre_trigger(self):
        """Включение в гейт отсчетов до пересечение сигналом уровня threshold"""
        rdata = self._rmap._if.read(self._rmap.GATE_CTRL_ADDR)
        return (rdata >> self._rmap.GATE_CTRL_PRE_TRIGGER_POS) & self._rmap.GATE_CTRL_PRE_TRIGGER_MSK

    @pre_trigger.setter
    def pre_trigger(self, val):
        rdata = self._rmap._if.read(self._rmap.GATE_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.GATE_CTRL_PRE_TRIGGER_MSK << self._rmap.GATE_CTRL_PRE_TRIGGER_POS))
        rdata = rdata | (val << self._rmap.GATE_CTRL_PRE_TRIGGER_POS)
        self._rmap._if.write(self._rmap.GATE_CTRL_ADDR, rdata)


class _RegDump_ctrl:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def enable(self):
        """Захватить следующий валидный гейт"""
        return 0

    @enable.setter
    def enable(self, val):
        rdata = self._rmap._if.read(self._rmap.DUMP_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.DUMP_CTRL_ENABLE_MSK << self._rmap.DUMP_CTRL_ENABLE_POS))
        rdata = rdata | (val << self._rmap.DUMP_CTRL_ENABLE_POS)
        self._rmap._if.write(self._rmap.DUMP_CTRL_ADDR, rdata)

    @property
    def samples(self):
        """Количество семплов для набора и передачи"""
        rdata = self._rmap._if.read(self._rmap.DUMP_CTRL_ADDR)
        return (rdata >> self._rmap.DUMP_CTRL_SAMPLES_POS) & self._rmap.DUMP_CTRL_SAMPLES_MSK

    @samples.setter
    def samples(self, val):
        rdata = self._rmap._if.read(self._rmap.DUMP_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.DUMP_CTRL_SAMPLES_MSK << self._rmap.DUMP_CTRL_SAMPLES_POS))
        rdata = rdata | (val << self._rmap.DUMP_CTRL_SAMPLES_POS)
        self._rmap._if.write(self._rmap.DUMP_CTRL_ADDR, rdata)


class _RegPileup_acc:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.PILEUP_ACC_ADDR)
        return (rdata >> self._rmap.PILEUP_ACC_VAL_POS) & self._rmap.PILEUP_ACC_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.PILEUP_ACC_ADDR)
        rdata = rdata & (~(self._rmap.PILEUP_ACC_VAL_MSK << self._rmap.PILEUP_ACC_VAL_POS))
        rdata = rdata | (val << self._rmap.PILEUP_ACC_VAL_POS)
        self._rmap._if.write(self._rmap.PILEUP_ACC_ADDR, rdata)


class _RegPileup_trend_delay:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.PILEUP_TREND_DELAY_ADDR)
        return (rdata >> self._rmap.PILEUP_TREND_DELAY_VAL_POS) & self._rmap.PILEUP_TREND_DELAY_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.PILEUP_TREND_DELAY_ADDR)
        rdata = rdata & (~(self._rmap.PILEUP_TREND_DELAY_VAL_MSK << self._rmap.PILEUP_TREND_DELAY_VAL_POS))
        rdata = rdata | (val << self._rmap.PILEUP_TREND_DELAY_VAL_POS)
        self._rmap._if.write(self._rmap.PILEUP_TREND_DELAY_ADDR, rdata)


class _RegPileup_actual:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.PILEUP_ACTUAL_ADDR)
        return (rdata >> self._rmap.PILEUP_ACTUAL_VAL_POS) & self._rmap.PILEUP_ACTUAL_VAL_MSK


class _RegPileup_cnt_ctrl:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def frame_rst(self):
        """Сбрасывать счетчик каждый кадр"""
        rdata = self._rmap._if.read(self._rmap.PILEUP_CNT_CTRL_ADDR)
        return (rdata >> self._rmap.PILEUP_CNT_CTRL_FRAME_RST_POS) & self._rmap.PILEUP_CNT_CTRL_FRAME_RST_MSK

    @frame_rst.setter
    def frame_rst(self, val):
        rdata = self._rmap._if.read(self._rmap.PILEUP_CNT_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.PILEUP_CNT_CTRL_FRAME_RST_MSK << self._rmap.PILEUP_CNT_CTRL_FRAME_RST_POS))
        rdata = rdata | (val << self._rmap.PILEUP_CNT_CTRL_FRAME_RST_POS)
        self._rmap._if.write(self._rmap.PILEUP_CNT_CTRL_ADDR, rdata)

    @property
    def pileup_cnt_rst(self):
        """Сброс счетчика"""
        return 0

    @pileup_cnt_rst.setter
    def pileup_cnt_rst(self, val):
        rdata = self._rmap._if.read(self._rmap.PILEUP_CNT_CTRL_ADDR)
        rdata = rdata & (~(self._rmap.PILEUP_CNT_CTRL_PILEUP_CNT_RST_MSK << self._rmap.PILEUP_CNT_CTRL_PILEUP_CNT_RST_POS))
        rdata = rdata | (val << self._rmap.PILEUP_CNT_CTRL_PILEUP_CNT_RST_POS)
        self._rmap._if.write(self._rmap.PILEUP_CNT_CTRL_ADDR, rdata)


class _RegPileup_cnt:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.PILEUP_CNT_ADDR)
        return (rdata >> self._rmap.PILEUP_CNT_VAL_POS) & self._rmap.PILEUP_CNT_VAL_MSK


class _RegCount_th_0:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.COUNT_TH_0_ADDR)
        return (rdata >> self._rmap.COUNT_TH_0_VAL_POS) & self._rmap.COUNT_TH_0_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.COUNT_TH_0_ADDR)
        rdata = rdata & (~(self._rmap.COUNT_TH_0_VAL_MSK << self._rmap.COUNT_TH_0_VAL_POS))
        rdata = rdata | (val << self._rmap.COUNT_TH_0_VAL_POS)
        self._rmap._if.write(self._rmap.COUNT_TH_0_ADDR, rdata)


class _RegCount_val_0:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.COUNT_VAL_0_ADDR)
        return (rdata >> self._rmap.COUNT_VAL_0_VAL_POS) & self._rmap.COUNT_VAL_0_VAL_MSK


class _RegCount_th_1:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.COUNT_TH_1_ADDR)
        return (rdata >> self._rmap.COUNT_TH_1_VAL_POS) & self._rmap.COUNT_TH_1_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.COUNT_TH_1_ADDR)
        rdata = rdata & (~(self._rmap.COUNT_TH_1_VAL_MSK << self._rmap.COUNT_TH_1_VAL_POS))
        rdata = rdata | (val << self._rmap.COUNT_TH_1_VAL_POS)
        self._rmap._if.write(self._rmap.COUNT_TH_1_ADDR, rdata)


class _RegCount_val_1:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.COUNT_VAL_1_ADDR)
        return (rdata >> self._rmap.COUNT_VAL_1_VAL_POS) & self._rmap.COUNT_VAL_1_VAL_MSK


class _RegVer:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.VER_ADDR)
        return (rdata >> self._rmap.VER_VAL_POS) & self._rmap.VER_VAL_MSK


class _RegSub:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.SUB_ADDR)
        return (rdata >> self._rmap.SUB_VAL_POS) & self._rmap.SUB_VAL_MSK


class _RegRev:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.REV_ADDR)
        return (rdata >> self._rmap.REV_VAL_POS) & self._rmap.REV_VAL_MSK


class RegMap:
    """Control/Status register map"""

    # SAMPL_NUM - Длительность интервала сбора данных. 125е6 (1 сек) по-умолчанию.
    SAMPL_NUM_ADDR = 0x00000000
    SAMPL_NUM_VAL_POS = 0
    SAMPL_NUM_VAL_MSK = 0xffffffff

    # AREA0_START - Начальный бин интеграла в спектре, зона 0
    AREA0_START_ADDR = 0x00000004
    AREA0_START_VAL_POS = 0
    AREA0_START_VAL_MSK = 0xffff

    # AREA1_START - Начальный бин интеграла в спектре, зона 1
    AREA1_START_ADDR = 0x00000008
    AREA1_START_VAL_POS = 0
    AREA1_START_VAL_MSK = 0xffff

    # AREA2_START - Начальный бин интеграла в спектре, зона 2
    AREA2_START_ADDR = 0x0000000c
    AREA2_START_VAL_POS = 0
    AREA2_START_VAL_MSK = 0xffff

    # AREA0_END - Последний бин интеграла в спектре, зона 0
    AREA0_END_ADDR = 0x00000010
    AREA0_END_VAL_POS = 0
    AREA0_END_VAL_MSK = 0xffff

    # AREA1_END - Последний бин интеграла в спектре, зона 1
    AREA1_END_ADDR = 0x00000014
    AREA1_END_VAL_POS = 0
    AREA1_END_VAL_MSK = 0xffff

    # AREA2_END - Последний бин интеграла в спектре, зона 2
    AREA2_END_ADDR = 0x00000018
    AREA2_END_VAL_POS = 0
    AREA2_END_VAL_MSK = 0xffff

    # BUF_CTRL - Управление сбором данных устройства
    BUF_CTRL_ADDR = 0x0000001c
    BUF_CTRL_SPEC_REQ_POS = 0
    BUF_CTRL_SPEC_REQ_MSK = 0x1
    BUF_CTRL_AREA_REQ_POS = 1
    BUF_CTRL_AREA_REQ_MSK = 0x1

    # ACC_START - Определяет момент начала расчета интеграла внутри гейта, сдвиг от начала гейта
    ACC_START_ADDR = 0x00000020
    ACC_START_VAL_POS = 0
    ACC_START_VAL_MSK = 0xff

    # ACC_STOP - Определяет момент окончания расчета интеграла внутри гейта, сдвиг от конца гейта
    ACC_STOP_ADDR = 0x00000024
    ACC_STOP_VAL_POS = 0
    ACC_STOP_VAL_MSK = 0xff

    # ADC_TH - Уровень входного сигнала, первышение которого считается началом импульса (началом гейта)
    ADC_TH_ADDR = 0x00000028
    ADC_TH_VAL_POS = 0
    ADC_TH_VAL_MSK = 0xffff

    # ADC_FILTER - Фильтр скользящего среднего входного импульса
    ADC_FILTER_ADDR = 0x0000002c
    ADC_FILTER_WINDOW_SIZE_POS = 0
    ADC_FILTER_WINDOW_SIZE_MSK = 0x7
    ADC_FILTER_BYPASS_POS = 7
    ADC_FILTER_BYPASS_MSK = 0x1

    # BLINE_CTRL - Управление модулем расчета baseline
    BLINE_CTRL_ADDR = 0x00000030
    BLINE_CTRL_AVERAGINGS_POS = 0
    BLINE_CTRL_AVERAGINGS_MSK = 0xf
    BLINE_CTRL_AUTO_BASELINE_POS = 7
    BLINE_CTRL_AUTO_BASELINE_MSK = 0x1

    # BLINE_MANUAL - Регистр установки baseline. Знаковое число, которое вычитается из входного сигнала. Применяется только при (auto_baseline == 0)
    BLINE_MANUAL_ADDR = 0x00000034
    BLINE_MANUAL_VAL_POS = 0
    BLINE_MANUAL_VAL_MSK = 0xffff

    # BLINE_ACC - Acceptance level baseline. Размах сигнала между BLINE_TREND_DELAY точками, который считается стабильный и используется для расчета.
    BLINE_ACC_ADDR = 0x00000038
    BLINE_ACC_VAL_POS = 0
    BLINE_ACC_VAL_MSK = 0xffff

    # BLINE_TREND_DELAY - Trend delay baseline. Расстояние между двумя отсчетами сигнала, разница которых измеряется BLINE_ACC.
    BLINE_TREND_DELAY_ADDR = 0x0000003c
    BLINE_TREND_DELAY_VAL_POS = 0
    BLINE_TREND_DELAY_VAL_MSK = 0x3f

    # BLINE_ACTUAL - Текущее значение baseline. Обновляется независимо от любых других сигналов.
    BLINE_ACTUAL_ADDR = 0x00000040
    BLINE_ACTUAL_VAL_POS = 0
    BLINE_ACTUAL_VAL_MSK = 0x7fff

    # GATE_CTRL - Управление гейтом
    GATE_CTRL_ADDR = 0x00000044
    GATE_CTRL_HYSTERESIS_EN_POS = 0
    GATE_CTRL_HYSTERESIS_EN_MSK = 0x1
    GATE_CTRL_PILEUP_REJECT_POS = 1
    GATE_CTRL_PILEUP_REJECT_MSK = 0x1
    GATE_CTRL_PRE_TRIGGER_POS = 2
    GATE_CTRL_PRE_TRIGGER_MSK = 0x3f

    # DUMP_CTRL - Управление режимом осциллографа
    DUMP_CTRL_ADDR = 0x00000048
    DUMP_CTRL_ENABLE_POS = 0
    DUMP_CTRL_ENABLE_MSK = 0x1
    DUMP_CTRL_SAMPLES_POS = 1
    DUMP_CTRL_SAMPLES_MSK = 0x7ff

    # PILEUP_ACC - Acceptance level pileup. Размах сигнала между PILEUP_TREND_DELAY точками, который считается pile-up.
    PILEUP_ACC_ADDR = 0x0000004c
    PILEUP_ACC_VAL_POS = 0
    PILEUP_ACC_VAL_MSK = 0xffff

    # PILEUP_TREND_DELAY - Trend delay pileup. Расстояние между двумя отсчетами сигнала, разница которых измеряется PILEUP_ACC.
    PILEUP_TREND_DELAY_ADDR = 0x00000050
    PILEUP_TREND_DELAY_VAL_POS = 0
    PILEUP_TREND_DELAY_VAL_MSK = 0x3f

    # PILEUP_ACTUAL - Флаг наличия pile-up в последнем запрошенном DUMP_CTRL кадре
    PILEUP_ACTUAL_ADDR = 0x00000054
    PILEUP_ACTUAL_VAL_POS = 0
    PILEUP_ACTUAL_VAL_MSK = 0x1

    # PILEUP_CNT_CTRL - Управление счетчиком pile-up
    PILEUP_CNT_CTRL_ADDR = 0x00000058
    PILEUP_CNT_CTRL_FRAME_RST_POS = 0
    PILEUP_CNT_CTRL_FRAME_RST_MSK = 0x1
    PILEUP_CNT_CTRL_PILEUP_CNT_RST_POS = 1
    PILEUP_CNT_CTRL_PILEUP_CNT_RST_MSK = 0x1

    # PILEUP_CNT - Счетчик pile-up
    PILEUP_CNT_ADDR = 0x0000005c
    PILEUP_CNT_VAL_POS = 0
    PILEUP_CNT_VAL_MSK = 0xffffffff

    # COUNT_TH_0 - Threshold счетчика импульсов 0
    COUNT_TH_0_ADDR = 0x00000060
    COUNT_TH_0_VAL_POS = 0
    COUNT_TH_0_VAL_MSK = 0xffff

    # COUNT_VAL_0 - Значение счетчика 0
    COUNT_VAL_0_ADDR = 0x00000064
    COUNT_VAL_0_VAL_POS = 0
    COUNT_VAL_0_VAL_MSK = 0xffffffff

    # COUNT_TH_1 - Threshold счетчика импульсов 1
    COUNT_TH_1_ADDR = 0x00000068
    COUNT_TH_1_VAL_POS = 0
    COUNT_TH_1_VAL_MSK = 0xffff

    # COUNT_VAL_1 - Значение счетчика 1
    COUNT_VAL_1_ADDR = 0x0000006c
    COUNT_VAL_1_VAL_POS = 0
    COUNT_VAL_1_VAL_MSK = 0xffffffff

    # VER - Ревизия прошивки ПЛИС
    VER_ADDR = 0x00000400
    VER_VAL_POS = 0
    VER_VAL_MSK = 0xff

    # SUB - Подверсия прошивки ПЛИС
    SUB_ADDR = 0x00000404
    SUB_VAL_POS = 0
    SUB_VAL_MSK = 0xff

    # REV - Ревизия прошивки ПЛИС
    REV_ADDR = 0x00000408
    REV_VAL_POS = 0
    REV_VAL_MSK = 0xff

    def __init__(self, interface):
        self._if = interface

    @property
    def sampl_num(self):
        """Длительность интервала сбора данных. 125е6 (1 сек) по-умолчанию."""
        return self._if.read(self.SAMPL_NUM_ADDR)

    @sampl_num.setter
    def sampl_num(self, val):
        self._if.write(self.SAMPL_NUM_ADDR, val)

    @property
    def sampl_num_bf(self):
        return _RegSampl_num(self)

    @property
    def area0_start(self):
        """Начальный бин интеграла в спектре, зона 0"""
        return self._if.read(self.AREA0_START_ADDR)

    @area0_start.setter
    def area0_start(self, val):
        self._if.write(self.AREA0_START_ADDR, val)

    @property
    def area0_start_bf(self):
        return _RegArea0_start(self)

    @property
    def area1_start(self):
        """Начальный бин интеграла в спектре, зона 1"""
        return self._if.read(self.AREA1_START_ADDR)

    @area1_start.setter
    def area1_start(self, val):
        self._if.write(self.AREA1_START_ADDR, val)

    @property
    def area1_start_bf(self):
        return _RegArea1_start(self)

    @property
    def area2_start(self):
        """Начальный бин интеграла в спектре, зона 2"""
        return self._if.read(self.AREA2_START_ADDR)

    @area2_start.setter
    def area2_start(self, val):
        self._if.write(self.AREA2_START_ADDR, val)

    @property
    def area2_start_bf(self):
        return _RegArea2_start(self)

    @property
    def area0_end(self):
        """Последний бин интеграла в спектре, зона 0"""
        return self._if.read(self.AREA0_END_ADDR)

    @area0_end.setter
    def area0_end(self, val):
        self._if.write(self.AREA0_END_ADDR, val)

    @property
    def area0_end_bf(self):
        return _RegArea0_end(self)

    @property
    def area1_end(self):
        """Последний бин интеграла в спектре, зона 1"""
        return self._if.read(self.AREA1_END_ADDR)

    @area1_end.setter
    def area1_end(self, val):
        self._if.write(self.AREA1_END_ADDR, val)

    @property
    def area1_end_bf(self):
        return _RegArea1_end(self)

    @property
    def area2_end(self):
        """Последний бин интеграла в спектре, зона 2"""
        return self._if.read(self.AREA2_END_ADDR)

    @area2_end.setter
    def area2_end(self, val):
        self._if.write(self.AREA2_END_ADDR, val)

    @property
    def area2_end_bf(self):
        return _RegArea2_end(self)

    @property
    def buf_ctrl(self):
        """Управление сбором данных устройства"""
        return 0

    @buf_ctrl.setter
    def buf_ctrl(self, val):
        self._if.write(self.BUF_CTRL_ADDR, val)

    @property
    def buf_ctrl_bf(self):
        return _RegBuf_ctrl(self)

    @property
    def acc_start(self):
        """Определяет момент начала расчета интеграла внутри гейта, сдвиг от начала гейта"""
        return self._if.read(self.ACC_START_ADDR)

    @acc_start.setter
    def acc_start(self, val):
        self._if.write(self.ACC_START_ADDR, val)

    @property
    def acc_start_bf(self):
        return _RegAcc_start(self)

    @property
    def acc_stop(self):
        """Определяет момент окончания расчета интеграла внутри гейта, сдвиг от конца гейта"""
        return self._if.read(self.ACC_STOP_ADDR)

    @acc_stop.setter
    def acc_stop(self, val):
        self._if.write(self.ACC_STOP_ADDR, val)

    @property
    def acc_stop_bf(self):
        return _RegAcc_stop(self)

    @property
    def adc_th(self):
        """Уровень входного сигнала, первышение которого считается началом импульса (началом гейта)"""
        return self._if.read(self.ADC_TH_ADDR)

    @adc_th.setter
    def adc_th(self, val):
        self._if.write(self.ADC_TH_ADDR, val)

    @property
    def adc_th_bf(self):
        return _RegAdc_th(self)

    @property
    def adc_filter(self):
        """Фильтр скользящего среднего входного импульса"""
        return self._if.read(self.ADC_FILTER_ADDR)

    @adc_filter.setter
    def adc_filter(self, val):
        self._if.write(self.ADC_FILTER_ADDR, val)

    @property
    def adc_filter_bf(self):
        return _RegAdc_filter(self)

    @property
    def bline_ctrl(self):
        """Управление модулем расчета baseline"""
        return self._if.read(self.BLINE_CTRL_ADDR)

    @bline_ctrl.setter
    def bline_ctrl(self, val):
        self._if.write(self.BLINE_CTRL_ADDR, val)

    @property
    def bline_ctrl_bf(self):
        return _RegBline_ctrl(self)

    @property
    def bline_manual(self):
        """Регистр установки baseline. Знаковое число, которое вычитается из входного сигнала. Применяется только при (auto_baseline == 0)"""
        return self._if.read(self.BLINE_MANUAL_ADDR)

    @bline_manual.setter
    def bline_manual(self, val):
        self._if.write(self.BLINE_MANUAL_ADDR, val)

    @property
    def bline_manual_bf(self):
        return _RegBline_manual(self)

    @property
    def bline_acc(self):
        """Acceptance level baseline. Размах сигнала между BLINE_TREND_DELAY точками, который считается стабильный и используется для расчета."""
        return self._if.read(self.BLINE_ACC_ADDR)

    @bline_acc.setter
    def bline_acc(self, val):
        self._if.write(self.BLINE_ACC_ADDR, val)

    @property
    def bline_acc_bf(self):
        return _RegBline_acc(self)

    @property
    def bline_trend_delay(self):
        """Trend delay baseline. Расстояние между двумя отсчетами сигнала, разница которых измеряется BLINE_ACC."""
        return self._if.read(self.BLINE_TREND_DELAY_ADDR)

    @bline_trend_delay.setter
    def bline_trend_delay(self, val):
        self._if.write(self.BLINE_TREND_DELAY_ADDR, val)

    @property
    def bline_trend_delay_bf(self):
        return _RegBline_trend_delay(self)

    @property
    def bline_actual(self):
        """Текущее значение baseline. Обновляется независимо от любых других сигналов."""
        return self._if.read(self.BLINE_ACTUAL_ADDR)

    @property
    def bline_actual_bf(self):
        return _RegBline_actual(self)

    @property
    def gate_ctrl(self):
        """Управление гейтом"""
        return self._if.read(self.GATE_CTRL_ADDR)

    @gate_ctrl.setter
    def gate_ctrl(self, val):
        self._if.write(self.GATE_CTRL_ADDR, val)

    @property
    def gate_ctrl_bf(self):
        return _RegGate_ctrl(self)

    @property
    def dump_ctrl(self):
        """Управление режимом осциллографа"""
        return self._if.read(self.DUMP_CTRL_ADDR)

    @dump_ctrl.setter
    def dump_ctrl(self, val):
        self._if.write(self.DUMP_CTRL_ADDR, val)

    @property
    def dump_ctrl_bf(self):
        return _RegDump_ctrl(self)

    @property
    def pileup_acc(self):
        """Acceptance level pileup. Размах сигнала между PILEUP_TREND_DELAY точками, который считается pile-up."""
        return self._if.read(self.PILEUP_ACC_ADDR)

    @pileup_acc.setter
    def pileup_acc(self, val):
        self._if.write(self.PILEUP_ACC_ADDR, val)

    @property
    def pileup_acc_bf(self):
        return _RegPileup_acc(self)

    @property
    def pileup_trend_delay(self):
        """Trend delay pileup. Расстояние между двумя отсчетами сигнала, разница которых измеряется PILEUP_ACC."""
        return self._if.read(self.PILEUP_TREND_DELAY_ADDR)

    @pileup_trend_delay.setter
    def pileup_trend_delay(self, val):
        self._if.write(self.PILEUP_TREND_DELAY_ADDR, val)

    @property
    def pileup_trend_delay_bf(self):
        return _RegPileup_trend_delay(self)

    @property
    def pileup_actual(self):
        """Флаг наличия pile-up в последнем запрошенном DUMP_CTRL кадре"""
        return self._if.read(self.PILEUP_ACTUAL_ADDR)

    @property
    def pileup_actual_bf(self):
        return _RegPileup_actual(self)

    @property
    def pileup_cnt_ctrl(self):
        """Управление счетчиком pile-up"""
        return self._if.read(self.PILEUP_CNT_CTRL_ADDR)

    @pileup_cnt_ctrl.setter
    def pileup_cnt_ctrl(self, val):
        self._if.write(self.PILEUP_CNT_CTRL_ADDR, val)

    @property
    def pileup_cnt_ctrl_bf(self):
        return _RegPileup_cnt_ctrl(self)

    @property
    def pileup_cnt(self):
        """Счетчик pile-up"""
        return self._if.read(self.PILEUP_CNT_ADDR)

    @property
    def pileup_cnt_bf(self):
        return _RegPileup_cnt(self)

    @property
    def count_th_0(self):
        """Threshold счетчика импульсов 0"""
        return self._if.read(self.COUNT_TH_0_ADDR)

    @count_th_0.setter
    def count_th_0(self, val):
        self._if.write(self.COUNT_TH_0_ADDR, val)

    @property
    def count_th_0_bf(self):
        return _RegCount_th_0(self)

    @property
    def count_val_0(self):
        """Значение счетчика 0"""
        return self._if.read(self.COUNT_VAL_0_ADDR)

    @property
    def count_val_0_bf(self):
        return _RegCount_val_0(self)

    @property
    def count_th_1(self):
        """Threshold счетчика импульсов 1"""
        return self._if.read(self.COUNT_TH_1_ADDR)

    @count_th_1.setter
    def count_th_1(self, val):
        self._if.write(self.COUNT_TH_1_ADDR, val)

    @property
    def count_th_1_bf(self):
        return _RegCount_th_1(self)

    @property
    def count_val_1(self):
        """Значение счетчика 1"""
        return self._if.read(self.COUNT_VAL_1_ADDR)

    @property
    def count_val_1_bf(self):
        return _RegCount_val_1(self)

    @property
    def ver(self):
        """Ревизия прошивки ПЛИС"""
        return self._if.read(self.VER_ADDR)

    @property
    def ver_bf(self):
        return _RegVer(self)

    @property
    def sub(self):
        """Подверсия прошивки ПЛИС"""
        return self._if.read(self.SUB_ADDR)

    @property
    def sub_bf(self):
        return _RegSub(self)

    @property
    def rev(self):
        """Ревизия прошивки ПЛИС"""
        return self._if.read(self.REV_ADDR)

    @property
    def rev_bf(self):
        return _RegRev(self)
