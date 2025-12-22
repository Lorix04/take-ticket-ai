from models.airport_models import QuestionCreate


def load_questions_from_txt(file_path: str) -> list[QuestionCreate]:
    """Load questions from a TXT file, one per line."""
    questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if line:  # Salta righe vuote
                questions.append(QuestionCreate(text=line, id=str(idx)))
    return questions