# Content Processor Tests

Test the Sheer content processors that bring content into Elasticsearch 
for cfgov-refresh.

## Running

From within this directory:

1. Install the requirements: `pip install -r requirements.txt`
2. Run the test runner: `python test_processors.py`

## Writing 

Tests are written using Python's [`unittest`](https://docs.python.org/2/library/unittest.html) (`unittest2` in Python 2.6). 

There are JSON files that is used to mock HTTP requests (`request.get()`) response content. 

An example:

```python
class WordpressPostProcessorTestCase(unittest.TestCase):
    @mock.patch('requests.get')
    def test_post(self, mock_requests_get):
        mock_response = mock.Mock()
        mock_response.content = open(os.path.join(os.path.dirname(__file__),
                                    'test_wordpress_post_processor_post.json')).read()
        mock_requests_get.return_value = mock_response

        name = 'post'
        url = 'http://mockmockmock/api/get_posts/'

        documents = list(wordpress_post_processor.documents(name, url))

        # ... make assertions about resulting document ...
```



