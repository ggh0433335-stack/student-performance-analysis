import unittest
import os
import tempfile
from src.student_dataset import StudentDataset

from src.student import Student

# Comprehensive test cases must be written for all implemented methods.  
# Sample tests are provided below as guidance. Note that the entire project  
# will also be evaluated with 45 hidden tests, so ensure thorough and robust coverage.


class TestStudentDataset(unittest.TestCase):

    def setUp(self):
        self.StudentDataset = StudentDataset()
        
    def test_init_creates_empty_dataset(self):
        """
        Test that the __init__ method creates an empty list of students.
        """
        
        new_dataset = StudentDataset()
        self.assertIsInstance(new_dataset.students, list, "students attribute should be a list")
        self.assertEqual(len(new_dataset.students), 0, "students list should be empty on initialization")

    def test_normalize_header(self):
        """
        Test that the header function eliminates or fixes incorrect values.
        """

        self.assertEqual(self.StudentDataset._normalize_header("ParT tiMe Job"), 'part_time_job')
        self.assertEqual(self.StudentDataset._normalize_header("  age   "), 'age')
        self.assertEqual(self.StudentDataset._normalize_header("   study Hours per day     "), 'study_hours_per_day')
    
    def test_normalize_categorical(self):
        """
        Test that normalize categorical works it capitalizes first word.
        """

        self.assertEqual(self.StudentDataset._normalize_categorical('hello'), 'Hello')
        self.assertEqual(self.StudentDataset._normalize_categorical('hello world'), 'Hello World')

    def test_process_row(self):
        """
        Test that both numerical and string processing works in process row.
        """

        row = {
            "student_id": "1", "age": "21", "major": "Computer science", "study_hours_per_day": "3",
            "social_media_hours": "2", "part_time_job": "yes", "attendance_percentage": "90", "sleep_hours": "7",
            "diet_quality": "good", "exercise_frequency": "3", "internet_quality": "medium",
            "extracurricular_participation": "no", "previous_gpa": "3.5", "semester": "2", "dropout_risk": "no",
            "social_activity": "4", "screen_time": "3", "study_environment": "quiet", "access_to_tutoring": "yes",
            "motivation_level": "8", "learning_style": "visual", "time_management_score": "7", "exam_score": "95"
        }

        invalid_row = row

        # test with float values all share same code so covers all cases

        self.assertIsInstance(self.StudentDataset._process_row(row), Student)
        invalid_row['exam_score'] = 1000
        self.assertIsNone(self.StudentDataset._process_row(invalid_row))
        invalid_row['exam_score'] = -100
        self.assertIsNone(self.StudentDataset._process_row(invalid_row))
        invalid_row['exam_score'] = "1000"
        self.assertIsNone(self.StudentDataset._process_row(invalid_row))
        invalid_row['exam_score'] = 10

        # test with str values all share same code so covers all cases

        invalid_row['part_time_job'] = 'yes'
        self.assertEqual(self.StudentDataset._process_row(invalid_row).part_time_job, 'Yes')
        invalid_row['part_time_job'] = 'ho'
        self.assertIsNone(self.StudentDataset._process_row(invalid_row))
    
    def test_load_from_csv(self):
        """
        Test to see that load form csv rejects wrong rows and appends good ones.
        """

        data: list = [["Student Id", "Age", "Major", "Study Hours Per Day", "Social Media Hours", "Part Time Job",
             "Attendance Percentage", "Sleep Hours", "Diet Quality", "Exercise Frequency", "Internet Quality",
             "Extracurricular Participation", "Previous GPA", "Semester", "Dropout Risk", "Social Activity",
             "Screen Time", "Study Environment", "Access To Tutoring", "Motivation Level", "Learning Style",
             "Time Management Score", "Exam Score"], 
             # valid row
             [1, 21, "engineering", 4, 2, "no", 88, 7, "fair", 3, "medium", "yes", 3.2, 4, "no", 3, 4, "group",
             "no", 7, "auditory", 8, 92],
             # ivalid row (str)
             [2, 22, "biology", 5, 3, "maybe", 90, 6, "good", 3, "high", "no", 3.0, 3, "yes", 2, 3, "quiet",
             "yes", 8, "visual", 7, 80],
             # invalid row (wrong exam grade range)
             [3, 19, "math", 4, 2, "yes", 90, 8, "poor", 4, "low", "no", 3.0, 2, "no", 3, 3, "group", "yes", 9,
             "reading", 6, 150]
             ]
        
        test_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        for row in data:
            test_file.write(','.join(map(str, row)) + '\n')
        test_file.close()
        self.assertIsNone(self.StudentDataset.load_from_csv(test_file.name))
        self.assertEqual(len(self.StudentDataset.students), 1)
        os.remove(test_file.name)