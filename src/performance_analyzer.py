from typing import List
from collections import Counter  
import math
import plotly.express as px
import pandas as pd


from src.student import Student
from src.student_dataset import StudentDataset

class PerformanceAnalyzer:
    """
    Represents a series of methods to obtain information from data.
    """

    def __init__(self, StudentDataset) -> None:
        """
        Initializes a 'PerformanceAnalyzer' object.

        :param StudentDataset: List of Student objects
        """

        self.StudentDataset = StudentDataset

    def filter_by_attribute(self, attribute: str, value: str) -> List[Student]:
        """
        Filters students by desired attribute and value.

        :param attribute: Name of specific field
        :param value: Value to match attribute with
        :returns: A list of Student objects
        """
        attributes = [
        'student_id', 'major', 'part_time_job', 'diet_quality', 'internet_quality', 'extracurricular_participation', 'dropout_risk', 'study_environment', 'access_to_tutoring', 'learning_style',
        'age','exercise_frequency', 'semester', 'social_activity', 'motivation_level',
        'study_hours_per_day', 'social_media_hours', 'attendance_percentage', 'sleep_hours', 'previous_gpa', 'screen_time', 'time_management_score', 'exam_score'
        ]
        if not isinstance(attribute, int) and not isinstance(value, int):
            if attribute.lower() in attributes and attribute.strip():
                return [student for student in self.StudentDataset.students if student.to_dict()[attribute.lower()].lower() == value.lower()]
            else:
                return []
        else:
            return []

    def compute_exam_statistics_by_attribute(self, attribute: str) -> dict[str : dict[str : float]]:
        """
        Computes mean, median, mode and standard deviation.

        :param attribute: Category to analyze
        :returns: A dictionary containing a dictionary with statistics per category
        """

        if isinstance(attribute, int):
            raise ValueError(f"Error: Invalid field '{attribute}'. This method only supports specific categorical fields.")
        
        if attribute.lower() in {"major", "part_time_job", "study_environment"}:

            values_in_attribute: set = {student.to_dict()[attribute.lower()].title() for student in self.StudentDataset.students }
            statistics: dict = {value: {'mean': 0, 'median': 0, 'mode': 0, 'std_dev': 0} for value in values_in_attribute}
                        
            for value in values_in_attribute:
                filtered_students = self.filter_by_attribute(attribute, value)
                scores: list = [student.to_dict()['exam_score'] for student in filtered_students]

                # mean
                mean = sum(scores)/len(scores)
                statistics[value]['mean'] = round(mean,1)
                
                # median 
                sorted_scores = sorted(scores)
                if len(scores) % 2 == 0: 
                    statistics[value]['median'] = round((sorted_scores[(len(sorted_scores)//2) - 1] + sorted_scores[len(sorted_scores)//2])/2, 1)
                else:
                    statistics[value]['median'] = sorted_scores[len(sorted_scores)//2]
                
                # mode 
                statistics[value]['mode'] = Counter(scores).most_common(1)[0][0]

                # std_dev
                variance = sum((score - statistics[value]['mean']) **2 for score in scores) / len(scores)
                statistics[value]['std_dev'] = round(math.sqrt(variance), 1)

            return statistics
        
        else:
            raise ValueError(f"Error: Invalid field '{attribute}'. This method only supports specific categorical fields.")
    

    def get_top_group_by_exam_score(self, attribute: str) -> str:
        """
        Finds the group with the highest mean exam score for a given attribute.

        :param attribute: The category on which the function analyzes and chooses the highest scoring group
        :returns: The name of the group with the highest average exam score
        """

        if isinstance(attribute, int):
            raise ValueError(f"Error: Invalid field '{attribute}'. This method only supports specific categorical fields.")
        
        if attribute.lower() not in {'major', 'part_time_job', 'study_environment'}:
            raise ValueError(f"Error: Invalid field '{attribute}'. This method only supports specific categorical fields.")
        
        stats: dict = self.compute_exam_statistics_by_attribute(attribute)
        top_group: str = max(stats, key=lambda group: stats[group]['mean'])
        top_stats: float = stats[top_group]

        return (top_group, top_stats['mean'])
    

    def compare_groups_by_exam_score(self, attribute: str, group1: str, group2: str) -> dict:
        """
        Compares exam scores of 2 groups within a certain category(attribute).

        :param attribute: The categorical field that we group by (e.g. major, part_time_job, or study environment)
        :param group1: The first group name
        :param group2: The second group name
        :returns: Dictionary containing statistics for each group, mean difference, and higher average group
        """
        if isinstance(attribute, int) or isinstance(group1, int) or isinstance(group2, int):
            raise ValueError("Error: There's an invalid input. This method only supports specific categorical fields.")
        
        stats: dict = self.compute_exam_statistics_by_attribute(attribute)
        stats_lower: dict = {key.lower(): value for key, value in stats.items()}

        g1_lower: str = group1.lower()
        g2_lower: str = group2.lower()
        
        if g1_lower not in stats_lower:
            raise ValueError(f"Error: Group {group1} is not in found for the attribute {attribute}")
        if g2_lower not in stats_lower:
            raise ValueError(f"Error: Group {group2} is not in found for the attribute {attribute}")
        
        stats_g1: dict = stats_lower[g1_lower]
        stats_g2: dict = stats_lower[g2_lower]

        mean_diff: float = round(abs(stats_g1['mean'] - stats_g2['mean']),1)
        higher_group: str = group1 if stats_g1['mean'] > stats_g2['mean'] else group2

        return {
            group1.title(): stats_g1,
            group2.title(): stats_g2,
            "mean_difference": mean_diff,
            "higher_average_group": higher_group.title()
        }

    def correlation_analysis(self, attribute: str, description: str) -> int:
        """
        Computes correlation factor and creates visual graphs.

        :param attribute: attribute to calculate correlation agains exam score
        :param description: string description to separate cases by
        """ 

        if isinstance(attribute, int) or isinstance(description, int):
            raise ValueError("Error: There's an invalid input. This method only supports specific categorical fields.")
        
        numeric_attributes: List = [['age','exercise_frequency', 'semester', 'social_activity', 'motivation_level'],
        ['study_hours_per_day', 'social_media_hours', 'attendance_percentage', 'sleep_hours', 'previous_gpa', 'screen_time', 'time_management_score', 'exam_score']]
        string_descriptions: List = ['major', 'part_time_job', 'diet_quality', 'internet_quality', 'extracurricular_participation', 'dropout_risk', 'study_environment', 'access_to_tutoring', 'learning_style']
        
        if attribute.lower() in numeric_attributes[0] or attribute.lower() in numeric_attributes[1]:
            if description.lower() in string_descriptions:
                x_values: float = [student.to_dict()['exam_score'] for student in self.StudentDataset.students]
                y_values: float = [student.to_dict()[attribute.lower()] for student in self.StudentDataset.students]
                interpretation: str = ""

                # compute correlation factor using pearson corellation coefficient formula

                correlation: float = round(((len(y_values)*sum([x_values[n] * y_values[n] for n in range(len(y_values))])) - sum(y_values)*sum(x_values)) / math.sqrt((len(y_values)*sum([x**2 for x in x_values]) - sum(x_values)**2) * (len(y_values)*sum([y**2 for y in y_values])-sum(y_values)**2)),2)

                # correlation interepretations
                if correlation == 0:
                    interpretation = "No correlation"
                elif correlation == 1:
                    interpretation = "Perfect positive"
                elif correlation == -1:
                    interpretation = "Perfect negative"
                elif 0.5 < correlation < 1:
                    interpretation = "Strong positive"
                elif -1 < correlation < -0.5:
                    interpretation = "Strong negative"
                elif 0 < correlation <= 0.5:
                    interpretation = "Weak positive"
                elif -0.5 <= correlation < 0:
                    interpretation = "Weak negative"
                
                data = pd.DataFrame({"Exam scores" : x_values,  attribute.lower().title() : y_values, description.lower().title() : [student.to_dict()[description.lower()] for student in self.StudentDataset.students] })


                # two cases are used to separeate cases on different graphs

                if attribute.lower() in numeric_attributes[1]:
                    # scatter plot graph
                    fig = px.scatter(data_frame = data, x = "Exam scores", y = attribute.lower().title(), trendline="ols", trendline_color_override = "black", color = description.lower().title(), facet_col = description.lower().title(),  labels={"Exam Score": "Exam Score", attribute.title(): attribute.title()})
                else:
                    # bar graph
                    fig = px.bar(data_frame = data, x = "Exam scores", y = attribute.lower().title(), color = description.lower().title(), facet_col = description.lower().title(),  labels={"Exam Score": "Exam Score", attribute.title(): attribute.title()})
                
                fig.show()

                return {"x_values" : "exam_score", "y_values" : attribute.lower(), "correlation" : correlation, "interpretation" : interpretation}
            else:
                raise ValueError(f"Error: {description} is not in selected categorical attributes.")
        else:
            raise ValueError(f"Error: {attribute} is not in selected numerical attributes.")