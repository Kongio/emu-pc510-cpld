# E-mu E5000 Ultra: 128-Voice Polyphony Hardware Upgrade Guide

A complete, component-level technical guide for upgrading the **E-mu E5000 Ultra** from factory 64-voice polyphony to full **128-voice polyphony** using ASICs harvested from a 64-voice donor board (such as the **E-mu Proteus XL-6**, **Proteus XL-1**, **PK-6**, or **Proteus 1000**).

---

## 1. Executive Summary & Architecture

### Motherboard Commonality
The E-mu Systems **E4 Ultra** product line—including the **E5000 Ultra**, **E6400 Ultra**, and **E4XT Ultra**—shares an identical common motherboard PCB: **`SK10485`** (Rev A.1 / D.2).

* **E4XT Ultra / E4 Platinum**: Factory-populated with 128 voices (2 $\times$ G-Chips, 4 $\times$ H-Chips).
* **E5000 Ultra / Standard E6400 Ultra**: Factory-populated with 64 voices (1 $\times$ G-Chip, 2 $\times$ H-Chips). The pads for the second 64-voice engine are left unpopulated at the factory.

```
                              E-MU E4 ULTRA SOUND ENGINE ARCHITECTURE (SK10485)
                                          
 +-------------------------------------------------------------------------------------------------------+
 |                                CODFIRE HOST CPU (MCF5206) & SOUND MEMORY                              |
 +-------------------------------------------------------------------------------------------------------+
                                  |                                             |
                  ColdFire Bus: BD[31:16], BA[11:1]              ColdFire Bus: BD[31:16], BA[11:1]
                  Chip Select: G20CS1N                           Chip Select: G20CS2N
                  Handshake: DTACKN, GHRWAITN                    Handshake: DTACKN, GHRWAITN
                                  |                                             |
                                  v                                             v
 +---------------------------------------------------+         +---------------------------------------------------+
 |             VOICES 1 - 64 (FACTORY POPULATED)     |         |            VOICES 65 - 128 (UPGRADE SECTION)      |
 |                                                   |         |                                                   |
 |   [U42] G-CHIP 2.0 #1 (IC402)                     |         |   [U53] G-CHIP 2.0 #2 (IC402)                     |
 |   Sample Playback, Pitch Interpolation & Mixing   |         |   Sample Playback, Pitch Interpolation & Mixing   |
 |   Pull-up: R208 (3.92k 1%)                        |         |   Pull-up: R209 (3.92k 1%)                        |
 |   Decoupling: C141..C144, C163, C167, C169        |         |   Decoupling: C164..C166, C168, C170, C191, C192  |
 +---------------------------------------------------+         +---------------------------------------------------+
                |                            |                                |                            |
         Audio: G1SRCD0               Audio: G1SRCD1                   Audio: G2SRCD0               Audio: G2SRCD1
         (Even Ch)                    (Odd Ch)                         (Even Ch)                    (Odd Ch)
                |                            |                                |                            |
                v                            v                                v                            v
 +----------------------------+ +----------------------------+ +----------------------------+ +----------------------------+
 | [U60] H-CHIP 1.5 #1        | | [U54] H-CHIP 1.5 #0        | | [U43] H-CHIP 1.5 #2        | | [U44] H-CHIP 1.5 #3        |
 | (IC413)                    | | (IC413)                    | | (IC413)                    | | (IC413)                    |
 | Even Channel Z-Plane Filter| | Odd Channel Z-Plane Filter | | Even Channel Z-Plane Filter| | Odd Channel Z-Plane Filter |
 | Decoupling: 6x 0.01uF Caps | | Decoupling: 6x 0.01uF Caps | | Decoupling: 6x 0.01uF Caps | | Decoupling: 6x 0.01uF Caps |
 +----------------------------+ +----------------------------+ +----------------------------+ +----------------------------+
                \                            /                                \                            /
                 \                          /                                  \                          /
                  +------------------------+                                    +------------------------+
                  |  Pull-up: R202 (1.0k)  |                                    |  Pull-up: R218 (3.92k) |
                  +------------------------+                                    +------------------------+
                               |                                                             |
                               +-----------------------------+-------------------------------+
                                                             |
                                                             v
                                             +-------------------------------+
                                             |  OCTOPUS EXPANDER / MAIN DACS |
                                             |  (CS4329 20-bit Stereo DACs)  |
                                             +-------------------------------+
```

