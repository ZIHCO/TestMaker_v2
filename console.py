#!/usr/bin/python3
"""This is the entry point of the command interpreter"""
from cmd import Cmd
from models import storage
from models.base_model import BaseModel
from models.exam import Exam
from models.examinee import Examinee
from models.examiner import Examiner
from models.grade import Grade
from models.question import Question

classes = ["BaseModel", "Examiner", "Exam", "Examinee", "Grade",
           "Question"]


class TestMakerCommand(Cmd):
    """this class implement commandline"""

    prompt = "(test) "

    def do_all(self, line):
        """print all instances based on class name"""
        list_strd_obj = []
        if not line:
            for key, value in storage.all().items():
                list_strd_obj.append(str(value))
        elif line not in classes:
            print("** class doesn't exist **")
        else:
            cls = eval(line)
            for key, value in storage.all(cls).items():
                list_strd_obj.append(str(value))
        print(list_strd_obj)


    def do_create(self, line):
        """create a new instance of the class"""
        validator = TestMakerCommand.line_validator(line, "create")
        if validator == 0:
            validator
        else:
            list_line = line.split()
            cls = eval(list_line[0])
            params = list_line[1:]
            if params:
                dct = {}
                for kwarg in params:
                    key = kwarg.split("=")[0]
                    value = eval(kwarg.split("=")[1])
                    if type(value) is str:
                        value = value.replace("_", " ")
                    dct[key] = value
                new_obj = cls(**dct)
                new_obj.save()
            else:
                new_obj = cls()
                new_obj.save()
            print(new_obj.id)

    def do_destroy(self, line):
        """delete an instance base on class name and id"""
        validator = TestMakerCommand.line_validator(line, "destroy")
        if validator == 0:
            validator
        else:
            list_line = line.split()
            obj_key = list_line[0] + '.' + list_line[1]
            storage.delete(storage.all()[obj_key])
            storage.save()

    def do_quit(self, line):
        """exit the program"""
        return True

    def do_show(self, line):
        """show instance base on class name and id"""
        validator = TestMakerCommand.line_validator(line, "show")
        if validator == 0:
            validator
        else:
            list_line = line.split()
            obj_key = list_line[0] + "." + list_line[1]
            obj = storage.all()[obj_key]
            print(obj)

    def do_update(self, line):
        """update an existing object"""
        validator = TestMakerCommand.line_validator(line, "update")
        if validator == 0:
            validator
        else:
            list_line = line.split()
            obj_key = list_line[0] + "." + list_line[1]
            new_attr = list_line[2]
            value = list_line[3]
            obj_to_dict = storage.all()[obj_key].to_dict()
            obj_to_dict[new_attr] = eval(value)
            updated_obj = eval(list_line[0])(**obj_to_dict)
            updated_obj.save()

    def emptyline(self):
        """Empty line does nothing"""
        pass

    @classmethod
    def line_validator(cls, line, cmd):
        """line validator"""
        list_line = line.split()
        if not line:
            print("** class name missing **")
            return 0
        if list_line[0] not in classes:
            print("** class doesn't exist **")
            return 0
        if cmd == "create":
            return 1
        try:
            id = list_line[1]
        except Exception:
            print("** instance id missing **")
            return 0
        obj_key = list_line[0] + "." + list_line[1]
        if obj_key not in storage.all():
            print("** no instance found **")
            return 0
        if cmd == "update":
            try:
                attr = list_line[2]
            except Exception:
                print("** attribute name missing **")
                return 0
            try:
                value = list_line[3]
            except Exception:
                print("** value missing **")
                return 0
        return 1

    do_EOF = do_quit

if __name__ == "__main__":
    TestMakerCommand().cmdloop()
