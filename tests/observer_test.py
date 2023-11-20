from typing import Union

from senzing import observer_example

# -----------------------------------------------------------------------------
# G2Config fixtures
# -----------------------------------------------------------------------------


def mock_senzing_method(
    fake_message: str, observer: Union[observer_example.ObserverAbstract, None] = None
) -> None:
    """
    An example of a call to a G2Engine method that has an optional Observer passed in.

    Args:
        fake_message (str): Just a message that the mock method will send to the Observer.
        observer (Union[observer_example.ObserverAbstract, None], optional): An observer to test. Defaults to None.
    """
    if observer is not None:
        observer.update(fake_message)


# -----------------------------------------------------------------------------
# G2Config testcases
# -----------------------------------------------------------------------------


def test_update():
    """Test observer.update()."""
    actual = "A test message"
    observer = observer_example.ObserverExample()
    observer.update(actual)


def test_get():
    """Test observer.get()."""
    actual = "A test message"
    observer = observer_example.ObserverExample()
    observer.update(actual)
    result = observer.get()
    assert result == actual
    assert observer.empty()


def test_empty():
    """Test observer.empty()."""
    actual = "A test message"
    observer = observer_example.ObserverExample()
    result = observer.empty()
    assert result
    observer.update(actual)
    result = observer.empty()
    assert not result
    result = observer.get()
    assert result
    assert observer.empty()


def test_qsize():
    """Test observer.qsize()."""
    actual = 5
    message_template = "A test message: {0}"
    observer = observer_example.ObserverExample()
    for i in range(actual):
        observer.update(message_template.format(i))
    result = observer.size()
    assert result == actual


def test_qsize_drain_with_qsize():
    """Test observer get and qsize."""
    actual = 5
    message_template = "A test message: {0}"
    observer = observer_example.ObserverExample()
    for i in range(actual):
        observer.update(message_template.format(i))
    while observer.size() > 0:
        _ = observer.get()
    assert observer.empty()


def test_qsize_drain_with_empty():
    """Test observer get and empty."""
    actual = 5
    message_template = "A test message: {0}"
    observer = observer_example.ObserverExample()
    for i in range(actual):
        observer.update(message_template.format(i))
    while not observer.empty():
        _ = observer.get()
    assert observer.size() == 0


def test_method_calling():
    """Test calling a function with an observer."""
    actual = "A test message"
    observer = observer_example.ObserverExample()
    mock_senzing_method(actual, observer)
    assert observer.size() == 1
    result = observer.get()
    assert result == actual
    assert observer.empty()


def test_method_calling_empty():
    """Test calling a function without an observer."""
    actual = "A test message that shouldn't be used"
    mock_senzing_method(actual)
