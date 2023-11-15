def func_help():
    return (
        (
            "\033[42m{:<50}***{:*^10}***{:>50}\033[0m".format(
                "",
                "ADDRESSBOOK",
                "",
            )
            + "\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}\n\033[32m{}\033[0m{}".format(
                "add record <name> <phone>",
                "  -> new record adding, follow the instruction to add other fields",
                "add address <name> <address>",
                "  -> adds address to existing contact",
                "add birthday <name> <birthday>",
                "  -> adds birthday to existing contact",
                "add email <name> <email>",
                "  -> adds email to existing contact",
                "edit record <name>",
                "  -> follow the instructions to edit or add info to existing contact",
                "phone of <name>",
                "  -> shows all phones of existing contact",
                "show all records",
                "  -> shows all existing contacts in your current addressbook",
                "show records <num per page>",
                "  -> shows defined number of contacts pro page",
                "find record <min 3 symb pattern>",
                "  -> searches defined symbols in all fields, all contacts",
                "change phone <name> <old phone> <new phone>",
                " -> replaces the existing in contact phone number to new provided",
                "remove record <name>",
                "  -> removes defined record from the addressbook",
                "birthday within days",
                "  -> follow the instructions, shows all contacts who have birthdays within defined days range",
            )
            + "\n\033[44m{:<50}***{:*^10}***{:>50}\033[0m".format(
                "",
                "NOTES",
                "",
            )
            + "\n\033[34m{}\033[0m{}\n\033[34m{}\033[0m{}\n\033[34m{}\033[0m{}\n\033[34m{}\033[0m{}\n\033[34m{}\033[0m{}\n\033[34m{}\033[0m{}\n\033[34m{}\033[0m{}\n\033[34m{}\033[0m{}\n\033[34m{}\033[0m{}".format(
                "add note <titel>",
                "  -> follow the instructions to create new note",
                "add tags <titel>",
                "  -> addes new tags to existing note",
                "edit note <titel>",
                "  -> follow the instructions to edit existing note",
                "edit tags <titel>",
                "  -> follow the instraction to edit tags in existing note",
                "find note <title> / <tag>",
                "  -> shows notes based on defined search pattern",
                "show notes",
                "  -> shows all existing notes",
                "sort notes",
                "  -> sort notes based on tags, print all notes sorted",
                "delete notes <titel>",
                "  -> delete note with defined titel",
                "delete notes",
                "  -> delete all existing notes",
            )
        )
        + "\n\033[41m{:<50}***{:*^10}***{:>50}\033[0m".format(
            "",
            "SERVICE",
            "",
        )
        + "\n\033[31m{}\033[0m{}\n\033[31m{}\033[0m{}\n\033[31m{}\033[0m{}".format(
            "hello",
            "  -> just to be polite",
            "exit / close / good bye",
            "  -> to save files and exit the assistant",
            "sort folder",
            "  -> follow the instruction to sort files in folder in defined directory",
        )
    )
