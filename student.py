"""Student Grade Management System.

Refactored version of test.py that follows PEP 8 and PEP 257 and
fulfills the user requirements of the Coding Standards workshop.
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
        """Create a student after validating the ID and the name."""
        self.student_id = self._validate_text(student_id, "Student ID")
        self.name = self._validate_text(name, "Student name")
        self.grades = []

    @staticmethod
    def _validate_text(value, field_name):
        """Return the value stripped, or raise ValueError if it is empty."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty text.")
        return value.strip()

    @staticmethod
    def _validate_grade(grade):
        """Return the grade as float, or raise an error if it is invalid."""
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            raise TypeError(f"Grade {grade!r} must be a number.")
        if not MIN_GRADE <= grade <= MAX_GRADE:
            raise ValueError(
                f"Grade {grade} must be between {MIN_GRADE} and {MAX_GRADE}."
            )
        return float(grade)

    def add_grade(self, grade):
        """Add a numeric grade between 0 and 100."""
        self.grades.append(self._validate_grade(grade))

    def calculate_average(self):
        """Return the average of the grades, or 0.0 if there are none."""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def get_letter_grade(self):
        """Return the letter grade (A-F) that matches the average."""
        average = self.calculate_average()
        for minimum, letter in LETTER_GRADE_THRESHOLDS:
            if average >= minimum:
                return letter
        return FAILING_LETTER

    def has_passed(self):
        """Return True if the average is 60 or higher."""
        return self.calculate_average() >= PASSING_AVERAGE

    def is_on_honor_roll(self):
        """Return True if the average is 90 or higher."""
        return self.calculate_average() >= HONOR_ROLL_AVERAGE

    def remove_grade_by_index(self, index):
        """Remove and return the grade at the given index."""
        if not isinstance(index, int) or not 0 <= index < len(self.grades):
            raise IndexError(
                f"Index {index} is out of range "
                f"(the student has {len(self.grades)} grades)."
            )
        return self.grades.pop(index)

    def remove_grade_by_value(self, value):
        """Remove the first grade equal to the given value."""
        grade = self._validate_grade(value)
        if grade not in self.grades:
            raise ValueError(f"Grade {grade} was not found.")
        self.grades.remove(grade)
        return grade

    def generate_report(self):
        """Return a formatted summary report of the student."""
        status = "Passed" if self.has_passed() else "Failed"
        honor_roll = "Yes" if self.is_on_honor_roll() else "No"
        lines = [
            "===== Student Summary Report =====",
            f"Student ID: {self.student_id}",
            f"Student Name: {self.name}",
            f"Number of Grades: {len(self.grades)}",
            f"Average Grade: {self.calculate_average():.2f}",
            f"Letter Grade: {self.get_letter_grade()}",
            f"Status: {status}",
            f"Honor Roll: {honor_roll}",
            "==================================",
        ]
        return "\n".join(lines)


def run_safely(action, *args):
    """Run an action and print a clear message instead of crashing."""
    try:
        return action(*args)
    except (TypeError, ValueError, IndexError) as error:
        print(f"Error: {error}")
        return None


def main():
    """Show the behavior of the system with valid and invalid inputs."""
    run_safely(Student, "", "Ana")
    run_safely(Student, "S001", "   ")

    student = Student("S001", "Ana Torres")
    for grade in (100, "Fifty", 105, 95.5, 88, 93.5):
        run_safely(student.add_grade, grade)

    run_safely(student.remove_grade_by_index, 5)
    run_safely(student.remove_grade_by_value, 50.0)
    print(student.generate_report())


if __name__ == "__main__":
    main()
