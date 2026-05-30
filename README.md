# Advanced Emotional Intelligence Assessment System

A lightweight Django web application for assessing emotional intelligence through profession-based scenarios and sentiment analysis.

## Project Structure

```
eq_system/
├── app/
│   ├── views.py          # 3 view functions: index, assessment, result
│   ├── models.py         # Assessment database model
│   ├── sentiment.py      # NLTK sentiment analysis
│   ├── utils.py          # Scenarios, questions, profession list
│   └── templates/        # 3 HTML pages
│       ├── index.html
│       ├── assessment.html
│       └── result.html
├── eq_system/            # Django settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static/               # Static files
│   └── css/
│       └── style.css
├── manage.py
├── requirements.txt
└── README.md
```
