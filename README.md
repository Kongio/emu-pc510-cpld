# E-mu E5000 Ultra: Complete Hardware Upgrade & Expansion Suite

A comprehensive technical repository for restoring, upgrading, and expanding the **E-mu E5000 Ultra** sampler to full flagship **E4XT Ultra / Platinum** hardware parity—expanding polyphony from 64 to **128 voices**, expanding onboard analog outputs from 4 to **8 outputs**, and supporting up to **16 discrete analog outputs** via the reverse-engineered **PC510 (Model 6313) Octopus Expander**.

---

## 1. Upgrade Comparison Matrix

The **E5000 Ultra**, **E6400 Ultra**, and **E4XT Ultra** all share the exact same motherboard PCB: **`SK10485`** (Rev A.1 / D.2). The E5000 Ultra was simply sold with several hardware sections unpopulated at the factory. 

By populating the factory-omitted footprints, the E5000 Ultra matches or exceeds the flagship specifications:

| Feature / Hardware | Factory E5000 Ultra | Factory E6400 Ultra | Factory E4XT Ultra | **E5000 Ultra (Fully Upgraded)** |
| :--- | :---: | :---: | :---: | :---: |
| **Polyphony** | 64 Voices | 64 Voices | 128 Voices | **128 Voices** |
| **G-Chip 2.0 (Sound Engine)** | 1 (`U42`) | 1 (`U42`) | 2 (`U42`, `U53`) | **2 (`U42`, `U53`)** |
| **H-Chip 1.5 (Z-Plane Filters)** | 2 (`U54`, `U60`) | 2 (`U54`, `U60`) | 4 (`U54`, `U60`, `U43`, `U44`) | **4 (`U54`, `U60`, `U43`, `U44`)** |
| **Motherboard Analog Outputs** | 4 (Main, Sub 1) | 8 (Main, Sub 1..3) | 8 (Main, Sub 1..3) | **8 (Main, Sub 1, Sub 2, Sub 3)** |
| **Motherboard DACs (CS4329)** | 2 (`U18`, `U20`) | 4 (`U18`, `U20`, `U22`, `U24`) | 4 (`U18`, `U20`, `U22`, `U24`) | **4 (`U18`, `U20`, `U22`, `U24`)** |
| **Motherboard Op-Amps (OP275)** | 8 | 12 | 12 | **12 (`U1..U8`, `U17`, `U23`, `U25`)** |
| **Motherboard 1/4" Audio Jacks** | 4 (`J1..J4`) | 8 (`J1..J8`) | 8 (`J1..J8`) | **8 (`J1..J8`)** |
| **Expander 6313 Support** | Optional | Optional | Optional | **Supported (Up to 16 Outputs Total)** |
| **EOS Auto-Detection** | Native | Native | Native | **Automatic (Zero Firmware Patches)** |

---

## 2. Overview of Upgrades in This Repository

```
                               E5000 ULTRA TOTAL SYSTEM EXPANSION (SK10485)
                                          
 +---------------------------------------------------------------------------------------------------------+
 |                                    COLDFIRE HOST CPU (MCF5206) & SOUND RAM                              |
 +---------------------------------------------------------------------------------------------------------+
          |                                                               |
          |  ColdFire Bus: BD[31:16], BA[11:1]                            |  Octopus Expander Bus:
          |                                                               |  BD[31:24], BA[14:1], EXPCSN
          v                                                               v
 +--------------------------------------------------+            +-----------------------------------------+
 |              MOTHERBOARD EXPANSION               |            |       OCTOPUS EXPANDER (PC510/PC511)    |
 |                                                  |            |                                         |
 |  [PROJECT 1: 128-VOICE UPGRADE]                  |            |  [PROJECT 3: CPLD REPLACEMENT]          |
 |  * [U53] G-Chip 2.0 (IC402) - Voices 65-128      |            |  * [U10] ATF1502AS CPLD (Replaces       |
 |  * [U43, U44] H-Chip 1.5 (IC413) - 64 Filters    |            |    obsolete Altera EPM7032LC44)         |
 |  * R209, R218 (3.92k 1%) + 19 Decoupling Caps    |            |  * Latches BA[1..9], decodes CSHCHPN,   |
 |  * Harvested from Proteus XL-6 donor board       |            |    WRPAGEN, and buffers BD[31:24]       |
 |                                                  |            |                                         |
 |  [PROJECT 2: 8-ANALOG OUTPUT UPGRADE]            |            |  * [U1, U2] Extra H-Chips (Voices/DSP)  |
 |  * [U22, U24] CS4329 20-bit Stereo DACs          |            |  * [U3..U6] CS4329 20-bit Stereo DACs   |
 |  * [U5..U8] OP275 Dual Audio Op-Amps             |            |  * 8 Balanced Outputs (Sub 4, 5, 6, 7)  |
 |  * [Q9..Q16] J109 Anti-Pop Muting JFETs          |            +-----------------------------------------+
 |  * [J5..J8] 1/4" Switched TRS Phone Jacks        |                                 |
 |  * Desolder RN10, Solder RN12 & RN13 (Jack Det)  |                                 |
 +--------------------------------------------------+                                 |
          |                                                                           |
          +------------------------------------+--------------------------------------+
                                               |
                                               v
                          +------------------------------------------+
                          |   TOTAL SYSTEM CAPACITY:                 |
                          |   * 128 VOICES OF POLYPHONY              |
                          |   * 16 DISCRETE BALANCED ANALOG OUTPUTS  |
                          +------------------------------------------+
```

