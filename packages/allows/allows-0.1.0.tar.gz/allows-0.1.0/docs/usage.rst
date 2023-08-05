=====
Usage
=====

To use Allows in a project::

    from unittest.mock import Mock

    from allows import allow, receive_method

    my_mock = Mock()
    allow(my_mock).to(
        receive_method('spam')
        .called_with(eggs='foo')
        .and_return_value('bar')
    )
    allow(my_mock).to(
        receive_method('spam')
        .called_with(eggs='no thanks')
        .and_return_value('ok')
    )

    assert my_mock.spam(eggs='foo') == 'bar'
    assert my_mock.spam(eggs='no thanks') == 'ok'

Allows specifies a similar grammar to Rspec to set up Mocks for tests. This allows complex side effects to be constructed more easily than with the standard Mock API.

Allows can be used without the grammar to build and compose side effects as well.

.. code:: python

    from unittest.mock import Mock, call

    from allows import SideEffect, SideEffectBuilder

    side_effect = SideEffectBuilder() \
        .with_return_value('bar') \
        .with_call_args(eggs='foo')

    args = call(eggs='no thanks')
    effect = lambda *args, **kwargs: 'bar'
    another_side_effect = SideEffect(args, effect)

    side_effect.merge(another_side_effect)

    my_mock = Mock()
    my_mock.spam.side_effect = side_effect

    assert my_mock.spam(eggs='foo') == 'bar'
    assert my_mock.spam(eggs='no thanks') == 'ok'
