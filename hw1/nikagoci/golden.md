# GymSplit · Golden Questions

## GQ1 — Basic workout generation

### Question

A beginner wants to build muscle, trains 4 days per week,
and has access to a full gym. What workout split does GymSplit
generate?

### Expected result

The application accepts all four inputs and returns a valid
4-day workout split for a beginner focused on muscle gain.

The generated plan should contain workouts corresponding to
the selected 4 training days.

### Acceptance criteria tested

AC1, AC2, AC3, AC4

## GQ2 — Different user configuration

### Question

An intermediate user wants to lose fat, trains 3 days per week,
and has access only to limited equipment. What workout split does
GymSplit generate?

### Expected result

The application accepts the selected goal, experience level,
training days, and equipment and returns a valid 3-day workout split.
The returned workout split has at least 4 exercises on each training day.
The workouts which needs gym equipment are not included.

### Acceptance criteria tested

AC1, AC2, AC3, AC4, AC5, AC6

## GQ3 — Invalid input

### Question

What happens when a user enters an invalid number of training days,
such as 7?

### Expected result

The application does not accept the invalid value and displays
a clear error message asking the user to enter a valid number
of training days.

### Acceptance criteria tested

AC3, AC7
