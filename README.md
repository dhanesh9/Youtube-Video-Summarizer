# Youtube-Video-Summarizer
This project is a Streamlit application that converts YouTube video transcripts into detailed notes. The application uses Google Generative AI for summarization and includes features such as keyword filtering, clustering, and a question-answering system.

# Features
-Transcript Extraction: Extracts the transcript of a YouTube video using the YouTube Transcript API.

-Summarization: Utilizes Google Generative AI to summarize the transcript into key points.

-Keyword Filtering: Allows users to filter the transcript based on keywords.

-Clustering: Implements KMeans clustering to extract and display important subtopics.Question-Answering: Provides a feature for users to ask questions about the video and get responses based on the transcript.

## Installation

1. **Clone the Repository**:

git clone https://github.com/dhanesh9/Youtube-Video-Summarizer.git
cd Youtube-Video-Summarizer

2.**Create a Virtual Environment**:

For Windows:
python -m venv venv
.\venv\Scripts\activate

For macOS/Linux:
python3 -m venv venv
source venv/bin/activate

3.**Install the Required Packages**:

pip install -r requirements.txt

4.**Create a .env File**:
Create a .env file in the root directory of the project and add your API key:

plaintext
Copy code
GOOGLE_API_KEY=your_google_api_key

## Usage
1. **Run the Streamlit Application**: streamlit run app.py

2. **Enter the YouTube Video Link**:
Paste the YouTube video link into the input field.

3. **Filter Keywords**:
Enter keywords to filter important timestamps (optional).

4. **Generate Detailed Notes**:
Click the "Get Detailed Notes" button to generate and view the detailed notes.

5. **Ask a Question**:
Enter a question about the video content and click "Get Answer" to receive an AI-generated response.
