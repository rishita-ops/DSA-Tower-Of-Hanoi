# DSA — Tower of Hanoi

A focused Python implementation of the **classic Tower of Hanoi puzzle** that **prints the complete optimal sequence of moves** to transfer a stack of disks from one rod to another, using a **single loop and bit operations instead of recursion**. Clean, minimal, and correct — this solution is the entry point to understanding the **2ⁿ − 1 move count**, the **ruler pattern** behind which disk moves, and the link between **recursion and binary numbers**. Tower of Hanoi is one of the most reused examples for teaching recursion, divide and conquer, and exponential growth.

---

## Problem Statement

You are given **three rods** named `A`, `B`, and `C`, and `n` disks of different sizes. All disks start stacked on rod `A`, with the largest at the bottom and the smallest at the top.

Move the entire stack from rod `A` to rod `C`, following these rules:

1. Only **one disk** can be moved at a time.
2. Only the **top disk** of a rod can be picked up.
3. A **larger disk can never be placed on top of a smaller disk**.

Print the **total number of moves** and every move in order. The minimum number of moves is always **2ⁿ − 1**.

**Example 1:**

```
Input:  num_disks = 1
Output: Total moves required: 1
        Move #1: Move disk 1 from Rod A to Rod C
Explanation: With a single disk, one direct move is enough.
```

**Example 2:**

```
Input:  num_disks = 2
Output: Total moves required: 3
        Move #1: Move disk 1 from Rod A to Rod B
        Move #2: Move disk 2 from Rod A to Rod C
        Move #3: Move disk 1 from Rod B to Rod C
Explanation: The small disk steps aside to rod B, the large disk goes to rod C,
and the small disk is placed on top of it.
```

**Example 3:**

```
Input:  num_disks = 3
Output: Total moves required: 7
        Move #1: Move disk 1 from Rod A to Rod C
        Move #2: Move disk 2 from Rod A to Rod B
        Move #3: Move disk 1 from Rod C to Rod B
        Move #4: Move disk 3 from Rod A to Rod C
        Move #5: Move disk 1 from Rod B to Rod A
        Move #6: Move disk 2 from Rod B to Rod C
        Move #7: Move disk 1 from Rod A to Rod C
Explanation: The top two disks are first parked on rod B, the largest disk moves
to rod C, and the two disks are then rebuilt on top of it.
```

**Constraints for this program:**

- `num_disks` is a non-negative integer
- The number of printed lines is `2^num_disks − 1`, so the practical limit is about `num_disks <= 20` (around one million lines)

**Start and goal for 3 disks:**

```
START                                   GOAL
    ███           │            │            │            │           ███
   █████          │            │            │            │          █████
  ███████         │            │            │            │         ███████
───────────  ───────────  ───────────  ───────────  ───────────  ───────────
     A            B            C            A            B            C
```

---

## The Code

```python
num_disks = int(input("Enter the number of disks: "))

total_moves = 2**num_disks - 1

print(f"\nTotal moves required: {total_moves}\n")

for move in range(1, total_moves + 1):
    disk = 1
    temp_move = move
    while temp_move % 2 == 0:
        disk += 1
        temp_move //= 2

    source_idx = (move & (move - 1)) % 3
    dest_idx = ((move | (move - 1)) + 1) % 3

    rods = ["A", "B", "C"]

    if num_disks % 2 == 0:
        if rods[source_idx] == "B":
            from_rod = "C"
        elif rods[source_idx] == "C":
            from_rod = "B"
        else:
            from_rod = "A"

        if rods[dest_idx] == "B":
            to_rod = "C"
        elif rods[dest_idx] == "C":
            to_rod = "B"
        else:
            to_rod = "A"
    else:
        from_rod = rods[source_idx]
        to_rod = rods[dest_idx]

    print(f"Move #{move}: Move disk {disk} from Rod {from_rod} to Rod {to_rod}")

print("\nAll disks have been successfully moved!")
```

---

## The Critical Idea — Every Move Is Decided by Its Number Alone

This is the most important thing to understand about this solution.

The usual solution is **recursive**: move `n − 1` disks out of the way, move the largest disk, then move the `n − 1` disks back on top. This program never simulates the rods at all. Instead, it uses one fact: **the move number `move` already tells you which disk moves and between which rods.** The loop simply counts from `1` to `2ⁿ − 1` and reads the answer out of the bits of that number.

**Which disk moves — the ruler pattern.** The disk moved at step `move` is `1 +` the number of trailing zeros in the binary form of `move`:

```
move:    1    2    3    4    5    6    7    8
binary:  001  010  011  100  101  110  111  1000
zeros:   0    1    0    2    0    1    0    3
disk:    1    2    1    3    1    2    1    4
```

