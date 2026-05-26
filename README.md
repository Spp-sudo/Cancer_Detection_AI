# Vayu Vectors - OnCoLens AI
# Cancer Detection AI

An AI/ML cancer image classification prototype that can train models from organized medical image folders and run predictions through a command-line tool, Streamlit dashboard, FastAPI backend, or Next.js frontend.

## Project Overview

This project helps classify uploaded medical images into cancer-related categories such as brain, breast, lung, pancreatic, and prostate cancer. It includes reusable training, preprocessing, feature extraction, inference, and reporting modules.

The system is designed for experimentation and education. Users can add images into class-based dataset folders, train a scikit-learn model, save the trained model as a `.joblib` file, and use it for image prediction through multiple interfaces.

Example classes:

- `no_cancer`
- `brain_cancer`
- `breast_cancer`
- `lung_cancer`
- `prostate_cancer`
- `pancreatic_cancer`
- `cancer` for mixed or unknown cancer images

The model saves a trained `.joblib` file that can be used from the command line or the Streamlit app.

## Tech Stack

- **Programming language:** Python, TypeScript
- **ML and data processing:** scikit-learn, NumPy, Pillow, pydicom, joblib
- **Backend API:** FastAPI, Uvicorn
- **Dashboard/UI:** Streamlit, Plotly, pandas
- **Frontend:** Next.js, React, Tailwind CSS, Radix UI, lucide-react, Three.js
- **Testing:** pytest
- **Deployment config:** Render YAML

## Medical Notice

This is an educational prototype. It is not clinically validated and must not be used for real diagnosis, treatment, or ruling out cancer.

## Architecture Summary

```text
Medical image upload
        |
        v
Preprocessing
  - Load PNG/JPG/TIFF/BMP/DICOM files
  - Normalize and resize image data
        |
        v
Feature extraction
  - Color, texture, contrast, density, and edge-based features
        |
        v
Model inference
  - Load trained .joblib model
  - Predict class probabilities
        |
        v
Reporting layer
  - Confidence score
  - Predicted class
  - Evidence-style image metrics
        |
        v
User interfaces
  - CLI prediction script
  - Streamlit dashboard
  - FastAPI endpoint
  - Next.js frontend
```

The core ML logic lives inside `src/cancer_detector/`. UI and delivery layers call this shared logic instead of duplicating prediction behavior.

## Project Structure

```text
app.py                         Simple Streamlit image upload app
dashboard.py                   Root Streamlit dashboard entry point
api_server.py                  FastAPI backend server
predict.py                     Command-line prediction script
predict_json.py                JSON prediction script
train_model.py                 Training entry point
colab_training.ipynb           Google Colab training notebook
requirements.txt               Python app/API dependencies
requirements-train.txt         Smaller dependency list for Colab training
render.yaml                    Render deployment configuration
models/                        Saved .joblib model files
tests/                         Automated tests
frontend/                      Streamlit multi-page dashboard modules
nextjs-frontend/               Next.js frontend application
dataset/
  no_cancer/                   Put non-cancer images here
    mri/
    ct/
    pet/
  brain_cancer/                Put brain cancer images here
    mri/
  breast_cancer/               Put breast cancer images here
    mri/
    pet/
  lung_cancer/                 Put lung cancer images here
    ct/
    pet/
  prostate_cancer/             Put prostate cancer images here
    mri/
    histopathology/
  pancreatic_cancer/           Put pancreatic cancer images here
    ct/
    mri/
    histopathology/
src/cancer_detector/
  config.py                    Labels and display text
  preprocessing.py             Image loading and resizing
  feature_extractor.py         Image feature extraction
  models.py                    Trained model loader and fallback model
  training.py                  Dataset loading and model training
  inference.py                 Prediction pipeline
  reporting.py                 Text and app output
```

## Dataset Format

Put images into one folder per class:

