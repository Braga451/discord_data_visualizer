import csv, json, os

class RetriveData:
    def __init__(self, path : str = ""):
        if(path == ""):
            raise NameError("Path not defined!")
        else:
            self.work_path = os.getcwd()
            self.path = path
            self.path_chats = list()
            self.int_total_chats = len(os.listdir(f"{path}/messages")) - 1
            
    def _getPathChats(self) -> None:
        os.chdir(self.path + "/messages")
        index_json = None
        with open("index.json", "r") as indexJson:
            index_json = json.load(indexJson)
            indexJson.close()
        for chat in os.listdir():
            if(chat != "index.json"):
                self.path_chats.append(self._returnChatWithPath(chat, index_json))

    def _returnChatWithPath(self, chat_path : str = "", index_json : dict = {}) -> dict:
        dict_name_path = dict()
        channel_json = None
        guild_name = ""
        name = ""
        channel_id = ""
        os.chdir(f"{os.getcwd()}/{chat_path}")
        with open("channel.json", "r") as channel:
            channel_json = json.load(channel)
            channel.close()
            if(channel_json.get("guild") is None):
                channel_id = channel_json.get("id")
                name = index_json.get(channel_id).replace("Direct Message with ", "") if index_json.get(channel_id) != None else "null"
                dict_name_path["name"] = name
                dict_name_path["path"] = os.getcwd()
            else:
                guild_name = channel_json.get("guild").get("name")
                name = channel_json.get("name")
                dict_name_path["name"] = f"Server: {guild_name} - Chat: {name}"
                dict_name_path["path"] = os.getcwd()
            os.chdir("../")
            return dict_name_path

    def _returnMessagesByPath(self, path : str = "") -> list:
        messages_list = list()
        csv_file = None
        os.chdir(path)
        with open("messages.csv", "r") as messages:
            csv_file = list(csv.reader(messages, delimiter= ","))
            for rows in csv_file[1::]:
                messages_list.append(rows)
            messages.close()
        os.chdir(self.work_path)
        return messages_list

