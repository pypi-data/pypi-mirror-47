# this american client
The [This American Life](https://www.thisamericanlife.org/) client library. 

Get structured data on transcripts, episodes, et c without worrying about all of the web scraping details. Intermediate
results are cached to keep it snappy.

## Install

```bash
pip install this-american-life
```

## Using the client

### Get the transcript of an episode
```python
from thisamericanlife import ThisAmericanLife

tal = ThisAmericanLife()
ep_one_transcript = tal.transcripts.get(episode_number=1)

print(ep_one_transcript.transcript)
```