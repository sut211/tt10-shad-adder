/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_shad_adder (
    input  wire [7:0] ui_in,    // Lower 8-bit input (B[7:0])
    output wire [7:0] uo_out,   // 8-bit output (C[7:0])
    input  wire [7:0] uio_in,   // Upper 8-bit input (A[7:0])
    output wire [7:0] uio_out,  // IOs: Output path (Unused, set to 0)
    output wire [7:0] uio_oe,   // IOs: Enable path (Unused, set to 0)
    input  wire       ena,      // always 1 when powered, ignore
    input  wire       clk,      // clock (Unused)
    input  wire       rst_n     // reset_n - low to reset (Unused)
);

  // Combine the two 8-bit inputs into a single 16-bit input vector
  wire [15:0] In = {uio_in, ui_in};  // In[15:8] = A[7:0], In[7:0] = B[7:0]
  reg  [7:0] C; // Output register

  always @(*) begin
    casez (In)
        16'b1???????????????: C = 8'd15;
        16'b01??????????????: C = 8'd14;
        16'b001?????????????: C = 8'd13;
        16'b0001????????????: C = 8'd12;
        16'b00001???????????: C = 8'd11;
        16'b000001??????????: C = 8'd10;
        16'b0000001?????????: C = 8'd9;
        16'b00000001????????: C = 8'd8;
        16'b000000001???????: C = 8'd7;
        16'b0000000001??????: C = 8'd6;
        16'b00000000001?????: C = 8'd5;
        16'b000000000001????: C = 8'd4;
        16'b0000000000001???: C = 8'd3;
        16'b00000000000001??: C = 8'd2;
        16'b000000000000001?: C = 8'd1;
        16'b0000000000000001: C = 8'd0;
        default: C = 8'b1111_0000;  // Special case: all zeros
    endcase
  end

  // Assign outputs
  assign uo_out  = C;   // Output priority position
  assign uio_out = 0;   // Unused bidirectional output set to 0
  assign uio_oe  = 0;   // Disable bidirectional outputs

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
