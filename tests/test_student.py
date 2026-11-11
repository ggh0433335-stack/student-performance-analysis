import unittest
from src.student import Student

# Comprehensive test cases must be written for all implemented methods.  
# Sample tests are provided below as guidance. Note that the entire project  
# will also be evaluated with 45 hidden tests, so ensure thorough and robust coverage.


class TestStudent(unittest.TestCase):
        
    def setUp(self):
        """
        Create a standard Student object for reuse in tests.
        """
        self.student = Student(
            student_id="S001",
            age=20,
            major="Computer Science",
            study_hours_per_day=4.5,
            social_media_hours=2.0,
            part_time_job="Yes",
            attendance_percentage=92.5,
            sleep_hours=7.0,
            diet_quality="Good",
            exercise_frequency=3,
            internet_quality="High",
            extracurricular_participation="No",
            previous_gpa=3.6,
            semester=4,
            dropout_risk="No",
            social_activity=3,
            screen_time=5.5,
            study_environment="Library",
            access_to_tutoring="Yes",
            motivation_level=8,
            learning_style="Visual",
            time_management_score=7.5,
            exam_score=88.0
        )

    def test_init_attributes(self):
        """
        Test that all attributes are initialized correctly.
        """
        self.assertEqual(self.student.student_id, "S001", "Incorrect student_id")
        self.assertEqual(self.student.age, 20, "Incorrect age")
        self.assertEqual(self.student.major, "Computer Science", "Incorrect major")
        self.assertEqual(self.student.study_hours_per_day, 4.5, "Incorrect study_hours_per_day")
        self.assertEqual(self.student.social_media_hours, 2.0, "Incorrect social_media_hours")
        self.assertEqual(self.student.part_time_job, "Yes", "Incorrect part_time_job")
        self.assertEqual(self.student.attendance_percentage, 92.5, "Incorrect attendance_percentage")
        self.assertEqual(self.student.sleep_hours, 7.0, "Incorrect sleep_hours")
        self.assertEqual(self.student.diet_quality, "Good", "Incorrect diet_quality")
        self.assertEqual(self.student.exercise_frequency, 3, "Incorrect exercise_frequency")
        self.assertEqual(self.student.internet_quality, "High", "Incorrect internet_quality")
        self.assertEqual(self.student.extracurricular_participation, "No", "Incorrect extracurricular_participation")
        self.assertEqual(self.student.previous_gpa, 3.6, "Incorrect previous_gpa")
        self.assertEqual(self.student.semester, 4, "Incorrect semester")
        self.assertEqual(self.student.dropout_risk, "No", "Incorrect dropout_risk")
        self.assertEqual(self.student.social_activity, 3, "Incorrect social_activity")
        self.assertEqual(self.student.screen_time, 5.5, "Incorrect screen_time")
        self.assertEqual(self.student.study_environment, "Library", "Incorrect study_environment")
        self.assertEqual(self.student.access_to_tutoring, "Yes", "Incorrect access_to_tutoring")
        self.assertEqual(self.student.motivation_level, 8, "Incorrect motivation_level")
        self.assertEqual(self.student.learning_style, "Visual", "Incorrect learning_style")
        self.assertEqual(self.student.time_management_score, 7.5, "Incorrect time_management_score")
        self.assertEqual(self.student.exam_score, 88.0, "Incorrect exam_score")

    def test_str_method(self):
        """
        Test that str method is correct.
        """

        self.assertEqual(str(self.student),"StudentID: S001, Age: 20, Major: Computer Science, Exam Score: 88.0", "__str__ method returned incorret string")

    def test_to_dict(self):
        """
        Test that student to dict works properly.
        """

        student_dict  =  self.student.to_dict()
        student_keys = ['student_id', 'major', 'part_time_job', 'diet_quality', 'internet_quality', 'extracurricular_participation', 'dropout_risk', 'study_environment', 'access_to_tutoring', 'learning_style', 'age', 'exercise_frequency', 'semester', 'social_activity', 'motivation_level', 'study_hours_per_day', 'social_media_hours', 'attendance_percentage', 'sleep_hours', 'previous_gpa', 'screen_time', 'time_management_score', 'exam_score']
        for key in student_dict:
            self.assertIn(key, student_keys, f"{key} is missing in the dictionary")

        self.assertEqual(student_dict['student_id'], 'S001')
        self.assertEqual(student_dict['age'], 20)
        self.assertEqual(student_dict['major'], 'Computer Science')
        self.assertEqual(student_dict['study_hours_per_day'], 4.5)
        self.assertEqual(student_dict['social_media_hours'], 2.0)
        self.assertEqual(student_dict['part_time_job'], 'Yes')
        self.assertEqual(student_dict['attendance_percentage'], 92.5)
        self.assertEqual(student_dict['sleep_hours'], 7.0)
        self.assertEqual(student_dict['diet_quality'], 'Good')
        self.assertEqual(student_dict['exercise_frequency'], 3)
        self.assertEqual(student_dict['internet_quality'], "High")
        self.assertEqual(student_dict['extracurricular_participation'], "No")
        self.assertEqual(student_dict['previous_gpa'], 3.6)
        self.assertEqual(student_dict['semester'], 4)
        self.assertEqual(student_dict['dropout_risk'], 'No')
        self.assertEqual(student_dict['social_activity'], 3)
        self.assertEqual(student_dict['screen_time'], 5.5)
        self.assertEqual(student_dict['study_environment'], 'Library')
        self.assertEqual(student_dict['access_to_tutoring'], "Yes")
        self.assertEqual(student_dict['motivation_level'], 8)
        self.assertEqual(student_dict['learning_style'], "Visual")
        self.assertEqual(student_dict['time_management_score'], 7.5)
        self.assertEqual(student_dict['exam_score'], 88.0)

    def test_update_from_dict(self):
        """
        Tests to see that update_from_dict is case sensitive and has proper validation.
        """

        new_dictionary = {'AGe': 2, 'hi': 5, 'exAm_sCore' : 'eighty', 'major':123, 'diet_quality':'123', 'previous_gpa' : 5}
        self.student.update_from_dict(new_dictionary)

        self.assertEqual(self.student.age, 2) # case sensitive test case
        self.assertFalse(hasattr(self.student,'hi')) # invalid attribute as key
        self.assertIsNot(self.student.exam_score, 'eighty') # invalid value for categorical attribute
        self.assertIsNot(self.student.major, 123) # invalid value for categorical attribute
        self.assertIsNot(self.student.diet_quality, '123') # invalid value for categorical attribute
        self.assertEqual(self.student.previous_gpa, 5.0) # converts int to float