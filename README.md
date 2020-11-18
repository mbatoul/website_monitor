# Simple website monitoring tool

## Installation

```bash
$ brew install postgresql
```

```bash
$ brew services start postgresql
```

```bash
$ createdb website_monitor
```

```
$ pip install .
```

## Usage

```
Usage: website_monitor [OPTIONS]

Options:
  --website, --w <TEXT TEXT INTEGER RANGE>...
                                  Name, URL and check interval in seconds (min
                                  1s) for a website. Example: --website github
                                  https://www.github.com 1 --website reddit
                                  https://www.reddit.com 1  [required]

  --metrics, --m <INTEGER INTEGER>...
                                  Reference period and refresh interval for a
                                  set of the tracked metrics. Example:
                                  --metrics 120 30 <=> Metrics for past 120
                                  minutes should be refreshed every 30
                                  seconds.  [default: (10, 10), (60, 60)]

  --period, --p INTEGER           Alerting period in seconds. Combined with
                                  alerting threshold. Example: --period 180
                                  <=> Websites' availabilities over the last 3
                                  minutes will be considered to open/close
                                  alerts.  [default: 120]

  --threshold, --t INTEGER RANGE  Alerting threshold in %. Must be between 1%
                                  and 99%. Combined with alerting period.
                                  Example: --threshold 90 <=> When a website
                                  availability is below (resp. above) 90%
                                  during the period of reference, an alert is
                                  opened (resp. closed).  [default: 80]

  --help                          Show this message and exit.
```

### Help

To get some help, run:

```
$ website_monitor --help
```

### Tests and coverage

To run tests:

```
$ pytest tests
```

To run tests and get test coverage, run:

```
$ pytest --cov=website_monitor tests
```