The sequence `1 2 1 3 1 2 1 4 …` looks like the markings on a ruler: the smallest disk moves every other step, the next disk every fourth step, and so on.

| Line of code                     | What it does                                                        |
| -------------------------------- | ------------------------------------------------------------------- |
| `while temp_move % 2 == 0`       | Counts trailing zeros of `move` by halving until it becomes odd     |
| `disk += 1`                      | Each trailing zero means the next larger disk is the one that moves |
| `(move & (move - 1)) % 3`        | Gives the index of the **source** rod                               |
| `((move \| (move - 1)) + 1) % 3` | Gives the index of the **destination** rod                          |
| `if num_disks % 2 == 0` block    | Swaps rods `B` and `C` when the disk count is even                  |

**Why the swap for even disk counts:** the smallest disk always travels in a fixed cycle. With an odd number of disks it goes `A → C → B → A`, and with an even number it goes `A → B → C → A`, so that the whole tower ends on rod `C` either way. The bit formulas produce the odd-case cycle, and swapping `B` and `C` turns it into the even-case cycle.

Because no rod contents are stored, the program needs **no stack, no recursion, and no list of disks**.

---

## How the Loop Works

```python
for move in range(1, total_moves + 1):
    disk = 1
    temp_move = move
    while temp_move % 2 == 0:
        disk += 1
        temp_move //= 2

    source_idx = (move & (move - 1)) % 3
    dest_idx = ((move | (move - 1)) + 1) % 3
    ...
    print(f"Move #{move}: Move disk {disk} from Rod {from_rod} to Rod {to_rod}")
```

- **Count:** `move` runs from `1` to `2ⁿ − 1`, one value per required move
- **Find the disk:** `temp_move` is a copy of `move` that is halved while it is even, and `disk` grows by one each time
- **Find the rods:** two bit expressions give the source and destination rod indices (`0`, `1`, `2` for `A`, `B`, `C`)
- **Correct for parity:** when `num_disks` is even, `B` and `C` are exchanged
- **Print:** one line per move in the same format every time
- **Result:** after the loop, the whole stack has moved from `A` to `C`

> **Why `temp_move` and not `move`:** the loop divides the number it is counting trailing zeros of. If it divided `move` itself, the bit formulas further down would be computed on the wrong value. The copy keeps `move` intact for them.

> **A common mistake this code avoids:** using `move % 3` for the rods. The rod pattern does not follow the move number directly. It follows the bits of `move & (move - 1)` (the number with its lowest set bit removed) and `move | (move - 1)` (the number with its trailing zeros turned into ones).

---

## Algorithm (Pseudocode)

```
read n
total = 2^n - 1
print total

for each move m from 1 to total:
    disk = 1 + (number of trailing zeros in m)
    source = (m AND (m - 1)) mod 3
    dest   = ((m OR (m - 1)) + 1) mod 3

    if n is even:
        swap the meaning of rods B and C

    print "Move disk <disk> from <source> to <dest>"

print "All disks have been successfully moved!"
```

---

## Dry Run

**Input:** `num_disks = 3` (odd, so no rod swapping)

| `move` | Binary | `disk` | `move & (move-1)` → source | `(move \| (move-1)) + 1` → dest | Printed move  |
| ------ | ------ | ------ | -------------------------- | ------------------------------- | ------------- |
| 1      | `001`  | 1      | `0 % 3 = 0` → **A**        | `2 % 3 = 2` → **C**             | Disk 1: A → C |
| 2      | `010`  | 2      | `0 % 3 = 0` → **A**        | `4 % 3 = 1` → **B**             | Disk 2: A → B |
| 3      | `011`  | 1      | `2 % 3 = 2` → **C**        | `4 % 3 = 1` → **B**             | Disk 1: C → B |
| 4      | `100`  | 3      | `0 % 3 = 0` → **A**        | `8 % 3 = 2` → **C**             | Disk 3: A → C |
| 5      | `101`  | 1      | `4 % 3 = 1` → **B**        | `6 % 3 = 0` → **A**             | Disk 1: B → A |
| 6      | `110`  | 2      | `4 % 3 = 1` → **B**        | `8 % 3 = 2` → **C**             | Disk 2: B → C |
| 7      | `111`  | 1      | `6 % 3 = 0` → **A**        | `8 % 3 = 2` → **C**             | Disk 1: A → C |

**State of the rods after each move** (stacks listed bottom to top):

