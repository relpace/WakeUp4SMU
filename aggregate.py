from typing import Iterable, Tuple, Dict

from models import SingleEvent, AggregatedCourse

def make_key(e:SingleEvent) -> Tuple[str, str, str, str, Tuple[int, int], int]:
    return (
        e.kcmc,
        e.jxcdmc,
        e.jxhjmc,
        e.teaxms,
        (e.ps, e.pe),
        e.xq
    )

def aggregate(events: Iterable[SingleEvent]) -> list[AggregatedCourse]:
    index: Dict[Tuple[str, str, str, str, Tuple[int, int], int], AggregatedCourse] = {}
    for e in events:
        key = make_key(e)
        week = e.zc
        ac = index.get(key)
        if ac is None:
            ac = AggregatedCourse(
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
                zc=set()

            )
            index[key] = ac
        ac.add_zc(week)
    return list(index.values())