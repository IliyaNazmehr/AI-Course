#Youtube Sentiment Analysis on iPhone 17 During September–October 2025

## 👥 Team Name
Tweetelligence

## 👤 Team Members
- Arian Khoshkholgh
- mohammad matin charkhand
- Mohammad Yusef Saadatzadeh
- Hasti Azimi
- Shayan Eskandari


## ✨ Project Description
This project focuses on analyzing youtube users’ sentiments toward the iPhone 17. By collecting and processing comments related to the product, we aim to identify users’ opinions and emotional reactions. The results provide insights into public perception of the iPhone 17 during the specified time period.


## 🎯 Project Objective
The goal of this project is to analyze Twitter users’ sentiments toward the iPhone 17 by examining their tweets. This analysis aims to understand public opinion and emotional responses related to the product.

This project analyzes YouTube comments about **iPhone 17** using a three-step pipeline:
⚠️pay attention: Becuase of limitations we can't access to twitter's token . so we shift to YouTube for collecting data.

![Pipeline](https://i.imgur.com/J4Gaiv9.png)

**Steps:**

1. **Scraping & Initialization** – Extract comments with **Selenium** and set up the environment.  
2. **Text Cleaning & Preprocessing** – Clean and normalize text for analysis.  
3. **Sentiment Analysis & Visualization** – Classify comments as Positive, Negative, or Neutral using **TextBlob** and **Matplotlib** and generate a **WordCloud**.
 
## 📂 Dataset

The dataset consists of YouTube comments collected specifically using the keywords **"آیفون 17"** and **"iPhone 17"**. The data was gathered between September and October 2025.

Each comment includes the following fields:
- `comment_text`: The text content of the comment
- `author`: The username of the commenter
- `timestamp`: Date and time when the comment was posted

The raw data is stored in **CSV format** and handled using the **Pandas** library in Python. 
After preprocessing, cleaned data is saved in a separate directory (`data/processed/`) for downstream analysis.

## 🛠 Technologies & Tools

The project is implemented using the following tools and libraries:

- **Programming Language:** Python 3.x
- **Web Automation & Scraping:** Selenium WebDriver
- **Data Handling & Processing:** Pandas, Regex
- **Natural Language Processing (NLP):** NLTK, TextBlob
- **Visualization:** Matplotlib, WordCloud

## ⚙️ Methodology

The project follows a clear, pipeline-oriented methodology:

1. **Data Collection (Scraping)**
   - YouTube comments are collected using Selenium WebDriver.
   - Keywords used: "آیفون 17" and "iPhone 17".
   - Output: CSV file containing comment text, author, and timestamp.

2. **Data Cleaning / Preprocessing**
   - Removes special characters, links, emojis, and empty comments.
   - Normalizes text (lowercasing, removing duplicates).
   - Output: Cleaned dataset ready for analysis.

3. **Sentiment Analysis**
   - Uses **TextBlob** to classify each comment into **Positive**, **Negative**, or **Neutral** categories.

4. **Visualization**
   - Generates **WordClouds** to highlight the most frequently mentioned words.
   - Words with higher frequency appear larger and bolder, providing an intuitive overview of the discussion topics.
   - Uses **Matplotlib** to render and customize visual outputs for clearer interpretation and presentation of results.
## 🚀 How To run
### Step 1: Selenium-Based Scraping & Project Initialization

The first script is responsible for initializing the project workflow and performing web scraping using **Selenium**.

The execution flow of this script is as follows:

- Importing all required libraries and dependencies.
- Launching a browser instance via Selenium WebDriver.
- Navigating to the YouTube homepage.
- Redirecting to the target video URL.
- Preparing the environment for subsequent data extraction processes.

This step establishes the initial connection to the web source and ensures that
the browser session is correctly configured before any scraping or data
collection operations begin.


### Step 2: Text Cleaning & Data Preprocessing

The second script is responsible for cleaning and preprocessing the raw textual
data extracted from YouTube comments.

This stage focuses on removing noise and irrelevant elements from the text in
order to prepare the data for downstream analysis. The main operations include:

- Removing special characters, symbols, and punctuation.
- Eliminating unnecessary words and repeated tokens.
- Normalizing text format (e.g., lowercasing).
- Handling empty or invalid comments.

This data cleaning step ensures that the resulting dataset is consistent,
readable, and suitable for sentiment analysis and machine learning models.


### Step 3: Sentiment Analysis & Visualization

In this stage, Natural Language Processing (NLP) techniques are applied to analyze
the cleaned YouTube comments.

Sentiment analysis is performed using the **TextBlob** library. Three sentiment
scores are computed for each comment, enabling classification into the following
categories:

- **Positive**
- **Negative**
- **Neutral**

Based on these sentiment scores, each comment is automatically assigned to one
of the sentiment classes.

In addition to sentiment classification, a **WordCloud** visualization is
generated to highlight the most frequently occurring words in the comments
related to *iPhone 17*. Words with higher frequencies are displayed more
prominently (in larger and bolder fonts), providing an intuitive overview of the
dominant discussion topics.



```bash
pip install -r requirements.txt
```
## 📊 Results

### 🎯 Summary
This project performed sentiment analysis on the dataset.  
The distribution of sentiments is as follows:

### 📈 Results Table
| Sentiment | Count | Percentage |
|-----------|-------|------------|
| Positive  | 29    | 39.19%     |
| Neutral   | 28    | 37.84%     |
| Negative  | 17    | 22.97%     |

### 🔑 Key Points
- ✅ The majority of the data is Positive  
- ⚠️ Negative sentiments are the least represented  
- 📌 Approximately 38% of the data is Neutral

![Result](https://i.imgur.com/k7PUbn7.jpeg)
![Result](https://i.imgur.com/u0p1Dlj.jpeg)
![Result](https://i.imgur.com/CrKbV49.jpeg)
