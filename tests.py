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

@pytest.fixture
def questao_multipla_escolha():
    questao = Question(title='Quais são linguagens de programação?', max_selections=3, points=10)
    questao.add_choice('Python', True)
    questao.add_choice('HTML', False)
    questao.add_choice('Java', True)
    questao.add_choice('CSS', False)
    questao.add_choice('JavaScript', True)
    return questao

@pytest.fixture
def questao_com_pontuacao_maxima():
    questao = Question(title='Questão Difícil', points=100)
    questao.add_choice('Resposta A', False)
    questao.add_choice('Resposta B', True)
    return questao

def test_deve_identificar_todas_respostas_corretas(questao_multipla_escolha):
    respostas_corretas = questao_multipla_escolha._correct_choice_ids()
    
    # Deve haver exatamente 3 respostas corretas (Python, Java e JavaScript)
    assert len(respostas_corretas) == 3
    
    # Verifica se as escolhas corretas são as esperadas
    escolhas_corretas = [choice for choice in questao_multipla_escolha.choices if choice.is_correct]
    assert 'Python' in [choice.text for choice in escolhas_corretas]
    assert 'Java' in [choice.text for choice in escolhas_corretas]
    assert 'JavaScript' in [choice.text for choice in escolhas_corretas]

def test_deve_permitir_selecao_parcial_de_respostas_corretas(questao_multipla_escolha):
    # Seleciona apenas 2 das 3 respostas corretas
    escolhas_corretas = [choice.id for choice in questao_multipla_escolha.choices if choice.is_correct][:2]
    
    respostas_selecionadas = questao_multipla_escolha.select_choices(escolhas_corretas)
    
    assert len(respostas_selecionadas) == 2
    assert all(id in escolhas_corretas for id in respostas_selecionadas)

def test_deve_manter_pontuacao_ao_modificar_escolhas(questao_com_pontuacao_maxima):
    pontuacao_original = questao_com_pontuacao_maxima.points
    
    # Modifica as escolhas
    questao_com_pontuacao_maxima.remove_all_choices()
    questao_com_pontuacao_maxima.add_choice('Nova Resposta A', True)
    questao_com_pontuacao_maxima.add_choice('Nova Resposta B', False)
    
    # Verifica se a pontuação permanece a mesma
    assert questao_com_pontuacao_maxima.points == pontuacao_original
    assert questao_com_pontuacao_maxima.points == 100