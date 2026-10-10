# E-mu E5000 Ultra: 8-Output Hardware Upgrade Guide (Sub 2 & Sub 3 Addition)

A complete, component-level technical guide for upgrading the **E-mu E5000 Ultra** from factory 4-analog outputs (Main L/R, Sub 1 L/R) to the full **8-analog outputs** of the **E6400 Ultra** and **E4XT Ultra** by populating the onboard **Sub 2 (Outs 5 & 6)** and **Sub 3 (Outs 7 & 8)** output stages.

---

## 1. Executive Summary & Architecture

### Motherboard Commonality
All E-mu "Ultra" samplers—the **E5000 Ultra**, **E6400 Ultra**, and **E4XT Ultra**—share the exact same motherboard PCB: **`SK10485`** (Rev A.1 / D.2).

* **E6400 Ultra / E4XT Ultra**: Factory-populated with all 8 balanced analog outputs (4 stereo pairs: Main, Sub 1, Sub 2, Sub 3).
* **E5000 Ultra**: Factory-populated with only 4 analog outputs (Main L/R and Sub 1 L/R) to hit a lower budget price point. The pads, traces, and chassis cutouts for **Sub 2 Out (J5/J6)** and **Sub 3 Out (J7/J8)** are present on the motherboard but left unpopulated at the factory.

```
                     E-MU E4 ULTRA DIGITAL-TO-ANALOG AUDIO ARCHITECTURE (SK10485)
                                          
 +-------------------------------------------------------------------------------------------------------+
 |                                 ALTERA EPF6016 REPROGRAMMABLE FPGA (U45)                              |
 |                      Generates Master Clocks, Bit Clocks, and Serial Audio Streams                    |
 +-------------------------------------------------------------------------------------------------------+
          |                               |                               |                               |
     I2SDO_0 (Main)                  I2SDO_1 (Sub 1)                 I2SDO_2 (Sub 2)                 I2SDO_3 (Sub 3)
     I2SLR0, I2SBCK                  I2SLR1, I2SBCK                  I2SLR2, I2SBCK                  I2SLR3, I2SBCK
          |                               |                               |                               |
          v                               v                               v                               v
 +------------------+            +------------------+            +------------------+            +------------------+
 |  [U18] CS4329    |            |  [U20] CS4329    |            |  [U22] CS4329    |            |  [U24] CS4329    |
 |  20-bit DAC      |            |  20-bit DAC      |            |  20-bit DAC      |            |  20-bit DAC      |
 |  (MAIN L / R)    |            |  (SUB 1 L / R)   |            |  (SUB 2 L / R)   |            |  (SUB 3 L / R)   |
 +------------------+            +------------------+            +------------------+            +------------------+
          |                               |                               |                               |
     Differential                    Differential                    Differential                    Differential
     Audio Outputs                   Audio Outputs                   Audio Outputs                   Audio Outputs
          |                               |                               |                               |
          v                               v                               v                               v
 +------------------+            +------------------+            +------------------+            +------------------+
 |  [U1, U2] OP275  |            |  [U3, U4] OP275  |            |  [U5, U6] OP275  |            |  [U7, U8] OP275  |
 |  Active Filters  |            |  Active Filters  |            |  Active Filters  |            |  Active Filters  |
 |  & Diff Buffers  |            |  & Diff Buffers  |            |  & Diff Buffers  |            |  & Diff Buffers  |
 +------------------+            +------------------+            +------------------+            +------------------+
          |                               |                               |                               |
     Mute: Q1..Q4                    Mute: Q5..Q8                    Mute: Q9..Q12                   Mute: Q13..Q16
     (J109 JFETs)                    (J109 JFETs)                    (J109 JFETs)                    (J109 JFETs)
          |                               |                               |                               |
          v                               v                               v                               v
 +------------------+            +------------------+            +------------------+            +------------------+
 |  [J1, J2] 1/4"   |            |  [J3, J4] 1/4"   |            |  [J5, J6] 1/4"   |            |  [J7, J8] 1/4"   |
 |  MAIN OUTS (L/R) |            |  SUB 1 OUTS(L/R) |            |  SUB 2 OUTS(L/R) |            |  SUB 3 OUTS(L/R) |
 +------------------+            +------------------+            +------------------+            +------------------+
    [FACTORY POP]                   [FACTORY POP]                   [UPGRADE SECTION]               [UPGRADE SECTION]
                                                                        (Sheet 14)                      (Sheet 15)
```

