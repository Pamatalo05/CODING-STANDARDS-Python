"""Unit tests for the Student Grade Management System."""

import unittest

from student import Student


class StudentTest(unittest.TestCase):
    """Check every user requirement of the Student class."""

    def setUp(self):
        """Create a student with three valid grades."""
        self.student = Student("S001", "Ana Torres")
        for grade in (95.0, 72.5, 88):
            self.student.add_grade(grade)

    def test_create_student(self):
        """A student is created with a valid ID and name."""
        self.assertEqual(self.student.student_id, "S001")
        self.assertEqual(self.student.name, "Ana Torres")

    def test_invalid_id_and_name(self):
        """Empty ID or name is rejected."""
        with self.assertRaises(ValueError):
            Student("", "Ana")
        with self.assertRaises(ValueError):
            Student("S002", "   ")

    def test_invalid_grades(self):
        """Text, booleans and values outside 0-100 are rejected."""
        with self.assertRaises(TypeError):
            self.student.add_grade("Fifty")
        with self.assertRaises(TypeError):
            self.student.add_grade(True)
        with self.assertRaises(ValueError):
            self.student.add_grade(105)
        with self.assertRaises(ValueError):
            self.student.add_grade(-1)

    def test_average(self):
        """The average is the mean of the grades, 0.0 when empty."""
        self.assertAlmostEqual(self.student.calculate_average(), 85.1666, 3)
        self.assertEqual(Student("S003", "Luis").calculate_average(), 0.0)

    def test_letter_grade(self):
        """The letter grade follows the A-F ranges."""
        expected = {95: "A", 85: "B", 75: "C", 65: "D", 40: "F"}
        for grade, letter in expected.items():
            student = Student("S004", "Eva")
            student.add_grade(grade)
            self.assertEqual(student.get_letter_grade(), letter)

    def test_pass_fail(self):
        """A student passes with an average of 60 or more."""
        self.assertTrue(self.student.has_passed())
        student = Student("S005", "Leo")
        student.add_grade(59.9)
        self.assertFalse(student.has_passed())

    def test_honor_roll(self):
        """The honor roll is a boolean for averages of 90 or more."""
        self.assertFalse(self.student.is_on_honor_roll())
        student = Student("S006", "Sara")
        student.add_grade(90)
        self.assertTrue(student.is_on_honor_roll())

    def test_remove_grade(self):
        """Grades are removed by index or by value with clear errors."""
        self.assertEqual(self.student.remove_grade_by_index(1), 72.5)
        self.assertEqual(self.student.remove_grade_by_value(95), 95.0)
        self.assertEqual(self.student.grades, [88.0])
        with self.assertRaises(IndexError):
            self.student.remove_grade_by_index(5)
        with self.assertRaises(ValueError):
            self.student.remove_grade_by_value(50)

    def test_report(self):
        """The report shows every required field."""
        report = self.student.generate_report()
        for text in ("Student ID: S001", "Student Name: Ana Torres",
                     "Number of Grades: 3", "Average Grade: 85.17",
                     "Letter Grade: B", "Status: Passed", "Honor Roll: No"):
            self.assertIn(text, report)


if __name__ == "__main__":
    unittest.main()
