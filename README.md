# Video Games Web Scraper

Video Games Web Scraper is a project that crawls websites and APIs and extracts video game related data from their pages.

This project uses an open-source and collaborative framework named [Scrapy][1].

## Sources

* [VideoGameGeek][3] (`vgg`)

## Installation

I strongly recommend that you install this project in a dedicated virtual environment to avoid conflicting with your system packages.

See [Virtual Environments and Packages][2] on how to create and use your virtual environment.

Use the package manager [pip][6] to install the requirements of this project.

```bash
pip install -r requirements.txt
```
## Usage

You can start crawling a source using a spider.

```bash
scrapy crawl <spider>
```

### VideoGameGeek

#### Spiders

* `vgg-games`
* `vgg-hotitems`

## Developer Resources

### Initialize your Development Environment

```bash
pip install -r requirements.txt
```

### Create and Run Tests

See the [Spiders Contracts][7] for more instructions on how to create tests for spiders and then run:

```bash
scrapy check
```

### Scrapy Documentation

See the [Scrapy Documentation][8] for more instructions on how to create and modify spiders.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Support
If you enjoy this repository, please [star][4] this repository. By starring a repository, it shows appreciation to the repository maintainer for their work. Many of GitHub's repository rankings depend on the number of stars a repository has.

## License
[MIT][5]

[1]: https://scrapy.org/
[2]: https://docs.python.org/3/tutorial/venv.html#tut-venv
[3]: https://www.videogamegeek.com/
[4]: https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars
[5]: LICENSE
[6]: https://pip.pypa.io/en/stable/
[7]: https://docs.scrapy.org/en/latest/topics/contracts.html
[8]: https://docs.scrapy.org/en/2.5/