### The Digital Audio Is Already Streaming
On all E-mu Ultra units running EOS, the Altera FPGA (`U45`, Sheet 16) **always serializes all four stereo audio streams** (`I2SDO_0`, `I2SDO_1`, `I2SDO_2`, `I2SDO_3`). The digital audio data and clocks are already pulsing across the motherboard traces to the empty pads of `U22` and `U24`. 

Once the missing DACs, op-amps, muting FETs, passives, and 1/4" phone jacks are soldered, Sub 2 and Sub 3 produce studio-grade analog audio immediately with zero firmware modification.

---

## 2. Complete Bill of Materials (BOM)

The upgrade spans three schematic sheets:
1. **Sheet 14 (`SK10485`)**: Sub Audio Out 2 Pair (J5 Left, J6 Right)
2. **Sheet 15 (`SK10485`)**: Sub Audio Out 3 Pair (J7 Left, J8 Right)
3. **Sheet 11 (`SK10485`)**: Jack Detection Circuitry (`RN10`, `RN12`, `RN13`)

---

### A. Integrated Circuits & Active Semiconductors

| Designators | Description | E-mu P/N | Package | Quantity | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`U22`, `U24`** | **Cirrus Logic CS4329-KS** | `II410` | SOIC-20 (Wide) | **2** | 20-bit Stereo Audio DAC (1 for Sub 2, 1 for Sub 3) |
| **`U5`, `U6`, `U7`, `U8`** | **Analog Devices OP275GS** | `IL361` | SOIC-8 | **4** | Dual Bipolar/JFET Audio Op-Amps (Differential filters) |
| **`Q9`, `Q10`, `Q11`, `Q12`, `Q13`, `Q14`, `Q15`, `Q16`** | **J109** (or MMBFJ109 / 2N5485) | — | SOT-23 (or TO-92) | **8** | N-Channel JFET audio muting switches (anti-pop) |
| **`D9`, `D10`, `D11`, `D12`, `D13`, `D14`, `D15`, `D16`** | **MMBZ15VAL** | — | SOT-23 | **8** | 15V Dual Common-Anode Zener / TVS ESD protection |

---

### B. Mechanical Hardware (Audio Jacks)

| Designators | Description | E-mu P/N | Footprint | Quantity | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`J5`, `J6`, `J7`, `J8`** | **1/4" Switched Stereo Phone Jack** | **`JA309`** | Through-hole PCB mount | **4** | Sub 2 L/R (`J5`/`J6`) & Sub 3 L/R (`J7`/`J8`) analog jacks |

