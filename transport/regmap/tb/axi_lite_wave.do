onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /regmap_tb/clk
add wave -noupdate /regmap_tb/rst
add wave -noupdate /regmap_tb/axi_lite_intf/axil_awprot
add wave -noupdate /regmap_tb/axi_lite_intf/axil_awready
add wave -noupdate /regmap_tb/axi_lite_intf/axil_wstrb
add wave -noupdate /regmap_tb/axi_lite_intf/axil_wready
add wave -noupdate /regmap_tb/axi_lite_intf/axil_bresp
add wave -noupdate /regmap_tb/axi_lite_intf/axil_bvalid
add wave -noupdate /regmap_tb/axi_lite_intf/axil_awaddr
add wave -noupdate /regmap_tb/axi_lite_intf/axil_awvalid
add wave -noupdate /regmap_tb/axi_lite_intf/axil_wdata
add wave -noupdate /regmap_tb/axi_lite_intf/axil_wvalid
add wave -noupdate /regmap_tb/axi_lite_intf/axil_bready
add wave -noupdate /regmap_tb/axi_lite_intf/axil_arprot
add wave -noupdate /regmap_tb/axi_lite_intf/axil_arready
add wave -noupdate /regmap_tb/axi_lite_intf/axil_rdata
add wave -noupdate /regmap_tb/axi_lite_intf/axil_rresp
add wave -noupdate /regmap_tb/axi_lite_intf/axil_rvalid
add wave -noupdate /regmap_tb/axi_lite_intf/axil_araddr
add wave -noupdate /regmap_tb/axi_lite_intf/axil_arvalid
add wave -noupdate /regmap_tb/axi_lite_intf/axil_rready
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {0 ns} 0}
quietly wave cursor active 0
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ns} {1 us}
