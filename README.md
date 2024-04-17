# Web-crawling-tool-for-NGO

This project is a web crawling tool specifically designed for Non-Governmental Organizations ([NGOs](https://fundusze.ngo.pl/aktualne)). It aims to automate the process of gathering relevant data and scheduling data extractions in order to keeping users up to date with newest oportunities.

[![Video](https://img.youtube.com/vi/VddchMtT9Aw/maxresdefault.jpg)](https://www.youtube.com/watch?v=VddchMtT9Aw)

## Features
 **Efficient Web Crawling**: The tool uses Scrapy, a fast and powerful scraping and web crawling framework. It is capable of crawling multiple websites concurrently, ensuring efficient data collection.
- **Data Extraction Speed**: The data extraction process is optimized for speed, and RedisStack is used to manage the workload.
- **Browser Automation**: With Playwright, the tool can automate browser tasks, which is particularly useful for crawling dynamic websites.
- **Tailored Offers**: The tool uses OpenAI to analyze user descriptions and tailor offers accordingly, providing a personalized experience for the users.
- **User Interface**: A user-friendly GUI is provided using Tkinter, making the tool easy to use even for non-technical users.
- **Proxies and User Agents**: Easy proxies and user agents integration to prevent IP blocking and ensure uninterrupted web crawling.

## Future Scope
Future enhancements to this tool may include:
- **Ability to Crawl More Complex and Dynamic Websites**: To expand the scope of data collection.
- **Scheduling Extractions**: Implementing cron jobs or using [Scrapyd](https://scrapyd.readthedocs.io/en/stable/) to schedule data extraction tasks.
- **Email Notifications**: Sending the newest notifications via email to keep users updated with the latest information.
- **Improved Data Extraction Accuracy**: To ensure the quality of the data collected.
- - **Advanced Data Analysis Features**: To provide more in-depth insights from the collected data.
