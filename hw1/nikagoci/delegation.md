# GymSplit · Delegation Log

## Task 1 — Project specification

Delegated to: ChatGPT

Task:
Help define the GymSplit project and create a concise specification
including the goal, acceptance criteria, constraints, out-of-scope
items, verification method, and first implementation slice.

Verification:
Reviewed the proposed specification and adjusted it to match the
requirements of the homework and the intended GymSplit functionality.

Result:
The final specification was created in spec.md.

## Task 2 — Golden questions

Delegated to: ChatGPT

Task:
Create three golden questions that test the main functionality of
GymSplit and map them to the acceptance criteria.

Verification:
Reviewed each question and checked that the expected result could
be objectively tested against the acceptance criteria.

Result:
Three golden questions were created in golden.md:

1. Basic workout generation
2. Different user configuration
3. Invalid input

## Task 3 — Python implementation

Delegated to: ChatGPT

Task:
Implement the GymSplit command-line application in Python based on
the requirements in spec.md.

The implementation needed to:

- accept the user's goal
- accept the user's experience level
- accept 3, 4, or 5 training days
- accept the available equipment
- generate a workout split
- provide at least 4 exercises per training day
- respect limited-equipment restrictions
- reject invalid input

Verification:
The generated Python program was run with the three golden-question
scenarios. The output was checked against the expected results and
the acceptance criteria.

Result:
The application successfully generated the requested workout plans,
respected limited-equipment restrictions, and rejected invalid
training-day input.

## Task 4 — Testing and debugging

Delegated to: ChatGPT

Task:
Help run and verify the GymSplit implementation against the three
golden questions.

Verification:
The program was executed with:

- beginner + muscle gain + 4 days + full gym
- intermediate + fat loss + 3 days + limited equipment
- invalid training days followed by a valid input

Result:
All three tests passed.