| After move | Rod A | Rod B | Rod C |
| ---------- | ----- | ----- | ----- |
| Start      | 3 2 1 | —     | —     |
| 1          | 3 2   | —     | 1     |
| 2          | 3     | 2     | 1     |
| 3          | 3     | 2 1   | —     |
| 4          | —     | 2 1   | 3     |
| 5          | 1     | 2     | 3     |
| 6          | 1     | —     | 3 2   |
| 7          | —     | —     | 3 2 1 |

**Output:** `7` moves, with all three disks on rod `C` ✅

Note that a larger disk is **never** placed on a smaller one at any point in the table. The bit formulas never need to check this rule, because the sequence they generate respects it by construction.

**Input:** `num_disks = 2` (even, so `B` and `C` are swapped)

| `move` | `disk` | Raw source → dest | After swapping B and C | Printed move  |
| ------ | ------ | ----------------- | ---------------------- | ------------- |
| 1      | 1      | A → C             | A → B                  | Disk 1: A → B |
| 2      | 2      | A → B             | A → C                  | Disk 2: A → C |
| 3      | 1      | C → B             | B → C                  | Disk 1: B → C |

**Output:** `3` moves, with both disks on rod `C` ✅

---

## Complexity Analysis

| Metric | Complexity                                                                                            |
| ------ | ----------------------------------------------------------------------------------------------------- |
| Time   | **O(2ⁿ)** — the loop runs `2ⁿ − 1` times, and the inner `while` loop averages about one step per move |
| Space  | **O(1)** — only a few integer and string variables, no recursion stack and no rod contents            |

The `2ⁿ − 1` moves are not a weakness of this code: that many moves **must** be printed, so no solution can do better than **O(2ⁿ)** time. The trailing-zero loop is cheap because half of all numbers have zero trailing zeros, a quarter have one, and so on, which adds up to about one iteration per move on average.

The recursive version below has the same time complexity but needs **O(n)** space for its call stack.

---

## Edge Cases

| Scenario                        | Behavior                                                                                        |
| ------------------------------- | ----------------------------------------------------------------------------------------------- |
| `0` disks                       | `total_moves` is `0`, the loop never runs — prints the total and the success message ✅         |
| `1` disk                        | One move: `A → C` ✅                                                                            |
| `2` disks (even)                | `B` and `C` are swapped — `A → B`, `A → C`, `B → C` ✅                                          |
| `3` disks (odd)                 | No swap — seven moves ending on rod `C` ✅                                                      |
| Large input such as `20`        | Prints `1,048,575` moves — works, but the output is huge ✅                                     |
| Very large input such as `64`   | `2⁶⁴ − 1` moves — Python integers do not overflow, but the loop would never finish ⚠️           |
| Negative number such as `-1`    | `2**-1` becomes a float, a meaningless total is printed, then `range()` raises a `TypeError` ❌ |
| Non-numeric input such as `abc` | `int()` raises a `ValueError` ❌                                                                |

---

## Code-Quality Notes

**This is a script with no input checks.** The program reads with `input()` and prints at the top level. Negative numbers and text crash it, as shown above. A small guard fixes this:

```python
if num_disks < 0:
    print("Number of disks cannot be negative.")
    raise SystemExit
```

**The rod swap can be shorter.** The two `if / elif / else` chains do the same job as a dictionary lookup:

```python
swap = {"A": "A", "B": "C", "C": "B"}
from_rod = swap[rods[source_idx]] if num_disks % 2 == 0 else rods[source_idx]
```

**`rods` is rebuilt on every iteration.** The list `["A", "B", "C"]` never changes, so it can be defined once before the loop.

**Trailing zeros have a one-line form.** The `while` loop can be replaced by `disk = (move & -move).bit_length()`, which isolates the lowest set bit and reads off its position.

**Output order matters.** The program prints the moves but never checks them. To verify correctness, simulate three lists (one per rod) and assert that no larger disk is ever placed on a smaller one.

---

## The Natural Extension — The Recursive Solution

The standard way to solve Tower of Hanoi is recursion: to move `n` disks from `source` to `target`, first move `n − 1` disks to the spare rod, then move disk `n`, then move the `n − 1` disks from the spare rod onto the target.

```python
def hanoi(n, source, target, spare):
    if n == 0:
        return
    hanoi(n - 1, source, spare, target)
    print(f"Move disk {n} from Rod {source} to Rod {target}")
    hanoi(n - 1, spare, target, source)

num_disks = int(input("Enter the number of disks: "))
print(f"\nTotal moves required: {2**num_disks - 1}\n")
hanoi(num_disks, "A", "C", "B")
print("\nAll disks have been successfully moved!")
```

**Trace for `hanoi(2, "A", "C", "B")`:**

