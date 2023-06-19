#!/usr/bin/env python
# coding: utf-8

# In[398]:


#基础数据

from tabulate import tabulate
from math import floor

charging_relic = 0.194 #充能绳-能量回复效率增加19.4%
onwak = 0.05 #翁瓦克-能量回复效率增加5%
relic_description = ["模式","默认","翁瓦克","充能绳","翁瓦克+充能绳"]
relic_modes = [0,onwak,charging_relic,onwak+charging_relic]


# In[415]:


#角色模块
#通用角色模板
class character():

    charging_requirement = 110 #能量上限
    additional_charging = 0 #攻击额外回能
    after_ult_additional_charging = 0 #攻击额外回能：通过伤害型大招触发
    self_recharge_per_action = 0 #每回合自回能
    charging_efficiency = 0 #充能效率
    A = 20 #释放普攻获得20点能量
    E = 30 #释放战技获得30点能量
    utimate_reset = 5 #释放终结技后回复5点能量
    additional_start_charging = 0 #开局额外获得能量

#佩拉
class Peila(character): 
    
    def __init__(self,trace_level=1,soul_level=0):
        self.name = f"佩拉,行迹等级{trace_level}"
        self.charging_requirement = 110 #释放终结技所需能量
        self.soul_level = soul_level
        self.trace_level = trace_level
        self.trace_charging_list = [5,5.5,6,6.5,7,7.5,8.1,8.7,9.3,10,10.5,11]
        self.additional_charging = self.trace_charging_list[self.trace_level-1] 
        self.after_ult_additional_charging = self.additional_charging    

#银狼
class Yinlang(character):
    
    def __init__(self,soul_level=0,trace_level=1):
        self.name = f"{soul_level}命银狼"
        self.charging_requirement = 110 #释放终结技所需能量
        self.soul_level = soul_level
        if self.soul_level >=1: #一魂银狼释放终结技之后，根据目标已有debuff回复能量，最多5*7=35点，此处按35点计算
            self.after_ult_additional_charging = 35
#停云
class Tingyun(character):
    
    def __init__(self,skill=0,soul_level=0,trace_level=1):
        self.name = f"停云,开局释放{skill}次秘技"
        self.skill = skill #开局放几次战技
        self.charging_requirement = 130 #释放终结技所需能量
        self.self_recharge_per_action = 5 #额外能力“亨通”，停云的回合开始时，停云回复5点能量，吃回能效率
        self.additional_start_charging = 50*self.skill #每放一次秘技，开局多50点能量
    
#艾丝妲
class Aisida(character):
    
    def __init__(self,soul_level=0,trace_level=1):
        self.name = f"{soul_level}命艾丝妲"
        self.charging_requirement = 120 #释放终结技所需能量
        self.soul_level = soul_level
        if self.soul_level >=1:  #一魂艾丝妲，战技多一段伤害，回能从30提升到35
            self.E += 5
        if self.soul_level >=4:
            self.charging_efficiency = 0.15  #四魂艾丝妲，被动大于2层时，充能效率提高15%，默认生效
            
#布洛妮娅
class Buluoniya(character):
    
    def __init__(self,soul_level=0,trace_level=1):
        self.name = "布洛妮娅"
        self.charging_requirement = 120 #释放终结技所需能量


# In[400]:


#光锥模块
#通用光锥模板
class weapon:
    name = "未佩戴充能光锥"
    additional_charging = 0 #攻击额外回能
    after_ult_additional_charging = 0 #攻击额外回能：通过伤害型大招触发
    charging_efficiency = 0 #充能效率
    additional_start_charging = 0 #开局额外获得能量

#新手任务开始前：攻击减防敌人获得8点能量，吃回能效果。
class New_player_mission(weapon): 
    name = "新手任务开始前"
    additional_charging = 8
    after_ult_additional_charging = 8

#但战斗还未结束：充能效率提升10%
class Battle_not_end(weapon):  
    name = "但战斗还未结束"
    charging_efficiency = 0.1
    
#轮契&记忆中的模样：攻击减防敌人获得4-8点能量，吃回能效果
class Memory(weapon):
    
    def __init__(self,shadow):
        self.name = f"叠影等级{shadow}轮契/记忆中的模样"
        self.shadow = shadow
        self.additional_charging = 3+self.shadow*1
        self.additional_start_charging = self.additional_charging #开局额外获得能量
    


# In[401]:


#主模块

