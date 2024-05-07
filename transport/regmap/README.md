# Register map

Created with [Corsair](https://github.com/esynr3z/corsair) v1.0.4.

## Conventions

| Access mode | Description               |
| :---------- | :------------------------ |
| rw          | Read and Write            |
| rw1c        | Read and Write 1 to Clear |
| rw1s        | Read and Write 1 to Set   |
| ro          | Read Only                 |
| roc         | Read Only to Clear        |
| roll        | Read Only / Latch Low     |
| rolh        | Read Only / Latch High    |
| wo          | Write only                |
| wosc        | Write Only / Self Clear   |

## Register map summary

Base address: 0x00000000

| Name                     | Address    | Description |
| :---                     | :---       | :---        |
| [SAMPL_NUM](#sampl_num)  | 0x00000000 | Длительность интервала сбора данных. 125е6 (1 сек) по-умолчанию. |
| [AREA0_START](#area0_start) | 0x00000004 | Начальный бин интеграла в спектре, зона 0 |
| [AREA1_START](#area1_start) | 0x00000008 | Начальный бин интеграла в спектре, зона 1 |
| [AREA2_START](#area2_start) | 0x0000000c | Начальный бин интеграла в спектре, зона 2 |
| [AREA0_END](#area0_end)  | 0x00000010 | Последний бин интеграла в спектре, зона 0 |
| [AREA1_END](#area1_end)  | 0x00000014 | Последний бин интеграла в спектре, зона 1 |
| [AREA2_END](#area2_end)  | 0x00000018 | Последний бин интеграла в спектре, зона 2 |
| [BUF_CTRL](#buf_ctrl)    | 0x0000001c | Управление сбором данных устройства |
| [ACC_START](#acc_start)  | 0x00000020 | Определяет момент начала расчета интеграла внутри гейта, сдвиг от начала гейта |
| [ACC_STOP](#acc_stop)    | 0x00000024 | Определяет момент окончания расчета интеграла внутри гейта, сдвиг от конца гейта |
| [ADC_TH](#adc_th)        | 0x00000028 | Уровень входного сигнала, первышение которого считается началом импульса (началом гейта) |
| [ADC_FILTER](#adc_filter) | 0x0000002c | Фильтр скользящего среднего входного импульса |
| [BLINE_CTRL](#bline_ctrl) | 0x00000030 | Управление модулем расчета baseline |
| [BLINE_MANUAL](#bline_manual) | 0x00000034 | Регистр установки baseline. Знаковое число, которое вычитается из входного сигнала. Применяется только при (auto_baseline == 0) |
| [BLINE_ACC](#bline_acc)  | 0x00000038 | Acceptance level baseline. Размах сигнала между BLINE_TREND_DELAY точками, который считается стабильный и используется для расчета. |
| [BLINE_TREND_DELAY](#bline_trend_delay) | 0x0000003c | Trend delay baseline. Расстояние между двумя отсчетами сигнала, разница которых измеряется BLINE_ACC. |
| [BLINE_ACTUAL](#bline_actual) | 0x00000040 | Текущее значение baseline. Обновляется независимо от любых других сигналов. |
| [GATE_CTRL](#gate_ctrl)  | 0x00000044 | Управление гейтом |
| [DUMP_CTRL](#dump_ctrl)  | 0x00000048 | Управление режимом осциллографа |
| [PILEUP_ACC](#pileup_acc) | 0x0000004c | Acceptance level pileup. Размах сигнала между PILEUP_TREND_DELAY точками, который считается pile-up. |
| [PILEUP_TREND_DELAY](#pileup_trend_delay) | 0x00000050 | Trend delay pileup. Расстояние между двумя отсчетами сигнала, разница которых измеряется PILEUP_ACC. |
| [PILEUP_ACTUAL](#pileup_actual) | 0x00000054 | Флаг наличия pile-up в последнем запрошенном DUMP_CTRL кадре |
| [PILEUP_CNT_CTRL](#pileup_cnt_ctrl) | 0x00000058 | Управление счетчиком pile-up |
| [PILEUP_CNT](#pileup_cnt) | 0x0000005c | Счетчик pile-up |
| [COUNT_TH_0](#count_th_0) | 0x00000060 | Threshold счетчика импульсов 0 |
| [COUNT_VAL_0](#count_val_0) | 0x00000064 | Значение счетчика 0 |
| [COUNT_TH_1](#count_th_1) | 0x00000068 | Threshold счетчика импульсов 1 |
| [COUNT_VAL_1](#count_val_1) | 0x0000006c | Значение счетчика 1 |
| [VER](#ver)              | 0x00000400 | Ревизия прошивки ПЛИС |
| [SUB](#sub)              | 0x00000404 | Подверсия прошивки ПЛИС |
| [REV](#rev)              | 0x00000408 | Ревизия прошивки ПЛИС |

## SAMPL_NUM

Длительность интервала сбора данных. 125е6 (1 сек) по-умолчанию.

Address offset: 0x00000000

Reset value: 0x07735940

![sampl_num](regs_img/sampl_num.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| val              | 31:0   | rw              | 0x07735940 | Value of the register |

Back to [Register map](#register-map-summary).

## AREA0_START

Начальный бин интеграла в спектре, зона 0

Address offset: 0x00000004

Reset value: 0x00000000

![area0_start](regs_img/area0_start.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x0000     | Value of the register |

Back to [Register map](#register-map-summary).

## AREA1_START

Начальный бин интеграла в спектре, зона 1

Address offset: 0x00000008

Reset value: 0x00000000

![area1_start](regs_img/area1_start.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x0000     | Value of the register |

Back to [Register map](#register-map-summary).

## AREA2_START

Начальный бин интеграла в спектре, зона 2

Address offset: 0x0000000c

Reset value: 0x00000000

![area2_start](regs_img/area2_start.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x0000     | Value of the register |

Back to [Register map](#register-map-summary).

## AREA0_END

Последний бин интеграла в спектре, зона 0

Address offset: 0x00000010

Reset value: 0x000003ff

![area0_end](regs_img/area0_end.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x03ff     | Value of the register |

Back to [Register map](#register-map-summary).

## AREA1_END

Последний бин интеграла в спектре, зона 1

Address offset: 0x00000014

Reset value: 0x00000000

![area1_end](regs_img/area1_end.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x0000     | Value of the register |

Back to [Register map](#register-map-summary).

## AREA2_END

Последний бин интеграла в спектре, зона 2

Address offset: 0x00000018

Reset value: 0x00000000

![area2_end](regs_img/area2_end.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x0000     | Value of the register |

Back to [Register map](#register-map-summary).

## BUF_CTRL

Управление сбором данных устройства

Address offset: 0x0000001c

Reset value: 0x00000000

![buf_ctrl](regs_img/buf_ctrl.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:2   | -               | 0x0000000  | Reserved |
| area_req         | 1      | wo              | 0x0        | Флаг запроса трех интегралов в заданных бинах спектра |
| spec_req         | 0      | wo              | 0x0        | Флаг запроса спектра |

Back to [Register map](#register-map-summary).

## ACC_START

Определяет момент начала расчета интеграла внутри гейта, сдвиг от начала гейта

Address offset: 0x00000020

Reset value: 0x00000000

![acc_start](regs_img/acc_start.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:8   | -               | 0x000000   | Reserved |
| val              | 7:0    | rw              | 0x00       | Value of the register |

Back to [Register map](#register-map-summary).

## ACC_STOP

Определяет момент окончания расчета интеграла внутри гейта, сдвиг от конца гейта

Address offset: 0x00000024

Reset value: 0x00000080

![acc_stop](regs_img/acc_stop.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:8   | -               | 0x000000   | Reserved |
| val              | 7:0    | rw              | 0x80       | Value of the register |

Back to [Register map](#register-map-summary).

## ADC_TH

Уровень входного сигнала, первышение которого считается началом импульса (началом гейта)

Address offset: 0x00000028

Reset value: 0x000000fa

![adc_th](regs_img/adc_th.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x00fa     | Value of the register |

Back to [Register map](#register-map-summary).

## ADC_FILTER

Фильтр скользящего среднего входного импульса

Address offset: 0x0000002c

Reset value: 0x00000082

![adc_filter](regs_img/adc_filter.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:8   | -               | 0x000000   | Reserved |
| bypass           | 7      | rw              | 0x1        | Bypass |
| -                | 6:3    | -               | 0x0        | Reserved |
| window_size      | 2:0    | rw              | 0x2        | Размер окна фильтра по степени двойки (2^window_size) |

Back to [Register map](#register-map-summary).

## BLINE_CTRL

Управление модулем расчета baseline

Address offset: 0x00000030

Reset value: 0x00000006

![bline_ctrl](regs_img/bline_ctrl.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:8   | -               | 0x000000   | Reserved |
| auto_baseline    | 7      | rw              | 0x0        | Включить автоматический расчет |
| -                | 6:4    | -               | 0x0        | Reserved |
| averagings       | 3:0    | rw              | 0x6        | Количество усреднений при расчете baseline, по степени двойки (2^averagings) |

Back to [Register map](#register-map-summary).

## BLINE_MANUAL

Регистр установки baseline. Знаковое число, которое вычитается из входного сигнала. Применяется только при (auto_baseline == 0)

Address offset: 0x00000034

Reset value: 0x00000000

![bline_manual](regs_img/bline_manual.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x0000     | Value of the register |

Back to [Register map](#register-map-summary).

## BLINE_ACC

Acceptance level baseline. Размах сигнала между BLINE_TREND_DELAY точками, который считается стабильный и используется для расчета.

Address offset: 0x00000038

Reset value: 0x00000014

![bline_acc](regs_img/bline_acc.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x0014     | Value of the register |

Back to [Register map](#register-map-summary).

## BLINE_TREND_DELAY

Trend delay baseline. Расстояние между двумя отсчетами сигнала, разница которых измеряется BLINE_ACC.

Address offset: 0x0000003c

Reset value: 0x0000000f

![bline_trend_delay](regs_img/bline_trend_delay.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:6   | -               | 0x000000   | Reserved |
| val              | 5:0    | rw              | 0xf        | Value of the register |

Back to [Register map](#register-map-summary).

## BLINE_ACTUAL

Текущее значение baseline. Обновляется независимо от любых других сигналов.

Address offset: 0x00000040

Reset value: 0x00000000

![bline_actual](regs_img/bline_actual.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:15  | -               | 0x0000     | Reserved |
| val              | 14:0   | ro              | 0x000      | Value of the register |

Back to [Register map](#register-map-summary).

## GATE_CTRL

Управление гейтом

Address offset: 0x00000044

Reset value: 0x00000000

![gate_ctrl](regs_img/gate_ctrl.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:8   | -               | 0x000000   | Reserved |
| pre_trigger      | 7:2    | rw              | 0x0        | Включение в гейт отсчетов до пересечение сигналом уровня threshold |
| pileup_reject    | 1      | rw              | 0x0        | Отбрасывать gates, где есть pileup |
| hysteresis_en    | 0      | rw              | 0x0        | Включить hysteresis снятия гейта на уровне threshold/2 |

Back to [Register map](#register-map-summary).

## DUMP_CTRL

Управление режимом осциллографа

Address offset: 0x00000048

Reset value: 0x00000000

![dump_ctrl](regs_img/dump_ctrl.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:12  | -               | 0x00000    | Reserved |
| samples          | 11:1   | rw              | 0x00       | Количество семплов для набора и передачи |
| enable           | 0      | wosc            | 0x0        | Захватить следующий валидный гейт |

Back to [Register map](#register-map-summary).

## PILEUP_ACC

Acceptance level pileup. Размах сигнала между PILEUP_TREND_DELAY точками, который считается pile-up.

Address offset: 0x0000004c

Reset value: 0x00000014

![pileup_acc](regs_img/pileup_acc.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x0014     | Value of the register |

Back to [Register map](#register-map-summary).

## PILEUP_TREND_DELAY

Trend delay pileup. Расстояние между двумя отсчетами сигнала, разница которых измеряется PILEUP_ACC.

Address offset: 0x00000050

Reset value: 0x00000000

![pileup_trend_delay](regs_img/pileup_trend_delay.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:6   | -               | 0x000000   | Reserved |
| val              | 5:0    | rw              | 0x0        | Value of the register |

Back to [Register map](#register-map-summary).

## PILEUP_ACTUAL

Флаг наличия pile-up в последнем запрошенном DUMP_CTRL кадре

Address offset: 0x00000054

Reset value: 0x00000000

![pileup_actual](regs_img/pileup_actual.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:1   | -               | 0x0000000  | Reserved |
| val              | 0      | ro              | 0x0        | Value of the register |

Back to [Register map](#register-map-summary).

## PILEUP_CNT_CTRL

Управление счетчиком pile-up

Address offset: 0x00000058

Reset value: 0x00000000

![pileup_cnt_ctrl](regs_img/pileup_cnt_ctrl.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:2   | -               | 0x0000000  | Reserved |
| pileup_cnt_rst   | 1      | wosc            | 0x0        | Сброс счетчика |
| frame_rst        | 0      | rw              | 0x0        | Сбрасывать счетчик каждый кадр |

Back to [Register map](#register-map-summary).

## PILEUP_CNT

Счетчик pile-up

Address offset: 0x0000005c

Reset value: 0x00000000

![pileup_cnt](regs_img/pileup_cnt.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| val              | 31:0   | ro              | 0x00000000 | Value of the register |

Back to [Register map](#register-map-summary).

## COUNT_TH_0

Threshold счетчика импульсов 0

Address offset: 0x00000060

Reset value: 0x000000fa

![count_th_0](regs_img/count_th_0.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x00fa     | Value of the register |

Back to [Register map](#register-map-summary).

## COUNT_VAL_0

Значение счетчика 0

Address offset: 0x00000064

Reset value: 0x00000000

![count_val_0](regs_img/count_val_0.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| val              | 31:0   | ro              | 0x00000000 | Value of the register |

Back to [Register map](#register-map-summary).

## COUNT_TH_1

Threshold счетчика импульсов 1

Address offset: 0x00000068

Reset value: 0x000001f4

![count_th_1](regs_img/count_th_1.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x01f4     | Value of the register |

Back to [Register map](#register-map-summary).

## COUNT_VAL_1

Значение счетчика 1

Address offset: 0x0000006c

Reset value: 0x00000000

![count_val_1](regs_img/count_val_1.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| val              | 31:0   | ro              | 0x00000000 | Value of the register |

Back to [Register map](#register-map-summary).

## VER

Ревизия прошивки ПЛИС

Address offset: 0x00000400

Reset value: 0x00000000

![ver](regs_img/ver.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:8   | -               | 0x000000   | Reserved |
| val              | 7:0    | ro              | 0x00       | Value of the register |

Back to [Register map](#register-map-summary).

## SUB

Подверсия прошивки ПЛИС

Address offset: 0x00000404

Reset value: 0x00000000

![sub](regs_img/sub.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:8   | -               | 0x000000   | Reserved |
| val              | 7:0    | ro              | 0x00       | Value of the register |

Back to [Register map](#register-map-summary).

## REV

Ревизия прошивки ПЛИС

Address offset: 0x00000408

Reset value: 0x00000000

![rev](regs_img/rev.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:8   | -               | 0x000000   | Reserved |
| val              | 7:0    | ro              | 0x00       | Value of the register |

Back to [Register map](#register-map-summary).
