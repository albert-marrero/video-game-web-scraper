## Bots

* Video Game Geek Bot

## Sources

* Video Game Geek

## Usage

You can start crawling a source using a spider.

```bash
export SCRAPY_PROJECT=videogamegeek
scrapy crawl <spider>
```


### VideoGameGeek

#### Spiders

* `hotvideogames`


## Developer Resources

By default, the scrapy command-line tool will use the default settings. Use the SCRAPY_PROJECT environment variable to specify a different project for scrapy to use:

```bash
$ scrapy settings --get BOT_NAME
SAMPLE PROJECT BOT
$ export SCRAPY_PROJECT=videogamegeek
$ scrapy settings --get BOT_NAME
Video Game Geek Bot
```

### Scrapy Documentation

