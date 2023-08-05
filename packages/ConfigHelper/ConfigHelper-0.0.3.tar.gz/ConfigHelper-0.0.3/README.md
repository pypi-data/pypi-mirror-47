# ConfigHelper
Can use it to save or recall preferences from Python.
 - Copyright (c) 2019 [InfoLab](http://infolab.kunsan.ac.kr) ([Donggun LEE](http://duration.digimoon.net/))
 - How to install
    ```bash
    pip install ConfigHelper
    ```
    - Other version
        ```bash
        # 0.0.3
        pip install ConfigHelper==0.0.3
        ```
 - Functions
    ```python
    config = ConfigHelper(data:dict)
    config = ConfigHelper(path:str) # URL is not supported.
    config = ConfigHelper(cls:type) # Class
    config = ConfigHelper(obj) # is not None

    # Returns the value.
    def getValue(key:str):
        return Value

    # Modify or add new value. 
    def setValue(key:str, value:object):
        return None

    # Create New Object. (Init Variable)
    def newObject(cls:Class):
        return Object

    # Put a value in Object
    def setObject(obj:Object):
        pass

    # Return as "Dictionary".
    def toDict():
        return Dictionary

    # Return as "JSON".
    def toJSON():
        return String(=JSON)

    # Return as "File".
    def toFile(path:string):
        return file
    ```

 - How to use

   - Test Class
        ```python
        # Test Class
        class Test:
            def __init__(self):
                self.name = "Donggun LEE"
                self.age = 24
            
            def __str__(self):
                return "name : {}, age : {}".format(self.name, self.age)
        ```
    - Import ConfigHelper
        ```python
        from ConfigHelper import Config
        ```
    - Config None Example
        ```python
        # Config None Example
        print("Config None Example")
        cfg_none = Config()
        cfg_none.setValue("Version", "0.0.1")
        cfg_none.setValue("isTemporary", 0)
        cfg_none.setValue("isUserMode", 1)

        print(cfg_none.isTemporary)
        """
            0
        """
        print(cfg_none.Version)
        """
            0.0.1
        """

        print(cfg_none.toJSON())
        """
            {
                "Version": "0.0.1",
                "isTemporary": 0,
                "isUserMode": 1
            }
        """

        test = Test()
        print(test)
        """
            name : Donggun LEE, age : 24
        """
        cfg_none.setValue("name", "LEE Donggun")
        cfg_none.setObject(test)
        print(test)
        """
            name : LEE Donggun, age : 24
        """
        try:
            print(test.Version)
            """
            """
        except Exception as e:
            print(e)
            """
                'Test' object has no attribute 'Version'
            """

        print(cfg_none.Version)
        """
            0.0.1
        """

        print(cfg_none.toDict()['Version'])
        """
            0.0.1
        """

        cfg_none.toFile("d:/a/b/c/d/e/f/config.json")
        ```
     - Config Dictionaray Example
        ```python
        # Config Dictionaray Example
        print("Config Dictionaray Example")

        cfg_dict = Config({"name":"LEE Donggun", "age":40})
        print(cfg_dict)
        """
            {
                "age": 40,
                "name": "LEE Donggun"
            }
        """
        test = cfg_dict.newObject(Test)
        print(test)
        """
            name : LEE Donggun, age : 40
        """
        cfg_dict.setValue("age",70)
        cfg_dict.setObject(test)
        print(test)
        """
            name : LEE Donggun, age : 70
        """
        ```
     - Config File Example
        ```python
        # Config File Example
        print("Config File Example")
        cfg_file = Config("d:/a/b/c/d/e/f/config.json")
        print(cfg_file)
        """
        {
                "Version": "0.0.1",
                "isTemporary": 0,
                "isUserMode": 1,
                "name": "LEE Donggun"
        }
        """
        ```
     - Config Class Example
        ```python
        # Config Class Example
        print("Config Class Example")

        cfg_class = Config(Test)
        print(cfg_class)
        """
            {
                "age": 24,
                "name": "Donggun LEE"
            }
        """
        ```
     - Config Object Example
        ```python
        # Config Object Example
        print("Config Object Example")

        cfg_obj = Config(Test())
        print(cfg_class)
        """
            {
                "age": 24,
                "name": "Donggun LEE"
            }
        """
        ```