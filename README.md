# Named entity recognition on personally identifiable information

## Contents

- model

  - taggers

    - pii-ner-v1

      - final_model.pt : A trained flair model for ner inference.

- data

  - PII_Train_Large_Data_Test_Data.xlsx: Original Data File

  - PII_Predictions_v1.xlsx: Inference Output File

- src

  - train_ner.ipynb: notebook detailing the steps to train a flair model and sample predictions

  - inference.ipynb: notebook detailing the steps to perform inference on the eval data and export to excel

  - evaluate_ner.ipynb: notebook detailing the evaluation measures

  - evaluation_report.text: output from evaluate_ner.ipynb

  - rules.py: regex helper script

  - preprocess.py: data formatting util

  - datagen.py: fake data generation helper

- ner.yaml: conda env export > ner.yaml (environment details)
