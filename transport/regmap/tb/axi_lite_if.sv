parameter ADDR_W = 32;
parameter DATA_W = 32;
parameter STRB_W = DATA_W / 8;

interface axi_lite;
  logic [2:0]        axil_awprot;
  logic              axil_awready;
  logic [STRB_W-1:0] axil_wstrb;
  logic              axil_wready;
  logic [1:0]        axil_bresp;
  logic              axil_bvalid;
  logic [ADDR_W-1:0] axil_awaddr;
  logic              axil_awvalid;
  logic [DATA_W-1:0] axil_wdata;
  logic              axil_wvalid;
  logic              axil_bready;

  logic [2:0]        axil_arprot;
  logic              axil_arready;
  logic [DATA_W-1:0] axil_rdata;
  logic [1:0]        axil_rresp;
  logic              axil_rvalid;
  logic [ADDR_W-1:0] axil_araddr;
  logic              axil_arvalid;
  logic              axil_rready;

 task automatic check_write_register;
    ref                clk;
    input [ADDR_W-1:0] waddr;
    input [DATA_W-1:0] wdata;
    ref   [DATA_W-1:0] reg_val;
    begin
      wait(axil_awready == 1'b1);
      wait(axil_wready == 1'b1);

      axil_awprot = 3'b010;
      axil_wstrb = 4'b1111;
      axil_awaddr = waddr;
      axil_wdata = wdata;

      @(posedge clk);
      axil_awvalid = 1'b1;
      axil_wvalid = 1'b1;
      @(posedge clk);
      axil_awvalid = 1'b0;
      axil_wvalid = 1'b0;

      wait(axil_bvalid == 1'b1);
      assert(axil_bresp == 2'b00) else begin
        $warning("response code is not OKAY");
      end
      @(posedge clk);
      axil_bready = 1'b1;
      @(posedge clk);
      axil_bready = 1'b0;

      assert(reg_val == wdata) else begin
        $error("register write failed for address %h", waddr);
      end
    end
  endtask : check_write_register

  task automatic check_read_register;
    ref                clk;
    input [ADDR_W-1:0] raddr;
    input [DATA_W-1:0] reg_val;
    begin
      wait(axil_arready == 1'b1);

      axil_arprot = 3'b010;
      axil_araddr = raddr;
      @(posedge clk);
      axil_arvalid = 1'b1;
      @(posedge clk);
      axil_arvalid = 1'b0;

      wait(axil_rvalid == 1'b1);
      assert(axil_rresp == 2'b00) else begin
        $warning("response code is not OKAY");
      end
      @(posedge clk);
      axil_rready = 1'b1;
      @(posedge clk);
      axil_rready = 1'b0;

      assert(reg_val == axil_rdata) else begin
        $error("register read failed for address %h", raddr);
      end
    end
  endtask : check_read_register

endinterface : axi_lite
