# Indonesian Hate Speech Tweet API Cleansing

This project is a challenge from Binar Academy aimed at building an API for cleansing Indonesian Hate Speech Tweet data from [Kaggle](https://www.kaggle.com/datasets/ilhamfp31/indonesian-abusive-and-hate-speech-twitter-text/code) and conducting a comprehensive analysis.

## Installation

To get started, install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

Run the application using the following command:

```bash
python app.py
```

## API

Access the API documentation by opening [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs) in your browser. The API offers two endpoints:

### 1. clean_teks

This endpoint requires inputting text and several additional parameters for processing.

```http
  POST /clean_teks
```

![image](https://github.com/imadaka19/24001074-18-iak-cleantweet-gold/assets/74599441/8aae3b2b-daa3-4405-99c7-220687837e00)

### 2. text-processing-file

This endpoint requires inputting a CSV file with specified columns for processing.

```http
  POST /text-processing-file
```

![image](https://github.com/imadaka19/24001074-18-iak-cleantweet-gold/assets/74599441/0cd5becb-d12b-48ba-bae9-dc125f95e8ff)

Those APIs will automatically import data to database as **tweet_table**.

The database will be saved in your local named **"challenge_database.db"**

Feel free to explore and integrate these APIs for effective cleansing and analysis of Indonesian Hate Speech Tweet data.
