from notebook import NoteBook

note_book = NoteBook()
note_book.load_data()

def input_t(prompt):
    lines = []
    print(prompt)
    while True:
        line = input()
        if line.lower() == "save":
            break
        lines.append(line)
    return '\n'.join(lines)

class KeywordError(Exception):
    pass

def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "No title entered "
        except KeywordError:
            return "No keyword entered "
        except TypeError:
                return "Too much arguments"
    return inner

@user_error
def func_add_note(*args):
    title = ' '.join(args)
    if not title:
        raise IndexError
    if title not in note_book:
        input_text = input_t("Enter the text. Type 'save' to finish:")
        question = input("want to add tags? (Y/N)" )
        if question == 'y'.casefold():
            tags_input = input_t("Input tags. Type 'save' to finish:") 
            tags = ['#' + tag.strip() for tag in tags_input.split()]
        else:
            tags = []
        if tags:
            note_book.add_note(title, input_text, tags)
            return 'ok' # тут напевно щось треба написати серйозніше
        else:
            note_book.add_note(title, input_text)
            return 'ok' 
    else:
        question = input(f"want edit note {title}? (Y/N)" ) 
        if question == 'y'.casefold():
            return func_edit_note(*args)
        else:
            return "ok"

@user_error        
def func_edit_note(*args):
    title = ' '.join(args)
    input_new_text = input_t("Input new text. Type 'save' to finish:")
    note_book.edit_note(title, input_new_text)
    return "ok"

@user_error
def func_edit_tags(*args):
    title = ' '.join(args)
    input_new_tags = input_t("Input new tags. Type 'save' to finish:")
    new_tags = ['#' + tag.strip() for tag in input_new_tags.split()]
    note_book.edit_note(title, None, new_tags)
    return "all ok"

@user_error        
def func_show_notes():
    return note_book

@user_error
def func_search_notes(*args):
    keyword = ' '.join(args)
    if not keyword:
        raise KeywordError 
    
    return note_book.search_notes(keyword)

@user_error
def func_sort_notes():
    return note_book.sort_notes()

def func_save_notes():
    note_book.save_data()

def func_delete_notes(*args):
    title = ' '.join(args)
    if not title:
        question = input("Are you sure you want to delete ALL notes? (Y/N)")
        if question == 'y'.casefold():
            return note_book.delete_note()
        return "Notes not deleted"
    else:    
        return note_book.delete_note(title)
    

OPERATORS = {
    "add note": func_add_note, # add note заголовок нотатку --> далі по підказкам
    "edit note": func_edit_note, # edit note заголовок --> далі по підказкам
    "edit tags": func_edit_tags, # edit tags заголовок --> далі по підказкам
    "show notes": func_show_notes, # show notes  (тут без заголовку)
    "show note": func_search_notes, # show note (будь яку слово з заголовку або #тег)
    "sort notes": func_sort_notes, # sort notes (без аргументів) - сортує, виводить та зберігає новий порядок нотатків, сортування за кількістю тегів, як замовляв викладач
    "delete notes": func_delete_notes
}
    


