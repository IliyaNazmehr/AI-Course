#Group 15

# 🎬 Movie Recommendation Chatbot (AI-Based)

Welcome! This project is an intelligent Movie Recommendation Chatbot powered by **TMDb API** and implemented using **TF-IDF Vectorization** and **Cosine Similarity** techniques.

Users can simply enter their favorite movie title, and the system will analyze the plot summaries to recommend the top 5 most similar movies.

---

## 1. Problem Statement

In the modern era of streaming, users often feel overwhelmed by the vast number of movie choices. 
- **The Challenge:** Building a simple yet effective system that suggests movies based on content similarity.
- **Application:** Helping users discover new content that aligns with their specific tastes.
- **Importance:** Enhances user engagement and saves time by providing personalized recommendations instantly.

---

## 2. Theoretical Background

To understand how the chatbot "thinks," we utilized two main concepts from Natural Language Processing (NLP):

* **TF-IDF (Term Frequency-Inverse Document Frequency):** This algorithm converts movie overviews (text) into a numerical format (vectors). It gives more weight to unique and meaningful words while ignoring common stop words.
* **Cosine Similarity:** This is used to calculate the distance between two vectors. By measuring the cosine of the angle between movie vectors, the system determines how closely related two movies are.
* **TMDb API:** We chose this as our primary data source because:
    - It provides a massive, real-time database of movies.
    - No manual data entry is required; the data is always up-to-date.
    - It is developer-friendly and ideal for educational AI projects.

---

## 3. Dataset & Data Source

The project does not rely on a static CSV file. Instead, it fetches live data from **The Movie Database (TMDb)**.
Each movie entry includes:
- **Title:** The official name of the movie.
- **Overview:** A text-based summary of the plot used for similarity analysis.
- **Movie ID:** Used to fetch additional details via the API.

---

## 4. Implementation Details

- **Programming Language:** Python  
- **Key Libraries & Frameworks:**
  - `streamlit`: For creating the interactive web-based user interface.
  - `tmdbv3api`: A Python wrapper to interact with the TMDb API.
  - `pandas`: Used for efficient data manipulation and structuring.
  - `scikit-learn`: Specifically for `TfidfVectorizer` and `cosine_similarity`.

- **Workflow:**
  1. User inputs a movie title in the Streamlit search bar.
  2. The program queries the TMDb API to find the specific movie.
  3. The system retrieves overviews for a set of related movies.
  4. The TF-IDF model is built on these summaries.
  5. Cosine Similarity is calculated, and the top 5 most similar movies are displayed.

---

## 5. Future Improvements (Next Steps)
To make this project even more powerful, the following features can be added:
- [ ] **Hybrid Filtering:** Combining Content-based filtering with Collaborative filtering (user ratings).
- [ ] **Sentiment Analysis:** Analyzing user reviews to improve recommendations.
- [ ] **Genre-based Tuning:** Giving more weight to movies within the same genre.
- [ ] **Deployment:** Hosting the app on Streamlit Cloud or Heroku.

---

## 6. Installation & How to Run

Follow these steps to run the project locally:

1. **Clone the project:**
   ```bash
   git clone [https://github.com/your-username/movie-chatbot.git]
   cd movie-chatbot

2. **Install required packages:**
   pip install streamlit tmdbv3api pandas scikit-learn

3. **Launch the application:**
   streamlit run app.py

---

## 🎓 Academic Information

* **Course:** [Artificial Intelligence]
* **Supervised by:** [Prof.Haji Esmaeili]
* **Teaching Assistant:** [Mr.Nazmehr]
* **University:** [Islamic Azad University-Tehran Central Branch]

### 👥 Development Team
* **[Aryanaz Minoui]** - Student ID: `[40010130117287]`
* **[Your Friend's Name]** - Student ID: `[40010130117283]`