| Call                        | Action                              | Printed move  |
| --------------------------- | ----------------------------------- | ------------- |
| `hanoi(2, A, C, B)`         | Move 1 disk from A to B first       | —             |
| `hanoi(1, A, B, C)`         | Base case work: print disk 1        | Disk 1: A → B |
| back in `hanoi(2, A, C, B)` | Move the largest disk               | Disk 2: A → C |
| `hanoi(1, B, C, A)`         | Move the small disk onto the target | Disk 1: B → C |

**Result:** the same three moves as the iterative program ✅ — for every `n`, both versions print exactly the same sequence.

| Property                   | Iterative bit-trick (this code) | Recursive version             |
| -------------------------- | ------------------------------- | ----------------------------- |
| Time                       | O(2ⁿ)                           | O(2ⁿ)                         |
| Extra space                | **O(1)**                        | O(n) call stack               |
| Recursion limit risk       | ❌ None                         | Only for very large `n`       |
| Easy to read and explain   | ❌ Needs bit knowledge          | ✅ Mirrors the problem itself |
| Matches the puzzle's logic | Indirectly                      | ✅ Directly                   |
| When to use                | Learning bit patterns           | Interviews and teaching       |

---

## Repository Structure

```
DSA-Tower-of-Hanoi/
│
├── tower_of_hanoi.py    # Main Python implementation
└── README.md            # Project documentation
```

---

## How to Compile and Run

**Prerequisites:** Python 3.8+

```bash
# Clone the repository
git clone https://github.com/<your-username>/DSA-Tower-of-Hanoi.git
cd DSA-Tower-of-Hanoi

# Run
python3 tower_of_hanoi.py
```

**On Windows:**

```bash
python tower_of_hanoi.py
```

**Sample session:**

```
Enter the number of disks: 3

Total moves required: 7

Move #1: Move disk 1 from Rod A to Rod C
Move #2: Move disk 2 from Rod A to Rod B
Move #3: Move disk 1 from Rod C to Rod B
Move #4: Move disk 3 from Rod A to Rod C
Move #5: Move disk 1 from Rod B to Rod A
Move #6: Move disk 2 from Rod B to Rod C
Move #7: Move disk 1 from Rod A to Rod C

All disks have been successfully moved!
```

---

## Key Concepts Covered

- **Recursion, unrolled** — the recursive solution rewritten as a plain loop
- **Minimum move count** — exactly `2ⁿ − 1` moves, which doubles (plus one) with every extra disk
- **Ruler pattern** — the disk moved at step `m` is `1 +` the trailing zeros of `m`
- **Bit tricks** — `move & (move - 1)` and `move | (move - 1)` locate the rods
- **Parity of `n`** — odd and even disk counts rotate the smallest disk in opposite directions
- **Rod swapping** — exchanging `B` and `C` for even `n` so the tower always ends on `C`
- **Constant space** — no stack and no rod simulation
- **Exponential growth** — why large inputs are impractical, whatever the language

---

## Why This Problem Matters in DSA

Tower of Hanoi is the textbook example for recursion, and its bit-pattern solution connects directly to many other problems:

| Problem / Concept                                 | Connection                                                             |
| ------------------------------------------------- | ---------------------------------------------------------------------- |
| **Hanota (Tower of Hanoi)** (LeetCode LCCI 08.06) | The same puzzle, solved with the recursive approach                    |
| **Gray Code** (LeetCode #89)                      | Another sequence generated from the step number using bit operations   |
| **Subsets** (LeetCode #78)                        | Another `2ⁿ`-sized output, built by recursion or by counting in binary |
| **Power of Two** (LeetCode #231)                  | Bit-level reasoning about powers of two, as in `2ⁿ − 1`                |
| **Climbing Stairs** (LeetCode #70)                | A classic recurrence that grows by combining smaller subproblems       |
| **Divide and conquer** (concept)                  | Splitting a problem into smaller copies of itself, as `n → n − 1` here |

Every problem that breaks a big task into smaller identical tasks traces back to the recursive idea introduced here.

---

## Contributing

Contributions are welcome. Consider adding:

- The **recursive version** as a separate, runnable file
- A version that **simulates the three rods** and verifies that no rule is broken
- A version that **prints the rods after every move** for visualization
- A version using a **dictionary** for the rod swap
- Input validation and tests for tricky inputs such as `0`, `1`, `2`, and negative numbers
- Implementations in C++, Java, or JavaScript

```bash
git checkout -b feature/your-feature
git commit -m "Add: your feature description"
git push origin feature/your-feature
# Then open a Pull Request
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

_Part of a structured DSA practice series — fundamentals, done right._
