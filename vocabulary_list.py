import pandas as pd
from sqlalchemy.orm import Session
import bd


def filling_bd():
    df = None
    file_path = None
    # Reading file .xlsx
    try:
        file_path = 'vocabulary_list.xlsx'
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as ex:
        print(f'Erro ao ler arquivo .xlsx / {ex}')
    else:
        # Creating a database session
        with bd.get_database_session()() as session:

            # Iterating in dataframe and add words in database
            try:
                for index, row in df.iterrows():
                    english_word = row[0]
                    translated_word = row[1]

                    # Checando se a palavra já existe no banco de dados
                    existing_word = session.query(bd.Word).filter_by(english=english_word).first()

                    # Creating a Word object and adding to database
                    if not existing_word:
                        new_word = bd.Word(english=english_word, translation=translated_word)
                        session.add(new_word)
            except Exception as ex:
                print(f'Error to iterating in {file_path} / {ex}')
            else:
                # Doing commit and closing the session
                session.commit()

