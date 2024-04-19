`timescale 1ns / 1ps

module top(
    input       clk,
    output reg  rst_n,

    output wire txp
    );

//Print Controll -------------------------------------------
`include "print.vh"
defparam tx.uart_freq=115200;
defparam tx.clk_freq=27_000_000;
assign print_clk = clk;
assign txp = uart_txp;

reg[2:0] state_0;
reg[2:0] state_1;
reg[2:0] state_old;
wire[2:0] state_new = state_1;

always@(posedge clk)begin
  if(rst_n==1'b0)`print("Perform Reset\nAuto Reset Every 100s\n",STR);
end
//Print Controll -------------------------------------------

endmodule