def cycle(character=character,weapon=weapon):
    
    table = []
    #计算攻击额外回能
    total_additional_charging = character.additional_charging + weapon.additional_charging 
    #计算释放伤害性大招因攻击额外回能所带来的回能
    total_after_ult_additional_charging = character.after_ult_additional_charging+weapon.after_ult_additional_charging 

        
    #二动一大
    #AA
    AA_list = ["AA"]
    action_point = 2
    action_charge = 2*character.A
    for relic_mode in relic_modes:
        relic_mode += (weapon.charging_efficiency+character.charging_efficiency)
        base_charging_level = action_charge+total_additional_charging*action_point+character.self_recharge_per_action*action_point+total_after_ult_additional_charging
        charging_level = floor(base_charging_level*(1+relic_mode)+character.utimate_reset)
        if charging_level >= character.charging_requirement:
            charging_level = '\033[1;32m' + str(charging_level) + '\033[0m'
        AA_list.append(charging_level)
    table.append(AA_list)
    
    #AE
    AE_list = ["AE"]
    action_point = 2
    action_charge = character.A+character.E
    for relic_mode in relic_modes:
        relic_mode += (weapon.charging_efficiency+character.charging_efficiency)
        base_charging_level = action_charge+total_additional_charging*action_point+character.self_recharge_per_action*action_point+total_after_ult_additional_charging
        charging_level = floor(base_charging_level*(1+relic_mode)+character.utimate_reset)
        if charging_level >= character.charging_requirement:
            charging_level = '\033[1;32m' + str(charging_level) + '\033[0m'        
        AE_list.append(charging_level)
    table.append(AE_list)
    
    #EE
    EE_list = ["EE"]
    action_point = 2
    action_charge = 2*character.E
    for relic_mode in relic_modes:
        relic_mode += (weapon.charging_efficiency+character.charging_efficiency)
        base_charging_level = action_charge+total_additional_charging*action_point+character.self_recharge_per_action*action_point+total_after_ult_additional_charging
        charging_level = floor(base_charging_level*(1+relic_mode)+character.utimate_reset)
        if charging_level >= character.charging_requirement:
            charging_level = '\033[1;32m' + str(charging_level) + '\033[0m'
        EE_list.append(charging_level)
    table.append(EE_list)
    
    #三动一大
    #AAA
    AAA_list = ["AAA"]
    action_point = 3
    action_charge = 3*character.A
    for relic_mode in relic_modes:
        relic_mode += (weapon.charging_efficiency+character.charging_efficiency)
        base_charging_level = action_charge+total_additional_charging*action_point+character.self_recharge_per_action*action_point+total_after_ult_additional_charging
        charging_level = floor(base_charging_level*(1+relic_mode)+character.utimate_reset)
        if charging_level >= character.charging_requirement:
            charging_level = '\033[1;32m' + str(charging_level) + '\033[0m'
        AAA_list.append(charging_level)
    table.append(AAA_list)
    
    #AAE
    AAE_list = ["AAE"]
    action_point = 3
    action_charge = 2*character.A+character.E
    for relic_mode in relic_modes:
        relic_mode += (weapon.charging_efficiency+character.charging_efficiency)
        base_charging_level = action_charge+total_additional_charging*action_point+character.self_recharge_per_action*action_point+total_after_ult_additional_charging
        charging_level = floor(base_charging_level*(1+relic_mode)+character.utimate_reset)
        if charging_level >= character.charging_requirement:
            charging_level = '\033[1;32m' + str(charging_level) + '\033[0m'
        AAE_list.append(charging_level)
    table.append(AAE_list)       
        
    #AEE
    AEE_list = ["AEE"]
    action_point = 3
    action_charge = character.A+2*character.E
    for relic_mode in relic_modes:
        relic_mode += (weapon.charging_efficiency+character.charging_efficiency)
        base_charging_level = action_charge+total_additional_charging*action_point+character.self_recharge_per_action*action_point+total_after_ult_additional_charging
        charging_level = floor(base_charging_level*(1+relic_mode)+character.utimate_reset)
        if charging_level >= character.charging_requirement:
            charging_level = '\033[1;32m' + str(charging_level) + '\033[0m'
        AEE_list.append(charging_level)
    table.append(AEE_list)       
    
    #EEE
    EEE_list = ["EEE"]
    action_point = 3
    action_charge = 3*character.E
    for relic_mode in relic_modes:
        relic_mode += (weapon.charging_efficiency+character.charging_efficiency)
        base_charging_level = action_charge+total_additional_charging*action_point+character.self_recharge_per_action*action_point+total_after_ult_additional_charging
        charging_level = floor(base_charging_level*(1+relic_mode)+character.utimate_reset)
        if charging_level > character.charging_requirement:
            charging_level = '\033[1;32m' + str(charging_level) + '\033[0m'
        EEE_list.append(charging_level)
    table.append(EEE_list)     
    
    #开局放大
    start_list = ["开局打战技后能量"]
    able_list = ["是否支持开局放大"]
    for relic_mode in relic_modes:
        relic_mode += (weapon.charging_efficiency+character.charging_efficiency)
        start_level = character.charging_requirement/2 #开局充能
        start_charging = floor(start_level+(character.E+total_additional_charging+weapon.additional_start_charging)*(1+relic_mode)+character.additional_start_charging) #开局放E后充能
        start_list.append(start_charging)
        if start_charging >= character.charging_requirement:
            able = "\033[1;32mYes\033[0m"
            able_list.append(able)
        else:
            able = "\033[1;31mNo\033[0m"
            able_list.append(able)  
    table.append(start_list)
    table.append(able_list)

    #制表
    if weapon.name == "未佩戴充能光锥":
        print(f"以下是<{character.name}><不佩戴充能光锥>的充能明细：")
    else:
        print(f"以下是<{character.name}>佩戴光锥<{weapon.name}>的充能明细：")
    print(tabulate(table, headers=relic_description,tablefmt='grid'))
    

    
    


# In[410]:


cycle(Aisida(4),Memory(2))
cycle(Aisida(1),Memory(5))


# In[411]:


cycle(Yinlang(),New_player_mission) #银狼携带光锥：新手任务开始前
cycle(Yinlang(1))


# In[412]:


cycle(Peila(5)) #佩拉
cycle(Peila(7),New_player_mission) #佩拉，携带光锥：新手任务开始前


# In[413]:


cycle(Tingyun(1),Battle_not_end) #停云
cycle(Tingyun(1))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




