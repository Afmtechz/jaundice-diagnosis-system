// Fetch and display symptoms
document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('/api/symptoms');
        const symptoms = await response.json();
        displaySymptoms(symptoms);
    } catch (error) {
        console.error('Error fetching symptoms:', error);
    }
});

function displaySymptoms(symptoms) {
    const container = document.getElementById('symptomsContainer');
    container.innerHTML = '';
    
    symptoms.forEach(symptom => {
        const col = document.createElement('div');
        col.className = 'col-md-6';
        col.innerHTML = `
            <div class="form-check symptom-checkbox">
                <input class="form-check-input" type="checkbox" value="${symptom.id}" id="symptom_${symptom.id}">
                <label class="form-check-label" for="symptom_${symptom.id}">
                    ${symptom.name}
                </label>
            </div>
        `;
        container.appendChild(col);
    });
}

// Image preview
document.getElementById('medicalReport')?.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const previewDiv = document.getElementById('imagePreview');
            previewDiv.innerHTML = `<div class="image-preview-container">
                <img src="${event.target.result}" alt="Medical Report Preview">
                <small class="text-muted">✓ Image selected</small>
            </div>`;
        };
        reader.readAsDataURL(file);
    }
});

// Form submission
document.getElementById('diagnosisForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const selectedSymptoms = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    if (selectedSymptoms.length === 0) {
        alert('Please select at least one symptom');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('symptoms', JSON.stringify(selectedSymptoms));
        
        const medicalReport = document.getElementById('medicalReport');
        if (medicalReport.files.length > 0) {
            formData.append('image', medicalReport.files[0]);
        }
        
        const response = await fetch('/api/diagnose', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        alert('An error occurred while processing the diagnosis');
    }
});

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const severityColor = getSeverityColor(data.severity);
    
    const html = `
        <div class="card results-card">
            <div class="card-header bg-success text-white">
                <h4 class="mb-0">✓ Diagnosis Results</h4>
            </div>
            <div class="card-body">
                <div class="severity-badge severity-${data.severity.toLowerCase()}">
                    ${data.severity} Jaundice
                </div>
                
                <div class="info-box">
                    <strong>Severity Score:</strong> ${data.severity_score}/10
                    <div class="progress mt-2">
                        <div class="progress-bar" style="width: ${data.severity_score * 10}%; background: ${severityColor};"></div>
                    </div>
                </div>
                
                <div class="info-box">
                    <strong>Matched Symptoms:</strong> ${data.matched_symptoms}
                    <br><strong>Confidence Score:</strong> ${data.confidence}%
                </div>
                
                ${data.bilirubin_level ? `
                <div class="info-box">
                    <strong>Estimated Bilirubin Level:</strong> ${data.bilirubin_level} mg/dL
                </div>
                ` : ''}
                
                <h5 class="mt-4">Treatment Recommendations</h5>
                <ul class="treatment-list">
                    ${data.treatment.advice.map(advice => `<li>${advice}</li>`).join('')}
                </ul>
                
                <div class="alert alert-info mt-3">
                    <strong>Follow-up:</strong> ${data.treatment.follow_up || 'As recommended'}
                </div>
                <div class="alert alert-warning">
                    <strong>Doctor Visit:</strong> ${data.treatment.doctor_visit || 'Consult as needed'}
                </div>
                
                <button class="btn btn-primary w-100 mt-3" onclick="window.location.reload()">
                    🔄 New Diagnosis
                </button>
            </div>
        </div>
    `;
    
    document.getElementById('resultsCard').innerHTML = html;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function getSeverityColor(severity) {
    const colors = {
        'MILD': '#28a745',
        'MODERATE': '#ffc107',
        'SEVERE': '#dc3545'
    };
    return colors[severity] || '#0066cc';
}