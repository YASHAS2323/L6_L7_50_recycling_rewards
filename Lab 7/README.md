# Lab 7: Fuzz testing with Hypothesis

This lab hardens the recycling rewards processor with property-based tests.
It reuses the three recycling functions already present in Lab 6 while keeping
the Lab 7 application and tests separate.

## Setup and run

From this folder, create an isolated environment, install the dependencies,
then run:

```powershell
python -m venv .venv-lab7
.venv-lab7\Scripts\python.exe -m pip install -r requirements.txt
.venv-lab7\Scripts\python.exe processor.py
.venv-lab7\Scripts\python.exe -m pytest -q test_processor.py
```

The tests check generated valid inputs, boundary behavior, and invalid input
types and values for all three functions. Invalid types raise `TypeError`;
invalid values raise `ValueError`.

## Deliverables

- `processor.py`: the input-validated application script.
- `test_processor.py`: Hypothesis property tests and validation examples.
- `evidence/`: screenshots documenting the initial failing fuzz run and the
  final application and test runs.
- `Lab7_FuzzTesting_Evidence.pdf`: compiled screenshot report.
