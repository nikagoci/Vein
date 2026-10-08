# GymSplit· Spec v1

## Goal

Creating application where user can enter thier goal, experience level,
number of training days, available equipment and the application will
return training split based on the information.

Users: gym users who want a simple structured resistance-training plan.

## Acceptance criteria

- AC1 User can select a goal: muscle gain, fat loss, or general fitness.
- AC2 User can select an experience level: beginner or intermediate.
- AC3 User can select 3, 4, or 5 training days per week.
- AC4 User can select available equipment: full gym or limited equipment.
- AC5 Every training day contains at least 4 exercises with sets and
  repetition ranges.
- AC6 Generated exercises respect the user's selected equipment.
- AC7 Invalid inputs are rejected with a clear error message and the
  program asks the user to enter a valid value.

## Context the agent needs

spec.md · golden.md

## Constraints

command-line interface · standard library only · no database

## Out of scope

database · calorie/nutrition tracking ·
· mobile or web front end · medical advice

## Verification

The program is tested locally against the acceptance criteria.
3 golden questions pass (golden.md).

## First slice

Criteria: AC1, AC2, AC3, AC4

Done when: the program accepts the user's goal, experience level,
number of training days, and available equipment.

Not in this slice: AC5, AC6, AC7
