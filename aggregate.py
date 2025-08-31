from typing import Iterable, Tuple, Dict
from models import SingleEvent, AggregatedCourse

def make_key(e:SingleEvent) -> Tuple[str, str, str, str, Tuple[int, int], int,int]:
    return (
        e.kcmc,
        e.jxcdmc,
        e.jxhjmc,
        e.teaxms,
        (e.ps, e.pe),
        e.xq,
        e.zc
    )

def seek_key(e:SingleEvent) -> Tuple[str, str, str, str, Tuple[int, int], int,int]:
    return (
        e.kcmc,
        e.jxcdmc,
        e.jxhjmc,
        e.teaxms,
        (e.ps, e.pe),
        e.xq,
        e.zc-1
    )


def aggregate(events: Iterable[SingleEvent]) -> Tuple[Dict, list[AggregatedCourse]]:
    index: Dict[Tuple[str, str, str, str, Tuple[int, int], int,int], AggregatedCourse] = {}
    Course: Dict[str, int] = {}
    idcount = 0
    for e in events:
        key = seek_key(e)
        week = e.zc
        ac = index.get(key)
        id = Course.get(e.kcmc)
        key_old = key
        key = make_key(e)
        if ac is None:
            if id is None:
                id = idcount
                Course[e.kcmc] = id
                idcount += 1
            ac = AggregatedCourse(
                id=id,
                kcmc=e.kcmc,
                jxcdmc=e.jxcdmc,
                jxhjmc=e.jxhjmc,
                teaxms=e.teaxms,
                xq=e.xq,
                xs=e.xs,
                qssj=e.qssj,
                jssj=e.jssj,
                pe=e.pe,
                ps=e.ps,
                zc=list()
            )
            index[key] = ac
        else:
            index[key] = index.pop(key_old)
            ac = index.get(key)
        ac.add_zc(week)


    return Course,list(index.values())