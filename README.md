# Network Intrusion Detection using Machine Learning

This project develops an advanced **Intrusion Detection System (IDS)** using machine learning to safeguard computer networks. With the increasing volume of network traffic, the threat of cyber-attacks has grown significantly. This system effectively identifies and classifies network connections as either **normal** or **malicious**, providing a robust defense against intruders.

The project leverages the well-known **KDD '99 dataset** and employs an ensemble of machine learning models to achieve high accuracy and a low rate of false positives.

-----

## About The Project

The core objective of this project is to build a highly accurate classifier for network intrusions. This is achieved through a systematic, multi-stage process that includes data preprocessing, exploratory analysis, model training, and a sophisticated ensemble technique to combine the strengths of multiple algorithms.

### Key Features

  * **Comprehensive Data Preprocessing**: The dataset undergoes rigorous cleaning, transformation of symbolic features to numeric ones, and feature selection to ensure the data is clean and non-redundant.
  * **In-Depth Exploratory Data Analysis (EDA)**: Visual tools like **PCA (Principal Component Analysis)** and **t-SNE (t-Distributed Stochastic Neighbor Embedding)** are used to gain a deep understanding of the data's structure and the relationships between different features.
  * **Multiple Classifier Implementation**: Three powerful and distinct machine learning models are trained and evaluated:
      * **Gaussian Naive Bayes**
      * **Decision Tree**
      * **XGBoost**
  * **Advanced Ensemble Modeling**: A **max-voting ensemble** method is used to aggregate the predictions from the individual models. This approach leverages the diversity of the classifiers to produce a more accurate and reliable final prediction.

-----

## Models and Techniques

This project employs a variety of techniques to achieve its goal.

### Building the Classifiers

  * **Gaussian Naive Bayes**: This classifier is a variant of Naive Bayes and is particularly effective with continuous data that follows a Gaussian (normal) distribution. Its simplicity and efficiency make it a great baseline model.
  * **Decision Tree**: A highly intuitive and powerful classifier, the decision tree creates a tree-like model of decisions. It's known for its ease of implementation and interpretation, making it a popular choice for classification tasks.
  * **XGBoost (eXtreme Gradient Boosting)**: This is an advanced and highly efficient implementation of gradient boosting. XGBoost builds decision trees sequentially, with each new tree correcting the errors of the previous one. It's renowned for its high performance and ability to handle complex datasets.

### Ensemble Technique

The project uses a **max-voting ensemble**, a method where multiple models make predictions for each data point. The final prediction is the one that receives the majority of "votes" from the individual models. This approach is highly effective in reducing variance and improving the overall accuracy of the system.

-----

## Results

The results demonstrate that the ensemble model, combining Gaussian Naive Bayes, Decision Tree, and XGBoost, delivers a highly efficient IDS with enhanced performance and a low number of false positives. It's also noteworthy that the **XGBoost classifier alone provides results nearly as effective as the full ensemble model**, showcasing its power as a standalone classifier.

-----

## Getting Started

To get a local copy of this project up and running, follow these simple steps.

### Prerequisites

You'll need **Python 3** and the **pip** package manager.

### Installation and Usage

1.  **Create a virtual environment:**
    ```sh
    pip install virtualenv
    virtualenv ids-env
    source ids-env/bin/activate
    ```
2.  **Clone the repository:**
    ```sh
    git clone https://github.com/adityanegiuk99/Intrusion-Detection-System-using-ML.git
    cd Intrusion-Detection-System/
    ```
3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Download the dataset:**
      * Download the dataset from this [link](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data_10_percent.gz).
      * Place the downloaded file in the same folder as the project.
5.  **Run the project:**
    ```sh
    jupyter notebook
    ```
      * Once Jupyter Notebook opens in your browser, select `IntrusionDetectionSystem.ipynb` to get started\!

-----

## About Us
My name is Aditya Negi. I'm a developer with a strong interest in data science and machine learning, and I'm passionate about using data to build smart, impactful solutions.
This project was developed by a team of individuals passionate about leveraging machine learning to solve real-world challenges in cybersecurity. Our goal is to create effective and accessible tools that can contribute to a safer digital environment. We believe that projects like this can serve as a valuable resource for students, researchers, and professionals in the fields of data science and network security.
