Yet Another Asyncio Requests

Install and usage are as expected. To install:

```sh
$ pip install yaar
```

And then the usage:

```python
import yaar

response = await yaar.get(url)
print(response.status, response.text)
print(response.json())


response = await yaar.post(url, data={"some": "json"})
print(response.status)
```
