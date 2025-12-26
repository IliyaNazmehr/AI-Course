# Text Summarizer - Group13

A simple but powerful AI text-summarization web app built with Django, the HuggingFace Inference API, and django-allauth for authentication.
Users can enter text, receive an AI-generated summary, and view their personal summary history when logged in.

![image alt](https://github.com/sepanta1/Text-summarizer/blob/main/main_page.png?raw=true)
![image alt](https://github.com/sepanta1/Text-summarizer/blob/main/summary_page.png?raw=true)
![image alt](https://github.com/sepanta1/Text-summarizer/blob/main/history_page.png?raw=true)

## Team members:
   * Sepanta MohammadGholian(40110130117210)
   * Faramarz Daniali(40110130117235)
   * Seyed Younes Hoseini Firozz (40110130117027)
   * Amirali Abedzade
   * Seyed Younes Hoseini Firozz (40110130117027)
   * Mojtaba Marhamati Gashti(40110130117052)
## Features
* AI Text Summarization
  * Uses HuggingFace InferenceClient for high-quality English summaries.
  * Validates input text before processing.
  * Displays both original text and generated summary.
    
* User Authentication (django-allauth)
  * Login using email or username.
  * Registration and logout included.
  * Email verification disabled for development.
 
* Summary History
  * Saves summaries to each logged-in user's history.
  * Paginated history page.
 
* Clean UI

## Setup Instructions

* Clone the repository
```bash
git clone https://github.com/yourusername/text-summarizer.git
cd text-summarizer
```
* Create & activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows
```
* Install dependencies
```bash
pip install -r requirements.txt
```
## Running in Development

* Set api keys
In development, you may store keys inside dev.py, not environment variables.
```python
# dev.py example
SECRET_KEY = "your-dev-secret-key"
HUGGINGFACE_API_KEY = "your-hf-api-key"
```
* Run the development server
```bash
python manage.py runserver
```
## Running in Production

* manage.py includes:
```python
# For production change dev to prod!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject_core.setting.dev')
```
To run in production, edit it to:
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject_core.setting.prod')
```
* Set required environment variables
```bash
export DJANGO_SECRET_KEY="your-production-secret"
export HUGGINGFACE_API_KEY="your-hf-key"
```
* Configure PostgreSQL

> [!TIP]
> If you're new to Django deployment, follow this official guide: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
