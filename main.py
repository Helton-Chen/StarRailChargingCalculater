#!/usr/bin/env python
# coding: utf-8

# In[151]:


#基础数据
import tabulate as tb

A = 20 #释放普攻获得20点能量
E = 30 #释放战技获得30点能量
utimate_reset = 5 #释放终结技后回复5点能量
charging_relic = 0.194 #充能绳-能量回复效率增加19.4%
onwak = 0.05 #翁瓦克-能量回复效率增加5%

relic_description = ["模式","默认","翁瓦克","充能绳","翁瓦克+充能绳"]
relic_mode = [0,onwak,charging_relic,onwak+charging_relic]


# In[152]:


#角色模块

class Pela:
    charging_requirement = 110 #释放终结技所需能量
    additional_charging = 8  #行迹7级，对拥有Debuff目标释放普攻或战技额外回复8点能量，吃回能项链效果。
    
class Silver_wolf:
    charging_requirement = 110 #释放终结技所需能量
    additional_charging = 0


# In[153]:


#光锥模块

class General_weapon:  #默认光锥
    additional_charging = 0

class New_player_mission: #新手任务开始前光锥：攻击减防敌人获得8点能量，吃回能项链效果。
    additional_charging = 8


# In[154]:


#攻击模式模块，暂时弃用
class Attack_mode:
    
    def __init__(self,mode):
        self.mode = mode
        
    def action_point(self,mode):
        action_point = mode.len()
    


# In[195]:


def calculate_charging_cycle(character,weapon=General_weapon):
    
    table = []
    total_additional_charging = character.additional_charging + weapon.additional_charging #计算攻击额外回能

        
    #二动一大
    #AA
    AA_list = ["AA"]
    action_point = 2
    for n in relic_mode:
        charging_level = (A+A+total_additional_charging*(action_point+1))*(1+n)+utimate_reset
        AA_list.append(charging_level)
    table.append(AA_list)
    
    #AE
    AE_list = ["AE"]
    action_point = 2
    for n in relic_mode:
        charging_level = (A+E+total_additional_charging*(action_point+1))*(1+n)+utimate_reset
        AE_list.append(charging_level)
    table.append(AE_list)
    
    #EE
    EE_list = ["EE"]
    action_point = 2
    for n in relic_mode:
        charging_level = (E+E+total_additional_charging*(action_point+1))*(1+n)+utimate_reset
        EE_list.append(charging_level)
    table.append(EE_list)
    
    #三动一大
    #AAA
    AAA_list = ["AAA"]
    action_point = 3
    for n in relic_mode:
        charging_level = (A+A+A+total_additional_charging*(action_point+1))*(1+n)+utimate_reset
        AAA_list.append(charging_level)
    table.append(AAA_list)
    
    #AAE
    AAE_list = ["AAE"]
    action_point = 3
    for n in relic_mode:
        charging_level = (A+A+E+total_additional_charging*(action_point+1))*(1+n)+utimate_reset
        AAE_list.append(charging_level)
    table.append(AAE_list)       
        
    #AEE
    AEE_list = ["AEE"]
    action_point = 3
    for n in relic_mode:
        charging_level = (A+E+E+total_additional_charging*(action_point+1))*(1+n)+utimate_reset
        AEE_list.append(charging_level)
    table.append(AEE_list)       
    
    #EEE
    EEE_list = ["EEE"]
    action_point = 3
    for n in relic_mode:
        charging_level = (E+E+E+total_additional_charging*(action_point+1))*(1+n)+utimate_reset
        EEE_list.append(charging_level)
    table.append(EEE_list)     
    
    #开局放大
    start_list = ["开局打战技后能量"]
    able_list = ["是否支持开局放大"]
    for n in relic_mode:
        start_level = character.charging_requirement/2 #开局充能
        start_charging = start_level+(E+total_additional_charging)*(1+n) #开局放E后充能
        start_list.append(start_charging)
        if start_charging > character.charging_requirement:
            able = "Yes"
            able_list.append(able)
        else:
            able = "No"
            able_list.append(able)  
    table.append(start_list)
    table.append(able_list)
    
    #制表
    print(tb.tabulate(table, headers=relic_description,tablefmt='grid'))
    

    
    


# In[196]:


calculate_charging_cycle(Silver_wolf,New_player_mission) #银狼携带光锥：新手任务开始前


# In[197]:


calculate_charging_cycle(Pela) #佩拉，行迹7级


# In[198]:


calculate_charging_cycle(Pela,New_player_mission) #佩拉，行迹7级，携带光锥：新手任务开始前


# In[ ]:





# In[ ]:




