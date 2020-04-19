# -*- coding: utf-8 -*- 

import pygame
import rospy


from gazebo_msgs.msg import ModelState
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Quaternion


BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# ROS通讯节点 
class Joystick_Controller(object):
    def __init__(self):

        rospy.init_node("joystick_controller_node", anonymous='True')
        self.rate = rospy.Rate(20)

        self.joystick_controller = rospy.Publisher('/joystick_controller', ModelState, queue_size=10)
        self.joystick_state_x = 0
        self.joystick_state_y = 0

    def publish_control(self, data):
        tmp_modelstate = ModelState()
        self.joystick_state_x = data[0]
        self.joystick_state_y = data[1]
        tmp_modelstate.pose.position.x = self.joystick_state_x
        tmp_modelstate.pose.position.y = self.joystick_state_y
        self.joystick_controller.publish(tmp_modelstate)
        

# 新建窗口打印结果
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)
 
    def print_on_screen(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
    
    # 初始化位置
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
    
    # 缩进
    def indent(self):
        self.x += 10
    
    # 取消缩进
    def unindent(self):
        self.x -= 10
    
'''
# Joystick状态

# JOYAXISMOTION 
# JOYBALLMOTION 
# JOYBUTTONDOWN 
# JOYBUTTONUP 
# JOYHATMOTION

# 按键上下
# if event.type == pygame.JOYBUTTONDOWN:
#     print("Joystick button pressed.")
# if event.type == pygame.JOYBUTTONUP:
#     print("Joystick button released.")
# joystick轴运动
# if event.type == pygame.JOYAXISMOTION:
#     print("Joystick axis moved.")
# if event.type == pygame.JOYBALLMOTION:
#     print("Joystick ball moved.")
# 控制pad，+-1表示
# if event.type == pygame.JOYHATMOTION:
#     print("Joystick hat moved.")
'''


'''
My Nintendo Switch Pro Controller Parameters

axis 0, 1 
max_axis_x = 0.678192138672
min_axis_x = -0.874969482422
max_axis_y = 0.973937988281
min_axis_y = -0.706390380859

axis 2, 3 
max_axis_x = 0.705108642578
min_axis_x = -0.917938232422
max_axis_y = 0.955688476562
min_axis_y = -0.721771240234

max_axis_x = -9
max_axis_y = -9
min_axis_x = 9
min_axis_y = 9

'''
# =================================================================================

def main():
    pygame.init()
    
    # 用于归一化输出的参数
    max_axis_x = 0.705108642578
    min_axis_x = -0.917938232422
    max_axis_y = 0.955688476562
    min_axis_y = -0.721771240234

    # length_x = max_axis_x - min_axis_x
    # length_y = max_axis_y - min_axis_y

    # mid_x = max_axis_x - length_x / 2
    # mid_y = max_axis_y - length_y / 2

    # 窗口初始化
    size = [400, 600]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Switch Pro Controller")
 
    # 循环标志，pygame.QUIT前不停止循环
    done = False
 
    # 控制窗口刷新率
    clock = pygame.time.Clock()
 
    # 初始化joysticks & print
    pygame.joystick.init()
    textPrint = TextPrint()
    controller = Joystick_Controller()


    while done==False:
        # 手柄事件处理
        for event in pygame.event.get(): # 事件发生
            if event.type == pygame.QUIT: # 停止
                done=True # 退出循环
        
    
        # 清屏
        screen.fill(WHITE)
        textPrint.reset()
    
        # joysticks 数目
        joystick_count = pygame.joystick.get_count()
    
        textPrint.print_on_screen(screen, "Number of joysticks: {}".format(joystick_count) )
        textPrint.indent()
        
        # ========== 所有设备 ==========
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
        
            textPrint.print_on_screen(screen, "Joystick {}".format(i))
            textPrint.indent()
        
            # ========== 设备名字 ==========
            name = joystick.get_name()
            textPrint.print_on_screen(screen, "Joystick name: {}".format(name))
            
            # ========== 轴 ==========
            axes = joystick.get_numaxes()
            textPrint.print_on_screen(screen, "Number of axes: {}".format(axes))
            textPrint.indent()
            
            for i in range( axes ):
                axis = joystick.get_axis(i)
                textPrint.print_on_screen(screen, "Axis {} value: {:>7.3f}".format(i, axis)) # {:>7.3f}空格填充至7字符长度，右对齐，精度三位
            
            axis_x = joystick.get_axis(2)
            axis_y = joystick.get_axis(3)
            
            # 记录joystick初始偏置
            if max_axis_x < axis_x:
                max_axis_x = axis_x
            if max_axis_y < axis_y:
                max_axis_y = axis_y
            if min_axis_x > axis_x:
                min_axis_x = axis_x
            if min_axis_y > axis_y:
                min_axis_y = axis_y

            # textPrint.print_on_screen(screen, "max_axis_x : {}".format(max_axis_x))
            # textPrint.print_on_screen(screen, "min_axis_x : {}".format(min_axis_x))
            # textPrint.print_on_screen(screen, "max_axis_y : {}".format(max_axis_y))
            # textPrint.print_on_screen(screen, "min_axis_y : {}".format(min_axis_y))
            
            # -1 => +1  left => right  up => down  
            if axis_x >= 0.0:
                normalized_axis_x = axis_x / max_axis_x
            elif axis_x < 0.0:
                normalized_axis_x = - axis_x / min_axis_x
            
            if axis_y >= 0.0:
                normalized_axis_y = axis_y / max_axis_y
            elif axis_y < 0.0:
                normalized_axis_y = - axis_y / min_axis_y

            normalized_axis_x = round(normalized_axis_x, 4)
            normalized_axis_y = - round(normalized_axis_y, 4) # 取反，坐标系为正方向

            textPrint.print_on_screen(screen, "normalized_axis_x : {}".format(normalized_axis_x))
            textPrint.print_on_screen(screen, "normalized_axis_y : {}".format(normalized_axis_y))

            controller.publish_control([normalized_axis_x, normalized_axis_y])
            textPrint.unindent()
                
            # # ========== 按键 ==========
            # buttons = joystick.get_numbuttons()
            # textPrint.print_on_screen(screen, "Number of buttons: {}".format(buttons))
            # textPrint.indent()
    
            # for i in range( buttons ):
            #     button = joystick.get_button(i)
            #     textPrint.print_on_screen(screen, "Button {:>2} value: {}".format(i,button))
            # textPrint.unindent()
                
            # # ========== Hat ==========
            # hats = joystick.get_numhats()
            # textPrint.print_on_screen(screen, "Number of hats: {}".format(hats))
            # textPrint.indent()
    
            # for i in range( hats ):
            #     hat = joystick.get_hat(i)
            #     textPrint.print_on_screen(screen, "Hat {} value: {}".format(i, str(hat)))
            # textPrint.unindent()
            
        
        # 刷新
        pygame.display.flip()
    
        # 刷新频率
        clock.tick(20)
        
    # 退出
    pygame.quit ()

if __name__ == "__main__":
    main()

