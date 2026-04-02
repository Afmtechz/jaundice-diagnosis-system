import cv2
import numpy as np
from datetime import datetime
from enum import Enum

# Step 1 & 2: Symptoms Database
class SeverityLevel(Enum):
    MILD = 1
    MODERATE = 2
    SEVERE = 3

SYMPTOMS_DATABASE = {
    "yellowing_of_skin": {"weight": 0.8, "severity": SeverityLevel.MODERATE},
    "yellowing_of_eyes": {"weight": 0.9, "severity": SeverityLevel.MODERATE},
    "dark_urine": {"weight": 0.7, "severity": SeverityLevel.MILD},
    "pale_stools": {"weight": 0.6, "severity": SeverityLevel.MILD},
    "abdominal_pain": {"weight": 0.8, "severity": SeverityLevel.MODERATE},
    "fatigue": {"weight": 0.5, "severity": SeverityLevel.MILD},
    "fever": {"weight": 0.7, "severity": SeverityLevel.MODERATE},
    "nausea": {"weight": 0.6, "severity": SeverityLevel.MILD},
    "loss_of_appetite": {"weight": 0.6, "severity": SeverityLevel.MILD},
    "joint_pain": {"weight": 0.5, "severity": SeverityLevel.MILD},
}

class JaundiceDiagnosisSystem:
    def __init__(self):
        self.patient_data = {}
        self.matched_symptoms = []
        self.severity_score = 0
        self.test_reports = {}
    
    # STEP 1: Input Symptoms
    def input_symptoms(self):
        """Collect symptoms from patient"""
        print("\n=== STEP 1: SYMPTOM INPUT ===")
        print("Available symptoms:")
        for idx, symptom in enumerate(SYMPTOMS_DATABASE.keys(), 1):
            print(f"{idx}. {symptom.replace('_', ' ').title()}")
        
        user_symptoms = []
        while True:
            try:
                choice = input("\nEnter symptom number (or 'done' to finish): ").strip().lower()
                if choice == 'done':
                    break
                choice = int(choice)
                symptom_list = list(SYMPTOMS_DATABASE.keys())
                if 1 <= choice <= len(symptom_list):
                    user_symptoms.append(symptom_list[choice - 1])
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a valid number or 'done'.")
        
        return user_symptoms
    
    # STEP 2: Check for Match in Symptoms Database
    def check_symptom_match(self, symptoms):
        """Match input symptoms with database"""
        print("\n=== STEP 2: SYMPTOM MATCHING ===")
        self.matched_symptoms = []
        total_weight = 0
        
        for symptom in symptoms:
            if symptom in SYMPTOMS_DATABASE:
                self.matched_symptoms.append({
                    'symptom': symptom,
                    'weight': SYMPTOMS_DATABASE[symptom]['weight'],
                    'severity': SYMPTOMS_DATABASE[symptom]['severity']
                })
                total_weight += SYMPTOMS_DATABASE[symptom]['weight']
                print(f"✓ Matched: {symptom.replace('_', ' ').title()}")
        
        # Calculate confidence score
        if self.matched_symptoms:
            confidence = (total_weight / len(self.matched_symptoms)) * 100
        else:
            confidence = 0
        
        print(f"\nConfidence Score: {confidence:.2f}%")
        return confidence
    
    # STEP 3: OpenCV Report Analysis
    def scan_medical_reports(self, image_path):
        """Analyze medical reports using OpenCV"""
        print("\n=== STEP 3: MEDICAL REPORT SCANNING ===")
        
        try:
            image = cv2.imread(image_path)
            if image is None:
                print("Error: Could not load image")
                return None
            
            # Convert to HSV for skin tone analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Detect yellowish tones (jaundice indicator)
            lower_yellow = np.array([15, 100, 100])
            upper_yellow = np.array([35, 255, 255])
            
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            yellow_pixels = cv2.countNonZero(mask)
            total_pixels = image.shape[0] * image.shape[1]
            yellow_percentage = (yellow_pixels / total_pixels) * 100
            
            print(f"Yellow tone detected: {yellow_percentage:.2f}%")
            
            # Analyze bilirubin levels (simulated from color analysis)
            bilirubin_estimate = self._estimate_bilirubin(yellow_percentage)
            print(f"Estimated Bilirubin Level: {bilirubin_estimate:.2f} mg/dL")
            
            self.test_reports['image_analysis'] = {
                'yellow_percentage': yellow_percentage,
                'bilirubin_estimate': bilirubin_estimate,
                'timestamp': datetime.now().isoformat()
            }
            
            return bilirubin_estimate
        
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return None
    
    def _estimate_bilirubin(self, yellow_percentage):
        """Estimate bilirubin levels from yellow tone percentage"""
        # Normal: <1.2, Mild: 1.2-3, Moderate: 3-10, Severe: >10
        return yellow_percentage * 0.15  # Simplified estimation
    
    # STEP 4: Check for Seriousness
    def assess_severity(self, symptoms, bilirubin_level=None):
        """Determine severity of jaundice"""
        print("\n=== STEP 4: SEVERITY ASSESSMENT ===")
        
        severity_points = 0
        
        # Calculate from symptoms
        for symptom_data in self.matched_symptoms:
            if symptom_data['severity'] == SeverityLevel.MILD:
                severity_points += 1
            elif symptom_data['severity'] == SeverityLevel.MODERATE:
                severity_points += 2
            elif symptom_data['severity'] == SeverityLevel.SEVERE:
                severity_points += 3
        
        # Add bilirubin level assessment
        if bilirubin_level:
            if bilirubin_level > 10:
                severity_points += 5
            elif bilirubin_level > 3:
                severity_points += 3
            elif bilirubin_level > 1.2:
                severity_points += 1
        
        self.severity_score = severity_points
        
        # Classify severity
        if severity_points >= 8:
            severity_classification = "SEVERE"
        elif severity_points >= 5:
            severity_classification = "MODERATE"
        else:
            severity_classification = "MILD"
        
        print(f"Severity Score: {severity_points}")
        print(f"Classification: {severity_classification}")
        
        return severity_classification
    
    # STEP 5: Suggest Treatment
    def suggest_treatment(self, severity_classification):
        """Suggest medicine or recommend doctor visit"""
        print("\n=== STEP 5: TREATMENT RECOMMENDATION ===")
        
        treatment_recommendations = {
            "MILD": {
                "advice": [
                    "Stay hydrated - drink plenty of water",
                    "Rest adequately",
                    "Avoid fatty and spicy foods",
                    "Take vitamin supplements (especially B-complex)"
                ],
                "home_remedies": [
                    "Turmeric milk daily",
                    "Lemon water in morning",
                    "Light herbal tea",
                    "Proper diet with proteins"
                ],
                "follow_up": "Monitor symptoms for 1 week and consult if not improved",
                "doctor_visit": "Not urgent, but consult within 1 week"
            },
            "MODERATE": {
                "advice": [
                    "Follow mild recommendations",
                    "Take prescribed liver support medicines",
                    "Get blood tests done (LFT, Bilirubin levels)",
                    "Avoid alcohol completely"
                ],
                "medicines": [
                    "Silymarin (Milk thistle) - 140mg twice daily",
                    "Ursodeoxycholic acid - as prescribed",
                    "Liver tonics - as prescribed"
                ],
                "follow_up": "Recheck bilirubin levels after 3-5 days",
                "doctor_visit": "Consult doctor within 2-3 days"
            },
            "SEVERE": {
                "advice": [
                    "IMMEDIATE MEDICAL ATTENTION REQUIRED",
                    "Do not delay - visit hospital now",
                    "Get comprehensive liver function tests",
                    "Possible hospitalization may be needed",
                    "May require IV therapy"
                ],
                "critical_tests": [
                    "Complete Blood Count (CBC)",
                    "Liver Function Tests (LFT)",
                    "Bilirubin (Total & Direct)",
                    "Imaging (Ultrasound/CT scan)",
                    "Viral markers if hepatitis suspected"
                ],
                "doctor_visit": "URGENT - Visit emergency room immediately"
            }
        }
        
        recommendations = treatment_recommendations.get(severity_classification, {})
        
        print(f"\n📋 Recommendations for {severity_classification} Jaundice:")
        print("\nGeneral Advice:")
        for advice in recommendations.get("advice", []):
            print(f"  • {advice}")
        
        if severity_classification == "MILD":
            print("\nHome Remedies:")
            for remedy in recommendations.get("home_remedies", []):
                print(f"  • {remedy}")
        
        elif severity_classification == "MODERATE":
            print("\nSuggested Medicines:")
            for medicine in recommendations.get("medicines", []):
                print(f"  • {medicine}")
        
        else:  # SEVERE
            print("\n🚨 CRITICAL TESTS NEEDED:")
            for test in recommendations.get("critical_tests", []):
                print(f"  • {test}")
        
        print(f"\n⏰ Follow-up: {recommendations.get('follow_up', 'N/A')}")
        print(f"👨‍⚕️ Doctor Visit: {recommendations.get('doctor_visit', 'Consult as needed')}")
        
        return recommendations
    
    def generate_report(self):
        """Generate comprehensive diagnosis report"""
        print("\n" + "="*50)
        print("JAUNDICE DIAGNOSIS REPORT")
        print("="*50)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Severity Score: {self.severity_score}")
        print(f"Matched Symptoms: {len(self.matched_symptoms)}")
        print("="*50 + "\n")

# Main execution
def main():
    print("🏥 JAUNDICE DIAGNOSIS SYSTEM 🏥")
    print("================================\n")
    
    system = JaundiceDiagnosisSystem()
    
    # Step 1: Input Symptoms
    symptoms = system.input_symptoms()
    
    if not symptoms:
        print("No symptoms entered. Exiting...")
        return
    
    # Step 2: Check for Match
    confidence = system.check_symptom_match(symptoms)
    
    # Step 3: Scan Medical Reports (Optional)
    image_path = input("\nEnter path to medical report image (or 'skip'): ").strip()
    bilirubin_level = None
    if image_path.lower() != 'skip':
        bilirubin_level = system.scan_medical_reports(image_path)
    
    # Step 4: Assess Severity
    severity = system.assess_severity(symptoms, bilirubin_level)
    
    # Step 5: Suggest Treatment
    treatment = system.suggest_treatment(severity)
    
    # Generate Report
    system.generate_report()

if __name__ == "__main__":
    main()