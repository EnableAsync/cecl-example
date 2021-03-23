from interface import Cecl


class CeclImpl(Cecl):
    """
    此处编写处理代码

    :参数 inputs:
        以字典的形式存储了所有的输入

        默认值： Flask 的 `request.form`

    :类型 inputs: 字典
    """

    def process(self, inputs):
        name = inputs['name']
        return f'Hi {name}, welcome to cecl.'
