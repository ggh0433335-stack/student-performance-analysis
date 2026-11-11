import csv
from typing import List
from src.student import Student

class StudentDataset:
    """
    Reptesents a list of all the students from the dataset.
    """

    def __init__(self) -> None:
        """
        Initializes the dataset with an empty list of students.
        """
        self.students: List = []

    def load_from_csv(self, file_path: str) -> None:
        """
        Loads and validates the student records from a cvs file.

        :param file_path: Path to desired file
        """
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            reader.fieldnames = [self._normalize_header(student) for student in reader.fieldnames]

            for row in reader:
                normalized_row = {self._normalize_header(key): value.strip() for key, value in row.items()}
                student = self._process_row(normalized_row)
                if student is not None:
                    self.students.append(student)

    def _normalize_header(self, header: str) -> str:
        """
        Normalizes collumn headers with lowercase and snake case.
        """
        header = header.strip().lower()
        return header.replace(" ", "_")
    
    def _normalize_categorical(self, value: str) -> str:
        """
        Capitalize the first letter of each word.
        """
        return " ".join([word.capitalize() for word in value.split()])  
    
    def _process_row(self, row: dict) -> Student:
        """
        Validates and converts row values into correct types.

        :param row: Row to analyze
        :returns: A Student object
        """
        try:
            
            student_id = int(row.get("student_id", -1))
            age = int(row.get("age", -1))
            study_hours_per_day = float(row.get("study_hours_per_day", -1))
            social_media_hours = float(row.get("social_media_hours", -1))
            attendance_percentage = float(row.get("attendance_percentage", -1))
            sleep_hours = float(row.get("sleep_hours", -1))
            exercise_frequency = int(row.get("exercise_frequency", -1))
            previous_gpa = float(row.get("previous_gpa", -1))
            semester = int(row.get("semester", -1))
            social_activity = int(row.get("social_activity", -1))
            screen_time = float(row.get("screen_time", -1))
            time_management_score = int(row.get("time_management_score", -1))
            exam_score = float(row.get("exam_score", -1))

            if not (0 <= exam_score <= 100):
                return None

            part_time_job = self._normalize_categorical(row.get("part_time_job", ""))
            if part_time_job not in {"Yes", "No"}:
                return None
            
            diet_quality = self._normalize_categorical(row.get("diet_quality", ""))
            if diet_quality not in {"Poor", "Fair", "Good"}:
                return None
            
            internet_quality = self._normalize_categorical(row.get("internet_quality", ""))
            if internet_quality not in {"Low", "Medium", "High"}:
                return None
            
            extracurricular_participation = self._normalize_categorical(row.get("extracurricular_participation", ""))
            if extracurricular_participation not in {"Yes", "No"}:
                return None
            
            dropout_risk = self._normalize_categorical(row.get("dropout_risk", ""))
            if dropout_risk not in {"Yes", "No"}:
                return None
            
            access_to_tutoring = self._normalize_categorical(row.get("access_to_tutoring", ""))
            if access_to_tutoring not in {"Yes", "No"}:
                return None
            
            motivation_level = int(row.get("motivation_level", -1))
            if not (0 < motivation_level < 11):
                return None

            major = self._normalize_categorical(row.get("major", ""))
            study_environment = self._normalize_categorical(row.get("study_environment", ""))
            learning_style = self._normalize_categorical(row.get("learning_style", ""))


            return Student(
                student_id=student_id,
                age=age,
                major=major,
                study_hours_per_day=study_hours_per_day,
                social_media_hours=social_media_hours,
                part_time_job=part_time_job,
                attendance_percentage=attendance_percentage,
                sleep_hours=sleep_hours,
                diet_quality=diet_quality,
                exercise_frequency=exercise_frequency,
                internet_quality=internet_quality,
                extracurricular_participation=extracurricular_participation,
                previous_gpa=previous_gpa,
                semester=semester,
                dropout_risk=dropout_risk,
                social_activity=social_activity,
                screen_time=screen_time,
                study_environment=study_environment,
                access_to_tutoring=access_to_tutoring,
                motivation_level=motivation_level,
                learning_style=learning_style,
                time_management_score=time_management_score,
                exam_score=exam_score,

            )
        
 
        except (ValueError, KeyError):
            """
            Skips the row is it fails.
            """
            return None