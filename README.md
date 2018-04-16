# GitRank

GitRank is a tool that compares arbitrary GitHub repositories or users side-by-side and computes a score based on a [weighted sum model](https://en.wikipedia.org/wiki/Weighted_sum_model) that takes into consideration a set of metrics like the number of commits, stars, how recent the latest commit is, etc. Additionally it is able to suggest related repositories based on previous comparisons.

## Development

```bash
docker-compose down --volumes
docker-compose build
docker-compose up
```

