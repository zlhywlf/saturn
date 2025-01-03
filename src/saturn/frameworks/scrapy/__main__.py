from scrapy.cmdline import execute


def main() -> None:
    """Main."""
    execute(["scrapy", "crawl", "quote"])


if __name__ == "__main__":
    main()
