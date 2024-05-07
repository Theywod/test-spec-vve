# Usage:
# do sim.do sim;         - libraries recompilation
# do sim.do; run X us;   - restart & run on X time

#.main clear
quietly set flag_restart 1

quietly set RTL_DIR "../rtl"
quietly set TB_DIR "."

# Argument parsing
if { $argc < 1 } {
  puts "Restarting..."
} elseif { $1 == "sim" } {
  puts "Recompiling..."
  set flag_restart 0
}

vlib work

# Update local files
vlog -work work -sv $RTL_DIR/regmap.sv
vlog -work work -sv $TB_DIR/axi_lite_if.sv
vlog -work work -sv $TB_DIR/regmap_tb.sv

# If recompiling - recreate all libraries. Else - just restart
if { $flag_restart == 1 } {
  restart -all -force
} elseif { $flag_restart == 0} {
  vsim +initreg+0 +initmem+0 -voptargs=+acc -L work work.regmap_tb -t 1ns
}

