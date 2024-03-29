# Guide to Using the VnExpress Comments Crawler Program

## Introduction
This program is written in Python and uses the Selenium and BeautifulSoup libraries to collect comment data from the VnExpress website and export it to an Excel file.

## System Requirements
- Python 3.x (latest version recommended)
- Chrome browser (version compatible with ChromeDriver)

## Installation
1. Download and install Python from the official website: https://www.python.org/downloads/
2. Open the Command Prompt (cmd) or Terminal
3. Install the required libraries using the following command:
   ```
   pip install selenium beautifulsoup4 openpyxl
   ```
4. Download the ChromeDriver compatible with your Chrome browser version from https://sites.google.com/a/chromium.org/chromedriver/downloads
5. Extract the ChromeDriver file and place it in the directory `E:/VnExpressCrawlData/CrawVnexpress/chromedriver_win32/`

## Usage
1. Open the `crawler.py` file using a text editor (such as Notepad, Sublime Text, or Visual Studio Code)
2. On line 66, change the URL of the VnExpress article from which you want to collect comment data. For example:
   ```python
   driver.get("https://vnexpress.net/ma-doc-nham-toi-nguoi-dung-iphone-viet-nguy-hiem-the-nao-4725781.html")
   ```
3. Save the `crawler.py` file
4. Open the Command Prompt (cmd) or Terminal
5. Navigate to the directory containing the `crawler.py` file using the `cd` command. For example:
   ```
   cd E:\VnExpressCrawlData\CrawVnexpress
   ```
6. Run the program using the command:
   ```
   python crawler.py
   ```
7. The program will automatically collect comment data from the VnExpress article and export it to an `Vnexpress_comment.xlsx` file in the same directory

## Notes
- The data collection process may take some time depending on the number of comments in the article.
- Do not close the Command Prompt (cmd) or Terminal window while the program is running.
- If you encounter any errors, double-check the installation steps and ensure that you have installed the correct version of ChromeDriver compatible with your Chrome browser.

Happy data collecting!# VnExpress-Comment-Crawler
