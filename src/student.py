from typing import Dict, Any


class Student:
    """
    Represents a single student object with all attributes from the dataset.
    """
    # attributes is a class variable that stores the str values for the general attributes of a 'Student' object
        # index 0 are attributes that store strings
        # index 1 are attributes that store integers
        # index 2 are attributes that store floats
    attributes = [
        ['student_id', 'major', 'part_time_job', 'diet_quality', 'internet_quality', 'extracurricular_participation', 'dropout_risk', 'study_environment', 'access_to_tutoring', 'learning_style'],
        ['age','exercise_frequency', 'semester', 'social_activity', 'motivation_level'],
        ['study_hours_per_day', 'social_media_hours', 'attendance_percentage', 'sleep_hours', 'previous_gpa', 'screen_time', 'time_management_score', 'exam_score']
    ]

    def __init__(
        self,
        student_id: str,
        age: int,
        major: str,
        study_hours_per_day: float,
        social_media_hours: float,
        part_time_job: str,
        attendance_percentage: float,
        sleep_hours: float,
        diet_quality: str,
        exercise_frequency: int,
        internet_quality: str,
        extracurricular_participation: str,
        previous_gpa: float,
        semester: int,
        dropout_risk: str,
        social_activity: int,
        screen_time: float,
        study_environment: str,
        access_to_tutoring: str,
        motivation_level: int,
        learning_style: str,
        time_management_score: float,
        exam_score: float
    ) -> None:
        """
        Initialize a Student object with all dataset attributes.

        :param student_id (str): Unique identifier for the student.
        :param age (int): Student's age in years.
        :param major (str): Academic major.
        :param study_hours_per_day (float): Average study hours per day.
        :param social_media_hours (float): Daily hours on social media.
        :param part_time_job (str): 'Yes' or 'No' indicating part-time job.
        :param attendance_percentage (float): Attendance percentage (0–100).
        :param sleep_hours (float): Average sleep hours per day.
        :param diet_quality (str): Diet quality - 'Poor', 'Fair', or 'Good'.
        :param exercise_frequency (int): Exercise sessions per week.
        :param internet_quality (str): Internet quality - 'Poor', 'Fair', or 'Good'.
        :param extracurricular_participation (str): 'Yes' or 'No'.
        :param previous_gpa (float): GPA from previous term (0–4 scale).
        :param semester (int): Current academic semester (1–8).
        :param dropout_risk (str): 'Yes' or 'No'.
        :param social_activity (int): Engagement in social activities (0–5).
        :param screen_time (float): Total screen time per day.
        :param study_environment (str): Typical study setting.
        :param access_to_tutoring (str): 'Yes' or 'No'.
        :param motivation_level (int): Motivation level (1–10).
        :param learning_style (str): Preferred learning style.
        :param time_management_score (float): Time management score (0–10).
        :param exam_score (float): Final exam score (0–100).  
        """
        self.student_id = student_id
        self.age = int(age)
        self.major = major.lower().title()
        self.study_hours_per_day = float(study_hours_per_day)
        self.social_media_hours = float(social_media_hours)
        self.part_time_job = part_time_job.lower().title()
        self.attendance_percentage = float(attendance_percentage)
        self.sleep_hours = float(sleep_hours)
        self.diet_quality = diet_quality.lower().title()
        self.exercise_frequency = int(exercise_frequency)
        self.internet_quality = internet_quality.lower().title()
        self.extracurricular_participation = extracurricular_participation.lower().title()
        self.previous_gpa = float(previous_gpa)
        self.semester = int(semester)
        self.dropout_risk = dropout_risk.lower().title()
        self.social_activity = int(social_activity)
        self.screen_time = float(screen_time)
        self.study_environment = study_environment.lower().title()
        self.access_to_tutoring = access_to_tutoring.lower().title()
        self.motivation_level = int(motivation_level)
        self.learning_style = learning_style.lower().title()
        self.time_management_score = float(time_management_score)
        self.exam_score = float(exam_score)

    def __str__ (self) -> str:
        """
        Represents 'Student' object as str.

        :returns: 'Student' str representation
        """

        return f"StudentID: {self.student_id}, Age: {self.age}, Major: {self.major.title()}, Exam Score: {self.exam_score}"
    
    def to_dict(self) -> Dict:
        """
        Converts a 'Student'object to a dictionary.

        :returns: Dictionary of student attributes
        """

        return {attribute : getattr(self, attribute) for attribute_type in self.attributes for attribute in attribute_type}
    
    def update_from_dict(self, new_dict: dict) -> None:
        """
        Updates the 'Student' object attributes from a given dictionary.

        :param new_dict: Dictonary with new attributes for 'Student'
        """

        for attribute in new_dict:
            if attribute.lower() in self.to_dict():
                if attribute.lower() in self.attributes[0] and not isinstance(new_dict[attribute], (int,float)) and not new_dict[attribute].isdigit():
                    setattr(self, attribute.lower(), str(new_dict[attribute]))

                elif attribute.lower() in self.attributes[1]:
                    try:
                        setattr(self, attribute.lower(), int(new_dict[attribute]))
                    except:
                        continue
                        
                elif attribute.lower() in self.attributes[2]:
                    try:
                        setattr(self, attribute.lower(), float(new_dict[attribute]))
                    except:
                        continue