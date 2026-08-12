import { Importance, isDone, type ShoppingList } from './index'

export const travelList: ShoppingList = {
  title: '前置物品清单',
  createdAt: '2026-07-27',
  categories: [
    {
      name: '食品',
      remark: '聚会零食和饮料，注意保质期',
      items: [
        { key:'0',name: '薯片', importance: Importance.Important, remark: '晚上看电影边看边吃',itemState:isDone.Done },
        { key:'1',name: '可乐', importance: Importance.Important, remark: '大家的快乐水' ,itemState:isDone.notDone},
        { key:'2',name: '脆脆鲨', importance: Importance.Unimportant, remark: '可能吃起来比较干',itemState:isDone.notDone },
      ],
    },
    {
      name: '药品',
      remark: '以备不时之需，出发前检查有效期',
      items: [
        { key:'0',name: '创可贴', importance: Importance.Important, remark: '户外活动容易磕碰',itemState:isDone.notDone },
        { key:'1',name: '晕车药', importance: Importance.Unimportant, remark: '路程不远，看情况带',itemState:isDone.notDone },
      ],
    },
    {
      name: '生活用品',
      remark: '日常消耗品，按人头估算数量',
      items: [
        { key:'0',name: '纸巾', importance: Importance.Important, remark: '多带几包，吃零食用',itemState:isDone.notDone },
        { key:'1',name: '垃圾袋', importance: Importance.Important, remark: '保持场地清洁',itemState:isDone.notDone },
        { key:'2',name: '一次性杯子', importance: Importance.Unimportant, remark: '有自带杯的话可以不带' ,itemState:isDone.notDone},
      ],
    },
  ],
}



export const localList: ShoppingList = {
  title: '当地推荐携带特产清单',
  createdAt: '2026-07-27',
  categories: [
    {
      name: '食品',
      remark: '噢噢噢噢噢泉州的好吃的真是太多了',
      items: [
        { key:'0',name: '土笋冻', importance: Importance.Important, remark: '有海虫，是冻的要和蒜蓉酱油一起吃',itemState:isDone.notDone },
        { key:'1',name: '亚润佛饼皮', importance: Importance.Important, remark: '8块钱一个小小的素菜卷',itemState:isDone.notDone },
        { key:'2',name: '蒜蓉枝', importance: Importance.Unimportant, remark: '看起来不怎么样实际上好吃得要死！！！',itemState:isDone.notDone },
      ],
    },
    {
      name: '药品',
      remark: '早6晚12地玩就很开心噢',
      items: [
        { key:'0',name: '创可贴', importance: Importance.Important, remark: '磨脚跟',itemState:isDone.notDone },
        { key:'1',name: '跌打油', importance: Importance.Unimportant, remark: '玩得太过很伤腿',itemState:isDone.notDone },
      ],
    },
    {
      name: '封神榜',
      remark: '这个不能带',
      items: [
        { key:'0',name: '导弹', importance: Importance.Important, remark: '会发射吗就带',itemState:isDone.notDone },
        { key:'1',name: '鞭炮', importance: Importance.Important, remark: '不样放',itemState:isDone.notDone },
        { key:'2',name: '手雷', importance: Importance.Unimportant, remark: '没人陪你玩了',itemState:isDone.notDone },
      ],
    },
  ],
}