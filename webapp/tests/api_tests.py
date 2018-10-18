#Alec Wang and Bat-Orgil Batjargal

import career_salary_data_source
import unittest

class career_salary_data_sourceTest(unittest.TestCase):
    def setUp(self):
        self.career_salary_data_source = career_salary_data_source.career_salary_data_sourceTest("test-recent-grads.csv")

    def tearDown(self):
        pass

    def test_specific_category(self):
        #EXAMPLE: majorinfo.com/majors/?maj=law_and_public_policy/
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
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3), majors_in_law_and_public_policy)

    def test_invalid_specific_category(self):
        #EXAMPLE: majorinfo.com/majors/?maj=extreme_sports/
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category_id = 'Extreme Sports'))

    def test_invalid_specific_category_out_of_range(self):

        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category_id = 17))

    def test_invalid_specific_category_float(self):
        #EXAMPLE:
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category_id = 3.14))

    def test_invalid_specific_category_boolean(self):
        #EXAMPLE:
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category_id = True))


    def test_specific_majors_from_any_category(self):
        #EXAMPLE: majorinfo.com/majors/?maj=chem/
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
        self.assertEquals(self.career_salary_data_source.get_majors(major_contains = 'chem'), chem_majors)

    def test_invalid_specific_major(self):
        #EXAMPLE: majorinfo.com/majors/?maj=skydiving/

        self.assertRaises(ValueError,
                self.career_salary_data_source.get_majors(major_contains = 'Skydiving'))

    def test_invalid_specific_major_int(self):
        self.assertRaises(ValueError,
                self.career_salary_data_source.get_majors(major_contains = 6))

    def test_invalid_specific_major_boolean(self):
        self.assertRaises(ValueError,
                self.career_salary_data_source.get_majors(major_contains = False))

    def test_specific_category_specific_major(self):
        #EXAMPLE: majorinfo.com/majors/?cat=4&maj=math/
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
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 4,
                major_contains = 'math'), math_majors_in_cs_and_math)

    def test_invalid_specific_category_specific_major(self):

        #EXAMPLE: majorinfo.com/majors/?cat=7&maj=physics/
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category_id = 7, major_contains = 'Physics'))


    def test_all_majors_above_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/?min_sal=70000/
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
        #EXAMPLE: majorinfo.com/majors/?min_sal=1000000/
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(minimum_salary = 1000000))

    def test_invalid_string_all_majors_above_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/?min_sal='lots of money'/
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(minimum_salary = 'lots of money'))

    def test_invalid_boolean_all_majors_above_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/?min_sal=True/
        self.assertRaises(ValueError, self.career_salary_data_source.get_majors(minimum_salary = True))

    def test_all_majors_from_specific_category_with_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/?cat=7&min_sal=45000/
        majors_in_arts_with_salary_above_45k = [{id: 6099, "major": "Miscellaneous fine arts", "total": 3340, "men": 1970, "women": 1370,
        "category_id": 7, "employed": 2914, "full_time": 2049, "part_time": 1067,
        "unemployed": 286, "unemployment_rate": 0.089375, "median": 50000, "p25th": 25000, "p75th": 66000,
        "college_jobs": 693, "non_college_jobs": 1714, "low_wage_jobs": 755}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 7, minimum_salary = 45000), majors_in_arts_with_salary_above_45k)

    def test_invalid_all_majors_from_specific_category_with_invalid_min_salary(self):

    	#Example: majorinfo.com/majors/?cat=7&min_sal=70000/
    	self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category_id = 7, minimum_salary = 70000))

    def test_specific_majors_from_any_category_with_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/?maj=physics&min_sal=55000/
        physics_majors_with_salary_above_55k = [{id: 5001, "major": "Astronomy And Astrophysics", "total": 1792, "men": 832, "women": 960,
        "category_id": 2, "employed": 1526, "full_time": 1085, "part_time": 553,
        "unemployed": 33, "unemployment_rate": 0.021167415, "median": 62000, "p25th": 31500, "p75th": 109000,
        "college_jobs": 972, "non_college_jobs": 500, "low_wage_jobs": 220},
        {id: 2409, "major": "Engineering Mechanics Physics And Science", "total": 4321, "men": 3526, "women": 795,
        "category_id": 0, "employed": 3608, "full_time": 2999, "part_time": 811,
        "unemployed": 23, "unemployment_rate": 0.006334343, "median": 58000, "p25th": 25000, "p75th": 74000,
        "college_jobs": 2439, "non_college_jobs": 947, "low_wage_jobs": 263}]
        self.assertEquals(self.career_salary_data_source.get_majors(major_contains = 'physics',minimum_salary = 55000), physics_majors_with_salary_above_55k)

    def test_invalid_specific_majors_from_any_category_with_min_salary(self):
    	#EXAMPLE: majorinfo.com/majors/?maj=physics&min_sal=65000/
    	self.assertRaises(ValueError, self.career_salary_data_source.get_majors(major_contains = 'physics', minimum_salary = 65000))

    def test_specific_majors_from_specific_category_above_min_salary(self):
        #EXAMPLE: majorinfo.com/majors/?cat=8&maj=medical&min_sal=40000/
        medical_majors_in_health_with_salary_above_40k = [{id: 6105, "major": "Medical Technologies Technicians", "total": 15914, "men": 3916, "women": 11998,
        "category_id": 8, "employed": 13150, "full_time": 11510, "part_time": 2665,
        "unemployed": 505, "unemployment_rate": 0.03698279, "median": 45000, "p25th":36000, "p75th": 50000,
        "college_jobs": 5546, "non_college_jobs": 7176, "low_wage_jobs": 1002},
        {id: 6105, "major": "Medical Assisting Services", "total": 11123, "men": 803, "women": 10320,
        "category_id": 8, "employed": 9168, "full_time": 5643, "part_time": 4107,
        "unemployed": 407, "unemployment_rate": 0.042506527, "median": 42000, "p25th": 30000, "p75th": 65000,
        "college_jobs": 2091, "non_college_jobs": 6948, "low_wage_jobs": 1270}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 8, major_contains = 'medical', minimum_salary = 40000), medical_majors_in_health_with_salary_above_40k)

    def test_invalid_specific_majors_from_specific_category_above_min_salary(self):
    	#EXAMPLE: majorinfo.com/majors/?cat=8&maj=medical&min_sal=50000/
    	self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category_id = 8,major_contains = 'medical', minimum_salary = 50000))

    def test_invalid_specific_majors_from_specific_category_above_min_salary(self):
    	#EXAMPLE: majorinfo.com/majors/?cat=8&maj=medico&min_sal=40000/
    	self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category_id = 8, major_contains = 'medico', minimum_salary = 40000))
	def test_invalid_specific_majors_from_specific_category_above_min_salary(self):
    	#EXAMPLE: majorinfo.com/majors/?cat=20&maj=medical&min_sal=40000/
    	self.assertRaises(ValueError, self.career_salary_data_source.get_majors(category_id = 8.5,major_contains = 'medical', minimum_salary = 40000))

    def test_sort_by_major(self):
        #EXAMPLE: majorinfo.com/majors/?maj=law_and_public_policy/
        majors_in_law_and_public_policy_sort_by_major_alphabetically = [{id: 3210, "major": "Court Reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144},
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404},
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336},
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496},
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = "major"), majors_in_law_and_public_policy_sort_by_major_alphabetically)

    def test_sort_by_category_id(self):
        pass

    def test_sort_by_total(self):
        #EXAMPLE: majorinfo.com/majors/?maj=law_and_public_policy&sort_by=total/
        majors_in_law_and_public_policy_sort_by_total = [{id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404},
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336},
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496},
        {id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = 'total'), majors_in_law_and_public_policy_sort_by_total)

    def test_sort_by_percent_men(self):
        majors_in_law_and_public_policy_sort_by_percent_men = [
        #0.76393728 men
        {id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144},
        #0.52498953 men
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404},
        #0.52353882 men
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496},
        #0.44145199 men
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        #0.32783856 men
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = 'percent_men'), majors_in_law_and_public_policy_sort_by_percent_men)

    def test_sort_by_women(self):
        majors_in_law_and_public_policy_sort_by_percent_women = [
        #0.32783856 men
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336},
        #0.44145199 men
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        #0.52353882 men
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496},
        #0.52498953 men
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404},
        #0.76393728 men
        {id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = 'percent_women'), majors_in_law_and_public_policy_sort_by_percent_women)

    def test_sort_by_percent_full_time(self):
        majors_in_law_and_public_policy_sort_by_percent_full_time_employed = [
        # 808/(930+11) = 0.8586609989373007
        {id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144},
        # 4148/(4158+789) = 0.8384879725085911
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496},
        # 109970/(125393+11268) = 0.8046919018593454
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404},
        # 4163/(4547+670) = 0.7979681809469044
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        # 7851/(9762+757) = 0.7463637227873372
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = 'percent_full_time'), majors_in_law_and_public_policy_sort_by_percent_full_time_employed)

    def test_sort_by_part_time(self):
        majors_in_law_and_public_policy_sort_by_percent_part_time_employed = [
        # 3595/(9762+757) = 0.3417625249548436
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336}
        # 1306/(4547+670) = 0.25033544182480355
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        # 223/(930+11) = 0.23698193411264612
        {id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144},
        # 32242/(125393+11268) = 0.2359268555037648
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404},
        # 847/(4158+789) = 0.17121487770365879
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = 'percent_part_time'), majors_in_law_and_public_policy_sort_by_percent_part_time_employed)

    def test_sort_by_unemployment_rate(self):
        majors_in_law_and_public_policy_sort_by_unemployment_rate = [
        # "unemployment_rate": 0.1594906,
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496},
        # "unemployment_rate": 0.128426299,
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        # "unemployment_rate": 0.082452199,
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404},
        # "unemployment_rate": 0.071965016,
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336},
        # "unemployment_rate": 0.011689692,
        {id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = 'unemployment_rate'), majors_in_law_and_public_policy_sort_by_unemployment_rate)

    def test_sort_by_employment_rate(self):
        majors_in_law_and_public_policy_sort_by_unemployment_rate = [
        # "unemployment_rate": 0.011689692,
        {id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144}
        # "unemployment_rate": 0.071965016,
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336},
        # "unemployment_rate": 0.082452199,
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404},
        # "unemployment_rate": 0.128426299,
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        # "unemployment_rate": 0.1594906,
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = 'employment_rate'), majors_in_law_and_public_policy_sort_by_unemployment_rate)

    def test_sort_by_p25th(self):
        majors_in_law_and_public_policy_sort_by_p25th = [
        {id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
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
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404},
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = 'p25th'), majors_in_law_and_public_policy_sort_by_p25th)

    def test_sort_by_p75th(self):
        majors_in_law_and_public_policy_sort_by_p75th = [
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496},
        {id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144},
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336},
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = 'p75th'), majors_in_law_and_public_policy_sort_by_p75th)

    def test_sort_by_percent_college_jobs(self):
        majors_in_law_and_public_policy_sort_by_college_jobs = [
        # 1550/(1550+1871+340) = 0.41212443499069396
        {id: 5402, "major": "Public Policy", "total": 5978, "men": 2639, "women": 3339,
        "category_id": 3, "employed": 4547, "full_time": 4163, "part_time":
        1306, "unemployed": 670, "unemployment_rate": 0.128426299, "median": 50000, "p25th": 35000, "p75th": 70000,
        "college_jobs": 1550, "non_college_jobs": 1871, "low_wage_jobs": 340},
        # 402/(402+528+144) = 0.3743016759776536
        {id: 3210, "major": "court reporting", "total": 1148, "men": 877, "women": 271,
        "category_id": 3, "employed": 930, "full_time": 808, "part_time": 223,
        "unemployed": 11, "unemployment_rate": 0.011689692, "median": 54000, "p25th": 50000, "p75th": 54000,
        "college_jobs": 402, "non_college_jobs": 528, "low_wage_jobs": 144},
        # 912/(912+2313+496) = 0.24509540446116634
        {id: 3210, "major": "Public Administration", "total": 5629, "men": 2947, "women": 2682,
        "category_id": 3, "employed": 4158, "full_time": 4148, "part_time": 847,
        "unemployed": 789, "unemployment_rate": 0.1594906, "median": 36000, "p25th": 23000, "p75th": 60000,
        "college_jobs": 912, "non_college_jobs": 2313, "low_wage_jobs": 496},
        # 2002/(2002+6454+1336) = 0.20445261437908496
        {id: 3210, "major": "Pre-law and Legal Studies", "total": 13528, "men": 4435, "women": 9093,
        "category_id": 3, "employed": 9762, "full_time": 7851, "part_time": 3595,
        "unemployed": 757, "unemployment_rate": 0.071965016, "median": 36000, "p25th": 29200, "p75th": 46000,
        "college_jobs": 2002, "non_college_jobs": 6454, "low_wage_jobs": 1336},
        # 24348/(24348+88858+18404) = 0.18500113973102347
        {id: 3210, "major": "Criminal Justice and Fire Protection", "total": 152824, "men": 80231, "women": 72593,
        "category_id": 3, "employed": 125393, "full_time": 109970, "part_time": 32242,
        "unemployed": 11268, "unemployment_rate": 0.082452199, "median": 35000, "p25th": 26000, "p75th": 45000,
        "college_jobs": 24348, "non_college_jobs": 88858, "low_wage_jobs": 18404}]
        self.assertEquals(self.career_salary_data_source.get_majors(category_id = 3, sort_by = 'college_jobs'), majors_in_law_and_public_policy_sort_by_college_jobs)

    def test_sort_by_non_college_jobs(self):
        pass

    def test_sort_by_low_wage_jobs(self):
        pass
