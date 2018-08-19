# -*-coding: utf-8 -*-

from Linephu.linepy import *
from Linephu.akad.ttypes import *
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse, timeit
#==============================================================================#
botStart = time.time()

cl = LINE()
cl.log("Auth Token : " + str(cl.authToken))

#ki = LINE()
#ki.log("Auth Token : " + str(ki.authToken))

#k1 = LINE()
#k1.log("Auth Token : " + str(k1.authToken))

#k2 = LINE()
#k2.log("Auth Token : " + str(k2.authToken))

clMID = cl.profile.mid
#AMID = ki.profile.mid
#BMID = k1.profile.mid
#CMID = k2.profile.mid

#KAC = [cl,ki,k1,k2]
#Bots = [clMID,AMID,BMID,CMID]

clProfile = cl.getProfile()
#kiProfile = ki.getProfile()
#k1Profile = k1.getProfile()
#k2Profile = k2.getProfile()
lineSettings = cl.getSettings()
#kiSettings = ki.getSettings()
#k1Settings = k1.getSettings()
#k2Settings = k2.getSettings()

oepoll = OEPoll(cl)
#oepoll1 = OEPoll(ki)
#oepoll2 = OEPoll(k1)
#oepoll3 = OEPoll(k2)
#==============================================================================#
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
banOpen = codecs.open("ban.json","r","utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)
ban = json.load(banOpen)

msg_dict = {}
bl = [""]

#==============================================================================#
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = ban
        f = codecs.open('ban.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def helpmessage():
    helpMessage = """╔══════════════
╠♥ ✿✿✿興の特製防翻半垢 ✿✿✿ ♥
║
╠══✪〘 Help Message 〙✪═══
║
╠✪〘 Help 〙✪══════════
╠➥ Help 查看指令
║
╠✪〘 Status 〙✪════════
╠➥ Restart 重新啟動
╠➥ Save 儲存設定
╠➥ Runtime 運作時間
╠➥ Speed 速度
╠➥ Set 設定
╠➥ About關於本帳
║
╠✪〘 Settings 〙✪═══════
╠➥ ReRead On/Off 查詢收回
╠➥ Share On/Off 公開/私人
╠➥ Pro On/Off 所有保護
╠➥ Protect On/Off 踢人保護
╠➥ QrProtect On/Off 網址保護
╠➥ Invprotect On/Off 邀請保護
║
╠✪〘 Blacklist 〙✪═══════
╠➥ Ban @ 加入黑單
╠➥ Unban @ 取消黑單
╠➥ Banlist 查看黑單
╠➥ CleanBan 清空黑單
╠➥ Nkban 踢除黑單
║
╠✪〘 Group 〙✪════════
╠➥ Nk @ 單、多踢
╠➥ Zk 踢出0字元
╠➥ Cancel 取消所有邀請
╠➥ Ri @ 來回機票
╠➥ Tagall 標註全體
╠➥ Setread 已讀點設置
╠➥ Cancelread 取消偵測
╠➥ Checkread 已讀偵測
║
╠✪〘 Admin 〙✪═════════
╠➥ Adminadd @ 新增權限
╠➥ Admindel @ 刪除權限
╠➥ Adminlist 查看權限表
╠
╠✪〘 Invite 〙✪════════
╠➥ Botsadd @ 加入自動邀請
╠➥ Botsdel @ 取消自動邀請
╠➥ Botslist 自動邀請表
╠➥ Join 自動邀請
║
╚═〘 Created By: 興興 〙"""
    return helpMessage
wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
}
setTime = {}
setTime = wait2['setTime']

def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))

