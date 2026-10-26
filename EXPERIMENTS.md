# Model Training Log

| Date             | Inputs Used                                                                                                         | Model                  | Final Accuracy |
| :--------------- | :------------------------------------------------------------------------------------------------------------------ | :--------------------- | :------------- |
| 2026-09-29 14:06 | Title + Description (TF-IDF max 1000)                                                                               | Logistic Regression    | 51.43%         |
| 2026-09-29 14:07 | Title + Description (TF-IDF max 100)                                                                                | Logistic Regression    | 65.71%         |
| 2026-09-29 14:26 | Title + Description (TF-IDF max 100)                                                                                | Logistic Regression    | 65.71%         |
| 2026-09-29 14:30 | Title + Description (TF-IDF max 1000)                                                                               | Logistic Regression    | 51.43%         |
| 2026-09-29 14:30 | Title + Description (TF-IDF max 75)                                                                                 | Logistic Regression    | 65.71%         |
| 2026-09-29 14:30 | Title + Description (TF-IDF max 125)                                                                                | Logistic Regression    | 57.14%         |
| 2026-09-29 14:39 | Title + Description (TF-IDF max 100)                                                                                | Logistic Regression    | 65.71%         |
| 2026-09-29 14:39 | Title + Description (TF-IDF max 100)                                                                                | Random Forest          | 71.43%         |
| 2026-10-03 14:13 | Title + Description (TF-IDF max 100)                                                                                | Multi-Layer Perceptron | 68.57%         |
| 2026-10-03 14:14 | Title + Description (TF-IDF max 150)                                                                                | Multi-Layer Perceptron | 68.57%         |
| 2026-10-03 14:21 | Title + Description (TF-IDF max 100)                                                                                | Support Vector Machine | 68.57%         |
| 2026-10-03 14:21 | Title + Description (TF-IDF max 100)                                                                                | Naive Bayes            | 71.43%         |
| 2026-10-21 10:56 | Title + Description (TF-IDF max 100)                                                                                | Logistic Regression    | 65.71%         |
| 2026-10-21 10:56 | Title + Description (TF-IDF max 100)                                                                                | Random Forest          | 71.43%         |
| 2026-10-21 10:56 | Title + Description (TF-IDF max 100)                                                                                | Multi-Layer Perceptron | 68.57%         |
| 2026-10-21 10:56 | Title + Description (TF-IDF max 100)                                                                                | Support Vector Machine | 68.57%         |
| 2026-10-21 10:56 | Title + Description (TF-IDF max 100)                                                                                | Naive Bayes            | 71.43%         |
| 2026-10-21 11:19 | Title + Description (TF-IDF max 100; word n-grams 1-1; stratified 80/20 holdout, seed 42; LR C=10)                  | Logistic Regression    | 71.43%         |
| 2026-10-21 11:19 | Title + Description (TF-IDF max 100; word n-grams 1-1; stratified 80/20 holdout, seed 42)                           | Random Forest          | 74.29%         |
| 2026-10-21 11:19 | Title + Description (TF-IDF max 100; word n-grams 1-1; stratified 80/20 holdout, seed 42)                           | Multi-Layer Perceptron | 65.71%         |
| 2026-10-21 11:19 | Title + Description (TF-IDF max 100; word n-grams 1-1; stratified 80/20 holdout, seed 42)                           | Support Vector Machine | 65.71%         |
| 2026-10-21 11:19 | Title + Description (TF-IDF max 100; word n-grams 1-1; stratified 80/20 holdout, seed 42)                           | Naive Bayes            | 74.29%         |
| 2026-10-21 11:36 | Title + Description (TF-IDF analyzer word; max 250; n-grams 1-1; stratified 80/20 holdout, seed 42; LR C=10)        | Logistic Regression    | 65.71%         |
| 2026-10-21 11:36 | Title + Description (TF-IDF analyzer word; max 500; n-grams 1-1; stratified 80/20 holdout, seed 42; LR C=10)        | Logistic Regression    | 68.57%         |
| 2026-10-21 11:36 | Title + Description (TF-IDF analyzer word; max 100; n-grams 1-1; stratified 80/20 holdout, seed 42; NB alpha=0.1)   | Naive Bayes            | 71.43%         |
| 2026-10-21 11:36 | Title + Description (TF-IDF analyzer word; max 100; n-grams 1-1; stratified 80/20 holdout, seed 42; NB alpha=0.5)   | Naive Bayes            | 71.43%         |
| 2026-10-21 11:36 | Title + Description (TF-IDF analyzer word; max 100; n-grams 1-1; stratified 80/20 holdout, seed 42; NB alpha=2)     | Naive Bayes            | 71.43%         |
| 2026-10-21 11:36 | Title + Description (TF-IDF analyzer char_wb; max 1000; n-grams 3-5; stratified 80/20 holdout, seed 42; LR C=1)     | Logistic Regression    | 68.57%         |
| 2026-10-21 11:36 | Title + Description (TF-IDF analyzer char_wb; max 1000; n-grams 3-5; stratified 80/20 holdout, seed 42)             | Random Forest          | 80.00%         |
| 2026-10-21 11:36 | Title + Description (TF-IDF analyzer char_wb; max 1000; n-grams 3-5; stratified 80/20 holdout, seed 42)             | Multi-Layer Perceptron | 71.43%         |
| 2026-10-21 11:36 | Title + Description (TF-IDF analyzer char_wb; max 1000; n-grams 3-5; stratified 80/20 holdout, seed 42)             | Support Vector Machine | 74.29%         |
| 2026-10-21 11:36 | Title + Description (TF-IDF analyzer char_wb; max 1000; n-grams 3-5; stratified 80/20 holdout, seed 42; NB alpha=1) | Naive Bayes            | 65.71%         |
| 2026-10-22 21:48 | Title + Description (TF-IDF analyzer char_wb; max 1000; n-grams 3-5; stratified 80/20 holdout, seed 42)             | Random Forest          | 80.00%         |
| 2026-10-23 01:03 | Title + Description (TF-IDF analyzer char_wb; max 1000; n-grams 3-5; stratified 80/20 holdout, seed 42)             | Random Forest          | 80.00%         |
| 2026-10-23 02:35 | Title + Description (TF-IDF analyzer char_wb; max 1000; n-grams 3-5; stratified 80/20 holdout, seed 42)             | Random Forest          | 80.00%         |
