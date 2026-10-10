#!/usr/bin/env python3
"""
Logic Simulator for E-mu PC510 (SK510 REV A) U10 CPLD
Simulates Address Decoding, Bus Buffers, and Address/Read Latching.
"""

def simulate_step(upclrn, expcsn, iowrn, rd, hwaitn, a13, a12, a11, a10, abus_val, prev_la, prev_lrd):
    # Output Enable governed by UPCLRN (Pin 1)
    if upclrn == 0:
        return {
            'bufoen': 'Z',
            'cshchpn': 'Z',
            'wrpagen': 'Z',
            'lrd': 'Z',
            'la': 0,
            'la_str': 'ZZZZZZZZZ'
        }
    
    # 1. BUFOEN: Active low for 0x540000 - 0x5407FF (!EXPCSN & !A13 & !A12 & !A11)
    bufoen = 0 if (expcsn == 0 and a13 == 0 and a12 == 0 and a11 == 0) else 1
    
    # 2. CSHCHPN: Active low for 0x540400 - 0x5407FF (!EXPCSN & !A13 & !A12 & !A11 & A10)
    cshchpn = 0 if (expcsn == 0 and a13 == 0 and a12 == 0 and a11 == 0 and a10 == 1) else 1
    
    # 3. WRPAGEN: Active low for 0x540000 - 0x5403FF during write (!EXPCSN & !A13 & !A12 & !A11 & !A10 & !IOWRN)
    wrpagen = 0 if (expcsn == 0 and a13 == 0 and a12 == 0 and a11 == 0 and a10 == 0 and iowrn == 0) else 1
    
    # 4. Latches: Transparent when idle (EXPCSN=1 and HWAITN=1), frozen during cycle
    latch_en = (expcsn == 1 and hwaitn == 1)
    if latch_en:
        la = abus_val
        lrd = rd
    else:
        la = prev_la
        lrd = prev_lrd
        
    la_bin = f"{la:09b}"
    return {
        'bufoen': str(bufoen),
        'cshchpn': str(cshchpn),
        'wrpagen': str(wrpagen),
        'lrd': str(lrd),
        'la': la,
        'la_str': la_bin
    }

def run_test_suite():
    tests = [
        # (Step Name, Description, UPCLRN, EXPCSN, IOWRN, RD, HWAITN, A13, A12, A11, A10, A[9:1])
        ("Test 1", "Power-on Reset (Outputs High-Z)",           0, 1, 1, 1, 1, 0, 0, 0, 0, 0x000),
        ("Test 2", "Bus Idle (Pattern 0x155 transparent)",     1, 1, 1, 1, 1, 0, 0, 0, 0, 0x155),
        ("Test 3", "Bus Idle (Address changes to 0x0AA)",       1, 1, 1, 1, 1, 0, 0, 0, 0, 0x0AA),
        ("Test 4", "Read H-Chips @ 0x540400 (EXPCSN=0,A10=1)",  1, 0, 1, 1, 1, 0, 0, 0, 1, 0x0AA),
        ("Test 5", "H-Chip asserts HWAITN=0 (via DTACKN)",      1, 0, 1, 1, 0, 0, 0, 0, 1, 0x0AA),
        ("Test 6", "Host address floats to 0x1FF during wait",  1, 0, 1, 1, 0, 0, 0, 0, 1, 0x1FF),
        ("Test 7", "H-Chip releases HWAITN=1 (Ready)",          1, 0, 1, 1, 1, 0, 0, 0, 1, 0x0AA),
        ("Test 8", "End Read Cycle / Setup Write (RD=0)",       1, 1, 1, 0, 1, 0, 0, 0, 0, 0x000),
        ("Test 9", "Write Page Reg Setup @ 0x540000 (RD=0)",    1, 0, 1, 0, 1, 0, 0, 0, 0, 0x000),
        ("Test 10", "Write Strobe asserts (IOWRN=0)",           1, 0, 0, 0, 1, 0, 0, 0, 0, 0x000),
        ("Test 11", "Write Strobe ends (IOWRN=1 -> clocks U9)", 1, 0, 1, 0, 1, 0, 0, 0, 0, 0x000),
        ("Test 12", "End Write Cycle (EXPCSN=1)",               1, 1, 1, 1, 1, 0, 0, 0, 0, 0x000),
        ("Test 13", "Isolated Range @ 0x540800 (A11=1)",        1, 0, 1, 1, 1, 0, 0, 1, 0, 0x000),
        ("Test 14", "Isolated Range @ 0x542000 (A13=1)",        1, 0, 1, 1, 1, 1, 0, 0, 0, 0x000),
    ]

    print("=" * 105)
    print("E-MU PC510 U10 CPLD LOGIC SIMULATION REPORT")
    print("=" * 105)
    print(f"{'Step':<8} | {'Description':<42} | {'BUFOEN':<6} | {'CSHCHPN':<7} | {'WRPAGEN':<7} | {'LRD':<3} | {'LA[9:1]':<11} | {'Status':<6}")
    print("-" * 105)

    current_la = 0
    current_lrd = 1
    all_passed = True

    expected = [
        ('Z', 'Z', 'Z', 'Z', 'ZZZZZZZZZ'),
        ('1', '1', '1', '1', '101010101'),
        ('1', '1', '1', '1', '010101010'),
        ('0', '0', '1', '1', '010101010'),
        ('0', '0', '1', '1', '010101010'),
        ('0', '0', '1', '1', '010101010'), # Must stay 010101010 even when bus is 111111111!
        ('0', '0', '1', '1', '010101010'),
        ('1', '1', '1', '0', '000000000'),
        ('0', '1', '1', '0', '000000000'),
        ('0', '1', '0', '0', '000000000'),
        ('0', '1', '1', '0', '000000000'),
        ('1', '1', '1', '1', '000000000'),
        ('1', '1', '1', '1', '000000000'),
        ('1', '1', '1', '1', '000000000'),
    ]

    for idx, (s_name, desc, up, cs, wr, rd, wt, a13, a12, a11, a10, abus) in enumerate(tests):
        out = simulate_step(up, cs, wr, rd, wt, a13, a12, a11, a10, abus, current_la, current_lrd)
        if out['la_str'] != 'ZZZZZZZZZ':
            current_la = out['la']
            current_lrd = int(out['lrd'])
            
        exp_b, exp_c, exp_w, exp_l, exp_la = expected[idx]
        pass_check = (out['bufoen'] == exp_b and 
                      out['cshchpn'] == exp_c and 
                      out['wrpagen'] == exp_w and 
                      out['lrd'] == exp_l and 
                      out['la_str'] == exp_la)
        
        status = "PASS" if pass_check else "FAIL"
        if not pass_check:
            all_passed = False
            
        print(f"{s_name:<8} | {desc:<42} | {out['bufoen']:<6} | {out['cshchpn']:<7} | {out['wrpagen']:<7} | {out['lrd']:<3} | {out['la_str']:<11} | {status:<6}")

    print("-" * 105)
    if all_passed:
        print("RESULT: ALL 14 TEST VECTORS PASSED PERFECTLY! LOGIC IS VERIFIED.")
    else:
        print("RESULT: VERIFICATION FAILED.")
    print("=" * 105)

if __name__ == "__main__":
    run_test_suite()
