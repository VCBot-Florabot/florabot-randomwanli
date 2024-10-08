import random,json,base64

flora_api = {}  # 顾名思义,FloraBot的API,载入(若插件已设为禁用则不载入)后会赋值上


def occupying_function(*values):  # 该函数仅用于占位,并没有任何意义
    pass


send_msg = occupying_function


def init():  # 插件初始化函数,在载入(若插件已设为禁用则不载入)或启用插件时会调用一次,API可能没有那么快更新,可等待,无传入参数
    global send_msg
    print(flora_api)
    send_msg = flora_api.get("SendMsg")
    #print("FloraBot插件模板 加载成功")


def api_update_event():  # 在API更新时会调用一次(若插件已设为禁用则不调用),可及时获得最新的API内容,无传入参数
    #print(flora_api)
    pass


def event(data: dict):  # 事件函数,FloraBot每收到一个事件都会调用这个函数(若插件已设为禁用则不调用),传入原消息JSON参数
    print(data)
    uid = data.get("user_id")  # 事件对象QQ号
    gid = data.get("group_id")  # 事件对象群号
    mid = data.get("message_id")  # 消息ID
    msg = data.get("raw_message")  # 消息内容
    try:
        global ws_client
        global ws_server
        send_address = data.get("SendAddress")
        ws_client = send_address.get("WebSocketClient")
        ws_server = send_address.get("WebSocketServer")
    except:
        ws_server=None
        ws_client=None
        pass
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        #print(uid, gid, mid, msg)
        if msg == "#随机梨梨":
            send_compatible(msg=f'[CQ:at,id={uid}]\n[CQ:image,file={get_random()}]',uid=uid,gid=gid)
def get_random(type:str=None):
    """
    返回随机图片(默认json文本,可307)
    """
    types=type
    if type is None or type not in ['jpg','png','gif']:
        types=random_type()
    endnum=check_type(types)
    num=random.randint(1,endnum)
    file_url=f"file://{flora_api.get('FloraPath')}/{flora_api.get('ThePluginPath')}/res/{types}/{num}.{types}"
    return file_url

def random_type():
    """
    随机返回图片类型
    """
    types=random.randint(1,3)
    return ['png', 'gif', 'jpg'][types - 1]
def check_type(type:str):
    num_group=json.load(open(f"./{flora_api.get('ThePluginPath')}/res/file.json",mode="r",errors="ignore"))
    return num_group[type]

def image_to_base64(image_path:str):
    if image_path.startswith("file://"):
        image_path=image_path.replace("file://","")
    with open(image_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        return f'base64://{base64_data}'
    
    
def send_compatible(msg:str,uid:str|int,gid: str|int,mid:int|str=None):  #兼容性函数,用于兼容旧版本API(请直接调用本函数)
    if flora_api.get("FloraVersion") == 'v1.01': #旧版本API
        send_msg(msg=msg,gid=gid,uid=uid,mid=mid)
    else:
        send_type=flora_api.get("ConnectionType")
        send_address=flora_api.get("FrameworkAddress")
        send_msg(msg=msg,gid=gid,uid=uid,mid=mid,send_type=send_type,ws_client=ws_client,ws_server=ws_server)