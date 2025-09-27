# Models Directory

This directory contains all model files and related assets.

## Structure

```
models/
├── trained/              # Trained model files
│   ├── config.json       # Model configuration
│   ├── model.safetensors # Model weights (or pytorch_model.bin)
│   ├── tokenizer_config.json
│   ├── vocab.txt
│   └── bpe.codes
├── backups/              # Model backups
└── exports/              # Exported models for deployment
```

## Usage

- Place your trained model files in `trained/` folder
- Keep backups of working models in `backups/`
- Export deployment-ready models to `exports/`

## Model Files

- **config.json**: Model configuration and metadata
- **model.safetensors**: Model weights (preferred) or pytorch_model.bin
- **tokenizer_config.json**: Tokenizer configuration
- **vocab.txt**: Vocabulary file
- **bpe.codes**: BPE encoding file
