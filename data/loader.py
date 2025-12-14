import os
import random


def load_questions(file_path='data/questions.txt'):
    try:
        if not os.path.exists(file_path):
            print(f"❌ KLAIDA: Failas '{file_path}' nerastas!")
            print(f"   Dabartinis katalogas: {os.getcwd()}")
            return []
        
        questions = []
        
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        
        if not lines:
            print("❌ KLAIDA: Klausimų failas tuščias!")
            return []
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('|')
            
            if len(parts) != 7:
                print(f"❌ Eilutė {line_num}: Neteisingas formatas (reikia 7 laukų, rasta {len(parts)})")
                continue
            
            try:
                question_id = int(parts[0])
                question_text = parts[1]
                option1 = parts[2]
                option2 = parts[3]
                option3 = parts[4]
                option4 = parts[5]
                correct_index = int(parts[6])
                
                question = {
                    'id': question_id,
                    'question': question_text,
                    'options': [option1, option2, option3, option4],
                    'correct': correct_index
                }
                
                if validate_question(question, line_num - 1):
                    questions.append(question)
                else:
                    print(f"⚠️  Klausimas eilutėje {line_num} praleistas dėl validacijos klaidų")
                    
            except ValueError as e:
                print(f"❌ Eilutė {line_num}: Klaida konvertuojant duomenis - {e}")
                continue
        
        if not questions:
            print("❌ KLAIDA: Nėra nei vieno teisingo klausimo!")
            return []
        
        print(f"✅ Sėkmingai įkelta {len(questions)} klausimų")
        return questions
        
    except Exception as e:
        print(f"❌ KLAIDA: {e}")
        return []


def validate_question(question, index):
    if not isinstance(question, dict):
        print(f"❌ Klausimas {index + 1}: Turi būti žodynas (dict)")
        return False
    
    required_fields = ['id', 'question', 'options', 'correct']
    for field in required_fields:
        if field not in question:
            print(f"❌ Klausimas {index + 1}: Trūksta lauko '{field}'")
            return False
    
    if not isinstance(question['question'], str) or not question['question'].strip():
        print(f"❌ Klausimas {index + 1}: Klausimo tekstas tuščias arba neteisingas")
        return False
    
    if not isinstance(question['options'], list):
        print(f"❌ Klausimas {index + 1}: 'options' turi būti sąrašas")
        return False
    
    if len(question['options']) != 4:
        print(f"❌ Klausimas {index + 1}: Turi būti tiksliai 4 atsakymai (dabar: {len(question['options'])})")
        return False
    
    for i, option in enumerate(question['options']):
        if not isinstance(option, str) or not option.strip():
            print(f"❌ Klausimas {index + 1}: Atsakymas {i + 1} tuščias arba neteisingas")
            return False
    
    if not isinstance(question['correct'], int):
        print(f"❌ Klausimas {index + 1}: 'correct' turi būti sveikasis skaičius")
        return False
    
    if question['correct'] not in [0, 1, 2, 3]:
        print(f"❌ Klausimas {index + 1}: 'correct' turi būti 0, 1, 2 arba 3 (dabar: {question['correct']})")
        return False
    
    return True


def get_random_questions(count=10, questions=None):
    if questions is None:
        questions = load_questions()
    
    if not questions:
        print("❌ Nepavyko gauti klausimų!")
        return []
    
    if len(questions) < count:
        print(f"⚠️  ĮSPĖJIMAS: Prašoma {count} klausimų, bet yra tik {len(questions)}")
        print(f"   Grąžinami visi {len(questions)} klausimai")
        return questions.copy()
    
    return random.sample(questions, count)


def get_question_by_id(question_id, questions=None):
    if questions is None:
        questions = load_questions()
    
    for q in questions:
        if q.get('id') == question_id:
            return q
    
    return None


def get_questions_stats(questions=None):
    if questions is None:
        questions = load_questions()
    
    if not questions:
        return {
            'total': 0,
            'valid': 0,
            'has_duplicates': False
        }
    
    ids = [q.get('id') for q in questions]
    has_duplicates = len(ids) != len(set(ids))
    
    return {
        'total': len(questions),
        'valid': len(questions),
        'has_duplicates': has_duplicates,
        'min_id': min(ids) if ids else 0,
        'max_id': max(ids) if ids else 0
    }


if __name__ == "__main__":
    print("=" * 60)
    print("KLAUSIMŲ ĮKĖLIMO TESTAVIMAS (TXT formatas)")
    print("=" * 60)
    
    print("\n1️⃣  Įkeliami klausimai...")
    questions = load_questions()
    
    if not questions:
        print("\n❌ Nepavyko įkelti klausimų. Patikrinkite failą.")
        exit(1)
    
    print("\n2️⃣  Statistika:")
    stats = get_questions_stats(questions)
    print(f"   Iš viso klausimų: {stats['total']}")
    print(f"   Validūs klausimai: {stats['valid']}")
    print(f"   ID intervalas: {stats['min_id']} - {stats['max_id']}")
    print(f"   Ar yra dublikatų: {'TAIP ⚠️' if stats['has_duplicates'] else 'NE ✅'}")
    
    print("\n3️⃣  Pirmojo klausimo pavyzdys:")
    q = questions[0]
    print(f"   ID: {q['id']}")
    print(f"   Klausimas: {q['question']}")
    print(f"   Atsakymai:")
    for i, opt in enumerate(q['options']):
        marker = "✅" if i == q['correct'] else "  "
        print(f"      {marker} {i}. {opt}")
    
    print("\n4️⃣  Atsitiktinė 10 klausimų imtis:")
    random_q = get_random_questions(10, questions)
    print(f"   Gauta {len(random_q)} klausimų")
    print(f"   ID: {[q['id'] for q in random_q]}")
    
    print("\n" + "=" * 60)
    print("✅ TESTAS BAIGTAS SĖKMINGAI!")
    print("=" * 60)