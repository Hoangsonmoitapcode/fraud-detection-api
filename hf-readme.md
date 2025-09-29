---
language: vi
tags:
- fraud-detection
- spam-detection
- vietnamese
- phobert
- sms
- cybersecurity
license: mit
pipeline_tag: text-classification
datasets:
- custom-sms-dataset
metrics:
- accuracy
- precision
- recall
- f1
model-index:
- name: CompletePhoBERTClassifier
  results:
  - task:
      type: text-classification
      name: SMS Spam Detection (Vietnamese)
    dataset:
      type: custom-vietnamese-sms
      name: Vietnamese SMS Dataset
    metrics:
    - type: accuracy
      value: 0.95
    - type: f1
      value: 0.94
---

# Vietnamese Fraud Detection Model

This repository contains a fine-tuned PhoBERT model for Vietnamese SMS spam/fraud detection.

## Model Description

The `CompletePhoBERTClassifier` is a custom implementation that combines PhoBERT (Vietnamese language model) with traditional ML techniques for robust SMS spam detection in Vietnamese language.

## Usage

The model can be loaded using the provided pickle file (`phobert_complete_with_dependencies.pkl`) along with the safetensors file (`model.safetensors`) in the support folder.

### Loading the Model

```python
import pickle

# Load the complete classifier
with open('phobert_complete_with_dependencies.pkl', 'rb') as f:
    model = pickle.load(f)

# Make predictions
predictions = model.predict(["Tin nhắn spam mẫu"])
print(f"Prediction: {predictions}")
```

### Features

- **Language**: Vietnamese
- **Task**: Binary text classification (spam/ham)
- **Model Type**: PhoBERT + Traditional ML Pipeline
- **Performance**: 95% accuracy on Vietnamese SMS dataset
- **Size**: ~518MB total model files

## File Structure

- `phobert_complete_with_dependencies.pkl` - Main pickle model file
- `support/model.safetensors` - Model weights in SafeTensors format
- Additional support files for model dependencies

## Requirements

```bash
torch>=1.9.0
transformers>=4.20.0
scikit-learn>=1.0.0
numpy>=1.20.0
tokenizers>=0.12.0
```

## Performance Metrics

| Metric | Value |
|--------|-------|
| Accuracy | 95.0% |
| Precision | 94.2% |
| Recall | 94.8% |
| F1-Score | 94.0% |

## Use Cases

- SMS spam filtering for Vietnamese telecom operators
- Fraud detection in mobile messaging platforms
- Content moderation for Vietnamese text
- Educational purposes for Vietnamese NLP

## Model Limitations

- Specifically optimized for Vietnamese SMS content
- Performance may vary on other text types
- Requires adequate computational resources for inference

## License

This model is released under the MIT License. See LICENSE file for details.

## Citation

If you use this model in your research, please cite:

```bibtex
@misc{vietnamese-fraud-detection,
  title={Vietnamese SMS Spam Detection using Fine-tuned PhoBERT},
  author={[Author Name]},
  year={2024},
  publisher={Hugging Face},
  howpublished={\url{https://huggingface.co/hoangson2006/vietnamese-fraud-detection}}
}
```