---

### Project 1: 128-Voice Polyphony Motherboard Upgrade
* **Documentation**: **[`E5000_Ultra_128_Voice_Hardware_Upgrade_Guide.md`](E5000_Ultra_128_Voice_Hardware_Upgrade_Guide.md)**
* **Donor Board**: E-mu **Proteus XL-6** (or Proteus XL-1, PK-6, Proteus 1000). Because these 64-voice synth boards contain exactly **1 $\times$ G-Chip 2.0** (`IC402`, 100-pin QFP) and **2 $\times$ H-Chips 1.5** (`IC413`, 68-pin), they provide 100% of the active silicon required for the second 64-voice engine.
* **Component Additions**:
  * `U53`: G-Chip 2.0 (Voices 65–128)
  * `U43`: H-Chip 1.5 (G2.0 #2 Even Channel Z-Plane Filters)
  * `U44`: H-Chip 1.5 (G2.0 #2 Odd Channel Z-Plane Filters)
  * `R209`, `R218`: 3.92 kΩ 1% 0805 pull-ups for `GHRWAITN` bus handshakes
  * 19 $\times$ 0.01 µF 50V X7R 0805 ceramic decoupling capacitors
* **Auto-Detection**: During power-on self-test, the EOS BootROM asserts `G20CS2N` and `HCHIPCSN`. Upon detecting the new silicon, EOS automatically upgrades the polyphony counter from 64 to **128 voices** with no firmware patching or jumper changes required.

---

### Project 2: 8-Analog Output Motherboard Upgrade (Sub 2 & Sub 3 Addition)
* **Documentation**: **[`E5000_Ultra_8_Output_Hardware_Upgrade_Guide.md`](E5000_Ultra_8_Output_Hardware_Upgrade_Guide.md)**
* **Objective**: Populates the factory-omitted onboard **Sub 2 (Outs 5 & 6)** and **Sub 3 (Outs 7 & 8)** analog stages, giving the E5000 complete feature parity with the **E6400 Ultra**.
* **Audio Clocks**: The Altera FPGA (`U45`) already serializes and transmits all four I2S stereo streams (`I2SDO_0..3`, `I2SLR0..3`, `I2SBCK`, `FS512_B`) on every E-mu Ultra. The digital audio is already present on the empty pads.
* **Component Additions**:
  * `U22`, `U24`: Cirrus Logic **CS4329-KS** (20-bit Stereo DACs, SOIC-20)
  * `U5`, `U6`, `U7`, `U8`: Analog Devices **OP275GS** (Dual Audio Op-Amps, SOIC-8)
  * `Q9`..`Q16`: **J109** (N-Channel JFET anti-pop muting switches, SOT-23)
  * `D9`..`D16`: **MMBZ15** (15V Zener / TVS transient protection, SOT-23)
  * `J5`, `J6`, `J7`, `J8`: E-mu **`JA309`** switched 1/4" TRS phone jacks
  * 50 $\times$ SMD resistors and 32 $\times$ SMD capacitors (complete BOM in guide)
* **The Jack Detection Modification (Sheet 11)**:
  * **Desolder & Remove `RN10`** (4.7 kΩ $\times$ 4 pack, `STUFF=NO_SUB23`).
  * **Solder & Install `RN12` & `RN13`** (4.7 kΩ $\times$ 4 packs, `STUFF=SUB23`).
  * Allows EOS to detect cable insertion and automatically isolate or sum Sub 2 and Sub 3 mixes back into Main L/R.

---

### Project 3: PC510 / SK510 (Model 6313) 8-Output Expander CPLD Replacement
* **Documentation Directory**: **[`Octopus/`](Octopus/)**
* **Technical Guides**:
  * **[`Octopus/PC510_U10_CPLD_Replacement_Guide.md`](Octopus/PC510_U10_CPLD_Replacement_Guide.md)**: Flashing walkthrough using OpenOCD and USB-Blaster clone.
  * **[`Octopus/PC510_U10_Operational_Walkthrough.md`](Octopus/PC510_U10_Operational_Walkthrough.md)**: Deep architectural & bus cycle analysis.
* **Objective**: Replaces the obsolete Altera **EPM7032LC44** (`U10` address latch & decoder) on the PC510 expansion board using a modern, in-system programmable Microchip **ATF1502AS-10JU44** (PLCC-44).
* **Firmware & Toolchain**:
  * Production CUPL logic: [`Octopus/PC510_U10.pld`](Octopus/PC510_U10.pld)
  * Compiled SVF file: [`Octopus/EMU6313-V2.svf`](Octopus/EMU6313-V2.svf) (patched with `MASK (00000000)` for universal Silicon ID bypass)
  * Python simulation suite: [`Octopus/simulate_vectors.py`](Octopus/simulate_vectors.py)
  * OpenOCD configuration: `program_atf.cfg`
  * Future re-flash override: +12V VPP on Pin 44 (`OE1`) to re-enable JTAG when disabled.

---

## 3. Motherboard Physical Layout Guide (`SK10485`)

```
   +-------------------------------------------------------------------------------------------------+
   |                                 E5000 ULTRA REAR PANEL (I/O)                                    |
   |                                                                                                 |
   |   [ J1 / J2 ]        [ J3 / J4 ]               [ J5 / J6 ]               [ J7 / J8 ]            |
   |    MAIN OUTS          SUB 1 OUTS                SUB 2 OUTS                SUB 3 OUTS            |
   |  (Factory Pop)       (Factory Pop)           [PROJECT 2 UPGRADE]       [PROJECT 2 UPGRADE]      |
   |                                                                                                 |
   |   [ U1, U2 ]         [ U3, U4 ]                [ U5, U6 ]                [ U7, U8 ]             |
   |   OP275 OpAmps       OP275 OpAmps              OP275 OpAmps              OP275 OpAmps           |
   |                                                                                                 |
   |     [ U18 ]            [ U20 ]                   [ U22 ]                   [ U24 ]              |
   |   CS4329 DAC         CS4329 DAC                CS4329 DAC                CS4329 DAC             |
   |                                                                                                 |
   |                      +-----------------------+                                                  |
   |                      |  JACK DETECT (SHT 11) |                                                  |
   |                      |  * Desolder RN10      |                                                  |
   |                      |  * Solder RN12, RN13  |                                                  |
   |                      +-----------------------+                                                  |
   |                                                                                                 |
   |   [ U60 ]            [ U54 ]                   [ U43 ]                   [ U44 ]                |
   |  H-CHIP #1          H-CHIP #0                 H-CHIP #2                 H-CHIP #3               |
   | (Factory Pop)       (Factory Pop)          [PROJECT 1 UPGRADE]       [PROJECT 1 UPGRADE]        |
   |                                                                                [ R218 ]         |
   |                                                                             (3.92k Pullup)      |
   |                                                                                                 |
   |             [ U42 ]                                           [ U53 ]                           |
   |         G-CHIP 2.0 #1                                     G-CHIP 2.0 #2                         |
   |       (Voices 1 - 64)                                   (Voices 65 - 128)                       |
   |        (Factory Pop)                                   [PROJECT 1 UPGRADE]                      |
   |           [ R208 ]                                           [ R209 ]                           |
   |        (3.92k Pullup)                                     (3.92k Pullup)                        |
   |                                                                                                 |
   |   +-------------------+  +-------------------+  +-------------------+  +--------------------+   |
   |   |   SOUND SIMM 0    |  |   SOUND SIMM 1    |  |   SOUND SIMM 2    |  |    SOUND SIMM 3    |   |
   |   +-------------------+  +-------------------+  +-------------------+  +--------------------+   |
   |                                                                                                 |
   +-------------------------------------------------------------------------------------------------+
   |                                    FRONT PANEL & LCD DISPLAY                                    |
   +-------------------------------------------------------------------------------------------------+
```

---

## 4. Built-In Factory Service Diagnostics (Password: `1358`)

EOS contains a built-in hardware diagnostic suite that can verify both the 128-voice expansion and the 8-output analog stages:

```
[ FRONT PANEL ]  -->  [ Master ]  -->  [ Utils ]  -->  [ Tests ]  -->  Enter Password " 1358 "
```

### Tests to Run After Upgrades:
1. **Polyphony / Voice Allocation Test**:
   * Sequentially triggers notes across channels 1 to 128.
   * Confirms that `U53` is generating voices 65–128 and that `U43`/`U44` are filtering odd/even channels cleanly.
2. **Interactive Jack Detection Test**:
   * Displays onscreen status (`[OPEN]` vs `[CLOSED]`) for all 8 output jacks.
   * Plug a 1/4" cable into `J5`, `J6`, `J7`, and `J8` individually to verify that the shunt switches toggle dynamically.
3. **Audio Output / DAC Sine Wave Test**:
   * Generates a 1 kHz reference tone through Sub 2 and Sub 3 to confirm full dynamic range and zero distortion.
4. **gRAM Memory Arbitration Test**:
   * Verifies shared sample DRAM bus timing between G-Chip #1 (`U42`) and G-Chip #2 (`U53`).

---

## 5. Repository File Index

```
.
├── README.md                                    # Master repository overview & hardware upgrade guide
├── E5000_Ultra_128_Voice_Hardware_Upgrade_Guide.md # Project 1: Complete 128-voice polyphony guide
├── E5000_Ultra_8_Output_Hardware_Upgrade_Guide.md  # Project 2: Complete 8-analog output hardware guide
├── e-mu_eos_technical_documents.pdf             # Official E-mu 1999 318-page technical manual & schematics
│
└── Octopus/                                     # Project 3: PC510 Octopus Expander CPLD Replacement
    ├── README.md                                # PC510 project summary & flashing reference
    ├── PC510_U10_CPLD_Replacement_Guide.md      # Step-by-step ATF1502 flashing guide (OpenOCD/ATMISP)
    ├── PC510_U10_Operational_Walkthrough.md     # Deep bus timing & address latch analysis
    ├── PC510_U10_test_guide.md                  # Bench verification voltage table
    ├── PC510_U10.pld                            # Production CUPL source code (transparent latches)
    ├── PC510_U10_passthrough.pld                # Combinatorial pass-through variant
    ├── simulate_vectors.py                      # Python bus cycle verification simulator
    ├── EMU6313-V2.svf                           # Production SVF file (patched with MASK 00000000)
    ├── EMU6313-V2.si                            # WinCUPL CSIM full vector test file
    ├── PC510_U10.si                             # WinCUPL CSIM primary test vectors
    ├── EMU6313-V2_decodes.si                    # WinCUPL CSIM decode-only test vectors
    └── EMU6313-V2_full.si                       # WinCUPL CSIM extended vectors
```

---

## 6. Credits & Technical References

* **Schematics & Service Data**: E-mu Systems Technical Documentation Archive (`SK10485` Rev A.1/D.2, `SK510` Rev A).
* **Silicon Architecture**: Designed by Dave Rossum and the E-mu Systems ASIC Engineering Team (G-Chip 2.0 / Gossett-Smith Interpolator, H-Chip 1.5 Z-Plane Filter Engine).
* **Reverse Engineering & Documentation**: Steve Seddon ([Kongio](https://github.com/Kongio)).
