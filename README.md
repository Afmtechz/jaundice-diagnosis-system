# 🏥 Jaundice Diagnosis System

A Python-based medical diagnostic tool that helps identify and assess jaundice severity using symptom analysis, medical report scanning with OpenCV, and intelligent treatment recommendations.

## 📋 Overview

The Jaundice Diagnosis System is an AI-assisted diagnostic application designed to:
- **Collect patient symptoms** through an interactive interface
- **Match symptoms** against a comprehensive medical database
- **Analyze medical reports** using computer vision (OpenCV)
- **Assess severity levels** based on multiple factors
- **Provide treatment recommendations** tailored to severity

> **⚠️ MEDICAL DISCLAIMER**: This system is for educational and informational purposes only. It should NOT replace professional medical consultation. Always consult a qualified healthcare provider for proper diagnosis and treatment.

## ✨ Features

### 1. **Symptom Collection & Database Matching**
   - Interactive symptom selection from predefined database
   - Weighted symptom analysis
   - Confidence scoring system
   - 10+ common jaundice symptoms included

### 2. **Medical Report Analysis with OpenCV**
   - Image-based analysis of medical reports
   - Yellow tone detection and quantification
   - Estimated bilirubin level calculation
   - HSV color space analysis for accuracy

### 3. **Intelligent Severity Assessment**
   - Multi-factor severity scoring
   - Three-tier classification: MILD, MODERATE, SEVERE
   - Symptom weight consideration
   - Bilirubin level integration

### 4. **Smart Treatment Recommendations**
   - **MILD**: Home remedies and lifestyle advice
   - **MODERATE**: Medication suggestions and precautions
   - **SEVERE**: Urgent medical attention alerts
   - Customized follow-up schedules

### 5. **Comprehensive Reporting**
   - Timestamped diagnosis reports
   - Severity scores
   - Treatment plans
   - Follow-up recommendations

## 🚀 Installation

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Afmtechz/jaundice-diagnosis-system.git
   cd jaundice-diagnosis-system
