# E-mu PC510 / SK510 U10 CPLD Replacement (ATF1502AS)

Drop-in replacement of the obsolete Altera **EPM7032LC44** (`U10` Chip Select & Address Latch) on the **E-mu PC510 / SK510 Rev A** Digital Audio & 8-Analog Output expansion board using an Atmel/Microchip **ATF1502AS-10JU44** (PLCC-44).

Used in **E-mu Emulator IV, E5000 Ultra, E6400, and E-Synth** samplers.

---

## Repository Contents

* **[`PC510_U10_Operational_Walkthrough.md`](PC510_U10_Operational_Walkthrough.md)**: Deep architectural & bus cycle walkthrough:
  * How the E-mu host CPU interacts with the PC510 expansion slot
  * Line-by-line breakdown of every input and output pin
  * Detailed step-by-step sequence diagrams for Page Register writes and H-Chip reads/writes
  * Transparent address latch timing and protection theory
* **[`E5000_Ultra_128_Voice_Hardware_Upgrade_Guide.md`](E5000_Ultra_128_Voice_Hardware_Upgrade_Guide.md)**: Hardware upgrade guide for converting the **E-mu E5000 Ultra** (64 voices) to full **128 voices** using donor ASICs from a Proteus XL-6 / Proteus 2000 series board:
  * Complete Bill of Materials (BOM) including missing passives (`R209`, `R218`, and 19 decoupling capacitors)
  * Component locations on motherboard schematic `SK10485` (`U53`, `U43`, `U44`)
  * Hot air harvesting, pad preparation, and drag-soldering steps
  * ColdFire bus, sample RAM, and G-to-H digital audio routing
  * EOS auto-detection sequence and hidden service diagnostics (`1358`)
* **[`E5000_Ultra_8_Output_Hardware_Upgrade_Guide.md`](E5000_Ultra_8_Output_Hardware_Upgrade_Guide.md)**: Hardware upgrade guide for converting the **E-mu E5000 Ultra** from 4 outputs to full **8 analog outputs** (Sub 2 & Sub 3 pairs), achieving complete motherboard feature parity with the **E6400 Ultra**:
  * Complete Bill of Materials (BOM): CS4329 DACs, OP275 Op-Amps, J109 muting FETs, and 1/4" phone jacks (`J5`..`J8`)
  * The critical Jack Detection resistor network modification (desoldering `RN10`, installing `RN12` & `RN13`)
  * Full schematic walkthrough of Sheets 11, 14, and 15 (`SK10485`)
  * EOS interactive jack detection diagnostics (`1358`) and audio routing verification
* **[`PC510_U10_CPLD_Replacement_Guide.md`](PC510_U10_CPLD_Replacement_Guide.md)**: Complete step-by-step technical guide covering:
  * Physical PLCC-44 pinout and schematic connections
  * CUPL decode and latch logic
  * WinCUPL compilation with ATF1502 Fitter (`JTAG = OFF`)
  * Microchip ATMISP 7.3 SVF generation
  * Silicon IDCODE patch (`MASK 00000000`)
  * OpenOCD + USB-Blaster flashing & verification
  * Future maintenance & the +12V high-voltage reflash override
* **[`PC510_U10.pld`](PC510_U10.pld)**: Production CUPL logic source file with transparent latches and exact PCB pinout.
* **[`PC510_U10_passthrough.pld`](PC510_U10_passthrough.pld)**: Combinatorial pass-through variant.
* **[`simulate_vectors.py`](simulate_vectors.py)**: Python logic simulator verifying all 14 expansion bus cycles.
* **[`EMU6313-V2.si`](EMU6313-V2.si)**, **[`PC510_U10.si`](PC510_U10.si)**, **[`EMU6313-V2_decodes.si`](EMU6313-V2_decodes.si)**: WinCUPL CSIM test vector files.
* **[`PC510_U10_test_guide.md`](PC510_U10_test_guide.md)**: Bench / breadboard voltage verification table.

---

## Quick Flashing Reference

1. Compile in **WinCUPL** using target device `f1502ispplcc44`.
2. Generate `.svf` via **Microchip ATMISP 7.3** (enable `[X] Write SVF file` and `STATE RESETS`).
3. Patch the `.svf` file at line 21: change `MASK (ffffffff)` to `MASK (00000000)`.
4. Flash via **OpenOCD** with a USB-Blaster clone:
   ```cmd
   openocd.exe -f program_atf.cfg
   ```
5. Install programmed chip into socket `U10` on the PC510 card (align Pin 1 chamfer).
