# Q&A Project - Group 20
![image alt](https://github.com/afkarireihaneh/AI-Course/blob/main/Student-Projects/group20/main_page.png?raw=true)
![image alt](https://github.com/afkarireihaneh/AI-Course/blob/main/Student-Projects/group20/eval.png?raw=true)
## Team Members
- Raheleh Afkari (40110130117488)
- Seyedeh Romina Mohammadi (40110130117346)
-  Tina Sadat Seyed Mohammad Lahijani (40110130117477)
- Student 4 (ID)


## Project Title
Persian Question Answering System for Renewable Energy Topics

## Summary
This project implements a Persian-language Question Answering (QA) system focused on renewable energy.  
It uses the pre-trained BERT-based model `SajjadAyoubi/bert-base-fa-qa` from Hugging Face to extract answers from a custom Persian context text about renewable energy sources (solar, wind, hydro, etc.).

Key features:
- Extractive QA pipeline using Transformers
- Text normalization for fair Persian evaluation
- Model evaluation on 50+ question-answer pairs with token-level F1 score
- Simple Flask web interface for interactive questions


## How to Run

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd <project-folder>

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```
### Run the Application
1. Open the Jupyter notebook Q&A_AI.ipynb and run all cells.

    * Running the evaluation cell is optional.

2. Open your browser and go to: http://127.0.0.1:5000

    * Type Persian questions about renewable energy to get answers.
    * Tip: End your questions with a question mark for better results.

### Evaluate the Model
* Run all cells in Q&A_AI.ipynb to:
    * Test the model on the full QA dataset
    * View individual predictions and F1 scores
    * See overall performance metrics

> [!Note]
> The model runs on CPU by default. For faster inference, set device=0 in the pipeline if a compatible GPU is available.
