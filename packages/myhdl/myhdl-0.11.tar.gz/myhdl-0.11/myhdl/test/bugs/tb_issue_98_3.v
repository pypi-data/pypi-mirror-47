module tb_issue_98_3;

wire [0:0] sda;
wire [0:0] scl;
wire [0:0] sda_i;
reg [0:0] sda_o;
wire [0:0] scl_i;
reg [0:0] scl_o;

initial begin
    $from_myhdl(
        sda_o,
        scl_o
    );
    $to_myhdl(
        sda,
        scl,
        sda_i,
        scl_i
    );
end

issue_98_3 dut(
    sda,
    scl,
    sda_i,
    sda_o,
    scl_i,
    scl_o
);

endmodule
