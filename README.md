# Retrieve Information from YouTube Videos in Private and Public Playlists Using the YouTube Data API v3

This Python application allows you to fetch information (e.g., URL, title) from **public YouTube playlists** and your **private YouTube playlists** using the YouTube Data API v3.
The application extracts all information from the playlists into CSV files and generates an additional summary CSV file, containing details of all retrieved videos across all playlists.

## Features

- Fetch information for **private** and **public playlists** (ID, URL, title). It does **not** retrieve saved playlists from other users or the **'Watch Later'** playlist.
- Uses **OAuth 2.0** for authentication.
- Exports the retrieved data into CSV files in an `output` directory

## Dependencies

This project uses the following Python main libraries (dependencies in `requirements.txt`):

- `pandas` - for data manipulation and analysis (https://pandas.pydata.org/)
- `yt-dlp` - for retrieving video information from public playlists (https://github.com/yt-dlp/yt-dlp)
- `tqdm` - for displaying progress bar (https://github.com/tqdm/tqdm)
- `google-auth-oauthlib` - for handling OAuth 2.0 authentication with Google APIs (https://github.com/googleapis/google-auth-library-python-oauthlib)
- `google-api-python-client` - for interacting with Google APIs, including YouTube Data API (https://github.com/googleapis/google-api-python-client)

## Requirements

- Python 3.12.5
- YouTube (Google Cloud) account (free) and Google Cloud Project (free) with **YouTube Data API v3** enabled (see Option 2 below)

---

## Setup Instructions

1. Install required dependencies:
```bash
pip install -r requirements.txt
```
2. Populate the `playlist_list` for fetching public playlists (see Option 1 below) or leave empty to retrieve private playlists (see Option 2 below).  


## Execution Instructions
### Option 1: Fetch Public Playlists
#### 1. Enter the public playlist links in the 'playlists_list' variable. Example:
```python
playlists_list = [
  "https://www.youtube.com/playlist?list=PL0lo9MOBetEF_de7yKAWpnMkTsKH6aJ4P",
  "https://www.youtube.com/playlist?list=PLFPUGjQjckXHAVzDxBpjXENRKgVU6KCzF"
]
```

#### 2. Run the script:
 ```bash
 python main.py
 ```

### Option 2: Fetch Your Private and Public Playlists

Retrieve private and public playlists from your YouTube account. 

1. **Empty the `playlists_list`** in `main.py`:
```python
playlists_list = []
```


2. **Create a Google Cloud Project:**

   - Go to the [Google Cloud Console](https://console.cloud.google.com).
   - Navigate to **API & Services > Dashboard**.
   - In the left sidebar, click on **Library**.
   - In the search bar, type **YouTube Data API v3** and select it.
   - Click **Enable** to enable the API for your project.


3. **Set Up OAuth 2.0 Credentials:**

   - In the left sidebar, navigate to **API & Services > Credentials**.
   - Click **Create Credentials** and choose **OAuth 2.0 Client IDs**.


4. **Configure the OAuth Consent Screen:**

   - In the sidebar, go to **OAuth consent screen**.
   - Select **User Type** as **External**.
   - Fill out the app information (app name, user support email, and developer contact info).
   - Under **Scopes**, click **Add or Remove Scopes** and add the following scope:
       - `https://www.googleapis.com/auth/youtube.readonly` (to access private YouTube playlists).
   - Click **Save** once done.


5. **Create OAuth 2.0 Credentials:**

   - After configuring the OAuth consent screen, go back to the **Credentials** page.
   - Click **Create Credentials > OAuth 2.0 Client IDs**.
   - For **Application Type**, choose **Desktop App**.
   - Name your client (e.g., "YouTube Playlist Access").
   - Click **Create**.


6. **Download the `client_secrets.json` File:**

   - Download the `client_secrets.json` file from the Google Cloud Console.


7. **Rename and Set Path in `main.py`:**

   - Optionally, rename the `client_secrets.json` file if desired.
   - Set the path to the `CLIENT_SECRET_FILE` in `main.py`.


8. **Add Test Users:**

   - In the left sidebar, go to **API & Services > OAuth consent screen**.
   - Under the **Test users** section, add the email addresses of users who should have access to the app.
   - Add your own email address to the list.


9. **Run the `main.py` Script:**

   - Run `main.py` with an empty playlist:
     ```bash
     python main.py
     ```

   - When prompted, log in and click **Continue** twice if required.

---
## Important Security Notice

**Warning:** The `client_secrets.json` file contains sensitive information, including your OAuth credentials. You **must** treat handle this file carefully to avoid exposing your secrets.

- **Do not upload** the `client_secrets.json` file to public repositories or share it with others.
- If the `client_secrets.json` file is in the same directory as your project, add it to your `.gitignore` file to avoid accidentally pushing it to GitHub.

## Authors
**Manuel V.**

[@gnxmanu](https://github.com/gnxmanu)

## Version History
* v1.0 –––––– Public Release. December 18, 2024

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.