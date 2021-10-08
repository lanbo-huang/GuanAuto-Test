log_path = "D:\Guanauto-test\GuanAuto-Test\log"
class Common():
    #封装日志方法
    def get_logs(self,path = log_path):
        import logging,time
        logs = logging.getLogger()
        logs.setLevel(logging.DEBUG)
        path = path+'/' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.log'
        write_file = logging.FileHandler(path,'a+',encoding='utf-8')
        write_file.setLevel(logging.DEBUG)
        set_logs = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
        write_file.setFormatter(set_logs)

        pycharm_text = logging.StreamHandler()
        pycharm_text.setFormatter(set_logs)
        logs.addHandler(write_file)
        #logs.addHandler(pycharm_text)
        return logs