*(E-mu Part `JA309`: Standard 1/4" switched TRS chassis jack, right-angle PCB pins with threaded nose and grounding bracket, as used across all E-mu samplers and modules).*

---

### C. Resistors (All 0805 SMD)

#### 1. Precision & Standard Resistors for Sub 2 & Sub 3 (50 Resistors Total)

| Quantity | Value | Tolerance | Designators (Sub 2 - Sheet 14) | Designators (Sub 3 - Sheet 15) | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2** | **10 Ω** | 5% | `R154` | `R159` | +5VA analog supply filter decoupling |
| **8** | **47 Ω** | 5% | `R54`, `R63`, `R66`, `R75` | `R78`, `R87`, `R90`, `R99` | Audio output protection series resistors |
| **8** | **560 Ω** | 5% | `R55`, `R64`, `R67`, `R76` | `R79`, `R88`, `R91`, `R100` | Op-amp output stage feedback & bias |
| **8** | **1.6 kΩ** | 5% | `R57`, `R60`, `R69`, `R72` | `R81`, `R84`, `R93`, `R96` | Low-pass filter input resistors |
| **8** | **3.92 kΩ** | **1%** | `R56`, `R65`, `R68`, `R77` | `R80`, `R89`, `R92`, `R101` | Active filter feedback resistors |
| **8** | **10.0 kΩ** | **1%** | `R59`, `R62`, `R71`, `R74` | `R83`, `R86`, `R95`, `R98` | Differential receiver bridge resistors |
| **8** | **16.5 kΩ** | **1%** | `R58`, `R61`, `R70`, `R73` | `R82`, `R85`, `R94`, `R97` | JFET gate pull-up / mute bias resistors |

---

### D. Capacitors (32 Capacitors Total)

| Quantity | Value | Type / Voltage | Designators (Sub 2 - Sheet 14) | Designators (Sub 3 - Sheet 15) | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **8** | **270 pF** | Ceramic NPO/C0G 50V (0805) | `C30`, `C33`, `C36`, `C39` | `C42`, `C45`, `C48`, `C51` | High-frequency active filter roll-off |
| **8** | **2200 pF** (2.2 nF) | Ceramic X7R 50V (0805) | `C31`, `C34`, `C37`, `C40` | `C43`, `C46`, `C49`, `C52` | Low-pass reconstruction filter |
| **12** | **0.1 µF** (100 nF) | Ceramic X7R 50V (0805) | `C29`, `C32`, `C35`, `C38`, `C80`, `C83` | `C41`, `C44`, `C47`, `C50`, `C88`, `C91` | $\pm 12\text{VA}$ and $+5\text{VA}$ power rail bypass |
| **4** | **1.0 µF** | Tantalum SMD (Case A/B, 25V) | `C81`, `C82` | `C86`, `C87` | DAC reference & analog bulk bypass |

---

### E. Resistor Networks for Jack Detection (Sheet 11)

> [!IMPORTANT]
> This is the single most critical step that distinguishes a factory-perfect installation from a malfunctioning one:
> * **`RN10`**: Factory-installed on the E5000 Ultra (`STUFF=NO_SUB23`). **MUST BE DESOLDERED & REMOVED**.
> * **`RN12` & `RN13`**: Factory-omitted on the E5000 Ultra (`STUFF=SUB23`). **MUST BE INSTALLED**.

| Network | Value / Type | E-mu P/N | Action on E5000 | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **`RN10`** | **4.7 kΩ $\times$ 4** (8-pin SMD concave/convex) | `RN348` | **DESOLDER & REMOVE** | Pulls unused jack lines high/low when Sub 2 & 3 are omitted |
| **`RN12`** | **4.7 kΩ $\times$ 4** (8-pin SMD concave/convex) | `RN348` | **SOLDER & INSTALL** | Connects `JKDET2`..`JKDET5` to jack switches on `J5`..`J8` |
| **`RN13`** | **4.7 kΩ $\times$ 4** (8-pin SMD concave/convex) | `RN348` | **SOLDER & INSTALL** | Pull-up biasing network for active jack insertion sensing |

---

## 3. Circuit Analysis: How the Output Stage Works

### 1. DAC Stage (`U22` and `U24`)
The **Cirrus Logic CS4329** is a 20-bit stereo delta-sigma digital-to-analog converter:
* Driven by FPGA audio clocks:
  * `FS512_B` on Pin 8 (`MCLK`): 24.576 MHz master clock (512 $\times$ 48 kHz).
  * `I2SBCK` on Pin 9 (`SCLK`): Serial bit clock.
  * `I2SLR2` / `I2SLR3` on Pin 7 (`LRCLK`): Word clock (48 kHz sample rate).
  * `I2SDO_2` / `I2SDO_3` on Pin 10 (`SDATA`): 20-bit serial audio data.
* Pin 11 (`AUTO_MUTE`): Drives active-low mute handshake `AUTOMUTEN` to prevent pops on sample rate changes or power glitches.
* Generates balanced differential voltage outputs on pins 17/18 (Left `AOUTL-`, `AOUTL+`) and pins 13/14 (Right `AOUTR-`, `AOUTR+`).

### 2. Low-Pass Filter & Differential-to-Single-Ended Stage (`U5`..`U8`)
Each channel uses one dual **OP275** operational amplifier:
* The first half acts as a balanced differential receiver, converting the CS4329’s differential voltage into a clean, ground-referenced single-ended signal while canceling common-mode DAC noise.
* The second half implements a 2nd-order active low-pass reconstruction filter (using the 270pF and 2200pF capacitors with 3.92kΩ/1.6kΩ feedback resistors) to eliminate out-of-band delta-sigma quantization noise.

### 3. Anti-Pop JFET Mute Circuit (`Q9`..`Q16`)
* The audio outputs are tied to ground through N-channel JFETs (`J109`).
* During power-up, power-down, or sample loading, the motherboard microprocessor asserts `FETMUTE` via supervisory circuit `U38`.
* The gates of the JFETs are pulled high through the 16.5kΩ resistors, turning the channels hard on and clamping the audio lines directly to ground.
* Once the analog rails ($\pm 12\text{VA}$) are stable and the DACs lock clock sync, `FETMUTE` goes low, reverse-biasing the JFET gates to high impedance and un-muting the outputs transparently.

### 4. Jack Sensing & Auto-Summing Logic
The 1/4" phone jacks (`JA309`) contain internal mechanical shunt switches:
* **No plug inserted**: The shunt switch contacts connect the jack detection lines to ground/bias. EOS detects the open jack and **automatically sums the submix into the Main L/R outputs**.
* **Plug inserted**: The sleeve/tip of the 1/4" phone plug physically lifts the contact, breaking the connection. The `JKDET` line transitions logic state.
* The octal buffer `U10` (`74VHCT244`, Sheet 11) drives this change onto the ColdFire data bus `BD[31:24]`.
* EOS senses the insertion and isolates the sub-channel, sending the audio exclusively out of the physical Sub 2 or Sub 3 jack!

---

## 4. Step-by-Step Rework & Installation Guide

### Phase 1: Rear Panel Chassis Preparation

1. **Unscrew and Remove the Top Cover**:
   * Remove the 6 chassis screws securing the top cover of the E5000 Ultra.
2. **Inspect the Rear Chassis Audio Port Openings**:
   * Next to `Sub 1 L/R`, locate the four factory-stamped holes for `Sub 2 L` (`J5`), `Sub 2 R` (`J6`), `Sub 3 L` (`J7`), and `Sub 3 R` (`J8`).
   * On most E5000 units, these holes are either covered by the rear panel vinyl decal or fitted with black plastic push-out plugs.
   * Carefully cut out the decal circles using a sharp X-Acto blade or push out the plastic plugs from the inside out to reveal the four clean 1/4" circular jack holes.

---

### Phase 2: Jack Detection Resistor Modification (Sheet 11)

1. Locate **`RN10`**, **`RN12`**, and **`RN13`** on the motherboard (located near `U10` and the Sub 1 output circuitry):
2. **Desolder `RN10`**:
   * Apply tacky flux across the 8 pins of `RN10`.
   * Using a hot air pencil or tweezer iron (or walking an iron tip between sides), carefully lift and remove `RN10`. Clean the pads flat with solder wick and IPA.
3. **Install `RN12` and `RN13`**:
   * Solder a **4.7 kΩ $\times$ 4** resistor network into footprint **`RN12`**.
   * Solder a **4.7 kΩ $\times$ 4** resistor network into footprint **`RN13`**.

---

### Phase 3: Soldering SMT Passives (Resistors & Capacitors)

Solder the low-profile 0805 components before the ICs and jacks to maintain easy iron access:

1. **Sub 2 Passives (Sheet 14 Area)**:
   * Solder resistor `R154` (10 Ω).
   * Solder resistors `R54`, `R63`, `R66`, `R75` (47 Ω).
   * Solder resistors `R55`, `R64`, `R67`, `R76` (560 Ω).
   * Solder resistors `R57`, `R60`, `R69`, `R72` (1.6 kΩ).
   * Solder resistors `R56`, `R65`, `R68`, `R77` (3.92 kΩ 1%).
   * Solder resistors `R59`, `R62`, `R71`, `R74` (10.0 kΩ 1%).
   * Solder resistors `R58`, `R61`, `R70`, `R73` (16.5 kΩ 1%).
   * Solder capacitors `C30`, `C33`, `C36`, `C39` (270 pF).
   * Solder capacitors `C31`, `C34`, `C37`, `C40` (2200 pF).
   * Solder capacitors `C29`, `C32`, `C35`, `C38`, `C80`, `C83` (0.1 µF).
   * Solder tantalum capacitors `C81`, `C82` (1.0 µF — **verify polarity stripe on positive terminal**).

2. **Sub 3 Passives (Sheet 15 Area)**:
   * Solder resistor `R159` (10 Ω).
   * Solder resistors `R78`, `R87`, `R90`, `R99` (47 Ω).
   * Solder resistors `R79`, `R88`, `R91`, `R100` (560 Ω).
   * Solder resistors `R81`, `R84`, `R93`, `R96` (1.6 kΩ).
   * Solder resistors `R80`, `R89`, `R92`, `R101` (3.92 kΩ 1%).
   * Solder resistors `R83`, `R86`, `R95`, `R98` (10.0 kΩ 1%).
   * Solder resistors `R82`, `R85`, `R94`, `R97` (16.5 kΩ 1%).
   * Solder capacitors `C42`, `C45`, `C48`, `C51` (270 pF).
   * Solder capacitors `C43`, `C46`, `C49`, `C52` (2200 pF).
   * Solder capacitors `C41`, `C44`, `C47`, `C50`, `C88`, `C91` (0.1 µF).
   * Solder tantalum capacitors `C86`, `C87` (1.0 µF — **verify polarity stripe**).

---

### Phase 4: Soldering Active SMT Semiconductors

1. **JFETs & Protection Diodes (SOT-23)**:
   * Solder `Q9`, `Q10`, `Q11`, `Q12` (`J109`) on Sheet 14.
   * Solder `Q13`, `Q14`, `Q15`, `Q16` (`J109`) on Sheet 15.
   * Solder `D9`, `D10`, `D11`, `D12` (`MMBZ15`) on Sheet 14.
   * Solder `D13`, `D14`, `D15`, `D16` (`MMBZ15`) on Sheet 15.

2. **Op-Amps (SOIC-8)**:
   * Align Pin 1 index dot and solder `U5` and `U6` (`OP275GS`) for Sub 2.
   * Align Pin 1 index dot and solder `U7` and `U8` (`OP275GS`) for Sub 3.

3. **Audio DACs (SOIC-20 Wide)**:
   * Align Pin 1 index notch/dot on `U22` (`CS4329-KS`) for Sub 2.
   * Align Pin 1 index notch/dot on `U24` (`CS4329-KS`) for Sub 3.
   * Tack corner pins, apply gel flux, and drag-solder both rows of 10 pins. Inspect with a loupe or microscope to ensure zero bridging between the 1.27mm pitch leads.

---

### Phase 5: Installing the 1/4" Phone Jacks (`J5`..`J8`)

1. Insert the four **`JA309`** 1/4" phone jacks into their through-hole footprint locations:
   * `J5` (Sub 2 Left), `J6` (Sub 2 Right)
   * `J7` (Sub 3 Left), `J8` (Sub 3 Right)
2. Ensure the threaded barrel of each jack extends through the circular rear chassis hole cleanly and sits flush with the rear panel.
3. Thread and hand-tighten the hex nuts onto the outside of the rear panel jacks to pull them firmly against the chassis before soldering. This prevents mechanical stress on the solder joints when cables are plugged in later.
4. Solder all through-hole pins on the component/solder side of the motherboard with ample solder to ensure solid structural and electrical connections.
5. Solder the chassis grounding tabs.
6. Clean the entire rework area with 99.9% IPA to remove all flux residue.

---

## 5. Verification & Built-in Hardware Diagnostics

### Pre-Power Cold Resistance Checks
Before applying AC power, use a digital multimeter in continuity / resistance mode:
* Check resistance between **`+12VA`** and **`AGND`** (across `C80` / `C88`): Must not be shorted.
* Check resistance between **`-12VA`** and **`AGND`** (across `C83` / `C91`): Must not be shorted.
* Check resistance between **`+5VA`** and **`AGND`** (across `C81` / `C86`): Must not be shorted.
* Check DC resistance from the **Tip and Ring** of each new jack (`J5`, `J6`, `J7`, `J8`) to ground: should read approximately 47 Ω (due to `R54`, `R63`, etc.) or higher.

---

### Built-in EOS Hardware Diagnostics

EOS features a dedicated hardware test suite that verifies both the DAC audio output and the mechanical jack detection switches:

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

1. Power on the sampler.
2. Press **`Master`** $\rightarrow$ **`Utils`** $\rightarrow$ **`Tests`**.
3. When prompted for the service password, enter **`1358`** and press **`OK`**.

#### 1. Interactive Jack Detection Test
* Select **`Jack Detect Test`**.
* The screen displays the status of all audio jacks:
  ```
  Main L: [OPEN]     Sub 1 L: [OPEN]     Sub 2 L: [OPEN]     Sub 3 L: [OPEN]
  Main R: [OPEN]     Sub 1 R: [OPEN]     Sub 2 R: [OPEN]     Sub 3 R: [OPEN]
  ```
* Plug a 1/4" cable into **Sub 2 Left (`J5`)**: The display should immediately change to `[CLOSED]` (or `[INSERTED]`).
* Unplug the cable: It should toggle back to `[OPEN]`.
* Repeat for **Sub 2 Right (`J6`)**, **Sub 3 Left (`J7`)**, and **Sub 3 Right (`J8`)**.
* **Pass criteria**: All four new jacks toggle reliably. If a jack does not toggle, verify `RN12`/`RN13` soldering or jack switch contacts.

#### 2. Audio Output DAC Sine Wave Test
* Select **`Audio Output Test`** (or **`DAC Test`**).
* Set output selection to **`Sub 2`** and press **`Play / Test`**: Verify a clean 1 kHz test tone from Sub 2 L and Sub 2 R on your studio monitors or audio interface.
* Set output selection to **`Sub 3`** and press **`Play / Test`**: Verify test tone from Sub 3 L and Sub 3 R.
* Verify there is zero audible distortion, noise floor is below -90 dB, and both left and right channels have balanced volume.

---

### Preset Voice Routing Test in EOS

1. Create or load a multi-sample preset.
2. In the preset editor, navigate to the **`Voice Routing`** (or **`Output`**) page.
3. Route Layer 1 to **`Sub 2`**. Play keys and confirm audio outputs exclusively from Sub 2 jacks.
4. Route Layer 2 to **`Sub 3`**. Play keys and confirm audio outputs exclusively from Sub 3 jacks.
5. Unplug the cables from Sub 2 and Sub 3: confirm EOS auto-sums the sound back into your Main outputs!

---

## 6. Troubleshooting & Fault Isolation Matrix

| Symptom | Probable Cause | Verification & Corrective Action |
| :--- | :--- | :--- |
| **Complete silence on Sub 2 or Sub 3** | DAC unpowered, missing clock, or held in mute | 1. Check +5VA on Pin 3 and Pin 18 of `U22`/`U24`.<br>2. Check `AUTOMUTEN` on Pin 11 of the DAC (must be HIGH ~5V during playback).<br>3. Check `FETMUTE` line at gates of `Q9..Q16` (must be LOW ~0V when unmuted).<br>4. Check `R154` / `R159` (10 Ω) supply resistor. |
| **Audio is distorted or clipped** | Op-amp missing $\pm 12\text{VA}$ power rail | 1. Measure Pin 8 of `U5..U8`: Must be **+12V DC**.<br>2. Measure Pin 4 of `U5..U8`: Must be **-12V DC**.<br>3. Inspect op-amp feedback resistors (3.92kΩ and 1.6kΩ) for cold solder joints. |
| **Output works, but audio always bleeds into Main mix even when plugged in** | `RN10` was not removed, or `RN12`/`RN13` not installed | 1. Verify `RN10` has been desoldered from Sheet 11.<br>2. Check solder joints on `RN12` and `RN13`.<br>3. Run Jack Detect Test (Password `1358`) to see which jack is failing to report insertion. |
| **Audio only plays out of Left or Right channel of a pair** | Single open lead on DAC output or op-amp pin | 1. Inspect solder joints on CS4329 pins 13/14 (Right) or pins 17/18 (Left).<br>2. Inspect corresponding op-amp inputs and 47 Ω output series resistor (`R54`, `R63`, etc.). |
| **Loud pop / thump through speakers when powering the sampler on or off** | Muting JFETs (`Q9..Q16`) not clamping audio during power transit | 1. Inspect J109 orientation (Source, Drain, Gate).<br>2. Check 16.5 kΩ gate bias resistors (`R58`, `R61`, `R70`, `R73`, etc.).<br>3. Ensure `FETMUTE` connects to all JFET gates. |
| **Excessive DC offset (>50 mV) measured across output jack** | Defective op-amp or leaking coupling/bypass capacitor | 1. Measure DC voltage from Tip to Sleeve with no audio playing (should be < 5 mV DC).<br>2. Replace op-amp if excessive DC offset persists. |

---

## 7. Motherboard Physical Component Map (Rear-Left Section)

```
   +-------------------------------------------------------------------------------------------------+
   |                                  REAR I/O PANEL JACK CONNECTORS                                 |
   |                                                                                                 |
   |   [ J1 / J2 ]         [ J3 / J4 ]                 [ J5 / J6 ]                 [ J7 / J8 ]       |
   |    MAIN OUTS           SUB 1 OUTS                  SUB 2 OUTS                  SUB 3 OUTS       |
   |  (Factory Pop)        (Factory Pop)             (UPGRADE SECTION)           (UPGRADE SECTION)   |
   |                                                                                                 |
   |   +----------+        +----------+              +---------------+           +---------------+   |
   |   | D1 .. D4 |        | D5 .. D8 |              |  D9 .. D12    |           |  D13 .. D16   |   |
   |   | Q1 .. Q4 |        | Q5 .. Q8 |              |  Q9 .. Q12    |           |  Q13 .. Q16   |   |
   |   +----------+        +----------+              +---------------+           +---------------+   |
   |                                                                                                 |
   |   [ U1, U2 ]           [ U3, U4 ]                  [ U5, U6 ]                  [ U7, U8 ]       |
   |   OP275 Dual           OP275 Dual                  OP275 Dual                  OP275 Dual       |
   |    Op-Amps              Op-Amps                     Op-Amps                     Op-Amps         |
   |                                                                                                 |
   |     [ U18 ]              [ U20 ]                     [ U22 ]                     [ U24 ]        |
   |   CS4329 DAC           CS4329 DAC                  CS4329 DAC                  CS4329 DAC       |
   |   (Main L/R)           (Sub 1 L/R)                 (Sub 2 L/R)                 (Sub 3 L/R)      |
   |                                                                                                 |
   |                                                                                                 |
   |                    +---------------------------------------------+                              |
   |                    |            JACK DETECT SECTION (SHEET 11)   |                              |
   |                    |                                             |                              |
   |                    |    [ U10 ] 74VHCT244 Octal Latch            |                              |
   |                    |    [ RN10 ] <-- DESOLDER & REMOVE           |                              |
   |                    |    [ RN12 ] <-- SOLDER & INSTALL (4.7k x 4) |                              |
   |                    |    [ RN13 ] <-- SOLDER & INSTALL (4.7k x 4) |                              |
   |                    +---------------------------------------------+                              |
   +-------------------------------------------------------------------------------------------------+
```

Once completed, your **E-mu E5000 Ultra** possesses the full **8-analog output stage** of the top-tier **E6400 Ultra** and **E4XT Ultra**. Combined with the **128-voice upgrade** and the **PC510 8-Output Expander**, your E5000 Ultra is capable of driving a massive **16 discrete balanced analog outputs**!
