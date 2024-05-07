// Created with Corsair v1.0.4
#ifndef __REGMAP_H
#define __REGMAP_H

#define __I  volatile const // 'read only' permissions
#define __O  volatile       // 'write only' permissions
#define __IO volatile       // 'read / write' permissions


#ifdef __cplusplus
#include <cstdint>
extern "C" {
#else
#include <stdint.h>
#endif

#define CSR_BASE_ADDR 0x0

// SAMPL_NUM - Длительность интервала сбора данных. 125е6 (1 сек) по-умолчанию.
#define CSR_SAMPL_NUM_ADDR 0x0
#define CSR_SAMPL_NUM_RESET 0x7735940
typedef struct {
    uint32_t VAL : 32; // Value of the register
} csr_sampl_num_t;

// SAMPL_NUM.val - Value of the register
#define CSR_SAMPL_NUM_VAL_WIDTH 32
#define CSR_SAMPL_NUM_VAL_LSB 0
#define CSR_SAMPL_NUM_VAL_MASK 0xffffffff
#define CSR_SAMPL_NUM_VAL_RESET 0x7735940

// AREA0_START - Начальный бин интеграла в спектре, зона 0
#define CSR_AREA0_START_ADDR 0x4
#define CSR_AREA0_START_RESET 0x0
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_area0_start_t;

// AREA0_START.val - Value of the register
#define CSR_AREA0_START_VAL_WIDTH 16
#define CSR_AREA0_START_VAL_LSB 0
#define CSR_AREA0_START_VAL_MASK 0xffff
#define CSR_AREA0_START_VAL_RESET 0x0

// AREA1_START - Начальный бин интеграла в спектре, зона 1
#define CSR_AREA1_START_ADDR 0x8
#define CSR_AREA1_START_RESET 0x0
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_area1_start_t;

// AREA1_START.val - Value of the register
#define CSR_AREA1_START_VAL_WIDTH 16
#define CSR_AREA1_START_VAL_LSB 0
#define CSR_AREA1_START_VAL_MASK 0xffff
#define CSR_AREA1_START_VAL_RESET 0x0

// AREA2_START - Начальный бин интеграла в спектре, зона 2
#define CSR_AREA2_START_ADDR 0xc
#define CSR_AREA2_START_RESET 0x0
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_area2_start_t;

// AREA2_START.val - Value of the register
#define CSR_AREA2_START_VAL_WIDTH 16
#define CSR_AREA2_START_VAL_LSB 0
#define CSR_AREA2_START_VAL_MASK 0xffff
#define CSR_AREA2_START_VAL_RESET 0x0

// AREA0_END - Последний бин интеграла в спектре, зона 0
#define CSR_AREA0_END_ADDR 0x10
#define CSR_AREA0_END_RESET 0x3ff
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_area0_end_t;

// AREA0_END.val - Value of the register
#define CSR_AREA0_END_VAL_WIDTH 16
#define CSR_AREA0_END_VAL_LSB 0
#define CSR_AREA0_END_VAL_MASK 0xffff
#define CSR_AREA0_END_VAL_RESET 0x3ff

// AREA1_END - Последний бин интеграла в спектре, зона 1
#define CSR_AREA1_END_ADDR 0x14
#define CSR_AREA1_END_RESET 0x0
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_area1_end_t;

// AREA1_END.val - Value of the register
#define CSR_AREA1_END_VAL_WIDTH 16
#define CSR_AREA1_END_VAL_LSB 0
#define CSR_AREA1_END_VAL_MASK 0xffff
#define CSR_AREA1_END_VAL_RESET 0x0

// AREA2_END - Последний бин интеграла в спектре, зона 2
#define CSR_AREA2_END_ADDR 0x18
#define CSR_AREA2_END_RESET 0x0
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_area2_end_t;

// AREA2_END.val - Value of the register
#define CSR_AREA2_END_VAL_WIDTH 16
#define CSR_AREA2_END_VAL_LSB 0
#define CSR_AREA2_END_VAL_MASK 0xffff
#define CSR_AREA2_END_VAL_RESET 0x0

// BUF_CTRL - Управление сбором данных устройства
#define CSR_BUF_CTRL_ADDR 0x1c
#define CSR_BUF_CTRL_RESET 0x0
typedef struct {
    uint32_t SPEC_REQ : 1; // Флаг запроса спектра
    uint32_t AREA_REQ : 1; // Флаг запроса трех интегралов в заданных бинах спектра
    uint32_t : 30; // reserved
} csr_buf_ctrl_t;

// BUF_CTRL.spec_req - Флаг запроса спектра
#define CSR_BUF_CTRL_SPEC_REQ_WIDTH 1
#define CSR_BUF_CTRL_SPEC_REQ_LSB 0
#define CSR_BUF_CTRL_SPEC_REQ_MASK 0x1
#define CSR_BUF_CTRL_SPEC_REQ_RESET 0x0

// BUF_CTRL.area_req - Флаг запроса трех интегралов в заданных бинах спектра
#define CSR_BUF_CTRL_AREA_REQ_WIDTH 1
#define CSR_BUF_CTRL_AREA_REQ_LSB 1
#define CSR_BUF_CTRL_AREA_REQ_MASK 0x2
#define CSR_BUF_CTRL_AREA_REQ_RESET 0x0

// ACC_START - Определяет момент начала расчета интеграла внутри гейта, сдвиг от начала гейта
#define CSR_ACC_START_ADDR 0x20
#define CSR_ACC_START_RESET 0x0
typedef struct {
    uint32_t VAL : 8; // Value of the register
    uint32_t : 24; // reserved
} csr_acc_start_t;

// ACC_START.val - Value of the register
#define CSR_ACC_START_VAL_WIDTH 8
#define CSR_ACC_START_VAL_LSB 0
#define CSR_ACC_START_VAL_MASK 0xff
#define CSR_ACC_START_VAL_RESET 0x0

// ACC_STOP - Определяет момент окончания расчета интеграла внутри гейта, сдвиг от конца гейта
#define CSR_ACC_STOP_ADDR 0x24
#define CSR_ACC_STOP_RESET 0x80
typedef struct {
    uint32_t VAL : 8; // Value of the register
    uint32_t : 24; // reserved
} csr_acc_stop_t;

// ACC_STOP.val - Value of the register
#define CSR_ACC_STOP_VAL_WIDTH 8
#define CSR_ACC_STOP_VAL_LSB 0
#define CSR_ACC_STOP_VAL_MASK 0xff
#define CSR_ACC_STOP_VAL_RESET 0x80

// ADC_TH - Уровень входного сигнала, первышение которого считается началом импульса (началом гейта)
#define CSR_ADC_TH_ADDR 0x28
#define CSR_ADC_TH_RESET 0xfa
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_adc_th_t;

// ADC_TH.val - Value of the register
#define CSR_ADC_TH_VAL_WIDTH 16
#define CSR_ADC_TH_VAL_LSB 0
#define CSR_ADC_TH_VAL_MASK 0xffff
#define CSR_ADC_TH_VAL_RESET 0xfa

// ADC_FILTER - Фильтр скользящего среднего входного импульса
#define CSR_ADC_FILTER_ADDR 0x2c
#define CSR_ADC_FILTER_RESET 0x82
typedef struct {
    uint32_t WINDOW_SIZE : 3; // Размер окна фильтра по степени двойки (2^window_size)
    uint32_t : 4; // reserved
    uint32_t BYPASS : 1; // Bypass
    uint32_t : 24; // reserved
} csr_adc_filter_t;

// ADC_FILTER.window_size - Размер окна фильтра по степени двойки (2^window_size)
#define CSR_ADC_FILTER_WINDOW_SIZE_WIDTH 3
#define CSR_ADC_FILTER_WINDOW_SIZE_LSB 0
#define CSR_ADC_FILTER_WINDOW_SIZE_MASK 0x7
#define CSR_ADC_FILTER_WINDOW_SIZE_RESET 0x2

// ADC_FILTER.bypass - Bypass
#define CSR_ADC_FILTER_BYPASS_WIDTH 1
#define CSR_ADC_FILTER_BYPASS_LSB 7
#define CSR_ADC_FILTER_BYPASS_MASK 0x80
#define CSR_ADC_FILTER_BYPASS_RESET 0x1

// BLINE_CTRL - Управление модулем расчета baseline
#define CSR_BLINE_CTRL_ADDR 0x30
#define CSR_BLINE_CTRL_RESET 0x6
typedef struct {
    uint32_t AVERAGINGS : 4; // Количество усреднений при расчете baseline, по степени двойки (2^averagings)
    uint32_t : 3; // reserved
    uint32_t AUTO_BASELINE : 1; // Включить автоматический расчет
    uint32_t : 24; // reserved
} csr_bline_ctrl_t;

// BLINE_CTRL.averagings - Количество усреднений при расчете baseline, по степени двойки (2^averagings)
#define CSR_BLINE_CTRL_AVERAGINGS_WIDTH 4
#define CSR_BLINE_CTRL_AVERAGINGS_LSB 0
#define CSR_BLINE_CTRL_AVERAGINGS_MASK 0xf
#define CSR_BLINE_CTRL_AVERAGINGS_RESET 0x6

// BLINE_CTRL.auto_baseline - Включить автоматический расчет
#define CSR_BLINE_CTRL_AUTO_BASELINE_WIDTH 1
#define CSR_BLINE_CTRL_AUTO_BASELINE_LSB 7
#define CSR_BLINE_CTRL_AUTO_BASELINE_MASK 0x80
#define CSR_BLINE_CTRL_AUTO_BASELINE_RESET 0x0

// BLINE_MANUAL - Регистр установки baseline. Знаковое число, которое вычитается из входного сигнала. Применяется только при (auto_baseline == 0)
#define CSR_BLINE_MANUAL_ADDR 0x34
#define CSR_BLINE_MANUAL_RESET 0x0
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_bline_manual_t;

// BLINE_MANUAL.val - Value of the register
#define CSR_BLINE_MANUAL_VAL_WIDTH 16
#define CSR_BLINE_MANUAL_VAL_LSB 0
#define CSR_BLINE_MANUAL_VAL_MASK 0xffff
#define CSR_BLINE_MANUAL_VAL_RESET 0x0

// BLINE_ACC - Acceptance level baseline. Размах сигнала между BLINE_TREND_DELAY точками, который считается стабильный и используется для расчета.
#define CSR_BLINE_ACC_ADDR 0x38
#define CSR_BLINE_ACC_RESET 0x14
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_bline_acc_t;

// BLINE_ACC.val - Value of the register
#define CSR_BLINE_ACC_VAL_WIDTH 16
#define CSR_BLINE_ACC_VAL_LSB 0
#define CSR_BLINE_ACC_VAL_MASK 0xffff
#define CSR_BLINE_ACC_VAL_RESET 0x14

// BLINE_TREND_DELAY - Trend delay baseline. Расстояние между двумя отсчетами сигнала, разница которых измеряется BLINE_ACC.
#define CSR_BLINE_TREND_DELAY_ADDR 0x3c
#define CSR_BLINE_TREND_DELAY_RESET 0xf
typedef struct {
    uint32_t VAL : 6; // Value of the register
    uint32_t : 26; // reserved
} csr_bline_trend_delay_t;

// BLINE_TREND_DELAY.val - Value of the register
#define CSR_BLINE_TREND_DELAY_VAL_WIDTH 6
#define CSR_BLINE_TREND_DELAY_VAL_LSB 0
#define CSR_BLINE_TREND_DELAY_VAL_MASK 0x3f
#define CSR_BLINE_TREND_DELAY_VAL_RESET 0xf

// BLINE_ACTUAL - Текущее значение baseline. Обновляется независимо от любых других сигналов.
#define CSR_BLINE_ACTUAL_ADDR 0x40
#define CSR_BLINE_ACTUAL_RESET 0x0
typedef struct {
    uint32_t VAL : 15; // Value of the register
    uint32_t : 17; // reserved
} csr_bline_actual_t;

// BLINE_ACTUAL.val - Value of the register
#define CSR_BLINE_ACTUAL_VAL_WIDTH 15
#define CSR_BLINE_ACTUAL_VAL_LSB 0
#define CSR_BLINE_ACTUAL_VAL_MASK 0x7fff
#define CSR_BLINE_ACTUAL_VAL_RESET 0x0

// GATE_CTRL - Управление гейтом
#define CSR_GATE_CTRL_ADDR 0x44
#define CSR_GATE_CTRL_RESET 0x0
typedef struct {
    uint32_t HYSTERESIS_EN : 1; // Включить hysteresis снятия гейта на уровне threshold/2
    uint32_t PILEUP_REJECT : 1; // Отбрасывать gates, где есть pileup
    uint32_t PRE_TRIGGER : 6; // Включение в гейт отсчетов до пересечение сигналом уровня threshold
    uint32_t : 24; // reserved
} csr_gate_ctrl_t;

// GATE_CTRL.hysteresis_en - Включить hysteresis снятия гейта на уровне threshold/2
#define CSR_GATE_CTRL_HYSTERESIS_EN_WIDTH 1
#define CSR_GATE_CTRL_HYSTERESIS_EN_LSB 0
#define CSR_GATE_CTRL_HYSTERESIS_EN_MASK 0x1
#define CSR_GATE_CTRL_HYSTERESIS_EN_RESET 0x0

// GATE_CTRL.pileup_reject - Отбрасывать gates, где есть pileup
#define CSR_GATE_CTRL_PILEUP_REJECT_WIDTH 1
#define CSR_GATE_CTRL_PILEUP_REJECT_LSB 1
#define CSR_GATE_CTRL_PILEUP_REJECT_MASK 0x2
#define CSR_GATE_CTRL_PILEUP_REJECT_RESET 0x0

// GATE_CTRL.pre_trigger - Включение в гейт отсчетов до пересечение сигналом уровня threshold
#define CSR_GATE_CTRL_PRE_TRIGGER_WIDTH 6
#define CSR_GATE_CTRL_PRE_TRIGGER_LSB 2
#define CSR_GATE_CTRL_PRE_TRIGGER_MASK 0xfc
#define CSR_GATE_CTRL_PRE_TRIGGER_RESET 0x0

// DUMP_CTRL - Управление режимом осциллографа
#define CSR_DUMP_CTRL_ADDR 0x48
#define CSR_DUMP_CTRL_RESET 0x0
typedef struct {
    uint32_t ENABLE : 1; // Захватить следующий валидный гейт
    uint32_t SAMPLES : 11; // Количество семплов для набора и передачи
    uint32_t : 20; // reserved
} csr_dump_ctrl_t;

// DUMP_CTRL.enable - Захватить следующий валидный гейт
#define CSR_DUMP_CTRL_ENABLE_WIDTH 1
#define CSR_DUMP_CTRL_ENABLE_LSB 0
#define CSR_DUMP_CTRL_ENABLE_MASK 0x1
#define CSR_DUMP_CTRL_ENABLE_RESET 0x0

// DUMP_CTRL.samples - Количество семплов для набора и передачи
#define CSR_DUMP_CTRL_SAMPLES_WIDTH 11
#define CSR_DUMP_CTRL_SAMPLES_LSB 1
#define CSR_DUMP_CTRL_SAMPLES_MASK 0xffe
#define CSR_DUMP_CTRL_SAMPLES_RESET 0x0

// PILEUP_ACC - Acceptance level pileup. Размах сигнала между PILEUP_TREND_DELAY точками, который считается pile-up.
#define CSR_PILEUP_ACC_ADDR 0x4c
#define CSR_PILEUP_ACC_RESET 0x14
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_pileup_acc_t;

// PILEUP_ACC.val - Value of the register
#define CSR_PILEUP_ACC_VAL_WIDTH 16
#define CSR_PILEUP_ACC_VAL_LSB 0
#define CSR_PILEUP_ACC_VAL_MASK 0xffff
#define CSR_PILEUP_ACC_VAL_RESET 0x14

// PILEUP_TREND_DELAY - Trend delay pileup. Расстояние между двумя отсчетами сигнала, разница которых измеряется PILEUP_ACC.
#define CSR_PILEUP_TREND_DELAY_ADDR 0x50
#define CSR_PILEUP_TREND_DELAY_RESET 0x0
typedef struct {
    uint32_t VAL : 6; // Value of the register
    uint32_t : 26; // reserved
} csr_pileup_trend_delay_t;

// PILEUP_TREND_DELAY.val - Value of the register
#define CSR_PILEUP_TREND_DELAY_VAL_WIDTH 6
#define CSR_PILEUP_TREND_DELAY_VAL_LSB 0
#define CSR_PILEUP_TREND_DELAY_VAL_MASK 0x3f
#define CSR_PILEUP_TREND_DELAY_VAL_RESET 0x0

// PILEUP_ACTUAL - Флаг наличия pile-up в последнем запрошенном DUMP_CTRL кадре
#define CSR_PILEUP_ACTUAL_ADDR 0x54
#define CSR_PILEUP_ACTUAL_RESET 0x0
typedef struct {
    uint32_t VAL : 1; // Value of the register
    uint32_t : 31; // reserved
} csr_pileup_actual_t;

// PILEUP_ACTUAL.val - Value of the register
#define CSR_PILEUP_ACTUAL_VAL_WIDTH 1
#define CSR_PILEUP_ACTUAL_VAL_LSB 0
#define CSR_PILEUP_ACTUAL_VAL_MASK 0x1
#define CSR_PILEUP_ACTUAL_VAL_RESET 0x0

// PILEUP_CNT_CTRL - Управление счетчиком pile-up
#define CSR_PILEUP_CNT_CTRL_ADDR 0x58
#define CSR_PILEUP_CNT_CTRL_RESET 0x0
typedef struct {
    uint32_t FRAME_RST : 1; // Сбрасывать счетчик каждый кадр
    uint32_t PILEUP_CNT_RST : 1; // Сброс счетчика
    uint32_t : 30; // reserved
} csr_pileup_cnt_ctrl_t;

// PILEUP_CNT_CTRL.frame_rst - Сбрасывать счетчик каждый кадр
#define CSR_PILEUP_CNT_CTRL_FRAME_RST_WIDTH 1
#define CSR_PILEUP_CNT_CTRL_FRAME_RST_LSB 0
#define CSR_PILEUP_CNT_CTRL_FRAME_RST_MASK 0x1
#define CSR_PILEUP_CNT_CTRL_FRAME_RST_RESET 0x0

// PILEUP_CNT_CTRL.pileup_cnt_rst - Сброс счетчика
#define CSR_PILEUP_CNT_CTRL_PILEUP_CNT_RST_WIDTH 1
#define CSR_PILEUP_CNT_CTRL_PILEUP_CNT_RST_LSB 1
#define CSR_PILEUP_CNT_CTRL_PILEUP_CNT_RST_MASK 0x2
#define CSR_PILEUP_CNT_CTRL_PILEUP_CNT_RST_RESET 0x0

// PILEUP_CNT - Счетчик pile-up
#define CSR_PILEUP_CNT_ADDR 0x5c
#define CSR_PILEUP_CNT_RESET 0x0
typedef struct {
    uint32_t VAL : 32; // Value of the register
} csr_pileup_cnt_t;

// PILEUP_CNT.val - Value of the register
#define CSR_PILEUP_CNT_VAL_WIDTH 32
#define CSR_PILEUP_CNT_VAL_LSB 0
#define CSR_PILEUP_CNT_VAL_MASK 0xffffffff
#define CSR_PILEUP_CNT_VAL_RESET 0x0

// COUNT_TH_0 - Threshold счетчика импульсов 0
#define CSR_COUNT_TH_0_ADDR 0x60
#define CSR_COUNT_TH_0_RESET 0xfa
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_count_th_0_t;

// COUNT_TH_0.val - Value of the register
#define CSR_COUNT_TH_0_VAL_WIDTH 16
#define CSR_COUNT_TH_0_VAL_LSB 0
#define CSR_COUNT_TH_0_VAL_MASK 0xffff
#define CSR_COUNT_TH_0_VAL_RESET 0xfa

// COUNT_VAL_0 - Значение счетчика 0
#define CSR_COUNT_VAL_0_ADDR 0x64
#define CSR_COUNT_VAL_0_RESET 0x0
typedef struct {
    uint32_t VAL : 32; // Value of the register
} csr_count_val_0_t;

// COUNT_VAL_0.val - Value of the register
#define CSR_COUNT_VAL_0_VAL_WIDTH 32
#define CSR_COUNT_VAL_0_VAL_LSB 0
#define CSR_COUNT_VAL_0_VAL_MASK 0xffffffff
#define CSR_COUNT_VAL_0_VAL_RESET 0x0

// COUNT_TH_1 - Threshold счетчика импульсов 1
#define CSR_COUNT_TH_1_ADDR 0x68
#define CSR_COUNT_TH_1_RESET 0x1f4
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_count_th_1_t;

// COUNT_TH_1.val - Value of the register
#define CSR_COUNT_TH_1_VAL_WIDTH 16
#define CSR_COUNT_TH_1_VAL_LSB 0
#define CSR_COUNT_TH_1_VAL_MASK 0xffff
#define CSR_COUNT_TH_1_VAL_RESET 0x1f4

// COUNT_VAL_1 - Значение счетчика 1
#define CSR_COUNT_VAL_1_ADDR 0x6c
#define CSR_COUNT_VAL_1_RESET 0x0
typedef struct {
    uint32_t VAL : 32; // Value of the register
} csr_count_val_1_t;

// COUNT_VAL_1.val - Value of the register
#define CSR_COUNT_VAL_1_VAL_WIDTH 32
#define CSR_COUNT_VAL_1_VAL_LSB 0
#define CSR_COUNT_VAL_1_VAL_MASK 0xffffffff
#define CSR_COUNT_VAL_1_VAL_RESET 0x0

// VER - Ревизия прошивки ПЛИС
#define CSR_VER_ADDR 0x400
#define CSR_VER_RESET 0x0
typedef struct {
    uint32_t VAL : 8; // Value of the register
    uint32_t : 24; // reserved
} csr_ver_t;

// VER.val - Value of the register
#define CSR_VER_VAL_WIDTH 8
#define CSR_VER_VAL_LSB 0
#define CSR_VER_VAL_MASK 0xff
#define CSR_VER_VAL_RESET 0x0

// SUB - Подверсия прошивки ПЛИС
#define CSR_SUB_ADDR 0x404
#define CSR_SUB_RESET 0x0
typedef struct {
    uint32_t VAL : 8; // Value of the register
    uint32_t : 24; // reserved
} csr_sub_t;

// SUB.val - Value of the register
#define CSR_SUB_VAL_WIDTH 8
#define CSR_SUB_VAL_LSB 0
#define CSR_SUB_VAL_MASK 0xff
#define CSR_SUB_VAL_RESET 0x0

// REV - Ревизия прошивки ПЛИС
#define CSR_REV_ADDR 0x408
#define CSR_REV_RESET 0x0
typedef struct {
    uint32_t VAL : 8; // Value of the register
    uint32_t : 24; // reserved
} csr_rev_t;

// REV.val - Value of the register
#define CSR_REV_VAL_WIDTH 8
#define CSR_REV_VAL_LSB 0
#define CSR_REV_VAL_MASK 0xff
#define CSR_REV_VAL_RESET 0x0


// Register map structure
typedef struct {
    union {
        __IO uint32_t SAMPL_NUM; // Длительность интервала сбора данных. 125е6 (1 сек) по-умолчанию.
        __IO csr_sampl_num_t SAMPL_NUM_bf; // Bit access for SAMPL_NUM register
    };
    union {
        __IO uint32_t AREA0_START; // Начальный бин интеграла в спектре, зона 0
        __IO csr_area0_start_t AREA0_START_bf; // Bit access for AREA0_START register
    };
    union {
        __IO uint32_t AREA1_START; // Начальный бин интеграла в спектре, зона 1
        __IO csr_area1_start_t AREA1_START_bf; // Bit access for AREA1_START register
    };
    union {
        __IO uint32_t AREA2_START; // Начальный бин интеграла в спектре, зона 2
        __IO csr_area2_start_t AREA2_START_bf; // Bit access for AREA2_START register
    };
    union {
        __IO uint32_t AREA0_END; // Последний бин интеграла в спектре, зона 0
        __IO csr_area0_end_t AREA0_END_bf; // Bit access for AREA0_END register
    };
    union {
        __IO uint32_t AREA1_END; // Последний бин интеграла в спектре, зона 1
        __IO csr_area1_end_t AREA1_END_bf; // Bit access for AREA1_END register
    };
    union {
        __IO uint32_t AREA2_END; // Последний бин интеграла в спектре, зона 2
        __IO csr_area2_end_t AREA2_END_bf; // Bit access for AREA2_END register
    };
    union {
        __O uint32_t BUF_CTRL; // Управление сбором данных устройства
        __O csr_buf_ctrl_t BUF_CTRL_bf; // Bit access for BUF_CTRL register
    };
    union {
        __IO uint32_t ACC_START; // Определяет момент начала расчета интеграла внутри гейта, сдвиг от начала гейта
        __IO csr_acc_start_t ACC_START_bf; // Bit access for ACC_START register
    };
    union {
        __IO uint32_t ACC_STOP; // Определяет момент окончания расчета интеграла внутри гейта, сдвиг от конца гейта
        __IO csr_acc_stop_t ACC_STOP_bf; // Bit access for ACC_STOP register
    };
    union {
        __IO uint32_t ADC_TH; // Уровень входного сигнала, первышение которого считается началом импульса (началом гейта)
        __IO csr_adc_th_t ADC_TH_bf; // Bit access for ADC_TH register
    };
    union {
        __IO uint32_t ADC_FILTER; // Фильтр скользящего среднего входного импульса
        __IO csr_adc_filter_t ADC_FILTER_bf; // Bit access for ADC_FILTER register
    };
    union {
        __IO uint32_t BLINE_CTRL; // Управление модулем расчета baseline
        __IO csr_bline_ctrl_t BLINE_CTRL_bf; // Bit access for BLINE_CTRL register
    };
    union {
        __IO uint32_t BLINE_MANUAL; // Регистр установки baseline. Знаковое число, которое вычитается из входного сигнала. Применяется только при (auto_baseline == 0)
        __IO csr_bline_manual_t BLINE_MANUAL_bf; // Bit access for BLINE_MANUAL register
    };
    union {
        __IO uint32_t BLINE_ACC; // Acceptance level baseline. Размах сигнала между BLINE_TREND_DELAY точками, который считается стабильный и используется для расчета.
        __IO csr_bline_acc_t BLINE_ACC_bf; // Bit access for BLINE_ACC register
    };
    union {
        __IO uint32_t BLINE_TREND_DELAY; // Trend delay baseline. Расстояние между двумя отсчетами сигнала, разница которых измеряется BLINE_ACC.
        __IO csr_bline_trend_delay_t BLINE_TREND_DELAY_bf; // Bit access for BLINE_TREND_DELAY register
    };
    union {
        __I uint32_t BLINE_ACTUAL; // Текущее значение baseline. Обновляется независимо от любых других сигналов.
        __I csr_bline_actual_t BLINE_ACTUAL_bf; // Bit access for BLINE_ACTUAL register
    };
    union {
        __IO uint32_t GATE_CTRL; // Управление гейтом
        __IO csr_gate_ctrl_t GATE_CTRL_bf; // Bit access for GATE_CTRL register
    };
    union {
        __IO uint32_t DUMP_CTRL; // Управление режимом осциллографа
        __IO csr_dump_ctrl_t DUMP_CTRL_bf; // Bit access for DUMP_CTRL register
    };
    union {
        __IO uint32_t PILEUP_ACC; // Acceptance level pileup. Размах сигнала между PILEUP_TREND_DELAY точками, который считается pile-up.
        __IO csr_pileup_acc_t PILEUP_ACC_bf; // Bit access for PILEUP_ACC register
    };
    union {
        __IO uint32_t PILEUP_TREND_DELAY; // Trend delay pileup. Расстояние между двумя отсчетами сигнала, разница которых измеряется PILEUP_ACC.
        __IO csr_pileup_trend_delay_t PILEUP_TREND_DELAY_bf; // Bit access for PILEUP_TREND_DELAY register
    };
    union {
        __I uint32_t PILEUP_ACTUAL; // Флаг наличия pile-up в последнем запрошенном DUMP_CTRL кадре
        __I csr_pileup_actual_t PILEUP_ACTUAL_bf; // Bit access for PILEUP_ACTUAL register
    };
    union {
        __IO uint32_t PILEUP_CNT_CTRL; // Управление счетчиком pile-up
        __IO csr_pileup_cnt_ctrl_t PILEUP_CNT_CTRL_bf; // Bit access for PILEUP_CNT_CTRL register
    };
    union {
        __I uint32_t PILEUP_CNT; // Счетчик pile-up
        __I csr_pileup_cnt_t PILEUP_CNT_bf; // Bit access for PILEUP_CNT register
    };
    union {
        __IO uint32_t COUNT_TH_0; // Threshold счетчика импульсов 0
        __IO csr_count_th_0_t COUNT_TH_0_bf; // Bit access for COUNT_TH_0 register
    };
    union {
        __I uint32_t COUNT_VAL_0; // Значение счетчика 0
        __I csr_count_val_0_t COUNT_VAL_0_bf; // Bit access for COUNT_VAL_0 register
    };
    union {
        __IO uint32_t COUNT_TH_1; // Threshold счетчика импульсов 1
        __IO csr_count_th_1_t COUNT_TH_1_bf; // Bit access for COUNT_TH_1 register
    };
    union {
        __I uint32_t COUNT_VAL_1; // Значение счетчика 1
        __I csr_count_val_1_t COUNT_VAL_1_bf; // Bit access for COUNT_VAL_1 register
    };
    __IO uint32_t RESERVED0[228];
    union {
        __I uint32_t VER; // Ревизия прошивки ПЛИС
        __I csr_ver_t VER_bf; // Bit access for VER register
    };
    union {
        __I uint32_t SUB; // Подверсия прошивки ПЛИС
        __I csr_sub_t SUB_bf; // Bit access for SUB register
    };
    union {
        __I uint32_t REV; // Ревизия прошивки ПЛИС
        __I csr_rev_t REV_bf; // Bit access for REV register
    };
} csr_t;

#define CSR ((csr_t*)(CSR_BASE_ADDR))

#ifdef __cplusplus
}
#endif

#endif /* __REGMAP_H */