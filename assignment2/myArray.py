class MyArray:
    def __init__(self, array):
        # check for 2D list
        if all(type(elem) == list for elem in array):
            nested = True
            for i in array:
                # check for numerical nested list elements
                if all(type(val) == int or type(val) == float for val in i):
                    continue
                else:
                    raise TypeError("nested lists must be of numerical type")

            if nested:
                # check for consistent length
                consistent = True
                length = len(array[0])
                for item in array:
                    if len(item) == length:
                        continue
                    else:
                        raise ValueError("nested lists must be of the same length")

                if consistent:
                    # create instance
                    self.array = array
                    self.nested = True
                    self.length = len(self.array)
                    self.nested_len = length

        # check for 1D list types
        elif all(type(elem) == int or type(elem) == float for elem in array):
            # create instance
            self.array = array
            self.nested = False
            self.length = len(self.array)

        else:
            raise TypeError("list elements must be numbers")

    def maximum(self, **kwargs):
        """Returns the maximum value of the array.

           Performs an initial check on 1D or 2D.
           Axis may be supplied for 2D arrays.
           Makes use of the weakly private __maximum method."""

        if not self.nested:
            result = self.__maximum(self.array)

        else:
            if "axis" in kwargs:
                ax = kwargs["axis"]
                if ax == 0:  # vertical axis
                    result = self.array[0]
                    for i, j in enumerate(self.array):  # for each index,value available in outer list
                        for a, b in enumerate(j):  # for each index,value available in inner list
                            if b > result[a]:  # if value is greater than that index of test list
                                result[a] = b  # replace test list value with new value

                elif kwargs["axis"] == 1:  # horizontal axis
                    result = []
                    for i in self.array:
                        result.append(self.__maximum(i))  # get the max value for each nested list

                else:
                    raise ValueError("Axis must be 1 or 0")

            else:
                new_list = []
                for i in self.array:
                    for j in i:
                        new_list.append(j)
                result = self.__maximum(new_list)

        return result

    def minimum(self, **kwargs):
        """Returns the minimum value of the array.

           Performs an initial check on 1D or 2D.
           Axis may be supplied for 2D arrays.
           Makes use of the weakly private __minimum method."""

        if not self.nested:
            result = self.__minimum(self.array)

        else:
            if "axis" in kwargs:
                ax = kwargs["axis"]
                if ax == 0:  # vertical axis
                    result = self.array[0]
                    for i, j in enumerate(self.array):  # for each index,value available in outer list
                        for a, b in enumerate(j):  # for each index,value available in inner list
                            if b < result[a]:  # if value is less than that index of result list
                                result[a] = b  # replace result list value with new value

                elif kwargs["axis"] == 1:  # horizontal axis
                    result = []
                    for i in self.array:
                        result.append(self.__minimum(i))  # get the in value for each nested list

                else:
                    raise ValueError("Axis must be 1 or 0")

            else:
                new_list = []
                for i in self.array:
                    for j in i:
                        new_list.append(j)
                result = self.__minimum(new_list)

        return result

    def mean(self, **kwargs):
        """Returns the mean value of the array.

           Performs an initial check on 1D or 2D."""

        if not self.nested:
            result = self.__mean(self.array)

        else:
            if "axis" in kwargs:
                ax = kwargs["axis"]
                if ax == 0:  # vertical axis
                    result = []
                    for i in range(self.nested_len):
                        new_list = []
                        for j in self.array:
                            new_list.append(j[i])
                        result.append(self.__mean(new_list))

                elif ax == 1:  # horizontal axis
                    result = []
                    for i in self.array:
                        result.append(self.__mean(i))  # get the max value for each nested list

                else:
                    raise ValueError("Axis must be 1 or 0")

            else:
                new_list = []
                for i in self.array:
                    for j in i:
                        new_list.append(j)
                result = self.__mean(new_list)

        return result

    def __maximum(self, arr):
        """Finds max of a 1D object"""

        max_ = 0
        for i in arr:
            if i > max_:
                max_ = i
        return max_

    def __minimum(self, arr):
        """Finds min of a 1D object"""

        min_ = self.__maximum(arr)
        for i in arr:
            if i < min_:
                min_ = i
        return min_

    def __mean(self, arr):
        """Returns the mean of a 1D object"""

        total = 0
        length = len(arr)
        for i in arr:
            total += i
        return total / length

    def copy(self):
        """Produces a copy of an instance"""

        cop = self.array.copy()
        if not nested:
            return MyArray(cop)

        else:
            replica = []
            for i in self.array:
                replica.append(i.copy())
            return MyArray(replica)


    @classmethod
    def zeros(cls, *args):
        """Alt constructor, object contains array of specified number of zeros in 1D or 2D"""

        outer = []

        # if 1D
        if len(args) == 1:
            for i in range(args[0]):
                outer.append(0)

        # if 2D
        elif len(args) == 2:
            for i in range(args[0]):
                inner = []
                for j in range(args[1]):
                    inner.append(0)
                outer.append(inner)

        else:
            raise ValueError("zeros array can be 1D or 2D only")

        return cls(outer)

    def __repr__(self):
        """Represents array in clean format"""

        string = ""

        if not self.nested:
            string += "| "
            for i in self.array:
                string += f"{i} "
            string += "|"

        else:
            for i in self.array:
                string += "| "
                for elem in i:
                    string += f"{elem} "
                string += "|\n"

        return string

    def __setitem__(self, index, new_val):
        """Allows re-assignment of array elements using [] notation"""

        if type(index) == int:
            if not self.nested:
                if type(new_val) == int or type(new_val) == float:
                    self.array[index] = new_val
                else:
                    raise ValueError("1D array elements cannot be replaced by non numerical type")
            else:
                if type(new_val) == list:
                    if len(new_val) == self.nested_len:
                        self.array[index] = new_val
                    else:
                        raise ValueError("nested array replacement must be the same length as original")
                else:
                    raise ValueError("nested array cannot be replaced by non-array type")

        elif type(index) == tuple:
            # if [x,y] notation is attempted on a 1D array
            if not self.nested:
                raise ValueError("array is 1D, nested index unavailable")
            else:
                if type(new_val) == int or type(new_val) == float:
                    self.array[index[0]][index[1]] = new_val
                else:
                    raise ValueError("replacements for nested array elements must be int or float type")

        else:
            raise ValueError("index does not exist")

    def __getitem__(self, index):
        """Allows array elements to be accessed using [] notation.

           Checks that array is 2D before a nested index is attempted"""

        if type(index) == int:
            val = self.array[index]

        elif type(index) == tuple:
            # if [x,y] notation is attempted on a 1D array
            if not self.nested:
                raise ValueError('array is 1D, nested index unavailable')
            else:
                val = self.array[index[0]][index[1]]

        else:
            raise ValueError("index does not exist")

        return val


test2 = MyArray([[12, 3, 4], [5, 6, 7]])
test2[1,0] = 30
print(test2)

