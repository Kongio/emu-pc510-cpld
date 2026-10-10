# E-mu PC510 (SK510 REV A) U10 CPLD Bench Test Guide

## 1. Power & Control Wiring (Mandatory for ALL tests)
- **VCC (+5V)**: Connect to **Pins 3, 15, 23, 35**
- **GND (0V)**: Connect to **Pins 10, 22, 30, 42**
- **UPCLRN / OE1 / OE2 (+5V)**: Connect **Pins 1, 2, 44** to **+5V** (Active-low reset negated / Outputs enabled).
  *(CRITICAL: If Pins 1, 2, 44 are left floating or grounded, all outputs remain in high-impedance / reset!)*
- **HWAITN (+5V)**: Connect **Pin 41** to **+5V** (No wait states requested).

---

## 2. Test 1: Data Buffer Enable (`BUFOEN`) Verification
- **Address Target**: `0x540000` (within `540000 - 5407FF`)
- **Inputs**:
  - `Pin 4 (EXPCSN)` -> **GND (0V)** (Card selected)
  - `Pin 19 (A13)` -> **GND (0V)**
  - `Pin 20 (A12)` -> **GND (0V)**
  - `Pin 17 (A11)` -> **GND (0V)**
  - `Pin 18 (A10)` -> **GND (0V)**
  - All other address pins (`A1..A9`) -> **GND (0V)**
- **Measure**:
  - **Pin 27 (`BUFOEN`)**: **EXPECT ~0V (LOW)** -> Data bus buffer enabled!
  - **Pin 38 (`CSHCHPN`)**: **EXPECT ~5V (HIGH)** -> Inactive
  - **Pin 32 (`WRPAGEN`)**: **EXPECT ~5V (HIGH)** -> Inactive (since `IOWRN` is high)

---

## 3. Test 2: Bus Isolation (`BUSISOLATE`) Range Verification
- **Address Target**: `0x540800` (within `540800 - 543FFF`)
- **Inputs**:
  - `Pin 4 (EXPCSN)` -> **GND (0V)**
  - `Pin 17 (A11)` -> **+5V** (Setting A11=1 moves into isolated range 0x540800+)
  - `Pin 19 (A13)` -> **GND (0V)**
  - `Pin 20 (A12)` -> **GND (0V)**
- **Measure**:
  - **Pin 27 (`BUFOEN`)**: **EXPECT ~5V (HIGH)** -> Buffer isolated!

---

## 4. Test 3: H-Chips Chip Select (`CSHCHPN`) Verification
- **Address Target**: `0x540400` (within `540400 - 5407FF`)
- **Inputs**:
  - `Pin 4 (EXPCSN)` -> **GND (0V)**
  - `Pin 19 (A13)` -> **GND (0V)**
  - `Pin 20 (A12)` -> **GND (0V)**
  - `Pin 17 (A11)` -> **GND (0V)**
  - `Pin 18 (A10)` -> **+5V** (A10=1 selects H-Chips!)
- **Measure**:
  - **Pin 38 (`CSHCHPN`)**: **EXPECT ~0V (LOW)** -> H-Chips selected!
  - **Pin 27 (`BUFOEN`)**: **EXPECT ~0V (LOW)** -> Buffer enabled!
  - **Pin 32 (`WRPAGEN`)**: **EXPECT ~5V (HIGH)** -> Inactive

---

## 5. Test 4: Write Page Register (`WRPAGEN`) Strobe Verification
- **Address Target**: `0x540000` (within `540000 - 5403FF`)
- **Inputs**:
  - `Pin 4 (EXPCSN)` -> **GND (0V)**
  - `Pin 19 (A13)` -> **GND (0V)**
  - `Pin 20 (A12)` -> **GND (0V)**
  - `Pin 17 (A11)` -> **GND (0V)**
  - `Pin 18 (A10)` -> **GND (0V)** (A10=0 selects Address Page Register)
  - `Pin 21 (IOWRN)` -> **GND (0V)** (Write strobe asserted)
- **Measure**:
  - **Pin 32 (`WRPAGEN`)**: **EXPECT ~0V (LOW)** -> Write strobe active!
  - Now change `Pin 21 (IOWRN)` -> **+5V**:
  - **Pin 32 (`WRPAGEN`)**: **EXPECT ~5V (HIGH)** (Rising edge latches data into U9!)

---

## 6. Test 5: Address Latch Pass-Through Verification
- **Inputs**:
  - `Pin 4 (EXPCSN)` -> **+5V** (Idle / transparent latch mode)
  - `Pin 6 (A1)` -> **+5V**
  - `Pin 8 (A2)` -> **GND (0V)**
  - `Pin 24 (RD)` -> **+5V**
- **Measure**:
  - **Pin 31 (`LA1`)**: **EXPECT ~5V (HIGH)**
  - **Pin 34 (`LA2`)**: **EXPECT ~0V (LOW)**
  - **Pin 37 (`LRD`)**: **EXPECT ~5V (HIGH)**
