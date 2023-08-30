# room-type-scraper
Abstraction of Archit Sharma's procedural scraper: Selenium Python scraper to collect photos of different rooms for training ML models to distinguish between {bathroom, kitchen, living room, outside, bedroom, terrace} types.


# Room Image Scraper Class: An Abstraction of Archit Sharma's Original Code

## Description
This `Scraper` class is an abstraction and improvement over Archit Sharma's [original](https://github.com/deepklarity/clean-or-messy/blob/main/scrapper/main.py) procedural Selenium Python scraper. The original code was designed to collect photos of different rooms for training machine learning models to distinguish between various room types like bathroom, kitchen, living room, etc. This class-based version aims to offer the same functionality but in a more reusable and maintainable format.

## Improvements Over Original Code
1. **Object-Oriented Design**: The original procedural code has been refactored into a class-based design, making it easier to integrate into larger, multi-functional projects.
2. **Modularization**: Methods like `get_images_from_google()` and `download_image()` encapsulate specific functionalities, improving code readability and maintainability.
3. **Error Handling**: Improved error handling mechanisms have been implemented in the class methods.
4. **Code Reusability**: The class-based structure allows for easy reusability across different scraping tasks without duplicating code.

## Usage
Instantiate an object of the `Scraper` class and call its `do_scrape()` method with the appropriate query file path.

```python
scraper = Scraper()
scraper.do_scrape("path/to/query_file.csv")
```

## Dependencies
- Selenium
- Pandas
- urllib
- requests
- PIL (Pillow)
- time
- os
- io
- datetime

## License
MIT License

## Future Goals
We plan to extend the functionality of this class to include more advanced features, such as AI-driven scraping based on user behavior and preferences.

## Methods

### `__init__`
Initializes the webdriver and sets the maximum number of images to scrape and the delay between actions.

### `get_images_from_google`
Fetches image URLs based on the query string.

### `download_image`
Downloads an image from a URL and saves it to a specified path.

### `do_scrape`
Reads a CSV file containing queries and download paths, then performs the scraping.

## Known Issues
- The script may encounter issues if the initial user interaction with the browser is not handled properly.

Feel free to contribute to this project to make it more robust and feature-rich.

---

This README aims to provide a comprehensive guide to understanding and using the `Scraper` class, highlighting its improvements over Archit Sharma's original procedural code and its benefits in terms of object-oriented design.
