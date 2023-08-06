**vcommand** is a lightweight framework for building voice-controlled applications. It is designed to be easy to create voice commands to automate tasks.

## Installing

Install and update with pip:

```shell
python -m pip install vcommand
```

## A Simple Example

```python
from vcommand import VCommand

app = VCommand()

@app.command("HELLO", "Say 'hello world!'")
def hello_world():
    app.speak("Hello world!")


if __name__ == "__main__":
    app.start(debug=0)

```

## License

This project is licensed under the BSD License.
