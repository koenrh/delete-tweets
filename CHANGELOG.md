# Changelog

## Unreleased

## v2.0.0

- Remove [`time.sleep`](https://docs.python.org/3/library/time.html#time.sleep)
    as a means of avoiding Twitter's rate-limiting in favour of [python-twitter](https://python-twitter.readthedocs.io/en/latest/rate_limits.html)'s
    `sleep_on_rate_limit` ([@0trenixjetix](https://github.com/0trenixjetix))
- Add `--since` option to delete tweets since a specific date [\#80](https://github.com/koenrh/delete-tweets/pull/80)
    ([@cyb3rsalih](https://github.com/cyb3rsalih))
- Remove support for Python 2.7 [\#66](https://github.com/koenrh/delete-tweets/pull/66)

## v1.0.6

- Fix script to work with Twitter's new data structure [\#75](https://github.com/koenrh/delete-tweets/pull/75)
    ([@vlaship](https://github.com/vlaship))

## v1.0.5

- Add missing required dependencies to setup file [\#73](https://github.com/koenrh/delete-tweets/pull/73)

## v1.0.4

- Fix crash if until date is not set [\#70](https://github.com/koenrh/delete-tweets/pull/70)

## v1.0.3

- Fix `--dry-run` command-line option [\#68](https://github.com/koenrh/delete-tweets/pull/68)

## v1.0.0

- Add option to spare specific tweets or conditionally based on the minimum number
    of likes or retweets [\#45](https://github.com/koenrh/delete-tweets/pull/45)
- Replace Travis CI with GitHub Actions [\#47](https://github.com/koenrh/delete-tweets/pull/47)
- Publish Python package to PyPI [\#53](https://github.com/koenrh/delete-tweets/pull/53)
- Add long command-line options and follow Twitter's naming convention [\#63](https://github.com/koenrh/delete-tweets/pull/63)
