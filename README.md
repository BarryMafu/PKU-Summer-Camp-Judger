# Summer Camp Judger

- Creater: BarryMafu
- Time: 25.June.27th
- Copyright: (2025) MizuStudio

### 简介
一个自动化测评程序和一些北京大学夏令营的题目解答

### 使用方法
请您先clone该仓库，然后按照以下步骤编写代码并自行测评。

1. 首先配置题目。请您确保你希望的题目在正确的文件夹当中，此时您的文件结构应该是：
```
Summer Camp 2024/
├── Problem A/
├── Problem B/
└── Problem E/
judge.py
README.md
```
2. 然后填入`time_memory_limit.txt`，里面放置每一道题目限定的时间和内存限制。单位是秒和MB（请提前换算）。值得注意的是，由于个人电脑上会有一些额外的时间开销，所以请您最好在题目的时间要求上**加上1s**或者**乘以2**，空间要求不变。结构是
```
<problem_code> <time_limit(s)> <memory_limit(MB)>
```
此时您的文件结构应该是：
```
Summer Camp 2024/
├── Problem A/
├── Problem B/
├── Problem E/
└── time_memory_limit.txt
judge.py
README.md
```

3. 编写输入数据和答案数据（*目前只支持一个case*），写入`input.txt`和`answer.txt`。此时您的文件结构应该是：
```
Summer Camp 2024/
├── Problem A/
│   ├── input.txt
│   └── answer.txt
├── Problem B/ ...
├── Problem E/ ...
└── time_memory_limit.txt
judge.py
README.md
```

4. 编写您的解答，写入`solution.cpp`，在这当中，您可以通过以下的代码结构进行本地测试。
```cpp
int main(){
    freopen("input.txt", "r", stdin);

    /* Your Code */

    fclose(stdin);
}
```
此时您的文件结构应该是：
```
Summer Camp 2024/
├── Problem A/
│   ├── solution.cpp
│   ├── input.txt
│   └── answer.txt
├── Problem B/ ...
├── Problem E/ ...
└── time_memory_limit.txt
judge.py
README.md
```

5. 更改`judge.py`中您希望批改的年份和问题名字（名字紧凑编写），如下
```python
@dataclass
class Config:
    year: int = 2024
    problems: str = "ABE"
```
然后运行便可以得到最后的结果。