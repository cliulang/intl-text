import pandas as pd
import jieba
import itertools


class App:
    def __init__(self, *args):
        """
        :param args: index.csv 分词词典txt 分词词典更新flag 初始行数
        :return
        """
        self.csv_file = pd.read_csv(args[0])
        self.txt_path = args[1]
        self.is_update_txt = args[2]
        self.start_line = args[3]
        # update jieba分词词典
        if self.is_update_txt is True:
            self._update_txt()
    
    def _update_txt(self):
        self.csv_file['固有名词'].to_csv(self.txt_path, index=False)
    
    def read_line(self):
        counter = itertools.count(1)
        jieba.load_userdict(self.txt_path)
        with open(r"Localizable_bk.strings", mode="r", encoding='utf-8') as f:
            while True:
                line = next(f)
                count_line = next(counter)
                if count_line < self.start_line:
                    continue
                else:
                    this_line = line.strip()
                    if len(this_line) != 0 and this_line.startswith("\"") and not this_line.endswith("//pass"):
                        print(this_line)
                        jieba_cut = [i for i in jieba.cut_for_search(this_line.split("=")[0])]
                        self.check_in_index_file(jieba_cut)
                        cmd_string = "------当前行数：{},  q键中止，其他任意键继续------\n".format(count_line)
                        a = input(cmd_string)
                        if a in ("q", "Q", "ｑ", "Ｑ"):
                            print("bye")
                            return
    
    def check_in_index_file(self, cut_list):
        # 去重
        cut_set = set(cut_list)
        cut_list = sorted(list(cut_set), key=cut_list.index)
        for i in cut_list:
            result = self.csv_file[self.csv_file["固有名词"] == i]
            if not result.empty:
                print(result)
    

if __name__ == "__main__":
    # args: index文件path 分词词典path 分词词典txt更新flag 初始行数
    a = App("index.csv", "word_for_cut.txt", True, 845)
    a.read_line()
    
