# import matplotlib.pyplot as plt
# import pandas as pd
# from matplotlib.font_manager import FontProperties
# from matplotlib.colors import LinearSegmentedColormap
#
# # 设置中文字体支持
# plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']
# plt.rcParams['axes.unicode_minus'] = False
#
# # 创建数据
# data = {
#     "插件名": [
#         "DreamAction", "DreamAntiFake", "DreamAntiFly", "DreamCountdown",
#         "DreamExchange", "DreamRecipe", "DreamRobot", "DreamShowcase",
#         "DreamSpawners", "DreamTimer", "Legendinlay", "LegendJewelry",
#         "LegendMaid", "LegendStrengthen", "LegendTalent", "LegendTome",
#         "HTAssist", "HTIdentity"
#     ],
#     "中文名": [
#         "梦交互", "梦反压测", "梦飞控", "梦计时", "梦兑换", "梦配方", "梦机器人",
#         "梦展柜(页面)", "梦刷怪点", "梦调度", "传奇宝石", "传奇饰品", "传奇女仆",
#         "传奇强化", "传奇天赋", "传奇图鉴", "喵娃辅助", "喵娃鉴定"
#     ],
#     "售价": [
#         "FL150", "免费", "FL50", "FL300", "FL350", "FL200", "免费", "FL250",
#         "免费", "FL100", "158", "88", "免费", "128", "58", "50", "免费", "128"
#     ],
#     "绑定信息": [
#         "暂未绑定", "暂未绑定", "暂未绑定", "暂未绑定", "暂未绑定", "暂未绑定",
#         "暂未绑定", "电信", "电信", "暂未绑定", "电信", "暂未绑定", "暂未绑定",
#         "暂未绑定", "暂未绑定", "暂未绑定", "暂未绑定", "电信"
#     ]
# }
#
# # 创建DataFrame
# df = pd.DataFrame(data)
#
# # 添加底部统计信息
# stats = {
#     "项目": ["QQ", "消费额", "贵族等级", "插件数量", "当前排名"],
#     "值": ["3014617667", "¥610.0", "5级", "18", "305"]
# }
# stats_df = pd.DataFrame(stats)
#
# # 创建图形
# fig = plt.figure(figsize=(12, 10), facecolor='#0C0C0C')
# ax = plt.subplot(111)
# ax.set_facecolor('#0C0C0C')
#
# # 隐藏坐标轴
# ax.axis('off')
#
# # 创建自定义深色渐变颜色映射
# colors = ["#1a1a1a", "#2d2d2d", "#1a1a1a"]
# cmap = LinearSegmentedColormap.from_list("custom_dark", colors, N=256)
#
# # 绘制主表格
# table = plt.table(
#     cellText=df.values,
#     colLabels=df.columns,
#     cellLoc='center',
#     loc='center',
#     colColours=['#333333']*4,
#     cellColours=[[cmap(0.2)]*len(df.columns)]*len(df),
#     bbox=[0, 0.2, 1, 0.7]
# )
#
# # 设置表格文本样式
# for key, cell in table.get_celld().items():
#     cell.set_text_props(color='white', fontsize=11)
#     cell.set_edgecolor('#444444')
#     if key[0] == 0:  # 表头行
#         cell.set_text_props(weight='bold', color='#FFD700')
#         cell.set_facecolor('#222222')
#
# # 绘制统计信息表格
# stats_table = plt.table(
#     cellText=stats_df.values,
#     colLabels=stats_df.columns,
#     cellLoc='center',
#     loc='bottom',
#     colColours=['#333333']*2,
#     cellColours=[[cmap(0.1)]*2]*len(stats_df),
#     bbox=[0.25, -0.15, 0.5, 0.2]
# )
#
# # 设置统计表格样式
# for key, cell in stats_table.get_celld().items():
#     cell.set_text_props(color='white', fontsize=12)
#     cell.set_edgecolor('#444444')
#     if key[0] == 0:  # 表头行
#         cell.set_text_props(weight='bold', color='#FFD700')
#         cell.set_facecolor('#222222')
#
# # 添加标题
# plt.suptitle('插件信息概览',
#             fontsize=18,
#             color='#FF9900',
#             y=0.92,
#             fontweight='bold')
#
# # 添加水印
# plt.figtext(0.5, 0.05, "Created with Python Matplotlib",
#            ha='center',
#            color='#555555',
#            fontsize=10,
#            alpha=0.7)
#
# # 调整布局
# plt.tight_layout(rect=[0, 0, 1, 0.95])
#
# # 保存图片
# plt.savefig('plugin_info_dashboard.png', dpi=120, facecolor=fig.get_facecolor())
# plt.show()
