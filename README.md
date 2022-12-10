## 人名生成器（起名器）
为了方便广大中文小说作者起名，本人设计了这个工具，使用方便，效果不错。

## 安装
```
pip install -r requirements.txt
```
## 使用
```
usage: name_generator.py [-h] [--sex SEX] [--num NUM] [--length LENGTH]

optional arguments:
  -h, --help       show this help message and exit
  --sex SEX        0 means woman, 1 means man.
  --num NUM        Number of names. Must be in [2, 100]
  --length LENGTH  Number of characters of name. 2/3/0 is allowed. 0 means 2 or 3 are both ok
```
例如生成60个三字女名
```
>python name_generator.py --sex 0 --num 60 --length 3
孟霞飞  钟铭悦  郑莉萍  刘松楠  孟可红  矫瑛玲
史芸飞  宋惠宁  张华芬  夏里莎  袁媛冬  索斓燕
魏华杏  李珠香  张义贞  张林芬  齐君丽  冀玲利
龚铭珍  陈丹铭  薛锋惠  富仙文  信树叶  蒋聪卓
许娟英  李陈婧  虞颖花  倪琴花  余萍萍  阮昭昀
吴玉惠  宋玲清  魏国红  骆秋蓉  刘虹竹  蔡玲俐
李鑫英  朱凤云  赖默思  贾景芸  田卿梅  穆馨遥
闵闵钰  尹虹霞  杨秀君  胡鹤晴  姚东芳  王燕宏
许睿芃  杨方芳  葛飘扬  宋珍妮  苏苹平  时坤莲
谢华琪  顾群惠  张艳春  林冬妮  乐育珍  谢茹英
```
生成30个两字男名
```
>python name_generator.py --sex 1 --num 30 --length 2 
吴川    王爷    孙航    费翔    何军    施勉
纪忠    翁驰    李军    罗军    逯媲    朱涛
侯政    纪东    曹松    宋彬    郭强    姜生
丁万    彭师    靳良    吴湖    曹庚    赵鹤
唐兴    张雄    严锋    吴昱    熊军    花和
```
生成30个两字/三字混合的女名
```
>python name_generator.py --sex 0 --num 30 --length 0 
薛红    房珍    骆沁冉  何兰兰  高伟芹  林英歌
葛潭湘  董伟琼  张莉    高让兰  吕琴素  邵志佳
李亚    肖俊红  田惠    李云玲  黄裳群  屈兰
余青春  李丽达  孟衡丽  袁静    国翔凤  杨雄英
冯娟娟  陈晨    荣英斯  李娜欣  许霞    杨菁菁
```
## 原理
分成两部分
- 起名器：基于频率统计的马尔科夫链
- 性别分类器：贝叶斯分类器

## 安利
顺便安利自己的小说网站
[化鼠的图书馆](https://xn--cjrq8lbyi02cyu8h.com/)
[Pixiv个人页](https://www.pixiv.net/users/48925041)