class ExtractError:
    def __init__(self, error_message: dict):
        self.error_message = error_message

    def extract_error(self) -> dict:
        error_dict = {}
        # 提取错误信息并转换为字符串
        for field, error_list in self.error_message.items():
            if error_list and len(error_list) > 0:  # 确保错误列表非空
                error_dict[field] = error_list[0]  # 取第一个错误
        return error_dict
