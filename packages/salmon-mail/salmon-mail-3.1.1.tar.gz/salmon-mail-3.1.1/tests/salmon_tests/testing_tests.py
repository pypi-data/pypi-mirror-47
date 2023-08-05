from mock import Mock, patch

from nose.tools import assert_equal, with_setup
from salmon.testing import RouterConversation, assert_in_state, clear_queue, delivered, queue, relay

from .setup_env import setup_salmon_dirs, teardown_salmon_dirs

relay = relay(port=0)


@with_setup(setup_salmon_dirs, teardown_salmon_dirs)
def test_clear_queue():
    queue().push("Test")
    assert_equal(queue().count(), 1)

    clear_queue()
    assert_equal(queue().count(), 0)


@patch("smtplib.SMTP")
@with_setup(setup_salmon_dirs, teardown_salmon_dirs)
def test_relay(smtp_mock):
    smtp_mock.return_value = Mock()

    relay.send('test@localhost', 'zedshaw@localhost', 'Test message', 'Test body')

    assert_equal(smtp_mock.return_value.sendmail.call_count, 1)
    assert_equal(smtp_mock.return_value.quit.call_count, 1)


@with_setup(setup_salmon_dirs, teardown_salmon_dirs)
def test_delivered():
    clear_queue()
    queue().push("To: gooduser@localhost\nFrom: tester@localhost\n\nHi\n")

    assert delivered("gooduser@localhost"), "Test message not delivered."
    assert not delivered("baduser@localhost")
    assert_in_state('salmon_tests.handlers.simple_fsm_mod', 'gooduser@localhost', 'tester@localhost', 'START')


@with_setup(setup_salmon_dirs, teardown_salmon_dirs)
def test_RouterConversation():
    client = RouterConversation('tester@localhost', 'Test router conversations.')
    client.begin()
    client.say('testlist@localhost', 'This is a test')
    delivered('testlist@localhost'), "Test message not delivered."
