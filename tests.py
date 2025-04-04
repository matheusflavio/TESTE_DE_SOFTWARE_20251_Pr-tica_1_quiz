import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_question_should_not_allow_points_outside_valid_range():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_question_should_allow_multiple_correct_choices():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('c', False)
    
    assert len([c for c in question.choices if c.is_correct]) == 2

def test_question_should_not_allow_selecting_more_than_max_selections():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('c', True)
    
    with pytest.raises(Exception):
        question.select_choices([choice1.id, choice2.id, choice3.id])

def test_choice_should_not_allow_empty_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')

def test_choice_should_not_allow_text_longer_than_limit():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_removing_choice_should_update_choices_list():
    question = Question(title='q1')
    choice = question.add_choice('a')
    initial_count = len(question.choices)
    
    question.remove_choice_by_id(choice.id)
    
    assert len(question.choices) == initial_count - 1
    assert choice not in question.choices

def test_removing_all_choices_should_clear_question():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_selecting_correct_choices_should_return_only_correct_ids():
    question = Question(title='q1', max_selections=3)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', True)
    
    selected_ids = question.select_choices([choice1.id, choice2.id, choice3.id])
    
    assert len(selected_ids) == 2
    assert choice2.id not in selected_ids

def test_setting_correct_choices_should_update_choices_status():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    
    question.set_correct_choices([choice1.id])
    
    assert choice1.is_correct
    assert not choice2.is_correct

def test_removing_invalid_choice_id_should_raise_exception():
    question = Question(title='q1')
    question.add_choice('a')
    
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)