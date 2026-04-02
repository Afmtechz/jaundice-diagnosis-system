"""Test cases for jaundice diagnosis system"""

import unittest
from jaundice_diagnosis import JaundiceDiagnosisSystem, SYMPTOMS_DATABASE

class TestJaundiceDiagnosis(unittest.TestCase):
    
    def setUp(self):
        self.system = JaundiceDiagnosisSystem()
    
    def test_symptoms_database(self):
        self.assertIn('yellowing_of_skin', SYMPTOMS_DATABASE)
        self.assertIn('weight', SYMPTOMS_DATABASE['yellowing_of_skin'])
    
    def test_symptom_matching(self):
        symptoms = ['yellowing_of_skin', 'dark_urine']
        confidence = self.system.check_symptom_match(symptoms)
        self.assertGreater(confidence, 0)
    
    def test_severity_assessment(self):
        symptoms = ['yellowing_of_skin', 'abdominal_pain', 'fever']
        self.system.check_symptom_match(symptoms)
        severity = self.system.assess_severity(symptoms, bilirubin_level=2.5)
        self.assertIn(severity, ['MILD', 'MODERATE', 'SEVERE'])

if __name__ == '__main__':
    unittest.main()