import unittest

from src.student_dataset import StudentDataset
from src.student import Student
from src.performance_analyzer import PerformanceAnalyzer

# Comprehensive test cases must be written for all implemented methods.  
# Sample tests are provided below as guidance. Note that the entire project  
# will also be evaluated with 45 hidden tests, so ensure thorough and robust coverage.

class TestPerformanceAnalyzer(unittest.TestCase):
    def setUp(self):
        self.test_students = [
            Student(100012,19,'Business',4.7,3.3,'No',93.4,7.4,'Good',1,'High','No',4,3,'No',2,12.1,'Dorm','Yes',10,'Auditory',2.9,96),
            Student(100004,25,'Business',4.7,0.8,'Yes',62.9,6.5,'Good',6,'Low','No',4,4,'No',2,9.4,'Quiet Room','Yes',1,'Reading',7.1,98.5),
            Student(100022,24,'Psychology',5.8,3.4,'Yes',95.2,7.8,'Good',7,'Medium','No',4,8,'No',1,11.1,'Quiet Room','No',10,'Visual',6.1,100)
        ]
        data = StudentDataset()
        data.students = self.test_students
        self.performance_analyzer = PerformanceAnalyzer(data)
        

    def test_filter_by_attribute_missing_attribute(self):
        filtered = self.performance_analyzer.filter_by_attribute("nonexistent_attribute", "notValidAttribute")
        self.assertEqual(len(filtered), 0, "Expected no students when filtering by nonexistent attribute")
    
    def test_filter_by_empty_attribute(self):
        """
        Test to ensure filter by method behaves correctly with non strings.
        """
        self.assertEqual(len(self.performance_analyzer.filter_by_attribute('major',123)),0, "Expected no student when filtering by not valid attribute")
        self.assertEqual(len(self.performance_analyzer.filter_by_attribute(123,'computer science')),0,"Expected no students when integer present")
        
    def test_filter_by_correct_attribute(self):
        """
        Test to ensure filter method retrieves correct students.
        """
        self.assertEqual(len(self.performance_analyzer.filter_by_attribute('Major',"business")),2)
        self.assertEqual(len(self.performance_analyzer.filter_by_attribute('Major',"Psychology")),1)

    def test_compute_compute_exam_statistics_by_invalid_attribute(self):
        """
        Test that compute exam statistics method denies invalid attributes.
        """
        with self.assertRaises(ValueError) as context:
            self.performance_analyzer.compute_exam_statistics_by_attribute('hi')
        self.assertEqual(str(context.exception), "Error: Invalid field 'hi'. This method only supports specific categorical fields.")
        with self.assertRaises(ValueError) as context:
            self.performance_analyzer.compute_exam_statistics_by_attribute(123)
        self.assertEqual(str(context.exception), "Error: Invalid field '123'. This method only supports specific categorical fields.")

    def test_compute_exam_statistics_by_valid_attribute(self):
        """
        Test that coompute exam statistics provides correct results.
        """
        valid_attribute_computation = self.performance_analyzer.compute_exam_statistics_by_attribute('Major')
        self.assertEqual(len(valid_attribute_computation),2)
        self.assertEqual(valid_attribute_computation['Business']['mean'], 97.2)
        self.assertEqual(valid_attribute_computation['Business']['median'], 97.2)
        self.assertEqual(valid_attribute_computation['Business']['mode'], 96.0)
        self.assertEqual(valid_attribute_computation['Business']['std_dev'], 1.3)
        self.assertEqual(valid_attribute_computation['Psychology']['mean'], 100)
        self.assertEqual(valid_attribute_computation['Psychology']['median'], 100)
        self.assertEqual(valid_attribute_computation['Psychology']['mode'], 100)
        self.assertEqual(valid_attribute_computation['Psychology']['std_dev'], 0)
    
    def test_get_top_group_by_exam_score_invalid_attribute(self):
        with self.assertRaises(ValueError) as context:
            self.performance_analyzer.get_top_group_by_exam_score("age")
        self.assertEqual(str(context.exception), "Error: Invalid field 'age'. This method only supports specific categorical fields.")
        with self.assertRaises(ValueError) as context:
            self.performance_analyzer.get_top_group_by_exam_score(123)
        self.assertEqual(str(context.exception), "Error: Invalid field '123'. This method only supports specific categorical fields.")

    def test_get_top_group_by_exam_score_valid_attribute(self):
        """
        Test that get top group by exam score works correctly.
        """
        self.assertEqual(len(self.performance_analyzer.get_top_group_by_exam_score('Major')),2)
        self.assertEqual(self.performance_analyzer.get_top_group_by_exam_score('Major'),('Psychology', 100))

    def test_compare_groups_by_exam_score_invalid_attribute(self):
        """
        Test that compare groups by exam score method works using invalid attributes.
        """
        with self.assertRaises(ValueError) as context:
            self.performance_analyzer.compare_groups_by_exam_score("hi","psychology","business")
        self.assertEqual(str(context.exception), "Error: Invalid field 'hi'. This method only supports specific categorical fields.")
        with self.assertRaises(ValueError) as context:
            self.performance_analyzer.compare_groups_by_exam_score("hi",123,"business")
        self.assertEqual(str(context.exception), "Error: There's an invalid input. This method only supports specific categorical fields.")
        with self.assertRaises(ValueError) as context:
            self.performance_analyzer.compare_groups_by_exam_score(123,'psychology',"business")
        self.assertEqual(str(context.exception), "Error: There's an invalid input. This method only supports specific categorical fields.")
    
    def test_compare_groups_by_exam_score_valid_attribute(self):
        """
        Test that compare groups by exam score method works using valid attributes.
        """
        self.assertEqual(len(self.performance_analyzer.compare_groups_by_exam_score('major','business','psychology')),4)
        self.assertEqual(self.performance_analyzer.compare_groups_by_exam_score('major','business','psychology')['Business'],{'mean': 97.2, 'median': 97.2, 'mode': 96.0, 'std_dev': 1.3})
        self.assertEqual(self.performance_analyzer.compare_groups_by_exam_score('major','business','psychology')['Psychology'],{'mean': 100.0, 'median': 100.0, 'mode': 100.0, 'std_dev': 0.0})
        self.assertEqual(self.performance_analyzer.compare_groups_by_exam_score('major','business','psychology')['mean_difference'],2.8)
        self.assertEqual(self.performance_analyzer.compare_groups_by_exam_score('major','business','psychology')['higher_average_group'],'Psychology')

    def test_correlation_analysis_invalid_attribute(self):
        """
        Test that correlation analysis method deals with invalid inputs.
        """

        with self.assertRaises(ValueError) as context:
            self.performance_analyzer.correlation_analysis('hi',"extracurricular_participation")
        self.assertEqual(str(context.exception), "Error: hi is not in selected numerical attributes.")
        with self.assertRaises(ValueError) as context:
            self.performance_analyzer.correlation_analysis(123,"extracurricular_participation")
        self.assertEqual(str(context.exception), "Error: There's an invalid input. This method only supports specific categorical fields.")
        with self.assertRaises(ValueError) as context:
            self.performance_analyzer.correlation_analysis('semester',123)
        self.assertEqual(str(context.exception), "Error: There's an invalid input. This method only supports specific categorical fields.")

    def test_correlation_analysis_valid_attribute(self):
        """
        Test that valid inputs for correlation analysis output correct values.
        """

        self.assertEqual(self.performance_analyzer.correlation_analysis('age','major'),{'x_values': 'exam_score', 'y_values': 'age','correlation': 0.86, 'interpretation': 'Strong positive'})
        self.assertEqual(self.performance_analyzer.correlation_analysis('study_hours_per_day','major'),{'x_values': 'exam_score', 'y_values': 'study_hours_per_day','correlation': 0.79, 'interpretation': 'Strong positive'})