admin =['u7760fe50542a165f561fe63f4dada95a',clMID]
owners = ["u7760fe50542a165f561fe63f4dada95a"]
#if clMID not in owners:
#    python = sys.executable
#    os.execl(python, python, *sys.argv)
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 11:
            group = cl.getGroup(op.param1)
            contact = cl.getContact(op.param2)
            if settings["qrprotect"] == True:
                if op.param2 in admin or op.param2 in ban["bots"]:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            if clMID in op.param3:
                group = cl.getGroup(op.param1)
            elif settings["invprotect"] == True:
                if op.param2 in admin or op.param2 in ban["bots"]:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1,[op.param3])
            else:
                group = cl.getGroup(op.param1)
                gInviMids = []
                for z in group.invitee:
                    if z.mid in ban["blacklist"]:
                        gInviMids.append(z.mid)
                if gInviMids == []:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1, gInviMids)
                    cl.sendMessage(op.param1,"被邀請者黑單中...")
        if op.type == 17:
            if op.param2 in admin or op.param2 in ban["bots"]:
                return
            ginfo = str(cl.getGroup(op.param1).name)
            try:
                strt = int(3)
                akh = int(3)
                akh = akh + 8
                aa = """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(op.param2)+"},"""
                aa = (aa[:int(len(aa)-1)])
                cl.sendMessage(op.param1, "歡迎 @wanping 加入"+ginfo , contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
            except Exception as e:
                print(str(e))
        if op.type == 19:
            msg = op.message
            chiya = []
            chiya.append(op.param2)
            chiya.append(op.param3)
            cmem = cl.getContacts(chiya)
            zx = ""
            zxc = ""
            zx2 = []
            xpesan ='警告!'
            for x in range(len(cmem)):
                xname = str(cmem[x].displayName)
                pesan = ''
                pesan2 = pesan+"@x 將"
                xlen = str(len(zxc)+len(xpesan))
                xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                zx2.append(zx)
                zxc += pesan2
            text = xpesan+ zxc + "出群組"
            try:
                cl.sendMessage(op.param1, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
            except:
                cl.sendMessage(op.param1,"Notified kick out from group")
            if op.param2 not in admin:
                if op.param2 in ban["bots"]:
                    pass
                elif settings["protect"] == True:
                    ban["blacklist"][op.param2] = True
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    cl.inviteIntoGroup(op.param1,[op.param3])
                else:
                    cl.sendMessage(op.param1,"")
            else:
                cl.sendMessage(op.param1,"")
        if op.type == 25 or op.type == 26:
            K0 = admin
            msg = op.message
            if settings["share"] == True:
                K0 = msg._from
            else:
                K0 = admin
#        if op.type == 25 :
#            if msg.toType ==2:
#                g = cl.getGroup(op.message.to)
#                print ("sended:".format(str(g.name)) + str(msg.text))
#            else:
#                print ("sended:" + str(msg.text))
#        if op.type == 26:
#            msg =op.message
#            pop = cl.getContact(msg._from)
#            print ("replay:"+pop.displayName + ":" + str(msg.text))
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
            if sender in K0 or sender in owners:
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                    cl.sendContact(to,"u7760fe50542a165f561fe63f4dada95a")
#==============================================================================#
                elif text.lower() == 'speed':
                    start = time.time()
                    cl.sendMessage(to, "檢查中...")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)) + "秒")
                elif text.lower() == 'save':
                    backupData()
                    cl.sendMessage(to,"儲存設定成功!")
                elif text.lower() == 'restart':
                    cl.sendMessage(to, "重新啟動中...")
                    time.sleep(5)
                    cl.sendMessage(to, "重啟成功，請重新登入")
                    restartBot()
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    cl.sendMessage(to, "系統已運作 {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        owner ="u7760fe50542a165f561fe63f4dada95a"
                        creator = cl.getContact(owner)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        ret_ = "╔══[ 關於使用者 ]"
                        ret_ += "\n╠ 使用者名稱 : {}".format(contact.displayName)
                        ret_ += "\n╠ 群組數 : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ 好友數 : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ 已封鎖 : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ 關於本bot ]"
                        ret_ += "\n╠ 版本 : 最新"
                        ret_ += "\n╠ 製作者 : {}".format(creator.displayName)
                        ret_ += "\n╚══[ 感謝您的使用 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == 'set':
                    try:
                        ret_ = "╔══[ 狀態 ]"
                        if settings["protect"] ==True: ret_+="\n╠ Protect ✅"
                        else: ret_ += "\n╠ Protect ❌"
                        if settings["qrprotect"] ==True: ret_+="\n╠ QrProtect ✅"
                        else: ret_ += "\n╠ QrProtect ❌"
                        if settings["invprotect"] ==True: ret_+="\n╠ InviteProtect ✅"
                        else: ret_ += "\n╠ InviteProtect ❌"
                        if settings["reread"] ==True: ret_+="\n╠ Reread ✅"
                        else: ret_ += "\n╠ Reread ❌"
                        if settings["share"] ==True: ret_+="\n╠ Share ✅"
                        else: ret_ += "\n╠ Share ❌"
                        ret_ += "\n╚══[ Finish ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'reread on':
                    settings["reread"] = True
                    cl.sendMessage(to,"成功開啟收回查看功能")
                elif text.lower() == 'reread off':
                    settings["reread"] = False
                    cl.sendMessage(to,"成功關閉收回查看功能")
                elif text.lower() == 'protect on':
                    settings["protect"] = True
                    cl.sendMessage(to, "踢人保護開啟")
                elif text.lower() == 'protect off':
                    settings["protect"] = False
                    cl.sendMessage(to, "踢人保護關閉")
                elif text.lower() == 'share on':
                    settings["share"] = True
                    cl.sendMessage(to, "已開啟分享")
                elif text.lower() == 'share off':
                    settings["share"] = False
                    cl.sendMessage(to, "已關閉分享")
                elif text.lower() == 'qrprotect on':
                    settings["qrprotect"] = True
                    cl.sendMessage(to, "網址保護開啟")
                elif text.lower() == 'qrprotect off':
                    settings["qrprotect"] = False
                    cl.sendMessage(to, "網址保護關閉")
                elif text.lower() == 'invprotect on':
                    settings["invprotect"] = True
                    cl.sendMessage(to, "邀請保護開啟")
                elif text.lower() == 'invprotect off':
                    settings["invprotect"] = False
                    cl.sendMessage(to, "邀請保護關閉")
                elif text.lower() == 'pro on':
                    settings["protect"] = True
                    settings["qrprotect"] = True
                    settings["invprotect"] = True
                    cl.sendMessage(to, "踢人保護開啟")
                    cl.sendMessage(to, "網址保護開啟")
                    cl.sendMessage(to, "邀請保護開啟")
                elif text.lower() == 'pro off':
                    settings["protect"] = False
                    settings["qrprotect"] = False
                    settings["invprotect"] = False
                    cl.sendMessage(to, "踢人保護關閉")
                    cl.sendMessage(to, "網址保護關閉")
                    cl.sendMessage(to, "邀請保護關閉")
#==============================================================================#
                elif msg.text.lower().startswith("adminadd "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    admin.append(str(inkey))
                    cl.sendMessage(to, "已獲得權限！")
                elif msg.text.lower().startswith("admindel "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    admin.remove(str(inkey))
                    cl.sendMessage(to, "已取消權限！")
                elif text.lower() == 'adminlist':
                    if admin == []:
                        cl.sendMessage(to,"無擁有權限者!")
                    else:
                        mc = "╔══[ Admin List ]"
                        for mi_d in admin:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
                elif msg.text.lower().startswith("botsadd "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    ban["bots"].append(str(inkey))
                    cl.sendMessage(to, "已加入分機！")
                elif msg.text.lower().startswith("botsdel "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    ban["bots"].remove(str(inkey))
                    cl.sendMessage(to, "已取消分機！")
                elif text.lower() == 'botslist':
                    if ban["bots"] == []:
                        cl.sendMessage(to,"無分機!")
                    else:
                        mc = "╔══[ Inviter List ]"
                        for mi_d in ban["bots"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
                elif text.lower() == 'join':
                    if msg.toType == 2:
                        G = cl.getGroup
                        cl.inviteIntoGroup(to,ban["bots"])
                elif msg.text.lower().startswith("ii "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    cl.createGroup("fuck",[inkey])
                    cl.leaveGroup(op.param1)
#==============================================================================#
                elif msg.text.lower().startswith("nk "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.sendMessage(to,"Fuck you")
                            cl.kickoutFromGroup(msg.to,[target])
                        except:
                            cl.sendMessage(to,"Error")
                
                elif "Zk" in msg.text:
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in admin:
                                pass
                            else:
                                try:
                                    cl.kickoutFromGroup(to,[target])
                                except:
                                    pass

                elif msg.text.lower().startswith("ri "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.sendMessage(to,"來回機票一張ww")
                            cl.kickoutFromGroup(msg.to,[target])
                            cl.inviteIntoGroup(to,[target])
                        except:
                            cl.sendMessage(to,"Error")
                elif text.lower() == 'cancel':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.invitee]
                    for _mid in gMembMids:
                        cl.cancelGroupInvitation(msg.to,[_mid])
                    cl.sendMessage(msg.to,"已取消所有邀請!")
#==============================================================================#
                elif text.lower() == 'tagall':
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        cl.sendMessage(to, "Total {} Mention".format(str(len(nama))))
                elif text.lower() == 'setread':
                    cl.sendMessage(msg.to, "已讀點設置成功")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                    except:
                        pass
                    now2 = datetime.now()
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = datetime.strftime(now2,"%H:%M")
                    wait2['ROM'][msg.to] = {}
                elif text.lower() == "cancelread":
                    cl.sendMessage(to, "已讀點已刪除")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                        del wait2['setTime'][msg.to]
                    except:
                        pass
                elif msg.text in ["checkread","Checkread"]:
                    if msg.to in wait2['readPoint']:
                        if wait2["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait2["ROM"][msg.to].items():
                                chiya += rom[1] + "\n"
                        cl.sendMessage(msg.to, "[已讀順序]%s\n\n[已讀的人]:\n%s\n查詢時間:[%s]" % (wait2['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        cl.sendMessage(msg.to, "請輸入setread")

#==============================================================================#
                elif msg.text.lower().startswith("ban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ban["blacklist"][target] = True
                            cl.sendMessage(msg.to,"已加入黑單!")
                            break
                        except:
                            cl.sendMessage(msg.to,"添加失敗 !")
                            break
                elif "Ban:" in msg.text:
                    mmtxt = text.replace("Ban:","")
                    try:
                        ban["blacklist"][mmtext] = True
                        cl.sendMessage(msg.to,"已加入黑單!")
                    except:
                        cl.sendMessage(msg.to,"添加失敗 !")
                elif msg.text.lower().startswith("unban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del ban["blacklist"][target]
                            cl.sendMessage(msg.to,"刪除成功 !")
                            break
                        except:
                            cl.sendMessage(msg.to,"刪除失敗 !")
                            break
                elif text.lower() == 'banlist':
                    if ban["blacklist"] == {}:
                        cl.sendMessage(msg.to,"無黑單成員!")
                    else:
                        mc = "╔══[ Black List ]"
                        for mi_d in ban["blacklist"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                elif text.lower() == 'nkban':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                    for tag in ban["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendMessage(msg.to,"There was no blacklist user")
                        return
                    for jj in matched_list:
                        cl.kickoutFromGroup(msg.to,[jj])
                    cl.sendMessage(msg.to,"Blacklist kicked out")
                elif text.lower() == 'cleanban':
                    for mi_d in ban["blacklist"]:
                        ban["blacklist"] = {}
                    cl.sendMessage(to, "已清空黑名單")
                elif text.lower() == 'banmidlist':
                    if ban["blacklist"] == {}:
                        cl.sendMessage(msg.to,"無黑單成員!")
                    else:
                        mc = "╔══[ Black List ]"
                        for mi_d in ban["blacklist"]:
                            mc += "\n╠ "+mi_d
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
#==============================================================================#
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
            try:
                msg = op.message
                if settings["reread"] == True:
                    if msg.toType == 0:
                        cl.log("[%s]"%(msg._from)+msg.text)
                    else:
                        cl.log("[%s]"%(msg.to)+msg.text)
                    if msg.contentType == 0:
                        msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                    elif msg.contentType == 7:
                        stk_id = msg.contentMetadata['STKID']
                        msg_dict[msg.id] = {"text":"貼圖id:"+str(stk_id),"from":msg._from,"createdTime":msg.createdTime}
                else:
                    pass
            except Exception as e:
                print(e)

#==============================================================================#
        if op.type == 65:
            print ("[ 65 ] REREAD")
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            timeNow = datetime.now()
                            timE = datetime.strftime(timeNow,"(%y-%m-%d %H:%M:%S)")
                            try:
                                strt = int(3)
                                akh = int(3)
                                akh = akh + 8
                                aa = """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(msg_dict[msg_id]["from"])+"},"""
                                aa = (aa[:int(len(aa)-1)])
                                cl.sendMessage(at, "收回訊息者 @wanping ", contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                            except Exception as e:
                                print(str(e))
                            cl.sendMessage(at,"[收回訊息者]\n%s\n[訊息內容]\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                            cl.sendMessage(at,"/n發送時間/n"+strftime("%y-%m-%d %H:%M:%S")+"/n收回時間/n"+timE)
                            
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print (e)
#==============================================================================#
        if op.type == 55:
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
            try:
                if op.param1 in wait2['readPoint']:
                    Name = cl.getContact(op.param2).displayName
                    if Name in wait2['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += "\n[※]" + Name
                        wait2['ROM'][op.param1][op.param2] = "[※]" + Name
                        print (time.time() + name)
                else:
                    pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
