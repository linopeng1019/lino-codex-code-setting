# CC Reduce Case

Use creduce to minimize a compiler test case that triggers an Internal Compiler Error (ICE).

## Arguments
- $ARGUMENTS: The full compiler command that triggers the ICE

## Instructions

1. **Parse the compiler command** from `$ARGUMENTS` to extract:
   - The compiler path (and -B flag if present)
   - The source file path (`.c` or `.cc` file)
   - All compiler flags
   - Identify `-march=` and `-mabi=` flags (these must always be preserved)

2. **Execute the original command** to capture the ICE error message:
   - Run the command and capture stderr
   - Extract the specific ICE error pattern (e.g., "internal compiler error: in XXX, at YYY")
   - This pattern will be used for the interestingness test

3. **Generate preprocessed source file**:
   - Run the compiler with `--save-temps -c` to generate preprocessed file
   - For `.c` files, this produces `.i` file
   - For `.cc`/`.cpp` files, this produces `.ii` file
   - Copy the preprocessed file to the current working directory
   - This ensures the test case is self-contained

4. **Minimize compiler flags**:
   - Start with all original flags (excluding `-o`, output file, and the original source file)
   - Those flags that must be preserved: `-march=*`, `-mabi=*`
   - For each other flag, try removing it one at a time:
     - Compile with the reduced flag set
     - Check if the same ICE pattern still occurs
     - If yes, the flag can be removed
     - If no, keep the flag
   - Build the minimal set of flags that still reproduces the ICE
   - Report which flags were removed and which were kept

5. **Set up the creduce environment**:
   - Create a `test.sh` interestingness test script that:
     - Uses absolute paths for the compiler and build directory
     - Uses the minimized flag set from step 4
     - Compiles with `-c -o /dev/null` (compile only, no linking)
     - Greps for the specific ICE error pattern
     - Returns 0 if the ICE is reproduced

6. **Write the test.sh script** with this template:
   ```bash
   #!/bin/bash

   # Interestingness test for creduce
   # Returns 0 if the compiler still crashes with the expected ICE

   <COMPILER> <MINIMIZED_FLAGS> <PREPROCESSED_FILENAME> -c -o /dev/null 2>&1 | \
       grep -q "<ICE_PATTERN>"
   ```

7. **Verify the interestingness test**:
   - Make test.sh executable with `chmod +x test.sh`
   - Run `./test.sh && echo "Exit code: $?"` to confirm it returns 0

8. **Run creduce**:
   - Execute: `creduce ./test.sh <preprocessed_file>`
   - Use a timeout of 600000ms (10 minutes) for the creduce process
   - Wait for creduce to complete

9. **Report the results**:
   - Show the reduced test case content
   - Verify the reduced case still triggers the same ICE
   - Report the reduction percentage (original size vs reduced size)
   - **Important**: Provide the simplified compilation command:
     ```
     <COMPILER> <MINIMIZED_FLAGS> <REDUCED_FILE> -c
     ```

## Example Usage

```
/cc-reduce-case /path/to/gcc -B/path/to/build -march=rv64gc -mabi=lp64d -O2 -std=gnu23 /path/to/test.c -o test.exe
```

## Example Output

After reduction, report should include:

```
## Reduced Test Case

<content of reduced file>

## Simplified Compilation Command

/path/to/gcc -B/path/to/build -march=rv64gc -mabi=lp64d -O2 reduced.i -c

## Flags Removed
- -fdiagnostics-plain-output (not needed for ICE)
- -mcmodel=medlow (not needed for ICE)

## Statistics
- Original size: 7451 bytes
- Reduced size: 128 bytes
- Reduction: 98.3%
```

## Notes

- Always use preprocessed files (`.i`/`.ii`) for creduce to ensure self-contained test cases
- The `-march=` and `-mabi=` flags are always preserved as they affect code generation
- The interestingness test must be deterministic
- For cross-compilers, ensure the test uses compile-only mode (`-c`) to avoid linking issues
- The reduced test case will be saved in the current working directory
