# X (Twitter) AI Agent - Ice Breaker

An AI-powered application that generates personalized ice breakers and conversation topics based on a person's Twitter activity.

## Features

-  Twitter profile lookup and tweet analysis
-  AI-powered personality insights
-  Custom ice breakers and conversation starters
-  Interest topics identification
-  Clean web interface

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your environment variables in `.env`:
   - OpenAI API key
   - SerpAPI key (for Twitter profile search)
   - Twitter API credentials

4. Run the application: `python app.py`

## Note

This application was previously called "LangChain Ice Breaker" and included LinkedIn functionality via ProxyCurl API. Due to ProxyCurl's service shutdown, the application now focuses exclusively on Twitter/X data for generating insights.

## Usage

1. Enter a person's name
2. The app will find their Twitter profile
3. Analyze their recent tweets
4. Generate personalized ice breakers and conversation topics

## Requirements

- Python 3.8+
- OpenAI API access
- Twitter API access (Bearer token)
- SerpAPI key