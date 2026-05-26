from __future__ import annotations

from dataclasses import dataclass


IMAGE_SIZE = (224, 224)

CANCER_CLASSES = (
    "cancer",
    "no_cancer",
    "brain_cancer",
    "leukemia",
    "breast_cancer",
    "lung_cancer",
    "skin_melanoma",
    "colon_cancer",
    "colorectal_cancer",
    "lymphoma",
    "prostate_cancer",
    "soft_tissue_sarcoma",
    "pancreatic_cancer",
    "liver_cancer",
    "kidney_cancer",
    "bladder_cancer",
)


@dataclass(frozen=True)
class CancerClassInfo:
    label: str
    display_name: str
    description: str


CANCER_CLASS_INFO = {
    "cancer": CancerClassInfo(
        label="cancer",
        display_name="Cancer",
        description="Image pattern learned from your cancer training examples.",
    ),
    "no_cancer": CancerClassInfo(
        label="no_cancer",
        display_name="No Cancer",
        description="Image pattern learned from your no-cancer training examples.",
    ),
    "brain_cancer": CancerClassInfo(
        label="brain_cancer",
        display_name="Brain Cancer",
        description="Image pattern learned from your brain-cancer training examples.",
    ),
    "leukemia": CancerClassInfo(
        label="leukemia",
        display_name="Leukemia",
        description="Image pattern learned from your leukemia training examples.",
    ),
    "breast_cancer": CancerClassInfo(
        label="breast_cancer",
        display_name="Breast Cancer",
        description="Image pattern learned from your breast-cancer training examples.",
    ),
    "lung_cancer": CancerClassInfo(
        label="lung_cancer",
        display_name="Lung Cancer",
        description="Image pattern learned from your lung-cancer training examples.",
    ),
    "skin_melanoma": CancerClassInfo(
        label="skin_melanoma",
        display_name="Skin Melanoma",
        description="Image pattern learned from your skin-melanoma training examples.",
    ),
    "colon_cancer": CancerClassInfo(
        label="colon_cancer",
        display_name="Colon Cancer",
        description="Image pattern learned from your colon-cancer training examples.",
    ),
    "colorectal_cancer": CancerClassInfo(
        label="colorectal_cancer",
        display_name="Colorectal Cancer",
        description="Image pattern learned from your colorectal-cancer training examples.",
    ),
    "lymphoma": CancerClassInfo(
        label="lymphoma",
        display_name="Lymphoma",
        description="Image pattern learned from your lymphoma training examples.",
    ),
    "prostate_cancer": CancerClassInfo(
        label="prostate_cancer",
        display_name="Prostate Cancer",
        description="Image pattern learned from your prostate-cancer training examples.",
    ),
    "soft_tissue_sarcoma": CancerClassInfo(
        label="soft_tissue_sarcoma",
        display_name="Soft Tissue Sarcoma",
        description="Image pattern learned from your soft-tissue-sarcoma training examples.",
    ),
    "pancreatic_cancer": CancerClassInfo(
        label="pancreatic_cancer",
        display_name="Pancreatic Cancer",
        description="Image pattern learned from your pancreatic-cancer training examples.",
    ),
    "liver_cancer": CancerClassInfo(
        label="liver_cancer",
        display_name="Liver Cancer",
        description="Image pattern learned from your liver-cancer training examples.",
    ),
    "kidney_cancer": CancerClassInfo(
        label="kidney_cancer",
        display_name="Kidney Cancer",
        description="Image pattern learned from your kidney-cancer training examples.",
    ),
    "bladder_cancer": CancerClassInfo(
        label="bladder_cancer",
        display_name="Bladder Cancer",
        description="Image pattern learned from your bladder-cancer training examples.",
    ),
}
