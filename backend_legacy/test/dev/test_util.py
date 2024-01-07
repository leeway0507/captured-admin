from components.dev.utils import util


def test_split_size():
    target = list(range(0, 9))
    output = util.ListSeparator.split(target, 3)
    # 3,3,3
    assert output[-1] == [6, 7, 8]

    target = list(range(0, 10))
    output = util.ListSeparator.split(target, 3)
    # 4,4,2
    assert output[-1] == [8, 9]


def test_split_rest_zero():
    # Given
    target = list(range(0, 15))
    group_num = 3
    group_size = len(target) // group_num

    # When
    output = util.ListSeparator.split_rest_zero(target, group_size)

    # Then
    # 5,5,5
    assert output[-1] == [10, 11, 12, 13, 14]


def test_split_rest_not_zero():
    # Given
    target = list(range(0, 16))
    group_num = 3
    group_size = len(target) // group_num

    # When
    output = util.ListSeparator.split_rest_not_zero(target, group_size)

    # Then
    # 6,6,4
    assert output[-1] == [12, 13, 14, 15]
