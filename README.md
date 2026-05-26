# Vayu Vectors - OnCoLens AI
# Cancer Detection AI

An educational Streamlit app for training and testing image-based cancer detection models. The project supports multiple trained `.joblib` models and lets the user choose the correct model before uploading a medical image.

The current app includes model selection, image quality checks, unsupported-image rejection, prediction history, readable evidence labels, and downloadable text reports.

## Important Medical Notice

This project is a research and education prototype only.

It is not clinically validated and must not be used for diagnosis, treatment decisions, or ruling out cancer. Always consult qualified medical professionals for real medical interpretation.

## Current Models

Trained using over 27 thousand images
trained models placed inside the `models/` folder.

```text
models/
  Brain.joblib       Brain cancer model
  Breast.joblib      Breast cancer model
  Lung.joblib        Lung cancer model
  pan.joblib         Pancreatic cancer model
  pro.joblib         Prostate cancer model
```

The Streamlit dropdown is configured in `app.py`:

```python
MODEL_OPTIONS = {
    "Brain cancer model": Path("models/Brain.joblib"),
    "Breast cancer model": Path("models/Breast.joblib"),
    "Lung cancer model": Path("models/Lung.joblib"),
    "Pancreatic cancer model": Path("models/pan.joblib"),
    "Prostate cancer model": Path("models/pro.joblib"),
}
```

## Features

- Select from multiple cancer models
- Upload `.png`, `.jpg`, `.jpeg`, `.tif`, `.tiff`, `.bmp`, `.dcm`, or `.dicom` files
- Reject random or unsupported images before prediction
- Show confidence, cancer-cell likelihood, and reliability level
- Display top class probabilities
- Show readable image evidence such as texture complexity and image contrast
- Keep recent prediction history in the sidebar
- Download a text report for each prediction
- Train new `.joblib` models locally or in Google Colab

## Project Structure

```text
app.py                         Streamlit web app
predict.py                     Command-line prediction script
train_model.py                 Training entry point
colab_training.ipynb           Google Colab training notebook
requirements.txt               App dependencies
requirements-train.txt         Smaller Colab training dependency list
models/                        Trained .joblib model files
dataset/                       Optional local training dataset
tests/                         Pipeline tests
src/cancer_detector/
  config.py                    Cancer class display metadata
  preprocessing.py             Image and DICOM loading
  feature_extractor.py         Image feature extraction
  models.py                    Model loading and prediction wrapper
  training.py                  Dataset extraction and training logic
  inference.py                 Prediction pipeline
  reporting.py                 Basic report helpers
```

## Dataset Format

Training data must be arranged with one top-level folder per class. The folder name becomes the model label.

Example for lung cancer:

```text
dataset/
  no_cancer/
    Normal case (1).jpg
    Normal case (2).jpg
  lung_cancer/
    Malignant case (1).jpg
    Malignant case (2).jpg
```

Subfolders are allowed for organization:

```text
dataset/
  no_cancer/
    ct/
      normal_1.png
  pancreatic_cancer/
    ct/
      pancreas_ct_1.png
    mri/
      pancreas_mri_1.png
    histopathology/
      pancreas_slide_1.jpg
```

Supported image types:

```text
.png, .jpg, .jpeg, .tif, .tiff, .bmp, .dcm, .dicom
```

Each class needs at least 2 images. For useful results, use many more images and keep the image type consistent with the selected model.

## Local Setup

From the project root:

```bash
cd "Cancer detection"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run The App

```bash
cd "Cancer detection"
source .venv/bin/activate
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Train Locally

Train from a local `dataset/` folder:

```bash
cd "Cancer detection"
source .venv/bin/activate
python train_model.py --data dataset --output models/cancer_classifier.joblib
```

Train a specific model file:

```bash
python train_model.py --data dataset --output models/Lung.joblib
python train_model.py --data dataset --output models/pan.joblib
python train_model.py --data dataset --output models/pro.joblib
```

The trainer prints accuracy, class names, image counts, and a validation report.

## Train In Google Colab

Use `colab_training.ipynb` for the easiest workflow.

Manual Colab steps:

1. Upload the project files to Colab.
2. Upload a dataset zip such as `lung.zip`.
3. Install training dependencies:

```python
!pip -q install -r requirements-train.txt
```

4. Train from the zip:

```python
!python train_model.py --zip-data "lung.zip" --output models/Lung.joblib
```

For pancreatic cancer:

```python
!python train_model.py --zip-data "pancreatic.zip" --output models/pan.joblib
```

For prostate cancer:

```python
!python train_model.py --zip-data "prostate.zip" --output models/pro.joblib
```

5. Download the trained model:

```python
from google.colab import files
files.download("models/Lung.joblib")
```

The trainer automatically extracts the zip and finds a dataset folder with at least two populated class folders.

## Command-Line Prediction

```bash
cd "Cancer detection"
source .venv/bin/activate
python predict.py path/to/image.png --model models/Lung.joblib
```

## Adding A New Model To The App

1. Put the trained file in `models/`.

Example:

```text
models/kidney.joblib
```

2. Add it to `MODEL_OPTIONS` in `app.py`:

```python
"Kidney cancer model": Path("models/kidney.joblib"),
```

3. Add guidance to `MODEL_GUIDANCE`:

```python
"Kidney cancer model": "Upload kidney CT, MRI, or histopathology medical images.",
```

4. Restart Streamlit.

## Troubleshooting

If training says no supported images were found, check the folder layout:

```bash
find dataset -maxdepth 2 -type f | head
find dataset/no_cancer -type f | head
find dataset/lung_cancer -type f | head
```

If `dataset/lung_cancer` does not exist, train from the zip instead:

```bash
python train_model.py --zip-data lung.zip --output models/Lung.joblib
```

If the app shows an unsupported-image message, the uploaded image probably does not match the selected model type. Choose the correct model or upload a scan/pathology image similar to the training data.

If a cancer image is predicted as `no_cancer`, improve the dataset and retrain. Use more cancer examples from the same image type, reduce mismatch between training and testing images, and verify that the correct model is selected.

## Notes On Accuracy

The printed validation accuracy is only a basic split of the provided dataset. It does not prove clinical performance. Real medical validation requires expert-labeled datasets, external test sets, bias checks, and clinical review.
