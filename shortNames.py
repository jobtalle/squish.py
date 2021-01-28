class ShortNames:
    def __init__(self):
        self.__name_list = ['a']

    def __increment(self, at):
        """ Increment the name
        :param at: The index in the list to increment
        """

        if at == -1:
            self.__name_list.append('a')
        else:
            char = self.__name_list[at]

            if char == 'z':
                self.__name_list[at] = 'A'
            elif char == 'Z':
                self.__name_list[at] = 'a'
                self.__increment(at - 1)
            else:
                self.__name_list[at] = chr(ord(char) + 1)

    def get_name(self):
        """ Get a new unique name

        :return: A new unique name
        """
        name = ''.join(self.__name_list)

        self.__increment(len(self.__name_list) - 1)

        return name
