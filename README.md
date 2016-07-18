# simple linux kernel

根据config文件中的定义，分析Linux Kernel代码，剔除无用的文件。

0. 编译Linux Kernel
2. 根据编译出的`.o`文件，找到对应的`.c`或`.S`文件
1. 根据config文件中的`CONFIG_XXX`定义，预处理`.c`和`.S`文件
5. 剔除原文件中多余的`CONFIG_YYY`
3. 分析`.c`或`.S`文件，找到其依赖的`.h`或`.c`文件
4. 删除所有没有用到的`.c`, `.S`, `.h`文件

