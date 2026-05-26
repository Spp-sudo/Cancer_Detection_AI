# Cancer Type Detection Model

A module-wise AI/ML project for training an image classifier from folders. Each folder becomes one class, so you can train `no_cancer` separately from each cancer type.

Example classes:

- `no_cancer`
- `brain_cancer`
- `breast_cancer`
- `lung_cancer`
- `prostate_cancer`
- `pancreatic_cancer`
- `cancer` for mixed or unknown cancer images

The model saves a trained `.joblib` file that can be used from the command line or the Streamlit app.

## Medical Notice

This is an educational prototype. It is not clinically validated and must not be used for real diagnosis, treatment, or ruling out cancer.

## Project Structure

```text
app.py                         Streamlit image upload app
colab_training.ipynb           Google Colab training notebook
predict.py                     Command-line prediction script
train_model.py                 Training entry point
requirements.txt               Python dependencies
requirements-train.txt         Smaller dependency list for Colab training
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

Use [colab_training.ipynb](</home/ace/Documents/CODE/HACKATHON/2026 - Code A Thon/Cancer detection/colab_training.ipynb>) for the easiest Colab workflow.

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

## Local Setup

```bash
cd "Cancer detection"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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
