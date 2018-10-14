import api
import unittest

class CareerSalaryDataSourceTest(unittest.TestCase):
    def setUp(self):
        self.careersalarydatasource = careersalarydatasource.CareerSalaryDataSourceTest("test-recent-grads.csv")

    def tearDown(self):
        pass

    def test_category(self):
        #EXAMPLE: majoroutcomes.com/majors/law_and_public_policy
        [{id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category": "Law & Public Policy", "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144},
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category": "Law & Public Policy", "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category": "Law & Public Policy", "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336},
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category": "Law & Public Policy", "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496},
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category": "Law & Public Policy", "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404}]

    def test_majors_from_specific_category(self):
        #EXAMPLE: majoroutcomes.com/majors/computer_science_mathematics/math
        [{id: 3700, "major": "Mathematics", "total": 72397, "men": 39956, "women": 32441,
        "category": "Computers & Mathematics", "employed": 58118, "full_time": 46399, "part_time": 18079,
        "unemployed": 2884, "unemployment_rate": 0.047277138, "median": 45000, "p25th": 33000, "p75th": 60000,
        "college_jobs": 34800, "non_college_jobs": 14829, "low_wage_jobs": 4569},
        {id: 3701, "major": "Applied Mathematics", "total": 4939, "men": 2794, "women": 2145,
        "category": "Computers & Mathematics", "employed": 3854, "full_time": 3465, "part_time": 1176,
        "unemployed": 385, "unemployment_rate": 0.090823307, "median": 45000, "p25th": 34000, "p75th": 63000,
        "college_jobs": 2437, "non_college_jobs": 803, "low_wage_jobs": 357},
        {id: 4005, "major": "Mathematics and Computer Science", "total": 609, "men": 500, "women": 109,
        "category": "Computers & Mathematics", "employed": 559, "full_time": 584, "part_time": 0,
        "unemployed": 0, "unemployment_rate": 0, "median": 42000, "p25th": 30000, "p75th": 78000,
        "college_jobs": 452, "non_college_jobs": 67, "low_wage_jobs": 25}]

    def test_major_from_any_category(self):
        #EXAMPLE: majorinfo.com/majors/null/chem
        [{id: 2405, "major": "Chemical Engineering", "total": 32260, "men": 21239, "women": 11021,
        "category": "Engineering", "employed": 25694, "full_time": 23170, "part_time": 5180,
        "unemployed": 1672, "unemployment_rate": 0.061097712, "median": 65000, "p25th": 50000, "p75th": 75000,
        "college_jobs": 18314, "non_college_jobs": 4440, "low_wage_jobs": 972},
        {id: 5003, "major": "Chemistry", "total": 66530, "men": 32923, "women": 33607,
        "category": "Physical Sciences", "employed": 48535, "full_time": 39509, "part_time": 15066,
        "unemployed": 2769, "unemployment_rate": 0.0539724, "median": 39000, "p25th": 30000, "p75th": 49900,
        "college_jobs": 30382, "non_college_jobs": 14718, "low_wage_jobs": 4288},
        {id: 3601, "major": "Biochemical Sciences", "total": 39107, "men": 18951, "women": 20156,
        "category": "Biology & Life Science", "employed": 25678, "full_time": 20643, "part_time": 9948,
        "unemployed": 2249, "unemployment_rate": 0.080531385, "median": 37400, "p25th": 29000, "p75th": 50000,
        "college_jobs": 15654, "non_college_jobs": 8394, "low_wage_jobs": 3012}]

    def test_majors_above_min_salary(self):
        #EXAMPLE: majoroutcomes.com/majors/70000
        [{id: 2419, "major": "Petroleum Engineering", "total": 2339, "men": 2057, "women": 282,
        "category": "Engineering", "employed": 1976, "full_time": 1849, "part_time": 270,
        "unemployed": 37, "unemployment_rate": 0.018380527, "median": 110000, "p25th": 95000, "p75th": 125000,
        "college_jobs": 1534, "non_college_jobs": 364, "low_wage_jobs": 193},
        {id: 2416, "major": "Mining And Mineral Engineering", "total": 756, "men": 679, "women": 77,
        "category": "Engineering", "employed": 640, "full_time": 556, "part_time": 170,
        "unemployed": 85, "unemployment_rate": 0.117241379, "median": 75000, "p25th": 55000, "p75th": 90000,
        "college_jobs": 350, "non_college_jobs": 257, "low_wage_jobs": 50},
        {id: 2415, "major": "Metallurgical Engineering", "total": 856, "men": 725, "women": 131,
        "category": "Engineering", "employed": 648, "full_time": 558, "part_time": 133,
        "unemployed": 16, "unemployment_rate": 0.024096386, "median": 73000, "p25th": 50000, "p75th": 105000,
        "college_jobs": 456, "non_college_jobs": 176, "low_wage_jobs": 0},
        {id: 2417, "major": "Naval Architecture And Marine Engineering", "total": 1258, "men": 1123, "women": 135,
        "category": "Engineering", "employed": 758, "full_time": 1069, "part_time": 150,
        "unemployed": 40, "unemployment_rate": 0.050125313, "median": 70000, "p25th": 43000, "p75th": 80000,
        "college_jobs": 529, "non_college_jobs": 102, "low_wage_jobs": 0}]

    def test_negative_majors_above_min_salary(self):
        #Example: majoroutcomes.com/majors/70000/arts


        #EXAMPLE: majoroutcomes.com/majors/arts/null/45000
        [{id: 6099, "major": "Miscellaneous fine arts", "total": 3340, "men": 1970, "women": 1370,
        "category": "Arts", "employed": 2914, "full_time": 2049, "part_time": 1067,
        "unemployed": 286, "unemployment_rate": 0.089375, "median": 50000, "p25th": 25000, "p75th": 66000,
        "college_jobs": 693, "non_college_jobs": 1714, "low_wage_jobs": 755}]


        #EXAMPLE: majoroutcomes.com/majors/null/physics/55000
        [{id: 5001, "major": "Astronomy And Astrophysics", "total": 1792, "men": 832, "women": 960,
        "category": "Physical Sciences", "employed": 1526, "full_time": 1085, "part_time": 553,
        "unemployed": 33, "unemployment_rate": 0.021167415, "median": 62000, "p25th": 31500, "p75th": 109000,
        "college_jobs": 972, "non_college_jobs": 500, "low_wage_jobs": 220},
        {id: 2409, "major": "Engineering Mechanics Physics And Science", "total": 4321, "men": 3526, "women": 795,
        "category": "Engineering", "employed": 3608, "full_time": 2999, "part_time": 811,
        "unemployed": 23, "unemployment_rate": 0.006334343, "median": 58000, "p25th": 25000, "p75th": 74000,
        "college_jobs": 2439, "non_college_jobs": 947, "low_wage_jobs": 263}]

        #EXAMPLE: majoroutcomes.com/majors/health/medical/40000
        [{id: 6105, "major": "Medical Technologies Technicians", "total": 15914, "men": 3916, "women": 11998,
        "category": "Health", "employed": 13150, "full_time": 11510, "part_time": 2665,
        "unemployed": 505, "unemployment_rate": 0.03698279, "median": 45000, "p25th":36000, "p75th": 50000,
        "college_jobs": 5546, "non_college_jobs": 7176, "low_wage_jobs": 1002},
        {id: 6105, "major": "Medical Assisting Services", "total": 11123, "men": 803, "women": 10320,
        "category": "Health", "employed": 9168, "full_time": 5643, "part_time": 4107,
        "unemployed": 407, "unemployment_rate": 0.042506527, "median": 42000, "p25th": 30000, "p75th": 65000,
        "college_jobs": 2091, "non_college_jobs": 6948, "low_wage_jobs": 1270}]


# 1: Petroleum Engineering
# 2: Mining And Mineral Engineering
# 3: Metallurgical Engineering
# 4: Naval Architecture And Marine Engineering
# 5: Chemical Engineering
# 20: Court reporting
# 30: Public Policy
# 42: Mathematics
# 48: Applied Mathematics
# 53: Mathematics and Computer Science
# 75: Chemistry
# 83: Biochemical Sciences
# 88: Pre-law and Legal Studies
# 90: Public Administration
# 95: Criminal Justice and Fire Protection
