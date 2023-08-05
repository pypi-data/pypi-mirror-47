module tb_issue_134;

reg inverta_sigin;
reg invertb_sigin;
wire inverta_sigout;
wire invertb_sigout;

initial begin
    $from_myhdl(
        inverta_sigin,
        invertb_sigin
    );
    $to_myhdl(
        inverta_sigout,
        invertb_sigout
    );
end

issue_134 dut(
    inverta_sigin,
    invertb_sigin,
    inverta_sigout,
    invertb_sigout
);

endmodule
