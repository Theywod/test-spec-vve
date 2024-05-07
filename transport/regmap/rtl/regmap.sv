// Created with Corsair v1.0.4

module regmap #(
    parameter ADDR_W = 32,
    parameter DATA_W = 32,
    parameter STRB_W = DATA_W / 8
)(
    // System
    input clk,
    input rst,
    // SAMPL_NUM.val
    output [31:0] csr_sampl_num_val_out,

    // AREA0_START.val
    output [15:0] csr_area0_start_val_out,

    // AREA1_START.val
    output [15:0] csr_area1_start_val_out,

    // AREA2_START.val
    output [15:0] csr_area2_start_val_out,

    // AREA0_END.val
    output [15:0] csr_area0_end_val_out,

    // AREA1_END.val
    output [15:0] csr_area1_end_val_out,

    // AREA2_END.val
    output [15:0] csr_area2_end_val_out,

    // BUF_CTRL.spec_req
    output  csr_buf_ctrl_spec_req_out,
    // BUF_CTRL.area_req
    output  csr_buf_ctrl_area_req_out,

    // ACC_START.val
    output [7:0] csr_acc_start_val_out,

    // ACC_STOP.val
    output [7:0] csr_acc_stop_val_out,

    // ADC_TH.val
    output [15:0] csr_adc_th_val_out,

    // ADC_FILTER.window_size
    output [2:0] csr_adc_filter_window_size_out,
    // ADC_FILTER.bypass
    output  csr_adc_filter_bypass_out,

    // BLINE_CTRL.averagings
    output [3:0] csr_bline_ctrl_averagings_out,
    // BLINE_CTRL.auto_baseline
    output  csr_bline_ctrl_auto_baseline_out,

    // BLINE_MANUAL.val
    output [15:0] csr_bline_manual_val_out,

    // BLINE_ACC.val
    output [15:0] csr_bline_acc_val_out,

    // BLINE_TREND_DELAY.val
    output [5:0] csr_bline_trend_delay_val_out,

    // BLINE_ACTUAL.val
    input csr_bline_actual_val_en,
    input [14:0] csr_bline_actual_val_in,

    // GATE_CTRL.hysteresis_en
    output  csr_gate_ctrl_hysteresis_en_out,
    // GATE_CTRL.pileup_reject
    output  csr_gate_ctrl_pileup_reject_out,
    // GATE_CTRL.pre_trigger
    output [5:0] csr_gate_ctrl_pre_trigger_out,

    // DUMP_CTRL.enable
    output  csr_dump_ctrl_enable_out,
    // DUMP_CTRL.samples
    output [10:0] csr_dump_ctrl_samples_out,

    // PILEUP_ACC.val
    output [15:0] csr_pileup_acc_val_out,

    // PILEUP_TREND_DELAY.val
    output [5:0] csr_pileup_trend_delay_val_out,

    // PILEUP_ACTUAL.val
    input csr_pileup_actual_val_en,
    input  csr_pileup_actual_val_in,

    // PILEUP_CNT_CTRL.frame_rst
    output  csr_pileup_cnt_ctrl_frame_rst_out,
    // PILEUP_CNT_CTRL.pileup_cnt_rst
    output  csr_pileup_cnt_ctrl_pileup_cnt_rst_out,

    // PILEUP_CNT.val
    input [31:0] csr_pileup_cnt_val_in,

    // COUNT_TH_0.val
    output [15:0] csr_count_th_0_val_out,

    // COUNT_VAL_0.val
    input csr_count_val_0_val_en,
    input [31:0] csr_count_val_0_val_in,

    // COUNT_TH_1.val
    output [15:0] csr_count_th_1_val_out,

    // COUNT_VAL_1.val
    input csr_count_val_1_val_en,
    input [31:0] csr_count_val_1_val_in,

    // VER.val
    input [7:0] csr_ver_val_in,

    // SUB.val
    input [7:0] csr_sub_val_in,

    // REV.val
    input [7:0] csr_rev_val_in,

    // AXI
    input  [ADDR_W-1:0] axil_awaddr,
    input  [2:0]        axil_awprot,
    input               axil_awvalid,
    output              axil_awready,
    input  [DATA_W-1:0] axil_wdata,
    input  [STRB_W-1:0] axil_wstrb,
    input               axil_wvalid,
    output              axil_wready,
    output [1:0]        axil_bresp,
    output              axil_bvalid,
    input               axil_bready,

    input  [ADDR_W-1:0] axil_araddr,
    input  [2:0]        axil_arprot,
    input               axil_arvalid,
    output              axil_arready,
    output [DATA_W-1:0] axil_rdata,
    output [1:0]        axil_rresp,
    output              axil_rvalid,
    input               axil_rready
);
wire              wready;
wire [ADDR_W-1:0] waddr;
wire [DATA_W-1:0] wdata;
wire              wen;
wire [STRB_W-1:0] wstrb;
wire [DATA_W-1:0] rdata;
wire              rvalid;
wire [ADDR_W-1:0] raddr;
wire              ren;
    reg [ADDR_W-1:0] waddr_int;
    reg [ADDR_W-1:0] raddr_int;
    reg [DATA_W-1:0] wdata_int;
    reg [STRB_W-1:0] strb_int;
    reg              awflag;
    reg              wflag;
    reg              arflag;
    reg              rflag;

    reg              axil_bvalid_int;
    reg [DATA_W-1:0] axil_rdata_int;
    reg              axil_rvalid_int;

    assign axil_awready = ~awflag;
    assign axil_wready  = ~wflag;
    assign axil_bvalid  = axil_bvalid_int;
    assign waddr        = waddr_int;
    assign wdata        = wdata_int;
    assign wstrb        = strb_int;
    assign wen          = awflag && wflag;
    assign axil_bresp   = 'd0; // always okay

    always @(posedge clk) begin
        if (rst == 1'b1) begin
            waddr_int       <= 'd0;
            wdata_int       <= 'd0;
            strb_int        <= 'd0;
            awflag          <= 1'b0;
            wflag           <= 1'b0;
            axil_bvalid_int <= 1'b0;
        end else begin
            if (axil_awvalid == 1'b1 && awflag == 1'b0) begin
                awflag    <= 1'b1;
                waddr_int <= axil_awaddr;
            end else if (wen == 1'b1 && wready == 1'b1) begin
                awflag    <= 1'b0;
            end

            if (axil_wvalid == 1'b1 && wflag == 1'b0) begin
                wflag     <= 1'b1;
                wdata_int <= axil_wdata;
                strb_int  <= axil_wstrb;
            end else if (wen == 1'b1 && wready == 1'b1) begin
                wflag     <= 1'b0;
            end

            if (axil_bvalid_int == 1'b1 && axil_bready == 1'b1) begin
                axil_bvalid_int <= 1'b0;
            end else if ((axil_wvalid == 1'b1 && awflag == 1'b1) || (axil_awvalid == 1'b1 && wflag == 1'b1) || (wflag == 1'b1 && awflag == 1'b1)) begin
                axil_bvalid_int <= wready;
            end
        end
    end

    assign axil_arready = ~arflag;
    assign axil_rdata   = axil_rdata_int;
    assign axil_rvalid  = axil_rvalid_int;
    assign raddr        = raddr_int;
    assign ren          = arflag && ~rflag;
    assign axil_rresp   = 'd0; // always okay

    always @(posedge clk) begin
        if (rst == 1'b1) begin
            raddr_int       <= 'd0;
            arflag          <= 1'b0;
            rflag           <= 1'b0;
            axil_rdata_int  <= 'd0;
            axil_rvalid_int <= 1'b0;
        end else begin
            if (axil_arvalid == 1'b1 && arflag == 1'b0) begin
                arflag    <= 1'b1;
                raddr_int <= axil_araddr;
            end else if (axil_rvalid_int == 1'b1 && axil_rready == 1'b1) begin
                arflag    <= 1'b0;
            end

            if (rvalid == 1'b1 && ren == 1'b1 && rflag == 1'b0) begin
                rflag <= 1'b1;
            end else if (axil_rvalid_int == 1'b1 && axil_rready == 1'b1) begin
                rflag <= 1'b0;
            end

            if (rvalid == 1'b1 && axil_rvalid_int == 1'b0) begin
                axil_rdata_int  <= rdata;
                axil_rvalid_int <= 1'b1;
            end else if (axil_rvalid_int == 1'b1 && axil_rready == 1'b1) begin
                axil_rvalid_int <= 1'b0;
            end
        end
    end

//------------------------------------------------------------------------------
// CSR:
// [0x0] - SAMPL_NUM - Длительность интервала сбора данных. 125е6 (1 сек) по-умолчанию.
//------------------------------------------------------------------------------
wire [31:0] csr_sampl_num_rdata;

wire csr_sampl_num_wen;
assign csr_sampl_num_wen = wen && (waddr == 32'h0);

wire csr_sampl_num_ren;
assign csr_sampl_num_ren = ren && (raddr == 32'h0);
reg csr_sampl_num_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_sampl_num_ren_ff <= 1'b0;
    end else begin
        csr_sampl_num_ren_ff <= csr_sampl_num_ren;
    end
end
//---------------------
// Bit field:
// SAMPL_NUM[31:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [31:0] csr_sampl_num_val_ff;

assign csr_sampl_num_rdata[31:0] = csr_sampl_num_val_ff;

assign csr_sampl_num_val_out = csr_sampl_num_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_sampl_num_val_ff <= 32'h7735940;
    end else  begin
     if (csr_sampl_num_wen) begin
            if (wstrb[0]) begin
                csr_sampl_num_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_sampl_num_val_ff[15:8] <= wdata[15:8];
            end
            if (wstrb[2]) begin
                csr_sampl_num_val_ff[23:16] <= wdata[23:16];
            end
            if (wstrb[3]) begin
                csr_sampl_num_val_ff[31:24] <= wdata[31:24];
            end
        end else begin
            csr_sampl_num_val_ff <= csr_sampl_num_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x4] - AREA0_START - Начальный бин интеграла в спектре, зона 0
//------------------------------------------------------------------------------
wire [31:0] csr_area0_start_rdata;
assign csr_area0_start_rdata[31:16] = 16'h0;

wire csr_area0_start_wen;
assign csr_area0_start_wen = wen && (waddr == 32'h4);

wire csr_area0_start_ren;
assign csr_area0_start_ren = ren && (raddr == 32'h4);
reg csr_area0_start_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_area0_start_ren_ff <= 1'b0;
    end else begin
        csr_area0_start_ren_ff <= csr_area0_start_ren;
    end
end
//---------------------
// Bit field:
// AREA0_START[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_area0_start_val_ff;

assign csr_area0_start_rdata[15:0] = csr_area0_start_val_ff;

assign csr_area0_start_val_out = csr_area0_start_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_area0_start_val_ff <= 16'h0;
    end else  begin
     if (csr_area0_start_wen) begin
            if (wstrb[0]) begin
                csr_area0_start_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_area0_start_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_area0_start_val_ff <= csr_area0_start_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x8] - AREA1_START - Начальный бин интеграла в спектре, зона 1
//------------------------------------------------------------------------------
wire [31:0] csr_area1_start_rdata;
assign csr_area1_start_rdata[31:16] = 16'h0;

wire csr_area1_start_wen;
assign csr_area1_start_wen = wen && (waddr == 32'h8);

wire csr_area1_start_ren;
assign csr_area1_start_ren = ren && (raddr == 32'h8);
reg csr_area1_start_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_area1_start_ren_ff <= 1'b0;
    end else begin
        csr_area1_start_ren_ff <= csr_area1_start_ren;
    end
end
//---------------------
// Bit field:
// AREA1_START[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_area1_start_val_ff;

assign csr_area1_start_rdata[15:0] = csr_area1_start_val_ff;

assign csr_area1_start_val_out = csr_area1_start_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_area1_start_val_ff <= 16'h0;
    end else  begin
     if (csr_area1_start_wen) begin
            if (wstrb[0]) begin
                csr_area1_start_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_area1_start_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_area1_start_val_ff <= csr_area1_start_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0xc] - AREA2_START - Начальный бин интеграла в спектре, зона 2
//------------------------------------------------------------------------------
wire [31:0] csr_area2_start_rdata;
assign csr_area2_start_rdata[31:16] = 16'h0;

wire csr_area2_start_wen;
assign csr_area2_start_wen = wen && (waddr == 32'hc);

wire csr_area2_start_ren;
assign csr_area2_start_ren = ren && (raddr == 32'hc);
reg csr_area2_start_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_area2_start_ren_ff <= 1'b0;
    end else begin
        csr_area2_start_ren_ff <= csr_area2_start_ren;
    end
end
//---------------------
// Bit field:
// AREA2_START[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_area2_start_val_ff;

assign csr_area2_start_rdata[15:0] = csr_area2_start_val_ff;

assign csr_area2_start_val_out = csr_area2_start_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_area2_start_val_ff <= 16'h0;
    end else  begin
     if (csr_area2_start_wen) begin
            if (wstrb[0]) begin
                csr_area2_start_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_area2_start_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_area2_start_val_ff <= csr_area2_start_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x10] - AREA0_END - Последний бин интеграла в спектре, зона 0
//------------------------------------------------------------------------------
wire [31:0] csr_area0_end_rdata;
assign csr_area0_end_rdata[31:16] = 16'h0;

wire csr_area0_end_wen;
assign csr_area0_end_wen = wen && (waddr == 32'h10);

wire csr_area0_end_ren;
assign csr_area0_end_ren = ren && (raddr == 32'h10);
reg csr_area0_end_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_area0_end_ren_ff <= 1'b0;
    end else begin
        csr_area0_end_ren_ff <= csr_area0_end_ren;
    end
end
//---------------------
// Bit field:
// AREA0_END[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_area0_end_val_ff;

assign csr_area0_end_rdata[15:0] = csr_area0_end_val_ff;

assign csr_area0_end_val_out = csr_area0_end_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_area0_end_val_ff <= 16'h3ff;
    end else  begin
     if (csr_area0_end_wen) begin
            if (wstrb[0]) begin
                csr_area0_end_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_area0_end_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_area0_end_val_ff <= csr_area0_end_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x14] - AREA1_END - Последний бин интеграла в спектре, зона 1
//------------------------------------------------------------------------------
wire [31:0] csr_area1_end_rdata;
assign csr_area1_end_rdata[31:16] = 16'h0;

wire csr_area1_end_wen;
assign csr_area1_end_wen = wen && (waddr == 32'h14);

wire csr_area1_end_ren;
assign csr_area1_end_ren = ren && (raddr == 32'h14);
reg csr_area1_end_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_area1_end_ren_ff <= 1'b0;
    end else begin
        csr_area1_end_ren_ff <= csr_area1_end_ren;
    end
end
//---------------------
// Bit field:
// AREA1_END[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_area1_end_val_ff;

assign csr_area1_end_rdata[15:0] = csr_area1_end_val_ff;

assign csr_area1_end_val_out = csr_area1_end_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_area1_end_val_ff <= 16'h0;
    end else  begin
     if (csr_area1_end_wen) begin
            if (wstrb[0]) begin
                csr_area1_end_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_area1_end_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_area1_end_val_ff <= csr_area1_end_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x18] - AREA2_END - Последний бин интеграла в спектре, зона 2
//------------------------------------------------------------------------------
wire [31:0] csr_area2_end_rdata;
assign csr_area2_end_rdata[31:16] = 16'h0;

wire csr_area2_end_wen;
assign csr_area2_end_wen = wen && (waddr == 32'h18);

wire csr_area2_end_ren;
assign csr_area2_end_ren = ren && (raddr == 32'h18);
reg csr_area2_end_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_area2_end_ren_ff <= 1'b0;
    end else begin
        csr_area2_end_ren_ff <= csr_area2_end_ren;
    end
end
//---------------------
// Bit field:
// AREA2_END[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_area2_end_val_ff;

assign csr_area2_end_rdata[15:0] = csr_area2_end_val_ff;

assign csr_area2_end_val_out = csr_area2_end_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_area2_end_val_ff <= 16'h0;
    end else  begin
     if (csr_area2_end_wen) begin
            if (wstrb[0]) begin
                csr_area2_end_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_area2_end_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_area2_end_val_ff <= csr_area2_end_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x1c] - BUF_CTRL - Управление сбором данных устройства
//------------------------------------------------------------------------------
wire [31:0] csr_buf_ctrl_rdata;
assign csr_buf_ctrl_rdata[31:2] = 30'h0;

wire csr_buf_ctrl_wen;
assign csr_buf_ctrl_wen = wen && (waddr == 32'h1c);

//---------------------
// Bit field:
// BUF_CTRL[0] - spec_req - Флаг запроса спектра
// access: wo, hardware: o
//---------------------
reg  csr_buf_ctrl_spec_req_ff;

assign csr_buf_ctrl_rdata[0] = 1'b0;

assign csr_buf_ctrl_spec_req_out = csr_buf_ctrl_spec_req_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_buf_ctrl_spec_req_ff <= 1'b0;
    end else  begin
     if (csr_buf_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_buf_ctrl_spec_req_ff <= wdata[0];
            end
        end else begin
            csr_buf_ctrl_spec_req_ff <= csr_buf_ctrl_spec_req_ff;
        end
    end
end


//---------------------
// Bit field:
// BUF_CTRL[1] - area_req - Флаг запроса трех интегралов в заданных бинах спектра
// access: wo, hardware: o
//---------------------
reg  csr_buf_ctrl_area_req_ff;

assign csr_buf_ctrl_rdata[1] = 1'b0;

assign csr_buf_ctrl_area_req_out = csr_buf_ctrl_area_req_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_buf_ctrl_area_req_ff <= 1'b0;
    end else  begin
     if (csr_buf_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_buf_ctrl_area_req_ff <= wdata[1];
            end
        end else begin
            csr_buf_ctrl_area_req_ff <= csr_buf_ctrl_area_req_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x20] - ACC_START - Определяет момент начала расчета интеграла внутри гейта, сдвиг от начала гейта
//------------------------------------------------------------------------------
wire [31:0] csr_acc_start_rdata;
assign csr_acc_start_rdata[31:8] = 24'h0;

wire csr_acc_start_wen;
assign csr_acc_start_wen = wen && (waddr == 32'h20);

wire csr_acc_start_ren;
assign csr_acc_start_ren = ren && (raddr == 32'h20);
reg csr_acc_start_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_acc_start_ren_ff <= 1'b0;
    end else begin
        csr_acc_start_ren_ff <= csr_acc_start_ren;
    end
end
//---------------------
// Bit field:
// ACC_START[7:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [7:0] csr_acc_start_val_ff;

assign csr_acc_start_rdata[7:0] = csr_acc_start_val_ff;

assign csr_acc_start_val_out = csr_acc_start_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_acc_start_val_ff <= 8'h0;
    end else  begin
     if (csr_acc_start_wen) begin
            if (wstrb[0]) begin
                csr_acc_start_val_ff[7:0] <= wdata[7:0];
            end
        end else begin
            csr_acc_start_val_ff <= csr_acc_start_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x24] - ACC_STOP - Определяет момент окончания расчета интеграла внутри гейта, сдвиг от конца гейта
//------------------------------------------------------------------------------
wire [31:0] csr_acc_stop_rdata;
assign csr_acc_stop_rdata[31:8] = 24'h0;

wire csr_acc_stop_wen;
assign csr_acc_stop_wen = wen && (waddr == 32'h24);

wire csr_acc_stop_ren;
assign csr_acc_stop_ren = ren && (raddr == 32'h24);
reg csr_acc_stop_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_acc_stop_ren_ff <= 1'b0;
    end else begin
        csr_acc_stop_ren_ff <= csr_acc_stop_ren;
    end
end
//---------------------
// Bit field:
// ACC_STOP[7:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [7:0] csr_acc_stop_val_ff;

assign csr_acc_stop_rdata[7:0] = csr_acc_stop_val_ff;

assign csr_acc_stop_val_out = csr_acc_stop_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_acc_stop_val_ff <= 8'h80;
    end else  begin
     if (csr_acc_stop_wen) begin
            if (wstrb[0]) begin
                csr_acc_stop_val_ff[7:0] <= wdata[7:0];
            end
        end else begin
            csr_acc_stop_val_ff <= csr_acc_stop_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x28] - ADC_TH - Уровень входного сигнала, первышение которого считается началом импульса (началом гейта)
//------------------------------------------------------------------------------
wire [31:0] csr_adc_th_rdata;
assign csr_adc_th_rdata[31:16] = 16'h0;

wire csr_adc_th_wen;
assign csr_adc_th_wen = wen && (waddr == 32'h28);

wire csr_adc_th_ren;
assign csr_adc_th_ren = ren && (raddr == 32'h28);
reg csr_adc_th_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_adc_th_ren_ff <= 1'b0;
    end else begin
        csr_adc_th_ren_ff <= csr_adc_th_ren;
    end
end
//---------------------
// Bit field:
// ADC_TH[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_adc_th_val_ff;

assign csr_adc_th_rdata[15:0] = csr_adc_th_val_ff;

assign csr_adc_th_val_out = csr_adc_th_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_adc_th_val_ff <= 16'hfa;
    end else  begin
     if (csr_adc_th_wen) begin
            if (wstrb[0]) begin
                csr_adc_th_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_adc_th_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_adc_th_val_ff <= csr_adc_th_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x2c] - ADC_FILTER - Фильтр скользящего среднего входного импульса
//------------------------------------------------------------------------------
wire [31:0] csr_adc_filter_rdata;
assign csr_adc_filter_rdata[6:3] = 4'h0;
assign csr_adc_filter_rdata[31:8] = 24'h0;

wire csr_adc_filter_wen;
assign csr_adc_filter_wen = wen && (waddr == 32'h2c);

wire csr_adc_filter_ren;
assign csr_adc_filter_ren = ren && (raddr == 32'h2c);
reg csr_adc_filter_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_adc_filter_ren_ff <= 1'b0;
    end else begin
        csr_adc_filter_ren_ff <= csr_adc_filter_ren;
    end
end
//---------------------
// Bit field:
// ADC_FILTER[2:0] - window_size - Размер окна фильтра по степени двойки (2^window_size)
// access: rw, hardware: o
//---------------------
reg [2:0] csr_adc_filter_window_size_ff;

assign csr_adc_filter_rdata[2:0] = csr_adc_filter_window_size_ff;

assign csr_adc_filter_window_size_out = csr_adc_filter_window_size_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_adc_filter_window_size_ff <= 3'h2;
    end else  begin
     if (csr_adc_filter_wen) begin
            if (wstrb[0]) begin
                csr_adc_filter_window_size_ff[2:0] <= wdata[2:0];
            end
        end else begin
            csr_adc_filter_window_size_ff <= csr_adc_filter_window_size_ff;
        end
    end
end


//---------------------
// Bit field:
// ADC_FILTER[7] - bypass - Bypass
// access: rw, hardware: o
//---------------------
reg  csr_adc_filter_bypass_ff;

assign csr_adc_filter_rdata[7] = csr_adc_filter_bypass_ff;

assign csr_adc_filter_bypass_out = csr_adc_filter_bypass_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_adc_filter_bypass_ff <= 1'b1;
    end else  begin
     if (csr_adc_filter_wen) begin
            if (wstrb[0]) begin
                csr_adc_filter_bypass_ff <= wdata[7];
            end
        end else begin
            csr_adc_filter_bypass_ff <= csr_adc_filter_bypass_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x30] - BLINE_CTRL - Управление модулем расчета baseline
//------------------------------------------------------------------------------
wire [31:0] csr_bline_ctrl_rdata;
assign csr_bline_ctrl_rdata[6:4] = 3'h0;
assign csr_bline_ctrl_rdata[31:8] = 24'h0;

wire csr_bline_ctrl_wen;
assign csr_bline_ctrl_wen = wen && (waddr == 32'h30);

wire csr_bline_ctrl_ren;
assign csr_bline_ctrl_ren = ren && (raddr == 32'h30);
reg csr_bline_ctrl_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_bline_ctrl_ren_ff <= 1'b0;
    end else begin
        csr_bline_ctrl_ren_ff <= csr_bline_ctrl_ren;
    end
end
//---------------------
// Bit field:
// BLINE_CTRL[3:0] - averagings - Количество усреднений при расчете baseline, по степени двойки (2^averagings)
// access: rw, hardware: o
//---------------------
reg [3:0] csr_bline_ctrl_averagings_ff;

assign csr_bline_ctrl_rdata[3:0] = csr_bline_ctrl_averagings_ff;

assign csr_bline_ctrl_averagings_out = csr_bline_ctrl_averagings_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_bline_ctrl_averagings_ff <= 4'h6;
    end else  begin
     if (csr_bline_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_bline_ctrl_averagings_ff[3:0] <= wdata[3:0];
            end
        end else begin
            csr_bline_ctrl_averagings_ff <= csr_bline_ctrl_averagings_ff;
        end
    end
end


//---------------------
// Bit field:
// BLINE_CTRL[7] - auto_baseline - Включить автоматический расчет
// access: rw, hardware: o
//---------------------
reg  csr_bline_ctrl_auto_baseline_ff;

assign csr_bline_ctrl_rdata[7] = csr_bline_ctrl_auto_baseline_ff;

assign csr_bline_ctrl_auto_baseline_out = csr_bline_ctrl_auto_baseline_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_bline_ctrl_auto_baseline_ff <= 1'b0;
    end else  begin
     if (csr_bline_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_bline_ctrl_auto_baseline_ff <= wdata[7];
            end
        end else begin
            csr_bline_ctrl_auto_baseline_ff <= csr_bline_ctrl_auto_baseline_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x34] - BLINE_MANUAL - Регистр установки baseline. Знаковое число, которое вычитается из входного сигнала. Применяется только при (auto_baseline == 0)
//------------------------------------------------------------------------------
wire [31:0] csr_bline_manual_rdata;
assign csr_bline_manual_rdata[31:16] = 16'h0;

wire csr_bline_manual_wen;
assign csr_bline_manual_wen = wen && (waddr == 32'h34);

wire csr_bline_manual_ren;
assign csr_bline_manual_ren = ren && (raddr == 32'h34);
reg csr_bline_manual_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_bline_manual_ren_ff <= 1'b0;
    end else begin
        csr_bline_manual_ren_ff <= csr_bline_manual_ren;
    end
end
//---------------------
// Bit field:
// BLINE_MANUAL[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_bline_manual_val_ff;

assign csr_bline_manual_rdata[15:0] = csr_bline_manual_val_ff;

assign csr_bline_manual_val_out = csr_bline_manual_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_bline_manual_val_ff <= 16'h0;
    end else  begin
     if (csr_bline_manual_wen) begin
            if (wstrb[0]) begin
                csr_bline_manual_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_bline_manual_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_bline_manual_val_ff <= csr_bline_manual_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x38] - BLINE_ACC - Acceptance level baseline. Размах сигнала между BLINE_TREND_DELAY точками, который считается стабильный и используется для расчета.
//------------------------------------------------------------------------------
wire [31:0] csr_bline_acc_rdata;
assign csr_bline_acc_rdata[31:16] = 16'h0;

wire csr_bline_acc_wen;
assign csr_bline_acc_wen = wen && (waddr == 32'h38);

wire csr_bline_acc_ren;
assign csr_bline_acc_ren = ren && (raddr == 32'h38);
reg csr_bline_acc_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_bline_acc_ren_ff <= 1'b0;
    end else begin
        csr_bline_acc_ren_ff <= csr_bline_acc_ren;
    end
end
//---------------------
// Bit field:
// BLINE_ACC[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_bline_acc_val_ff;

assign csr_bline_acc_rdata[15:0] = csr_bline_acc_val_ff;

assign csr_bline_acc_val_out = csr_bline_acc_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_bline_acc_val_ff <= 16'h14;
    end else  begin
     if (csr_bline_acc_wen) begin
            if (wstrb[0]) begin
                csr_bline_acc_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_bline_acc_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_bline_acc_val_ff <= csr_bline_acc_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x3c] - BLINE_TREND_DELAY - Trend delay baseline. Расстояние между двумя отсчетами сигнала, разница которых измеряется BLINE_ACC.
//------------------------------------------------------------------------------
wire [31:0] csr_bline_trend_delay_rdata;
assign csr_bline_trend_delay_rdata[31:6] = 26'h0;

wire csr_bline_trend_delay_wen;
assign csr_bline_trend_delay_wen = wen && (waddr == 32'h3c);

wire csr_bline_trend_delay_ren;
assign csr_bline_trend_delay_ren = ren && (raddr == 32'h3c);
reg csr_bline_trend_delay_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_bline_trend_delay_ren_ff <= 1'b0;
    end else begin
        csr_bline_trend_delay_ren_ff <= csr_bline_trend_delay_ren;
    end
end
//---------------------
// Bit field:
// BLINE_TREND_DELAY[5:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [5:0] csr_bline_trend_delay_val_ff;

assign csr_bline_trend_delay_rdata[5:0] = csr_bline_trend_delay_val_ff;

assign csr_bline_trend_delay_val_out = csr_bline_trend_delay_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_bline_trend_delay_val_ff <= 6'hf;
    end else  begin
     if (csr_bline_trend_delay_wen) begin
            if (wstrb[0]) begin
                csr_bline_trend_delay_val_ff[5:0] <= wdata[5:0];
            end
        end else begin
            csr_bline_trend_delay_val_ff <= csr_bline_trend_delay_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x40] - BLINE_ACTUAL - Текущее значение baseline. Обновляется независимо от любых других сигналов.
//------------------------------------------------------------------------------
wire [31:0] csr_bline_actual_rdata;
assign csr_bline_actual_rdata[31:15] = 17'h0;


wire csr_bline_actual_ren;
assign csr_bline_actual_ren = ren && (raddr == 32'h40);
reg csr_bline_actual_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_bline_actual_ren_ff <= 1'b0;
    end else begin
        csr_bline_actual_ren_ff <= csr_bline_actual_ren;
    end
end
//---------------------
// Bit field:
// BLINE_ACTUAL[14:0] - val - Value of the register
// access: ro, hardware: ie
//---------------------
reg [14:0] csr_bline_actual_val_ff;

assign csr_bline_actual_rdata[14:0] = csr_bline_actual_val_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_bline_actual_val_ff <= 15'h0;
    end else  begin
      if (csr_bline_actual_val_en) begin
            csr_bline_actual_val_ff <= csr_bline_actual_val_in;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x44] - GATE_CTRL - Управление гейтом
//------------------------------------------------------------------------------
wire [31:0] csr_gate_ctrl_rdata;
assign csr_gate_ctrl_rdata[31:8] = 24'h0;

wire csr_gate_ctrl_wen;
assign csr_gate_ctrl_wen = wen && (waddr == 32'h44);

wire csr_gate_ctrl_ren;
assign csr_gate_ctrl_ren = ren && (raddr == 32'h44);
reg csr_gate_ctrl_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_gate_ctrl_ren_ff <= 1'b0;
    end else begin
        csr_gate_ctrl_ren_ff <= csr_gate_ctrl_ren;
    end
end
//---------------------
// Bit field:
// GATE_CTRL[0] - hysteresis_en - Включить hysteresis снятия гейта на уровне threshold/2
// access: rw, hardware: o
//---------------------
reg  csr_gate_ctrl_hysteresis_en_ff;

assign csr_gate_ctrl_rdata[0] = csr_gate_ctrl_hysteresis_en_ff;

assign csr_gate_ctrl_hysteresis_en_out = csr_gate_ctrl_hysteresis_en_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_gate_ctrl_hysteresis_en_ff <= 1'b0;
    end else  begin
     if (csr_gate_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_gate_ctrl_hysteresis_en_ff <= wdata[0];
            end
        end else begin
            csr_gate_ctrl_hysteresis_en_ff <= csr_gate_ctrl_hysteresis_en_ff;
        end
    end
end


//---------------------
// Bit field:
// GATE_CTRL[1] - pileup_reject - Отбрасывать gates, где есть pileup
// access: rw, hardware: o
//---------------------
reg  csr_gate_ctrl_pileup_reject_ff;

assign csr_gate_ctrl_rdata[1] = csr_gate_ctrl_pileup_reject_ff;

assign csr_gate_ctrl_pileup_reject_out = csr_gate_ctrl_pileup_reject_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_gate_ctrl_pileup_reject_ff <= 1'b0;
    end else  begin
     if (csr_gate_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_gate_ctrl_pileup_reject_ff <= wdata[1];
            end
        end else begin
            csr_gate_ctrl_pileup_reject_ff <= csr_gate_ctrl_pileup_reject_ff;
        end
    end
end


//---------------------
// Bit field:
// GATE_CTRL[7:2] - pre_trigger - Включение в гейт отсчетов до пересечение сигналом уровня threshold
// access: rw, hardware: o
//---------------------
reg [5:0] csr_gate_ctrl_pre_trigger_ff;

assign csr_gate_ctrl_rdata[7:2] = csr_gate_ctrl_pre_trigger_ff;

assign csr_gate_ctrl_pre_trigger_out = csr_gate_ctrl_pre_trigger_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_gate_ctrl_pre_trigger_ff <= 6'h0;
    end else  begin
     if (csr_gate_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_gate_ctrl_pre_trigger_ff[5:0] <= wdata[7:2];
            end
        end else begin
            csr_gate_ctrl_pre_trigger_ff <= csr_gate_ctrl_pre_trigger_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x48] - DUMP_CTRL - Управление режимом осциллографа
//------------------------------------------------------------------------------
wire [31:0] csr_dump_ctrl_rdata;
assign csr_dump_ctrl_rdata[31:12] = 20'h0;

wire csr_dump_ctrl_wen;
assign csr_dump_ctrl_wen = wen && (waddr == 32'h48);

wire csr_dump_ctrl_ren;
assign csr_dump_ctrl_ren = ren && (raddr == 32'h48);
reg csr_dump_ctrl_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_dump_ctrl_ren_ff <= 1'b0;
    end else begin
        csr_dump_ctrl_ren_ff <= csr_dump_ctrl_ren;
    end
end
//---------------------
// Bit field:
// DUMP_CTRL[0] - enable - Захватить следующий валидный гейт
// access: wosc, hardware: o
//---------------------
reg  csr_dump_ctrl_enable_ff;

assign csr_dump_ctrl_rdata[0] = 1'b0;

assign csr_dump_ctrl_enable_out = csr_dump_ctrl_enable_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_dump_ctrl_enable_ff <= 1'b0;
    end else  begin
     if (csr_dump_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_dump_ctrl_enable_ff <= wdata[0];
            end
        end else begin
            csr_dump_ctrl_enable_ff <= 1'b0;
        end
    end
end


//---------------------
// Bit field:
// DUMP_CTRL[11:1] - samples - Количество семплов для набора и передачи
// access: rw, hardware: o
//---------------------
reg [10:0] csr_dump_ctrl_samples_ff;

assign csr_dump_ctrl_rdata[11:1] = csr_dump_ctrl_samples_ff;

assign csr_dump_ctrl_samples_out = csr_dump_ctrl_samples_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_dump_ctrl_samples_ff <= 11'h0;
    end else  begin
     if (csr_dump_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_dump_ctrl_samples_ff[6:0] <= wdata[7:1];
            end
            if (wstrb[1]) begin
                csr_dump_ctrl_samples_ff[10:7] <= wdata[11:8];
            end
        end else begin
            csr_dump_ctrl_samples_ff <= csr_dump_ctrl_samples_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x4c] - PILEUP_ACC - Acceptance level pileup. Размах сигнала между PILEUP_TREND_DELAY точками, который считается pile-up.
//------------------------------------------------------------------------------
wire [31:0] csr_pileup_acc_rdata;
assign csr_pileup_acc_rdata[31:16] = 16'h0;

wire csr_pileup_acc_wen;
assign csr_pileup_acc_wen = wen && (waddr == 32'h4c);

wire csr_pileup_acc_ren;
assign csr_pileup_acc_ren = ren && (raddr == 32'h4c);
reg csr_pileup_acc_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_pileup_acc_ren_ff <= 1'b0;
    end else begin
        csr_pileup_acc_ren_ff <= csr_pileup_acc_ren;
    end
end
//---------------------
// Bit field:
// PILEUP_ACC[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_pileup_acc_val_ff;

assign csr_pileup_acc_rdata[15:0] = csr_pileup_acc_val_ff;

assign csr_pileup_acc_val_out = csr_pileup_acc_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_pileup_acc_val_ff <= 16'h14;
    end else  begin
     if (csr_pileup_acc_wen) begin
            if (wstrb[0]) begin
                csr_pileup_acc_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_pileup_acc_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_pileup_acc_val_ff <= csr_pileup_acc_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x50] - PILEUP_TREND_DELAY - Trend delay pileup. Расстояние между двумя отсчетами сигнала, разница которых измеряется PILEUP_ACC.
//------------------------------------------------------------------------------
wire [31:0] csr_pileup_trend_delay_rdata;
assign csr_pileup_trend_delay_rdata[31:6] = 26'h0;

wire csr_pileup_trend_delay_wen;
assign csr_pileup_trend_delay_wen = wen && (waddr == 32'h50);

wire csr_pileup_trend_delay_ren;
assign csr_pileup_trend_delay_ren = ren && (raddr == 32'h50);
reg csr_pileup_trend_delay_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_pileup_trend_delay_ren_ff <= 1'b0;
    end else begin
        csr_pileup_trend_delay_ren_ff <= csr_pileup_trend_delay_ren;
    end
end
//---------------------
// Bit field:
// PILEUP_TREND_DELAY[5:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [5:0] csr_pileup_trend_delay_val_ff;

assign csr_pileup_trend_delay_rdata[5:0] = csr_pileup_trend_delay_val_ff;

assign csr_pileup_trend_delay_val_out = csr_pileup_trend_delay_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_pileup_trend_delay_val_ff <= 6'h0;
    end else  begin
     if (csr_pileup_trend_delay_wen) begin
            if (wstrb[0]) begin
                csr_pileup_trend_delay_val_ff[5:0] <= wdata[5:0];
            end
        end else begin
            csr_pileup_trend_delay_val_ff <= csr_pileup_trend_delay_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x54] - PILEUP_ACTUAL - Флаг наличия pile-up в последнем запрошенном DUMP_CTRL кадре
//------------------------------------------------------------------------------
wire [31:0] csr_pileup_actual_rdata;
assign csr_pileup_actual_rdata[31:1] = 31'h0;


wire csr_pileup_actual_ren;
assign csr_pileup_actual_ren = ren && (raddr == 32'h54);
reg csr_pileup_actual_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_pileup_actual_ren_ff <= 1'b0;
    end else begin
        csr_pileup_actual_ren_ff <= csr_pileup_actual_ren;
    end
end
//---------------------
// Bit field:
// PILEUP_ACTUAL[0] - val - Value of the register
// access: ro, hardware: ie
//---------------------
reg  csr_pileup_actual_val_ff;

assign csr_pileup_actual_rdata[0] = csr_pileup_actual_val_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_pileup_actual_val_ff <= 1'b0;
    end else  begin
      if (csr_pileup_actual_val_en) begin
            csr_pileup_actual_val_ff <= csr_pileup_actual_val_in;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x58] - PILEUP_CNT_CTRL - Управление счетчиком pile-up
//------------------------------------------------------------------------------
wire [31:0] csr_pileup_cnt_ctrl_rdata;
assign csr_pileup_cnt_ctrl_rdata[31:2] = 30'h0;

wire csr_pileup_cnt_ctrl_wen;
assign csr_pileup_cnt_ctrl_wen = wen && (waddr == 32'h58);

wire csr_pileup_cnt_ctrl_ren;
assign csr_pileup_cnt_ctrl_ren = ren && (raddr == 32'h58);
reg csr_pileup_cnt_ctrl_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_pileup_cnt_ctrl_ren_ff <= 1'b0;
    end else begin
        csr_pileup_cnt_ctrl_ren_ff <= csr_pileup_cnt_ctrl_ren;
    end
end
//---------------------
// Bit field:
// PILEUP_CNT_CTRL[0] - frame_rst - Сбрасывать счетчик каждый кадр
// access: rw, hardware: o
//---------------------
reg  csr_pileup_cnt_ctrl_frame_rst_ff;

assign csr_pileup_cnt_ctrl_rdata[0] = csr_pileup_cnt_ctrl_frame_rst_ff;

assign csr_pileup_cnt_ctrl_frame_rst_out = csr_pileup_cnt_ctrl_frame_rst_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_pileup_cnt_ctrl_frame_rst_ff <= 1'b0;
    end else  begin
     if (csr_pileup_cnt_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_pileup_cnt_ctrl_frame_rst_ff <= wdata[0];
            end
        end else begin
            csr_pileup_cnt_ctrl_frame_rst_ff <= csr_pileup_cnt_ctrl_frame_rst_ff;
        end
    end
end


//---------------------
// Bit field:
// PILEUP_CNT_CTRL[1] - pileup_cnt_rst - Сброс счетчика
// access: wosc, hardware: o
//---------------------
reg  csr_pileup_cnt_ctrl_pileup_cnt_rst_ff;

assign csr_pileup_cnt_ctrl_rdata[1] = 1'b0;

assign csr_pileup_cnt_ctrl_pileup_cnt_rst_out = csr_pileup_cnt_ctrl_pileup_cnt_rst_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_pileup_cnt_ctrl_pileup_cnt_rst_ff <= 1'b0;
    end else  begin
     if (csr_pileup_cnt_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_pileup_cnt_ctrl_pileup_cnt_rst_ff <= wdata[1];
            end
        end else begin
            csr_pileup_cnt_ctrl_pileup_cnt_rst_ff <= 1'b0;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x5c] - PILEUP_CNT - Счетчик pile-up
//------------------------------------------------------------------------------
wire [31:0] csr_pileup_cnt_rdata;


wire csr_pileup_cnt_ren;
assign csr_pileup_cnt_ren = ren && (raddr == 32'h5c);
reg csr_pileup_cnt_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_pileup_cnt_ren_ff <= 1'b0;
    end else begin
        csr_pileup_cnt_ren_ff <= csr_pileup_cnt_ren;
    end
end
//---------------------
// Bit field:
// PILEUP_CNT[31:0] - val - Value of the register
// access: ro, hardware: i
//---------------------
reg [31:0] csr_pileup_cnt_val_ff;

assign csr_pileup_cnt_rdata[31:0] = csr_pileup_cnt_val_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_pileup_cnt_val_ff <= 32'h0;
    end else  begin
              begin            csr_pileup_cnt_val_ff <= csr_pileup_cnt_val_in;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x60] - COUNT_TH_0 - Threshold счетчика импульсов 0
//------------------------------------------------------------------------------
wire [31:0] csr_count_th_0_rdata;
assign csr_count_th_0_rdata[31:16] = 16'h0;

wire csr_count_th_0_wen;
assign csr_count_th_0_wen = wen && (waddr == 32'h60);

wire csr_count_th_0_ren;
assign csr_count_th_0_ren = ren && (raddr == 32'h60);
reg csr_count_th_0_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_count_th_0_ren_ff <= 1'b0;
    end else begin
        csr_count_th_0_ren_ff <= csr_count_th_0_ren;
    end
end
//---------------------
// Bit field:
// COUNT_TH_0[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_count_th_0_val_ff;

assign csr_count_th_0_rdata[15:0] = csr_count_th_0_val_ff;

assign csr_count_th_0_val_out = csr_count_th_0_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_count_th_0_val_ff <= 16'hfa;
    end else  begin
     if (csr_count_th_0_wen) begin
            if (wstrb[0]) begin
                csr_count_th_0_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_count_th_0_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_count_th_0_val_ff <= csr_count_th_0_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x64] - COUNT_VAL_0 - Значение счетчика 0
//------------------------------------------------------------------------------
wire [31:0] csr_count_val_0_rdata;


wire csr_count_val_0_ren;
assign csr_count_val_0_ren = ren && (raddr == 32'h64);
reg csr_count_val_0_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_count_val_0_ren_ff <= 1'b0;
    end else begin
        csr_count_val_0_ren_ff <= csr_count_val_0_ren;
    end
end
//---------------------
// Bit field:
// COUNT_VAL_0[31:0] - val - Value of the register
// access: ro, hardware: ie
//---------------------
reg [31:0] csr_count_val_0_val_ff;

assign csr_count_val_0_rdata[31:0] = csr_count_val_0_val_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_count_val_0_val_ff <= 32'h0;
    end else  begin
      if (csr_count_val_0_val_en) begin
            csr_count_val_0_val_ff <= csr_count_val_0_val_in;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x68] - COUNT_TH_1 - Threshold счетчика импульсов 1
//------------------------------------------------------------------------------
wire [31:0] csr_count_th_1_rdata;
assign csr_count_th_1_rdata[31:16] = 16'h0;

wire csr_count_th_1_wen;
assign csr_count_th_1_wen = wen && (waddr == 32'h68);

wire csr_count_th_1_ren;
assign csr_count_th_1_ren = ren && (raddr == 32'h68);
reg csr_count_th_1_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_count_th_1_ren_ff <= 1'b0;
    end else begin
        csr_count_th_1_ren_ff <= csr_count_th_1_ren;
    end
end
//---------------------
// Bit field:
// COUNT_TH_1[15:0] - val - Value of the register
// access: rw, hardware: o
//---------------------
reg [15:0] csr_count_th_1_val_ff;

assign csr_count_th_1_rdata[15:0] = csr_count_th_1_val_ff;

assign csr_count_th_1_val_out = csr_count_th_1_val_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_count_th_1_val_ff <= 16'h1f4;
    end else  begin
     if (csr_count_th_1_wen) begin
            if (wstrb[0]) begin
                csr_count_th_1_val_ff[7:0] <= wdata[7:0];
            end
            if (wstrb[1]) begin
                csr_count_th_1_val_ff[15:8] <= wdata[15:8];
            end
        end else begin
            csr_count_th_1_val_ff <= csr_count_th_1_val_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x6c] - COUNT_VAL_1 - Значение счетчика 1
//------------------------------------------------------------------------------
wire [31:0] csr_count_val_1_rdata;


wire csr_count_val_1_ren;
assign csr_count_val_1_ren = ren && (raddr == 32'h6c);
reg csr_count_val_1_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_count_val_1_ren_ff <= 1'b0;
    end else begin
        csr_count_val_1_ren_ff <= csr_count_val_1_ren;
    end
end
//---------------------
// Bit field:
// COUNT_VAL_1[31:0] - val - Value of the register
// access: ro, hardware: ie
//---------------------
reg [31:0] csr_count_val_1_val_ff;

assign csr_count_val_1_rdata[31:0] = csr_count_val_1_val_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_count_val_1_val_ff <= 32'h0;
    end else  begin
      if (csr_count_val_1_val_en) begin
            csr_count_val_1_val_ff <= csr_count_val_1_val_in;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x400] - VER - Ревизия прошивки ПЛИС
//------------------------------------------------------------------------------
wire [31:0] csr_ver_rdata;
assign csr_ver_rdata[31:8] = 24'h0;


wire csr_ver_ren;
assign csr_ver_ren = ren && (raddr == 32'h400);
reg csr_ver_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_ver_ren_ff <= 1'b0;
    end else begin
        csr_ver_ren_ff <= csr_ver_ren;
    end
end
//---------------------
// Bit field:
// VER[7:0] - val - Value of the register
// access: ro, hardware: i
//---------------------
reg [7:0] csr_ver_val_ff;

assign csr_ver_rdata[7:0] = csr_ver_val_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_ver_val_ff <= 8'h0;
    end else  begin
              begin            csr_ver_val_ff <= csr_ver_val_in;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x404] - SUB - Подверсия прошивки ПЛИС
//------------------------------------------------------------------------------
wire [31:0] csr_sub_rdata;
assign csr_sub_rdata[31:8] = 24'h0;


wire csr_sub_ren;
assign csr_sub_ren = ren && (raddr == 32'h404);
reg csr_sub_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_sub_ren_ff <= 1'b0;
    end else begin
        csr_sub_ren_ff <= csr_sub_ren;
    end
end
//---------------------
// Bit field:
// SUB[7:0] - val - Value of the register
// access: ro, hardware: i
//---------------------
reg [7:0] csr_sub_val_ff;

assign csr_sub_rdata[7:0] = csr_sub_val_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_sub_val_ff <= 8'h0;
    end else  begin
              begin            csr_sub_val_ff <= csr_sub_val_in;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x408] - REV - Ревизия прошивки ПЛИС
//------------------------------------------------------------------------------
wire [31:0] csr_rev_rdata;
assign csr_rev_rdata[31:8] = 24'h0;


wire csr_rev_ren;
assign csr_rev_ren = ren && (raddr == 32'h408);
reg csr_rev_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_rev_ren_ff <= 1'b0;
    end else begin
        csr_rev_ren_ff <= csr_rev_ren;
    end
end
//---------------------
// Bit field:
// REV[7:0] - val - Value of the register
// access: ro, hardware: i
//---------------------
reg [7:0] csr_rev_val_ff;

assign csr_rev_rdata[7:0] = csr_rev_val_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_rev_val_ff <= 8'h0;
    end else  begin
              begin            csr_rev_val_ff <= csr_rev_val_in;
        end
    end
end


//------------------------------------------------------------------------------
// Write ready
//------------------------------------------------------------------------------
assign wready = 1'b1;

//------------------------------------------------------------------------------
// Read address decoder
//------------------------------------------------------------------------------
reg [31:0] rdata_ff;
always @(posedge clk) begin
    if (rst) begin
        rdata_ff <= 32'h0;
    end else if (ren) begin
        case (raddr)
            32'h0: rdata_ff <= csr_sampl_num_rdata;
            32'h4: rdata_ff <= csr_area0_start_rdata;
            32'h8: rdata_ff <= csr_area1_start_rdata;
            32'hc: rdata_ff <= csr_area2_start_rdata;
            32'h10: rdata_ff <= csr_area0_end_rdata;
            32'h14: rdata_ff <= csr_area1_end_rdata;
            32'h18: rdata_ff <= csr_area2_end_rdata;
            32'h1c: rdata_ff <= csr_buf_ctrl_rdata;
            32'h20: rdata_ff <= csr_acc_start_rdata;
            32'h24: rdata_ff <= csr_acc_stop_rdata;
            32'h28: rdata_ff <= csr_adc_th_rdata;
            32'h2c: rdata_ff <= csr_adc_filter_rdata;
            32'h30: rdata_ff <= csr_bline_ctrl_rdata;
            32'h34: rdata_ff <= csr_bline_manual_rdata;
            32'h38: rdata_ff <= csr_bline_acc_rdata;
            32'h3c: rdata_ff <= csr_bline_trend_delay_rdata;
            32'h40: rdata_ff <= csr_bline_actual_rdata;
            32'h44: rdata_ff <= csr_gate_ctrl_rdata;
            32'h48: rdata_ff <= csr_dump_ctrl_rdata;
            32'h4c: rdata_ff <= csr_pileup_acc_rdata;
            32'h50: rdata_ff <= csr_pileup_trend_delay_rdata;
            32'h54: rdata_ff <= csr_pileup_actual_rdata;
            32'h58: rdata_ff <= csr_pileup_cnt_ctrl_rdata;
            32'h5c: rdata_ff <= csr_pileup_cnt_rdata;
            32'h60: rdata_ff <= csr_count_th_0_rdata;
            32'h64: rdata_ff <= csr_count_val_0_rdata;
            32'h68: rdata_ff <= csr_count_th_1_rdata;
            32'h6c: rdata_ff <= csr_count_val_1_rdata;
            32'h400: rdata_ff <= csr_ver_rdata;
            32'h404: rdata_ff <= csr_sub_rdata;
            32'h408: rdata_ff <= csr_rev_rdata;
            default: rdata_ff <= 32'h0;
        endcase
    end else begin
        rdata_ff <= 32'h0;
    end
end
assign rdata = rdata_ff;

//------------------------------------------------------------------------------
// Read data valid
//------------------------------------------------------------------------------
reg rvalid_ff;
always @(posedge clk) begin
    if (rst) begin
        rvalid_ff <= 1'b0;
    end else if (ren && rvalid) begin
        rvalid_ff <= 1'b0;
    end else if (ren) begin
        rvalid_ff <= 1'b1;
    end
end

assign rvalid = rvalid_ff;

endmodule