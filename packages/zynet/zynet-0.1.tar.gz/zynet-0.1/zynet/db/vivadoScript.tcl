create_project -in_memory -part [lindex $argv 0]
set_param synth.vivado.isSynthRun true
set_property default_lib xil_defaultlib [current_project]
set_property target_language Verilog [current_project]

read_mem [glob ./src/fpga/rtl/*.mif ]
read_verilog -library xil_defaultlib [glob ./src/fpga/rtl/*.v]
set_property top zyNet [current_fileset]

#read_xdc ./src/fpga/constraints/constraints.xdc
#set_property used_in_implementation true [get_files ./src/fpga/constraints/constraints.xdc]

write_project_tcl -force -no_copy_sources -all_properties -use_bd_files {zynet.tcl}

#synth_design -quiet -top zyNet -part xc7z020clg484-1
#opt_design -quiet
#place_design -quiet
#route_design -quiet
#report_utilization -file utilization.log
#report_timing_summary -file timing.log
exit
