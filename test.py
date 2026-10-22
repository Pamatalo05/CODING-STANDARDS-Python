"""Student Grade Management System.

This module manages student records: it stores grades, calculates the
average, converts it to a letter grade, determines the pass/fail and
honor roll status, and generates a formatted summary report.
"""

MIN_GRADE = 0.0
MAX_GRADE = 100.0
PASSING_AVERAGE = 60.0
HONOR_ROLL_AVERAGE = 90.0
LETTER_GRADE_THRESHOLDS = (
    (90.0, "A"),
    (80.0, "B"),
    (70.0, "C"),
    (60.0, "D"),
)
FAILING_LETTER = "F"


class Student:
    """Represent a student with an ID, a name and a list of grades."""

    def __init__(self, student_id, name):
        """Create a student after validating that ID and name are not empty."""
        self.student_id = self._validate_text(student_id, "Student ID")
        self.name = self._validate_text(name, "Student name")
        self.grades = []

    @staticmethod
    def _validate_text(value, field_name):
        """Return the stripped text or raise ValueError if it is empty."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty text.")
        return value.strip()

    @staticmethod
    def _validate_grade(grade):
        """Return the grade as float or raise an error if it is invalid."""
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            raise TypeError(f"Grade '{grade}' must be a number.")
        if not MIN_GRADE <= grade <= MAX_GRADE:
            raise ValueError(
                f"Grade {grade} must be between {MIN_GRADE} and {MAX_GRADE}."
            )
        return float(grade)

    def add_grade(self, grade):
        """Add a numeric grade in the 0-100 range."""
        self.grades.append(self._validate_grade(grade))

    def calculate_average(self):
        """Return the average of the grades, or 0.0 if there are none."""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def get_letter_grade(self):
        """Convert the average grade into a letter grade (A-F)."""
        average = self.calculate_average()
        for threshold, letter in LETTER_GRADE_THRESHOLDS:
            if average >= threshold:
                return letter
        return FAILING_LETTER

    def has_passed(self):
        """Return True if the average is 60 or higher."""
        return self.calculate_average() >= PASSING_AVERAGE

    def is_on_honor_roll(self):
        """Return True if the average is 90 or higher."""
        return self.calculate_average() >= HONOR_ROLL_AVERAGE

    def remove_grade_by_value(self, value):
        """Remove the first grade equal to the given value."""
        grade = self._validate_grade(value)
        if grade not in self.grades:
            raise ValueError(f"Grade {grade} was not found.")
        self.grades.remove(grade)

    def remove_grade_by_index(self, index):
        """Remove and return the grade at the given position."""
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError(f"Index '{index}' must be an integer.")
        if not 0 <= index < len(self.grades):
            raise IndexError(
                f"Index {index} is out of range "
                f"(the student has {len(self.grades)} grades)."
            )
        return self.grades.pop(index)

    def generate_report(self):
        """Return a formatted summary report of the student."""
        passed_text = "Passed" if self.has_passed() else "Failed"
        honor_text = "Yes" if self.is_on_honor_roll() else "No"
        return (
            "===== Student Summary Report =====\n"
            f"Student ID     : {self.student_id}\n"
            f"Student Name   : {self.name}\n"
            f"Number of Grades: {len(self.grades)}\n"
            f"Average Grade  : {self.calculate_average():.2f}\n"
            f"Letter Grade   : {self.get_letter_grade()}\n"
            f"Status         : {passed_text}\n"
            f"Honor Roll     : {honor_text}\n"
            "=================================="
        )


def run_safely(action, *args):
    """Run an action and show a clear message instead of crashing."""
    try:
        return action(*args)
    except (TypeError, ValueError, IndexError) as error:
        print(f"Error: {error}")
        return None


def main():
    """Demonstrate every requirement, including invalid inputs."""
    run_safely(Student, "", "No Name")
    run_safely(Student, "S002", "   ")

    student = run_safely(Student, "S001", "Ana Torres")
    if student is None:
        return

    for grade in (95.0, 88.5, 72.5, 100, "Fifty", 105, -3):
        run_safely(student.add_grade, grade)

    run_safely(student.remove_grade_by_index, 5)
    run_safely(student.remove_grade_by_value, 50.0)
    run_safely(student.remove_grade_by_value, 72.5)
    run_safely(student.remove_grade_by_index, 0)

    print(student.generate_report())


if __name__ == "__main__":
    main()