### Why the Proteus XL-6 Is the Exact Donor
The Proteus 2000 series sound modules use the exact same custom E-mu VLSI chips. While 128-voice rack units (like the standard Proteus 2000, Orbit-3, or Turbo models) contain 2 G-chips and 4 H-chips, the **64-voice keyboards and modules**—including the **Proteus XL-6 (Xtreme Keys)**, **XL-1 (standard)**, **PK-6**, and **Proteus 1000**—are built with **exactly 1 G-Chip and 2 H-Chips**.

Harvesting these three chips from an XL-6 provides **100% of the missing active silicon** needed to complete the second 64-voice group on the E5000 Ultra motherboard.

---

## 2. Complete Bill of Materials (BOM)

To successfully upgrade the motherboard, you must install the **3 ASICs** and **21 supporting passives** (2 pull-up resistors and 19 decoupling capacitors).

### A. Active ASICs (Harvested from Donor)

| Reference | Part Description | E-mu P/N | Schematic Sheet | Footprint / Package | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`U53`** | **G-Chip 2.0** | `IC402` (G2.0 / G-II) | Sheet 9 (`SK10485`) | 100-pin PQFP (0.65mm pitch) | Second Sound Engine (Voices 65–128) |
| **`U43`** | **H-Chip 1.5** | `IC413` (H-1.5) | Sheet 13 (`SK10485`) | 68-pin PLCC / Surface Mount | Z-Plane Filter (G2.0 #2 Even Channels) |
| **`U44`** | **H-Chip 1.5** | `IC413` (H-1.5) | Sheet 13 (`SK10485`) | 68-pin PLCC / Surface Mount | Z-Plane Filter (G2.0 #2 Odd Channels) |

> [!NOTE]
> `U43` and `U44` are identical H-1.5 silicon (`IC413`). Either donor H-chip can be soldered into either position; the board traces configure their odd/even role via hardware strapping pins `CHPN0` (Pin 20) and `CHPN1` (Pin 21).

### B. Pull-Up Resistors (0805 SMD)

| Reference | Value | Tolerance | Schematic Sheet | Connected Signal | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`R209`** | **3.92 kΩ** | 1% (Metal Film) | Sheet 9 | `GHRWAITN` $\leftrightarrow$ `VCC` (+5V) | Bus handshake ready/wait line pull-up for G-Chip #2 (`U53`) |
| **`R218`** | **3.92 kΩ** | 1% (Metal Film) | Sheet 13 | `GHRWAITN` $\leftrightarrow$ `VCC` (+5V) | Bus handshake ready/wait line pull-up for H-Chips #2 & #3 (`U43`/`U44`) |

### C. Power Decoupling Capacitors (0805 SMD Ceramic)

All decoupling capacitors are **0.01 µF (10 nF), 50V, X7R, 0805 SMD**.

#### 1. For G-Chip 2.0 (`U53`) — 7 Capacitors (Sheet 9)
* **`C164`**, **`C165`**, **`C166`**, **`C168`**, **`C170`**, **`C191`**, **`C192`**
*(Note: C141, C142, C143, C144, C163, C167, and C169 are already factory-installed for U42).*

#### 2. For H-Chips 1.5 (`U43` & `U44`) — 12 Capacitors (Sheet 13)
* **`C127`**, **`C128`**, **`C130`**, **`C131`**, **`C145`**, **`C146`**, **`C147`**, **`C148`**, **`C149`**, **`C150`**, **`C172`**, **`C175`**
*(6 capacitors decouple `U43`, and 6 capacitors decouple `U44`).*

---

## 3. Bus Signals & Signal Interconnect Breakdown

Understanding how the new chips interact with the rest of the motherboard helps with troubleshooting and oscilloscope probing:

### 1. Host ColdFire CPU Interface
* **Data Bus**: `BD[31:16]` (Upper 16 bits of the buffered processor data bus). Both `U53` and `U43`/`U44` share this data bus with the existing chips.
* **Address Bus**: `BA[11:1]` (Buffered processor address bus).
* **Chip Selects**:
  * `G20CS2N` (Sheet 9, Pin 74 of `U53`): Active-low chip select dedicated exclusively to G-Chip #2. Driven by the motherboard PLD/FPGA memory decoder.
  * `HCHIPCSN` (Sheet 13, Pin 18 of `U43` and `U44`): Active-low chip select for the H-chips, further qualified by individual channel addresses.
* **Handshake Lines**:
  * `DTACKN` (Data Acknowledge): Notifies the ColdFire CPU that read data is valid or write data has been latched.
  * `GHRWAITN` (G/H Ready Wait Line): Open-drain bus handshake pulled up by `R209` and `R218`.

### 2. Sound RAM Access
* G-Chip #2 (`U53`) connects directly to the shared Sample Memory Bus:
  * Address: `SMA[25:0]`
  * Data: `SMD[15:0]`
  * Controls: `SMRAS0N`..`SMRAS3N`, `SMOEN`, `SMWEN`, `SMBSYN`, `SMREQN`.
* When voices 65–128 are triggered, `U53` arbitrates for memory access to fetch sample words without interfering with `U42`.

### 3. Digital Audio Interconnect (G-to-H Serial Stream)
* `U53` generates two digital serial audio streams:
  * **`G2SRCD0`** (Pin 83 of `U53`): Routes to **Pin 67 of `U43`** (Even voice filter channel).
  * **`G2SRCD1`** (Pin 84 of `U53`): Routes to **Pin 67 of `U44`** (Odd voice filter channel).
* If `U53` is installed without `U43`/`U44`, the sound engine calculates voices 65–128 in software, but the audio never reaches the filter or DAC stage.
* If `U43`/`U44` are installed without `U53`, the filters run idle with no input signal.
* **Both ASICs must be present for functional 128-voice operation.**

---

## 4. Step-by-Step Rework & Installation Procedure

### Required Equipment
* **Hot Air Rework Station** with temperature calibration and a ~10–12mm round nozzle.
* **Temperature-controlled Soldering Iron** with a fine chisel or bevel/hoof tip (e.g., Hakko T18-C2 or T18-CF15).
* **High-grade Tacky Flux** (Amtech NC-559-V2-TF, ChipQuik SMD291, or equivalent).
* **Desoldering Braid / Solder Wick** (2.0mm–2.5mm width) with rosin core.
* **Kapton (Polyimide) Tape** (10mm–20mm width).
* **Stereo Inspection Microscope** or high-magnification jeweler’s loupe (10x–20x).
* **Isopropyl Alcohol (IPA 99.9%)** and lint-free cotton swabs.
* **Anti-static Tweezers** and vacuum IC pickup pen.

---

### Step 1: Harvesting ASICs from the Donor Board

1. **Protect Surrounding Components**:
   * Wrap high-temperature Kapton tape around adjacent electrolytic capacitors, plastic connectors, and delicate passives on the Proteus XL-6 board.
2. **Apply Flux**:
   * Generously apply tacky flux around all four sides of `IC402` (G-Chip) and both `IC413` (H-Chips).
3. **Hot Air Removal**:
   * Set hot air station to **360°C–380°C** with medium airflow (~30–40 L/min).
   * Move nozzle in a continuous rectangular motion 15–20mm above the pins. Heat the ground plane and leads evenly for 45–60 seconds.
   * **Do not force or pry the chip.** Test readiness by touching the corner lightly with tweezers. Once all pins are molten, lift cleanly with a vacuum pen or tweezers.
4. **Clean Donor Chip Leads**:
   * Place harvested chips onto a heat-resistant silicone mat.
   * Add a drop of flux and gently sweep a clean iron tip with solder wick across the leads to remove oxidation and excess solder. Straighten any bent pins under magnification.

---

### Step 2: Preparing the E5000 Motherboard Pads

1. **Inspect Pad Condition**:
   * Locate `U53` (Sheet 9, adjacent to `U42`) and `U43` / `U44` (Sheet 13).
   * Locate resistor footprints `R209`, `R218`, and the 19 capacitor footprints.
2. **Flatten the Solder Pads**:
   * Apply flux to the unpopulated pads.
   * Lay clean copper braid across the pads and gently glide the iron tip across the braid.
   * Ensure all pads are coplanar and completely flat. Wipe thoroughly with IPA.

---

### Step 3: Soldering G-Chip 2.0 (`U53`)

1. **Pin 1 Orientation**:
   * Locate the Pin 1 indicator (chamfered corner / round index dimple) on the `U53` PCB silkscreen and match it with the index mark on the harvested G-Chip.
2. **Tacking Diagonal Corners**:
   * Align all 100 leads perfectly with the PCB pads under magnification.
   * Apply light downward pressure on the center of the chip package.
   * Solder Pin 1 and the diagonally opposite corner pin (Pin 51) to lock the chip in position. Double-check alignment on all four sides.
3. **Drag Soldering**:
   * Apply tacky flux across the entire row of pins on one side.
   * Feed a small bead of 63/37 leaded (or lead-free SAC305) solder onto your bevel/hoof iron tip.
   * Glide the iron smoothly down the row across the pad-lead junctions. Surface tension and flux will draw solder into each joint.
   * Repeat for all four sides.
4. **Bridge Removal**:
   * If bridges form between adjacent pins, add a drop of flux, clean your iron tip, and drag the dry tip away from the chip package outward along the pins to pull away excess solder.

---

### Step 4: Soldering H-Chips 1.5 (`U43` & `U44`)

1. Verify Pin 1 alignment for `U43` and `U44`.
2. Follow the same alignment, corner tacking, and drag soldering technique as described for `U53`.
3. Clean the board with IPA and inspect every lead under the microscope for cold solder joints or micro-bridges.

---

### Step 5: Installing Pull-Up Resistors & Decoupling Capacitors

1. **Solder Resistors**:
   * **`R209`**: 3.92 kΩ 1% 0805 SMD (Sheet 9).
   * **`R218`**: 3.92 kΩ 1% 0805 SMD (Sheet 13).
2. **Solder Decoupling Capacitors**:
   * Solder the **7 capacitors for `U53`**: `C164`, `C165`, `C166`, `C168`, `C170`, `C191`, `C192`.
   * Solder the **12 capacitors for `U43`/`U44`**: `C127`, `C128`, `C130`, `C131`, `C145`, `C146`, `C147`, `C148`, `C149`, `C150`, `C172`, `C175`.
3. Perform a final wash with IPA to eliminate any conductive flux residues.

---

## 5. Firmware & EOS Auto-Detection Mechanism

One of the greatest design features of E-mu Systems' EOS architecture is that **no firmware flashing, EEPROM reprogramming, or jumper modification is required**:

1. **Power-On Reset (POR)**:
   * During the ColdFire processor boot sequence, the EOS kernel executes hardware self-tests.
2. **Chip Select Polling**:
   * The kernel asserts `G20CS2N` (Chip Select 2) and performs a probe read on `U53` registers over `BD[31:16]`.
   * If `U53` responds with a valid device handshake and clear data ack (`DTACKN`), EOS marks G-Chip #2 as present.
   * It then addresses `U43` and `U44` through `HCHIPCSN`.
3. **Dynamic Voice Table Reallocation**:
   * If both G-Chip #2 and H-Chips #2 & #3 respond successfully, EOS sets the global polyphony constant from `64` to `128`.
   * The boot splash screen will immediately display:
     ```
     E5000 Ultra
     EOS 4.70 (or current version)
     128 MB RAM / 128 Voices
     ```

---

## 6. Verification & Hardware Diagnostics Walkthrough

### Pre-Power Cold Resistance Checks
Before plugging in the AC power cord, use a digital multimeter in resistance / continuity mode:
* Measure resistance between **`+5V` (`VCC`)** and **`GND`** at any of the new decoupling capacitors (e.g., across `C164`).
* Verify that there is **no short circuit** (resistance should start low while filter caps charge, then rise to several hundred ohms or kilohms).

### Initial Power-Up
1. Reconnect the motherboard to the power supply and front panel.
2. Power on the unit with the top cover removed.
3. Touch the packages of `U53`, `U43`, and `U44` after 10–15 seconds: they should be slightly warm to the touch, **never hot**.
4. Confirm the splash screen displays **128 Voices**.

---

### Built-in EOS Hardware Diagnostics

EOS contains a hidden factory diagnostic suite that allows individual testing of the voice chips:

```
[ FRONT PANEL ]
      |
      v
  [ Master ]  -->  [ Utils ]  -->  [ Tests ]
                                       |
                                       v
                              [ Enter Password ]
                                       |
                                       v
                                    " 1358 "
                                       |
                                       v
                             [ Factory Diagnostics ]
```

1. Press the **`Master`** button.
2. Select **`Utils`** (Sub-menu).
3. Select **`Tests`**.
4. When prompted for a password, enter **`1358`** and press **`OK`**.
5. Available Diagnostic Routines:
   * **gRAM Test**: Tests sample memory address decoding and bus arbitration for both G-Chips (`U42` and `U53`).
   * **Voice Allocation / Output Test**: Cycles voices 1 through 128 individually, confirming that notes 65–128 trigger cleanly through `U53` and filter correctly through `U43`/`U44`.
   * **Jack Detect / DAC Routing**: Tests that audio output channels are cleanly addressed across the Sub and Main DACs.

---

### Real-World Polyphony Stress Test

To verify stability under real-world conditions:
1. Load or create a multi-sample preset with long release envelopes (e.g., a stereo piano or synth pad).
2. Set voice assignment to **Poly**.
3. Connect a MIDI sequencer or hold down the sustain pedal while sweeping the full keyboard range with continuous notes.
4. Watch the voice meter on the front panel display: confirm the voice counter exceeds 64 and reaches **128 voices** without voice-stealing, dropouts, or audio glitching.

---

## 7. Troubleshooting & Diagnostic Matrix

| Symptom | Probable Cause | Verification & Corrective Action |
| :--- | :--- | :--- |
| **Sampler boots normally, but still shows 64 voices** | `U53` not recognized by EOS bootloader; `G20CS2N` or `DTACKN` handshake open | 1. Check `R209` (3.92kΩ) pull-up resistor.<br>2. Inspect `U53` Pin 74 (`G20CS2N`) and Pin 24 (`DTACKN`) for cold joints or open pins.<br>3. Inspect ColdFire upper data bus leads `BD[31:16]` on `U53`. |
| **Sampler hangs or freezes on splash screen during boot** | Data bus bridge or address line shorted on `U53` | 1. Power off immediately.<br>2. Check for micro-solder bridges between adjacent pins on `BD[31:16]` and `BA[11:1]` at `U53`.<br>3. Use braid and flux to clear bridges. |
| **Shows 128 voices, but voices 65–128 are silent** | Audio interconnect disconnected between G-Chip #2 and H-Chips #2 & #3 | 1. Inspect Pin 83 (`G2SRCD0`) and Pin 84 (`G2SRCD1`) on `U53`.<br>2. Inspect Pin 67 (`SRCD`) on both `U43` and `U44`. |
| **Shows 128 voices, but voices 65–128 sound harsh/unfiltered** | H-Chips (`U43`/`U44`) not running filter algorithm or unpowered | 1. Check `R218` (3.92kΩ) pull-up resistor.<br>2. Inspect all pins of `U43` and `U44` under magnification.<br>3. Check 5V power and ground continuity on all H-chip power pins. |
| **System crashes or reboots under heavy polyphony load** | Missing or inadequate power decoupling capacitors | 1. Verify all 19 decoupling capacitors (7 for `U53`, 12 for `U43`/`U44`) are installed.<br>2. Check for dry joints on capacitor pads. High dynamic current draw during 128-voice playback requires full decoupling. |

---

## 8. Summary of Motherboard Locations

```
   +-----------------------------------------------------------------------------------------+
   |                              E5000 ULTRA REAR PANEL (I/O)                               |
   +-----------------------------------------------------------------------------------------+
   |                                                                                         |
   |   [ U60 ]           [ U54 ]             [ U43 ]           [ U44 ]                       |
   |  H-CHIP #1         H-CHIP #0           H-CHIP #2         H-CHIP #3                      |
   | (Voices 1-64)     (Voices 1-64)     (Voices 65-128)   (Voices 65-128)     [ R218 ]      |
   |                                                                          (3.92k Pullup) |
   |                                                                                         |
   |             [ U42 ]                               [ U53 ]                               |
   |         G-CHIP 2.0 #1                         G-CHIP 2.0 #2                             |
   |         (Voices 1-64)                        (Voices 65-128)                            |
   |                                                                                         |
   |           [ R208 ]                              [ R209 ]                                |
   |        (3.92k Pullup)                        (3.92k Pullup)                             |
   |                                                                                         |
   |                                                                                         |
   |   +-------------------+  +-------------------+  +-------------------+  +------------+   |
   |   |   SOUND SIMM 0    |  |   SOUND SIMM 1    |  |   SOUND SIMM 2    |  | SOUND SIMM3|   |
   |   +-------------------+  +-------------------+  +-------------------+  +------------+   |
   |                                                                                         |
   +-----------------------------------------------------------------------------------------+
   |                                 FRONT PANEL & LCD DISPLAY                               |
   +-----------------------------------------------------------------------------------------+
```

With `U53`, `U43`, and `U44` in place and all supporting passives installed, your E5000 Ultra is converted to the full 128-voice processing capacity of the flagship E4XT Ultra.
