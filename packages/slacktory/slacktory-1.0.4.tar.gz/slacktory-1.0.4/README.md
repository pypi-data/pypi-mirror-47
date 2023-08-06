# Slacktory

A decorator which is called using:
```python
@slacktory.watch('the text to watch for')
``` 
...that watches a specified Slack channel for **new** Slack message posts whose ['text'] value is equivalent to the provided string argument

Requires **Python 3.7**
## Installation



```sh
pip install slacktory
```
For this decorator to work, you must first create a [Slack App](https://api.slack.com/apps)
 
Then create a **local_settings.py** file in your project's root directory with the following content:

```python
name = '<your Slack channel name>'
channel = '<your Slack channel id>'
token = '<your Slack API token>'
webhook = '<your Slack channel webhook>'

```

---------------------------------------------------

All of the above information can be obtained when setting up your [Slack App](https://api.slack.com/apps)

## Usage example

```python
>>> import slacktory
>>> @slacktory.watch('do the thing') # the decorator 
>>> def the_thing():

        # do something here...
  
```
In the above example, the_thing() will be called once the @slacktory.watch decorator has detected the text '_do the thing_' in a new Slack message in the Slack channel (specified in **local_settings.py**).



## Release History


* 1.0.0
    * first release
* 1.0.1
    * minor README changes
* 1.0.2
    * minor README changes
* 1.0.3
    * use nonlocal variables to remove the need for a recursive call on decorated function
    * remove polling, add while True
* 1.0.4
    * Add try/except with error message for import local_settings
    * Add license copy

## Meta

James Coleman – jamescoleman@me.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[gitlab.com/jamescoleman/slacktory](https://gitlab.com/j9mes/slacktory)

## Contributing

1. Fork it (<https://gitlab.com/j9mes/slacktory/forks/new>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