```text
dataset/
  no_cancer/
    mri/
      normal_mri_1.dcm
    ct/
      normal_ct_1.png
    pet/
      normal_pet_1.jpg
  brain_cancer/
    mri/
      brain_mri_1.dcm
  leukemia/
    blood_smear/
      leukemia_blood_1.png
    bone_marrow_smear/
      leukemia_marrow_1.png
  breast_cancer/
    mri/
      breast_mri_1.dcm
    pet/
      breast_pet_1.png
  lung_cancer/
    ct/
      lung_ct_1.dcm
    pet/
      lung_pet_1.png
  prostate_cancer/
    mri/
      prostate_mri_1.dcm
  pancreatic_cancer/
    ct/
      pancreas_ct_1.dcm
  kidney_cancer/
    ct/
      kidney_ct_1.dcm
  bladder_cancer/
    cystoscopy/
      bladder_cystoscopy_1.jpg
  skin_melanoma/
    dermoscopy/
      melanoma_dermoscopy_1.jpg
```

The top-level folder name is the label the model learns. The scan/image-source folders below it are only for organization; they are not treated as labels.

Supported image types: `.png`, `.jpg`, `.jpeg`, `.tif`, `.tiff`, `.bmp`, `.dcm`, `.dicom`.

Each class needs at least 2 images. For useful results, use many more and keep a mix of lighting, magnification, stain, and cell appearance.

## Train In Google Colab

Use `colab_training.ipynb` for the easiest Colab workflow.

Your dataset zip should contain class folders:

```text
dataset.zip
  dataset/
    no_cancer/
      mri/
        normal_mri_1.dcm
      ct/
        normal_ct_1.png
    brain_cancer/
      mri/
        brain_mri_1.dcm
    leukemia/
      blood_smear/
        leukemia_blood_1.png
    breast_cancer/
      mri/
        breast_mri_1.dcm
```

In Colab:

1. Upload this project folder or notebook to Colab.
2. Run the install cell.
3. Upload your `dataset.zip`.
4. Run the training cell.
5. Download `models/cancer_classifier.joblib`.

Manual Colab command:

```bash
pip install -r requirements-train.txt
python train_model.py --zip-data dataset.zip --output models/cancer_classifier.joblib
```

The trainer automatically extracts the zip and finds the folder that contains at least two populated class folders.

## Setup Instructions

### 1. Clone or Open the Project

```bash
cd Cancer_Detection_Final-main
```

### 2. Create a Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Verify the Python Pipeline

```bash
python -m pytest
```

### 4. Train or Use an Existing Model

Train a new model:

```bash
python train_model.py --data dataset --output models/cancer_classifier.joblib
```

Or use the existing model files in `models/`.

### 5. Run the Streamlit App

```bash
streamlit run app.py -- --model models/cancer_classifier.joblib
```

For the full dashboard:

```bash
streamlit run dashboard.py
```

### 6. Run the FastAPI Backend

```bash
uvicorn api_server:app --reload
```

API health check:

```text
http://127.0.0.1:8000/health
```

Prediction endpoint:

```text
POST http://127.0.0.1:8000/api/v1/predict
```

### 7. Run the Next.js Frontend

```bash
cd nextjs-frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Local Training

```bash
source .venv/bin/activate
python train_model.py --data dataset --output models/cancer_classifier.joblib
```

The trainer prints accuracy, image counts, and a validation report.

## Predict From Command Line

```bash
python predict.py path/to/test-image.png --model models/cancer_classifier.joblib
```

## Run The App

```bash
streamlit run app.py -- --model models/cancer_classifier.joblib
```

Upload an image and the app will show the predicted class, confidence, cancer-cell likelihood, and extracted image evidence.

## Team Members

| Name | Role |
| --- | --- |
| Niranjan K | Frontend Dev |
| Sourav P P | Backend/API development |
| Sanjana  | Reasearch |
| Nishanth R Gowda | Dataset Provider |
| Manikanta J N | PPT |

## Demo Screenshot

Add the final application screenshot at:

```text
docs/demo-screenshot.png
```

Then uncomment or update this image link in the README:

```markdown
![Cancer Detection Demo](docs/demo-screenshot.png)
```


## Notes On Accuracy

The printed validation accuracy is only a basic split of the provided dataset. It does not prove clinical performance. Real medical validation requires expert-labeled datasets, external test sets, bias checks, and clinical review.
