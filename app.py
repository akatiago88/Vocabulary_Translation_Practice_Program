from tkinter import *
import random
from tkinter import messagebox

from sqlalchemy.orm import Session

import bd
import vocabulary_list
from bd import *
from vocabulary_list import filling_bd
import datetime


# Variáveis Globais
current_word = None
correct_answers = []
incorrect_answers = []
used_words = []


# Função para obter uma palavra aleatória e verificar se ela já foi usada
def get_random_word():
    global used_words
    with bd.get_database_session()() as session:
        remaining_words = session.query(Word).filter(~Word.id.in_(used_words)).all()

        if not remaining_words:
            return None

    random_word = random.choice(remaining_words)
    used_words.append(random_word.id)
    return random_word


# Função para verificar a resposta
def check_answer():
    global current_word, correct_answers, incorrect_answers
    user_translation = user_input.get().strip().lower()
    valid_translations = [t.strip().lower() for t in current_word.translation.split(',')]

    if user_translation in valid_translations:
        correct_answers.append(f'{current_word.english} - {current_word.translation}')
    else:
        incorrect_answers.append(f'{current_word.english} - {current_word.translation}')

    user_input.delete(0, END)

    # Atualizar a interface do usuário e verificar se todas as palavras foram usadas
    update_ui()


def update_ui():
    global current_word, used_words, correct_answers, incorrect_answers

    with bd.get_database_session()() as session:
        total_words = session.query(bd.Word).count()

        current_word = get_random_word()

    english_word_label.config(text=current_word.english)
    correct_listbox.delete(0, END)
    incorrect_listbox.delete(0, END)

    for correct in correct_answers:
        correct_listbox.insert(0, correct)

    for incorrect in incorrect_answers:
        incorrect_listbox.insert(0, incorrect)

    try:
        answered_words = len(correct_answers) + len(incorrect_answers)
        progress_label.config(text=f'{answered_words} / {total_words}')
        accuracy_label.config(text=f'{(len(correct_answers) / answered_words) * 100:.2f}%')
    except ZeroDivisionError:
        progress_label.config(text=f'0 / {total_words}')
        accuracy_label.config(text=f'0%')

    if len(used_words) == total_words:
        if correct_answers or incorrect_answers:
            end_quiz()
        else:
            messagebox.showinfo('Informação', 'Não há palavras no banco de dados')
            app.quit()
            return


# Função para encerrar o Quiz e exibir o messagebox com o score
def end_quiz():
    global correct_answers, incorrect_answers

    total_words = len(correct_answers) + len(incorrect_answers)
    if total_words == 0:
        accuracy = 0
    else:
        accuracy = (len(correct_answers) / total_words) * 100
    messagebox.showinfo('Fim do Quiz', f'Você completou o quiz!\nAcurácia: {accuracy:.2f}%')

    # Salvar o resultado na tabela scores
    with bd.get_database_session()() as session:
        new_score = Score(date=datetime.date.today(), word_count=total_words, accuracy=accuracy)
        session.add(new_score)
        session.commit()


# Função da tecla enter para validação
def on_enter(event):
    check_answer()


filling_bd()
app = Tk()
app.title('QUIZ - English Vocabulary')
app.geometry('800x800')
app.configure(background='#2F4F4F')


english_word_label = Label(app, text='', font=('Arial', 24), bg='#2F4F4F', fg='white')
english_word_label.pack(pady=20)

user_input = Entry(app, font=('Arial', 24))
user_input.pack(pady=20)
user_input.bind('<Return>', on_enter)  # Ativado a tecla enter para aplicar validação

submit_button = Button(app, text='Validate', font=('Arial', 18), command=check_answer)
submit_button.pack(pady=20)

correct_listbox = Listbox(app, font=('Arial', 14), bg='#90EE90', fg='#2F4F4F')
correct_listbox.pack(side=LEFT, padx=15, pady=5, fill=BOTH, expand=True)

incorrect_listbox = Listbox(app, font=('Arial', 14), bg='#F08080', fg='#2F4F4F')
incorrect_listbox.pack(side=RIGHT, padx=15, pady=5, fill=BOTH, expand=True)

progress_text = Label(text='Progresso', font=('Arial', 14), bg='#2F4F4F', fg='white')
progress_text.pack(side=TOP, padx=15, pady=5)

progress_label = Label(app, text='', font=('Arial', 14), bg='#2F4F4F', fg='white')
progress_label.pack(side=TOP, padx=15, pady=5)

accuracy_text = Label(text='Taxa de acerto', font=('Arial', 14), bg='#2F4F4F', fg='white')
accuracy_text.pack(side=TOP, padx=15, pady=5)

accuracy_label = Label(app, text='', font=('Arial', 14), bg='#2F4F4F', fg='white')
accuracy_label.pack(side=TOP, padx=15, pady=5)

# Atualizar a interface do usuário e começar o quiz
update_ui()
app.mainloop()
