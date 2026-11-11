from src.student import Student
from src.student_dataset import StudentDataset
from src.performance_analyzer import PerformanceAnalyzer

data = StudentDataset()
data.load_from_csv("data\student__dataset.csv")
p = PerformanceAnalyzer(data)
print(p.correlation_analysis("age", "extracurricular_participation"))