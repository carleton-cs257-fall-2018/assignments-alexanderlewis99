#Alec Wang and Bat-Orgil Batjargal

import career_salary_data_source
import unittest

class career_salary_data_sourceTest(unittest.TestCase):
    def setUp(self):
        self.career_salary_data_source = career_salary_data_source.career_salary_data_sourceTest("test-recent-grads.csv")

    def tearDown(self):
        pass

    def test_specific_category(self):
        #EXAMPLE: majorinfo.com/majors/law_and_public_policy/
        majors_in_law_and_public_policy = [{id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144},
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336},
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496},
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404}]
        self.assertEquals(self.career_salary_data_source.get_majors(category = 'Law & Public Policy'), majors_in_law_and_public_policy)

    def test_invalid_specific_category(self):
        #EXAMPLE: majorinfo.com/majors/extreme_sports/
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category = 'Extreme Sports'))

    def test_specific_majors_from_any_category(self):
        #EXAMPLE: majorinfo.com/majors/null/chem/
        chem_majors = [{id: 2405, "major": "Chemical Engineering", "total": 32260, "men": 21239, "women": 11021,
        "category_id": 0, "employed": 25694, "full_time": 23170, "part_time": 5180,
        "unemployed": 1672, "unemployment_rate": 0.061097712, "median": 65000, "p25th": 50000, "p75th": 75000,
        "college_jobs": 18314, "non_college_jobs": 4440, "low_wage_jobs": 972},
        {id: 5003, "major": "Chemistry", "total": 66530, "men": 32923, "women": 33607,
        "category_id": 2, "employed": 48535, "full_time": 39509, "part_time": 15066,
        "unemployed": 2769, "unemployment_rate": 0.0539724, "median": 39000, "p25th": 30000, "p75th": 49900,
        "college_jobs": 30382, "non_college_jobs": 14718, "low_wage_jobs": 4288},
        {id: 3601, "major": "Biochemical Sciences", "total": 39107, "men": 18951, "women": 20156,
        "category_id": 10, "employed": 25678, "full_time": 20643, "part_time": 9948,
        "unemployed": 2249, "unemployment_rate": 0.080531385, "median": 37400, "p25th": 29000, "p75th": 50000,
        "college_jobs": 15654, "non_college_jobs": 8394, "low_wage_jobs": 3012}]
        self.assertEquals(self.career_salary_data_source.get_majors(major_search_text = 'chem'), chem_majors)
  
    def test_invalid_specific_major(self):
        #EXAMPLE: majorinfo.com/majors/null/skydiving/
        self.assertRaises(ValueError,
                self.career_salary_data_source.get_majors_in_program(major_search_text = 'Skydiving'))

    def test_specific_category_specific_major(self):
        #EXAMPLE: majorinfo.com/majors/computers_and_mathematics/math/
        math_majors_in_cs_and_math =  [{id: 3700, "major": "Mathematics", "total": 72397, "men": 39956, "women": 32441,
        "category_id": 4, "employed": 58118, "full_time": 46399, "part_time": 18079,
        "unemployed": 2884, "unemployment_rate": 0.047277138, "median": 45000, "p25th": 33000, "p75th": 60000,
        "college_jobs": 34800, "non_college_jobs": 14829, "low_wage_jobs": 4569},
        {id: 3701, "major": "Applied Mathematics", "total": 4939, "men": 2794, "women": 2145,
        "category_id": 4, "employed": 3854, "full_time": 3465, "part_time": 1176,
        "unemployed": 385, "unemployment_rate": 0.090823307, "median": 45000, "p25th": 34000, "p75th": 63000,
        "college_jobs": 2437, "non_college_jobs": 803, "low_wage_jobs": 357},
        {id: 4005, "major": "Mathematics and Computer Science", "total": 609, "men": 500, "women": 109,
        "category_id": 4, "employed": 559, "full_time": 584, "part_time": 0,
        "unemployed": 0, "unemployment_rate": 0, "median": 42000, "p25th": 30000, "p75th": 78000,
        "college_jobs": 452, "non_college_jobs": 67, "low_wage_jobs": 25}]
        self.assertEquals(self.career_salary_data_source.get_majors(category = 'Computers & Mathematics',
                major_search_text = 'math'), math_majors_in_cs_and_math)

    def test_invalid_specific_category_specific_major(self):
        #EXAMPLE: majorinfo.com/majors/arts/physics/
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category = 'Arts', major_search_text = 'Physics'))

    def test_all_majors_above_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/70000/
        majors_with_salary_above_70k = [{id: 2419, "major": "Petroleum Engineering", "total": 2339, "men": 2057, "women": 282,
        "category_id": 0, "employed": 1976, "full_time": 1849, "part_time": 270,
        "unemployed": 37, "unemployment_rate": 0.018380527, "median": 110000, "p25th": 95000, "p75th": 125000,
        "college_jobs": 1534, "non_college_jobs": 364, "low_wage_jobs": 193},
        {id: 2416, "major": "Mining And Mineral Engineering", "total": 756, "men": 679, "women": 77,
        "category_id": 0, "employed": 640, "full_time": 556, "part_time": 170,
        "unemployed": 85, "unemployment_rate": 0.117241379, "median": 75000, "p25th": 55000, "p75th": 90000,
        "college_jobs": 350, "non_college_jobs": 257, "low_wage_jobs": 50},
        {id: 2415, "major": "Metallurgical Engineering", "total": 856, "men": 725, "women": 131,
        "category_id": 0, "employed": 648, "full_time": 558, "part_time": 133,
        "unemployed": 16, "unemployment_rate": 0.024096386, "median": 73000, "p25th": 50000, "p75th": 105000,
        "college_jobs": 456, "non_college_jobs": 176, "low_wage_jobs": 0},
        {id: 2417, "major": "Naval Architecture And Marine Engineering", "total": 1258, "men": 1123, "women": 135,
        "category_id": 0, "employed": 758, "full_time": 1069, "part_time": 150,
        "unemployed": 40, "unemployment_rate": 0.050125313, "median": 70000, "p25th": 43000, "p75th": 80000,
        "college_jobs": 529, "non_college_jobs": 102, "low_wage_jobs": 0}]
        self.assertEquals(self.career_salary_data_source.get_majors(minimum_salary = 70000), majors_with_salary_above_70k)

    def test_all_majors_above_min_salary_float(self):
        majors_with_salary_above_10950_point_35 = [{id: 2419, "major": "Petroleum Engineering", "total": 2339, "men": 2057, "women": 282,
        "category_id": 0, "employed": 1976, "full_time": 1849, "part_time": 270,
        "unemployed": 37, "unemployment_rate": 0.018380527, "median": 110000, "p25th": 95000, "p75th": 125000,
        "college_jobs": 1534, "non_college_jobs": 364, "low_wage_jobs": 193}]
        self.assertEquals(self.career_salary_data_source.get_majors(minimum_salary = 10950.35), majors_with_salary_above_10950_point_35)

    def test_invalid_number_all_majors_above_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/null/null/1000000/
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(minimum_salary = 1000000))

    def test_invalid_string_all_majors_above_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/null/null/1000000/
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(minimum_salary = 'lots of money'))

    def test_invalid_boolean_all_majors_above_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/null/null/1000000/
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(minimum_salary = True))

    def test_all_majors_from_specific_category_with_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/arts/null/45000/
        majors_in_arts_with_salary_above_45k = [{id: 6099, "major": "Miscellaneous fine arts", "total": 3340, "men": 1970, "women": 1370,
        "category_id": 7, "employed": 2914, "full_time": 2049, "part_time": 1067,
        "unemployed": 286, "unemployment_rate": 0.089375, "median": 50000, "p25th": 25000, "p75th": 66000,
        "college_jobs": 693, "non_college_jobs": 1714, "low_wage_jobs": 755}]
        self.assertEquals(self.career_salary_data_source.get_majors(category = 'arts', minimum_salary = 45000), majors_in_arts_with_salary_above_45k)

    def test_invalid_all_majors_from_specific_category_with_invalid_min_salary(self):
    	#Example: majorinfo.com/majors/70000/arts/
    	self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category = 'arts', minimum_salary = 70000))

    def test_specific_majors_from_any_category_with_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/null/physics/55000/
        physics_majors_with_salary_above_55k = [{id: 5001, "major": "Astronomy And Astrophysics", "total": 1792, "men": 832, "women": 960,
        "category_id": 2, "employed": 1526, "full_time": 1085, "part_time": 553,
        "unemployed": 33, "unemployment_rate": 0.021167415, "median": 62000, "p25th": 31500, "p75th": 109000,
        "college_jobs": 972, "non_college_jobs": 500, "low_wage_jobs": 220},
        {id: 2409, "major": "Engineering Mechanics Physics And Science", "total": 4321, "men": 3526, "women": 795,
        "category_id": 0, "employed": 3608, "full_time": 2999, "part_time": 811,
        "unemployed": 23, "unemployment_rate": 0.006334343, "median": 58000, "p25th": 25000, "p75th": 74000,
        "college_jobs": 2439, "non_college_jobs": 947, "low_wage_jobs": 263}]
        self.assertEquals(self.career_salary_data_source.get_majors(major_search_text = 'physics',minimum_salary = 55000), physics_majors_with_salary_above_55k)

    def test_invalid_specific_majors_from_any_category_with_min_salary(self):
    	#EXAMPLE: majorinfo.com/majors/null/physics/65000/
    	self.assertRaises(ValueError, self.career_salary_data_source.get_majors(major_search_text = 'physics', minimum_salary = 65000))

    def test_specific_majors_from_specific_category_above_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/health/medical/40000/
        medical_majors_in_health_with_salary_above_40k = [{id: 6105, "major": "Medical Technologies Technicians", "total": 15914, "men": 3916, "women": 11998,
        "category_id": 8, "employed": 13150, "full_time": 11510, "part_time": 2665,
        "unemployed": 505, "unemployment_rate": 0.03698279, "median": 45000, "p25th":36000, "p75th": 50000,
        "college_jobs": 5546, "non_college_jobs": 7176, "low_wage_jobs": 1002},
        {id: 6105, "major": "Medical Assisting Services", "total": 11123, "men": 803, "women": 10320,
        "category_id": 8, "employed": 9168, "full_time": 5643, "part_time": 4107,
        "unemployed": 407, "unemployment_rate": 0.042506527, "median": 42000, "p25th": 30000, "p75th": 65000,
        "college_jobs": 2091, "non_college_jobs": 6948, "low_wage_jobs": 1270}]
        self.assertEquals(self.career_salary_data_source.get_majors(category = 'health', major_search_text = 'medical', minimum_salary = 40000), medical_majors_in_health_with_salary_above_40k)

    def test_invalid_specific_majors_from_specific_category_above_min_salary(self):
    	#EXAMPLE: majorinfo.com/majors/health/medical/50000/
    	self.assertRaises(ValueError, self.career_salary_data_source.get_majors_by_minimum_salary_in_category_and_program(category = 'health',major_search_text = 'medical', minimum_salary = 50000))

    def test_invalid_specific_majors_from_specific_category_above_min_salary(self):
    	#EXAMPLE: majorinfo.com/majors/health/medico/40000/
    	self.assertRaises(ValueError, self.career_salary_data_source.get_majors_by_minimum_salary_in_category_and_program(category = 'health',major_search_text = 'medico', minimum_salary = 40000))
	def test_invalid_specific_majors_from_specific_category_above_min_salary(self):
    	#EXAMPLE: majorinfo.com/majors/healthico/medical/40000/
    	self.assertRaises(ValueError, self.career_salary_data_source.get_majors_by_minimum_salary_in_category_and_program(category = 'healthico',major_search_text = 'medical', minimum_salary = 40000))
