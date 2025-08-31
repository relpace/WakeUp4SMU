from dataclasses import dataclass
from typing import Tuple, Dict, List, Set, Iterable, Optional
@dataclass(frozen=True)
class SingleEvent:
    kcmc: str  # 课程名称
    jxcdmc: str # 教学场地名称
    jxhjmc: str # 教学环节（理论/实验/自主学习）
    teaxms: str # 教师姓名
    xq: int # 星期几
    xs: str # 学时
    qssj: str # 起始时间
    jssj: str # 结束时间
    ps: int # 第几节开始
    pe: int # 第几节结束
    zc: int # 周次

@dataclass
class AggregatedCourse:
    kcmc: str # 课程名称
    jxcdmc: str # 教学场地名称
    jxhjmc: str # 教学环节（理论/实验/自主学习）
    teaxms: str # 教师姓名
    xq: int # 星期几
    xs: str # 学时
    qssj: str # 起始时间
    jssj: str # 结束时间
    ps: int # 第几节开始
    pe: int # 第几节结束
    zc: List[int]  # 周次
    id: int

    def add_zc(self,zc: int):
        self.zc.append(zc)
