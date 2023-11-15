from .notebook import NoteBook

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
    return "\n".join(lines)


def args_to_title(args=None):
    if not args:
        raise IndexError
    title = " ".join(args)
    if title not in note_book:
        raise KeyError
    return title


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
        except KeyError:
            return "No notes with this name"

    return inner


@user_error
def func_add_note(*args):
    title = " ".join(args)
    if not title:
        raise IndexError
    if title not in note_book:
        input_text = input_t("Enter the text. Type 'save' to finish:")
        question = input("Want to add tags? (Y/N)")
        if question == "y".casefold():
            tags_input = input_t("Input tags. Type 'save' to finish:")
            tags = ["#" + tag.strip() for tag in tags_input.split()]
        else:
            tags = []
        if tags:
            note_book.add_note(title, input_text, tags)
            tags_str = " ".join(x for x in tags)
            return f"New note with title: {title} and tags: {tags_str} was saved"  # тут напевно щось треба написати серйозніше
        else:
            note_book.add_note(title, input_text)
            return f"New note with {title} was saved"
    else:
        question = input(f"Note {title} already exist. Want to edit note? (Y/N)")
        if question == "y".casefold():
            return func_edit_note(*args)
        else:
            return "Note was not changed"


@user_error
def func_edit_note(*args):
    title = args_to_title(args)
    text_note = note_book[title]["text"].split("\n")
    flag = False
    while True:
        if flag == False:
            for i, line in enumerate(text_note):
                print(f"{i+1}: {line}")
            print('Enter line number to edit (Type "save" to finish:):')
        user_input = input()
        if user_input == "save":
            break
        if user_input.isdigit() and 0 <= int(user_input) <= len(text_note):
            user_input = int(user_input)
            edited_line = input(
                f"Edit line {user_input}: {text_note[user_input - 1]}\n"
            )
            text_note[user_input - 1] = edited_line
            flag = False
        else:
            print("Invalid input. Enter line number to edit (0 to exit):")
            flag = True
        new_text = "\n".join(text_note)
    note_book.edit_note(title, new_text)
    return f"Note {title} was updated"


@user_error
def func_edit_tags(*args):
    title = args_to_title(args)
    input_new_tags = input_t("Input new tags. Type 'save' to finish:")
    new_tags = ["#" + tag.strip() for tag in input_new_tags.split()]
    note_book.edit_note(title, None, new_tags)
    return f"Tags in note {title} are updated"


@user_error
def func_add_tags(*args):
    title = args_to_title(args)
    input_new_tags = input_t("Input new tags. Type 'save' to finish:")
    new_tags = ["#" + tag.strip() for tag in input_new_tags.split()]
    note_book[title]["tags"].extend(new_tags)
    return f"New tags were added to note {title}" 


@user_error
def func_show_notes():
    return note_book


@user_error
def func_search_notes(*args):
    keyword = " ".join(args)
    if not keyword:
        raise KeywordError

    return note_book.search_notes(keyword)


@user_error
def func_sort_notes():
    return note_book.sort_notes()


def func_save_notes():
    note_book.save_data()


def func_delete_notes(*args):
    title = " ".join(args)
    if not title:
        question = input("Are you sure you want to delete ALL notes? (Y/N)")
        if question == "y".casefold():
            return note_book.delete_note()
        return "Notes not deleted"
    else:
        return note_book.delete_note(title)


OPERATORS = {
    "add note": func_add_note,  # add note заголовок нотатку --> далі по підказкам
    "add tags": func_add_tags,  # add tags заголовок --> додасть нові теги до уже існуючих
    "edit note": func_edit_note,  # edit note заголовок --> далі по підказкам
    "edit tags": func_edit_tags,  # edit tags заголовок --> далі по підказкам
    "show notes": func_show_notes,  # show notes  (тут без заголовку)
    "find note": func_search_notes,  # show note (будь яку слово з заголовку або #тег)
    "sort notes": func_sort_notes,  # sort notes (без аргументів) - сортує, виводить та зберігає новий порядок нотатків, сортування за кількістю тегів, як замовляв викладач
    "delete notes": func_delete_notes,  # якщо вказати заголовок, то видалиться запис, якщо без аргументів, то видаляться всі записи, після підтвердження видалення
}
