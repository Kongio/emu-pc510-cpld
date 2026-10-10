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
