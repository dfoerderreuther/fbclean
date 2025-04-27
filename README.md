# Facebook Activity Cleaner

> ⚠️ **WARNING** ⚠️
> 
> **THIS SOFTWARE WILL DELETE POSTS, LIKES AND COMMENTS. ACTIONS CANNOT BE UNDONE.**
> 
> **THIS IS NOT A CLICK-AND-RUN SOFTWARE. OBSERVATION AND CODE ADOPTION DURING RUN IS REQUIRED.**
> 
> Please proceed with extreme caution.

This program helps you clean up your Facebook activity history by automatically removing likes and comments from your profile.

## Prerequisites

- Python 3.x
- Chrome browser installed
- Facebook account

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

2. Edit the `.env` file and replace `YOUR_USER_ID` with your Facebook user ID in each URL:
   - `LIKES_URL`: For removing likes
   - `COMMENTS_URL`: For removing comments on posts
   - `GROUP_COMMENTS_URL`: For removing comments in Facebook groups

To find your user ID:
1. Go to your Facebook profile
2. The URL will contain your user ID (e.g., `https://www.facebook.com/10000000012345`)

## Usage

1. Open `main.py`
2. Choose which mode you want to run by uncommenting the desired function call:

```python
if __name__ == "__main__":
    # Uncomment one of these lines to run the desired mode
    # delete_likes(driver)
    # delete_comments(driver)
    # delete_group_comments(driver)
```

3. Run the program:
```bash
python main.py
```

## Features

- **Likes Cleaner**: Removes all your likes on posts, photos, and other content
- **Comments Cleaner**: Removes all your comments on other people's or organization's posts
- **Group Comments Cleaner**: Removes all your comments in Facebook groups

Each mode will:
- Automatically log in to Facebook
- Navigate to your activity page
- Select and remove items
- Refresh the page every 5 iterations to prevent stale content
- Continue until manually stopped (Ctrl+C)

## Notes

- The program uses Selenium with Chrome WebDriver
- It includes automatic page refreshing every 5 iterations to prevent stale content
- The program will continue running until you stop it with Ctrl+C
- Make sure you're logged into Facebook in Chrome before running the program
- The program includes error handling and will retry if it encounters issues

## Troubleshooting

If you encounter any issues:
1. Make sure you're logged into Facebook in Chrome
2. Verify your user ID is correct in the TARGET_URL
3. Check that all dependencies are installed
4. Ensure you have a stable internet connection 